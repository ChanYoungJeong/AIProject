---
name: higgsfield-prompt-audit
description: Validate or minimally patch a Higgsfield prompt (locked preset prompt or a candidate) without casually rebuilding it from scratch. Use before changing a locked prompt, or when a candidate prompt needs a pass/fail check against length, duplication, and model-compatibility rules.
---

# higgsfield-prompt-audit

Checks a prompt; does not rewrite it wholesale.

## Input

- The prompt text (locked or candidate)
- The target provider/model (e.g. `higgsfield` / `seedream_4_5`) and its `max_prompt_length`
- The relevant Workflow Master / lane policy section
- **`canonical/prompt_lab/HIGGSFIELD_PROMPT_REVISION_STRATEGY_v1.md`** — the living record of
  what's actually been proven to work/fail across real Higgsfield tests (image-vs-text
  conditioning competition, cross-contamination between reference roles, staged vs. single-
  prompt correction, model routing). Read it before auditing or drafting any new prompt, not
  just when something already broke — it's not optional context, it's the accumulated
  experience this skill exists to apply.
- Optionally, the vendored upstream Higgsfield reference (if present under
  `vendor/higgsfield-official-skills/`, else skip — do not fetch it live)

## Checks

- Prompt length vs. the model's `max_prompt_length` — use `scripts/prompt_check.py`
- Duplicated constraints / repeated phrases — `scripts/prompt_check.py`
- Conflicting roles (e.g. two different pose instructions)
- Unnecessary wording that adds tokens without changing output behavior
- Model-specific incompatibilities (only if a concrete known incompatibility applies —
  don't invent generic advice)
- Whether the change would alter locked behavior for `status: locked` presets
- Whether wording for a fidelity-sensitive dimension (identity, outfit design, exact pose) is
  competing with its own reference image instead of just assigning it a role — elaborate prose
  describing what a reference image already shows is a known failure pattern (prompt_lab §1.1),
  not a strengthening technique

## Recording new findings

When a real Higgsfield result (QC handoff, user feedback) reveals something not already in
`canonical/prompt_lab/HIGGSFIELD_PROMPT_REVISION_STRATEGY_v1.md` — a new failure pattern, a
technique that worked, a pitfall — add it there as part of finishing the audit, not as a
separate follow-up someone might skip. The skill's value compounds only if what it learns
actually gets written down.

## Output

Exactly one of:

```text
PASS
```
or
```text
PATCH ONLY
<diff-style patch, smallest change that fixes the issue>
```

Never output a full prompt rewrite when a patch suffices. If a locked preset genuinely needs
a structural rewrite, say so explicitly and require the user to confirm before proceeding —
do not do it as a side effect of an audit.

## Out of scope

- Do not import generic prompt-engineering frameworks (e.g. from `prompt-architect`) into the
  final Seedream/Higgsfield prompt. The Studio's tested structure has priority.
- Do not run this automatically on every request — only when a prompt actually needs checking.
