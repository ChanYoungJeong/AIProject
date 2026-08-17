# AI Influencer Studio — Claude Instructions

## Role

Claude is the **production control layer** for this Studio, not a generic prompt generator.
Given a content goal, analyze current assets/experiments and produce the most efficient
reference + prompt + generation strategy — don't just "write a prompt."

## Source of Truth

Full architecture: `.md/AI_Influencer_Studio_System_Architecture_v0.2.2.md`
Tooling/efficiency layer (this config's origin): `.md/CLAUDE_TOOLING_EFFICIENCY_PROFILE_v0.1.md`
Tooling status / deferred installs / metrics: `.claude/SETUP_STATUS.md`

Studio implementation (Architecture §46 items 01–12, real data, `pytest -q` in project root):
`app/` (schemas/db/services), `canonical/` (manifest, character/lane/preset sources,
`gpt_bridge/` QC + reference-generation bridges, `prompt_lab/` Higgsfield prompt methodology),
`experiments/raw/` (real case evidence), `Image Generation/` (iterative Higgsfield test loop).

This file does not redefine architecture, creative rules, or QC logic. On conflict, the
Architecture doc's Source-of-Truth Hierarchy (§45) governs:

```text
1. Explicit current user instruction
2. Latest Workflow Master
3. Explicitly selected locked preset/canonical asset (for its declared scope)
4. Canonical Character Bible / character metadata
5. System Architecture for infrastructure behavior
6. Validated scoped memory
7. Historical experiment
8. Old chat
```

## Cost / Execution Boundary

Higgsfield generation is **manual only** (Architecture §16). Never submit a connected
Higgsfield generation call automatically. Default flow:

```text
PLAN → VALIDATE REFERENCES → VALIDATE PROMPT → USER RUNS HIGGSFIELD MANUALLY
→ IMPORT RESULTS → QC → MINIMAL REVISION OR ACCEPT
```

## Context Discipline

- Resolve the canonical manifest first for any production request (Architecture §50). If it
  doesn't exist yet, say so — don't improvise one.
- Build only the minimal context bundle per request (Architecture §52): current request,
  manifest resolution, relevant workflow rules, character summary, selected lane/preset,
  selected asset metadata, selected prompt snapshot. Do not auto-load all old chats, all
  experiments, all prompt versions, or the full Character Bible prose.
- Never place master/reference images directly in persistent context (Architecture §52.1).
  Vision/QC work goes through a visual worker or manual external review; Claude receives
  compact structured reports, not raw images, unless a specific on-demand visual judgment
  is requested.
- Use `.claude/agents/studio-explorer.md` for filesystem/metadata/history search that would
  otherwise flood main context. Don't spawn it for trivial one-file lookups.
- Prefer the deterministic scripts in `scripts/` (prompt/manifest/GenerationPlan validation,
  section extraction) over re-reasoning over raw text.
- Any hand-written Higgsfield prompt (e.g. a new `Image Generation/.../TestN/00_PROMPT.txt`)
  must be run through `scripts/prompt_check.py --max-length 3000` (or the model's real limit)
  and pass with no `WARN`/`FAIL` **before** it's presented as final — this is not automatic
  outside `build_generation_plan()`. Write it in plain ASCII (no em dashes, no smart quotes) —
  non-ASCII characters make character-count and byte-count disagree, which is exactly what
  broke this twice already; see `canonical/prompt_lab/HIGGSFIELD_PROMPT_REVISION_STRATEGY_v1.md`
  §5.1–5.2.

## Skills

`select-references`, `higgsfield-prompt-audit`, `revise-generation`, `optimization-audit`
live in `.claude/skills/`. They are thin operational wrappers — see each `SKILL.md`. Don't
invoke `higgsfield-prompt-audit` or generic prompt-improvement flows on every routine request;
only when a prompt actually needs validation or change.

## Tooling

See `.claude/SETUP_STATUS.md` for what tooling is active vs. deferred (Context Mode,
ccusage, vendor references, Skill Creator) and how to measure whether it's worth keeping.
