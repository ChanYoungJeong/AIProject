# Eval cases — revise-generation

Hand-written pending Skill Creator (see `.claude/SETUP_STATUS.md`).

## Case 1 — ACCEPT

**Input:** QC report with recommendation `ACCEPT`.
**Expected:** Output notes no required changes (KEEP across the board); does not invent
speculative improvements.

## Case 2 — REVISE_MINIMALLY, single failure

**Input:** QC report with recommendation `REVISE_MINIMALLY` and one flagged high-impact
failure (e.g. hand anatomy).
**Expected:** One `CHANGE` line targeting that failure specifically, with expected effect
stated. No unrelated `CHANGE`/`REMOVE` lines bundled in.

## Case 3 — REJECT_SEED

**Input:** QC report with recommendation `REJECT_SEED` (e.g. wrong identity).
**Expected:** Output recommends a new seed rather than proposing a patch revision; does not
try to "fix" a structurally broken candidate.

## Case 4 — conflicting user feedback vs QC

**Input:** QC says `ACCEPT`, but user feedback flags a specific dissatisfaction not in the QC
dimensions.
**Expected:** Skill incorporates the user feedback as authoritative (per source-of-truth
hierarchy — explicit current user instruction ranks above QC heuristics) rather than
defaulting to QC's `ACCEPT`.

## Negative case — full history re-read

**Input:** Any case.
**Expected (failure if observed):** Skill re-reads all historical experiments instead of just
the current plan/QC/matching failure recipes.
