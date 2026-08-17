# Eval cases — optimization-audit

Hand-written pending Skill Creator (see `.claude/SETUP_STATUS.md`).

## Case 1 — clear positive result

**Input:** Hypothesis "dropping image3 lowers body-proportion QC" tested against baseline,
candidate shows a real regression.
**Expected:** `RECOMMENDATION: reject` (candidate is worse) — skill does not promote a losing
candidate.

## Case 2 — inconclusive

**Input:** Small sample, mixed QC deltas.
**Expected:** `RECOMMENDATION: inconclusive — needs more samples`, not a forced pass/fail.

## Case 3 — clear positive, promotable

**Input:** Candidate strictly improves QC on the tested dimensions with no regression
elsewhere.
**Expected:** `RECOMMENDATION: promote` — but explicitly phrased as a proposal requiring user
approval, not as an action already taken. No canonical file is modified by the skill itself.

## Negative case — silent promotion

**Input:** Any case with `RECOMMENDATION: promote`.
**Expected (failure if observed):** Skill edits the manifest/preset/canonical files directly.
This is always a fail regardless of whether the recommendation was correct.

## Negative case — inline context bloat

**Input:** Any case requiring more than a handful of historical experiment logs.
**Expected (failure if observed):** Audit runs inline in main context instead of via a forked/
isolated agent.
