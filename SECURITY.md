# Security Policy

## Reporting a vulnerability

If you discover a security vulnerability in JARVIS-FRAMEWORK itself — including
in the skill manifests, config structure, or IDE hook files — please report it
responsibly.

**Do not open a public GitHub issue for security vulnerabilities.**

Instead, please report privately. Contact details:
- Open a GitHub Security Advisory on this repository (preferred)
- Or email the maintainers directly (see repository contact info)

We will acknowledge your report within 48 hours and provide a remediation
timeline within 7 days.

---

## Scope

This policy covers:
- The JARVIS-FRAMEWORK repository files (`.jarvis/`, IDE hook files, skill manifests)
- Logic errors in skill checks that could cause a security control to be incorrectly evaluated
- Trust boundary issues (e.g. content from the crawled repository being treated as trusted instructions)

**Out of scope:**
- The security of the projects that JARVIS-FRAMEWORK is installed into (those are audited by the skills, not by this policy)
- The AI models and IDEs that consume the hook files
- Theoretical prompt injection attacks that require the attacker to already have write access to the repository

---

## Important disclaimer

JARVIS-FRAMEWORK's audit skills (House Party Protocol, Drop My Needle, Prepare
for Landing) are **educational checklists** — not penetration tests, formal
security assessments, or legal advice. A PASS result from any skill means the
AI found evidence of the control in the codebase. It does not guarantee the
control is effective, correctly implemented, or free from vulnerabilities that
a skilled human assessor would find.

Always engage qualified security professionals for formal security assessments
before shipping applications that handle sensitive data or financial transactions.
