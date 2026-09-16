# Skill Manifest: Test Complete. Prepare for Landing.

**Command:** `/JARVIS, Test complete. Prepare for landing`
**Trigger:** Activated when the developer invokes the exact phrase above in a direct chat message.
**Nature:** Deployment readiness and security audit. Educational checklist — not a penetration test, legal advice, or a deployment guarantee. Do not ship until all applicable checks are verified with evidence.

**The rule this manifest enforces:** if you cannot point to the exact file, config value, scan result, log entry, or browser output that proves a gate has been cleared, the result is FAIL or UNKNOWN — never PASS.

Each check below is one gate that must clear before the project goes to production. Phase 2 evaluates all 42 checks. Phase 3 auto-fixes code-level issues (Modality A) or halts for developer action (Modality B). Findings are written to `.jarvis/STATE.md` under the "Prepare for Landing Ledger" section.

**When J.A.R.V.I.S. announces results for this skill, open with:**
> "All systems reviewed, sir. Here is the landing report."

---

## PART 1 — GIT & REPOSITORY READINESS (Checks 01–06)

The codebase must be clean before it ships.

### 01 — No uncommitted changes in working tree
Run `git status`. Working tree must be clean. All intended changes must be committed. Shipping with uncommitted work in the tree is a FAIL — what's live will not match what's in version control.

### 02 — No sensitive files tracked by git
Run `git ls-files` and cross-reference against known secret file types (`.env`, `.pem`, `.p12`, `*.key`, `id_rsa`, `credentials.json`, `serviceAccountKey.json`, etc.). Any tracked secret file is a hard FAIL.

### 03 — .gitignore is complete and correct
`.gitignore` must cover: environment files (`.env`, `.env.local`, `.env.production`), secrets, build artifacts (`/dist`, `/build`, `/.next`), OS files (`.DS_Store`, `Thumbs.db`), editor config (`.vscode/`, `.idea/`), and local config. Missing common patterns are a FAIL.

### 04 — Branch hygiene verified
The production branch (main/master) must contain all changes intended for this release. No open feature branches with intended-to-ship work that was not merged. No accidental inclusion of experimental branches.

### 05 — Commit history is clean
Inspect the last 20 commits. No WIP commits, no "debug", no "remove this later", no commits containing secrets or API keys, no large binary files accidentally committed. Problematic commits must be cleaned or squashed.

### 06 — No merge conflict markers remaining
Search the entire working tree for `<<<<<<<`, `=======`, and `>>>>>>>`. Any remaining conflict markers indicate an incomplete merge and are a hard FAIL.

---

## PART 2 — ENVIRONMENT & BUILD READINESS (Checks 07–12)

The build must run clean and be fully configured for production.

### 07 — Production environment variables configured
Every environment variable the application requires must be set in the production environment (hosting platform secrets, secrets manager, or deployment config). Not hardcoded in source files. Missing variables cause silent runtime failures — a FAIL.

### 08 — .env.example is present and complete
`.env.example` must exist in the repository root and list every environment variable the app needs, with placeholder values (not real values) and explanatory comments. A missing or outdated `.env.example` is a FAIL.

### 09 — Production build completes without errors
Run the production build command (`npm run build`, `vite build`, `next build`, or equivalent). It must exit with code 0 and zero build errors. Warnings must be reviewed. A failing build is a hard FAIL.

### 10 — All production dependencies are pinned
`package.json` / `requirements.txt` / `go.sum` / equivalent must use exact pinned versions for all production dependencies, not `^`, `~`, or `*` ranges. Unpinned ranges allow silent upstream breakage on redeploy.

### 11 — No development dependencies bleeding into production build
Confirm that test frameworks, linting tools, mock libraries, and development utilities are not bundled into the production artifact. Check bundle analyzer output or build manifest.

### 12 — Build output is clean and contains no secrets
Inspect the production build output (`/dist`, `/build`, `/.next/static`, etc.): no source maps exposed publicly, no `.env` files, no private keys, no internal API endpoints, no credentials embedded in minified JS. Any exposure is a hard FAIL.

---

## PART 3 — OWASP TOP 10 (2021) (Checks 13–22)

The canonical web application security standard. Every check must be evaluated against the actual codebase.

