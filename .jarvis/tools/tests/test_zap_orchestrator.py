"""Unit + end-to-end tests for the Live Fire Protocol ZAP orchestrator.

Stdlib only (unittest + http.server). Run from the repository root:

    python -m unittest discover -s .jarvis/tools/tests -v

The MockZAPHandler emulates just enough of the OWASP ZAP REST API to drive
the full orchestration path: health check -> spider poll loop -> active-scan
poll loop -> alert harvest. Assertions below verify the contract the skill
manifest depends on (exit codes, normalized schema, route enrichment,
fail-closed behavior) — not the behavior of real ZAP itself.
"""

import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from zap_orchestrator import (  # noqa: E402
    RouteMapper,
    check_target_safety,
    main,
    map_url_to_source,
    normalize_alert,
)

# ---------------------------------------------------------------------------
# Mock servers
# ---------------------------------------------------------------------------

MOCK_ALERTS = [
    {
        "id": "101",
        "name": "SQL Injection",
        "risk": "High",
        "confidence": "Medium",
        "url": "http://127.0.0.1:PORT/api/users?id=1",
        "param": "id",
        "evidence": "syntax error in SQL statement",
        "cweid": "89",
        "solution": "Use parameterized queries",
        "description": "Mock SQLi alert",
    },
    {
        "id": "102",
        "name": "Cross Site Scripting (Reflected)",
        "risk": "High",
        "confidence": "High",
        "url": "http://127.0.0.1:PORT/search?q=<script>",
        "param": "q",
        "evidence": "<script>alert(1)</script>",
        "cweid": "79",
        "solution": "Encode output",
        "description": "Mock XSS alert",
    },
]


class MockZAPHandler(BaseHTTPRequestHandler):
    """Faithful-enough ZAP API double: spider/ascan go 0 -> 100."""

    spider_calls = 0
    protocol_version = "HTTP/1.1"

    def _send(self, payload):
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path == "/JSON/core/view/version/":
            self._send({"version": "2.14.0-mock"})
        elif path == "/JSON/spider/action/scan/":
            self._send({"scan": "1"})
        elif path == "/JSON/spider/view/status/":
            type(self).spider_calls += 1
            pct = "0" if type(self).spider_calls < 2 else "100"
            self._send({"status": pct})
        elif path == "/JSON/ascan/action/scan/":
            self._send({"scan": "2"})
        elif path == "/JSON/ascan/view/status/":
            self._send({"status": "100"})
        elif path == "/JSON/core/view/alerts/":
            port = self.server.server_address[1]  # not used; URLs fixed by test
            _ = port
            self._send({"alerts": self.server.alerts})
        else:
            self.send_error(404, "mock zap: unknown path")

    def log_message(self, *args):
        pass


class MockTargetHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _ok(self, body=b"ok"):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._ok()

    def log_message(self, *args):
        pass


def _serve(handler):
    server = HTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class SafetyGateTests(unittest.TestCase):
    def test_loopback_allowed_without_flag(self):
        for url in ("http://localhost:3000", "http://127.0.0.1:8080/api",
                    "http://localhost:9"):
            allowed, _ = check_target_safety(url)
            self.assertTrue(allowed, url)

    def test_external_blocked_without_flag(self):
        allowed, reason = check_target_safety("https://example.com/")
        self.assertFalse(allowed)
        self.assertIn("--allow-staging", reason)

    def test_external_blocked_even_with_flag_unless_private_or_allowlisted(self):
        allowed, _ = check_target_safety("https://example.com/", allow_staging=True)
        self.assertFalse(allowed)
        allowed, _ = check_target_safety(
            "http://staging.internal:3000", allow_staging=True,
            staging_allowlist=["staging.internal"])
        self.assertTrue(allowed)

    def test_private_ip_allowed_only_with_flag(self):
        allowed, _ = check_target_safety("http://192.168.1.10:3000")
        self.assertFalse(allowed)
        allowed, _ = check_target_safety("http://192.168.1.10:3000",
                                         allow_staging=True)
        self.assertTrue(allowed)

    def test_unsupported_scheme_rejected(self):
        allowed, _ = check_target_safety("ftp://localhost/x")
        self.assertFalse(allowed)


class NormalizeTests(unittest.TestCase):
    def test_schema_keys_present_and_no_fabrication(self):
        raw = {"name": "SQL Injection", "risk": "High",
               "url": "http://localhost:3000/api/users?id=1"}
        n = normalize_alert(raw, 0)
        self.assertEqual(
            sorted(n), ["confidence", "cweid", "description", "evidence",
                        "id", "name", "param", "risk", "solution", "url"])
        self.assertEqual(n["risk"], "High")
        self.assertEqual(n["param"], "")  # missing -> "" not invented
        self.assertEqual(n["cweid"], "")

    def test_unknown_risk_downgraded_not_dropped(self):
        n = normalize_alert({"name": "Weird", "risk": "Critical!!"}, 7)
        self.assertEqual(n["risk"], "Informational")


class RouteMapperTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "src").mkdir()
        (root / "src" / "routes_auth.js").write_text(
            "const express = require('express');\n"
            "const router = express.Router();\n"
            "router.post('/api/auth/login', (req, res) => res.send('ok'));\n")
        (root / "app_api.py").write_text(
            "from fastapi import FastAPI\napp = FastAPI()\n\n"
            "@app.get('/api/users')\ndef list_users():\n    return []\n")
        (root / "views.py").write_text(
            "from flask import Flask\napp = Flask(__name__)\n\n"
            "@app.route('/search')\ndef search():\n    return 'ok'\n")
        self.mapper = RouteMapper(root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_express_hit(self):
        hit = self.mapper.map("http://localhost:3000/api/auth/login")
        self.assertTrue(hit["file"].endswith("routes_auth.js"))
        self.assertEqual(hit["line"], 3)
        self.assertEqual(hit["framework"], "express")

    def test_fastapi_label_not_swallowed_by_express(self):
        hit = self.mapper.map("http://localhost:3000/api/users?page=2")
        self.assertTrue(hit["file"].endswith("app_api.py"))
        self.assertEqual(hit["framework"], "fastapi")

    def test_flask_hit(self):
        hit = self.mapper.map("http://localhost:3000/search?q=x")
        self.assertTrue(hit["file"].endswith("views.py"))
        self.assertEqual(hit["framework"], "flask")

    def test_unmapped_returns_empty_never_invented(self):
        hit = self.mapper.map("http://localhost:3000/no/such/route")
        self.assertEqual(hit, {"file": "", "line": None, "framework": ""})

    def test_enrich_adds_source_fields(self):
        alerts = [{"url": "http://localhost:3000/api/users", "name": "X"}]
        enriched = self.mapper.enrich(alerts)
        self.assertTrue(enriched[0]["source_file"].endswith("app_api.py"))
        self.assertEqual(enriched[0]["source_line"], 4)


class EndToEndTests(unittest.TestCase):
    """Drive main() against mock ZAP + mock target + fixture repo."""

    def setUp(self):
        MockZAPHandler.spider_calls = 0
        self.zap = _serve(MockZAPHandler)
        self.target = _serve(MockTargetHandler)
        target_url = f"http://127.0.0.1:{self.target.server_address[1]}"
        self.zap.alerts = [
            {**a, "url": a["url"].replace(
                "http://127.0.0.1:PORT", target_url)}
            for a in MOCK_ALERTS
        ]
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "server.js").write_text(
            "const app = require('express')();\n"
            "app.get('/api/users', (req, res) => res.json([]));\n")
        self.repo_root = str(root)
        self.out = str(Path(self.tmp.name) / "report.json")
        self.zap_url = f"http://127.0.0.1:{self.zap.server_address[1]}"
        self.target_url = target_url

    def tearDown(self):
        self.zap.shutdown()
        self.target.shutdown()
        self.zap.server_close()
        self.target.server_close()
        self.tmp.cleanup()

    def test_active_mode_full_path(self):
        rc = main(["--target-url", self.target_url, "--zap-url", self.zap_url,
                   "--mode", "active", "--output-json", self.out,
                   "--poll-interval", "1", "--scan-timeout", "60",
                   "--repo-root", self.repo_root])
        self.assertEqual(rc, 0)
        payload = json.loads(Path(self.out).read_text())
        self.assertEqual(payload["tool"], "owasp-zap")
        self.assertEqual(payload["zap_version"], "2.14.0-mock")
        self.assertEqual(payload["mode"], "active")
        self.assertEqual(payload["alert_count"], 2)
        by_name = {a["name"]: a for a in payload["alerts"]}
        sqli = by_name["SQL Injection"]
        self.assertEqual(sqli["risk"], "High")
        self.assertEqual(sqli["param"], "id")
        self.assertEqual(sqli["cweid"], "89")
        self.assertTrue(sqli["source_file"].endswith("server.js"))
        self.assertEqual(sqli["source_line"], 2)
        self.assertEqual(sqli["framework"], "express")
        xss = by_name["Cross Site Scripting (Reflected)"]
        self.assertEqual(xss["source_file"], "")  # honestly unmapped

    def test_modality_b_halt_on_external_target(self):
        with self.assertRaises(SystemExit) as ctx:
            main(["--target-url", "https://example.com/",
                  "--zap-url", self.zap_url])
        self.assertEqual(ctx.exception.code, 2)

    def test_fail_closed_when_zap_down(self):
        rc = main(["--target-url", self.target_url,
                   "--zap-url", "http://127.0.0.1:9",
                   "--timeout", "2"])
        self.assertEqual(rc, 3)


if __name__ == "__main__":
    unittest.main()
