#!/usr/bin/env python3
"""J.A.R.V.I.S. Live Fire Protocol — OWASP ZAP orchestration client.

Runs headless OWASP ZAP (daemon / Docker mode) against an active local or
explicitly-authorized staging endpoint, harvests JSON alerts, maps alert URLs
back to local source route definitions, and emits a normalized JSON report
suitable for the Live Fire Protocol skill
(`.jarvis/skills/live-fire-protocol.md`).

Stdlib only: urllib, json, time, re, pathlib, argparse, sys, socket,
urllib.parse. No third-party dependencies.

Safety (fail-closed, per `.jarvis/system.md` global rules):
  * Targets MUST resolve to loopback (localhost / 127.0.0.1 / ::1) unless
    --allow-staging is explicitly passed AND the hostname is on the staging
    allowlist (--staging-allowlist) or is an RFC-1918 private address.
  * Any non-localhost / non-authorized target -> Modality B halt: exit code 2
    with the standardized AUTHORIZATION REQUIRED template on stderr.
  * Never scans when ZAP daemon is unreachable; never fabricates alerts.

Typical usage:
  python .jarvis/tools/zap_orchestrator.py --target-url http://localhost:3000 --mode baseline
  python .jarvis/tools/zap_orchestrator.py --target-url http://localhost:3000 --mode active --output-json zap_report.json

ZAP daemon prerequisite (see scripts/run_zap.sh / run_zap.ps1):
  docker run -u zap -p 8080:8080 -d --name zap-daemon owasp/zap2docker-stable \\
      zap.sh -daemon -host 0.0.0.0 -port 8080 \\
      -config api.disablekey=true -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ZAP_DEFAULT_URL = "http://localhost:8080"
DEFAULT_TIMEOUT = 30
DEFAULT_POLL_INTERVAL = 5
DEFAULT_SCAN_TIMEOUT = 1800  # 30 min cap for spider / ascan polling

MODALITY_B_TEMPLATE = (
    "⚠️ AUTHORIZATION REQUIRED ON PROTOCOL {check_id} - {name}: {question}"
)

# ---------------------------------------------------------------------------
# HTTP helpers (urllib, stdlib only)
# ---------------------------------------------------------------------------

def _http_get_json(base_url: str, path: str, params: dict | None = None,
                   timeout: int = DEFAULT_TIMEOUT) -> dict:
    """GET <base_url><path>?<params> and decode the JSON body."""
    url = base_url.rstrip("/") + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="GET",
                                 headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        raise ConnectionError(f"GET {url} failed: {exc}") from exc
    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Non-JSON response from ZAP {url}: {body[:200]}") from exc
    return data


def _http_get_status(url: str, timeout: int = 10) -> int | None:
    """Lightweight availability probe of the scan target. Returns HTTP status or None."""
    req = urllib.request.Request(url, method="GET",
                                 headers={"User-Agent": "JARVIS-LiveFire/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return int(resp.status)
    except urllib.error.HTTPError as exc:  # target answered with 4xx/5xx -> reachable
        return int(exc.code)
    except (urllib.error.URLError, socket.timeout, OSError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Safety gate
# ---------------------------------------------------------------------------

LOOPBACK_NAMES = {"localhost"}
LOOPBACK_IPS = {"127.0.0.1", "::1"}


def _resolve_host_ips(hostname: str) -> list[str]:
    """Resolve hostname to IP strings. Returns [] when unresolvable."""
    try:
        _, _, ips = socket.gethostbyname_ex(hostname)
        return ips
    except socket.gaierror:
        # May already be a literal IP (incl. IPv6).
        try:
            ipaddress.ip_address(hostname)
            return [hostname]
        except ValueError:
            return []


def _is_private_ip(ip_str: str) -> bool:
    try:
        return ipaddress.ip_address(ip_str).is_private
    except ValueError:
        return False


def is_loopback_target(hostname: str) -> bool:
    """True when hostname is localhost or resolves exclusively to loopback."""
    if hostname.lower() in LOOPBACK_NAMES:
        return True
    ips = _resolve_host_ips(hostname)
    if not ips:
        return False
    return all(ip in LOOPBACK_IPS or ipaddress.ip_address(ip).is_loopback for ip in ips)


def check_target_safety(target_url: str, allow_staging: bool = False,
                        staging_allowlist: list[str] | None = None) -> tuple[bool, str]:
    """Fail-closed safety gate.

    Returns (allowed, reason). Allowed when:
      * hostname is loopback, OR
      * --allow-staging given AND hostname is allowlisted or RFC-1918 private.
    """
    parsed = urllib.parse.urlparse(target_url)
    if parsed.scheme not in ("http", "https"):
        return False, f"unsupported scheme '{parsed.scheme}' (expected http/https)"
    hostname = (parsed.hostname or "").lower()
    if not hostname:
        return False, "target URL has no hostname"
    if is_loopback_target(hostname):
        return True, f"loopback target '{hostname}' authorized"
    if not allow_staging:
        return False, (
            f"non-loopback target '{hostname}' blocked: re-run with "
            "--allow-staging plus --staging-allowlist, or scan localhost only"
        )
    allowlist = {h.lower() for h in (staging_allowlist or [])}
    if hostname in allowlist:
        return True, f"staging target '{hostname}' explicitly allowlisted"
    for ip in _resolve_host_ips(hostname):
        if _is_private_ip(ip):
            return True, f"staging target '{hostname}' resolves to private IP {ip}"
    # Bare private literal that failed DNS still counts.
    if _is_private_ip(hostname):
        return True, f"staging target '{hostname}' is a private IP literal"
    return False, (
        f"staging target '{hostname}' is not loopback, not allowlisted, and not "
        "RFC-1918 private — refusing to scan"
    )


def modality_b_halt(check_id: str, name: str, question: str) -> "NoReturn":
    """Emit the standardized Modality B halt template and exit 2."""
    print(MODALITY_B_TEMPLATE.format(check_id=check_id, name=name,
                                     question=question), file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# ZAP client
# ---------------------------------------------------------------------------

class ZAPClient:
    """Thin stdlib client for the OWASP ZAP REST API (daemon mode)."""

    def __init__(self, zap_url: str = ZAP_DEFAULT_URL, api_key: str | None = None,
                 timeout: int = DEFAULT_TIMEOUT) -> None:
        self.zap_url = zap_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    # -- low level ------------------------------------------------------
    def _api(self, path: str, params: dict | None = None) -> dict:
        q = dict(params or {})
        if self.api_key:
            q["apikey"] = self.api_key
        return _http_get_json(self.zap_url, path, q, timeout=self.timeout)

    # -- health / preflight ---------------------------------------------
    def health_check(self) -> str:
        """Return ZAP version string; raise ConnectionError when daemon is down."""
        data = self._api("/JSON/core/view/version/")
        version = str(data.get("version", "")).strip()
        if not version:
            raise ConnectionError(f"ZAP at {self.zap_url} returned no version")
        return version

    def check_target_reachable(self, target_url: str) -> int | None:
        return _http_get_status(target_url, timeout=10)

    # -- spider ----------------------------------------------------------
    def spider_scan(self, target_url: str, poll_interval: int = DEFAULT_POLL_INTERVAL,
                    timeout: int = DEFAULT_SCAN_TIMEOUT) -> str:
        resp = self._api("/JSON/spider/action/scan/", {"url": target_url})
        scan_id = str(resp.get("scan", "0"))
        deadline = time.time() + timeout
        while True:
            status = self._api("/JSON/spider/view/status/", {"scanId": scan_id})
            pct = int(str(status.get("status", "0")))
            if pct >= 100:
                return scan_id
            if time.time() > deadline:
                raise TimeoutError(f"Spider scan {scan_id} exceeded {timeout}s")
            time.sleep(poll_interval)

    # -- active scan ------------------------------------------------------
    def active_scan(self, target_url: str, poll_interval: int = DEFAULT_POLL_INTERVAL,
                    timeout: int = DEFAULT_SCAN_TIMEOUT) -> str:
        resp = self._api("/JSON/ascan/action/scan/", {"url": target_url, "recurse": "true"})
        scan_id = str(resp.get("scan", "0"))
        deadline = time.time() + timeout
        while True:
            status = self._api("/JSON/ascan/view/status/", {"scanId": scan_id})
            pct = int(str(status.get("status", "0")))
            if pct >= 100:
                return scan_id
            if time.time() > deadline:
                raise TimeoutError(f"Active scan {scan_id} exceeded {timeout}s")
            time.sleep(poll_interval)

    # -- alerts ------------------------------------------------------------
    def get_alerts(self, base_url: str | None = None) -> list[dict]:
        params: dict = {}
        if base_url:
            params["baseurl"] = base_url
        data = self._api("/JSON/core/view/alerts/", params)
        raw = data.get("alerts", [])
        return [normalize_alert(a, idx) for idx, a in enumerate(raw)]


def normalize_alert(raw: dict, idx: int = 0) -> dict:
    """Normalize one raw ZAP alert dict to the Live Fire schema.

    Never fabricates fields: missing values become "" (never invented).
    """
    get = lambda *keys: next((str(raw.get(k, "") or "") for k in keys if raw.get(k) not in (None, "")), "")
    risk_raw = get("risk", "riskdesc")
    risk = risk_raw.split(" ")[0].capitalize() if risk_raw else "Informational"
    if risk not in ("High", "Medium", "Low", "Informational"):
        risk = "Informational"
    return {
        "id": str(raw.get("id", f"zap-{idx}")),
        "risk": risk,
        "confidence": get("confidence") or "Low",
        "name": get("name", "alert"),
        "url": get("url"),
        "param": get("param"),
        "evidence": get("evidence"),
        "cweid": str(raw.get("cweid", "")),
        "solution": get("solution"),
        "description": get("description"),
    }


# ---------------------------------------------------------------------------
# RouteMapper — alert URL path -> local source file:line
# ---------------------------------------------------------------------------

# (framework, file glob, route regex with named group 'route')
# NOTE: framework-specific decorators (FastAPI/Flask/Django) are matched
# before the generic Express pattern, because e.g. `@app.get('/x')` would
# otherwise match the Express `app.get('...')` alternative first.
ROUTE_PATTERNS: list[tuple[str, str, str]] = [
    ("fastapi", "*.py",
     r"""@\s*(?:app|router|api)\s*\.\s*(?:get|post|put|patch|delete|head|options|trace)\s*\(\s*['"](?P<route>/[^'"]*?)['"]"""),
    ("flask", "*.py",
     r"""@\s*(?:app|bp|blueprint)\s*\.\s*route\s*\(\s*['"](?P<route>/[^'"]*?)['"]"""),
    ("django", "*.py",
     r"""(?:path|re_path|url)\s*\(\s*[r]?['"](?P<route>[^'"]*?)['"]"""),
    ("express", "*.{js,ts,mjs,cjs}",
     r"""(?:app|router)\s*\.\s*(?:get|post|put|patch|delete|all|use)\s*\(\s*['"`](?P<route>/[^'"`]*?)['"`]"""),
    ("next-app", "*.{js,ts,tsx}",
     r"""export\s+(?:async\s+)?function\s+(?:GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\b"""),
]

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next", "venv", ".venv",
             "__pycache__", ".jarvis", ".agents", ".opencode"}


def _iter_candidate_files(repo_root: Path):
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        suffix = path.suffix.lower()
        if suffix in {".js", ".ts", ".tsx", ".mjs", ".cjs", ".py"}:
            yield path


def _normalize_route(route: str) -> str:
    route = "/" + route.strip().strip("^$").strip("/")
    route = re.sub(r"\(.+?\)", "*", route)          # Django regex groups -> wildcard
    route = re.sub(r"<[^>]+>", "*", route)          # Flask <int:id> / Django <int:id>
    route = re.sub(r"[:{][\w$]+[}]?", "*", route)   # Express :id / {id}
    route = re.sub(r"\*+", "*", route)
    return route.rstrip("/") or "/"


def _route_matches(alert_path: str, defined_route: str) -> bool:
    a = _normalize_route(alert_path)
    d = _normalize_route(defined_route)
    if a == d:
        return True
    # Prefix match for mounted routers (defined '/api' serves '/api/users').
    if a.startswith(d.rstrip("/") + "/"):
        return True
    # Wildcard support: defined '/api/users/*' matches '/api/users/123'.
    regex = "^" + re.escape(d).replace(r"\*", "[^/]+") + "$"
    return re.match(regex, a) is not None


def map_url_to_source(alert_url: str, repo_root: Path) -> dict:
    """Map a ZAP alert URL to {'file': str, 'line': int|None, 'framework': str}.

    Evidence-grounded: only returns entries backed by an actual regex hit in
    the working tree; otherwise file == "" (never invented).
    """
    empty = {"file": "", "line": None, "framework": ""}
    try:
        alert_path = urllib.parse.urlparse(alert_url).path or "/"
    except ValueError:
        return empty
    # Next.js App-router convention: app/api/login/route.ts serves /api/login.
    nextjs_convention = alert_path.strip("/")
    for path in _iter_candidate_files(repo_root):
        # Convention-based Next.js App Router match (no regex needed).
        parts = path.as_posix().lower()
        if "app/" in parts and path.name.startswith("route."):
            convention = re.sub(r".*/app/", "", path.as_posix())
            convention = re.sub(r"/route\.(js|ts|tsx)$", "", convention)
            if _normalize_route(convention) == _normalize_route(nextjs_convention):
                return {"file": path.as_posix(), "line": 1, "framework": "next-app"}
    for framework, glob_suffix, pattern in ROUTE_PATTERNS:
        _ = glob_suffix  # documented per-framework glob; filtered by suffix above
        try:
            rx = re.compile(pattern)
        except re.error:
            continue
        for path in _iter_candidate_files(repo_root):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for m in rx.finditer(text):
                defined = m.groupdict().get("route")
                if defined is None:  # e.g. Next.js exported handler -> whole file is the route
                    if framework == "next-app" and nextjs_convention in path.as_posix():
                        line = text[:m.start()].count("\n") + 1
                        return {"file": path.as_posix(), "line": line, "framework": framework}
                    continue
                if _route_matches(alert_path, defined):
                    line = text[:m.start()].count("\n") + 1
                    try:
                        rel = path.relative_to(repo_root).as_posix()
                    except ValueError:
                        rel = path.as_posix()
                    return {"file": rel, "line": line, "framework": framework}
    return empty


class RouteMapper:
    """Repo-wide route index wrapper around map_url_to_source."""

    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root).resolve()

    def map(self, alert_url: str) -> dict:
        return map_url_to_source(alert_url, self.repo_root)

    def enrich(self, alerts: list[dict]) -> list[dict]:
        enriched = []
        for alert in alerts:
            mapping = self.map(alert.get("url", ""))
            merged = dict(alert)
            merged["source_file"] = mapping.get("file", "")
            merged["source_line"] = mapping.get("line")
            merged["framework"] = mapping.get("framework", "")
            enriched.append(merged)
        return enriched


# ---------------------------------------------------------------------------
# Orchestration entry point
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="JARVIS Live Fire Protocol — OWASP ZAP DAST orchestrator (stdlib only).")
    p.add_argument("--target-url", required=True, help="Scan target, e.g. http://localhost:3000")
    p.add_argument("--zap-url", default=ZAP_DEFAULT_URL, help="ZAP daemon base URL")
    p.add_argument("--api-key", default=None, help="ZAP API key (omit when api.disablekey=true)")
    p.add_argument("--mode", choices=("baseline", "active"), default="baseline",
                   help="baseline = spider+passive only; active = + active scan")
    p.add_argument("--output-json", default=None, help="Write normalized alert JSON here")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Per-request timeout (s)")
    p.add_argument("--scan-timeout", type=int, default=DEFAULT_SCAN_TIMEOUT,
                   help="Max seconds to poll spider/ascan to 100%%")
    p.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL,
                   help="Poll interval in seconds")
    p.add_argument("--no-spider", action="store_true", help="Skip spider phase")
    p.add_argument("--allow-staging", action="store_true",
                   help="Permit non-loopback private/staging targets (Modality B bypass)")
    p.add_argument("--staging-allowlist", default="",
                   help="Comma-separated staging hostnames explicitly authorized")
    p.add_argument("--repo-root", default=".",
                   help="Repository root used by RouteMapper for source mapping")
    p.add_argument("--no-map-routes", action="store_true", help="Skip RouteMapper enrichment")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    # -- Phase 1: PRE_FLIGHT_SAFETY -------------------------------------
    allowed, reason = check_target_safety(
        args.target_url, allow_staging=args.allow_staging,
        staging_allowlist=[h.strip() for h in args.staging_allowlist.split(",") if h.strip()])
    if not allowed:
        modality_b_halt(
            "PRE-FLIGHT", "Target safety gate",
            f"Refusing to scan {args.target_url}: {reason}. "
            "Confirm the target is a local or explicitly authorized private staging "
            "environment, then re-run with --allow-staging and --staging-allowlist.")

    client = ZAPClient(zap_url=args.zap_url, api_key=args.api_key, timeout=args.timeout)
    try:
        version = client.health_check()
    except (ConnectionError, ValueError) as exc:
        print(f"ZAP daemon unreachable at {args.zap_url}: {exc}", file=sys.stderr)
        print("Start ZAP first: scripts/run_zap.sh (or run_zap.ps1 on Windows).",
              file=sys.stderr)
        return 3
    print(f"[live-fire] ZAP {version} reachable at {args.zap_url}", file=sys.stderr)

    status = client.check_target_reachable(args.target_url)
    if status is None:
        print(f"[live-fire] FAIL CLOSED: target {args.target_url} unreachable; "
              "start the app under test, then re-run.", file=sys.stderr)
        return 4
    print(f"[live-fire] target {args.target_url} answered HTTP {status}", file=sys.stderr)
    print(f"[live-fire] safety gate: {reason}", file=sys.stderr)

    # -- Phase 2: DYNAMIC_INFILTRATION -----------------------------------
    try:
        if not args.no_spider:
            print("[live-fire] spidering…", file=sys.stderr)
            client.spider_scan(args.target_url, poll_interval=args.poll_interval,
                               timeout=args.scan_timeout)
            print("[live-fire] spider complete (100%)", file=sys.stderr)
        if args.mode == "active":
            print("[live-fire] active scan running…", file=sys.stderr)
            client.active_scan(args.target_url, poll_interval=args.poll_interval,
                               timeout=args.scan_timeout)
            print("[live-fire] active scan complete (100%)", file=sys.stderr)
        # Brief settle so passive rules finish before harvest.
        time.sleep(2)
        alerts = client.get_alerts()
    except TimeoutError as exc:
        print(f"[live-fire] scan timeout: {exc}", file=sys.stderr)
        return 5
    except (ConnectionError, ValueError) as exc:
        print(f"[live-fire] ZAP API error mid-scan: {exc}", file=sys.stderr)
        return 5

    # -- Phase 3: THREAT_AUDIT (route mapping) -----------------------------
    if not args.no_map_routes:
        mapper = RouteMapper(args.repo_root)
        alerts = mapper.enrich(alerts)

    payload = {
        "tool": "owasp-zap",
        "zap_version": version,
        "target_url": args.target_url,
        "mode": args.mode,
        "alert_count": len(alerts),
        "alerts": alerts,
    }
    rendered = json.dumps(payload, indent=2)
    if args.output_json:
        Path(args.output_json).write_text(rendered + "\n", encoding="utf-8")
        print(f"[live-fire] {len(alerts)} alert(s) -> {args.output_json}", file=sys.stderr)
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