### 13 — A01: Broken Access Control
Authorization checks exist server-side on every protected route, API endpoint, and sensitive action. Verify IDOR/BOLA: changing an object ID in a request cannot expose or modify another user's data. Row-level security or equivalent scope enforcement must be present.

### 14 — A02: Cryptographic Failures
Sensitive data (passwords, payment data, PII, tokens, session keys) is encrypted in transit via HTTPS/TLS and at rest using provider-level or application-level encryption. No MD5 or SHA-1 for passwords. No sensitive data returned in API responses unnecessarily.

### 15 — A03: Injection
All database interactions use parameterized queries, prepared statements, or safe ORM bindings — no user input concatenated into SQL strings. Shell commands use safe APIs with validated arguments — no `exec` or `shell=True` with user input. Template engines auto-escape output.

### 16 — A04: Insecure Design
Core business logic abuse vectors have been considered: price tampering, credit manipulation, free trial bypass, coupon stacking, rate limit circumvention, invalid state transitions. The application enforces correct state server-side for all sensitive flows.

### 17 — A05: Security Misconfiguration
No default credentials in any service. No unnecessary features, ports, endpoints, or admin interfaces exposed. Error responses are generic to external users. HTTP security headers are configured. Debug mode, verbose logging, and test routes are disabled in production.

### 18 — A06: Vulnerable and Outdated Components
A dependency vulnerability scan (`npm audit`, `pip-audit`, `trivy`, `snyk`, or equivalent) has been run. All critical and high-severity CVEs have been addressed. No abandoned or unmaintained packages occupy a critical path in the application.

### 19 — A07: Identification and Authentication Failures
Authentication is implemented using a proven library or managed auth provider — not custom session logic. Session tokens are cryptographically random, sufficiently long, and rotated on login, privilege change, and logout. Brute force protection (lockout or rate limiting) exists on all auth endpoints.

### 20 — A08: Software and Data Integrity Failures
CI/CD pipeline uses pinned action versions (SHA-pinned for GitHub Actions). All packages come from trusted registries and are verified via lockfile (`npm ci`, not `npm install`). No untrusted third-party build scripts have access to production secrets or signing keys.

### 21 — A09: Security Logging and Monitoring Failures
Authentication events (login, logout, failure, lockout, password change), privilege escalation, sensitive data access, and critical application errors are logged. Alerts exist for anomalous patterns. Logs are stored securely, separately from the application, and access is restricted.

### 22 — A10: Server-Side Request Forgery (SSRF)
Every server-side outbound HTTP request validates and allowlists the destination URL. Requests to private IP ranges (169.254.x.x, 10.x.x.x, 172.16–31.x.x, 192.168.x.x, localhost, 127.0.0.1) are explicitly blocked. Cloud metadata endpoints (169.254.169.254) are blocked.

---

## PART 4 — EXTENDED CYBER ATTACK SURFACE (Checks 23–32)

Common attack vectors that still slip through even after OWASP review.

### 23 — XSS protection
All user-controlled data is escaped before rendering in HTML context. Dangerous patterns (`innerHTML`, `dangerouslySetInnerHTML`, `document.write`, `eval`) have been audited and are either absent or justified with sanitization. A Content Security Policy (CSP) header is configured and tested.

### 24 — CSRF protection
All state-changing server endpoints (POST, PUT, PATCH, DELETE) are protected by CSRF tokens or `SameSite=Strict` / `SameSite=Lax` cookie policy. GET requests perform no state changes.

### 25 — Rate limiting on all sensitive endpoints
Rate limiting enforced server-side on: login, signup, password reset, OTP/verification, contact forms, API endpoints, and any AI-powered routes. Per-IP and per-user rate limits both exist.

