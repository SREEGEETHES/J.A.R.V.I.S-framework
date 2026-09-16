<div align="center">

# J.A.R.V.I.S. Framework

**Just A Rather Very Intelligent System**

*Universal trigger-phrase & slash-command skill framework for AI coding agents.*

[![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)

</div>

---

## Overview

**JARVIS-FRAMEWORK** gives your AI coding agents specialized audit and diagnostic skills accessible via slash-command popups (`/jarvis-...`) and natural trigger phrases.

Works seamlessly across **Antigravity IDE**, **OpenCode**, **Claude Code**, **Cursor**, **Windsurf**, and **Cline**.

---

## Available Skills

| Slash Command in Popup | Description | Checks |
|---|---|---|
| `/jarvis-house-party-protocol` | Full security audit – secrets, auth, injections, AI risks, CI/CD | 70 |
| `/jarvis-drop-my-needle` | Pre-launch website checklist – performance, aesthetics, legal, a11y | 46 |
| `/jarvis-prepare-for-landing` | Deployment readiness – OWASP Top 10, git hygiene, ops | 42 |
| `/jarvis-dont-leave-me-buddy` | Companion check-in protocol – presence and grounding activity | Human |
| `/jarvis-what-can-you-do` | Displays the full JARVIS skill directory and usage guide | — |

> *Natural trigger phrases (e.g. `/JARVIS, drop my needle` or `/JARVIS, House Party Protocol`) are also fully supported.*

---

## Installation Guide (New Machine Setup)

### Method 1: Global Installation (Recommended)
*Install once on your machine and use `/jarvis` across **all** your projects without modifying individual project repositories.*

**On Windows (PowerShell):**
```powershell
git clone https://github.com/YOUR_USERNAME/JARVIS-FRAMEWORK.git
cd JARVIS-FRAMEWORK
.\install.ps1 -Global
```

**On macOS / Linux:**
```bash
git clone https://github.com/YOUR_USERNAME/JARVIS-FRAMEWORK.git
cd JARVIS-FRAMEWORK
chmod +x install.sh && ./install.sh --global
```

*Installs skills to `~/.gemini/config/skills/` (Antigravity), `~/.config/opencode/commands/` (OpenCode), and `~/.claude/commands/` (Claude Code).*

---

### Method 2: Project-Level Installation
*Use this if you want to commit JARVIS into a specific project repository so your entire team gets it automatically when they clone your project.*

**On Windows (PowerShell):**
```powershell
.\install.ps1 -TargetDir "C:\path\to\your-project"
```

**On macOS / Linux:**
```bash
./install.sh /path/to/your-project
```

This installs the necessary hook and skill directories into your target project:
- `.agents/skills/` (Antigravity IDE)
- `.opencode/commands/` (OpenCode)
- `.claude/commands/` (Claude Code)
- `.jarvis/` (Core rulebook & manifests)
- `.cursorrules`, `.windsurfrules`, `.clinerules`, `GEMINI.md`, `CLAUDE.md`

---

## Supported IDEs & Assistants

| IDE / Assistant | Integration Method | Slash Popup Support |
|---|---|---|
| **Antigravity IDE** | `.agents/skills/` & `GEMINI.md` | **Yes** (Type `/jarvis` in chat) |
| **OpenCode** | `.opencode/commands/` & `AGENTS.md` | **Yes** (Type `/jarvis` in terminal) |
| **Claude Code** | `.claude/commands/` & `CLAUDE.md` | **Yes** (Type `/jarvis` in terminal) |
| **Cursor** | `.cursorrules` | Trigger phrase in chat |
| **Windsurf** | `.windsurfrules` | Trigger phrase in chat |
| **Cline / Roo Code** | `.clinerules` | Trigger phrase in chat |

---

## How It Works

Each audit skill runs a disciplined **4-phase loop**:

1. **Diagnostic Discovery** — Agent scans repo, git status, and project configuration.
2. **Threat Audit** — Evaluates every checklist control (`PASS`, `FAIL`, or `WAITING_AUTH`).
3. **Protocol Remediation**:
   - **Modality A (Auto-Fix Armor):** Safe code-level fixes applied automatically to source files.
   - **Modality B (Human Authorization Required):** Halts and requests user approval for infrastructure, secrets, or external changes.
4. **Secure Reporting** — Findings logged to `.jarvis/STATE.md` and summarized in chat.

---

## Adding Custom Skills

1. Add your skill manifest to `.jarvis/skills/your-skill-name.md`
2. Register it in `.jarvis/config.json`
3. Add the command file to `.opencode/commands/`, `.agents/skills/`, and `.claude/commands/`

---

## License

MIT — see [LICENSE](LICENSE).
