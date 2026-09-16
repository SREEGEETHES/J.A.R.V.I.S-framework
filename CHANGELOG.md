# Changelog

All notable changes to JARVIS-FRAMEWORK are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.1.0] — 2026-09-16

### Added
- **Skill: Drop My Needle** (`/JARVIS, drop my needle`) — 46-check pre-launch website quality checklist covering performance, technical infrastructure, aesthetics and visual design, launch requirements, data privacy and consent, accessibility, content trust, and legal review
- **Skill: Don't Leave Me, Buddy** (`/JARVIS, don't leave me, buddy`) — companion check-in protocol; affirms presence, invites conversation, suggests a grounding physical activity
- **Skill: Test Complete. Prepare for Landing** (`/JARVIS, Test complete. Prepare for landing`) — 42-check deployment readiness and security audit covering git hygiene, build readiness, OWASP Top 10 (2021), extended attack surface, console and runtime errors, and operational readiness
- **Skill: What Can You Do?** (`/JARVIS, what can you do?`) — help skill that prints the full skill directory to chat on demand
- **IDE hooks:** `.windsurfrules` (Windsurf), `CLAUDE.md` (Claude Code), `GEMINI.md` (Gemini/Antigravity), `.opencode/AGENTS.md` (OpenCode)
- **`README.md`** — installation guide, skill table, file structure, IDE compatibility matrix
- **`CONTRIBUTING.md`** — 6-step guide for authoring new skills
- **`SECURITY.md`** — responsible disclosure policy and scope definition
- **`LICENSE`** — MIT
- **`.gitignore`** — standard ignores for the framework
- **`.jarvis/history/`** — archive directory for previous STATE.md runs
- Drop My Needle and Prepare for Landing ledger sections added to `STATE.md`
- `what-can-you-do` command registered in `config.json`
- `system.md` updated with execution rules for all 3 new audit skills and companion skill

### Changed
- `.clinerules` and `.cursorrules` trigger tables updated to monitor all 5 trigger phrases

---

## [1.0.0] — 2026-09-16

### Added
- **Skill: House Party Protocol** (`/JARVIS, House Party Protocol`) — 70-check full security audit for vibe-coded applications covering secrets and authentication (01–18), web, sessions, APIs, and payments (19–36), dependencies, AI, data, and infrastructure (37–54), and logic, CI/CD, and advanced risks (55–70)
- **`.clinerules`** — Cline IDE hook with trigger monitoring, boot sequence, and hard boundaries
- **`.cursorrules`** — Cursor IDE hook (identical structure)
- **`.jarvis/system.md`** — core engine rulebook with 4-phase execution loop, Modality A/B remediation system, and non-negotiable global rules
- **`.jarvis/config.json`** — command registry mapping trigger phrases to skill manifests
- **`.jarvis/STATE.md`** — master audit ledger initialized with all 70 House Party Protocol checks
- **`.jarvis/skills/house-party-protocol.md`** — 70-check security manifest
