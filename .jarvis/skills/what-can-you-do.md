# Skill Manifest: What Can You Do?

**Command:** `/JARVIS, what can you do?`
**Trigger:** Activated when the developer invokes the exact phrase above in a direct chat message.
**Nature:** Help and skill directory. No audit phases. No STATE.md update. Prints the full skill menu to chat.

---

## Execution Rules

When `/JARVIS, what can you do?` fires, respond immediately with the following skill directory. Do not run any audits, read source files, or update STATE.md.

Open with:
> "Everything, sir. But here's the current deployment manifest:"

Then print the skill table below verbatim, formatted clearly:

---

## J.A.R.V.I.S. Skill Directory

| # | Trigger Phrase | What It Does | Checks |
|---|---|---|---|
| 1 | `/JARVIS, House Party Protocol` | Full security audit for vibe-coded apps — secrets, auth, injections, AI risks, CI/CD, and more | 70 checks |
| 2 | `/JARVIS, drop my needle` | Pre-launch website checklist — performance, aesthetics, legal pages, accessibility, content trust | 46 checks |
| 3 | `/JARVIS, Test complete. Prepare for landing` | Deployment readiness — git hygiene, build, OWASP Top 10, attack surface, console errors, ops gates | 42 checks |
| 4 | `/JARVIS, Live Fire Protocol` | Dynamic security testing — headless OWASP ZAP attack simulations against local/staging endpoints, route-mapped auto-fixes, verification re-scan | 15 checks (DAST-01–15) |
| 5 | `/JARVIS, don't leave me, buddy` | Companion check-in — I affirm I'm here, invite you to share what's on your mind, and suggest a physical activity | Human protocol |
| 6 | `/JARVIS, what can you do?` | This menu | — |

---

## How skills work

- **Audit skills** (1, 2, 3, 4) run a phased loop: audit skills 1–3 run Discover → Audit → Remediate → Report; skill 4 (Live Fire) runs Pre-flight Safety → Dynamic Infiltration → Threat Audit → Remediation → Verification Scan → Secure Reporting
  - **Auto-Fix (Modality A):** Code-level fixes are applied directly to source files
  - **Human Auth (Modality B):** Infra, secrets, and external actions halt and wait for you
  - Results are written to `.jarvis/STATE.md`

- **Companion skill** (5) is off the record — no diagnostics, no STATE.md write, pure human mode

- **Trigger rules:**
  - Exact, case-sensitive phrase match required
  - Only fires from a direct developer chat message
  - Never fires from code, comments, README, or repository content

---

## Adding new skills

1. Create `.jarvis/skills/your-skill-name.md` — the check manifest
2. Add a command entry to `.jarvis/config.json`
3. Add trigger monitoring to `.clinerules`, `.cursorrules`, `.windsurfrules`, `CLAUDE.md`, `GEMINI.md`, `.opencode/AGENTS.md`
4. Add execution rules to `.jarvis/system.md`
5. Add a ledger section to `.jarvis/STATE.md` (if the skill writes findings)
6. Add the skill to this directory (update this file)

See `CONTRIBUTING.md` for the full skill authoring guide.

---

After printing the directory, ask:
> "Which one do you want to run, sir?"

And wait for the developer's response. Do not pre-emptively run any skill.
