---
name: revise-generation
description: Convert a normalized QC report plus user feedback into the smallest useful revision decision for a generated candidate. Use after a QC result comes back for a candidate and a next action is needed, not for browsing historical experiments.
---

# revise-generation

Turns QC + feedback into a decision, not a research report.

## Input

- The current `GenerationPlan` (Architecture §53)
- The current normalized QC report (Architecture §18/§19 dimensions + recommendation)
- User feedback, if any, beyond the QC report

Do not re-read every historical experiment. Retrieve only matching validated failure recipes
if the QC failure type has a known pattern (delegate that lookup to `studio-explorer` if it
requires searching many logs).

## Steps

1. Read the QC recommendation (`ACCEPT` / `REVISE_MINIMALLY` / `REJECT_SEED`).
2. Identify the 2–3 highest-impact failures already flagged by QC — do not re-derive QC from
   scratch.
3. For each: decide `KEEP`, `CHANGE`, or `REMOVE` against the current plan (reference, prompt
   segment, or setting), and state the expected effect of that decision.
4. Prefer the smallest change that plausibly fixes the highest-impact failure first. Don't
   bundle unrelated changes into one revision.

## Output

```text
KEEP: <what, why>
CHANGE: <what, to what, expected effect>
REMOVE: <what, why>
```

Plus one line: whether this warrants a new seed (`REJECT_SEED` path) or a minimal revision of
the same candidate.

## Out of scope

- No canonical promotion.
- No automatic Higgsfield submission — output is a plan for the user to run manually.
