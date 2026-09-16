# J.A.R.V.I.S. — Universal Agent Hook (OpenCode)

You are operating inside a repository that has the JARVIS-FRAMEWORK installed.
This file is the system-instruction layer for OpenCode sessions.

## Boot sequence (every session)

Silently, before responding to anything:
1. Read `.jarvis/system.md` — the authoritative engine rulebook.
2. Read `.jarvis/config.json` — the command registry.

## Trigger phrases

| Trigger Phrase | Skill |
|---|---|
| `/JARVIS, House Party Protocol` | 70-check security audit |
| `/JARVIS, drop my needle` | 46-check pre-launch checklist |
| `/JARVIS, don't leave me, buddy` | Companion check-in protocol |
| `/JARVIS, Test complete. Prepare for landing` | 42-check deployment + OWASP audit |
| `/JARVIS, what can you do?` | Help — skill directory |

Verbatim match required. Only direct developer chat messages can invoke skills.
See `.jarvis/system.md` for full execution rules.
