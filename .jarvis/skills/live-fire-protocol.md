# Skill Manifest: Live Fire Protocol (Dynamic Application Security Testing & Automated Remediation)

**Command:** `/JARVIS, Live Fire Protocol`
**Trigger:** Activated when the developer invokes the exact phrase above in a direct chat message (trailing free text captured as `user_supplied_context`, e.g. a target URL or staging hostname).
**Nature:** Dynamic Application Security Testing against a RUNNING app. Spiders and attacks the live target with headless OWASP ZAP, correlates each alert back to a local source route, auto-fixes code-level findings (Modality A), halts on infra/secret/destructive actions (Modality B), then re-scans to verify. Educational DAST pass — not a penetration test, legal advice, or security guarantee.

**The rule this manifest enforces:** every reported finding, file:line citation, and verification claim must be grounded in an actual ZAP REST API response plus a repository grep/AST hit. If you cannot point to the alert JSON and the source line, the result is UNKNOWN — never PASS.

**Runner:** `.jarvis/tools/zap_orchestrator.py` (stdlib only). ZAP daemon prerequisite — start with `scripts/run_zap.sh` (Linux/macOS) or `scripts/run_zap.ps1` (Windows).

**When J.A.R.V.I.S. announces this skill, open with:**
> "Live fire authorized, sir. Spinning up dynamic attack simulations."

---

## Execution flow (6 phases)

### Phase 1 — PRE_FLIGHT_SAFETY (fail closed)

1. Resolve the target URL: explicit `--target-url` from `user_supplied_context` wins; otherwise default to `http://localhost:3000` and ask the developer to confirm.
2. Verify the ZAP daemon answers `GET /JSON/core/view/version/` at `--zap-url` (default `http://localhost:8080`). If unreachable, FAIL CLOSED: print the `run_zap` helper command and stop — never simulate results.
3. Enforce the **strict target whitelist**: hostname must be `localhost` / `127.0.0.1` / `::1` (loopback). Any other host halts under **Modality B** with the verbatim template:
   ```
   ⚠️ AUTHORIZATION REQUIRED ON PROTOCOL PRE-FLIGHT - Target safety gate: Confirm [target URL] is an explicitly authorized private staging environment you own, then re-run with --allow-staging and --staging-allowlist=[host]. No external scan proceeds without this confirmation.
   ```
4. Ping the target URL. If unreachable, fail closed and ask the developer to start the app under test.

### Phase 2 — DYNAMIC_INFILTRATION

1. Invoke the runner via subprocess:
   - `baseline` (default): spider + passive rules only — safe for any running dev server.
   - `active`: spider + full active attack scan — only against local/staging targets cleared in Phase 1.
   ```
   python .jarvis/tools/zap_orchestrator.py --target-url <URL> --mode <baseline|active> --output-json .jarvis/history/zap-<timestamp>.json
   ```
2. Poll spider status to 100%, then active-scan status to 100% (handled inside the runner with `--scan-timeout` / `--poll-interval`).
3. Treat any runner exit code != 0 as an infrastructure failure, not a clean bill of health — report it, never convert it to PASS.

### Phase 3 — THREAT_AUDIT

1. Load the JSON alerts. Each alert carries ZAP-grounded `name`, `risk`, `confidence`, `url`, `param`, `evidence`, `cweid`, `solution`.
2. Run `RouteMapper` (`--repo-root .`) to map each alert path (e.g. `/api/auth/login`) to a local handler (`src/routes/auth.ts:24`). Supported: Express (`app.get('/…')`), Next.js App Router (`app/api/…/route.ts`) and Pages Router, FastAPI (`@app.get('/…')`), Flask (`@app.route('/…')`), Django (`path('…')`).
3. Evaluate every mapped finding against checks DAST-01–DAST-15 below. Unmapped alerts stay in the report with `Source File:Line = unmapped (no route hit)` — never dropped, never invented.
4. Risk order: High → Medium → Low → Informational. `UNKNOWN` (no ZAP evidence either way for a check) counts as FAIL-equivalent until a verification scan proves otherwise.

