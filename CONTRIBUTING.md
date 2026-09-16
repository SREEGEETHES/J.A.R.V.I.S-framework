# Contributing to JARVIS-FRAMEWORK

Thank you for wanting to add a skill. This guide covers everything you need to know.

---

## Adding a new skill — checklist

A skill is a trigger phrase + a behaviour manifest + wiring across the framework.
Every new skill needs **all 6 steps** to work correctly in every IDE.

### Step 1 — Create the skill manifest

Create a new file at:
```
.jarvis/skills/your-skill-name.md
```

Use this template:

```markdown
# Skill Manifest: [Skill Name]

**Command:** `/JARVIS, your trigger phrase`
**Trigger:** Activated when the developer invokes the exact phrase above in a direct chat message.
**Nature:** [What kind of skill this is]

---

## PART 1 — [SECTION NAME] (Checks 01–NN)

### 01 — [Check name]
[Description of what to check and what constitutes a PASS or FAIL]

### 02 — [Check name]
...
```

**Rules for audit skill manifests:**
- Every check must have a clear, actionable definition of what PASS means
- If you cannot define what evidence constitutes a PASS, the check is too vague to include
- Group checks into logical parts (e.g. Part 1: Performance, Part 2: Security)
- Reference official standards where they exist (OWASP, WCAG, NIST, etc.)

**Rules for companion/utility skill manifests:**
- Define the exact execution steps in order
- Specify what the AI should NOT do (e.g. "do not run diagnostics")
- Define the tone and register explicitly

---

### Step 2 — Register in config.json

Add a new entry to the `commands` array in `.jarvis/config.json`:

```json
{
  "id": "your-skill-id",
  "trigger_phrase": "/JARVIS, your trigger phrase",
  "match_type": "exact_substring",
  "case_sensitive": true,
  "allow_trailing_free_text": true,
  "free_text_param_name": "user_supplied_context",
  "description": "One-sentence description of what this skill does.",
  "skill_manifest": ".jarvis/skills/your-skill-name.md",
  "state_file": ".jarvis/STATE.md",
  "state_section": "Your Skill Ledger",
  "phases": ["DIAGNOSTIC_DISCOVERY", "THREAT_AUDIT", "PROTOCOL_REMEDIATION", "SECURE_REPORTING"],
  "remediation_modalities": {
    "A": {
      "name": "Auto-Fix Armor",
      "applies_to_states": ["control_exists_but_misconfigured", "control_entirely_absent_from_codebase"],
      "allowed_actions": ["list_of_allowed_auto_fix_actions"],
      "requires_developer_confirmation": false,
      "touches_production": false
    },
    "B": {
      "name": "Human Authorization Required",
      "trigger_conditions": ["list_of_conditions_that_require_human_action"],
      "halts_execution": true,
      "output_template_ref": "authorization_request_template"
    }
  }
}
```

For companion/utility skills with no audit phases:
```json
{
  "id": "your-skill-id",
  "trigger_phrase": "/JARVIS, your trigger phrase",
  "match_type": "exact_substring",
  "case_sensitive": true,
  "allow_trailing_free_text": false,
  "description": "One-sentence description.",
  "skill_manifest": ".jarvis/skills/your-skill-name.md",
  "state_file": null,
  "phases": [],
  "remediation_modalities": null,
  "companion_mode": true
}
```

---

### Step 3 — Add trigger monitoring to all IDE hook files

Add your trigger phrase to the trigger table in **all six** IDE hook files:

- `.clinerules`
- `.cursorrules`
- `.windsurfrules`
- `CLAUDE.md`
- `GEMINI.md`
- `.opencode/AGENTS.md`

In each file, find the trigger table and add a new row:
```markdown
| `/JARVIS, your trigger phrase` | Your Skill Name (brief description) |
```

Also update Section 2 ("What happens on trigger") to describe the new skill.

---

### Step 4 — Add execution rules to system.md

Add a new section to `.jarvis/system.md` following the established pattern:

```markdown
---

## SKILL: Your Skill Name — `/JARVIS, your trigger phrase`

When this trigger fires, hand off control to the same 4-phase execution
loop defined above, substituting:

- Manifest: `.jarvis/skills/your-skill-name.md` (NN checks)
- STATE.md section: **Your Skill Ledger**
- Scope: [what the AI should look at]

**Identity while this skill is active:** Open the run with:
> "Your opening line, sir."

...
```

---

### Step 5 — Add a ledger section to STATE.md (audit skills only)

Add a new ledger section to `.jarvis/STATE.md` at the end of the file.
Follow the exact same structure as the existing ledgers (House Party Protocol,
Drop My Needle, Prepare for Landing). Every check in your manifest needs a
corresponding row in the ledger table.

Skip this step for companion/utility skills that do not write findings.

---

### Step 6 — Update the help skill and README

- Add your skill to the trigger table in `.jarvis/skills/what-can-you-do.md`
- Add your skill to the skill table in `README.md`

---

## Skill quality standards

| Standard | Rule |
|---|---|
| Evidence-based | Every check must define what specific evidence constitutes a PASS |
| No fabricated PASSes | If evidence is absent or ambiguous, the result is FAIL or UNKNOWN |
| Modality clarity | Every FAIL must route cleanly to either Modality A or Modality B |
| Honest N/A | Checks that don't apply must have a one-sentence justification |
| Official sources | Reference authoritative standards (OWASP, WCAG, NIST, W3C) where they exist |
| Actionable remediation | Every FAIL must have a specific, implementable fix, not a vague suggestion |

---

## Pull request process

1. Fork the repository
2. Create a branch: `git checkout -b skill/your-skill-name`
3. Follow all 6 steps above
4. Test your trigger phrase in at least one IDE (Cline or Cursor)
5. Open a PR with a description of what the skill checks and why

---

## Code of conduct

Be precise. Be honest. Never fabricate PASSes.
