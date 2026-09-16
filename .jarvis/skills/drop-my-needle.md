# Skill Manifest: Drop My Needle

**Command:** `/JARVIS, drop my needle`
**Trigger:** Activated when the developer invokes the exact phrase above in a direct chat message.
**Nature:** Pre-launch website quality and compliance checklist. Educational audit — not a legal review, penetration test, or guarantee. Do not launch until all applicable items are verified with evidence.

**The rule this manifest enforces:** if you cannot point to the code, live page, configuration, or URL that proves a requirement is met, treat it as missing — FAIL, never PASS.

Each check below is one "needle" that must pass before the site goes live. Phase 2 (Threat Audit) evaluates all 46 checks. Phase 3 auto-fixes code-level issues (Modality A) or halts for developer action (Modality B). Findings are written to `.jarvis/STATE.md` under the "Drop My Needle Ledger" section.

---

## PART 1 — PERFORMANCE & TECHNICAL INFRASTRUCTURE (Checks 01–10)

Stop the shortcuts that kill a site under real traffic.

### 01 — Rate limiting
Implement rate limiting on all traffic entry points — login, signup, API endpoints, form submissions, and any AI routes. Per-IP and per-user ceilings must exist and be enforced server-side.

### 02 — API spending caps and usage limits
Set hard spending caps and quota limits on all paid external APIs (OpenAI, Stripe, SendGrid, Twilio, etc.) to prevent runaway costs. Caps must exist in the provider dashboard, not just in application code.

### 03 — Error handling, loading states, and empty states
Every async operation must show a loading state while pending, a meaningful error message on failure, and a designed empty state when results are zero. Blank or frozen UI is a FAIL.

### 04 — Failed request and API timeout handling
Implement retry logic with exponential backoff and user-facing fallback messages for failed HTTP requests and timed-out API calls. Silent failures that leave the user with a broken page are a FAIL.

### 05 — Duplicate submission and payment prevention
Use idempotency keys, server-side deduplication, or UI submission locks to prevent users from submitting forms or triggering payments multiple times. Double charges are a FAIL.

### 06 — Database query optimization and indexes
Profile slow queries. Add indexes on columns used in WHERE, ORDER BY, JOIN, and GROUP BY clauses. Eliminate N+1 query patterns. Missing indexes on high-traffic queries are a FAIL.

### 07 — Large result pagination
All endpoints or UI views returning potentially large datasets must paginate, use cursor-based pagination, or implement infinite scroll with hard limits. Unbounded queries are a FAIL.

### 08 — File compression and upload size limits
Compress image and asset uploads server-side (lossy where acceptable). Enforce upload file size limits with clear user feedback when the limit is exceeded. No server-side limit is a FAIL.

### 09 — Request caching and uptime monitoring
Implement caching for repeated expensive requests (HTTP cache headers, CDN, in-memory, or Redis). Set up uptime monitoring with alerting (UptimeRobot, Better Uptime, or similar) before go-live.

### 10 — Error logging, load testing, and backup restoration
Integrate an error logging service (Sentry, Rollbar, Datadog, or similar). Confirm that backups exist and have been successfully restored at least once. Untested backups are a FAIL.

---

## PART 2 — AESTHETICS & VISUAL DESIGN (Checks 11–20)

Ship something that looks intentional and professional, not like a default AI output.

### 11 — No purple gradients
Audit the stylesheet and design system. Any default purple-to-blue or purple-to-pink gradient that was not deliberately chosen as part of the brand must be replaced with a curated, branded color palette.

### 12 — No pill-shaped buttons
Replace pill (`border-radius: 9999px`) buttons that are not part of a deliberate design system with buttons that match the brand's shape language. Default rounded-full CTAs are a design red flag.

### 13 — No emoji used as UI icons
Replace emoji used as functional interface icons (🔒, ✅, ➡️, etc.) with a proper icon library (Lucide, Heroicons, Phosphor, Tabler) for consistency, scalability, and accessibility.

