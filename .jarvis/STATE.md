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
**Status:** `NOT YET RUN`
**Last run:** —
**Trigger context supplied by developer:** —

> This ledger is overwritten each time `/JARVIS, Test complete. Prepare for landing`
> is run. Educational checklist audit — not a penetration test, legal advice,
> or a deployment guarantee.

## Run summary

| Metric | Count |
|---|---|
| PASS | — |
| FAIL | — |
| WAITING_AUTH | — |
| N/A | — |
| Total checks | 42 |

## Open items requiring developer authorization

_(populated automatically at the end of a run — see the `WAITING_AUTH` rows below)_

---

## Full ledger

| Gate ID | Gate Name | Status | Evidence | Remediation (taken or needed) |
|---|---|---|---|---|
| 01 | No uncommitted changes in working tree | — | — | — |
| 02 | No sensitive files tracked by git | — | — | — |
| 03 | .gitignore is complete and correct | — | — | — |
| 04 | Branch hygiene verified | — | — | — |
| 05 | Commit history is clean | — | — | — |
| 06 | No merge conflict markers remaining | — | — | — |
| 07 | Production environment variables configured | — | — | — |
| 08 | .env.example is present and complete | — | — | — |
| 09 | Production build completes without errors | — | — | — |
| 10 | All production dependencies are pinned | — | — | — |
| 11 | No dev dependencies in production build | — | — | — |
| 12 | Build output is clean and contains no secrets | — | — | — |
| 13 | A01: Broken Access Control | — | — | — |
| 14 | A02: Cryptographic Failures | — | — | — |
| 15 | A03: Injection | — | — | — |
| 16 | A04: Insecure Design | — | — | — |
| 17 | A05: Security Misconfiguration | — | — | — |
| 18 | A06: Vulnerable and Outdated Components | — | — | — |
| 19 | A07: Identification and Authentication Failures | — | — | — |
| 20 | A08: Software and Data Integrity Failures | — | — | — |
| 21 | A09: Security Logging and Monitoring Failures | — | — | — |
| 22 | A10: Server-Side Request Forgery (SSRF) | — | — | — |
| 23 | XSS protection | — | — | — |
| 24 | CSRF protection | — | — | — |
| 25 | Rate limiting on sensitive endpoints | — | — | — |
| 26 | HTTP security headers present | — | — | — |
| 27 | No sensitive data exposed in URLs | — | — | — |
| 28 | Admin and internal endpoints protected | — | — | — |
| 29 | No open redirects | — | — | — |
| 30 | Supply chain integrity verified | — | — | — |
| 31 | Prompt injection protection | — | — | — |
| 32 | Webhook signature verification | — | — | — |
| 33 | No JavaScript console errors | — | — | — |
| 34 | No unhandled promise rejections | — | — | — |
| 35 | No 404 errors for linked assets | — | — | — |
| 36 | No mixed content warnings | — | — | — |
| 37 | No deprecated API warnings | — | — | — |
| 38 | Core Web Vitals in acceptable range | — | — | — |
| 39 | Production database ready | — | — | — |
| 40 | SSL certificate valid and auto-renewing | — | — | — |
| 41 | Rollback plan documented and tested | — | — | — |
| 42 | Post-deployment smoke tests passing | — | — | — |

---

**Launch standard:** ship when all 42 gates are verified with evidence.
Re-run after any meaningful changes to the codebase, infrastructure,
dependencies, or authentication. Godspeed, sir.

