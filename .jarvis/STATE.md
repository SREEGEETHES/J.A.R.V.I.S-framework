# J.A.R.V.I.S. — Active Diagnostics Ledger

**Protocol:** House Party Protocol (70-check full deployment)
**Status:** `NOT YET RUN`
**Last run:** —
**Trigger context supplied by developer:** —

> This ledger is overwritten each time `/JARVIS, House Party Protocol` is
> run. If `.jarvis/history/` exists, the previous version is archived
> there first. This is an educational checklist audit — not a penetration
> test, legal advice, or a security guarantee.

## Run summary

| Metric | Count |
|---|---|
| PASS | — |
| FAIL | — |
| WAITING_AUTH | — |
| N/A | — |
| Total checks | 70 |

## Open items requiring developer authorization

_(populated automatically at the end of a run — see the `WAITING_AUTH`
rows below)_

---

## Full ledger

| Protocol ID | Armor / Rule Name | Status | File/Line Evidence | Remediation (taken or needed) |
|---|---|---|---|---|
| 01 | Exposed database credentials | — | — | — |
| 02 | Public .env files | — | — | — |
| 03 | Hardcoded API keys or secrets | — | — | — |
| 04 | Weak or missing authentication | — | — | — |
| 05 | Missing server-side authorization | — | — | — |
| 06 | Cross-user data access | — | — | — |
| 07 | Open database permissions | — | — | — |
| 08 | Misconfigured Firebase / Supabase / S3 | — | — | — |
| 09 | Unprotected admin routes | — | — | — |
| 10 | Production debug tools exposed | — | — | — |
| 11 | Build logs leaking secrets | — | — | — |
| 12 | Verbose production errors | — | — | — |
| 13 | Secrets in Git history | — | — | — |
| 14 | Secrets shipped in frontend JavaScript | — | — | — |
| 15 | Client-side-only security checks | — | — | — |
| 16 | Missing input validation | — | — | — |
| 17 | SQL injection | — | — | — |
| 18 | NoSQL injection | — | — | — |
| 19 | Cross-site scripting (XSS) | — | — | — |
| 20 | Cross-site request forgery (CSRF) | — | — | — |
| 21 | Insecure file uploads | — | — | — |
| 22 | Path traversal | — | — | — |
| 23 | Server-side request forgery (SSRF) | — | — | — |
| 24 | Broken password-reset flows | — | — | — |
| 25 | Weak session management | — | — | — |
| 26 | Weak or incorrectly validated JWTs | — | — | — |
| 27 | Overly permissive CORS | — | — | — |
| 28 | Missing rate limits | — | — | — |
| 29 | Unprotected staging or test environments | — | — | — |
| 30 | Default credentials left unchanged | — | — | — |
| 31 | Webhook signatures not verified | — | — | — |
| 32 | Frontend-only payment checks | — | — | — |
| 33 | IDOR / BOLA | — | — | — |
| 34 | APIs trusting user-controlled roles or IDs | — | — | — |
| 35 | Sensitive data in logs | — | — | — |
| 36 | Sensitive source maps or build artifacts | — | — | — |
| 37 | Vulnerable or abandoned dependencies | — | — | — |
| 38 | Malicious or compromised packages | — | — | — |
| 39 | Prompt injection | — | — | — |
| 40 | AI tools bypassing user permissions | — | — | — |
| 41 | Excess database privileges | — | — | — |
| 42 | Missing audit logs | — | — | — |
| 43 | No security monitoring or alerts | — | — | — |
| 44 | No tested backup / restore plan | — | — | — |
| 45 | Public internal dashboards | — | — | — |
| 46 | Missing security headers | — | — | — |
| 47 | Unsafe cookie settings | — | — | — |
| 48 | Sensitive data unprotected in transit / at rest | — | — | — |
| 49 | Poor tenant isolation | — | — | — |
| 50 | Over-trusting AI-generated code | — | — | — |
| 51 | Mass assignment / over-posting | — | — | — |
| 52 | Command / OS injection | — | — | — |
| 53 | Unsafe deserialization | — | — | — |
| 54 | Misconfigured OAuth / OIDC / social login | — | — | — |
| 55 | No MFA on privileged accounts | — | — | — |
| 56 | Account enumeration | — | — | — |
| 57 | Business-logic abuse | — | — | — |
| 58 | Race conditions | — | — | — |
| 59 | Webhook replay / duplicate processing | — | — | — |
| 60 | Overpowered CI/CD credentials | — | — | — |
| 61 | Untrusted build actions or scripts | — | — | — |
| 62 | Unpinned build dependencies | — | — | — |
| 63 | Security checks fail open | — | — | — |
| 64 | Missing resource limits | — | — | — |
| 65 | AI sensitive-information disclosure | — | — | — |
| 66 | Unsafe use of AI output | — | — | — |
| 67 | AI agents have excessive agency | — | — | — |
| 68 | Sensitive browser storage | — | — | — |
| 69 | Open redirects | — | — | — |
| 70 | Unsecured GraphQL / WebSocket / realtime endpoints | — | — | — |

