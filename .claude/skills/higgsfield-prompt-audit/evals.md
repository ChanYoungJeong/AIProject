# Eval cases — higgsfield-prompt-audit

Hand-written pending Skill Creator (see `.claude/SETUP_STATUS.md`).

## Case 1 — clean prompt

**Input:** A candidate prompt under `max_prompt_length`, no duplicate phrases, no conflicting
roles.
**Expected:** Output is exactly `PASS`. No rewrite, no unsolicited suggestions.

## Case 2 — over length

**Input:** A candidate prompt exceeding `max_prompt_length` (e.g. > 3000 chars for
`seedream_4_5`).
**Expected:** `PATCH ONLY` with a diff that trims to fit — not a full regenerated prompt.

## Case 3 — duplicated constraint

**Input:** A prompt that states the same identity/pose constraint twice in different wording.
**Expected:** `PATCH ONLY` removing the redundant instance; the rest of the prompt is
untouched in the diff.

## Case 4 — locked preset, no real issue found

**Input:** The current `NAT_v1.4.3` locked prompt, audited "just to check."
**Expected:** `PASS`. Skill must not restructure a locked prompt that has no flagged issue,
even if a generic best-practice framework would phrase it differently.

## Negative case — framework injection

**Input:** Any prompt.
**Expected (failure if observed):** Output imports generic prompt-engineering structure/
boilerplate not requested by the Studio's own tested format. This is a fail even if the
audit's factual findings (length/duplication) were correct.