### 14 — No over-the-top scroll animations
Remove or significantly reduce excessive scroll-triggered animations, parallax layers, or staggered cascade reveals that slow perceived performance, cause layout shift, or feel gimmicky rather than purposeful.

### 15 — No cursor animations
Remove custom cursor animations, cursor trails, magnetic cursor effects, or cursor-follow elements unless they are demonstrably core to the product's interaction model.

### 16 — No vague or generic hero text
Replace placeholder-feeling hero headlines ("Build faster", "The future of X", "Everything you need") with specific, benefit-driven copy that names who the product is for and what specific problem it solves.

### 17 — No em dashes in marketing copy
Search for em dashes (—) in all landing page and marketing copy. Replace with cleaner sentence construction, commas, colons, or parentheses. Em dashes are a statistically significant AI writing signal.

### 18 — No AI-generated stock photography
Replace generic AI-generated stock imagery (overly smooth faces, surreal office scenes, impossible hands) with real photography, authentic product screenshots, or custom illustration. Uncanny stock is a trust killer.

### 19 — No AI slop marketing copy
Audit all landing page copy for AI filler language ("game-changing", "seamlessly", "unlock your potential", "revolutionize", "leverage", "robust solution"). Rewrite for specificity and human voice.

### 20 — No fake social proof
Remove any fabricated reviews, inflated testimonials, fake "X customers served" counters, or unverifiable metric claims. Every social proof element must be real and verifiable, or it must be removed.

---

## PART 3 — LAUNCH REQUIREMENTS (Checks 21–27)

The non-negotiable gates — if any fail, the site does not ship.

### 21 — Custom domain connected
The site must resolve from a custom domain. Builder subdomains (*.vercel.app, *.netlify.app, *.webflow.io, *.framer.app) are not acceptable for a public launch unless the product genuinely has no domain yet.

### 22 — Favicon present
A favicon must exist and render correctly in browser tabs, bookmark bars, and mobile home screens. Check all standard sizes: 16×16, 32×32, 180×180 (apple-touch-icon), and 192×192 (Android). Missing favicon is a FAIL.

### 23 — Builder / platform branding removed
Audit the visible UI for "Made with [Tool]", "Powered by [Builder]", "Built on [Platform]", or similar attribution badges. Remove all unless contractually required by the builder's free-tier terms.

### 24 — Privacy policy page live and linked
A privacy policy must exist at a public, stable URL. It must be linked in the site footer and from every form that collects user data or email. Absence is a FAIL and a legal risk.

### 25 — Terms and conditions page live and linked
Terms of service must exist at a public URL. Linked in the site footer and from every signup or purchase flow. Required for any site collecting accounts or money.

### 26 — Cookie policy page live and linked
A cookie policy must exist and be linked from the cookie consent banner and the site footer. Required wherever tracking or analytics cookies are set.

### 27 — Refund policy live and linked (if selling)
If the site sells products or subscriptions, a refund and return policy must exist at a public URL and be linked from checkout confirmation and the site footer. N/A if no commerce.

---

## PART 4 — DATA PRIVACY & CONSENT (Checks 28–32)

Collect only what you need. Tell users clearly. Respect the law.

### 28 — Cookie consent mechanism implemented
If the site uses cookies beyond strictly necessary session management (analytics, advertising, tracking, preferences), a cookie consent banner with genuine Accept / Decline / Manage options must be shown to new visitors before any non-essential cookies fire.

### 29 — Form consent checkboxes present
Forms that collect personal data for marketing, newsletters, or data processing must include an unchecked consent checkbox with a clear label explaining what the user is consenting to. Pre-checked boxes are illegal in many jurisdictions.

### 30 — Data minimization enforced
Audit every form and API endpoint. Remove fields that are not strictly necessary for the stated purpose. Do not store data longer than the period justified by its use. "Just in case" collection is a FAIL.

### 31 — Analytics tracking verified and disclosed
Confirm analytics (GA4, Plausible, Fathom, PostHog, etc.) is firing correctly on production. Confirm it is disclosed in the privacy policy. Confirm IP anonymization is enabled where required by applicable law.