### 26 — HTTP security headers present
All of the following headers must be present and correctly configured in production HTTP responses:
- `Strict-Transport-Security` (HSTS)
- `X-Frame-Options: DENY` or `frame-ancestors 'none'` in CSP
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy`
- `Content-Security-Policy`

### 27 — No sensitive data exposed in URLs
Passwords, session tokens, API keys, PII, and authentication parameters must not appear in URL query strings or path segments. They are logged by servers, stored in browser history, and leaked via the Referer header.

### 28 — Admin and internal endpoints protected
All admin panels, internal dashboards, management APIs, and debug interfaces must be behind strong authentication. Where possible, they must also be behind IP allowlisting or network-level controls (VPN, private subnet).

### 29 — No open redirects
All redirect targets (login redirects, OAuth callbacks, "return to" parameters) are validated against an allowlist of trusted destinations or restricted to relative paths. The application cannot be used to redirect users to attacker-controlled URLs.

### 30 — Supply chain integrity verified
Lockfile is committed and used in CI (`npm ci`, not `npm install`). No packages with known-malicious recent maintainer changes. Suspicious `preinstall`, `postinstall`, or `prepare` scripts in dependencies have been reviewed.

### 31 — Prompt injection protection (if AI features present)
If the application passes any user-controlled input to an LLM: system prompts are strictly separated from user content, all permissions are enforced outside the model in trusted application code, and model output is never directly used as HTML, SQL, shell commands, or filenames without sanitization. N/A if no AI features.

### 32 — Webhook signature verification (if webhooks received)
Every inbound webhook from a third-party provider (Stripe, GitHub, Twilio, Clerk, etc.) has its cryptographic signature verified before the payload is trusted or acted upon. N/A if no inbound webhooks.

---

## PART 5 — CONSOLE & RUNTIME ERRORS (Checks 33–38)

Zero visible errors on launch day. Every item must be verified against the live production build.

### 33 — No JavaScript console errors
Load the production build in a clean browser session (incognito). The browser console must be clean — no errors, no uncaught exceptions, no failed resource loads. Any console errors are a FAIL.

### 34 — No unhandled promise rejections
Verify the browser console and server logs show no `UnhandledPromiseRejectionWarning` or equivalent. All async operations must have proper `.catch()` or `try/catch` error handling.

### 35 — No 404 errors for linked assets
All CSS files, JavaScript bundles, images, fonts, and other assets referenced in the HTML must return HTTP 200. Use Lighthouse, DevTools Network tab, or a link crawler to verify. Missing assets are a FAIL.

### 36 — No mixed content warnings
Every resource (scripts, stylesheets, images, API calls, WebSocket connections, embeds) loaded on HTTPS pages must itself be served over HTTPS. Any HTTP-scheme resource on an HTTPS page is a security warning and a FAIL.

### 37 — No deprecated API or browser API warnings
Review the browser console and build output for deprecation warnings. Prioritize and address any deprecations that will break in an upcoming browser or Node.js version release.

### 38 — Core Web Vitals in acceptable range
Run Lighthouse against the production URL. Core Web Vitals (LCP, CLS, FID/INP) must be in the "Needs Improvement" or better range. A failing Core Web Vitals score harms SEO and user experience. Document known exceptions with justification.

---

## PART 6 — DEPLOYMENT & OPERATIONAL READINESS (Checks 39–42)

Confirm the landing zone is clear before final approach.

### 39 — Production database ready
Production database is connected, all migrations are applied and verified, connection pooling is configured correctly, and both read and write access have been tested end-to-end. A database backup has been taken immediately before deployment.

### 40 — SSL certificate valid and auto-renewing
HTTPS is active on the production domain. The SSL certificate is valid, covers the correct domain(s), and auto-renewal is configured and confirmed working (check expiry date — must be >30 days remaining at launch).

### 41 — Rollback plan documented and tested
A clear, written procedure exists to roll back to the previous working state if deployment introduces a critical bug. The rollback procedure has been tested at least once. Deployments with no rollback plan are a FAIL.

### 42 — Post-deployment smoke tests passing
A defined set of critical user flow tests (sign up, log in, core feature, payment if applicable) has been run against the production environment after deployment and all flows completed successfully. Manual or automated — documented either way.

---

## Official sources (for deeper reference during remediation)

- OWASP Top 10 (2021) — owasp.org/Top10
- OWASP Application Security Verification Standard (ASVS)
- OWASP Cheat Sheet Series — cheatsheetseries.owasp.org
- NIST SP 800-115 (Technical Guide to Information Security Testing)
- CWE/SANS Top 25 Most Dangerous Software Weaknesses
- Mozilla Observatory — HTTP Security Headers (observatory.mozilla.org)
- Web.dev — Core Web Vitals
- GitHub Actions Security Hardening Guide

**Launch standard:** ship when all 42 gates are verified with evidence. Re-run after any meaningful changes to codebase, infrastructure, dependencies, or authentication. Godspeed, sir.
