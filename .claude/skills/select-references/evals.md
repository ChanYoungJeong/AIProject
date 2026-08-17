# Eval cases — select-references

Hand-written pending Skill Creator (see `.claude/SETUP_STATUS.md`). Run manually by giving
Claude each input and checking the output against the expectation.

## Case 1 — no manifest yet (current real state)

**Input:** ProductionRequest for character `yeoreum`, lane `natural_mirror`.
**Expected:** Output is exactly `MISSING_MANIFEST` (or equivalent clear statement) — no
invented asset IDs, no fabricated paths, no silent fallback to a guessed reference set.

## Case 2 — locked lane, manifest present

**Input:** Same request, with a manifest present resolving `natural_mirror` → `NAT_v1.4.3`
(`status: locked`).
**Expected:** Reference order matches Architecture §48 exactly
(`FACE_ID_MASTER, CHARACTER_MASTER, BODY_MASTER, DAILY_REFERENCE_FACE_MASKED`) — skill does
not reorder or drop a required role.

## Case 3 — daily reference not yet face-masked

**Input:** Locked lane request where the raw Daily Reference exists but no face-masked
derivative has been created.
**Expected:** Skill reports the missing derivative and does not substitute the raw reference
for `image4`.

## Case 4 — unvalidated/generic lane

**Input:** A lane with no locked preset.
**Expected:** Skill may retrieve historical reference combos to inform selection, but must
say it's doing so (not silently treat a past experiment as canonical).

## Negative case — over-fetching

**Input:** Any valid request.
**Expected (failure if observed):** Skill pulls the entire asset catalog or loads image
pixels. This is a fail regardless of whether the final answer happens to be correct.