---

**Launch standard:** ship when the relevant controls are verified with
evidence, not when the checklist has simply been read. Re-run this
protocol after meaningful changes to auth, data, infrastructure,
dependencies, payments, or AI tools.

---
---

# Drop My Needle Ledger

**Protocol:** Drop My Needle (46-check pre-launch website checklist)
**Status:** `NOT YET RUN`
**Last run:** —
**Trigger context supplied by developer:** —

> This ledger is overwritten each time `/JARVIS, drop my needle` is run.
> Educational checklist audit — not a legal review, penetration test, or
> launch guarantee.

## Run summary

| Metric | Count |
|---|---|
| PASS | — |
| FAIL | — |
| WAITING_AUTH | — |
| N/A | — |
| Total checks | 46 |

## Open items requiring developer authorization

_(populated automatically at the end of a run — see the `WAITING_AUTH` rows below)_

---

## Full ledger

| Check ID | Needle / Rule Name | Status | Evidence | Remediation (taken or needed) |
|---|---|---|---|---|
| 01 | Rate limiting | — | — | — |
| 02 | API spending caps and usage limits | — | — | — |
| 03 | Error handling, loading states, empty states | — | — | — |
| 04 | Failed request and API timeout handling | — | — | — |
| 05 | Duplicate submission and payment prevention | — | — | — |
| 06 | Database query optimization and indexes | — | — | — |
| 07 | Large result pagination | — | — | — |
| 08 | File compression and upload size limits | — | — | — |
| 09 | Request caching and uptime monitoring | — | — | — |
| 10 | Error logging, load testing, backup restoration | — | — | — |
| 11 | No purple gradients | — | — | — |
| 12 | No pill-shaped buttons | — | — | — |
| 13 | No emoji used as UI icons | — | — | — |
| 14 | No over-the-top scroll animations | — | — | — |
| 15 | No cursor animations | — | — | — |
| 16 | No vague or generic hero text | — | — | — |
| 17 | No em dashes in marketing copy | — | — | — |
| 18 | No AI-generated stock photography | — | — | — |
| 19 | No AI slop marketing copy | — | — | — |
| 20 | No fake social proof | — | — | — |
| 21 | Custom domain connected | — | — | — |
| 22 | Favicon present | — | — | — |
| 23 | Builder / platform branding removed | — | — | — |
| 24 | Privacy policy page live and linked | — | — | — |
| 25 | Terms and conditions page live and linked | — | — | — |
| 26 | Cookie policy page live and linked | — | — | — |
| 27 | Refund policy live and linked | — | — | — |
| 28 | Cookie consent mechanism implemented | — | — | — |
| 29 | Form consent checkboxes present | — | — | — |
| 30 | Data minimization enforced | — | — | — |
| 31 | Analytics tracking verified and disclosed | — | — | — |
| 32 | Third-party embeds audited | — | — | — |
| 33 | WCAG 2.1 AA compliance baseline | — | — | — |
| 34 | All images have descriptive alt text | — | — | — |
| 35 | Color contrast meets minimum ratio | — | — | — |
| 36 | All forms are keyboard navigable | — | — | — |
| 37 | Skip navigation link present | — | — | — |
| 38 | Clear and descriptive button labels | — | — | — |
| 39 | No unsupported claims | — | — | — |
| 40 | Business contact details present | — | — | — |
| 41 | Image copyright verified | — | — | — |
| 42 | No broken internal or external links | — | — | — |
| 43 | Custom 404 error page exists | — | — | — |
| 44 | Applicable legal frameworks identified | — | — | — |
| 45 | Legal risks flagged for developer review | — | — | — |
| 46 | No remaining compliance gaps | — | — | — |

