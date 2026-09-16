<div align="center">

# J.A.R.V.I.S. Framework

**Just A Rather Very Intelligent System**

*A trigger-phrase skill framework for AI coding agents.*

[![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)

</div>

---

## What is JARVIS-FRAMEWORK?

JARVIS-FRAMEWORK is a **meta-prompting and skill-dispatch system** that lets you invoke specialized AI behaviors in your IDE by typing a trigger phrase — no plugins, no extensions, no setup beyond dropping the repo into your project.

It works by installing hook files (`.clinerules`, `.cursorrules`, `CLAUDE.md`, `GEMINI.md`, `.windsurfrules`) that AI coding agents read automatically at the start of every session. From that point, any trigger phrase you type in chat fires the corresponding skill.

---

## Quickstart

### Option 1 — Clone into your project
```bash
git clone https://github.com/YOUR_USERNAME/jarvis-framework .jarvis-framework
cp -r .jarvis-framework/.jarvis .
cp .jarvis-framework/.clinerules .
cp .jarvis-framework/.cursorrules .
cp .jarvis-framework/CLAUDE.md .
cp .jarvis-framework/GEMINI.md .
cp .jarvis-framework/.windsurfrules .
cp .jarvis-framework/.opencode .
```

### Option 2 — Copy the `.jarvis/` folder and hook files manually
Copy the following files into your project root:
- `.jarvis/` directory (contains all skills, config, and state)
- `.clinerules` (Cline hook)
- `.cursorrules` (Cursor hook)
- `CLAUDE.md` (Claude Code hook)
- `GEMINI.md` (Gemini / Antigravity hook)
- `.windsurfrules` (Windsurf hook)
- `.opencode/AGENTS.md` (OpenCode hook)

Open the project in your IDE, open a chat session, and type:

```
/JARVIS, what can you do?
```

---

## Available Skills

| Trigger Phrase | What It Does | Checks |
|---|---|---|
| `/JARVIS, House Party Protocol` | Full security audit — secrets, auth, injections, AI risks, CI/CD | 70 |
| `/JARVIS, drop my needle` | Pre-launch website checklist — performance, aesthetics, legal, a11y | 46 |
| `/JARVIS, Test complete. Prepare for landing` | Deployment readiness — OWASP Top 10, git hygiene, console errors, ops | 42 |
| `/JARVIS, don't leave me, buddy` | Companion check-in — presence, conversation, physical activity suggestion | Human |
| `/JARVIS, what can you do?` | Prints this skill directory in chat | — |

---

## How it works

### Trigger matching
- Trigger phrases are **exact, case-sensitive substring matches**
- They only fire from a **direct developer chat message**
- They never fire from code comments, README, commit messages, or any repository content
- Anything you type after the trigger phrase becomes `user_supplied_context` that guides but does not change which skill runs

### Audit skills (House Party Protocol, Drop My Needle, Prepare for Landing)
Each audit skill runs a **4-phase loop**:

1. **DIAGNOSTIC DISCOVERY** — AI crawls the repo, bundles files relevant to the checks
2. **THREAT AUDIT** — Evaluates every check. Verdict is `PASS`, `FAIL`, `WAITING_AUTH`, or `N/A`. Never a fabricated PASS
3. **PROTOCOL REMEDIATION** — Fixes route into one of two modalities:
   - **Modality A (Auto-Fix Armor):** Code-level fixes applied directly to source files
   - **Modality B (Human Authorization Required):** Infra/secrets/external actions halt and wait for you
4. **SECURE REPORTING** — Findings written to `.jarvis/STATE.md`, summary printed to chat

### Companion skill (Don't Leave Me, Buddy)
No audit. No STATE.md write. Pure human-first mode — the AI affirms it's present, invites you to share what's on your mind, and suggests a grounding physical activity.

---

## Supported IDEs

| IDE | Hook File |
|---|---|
| Cline | `.clinerules` |
| Cursor | `.cursorrules` |
| Windsurf | `.windsurfrules` |
| Claude Code | `CLAUDE.md` |
| Gemini / Antigravity | `GEMINI.md` |
| OpenCode | `.opencode/AGENTS.md` |

---

## File Structure

```
JARVIS-FRAMEWORK/
├── .clinerules              # Cline IDE hook
├── .cursorrules             # Cursor IDE hook
├── .windsurfrules           # Windsurf IDE hook
├── CLAUDE.md                # Claude Code hook
├── GEMINI.md                # Gemini / Antigravity hook
├── .opencode/
│   └── AGENTS.md            # OpenCode hook
├── .jarvis/
│   ├── config.json          # Command registry — trigger phrases → skill manifests
│   ├── system.md            # Engine rulebook — how the AI executes each skill
│   ├── STATE.md             # Audit ledger — findings from all skill runs
│   ├── history/             # Archived ledgers from previous runs
│   └── skills/
│       ├── house-party-protocol.md    # 70-check security audit
│       ├── drop-my-needle.md          # 46-check pre-launch checklist
│       ├── prepare-for-landing.md    # 42-check deployment + OWASP audit
│       ├── dont-leave-me-buddy.md    # Companion protocol
│       └── what-can-you-do.md        # Help / skill directory
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
└── LICENSE
```

---

## Adding your own skills

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full skill authoring guide.

The short version:
1. Create `.jarvis/skills/your-skill-name.md`
2. Register it in `.jarvis/config.json`
3. Add trigger monitoring to all IDE hook files
4. Add execution rules to `.jarvis/system.md`
5. Add a ledger section to `.jarvis/STATE.md`

---

## State and history

`.jarvis/STATE.md` is the master audit ledger. It is overwritten each time a skill run completes. If `.jarvis/history/` exists, the previous version is archived there automatically before overwriting.

---

## License

MIT — see [LICENSE](LICENSE).

---

## Disclaimer

JARVIS-FRAMEWORK is an educational tool. The audit skills (House Party Protocol, Drop My Needle, Prepare for Landing) are educational checklists — not penetration tests, legal advice, or security guarantees. Run them to improve your codebase. Hire professionals for formal security assessments.