### 32 — Third-party embeds audited
List every third-party script, embed, widget, font provider, and SDK loaded by the site. Confirm each is disclosed in the privacy policy, is necessary, and complies with applicable data protection law.

---

## PART 5 — ACCESSIBILITY (Checks 33–37)

A site that excludes users due to disability is both an ethical and legal problem.

### 33 — WCAG 2.1 AA compliance baseline
Run an automated accessibility audit (axe DevTools, Lighthouse Accessibility, or WAVE). All critical and serious violations must be addressed before launch. Document known acceptable exceptions.

### 34 — All images have descriptive alt text
Every content image must have a meaningful, descriptive `alt` attribute. Purely decorative images must use `alt=""`. Images with missing `alt` attributes are a hard FAIL.

### 35 — Color contrast meets minimum ratio
All text must achieve at least 4.5:1 contrast ratio against its background (3:1 for large text ≥18pt or bold ≥14pt). Check every foreground/background combination in the live design.

### 36 — All forms are keyboard navigable
Every form input, button, select, and interactive element must be reachable and operable using only a keyboard (Tab, Shift+Tab, Enter, Space, arrow keys). Visible focus indicators must be present.

### 37 — Skip navigation link present
A "Skip to main content" link must exist at the top of each page, visible on keyboard focus. Required for screen reader and keyboard-only users to bypass repeated navigation.

---

## PART 6 — CONTENT & TRUST (Checks 38–43)

The site must feel credible and trustworthy to first-time visitors.

### 38 — Clear and descriptive button labels
Every call-to-action and button must have specific, action-oriented labels ("Start free trial", "Download report", "Save changes") rather than generic labels ("Click here", "Go", "Submit"). Vague labels are a FAIL.

### 39 — No unsupported claims
Remove or substantiate every claim about results, efficacy, speed, or comparisons. Unsubstantiated superlatives ("the best", "the fastest", "guaranteed results") that cannot be verified are a legal and trust risk.

### 40 — Business contact details present
The site must display a business or creator name, a contact email address, and a physical address where required by law (e.g. required by EU distance selling rules, GDPR, and consumer protection laws in many jurisdictions).

### 41 — Image copyright verified
Every image used on the site must be: original, licensed for commercial web use, or sourced from a royalty-free provider with the correct license type. Unlicensed stock imagery is a FAIL.

### 42 — No broken internal or external links
Crawl all internal links and spot-check key external links. Fix or remove any that return 404 or lead to dead destinations. Broken links harm trust and SEO.

### 43 — Custom 404 error page exists
A branded, helpful 404 page must exist with navigation back to the main site and a search or next-step prompt. The server's default error page is a FAIL.

---

## PART 7 — LEGAL REVIEW (Checks 44–46)

Flag what needs professional attention before the site handles real users or money.

### 44 — Applicable legal frameworks identified
Based on where the business operates and where users are located, identify which legal requirements apply: GDPR (EU), CCPA (California), PECR (UK), local consumer protection laws, e-commerce regulations, sector-specific rules (health, finance, children's data).

### 45 — Legal risks flagged for developer review
Flag every identified legal gap, ambiguous claim, missing disclosure, or unresolved compliance issue for the developer's explicit review. Do not mark this PASS unless every flagged item has a documented resolution or accepted risk.

### 46 — No remaining compliance gaps
Confirm that all requirements identified in Checks 44–45 have either been addressed in the codebase or explicitly accepted in writing as known risk by the developer. If any gap is unresolved, this check is FAIL.

---

## Official sources (for deeper reference during remediation)

- WCAG 2.1 Guidelines (W3C)
- GDPR (Regulation (EU) 2016/679)
- CCPA (California Consumer Privacy Act)
- PECR (Privacy and Electronic Communications Regulations, UK)
- FTC Guidelines on Endorsements and Testimonials
- Web.dev Performance Best Practices
- OWASP Input Validation Cheat Sheet
- axe Accessibility Rules

**Launch standard:** ship when each needle is verified with evidence, not when the checklist has simply been read. Re-run after meaningful changes to UI, copy, legal pages, data collection, or third-party integrations.
