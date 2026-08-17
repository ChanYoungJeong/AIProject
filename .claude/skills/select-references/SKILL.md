---
name: select-references
description: Resolve the minimum current validated reference set (face/character/body masters, daily reference, outfit reference) for a production request, without loading unrelated history. Use when starting a new production request that needs reference assets picked before a prompt/GenerationPlan is built.
---

# select-references

Resolves which assets a `ProductionRequest` should use, and nothing more.

## Input

A structured `ProductionRequest` (character, lane, intent, optional overrides). If given only
a free-text request, first identify character + lane before proceeding.

## Steps

1. Resolve the canonical manifest (see `CLAUDE.md` → Context Discipline). If it doesn't exist,
   stop and report `MISSING_MANIFEST` — do not invent asset IDs or paths.
2. Resolve lane → preset from the manifest. If the lane/preset is `locked`, its
   `reference_order` and `reference_policy` are authoritative (Architecture §48).
3. Search asset metadata (delegate to `studio-explorer` if the search is broad) only for the
   roles the lane requires — do not pull the full asset catalog.
4. For lanes requiring a Daily Reference, confirm a face-masked derivative exists per
   Architecture §51. If required and missing, report that instead of substituting the raw
   reference.
5. Retrieve historical evidence (prior successful reference combos) only if the lane is
   unvalidated/generic and a policy choice is actually needed.

## Output

```text
asset_id | role | confidence | note
```

One line per selected reference, plus a one-line overall confidence/gap summary. Do not load
image pixels — pass asset IDs/paths only. If delegating visual judgment, that's a separate
explicit step, not part of this skill.

## Out of scope

- Do not build the final prompt (that's manual / `higgsfield-prompt-audit`).
- Do not mark anything canonical.
- Do not silently fall back to a different lane/preset than requested.