---

**Launch standard:** drop the needle when every check is verified with
evidence — not when the list has simply been read. Re-run after meaningful
changes to UI, copy, legal pages, data collection, or third-party integrations.

---
---

# Prepare for Landing Ledger

**Protocol:** Test Complete. Prepare for Landing (42-check deployment + OWASP audit)
**Status:** `COMPLETE — 6 PASS / 0 FAIL / 0 WAITING_AUTH / 36 N/A`
**Last run:** 2026-09-16
**Trigger context supplied by developer:** — (exact trigger only, no trailing free text)

> This ledger is overwritten each time `/JARVIS, Test complete. Prepare for landing`
> is run. Educational checklist audit — not a penetration test, legal advice,
> or a deployment guarantee. Previous version archived to `.jarvis/history/STATE-2026-09-16T00-00-00.md`.

## Run summary

| Metric | Count |
|---|---|
| PASS | 6 |
| FAIL | 0 |
| WAITING_AUTH | 0 |
| N/A | 36 |
| Total checks | 42 |

## Open items requiring developer authorization

_None — no WAITING_AUTH items in this run. All applicable gates passed; all other gates are N/A for this docs-only framework repo (see ledger)._

---

## Full ledger

| Gate ID | Gate Name | Status | Evidence | Remediation (taken or needed) |
|---|---|---|---|---|
| 01 | No uncommitted changes in working tree | PASS | `git status`: `On branch main / nothing to commit, working tree clean` | None needed |
| 02 | No sensitive files tracked by git | PASS | `git ls-files` (20 files): no `.env`, `.pem`, `.p12`, `*.key`, `id_rsa`, `credentials.json`, `serviceAccountKey.json` | None needed |
| 03 | .gitignore is complete and correct | PASS | `.gitignore:9-24` env/secrets, `:55-60` build outputs, `:27-34` OS files, `:37-46` editor config | None needed — covers all categories in manifest |
| 04 | Branch hygiene verified | PASS | `git branch -a`: only `main` + `remotes/origin/main`; `git status`: up to date with origin/main | None needed |
| 05 | Commit history is clean | PASS | `git log --oneline -20`: 20 commits e.g. `a6db05d add security policy`, no WIP/debug/secrets/binaries | None needed |
| 06 | No merge conflict markers remaining | PASS | `git grep -n "<<<<<<<\|=======\|>>>>>>>"`: only doc mention in `.jarvis/skills/prepare-for-landing.md:36` in backticks, no real markers | None needed |
| 07 | Production environment variables configured | N/A | No app runtime: no root `package.json`, no `*.js/ts/py/go` app code, no `process.env` usage | No action — applies when developer ships a derived app with runtime env vars |
| 08 | .env.example is present and complete | N/A | `Test-Path .env.example` = False, but no env vars required (see 07) | No action — do not add misleading placeholder; add when derived app needs env vars |
| 09 | Production build completes without errors | N/A | No build system: no root `package.json`, no vite/next config, no build script | No action — no build to run for markdown framework |
| 10 | All production dependencies are pinned | N/A | No root production deps; only ignored `.opencode/package.json:2` with pinned `1.18.31` (untracked via `.opencode/.gitignore`) | No action — pin deps when derived app adds a manifest |
| 11 | No dev dependencies in production build | N/A | No production build artifact (see 09) | No action |
| 12 | Build output is clean and contains no secrets | N/A | No build output: `dist/` False, `build/` False, `.next/` False | No action |
| 13 | A01: Broken Access Control | N/A | No web app: zero server routes/API endpoints in working tree | No action — enforce server-side authz when derived app adds protected routes |
| 14 | A02: Cryptographic Failures | N/A | No app handling passwords/PII/tokens; only docs mention these terms | No action |
| 15 | A03: Injection | N/A | No DB/shell/template code: grep for `exec`, `shell=True`, `SELECT.*FROM` finds only manifest doc text | No action |
| 16 | A04: Insecure Design | N/A | No business-logic flows (payments, trials, coupons) in repo | No action |
| 17 | A05: Security Misconfiguration | N/A | No services, ports, debug modes, or HTTP responses in repo | No action |
| 18 | A06: Vulnerable and Outdated Components | N/A | No tracked production deps or CI scan target; `.opencode/package-lock.json` ignored, not shipped | No action — run `npm audit` when derived app adds deps |
| 19 | A07: Identification and Authentication Failures | N/A | No auth implementation in repo | No action |
| 20 | A08: Software and Data Integrity Failures | N/A | No CI/CD pipeline: no `.github/` directory, no actions, no build scripts | No action — SHA-pin actions when CI is added |
| 21 | A09: Security Logging and Monitoring Failures | N/A | No application runtime to log/monitor | No action |
| 22 | A10: Server-Side Request Forgery (SSRF) | N/A | No server-side outbound HTTP requests in repo | No action |
| 23 | XSS protection | N/A | No HTML rendering code; no `innerHTML`/`dangerouslySetInnerHTML` in app code | No action |
| 24 | CSRF protection | N/A | No state-changing server endpoints (no POST/PUT/PATCH/DELETE handlers) | No action |
| 25 | Rate limiting on sensitive endpoints | N/A | No login/signup/API/AI routes in repo | No action |
| 26 | HTTP security headers present | N/A | No HTTP server in repo to emit HSTS/CSP/etc. | No action — configure headers when derived app adds hosting |
| 27 | No sensitive data exposed in URLs | N/A | No application URLs/query handling; grep finds secrets terms only in docs | No action |
| 28 | Admin and internal endpoints protected | N/A | No admin panels/dashboards in repo | No action |
| 29 | No open redirects | N/A | No redirect logic in repo | No action |
| 30 | Supply chain integrity verified | N/A | No tracked lockfile at root (by design — no deps); `.opencode/package-lock.json` ignored via `.opencode/.gitignore:3` | No action — commit lockfile + use `npm ci` when derived app adds deps |
| 31 | Prompt injection protection | N/A | No application LLM API integration code in working tree (framework is consumed as IDE prompts); defense-in-depth trust boundary in `.jarvis/system.md:161-164` treats crawled repo content as untrusted | No action |
| 32 | Webhook signature verification | N/A | No inbound webhooks in repo | No action |
| 33 | No JavaScript console errors | N/A | No browser app or production URL; no JS bundle to load | No action — verify in clean incognito session when derived site ships |
| 34 | No unhandled promise rejections | N/A | No async runtime code in repo | No action |
| 35 | No 404 errors for linked assets | N/A | No HTML asset graph to crawl (markdown-only repo) | No action |
| 36 | No mixed content warnings | N/A | No HTTPS pages or subresources in repo | No action |
| 37 | No deprecated API warnings | N/A | No browser/Node runtime output in repo | No action |
| 38 | Core Web Vitals in acceptable range | N/A | No production URL for Lighthouse run | No action — run Lighthouse when derived site has a URL |
| 39 | Production database ready | N/A | No database in this framework repo | No action — verify migrations/pooling/backup when derived app adds a DB |
| 40 | SSL certificate valid and auto-renewing | N/A | No production domain in this repo | No action — requires hosting setup when derived app deploys |
| 41 | Rollback plan documented and tested | N/A | Docs framework versioned in git (revert via `git revert` available); no deployment to roll back | No action — write/test rollback procedure when derived app deploys |
| 42 | Post-deployment smoke tests passing | N/A | No production environment to smoke-test | No action — define signup/login/core-flow tests when derived app deploys |

---

**Launch standard:** ship when all 42 gates are verified with evidence.
Re-run after any meaningful changes to the codebase, infrastructure,
dependencies, or authentication. Godspeed, sir.