### Phase 4 — PROTOCOL_REMEDIATION (modality routing per check)

- **Modality A (Auto-Fix Armor):** apply the Armor Fix Template directly to source files, then log exactly:
  ```
  🛠️ ARMOR DEPLOYED — PROTOCOL [DAST-ID] - [NAME]
  File(s): [path(s):line(s)]
  Change: [one-sentence description of exactly what was changed]
  Verification: [targeted re-scan command, e.g. "re-run baseline scan against /api/users?id=1"]
  ```
- **Modality B (Human Authorization Required):** HALT that check and print verbatim:
  ```
  ⚠️ AUTHORIZATION REQUIRED ON PROTOCOL [DAST-ID] - [NAME]: [single concrete question/instruction]
  ```

### Phase 5 — VERIFICATION_SCAN

Re-run the runner in `baseline` mode (or a targeted `active` pass over remediated endpoints) and diff the alert sets. A check flips to PASS only when the original alert ID/URL no longer reproduces AND the fix is cited file:line. Otherwise it stays FAIL.

### Phase 6 — SECURE_REPORTING

1. Archive any prior Live Fire section per `reporting.keep_previous_run_archive`, then overwrite the `Live Fire Protocol Ledger` in `.jarvis/STATE.md` with the table in that section's header.
2. Print a chat summary: total alerts by risk, PASS/FAIL/WAITING_AUTH counts across DAST-01–15, and every open WAITING_AUTH item.
3. Close with: "This was a dynamic scan of [target] in [mode] mode — not a penetration test or security guarantee. Re-run after meaningful changes to routes, auth, data handling, or headers. Standing by, sir."

---

## Checks DAST-01–DAST-15

### DAST-01 — Injection Flaws (SQLi, NoSQLi, Command Injection)
- **Risk:** High
- **DAST trigger rule:** ZAP active-scan alerts matching `SQL Injection`, `NoSQL`, `Remote OS Command Injection`, or error-signature evidence (`SQL syntax`, `MongoError`, `command not found`) on any `url`+`param`.
- **Modality:** A for code fixes; B if the fix requires a production DB migration or WAF/infra rule change.
- **Armor fix template:** Parameterize the query at the mapped handler — prepared statements / ORM-bound parameters (never string-concatenated input); validate `param` against an allowlist/type schema; for shell, replace `exec`/`shell=True` with `spawn`/`subprocess` argv arrays. Log the ARMOR block with file:line.

### DAST-02 — Cross-Site Scripting (Reflected & Stored XSS)
- **Risk:** High
- **DAST trigger rule:** ZAP `Cross Site Scripting (Reflected)` / `(Stored/Persistent)` alerts, or unencoded `evidence` echoing the attack payload in a response body.
- **Modality:** A.
- **Armor fix template:** Context-appropriate output encoding at the mapped render path (`escapeHtml` / framework auto-escaping; never `innerHTML` / `dangerouslySetInnerHTML` with raw input); strip/allowlist-sanitize stored content on write; add a nonce- or hash-based CSP (see DAST-13).

### DAST-03 — Broken Access Control & Forced Browsing
- **Risk:** High
- **DAST trigger rule:** ZAP forced-browsing / `Access Control` / 200-OK on paths that should require auth (admin, `/actuator`, backup files), or IDOR-differentiated responses across two identities.
- **Modality:** A for missing server-side checks; B if lockdown needs IdP/network/VPN changes.
- **Armor fix template:** Add server-side authorization at the mapped route (deny-by-default, ownership/role check before any read/write); remove or auth-gate debug/backup endpoints; never rely on hidden URLs.

### DAST-04 — Missing Anti-CSRF Guardrails
- **Risk:** Medium
- **DAST trigger rule:** ZAP `Absence of Anti-CSRF Tokens` alert on any state-changing form/endpoint (POST/PUT/PATCH/DELETE without token evidence).
- **Modality:** A.
- **Armor fix template:** Issue per-session CSRF tokens and verify them server-side on every state-changing route; set cookies `SameSite=Lax` minimum (`Strict` where UX allows); ensure GET performs no mutations.

### DAST-05 — Insecure HTTP Headers (HSTS, CSP, X-Content-Type-Options)
- **Risk:** Medium
- **DAST trigger rule:** ZAP `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options` missing/misconfigured header alerts on any in-scope response.
- **Modality:** A for app-emitted headers; B if headers must be set on external CDN/LB the repo cannot control.
- **Armor fix template:** Emit from app middleware (or verified reverse-proxy config in-repo): `Strict-Transport-Security: max-age=31536000; includeSubDomains`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY` (or `frame-ancestors 'none'`), `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy` least-privilege, and a tested CSP (see DAST-13).

### DAST-06 — Sensitive Data Exposure via URL / Verbose Errors
- **Risk:** High
- **DAST trigger rule:** ZAP `Sensitive Information in URL`, session/PII tokens in query strings, or stack traces / SQL / paths in response bodies (`500` with `Traceback`, `at … (…)`, `SELECT` fragments).
- **Modality:** A for code-level leaks; B if rotation of an exposed live secret is required.
- **Armor fix template:** Move secrets/tokens/PII out of URLs into headers/body; return generic external error shapes and confine stack traces to private logs; if a live secret was exposed, halt for rotation confirmation (Modality B) before marking PASS.

### DAST-07 — Insecure Cookie Flags (`HttpOnly`, `Secure`, `SameSite`)
- **Risk:** Medium
- **DAST trigger rule:** ZAP `Cookie No HttpOnly Flag`, `Cookie Without Secure Flag`, `Cookie Without SameSite Attribute` alerts naming the offending `Set-Cookie`.
- **Modality:** A.
- **Armor fix template:** Set session/auth cookies `HttpOnly; Secure; SameSite=Lax-or-Strict; Path=/` (and `__Host-` prefix where applicable) at the mapped session/cookie code; verify via re-scan `Set-Cookie` inspection.

### DAST-08 — Open Redirection Vulnerabilities
- **Risk:** Medium
- **DAST trigger rule:** ZAP `Open Redirect` alert where a query param (`next`, `returnUrl`, `redirect`) controls `Location` to an external host.
- **Modality:** A.
- **Armor fix template:** Validate redirect destinations against an allowlist or restrict to same-origin relative paths at the mapped handler; reject protocol-relative (`//evil`) and absolute external URLs.

### DAST-09 — Insecure Direct Object References (IDOR)
- **Risk:** High
- **DAST trigger rule:** Sequential/tampered object IDs (`/api/orders/124` vs `/125`) returning another principal's data in the scan (differential evidence), or ZAP IDOR-pattern alerts.
- **Modality:** A for ownership checks; B if remediation needs a data-model/tenant migration.
- **Armor fix template:** Enforce server-side ownership/scope checks (row-level scoping to the authenticated principal) at the mapped handler; prefer indirection (opaque IDs) plus authorization — never bare sequential IDs alone.

### DAST-10 — Server-Side Request Forgery (SSRF)
- **Risk:** High
- **DAST trigger rule:** ZAP `Server Side Request Forgery` alert or a scanned parameter that causes the server to fetch an attacker-influenced URL (evidence: fetched internal/metadata content).
- **Modality:** A for allowlist/blocklist code; B if cloud-metadata/network egress must change outside the repo.
- **Armor fix template:** Allowlist destination hosts/schemes at the mapped fetch site; explicitly block private ranges (`169.254.0.0/16`, `10/8`, `172.16/12`, `192.168/16`, loopback) and the cloud metadata endpoint; never fetch raw user-supplied URLs.

### DAST-11 — CORS Misconfiguration (Overly Permissive Origins)
- **Risk:** Medium
- **DAST trigger rule:** ZAP `CORS` alerts showing `Access-Control-Allow-Origin: *` (or reflected arbitrary `Origin`) combined with `Access-Control-Allow-Credentials: true` on credentialed endpoints.
- **Modality:** A.
- **Armor fix template:** Replace `*` with an explicit origin allowlist at the mapped CORS config; never echo arbitrary `Origin`; disable credentials unless strictly required, and then only for allowlisted origins.

### DAST-12 — Cache-Control & Information Leakage
- **Risk:** Low
- **DAST trigger rule:** ZAP `Incomplete or No Cache-control` / `Private IP Disclosure` / `Information Disclosure` alerts (server banners, internal IPs, e-mails in responses).
- **Modality:** A.
- **Armor fix template:** Send `Cache-Control: no-store` (plus `Pragma: no-cache`) on authenticated/sensitive responses; suppress banner/version headers and internal addresses from scan-visible output; scope public caching to genuinely public assets only.

### DAST-13 — Content Security Policy Missing or Bypassable
- **Risk:** Medium
- **DAST trigger rule:** ZAP `Content Security Policy (CSP) Header Not Set` or CSP-analyzer findings (`unsafe-inline`, `unsafe-eval`, `*` / `http:` source lists that neutralize the policy).
- **Modality:** A.
- **Armor fix template:** Ship a restrictive tested CSP from app middleware (e.g. `default-src 'self'; script-src 'self'` + nonces/hashes for required inline; `object-src 'none'; frame-ancestors 'none'; base-uri 'self'`); remove `unsafe-inline`/`unsafe-eval`/wildcards; verify no console breakage and re-scan.

### DAST-14 — Unhandled Server Exceptions & Stack Trace Leaks
- **Risk:** Medium
- **DAST trigger rule:** ZAP `Application Error Disclosure` alerts or 500-class responses during the scan containing framework tracebacks, file paths, or query fragments.
- **Modality:** A for handlers; B if the fix needs centralized log-infra provisioning.
- **Armor fix template:** Add catch-all error middleware at/above the mapped route returning a stable generic shape (e.g. `{"error":"internal_error"}` + correlation ID); route full traces to the private logger; add regression coverage for the crashing input.

### DAST-15 — Rate Limiting & Denial-of-Service Defense
- **Risk:** Medium
- **DAST trigger rule:** No ZAP alert proves a negative — trigger by *absence*: unusually large active-scan request volume against auth/OTP/search endpoints with zero `429` responses, or response-time degradation observed during the scan.
- **Modality:** A when middleware suffices; B if protection requires external rate-limit infra (Redis plan, CDN/WAF rules) the repo cannot provision.
- **Armor fix template:** Add per-IP + per-account throttling middleware on the mapped sensitive routes (e.g. login/OTP/search/export) with `429 + Retry-After`; add payload/timeout caps on expensive handlers; re-probe to confirm `429` behavior. Never claim PASS without observed `429`/throttle evidence.

---

## Official sources (for deeper reference during remediation)

- OWASP ZAP API documentation (zaproxy.org/docs/api)
- OWASP Top 10 (2021) — owasp.org/Top10
- OWASP Testing Guide v4 (OTG) — dynamic testing procedures
- OWASP Cheat Sheet Series — cheatsheetseries.owasp.org (SQLi, XSS, CSRF, SSRF, CORS, CSP)
- CWE/SANS Top 25 Most Dangerous Software Weaknesses
- Mozilla Observatory — HTTP Security Headers (observatory.mozilla.org)

**Launch standard:** a check passes only when the ZAP alert no longer reproduces on re-scan AND the fix is cited file:line. Re-run Live Fire after meaningful changes to routes, auth, data handling, or headers.
