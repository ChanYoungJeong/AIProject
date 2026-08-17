# Claude Tooling & Efficiency Profile — AI Influencer Studio
Version: 0.1
Purpose: Tooling-only setup for `AI_Influencer_Studio_System_Architecture_v0.2.2`
Scope: Claude Code efficiency, context/token control, prompt quality, and repeatable evaluation.
Non-goal: This file MUST NOT redefine the Studio architecture, canonical creative rules, reference policies, or QC logic.

---

# 1. Operating Rule

The existing System Architecture is the source for workflow/business logic.

This file adds only an **execution/tooling layer**.

Do NOT copy architecture sections into `CLAUDE.md`.
Do NOT duplicate the full architecture inside Skills.
Do NOT install large skill packs by default.

Optimization target:

```text
minimum persistent context
+ minimum duplicate tool output
+ on-demand specialized skills
+ measurable prompt quality
+ no accidental paid Higgsfield generation
```

---

# 2. Read First

Before changing configuration:

1. Locate the latest `AI_Influencer_Studio_System_Architecture*.md`.
2. Locate the latest Workflow Master and canonical manifest.
3. Read only the sections needed to understand:
   - source-of-truth hierarchy,
   - context assembly,
   - visual token/cost control,
   - prompt engine,
   - manual Higgsfield boundary.
4. Do not import the entire architecture into startup context.

The architecture remains unchanged unless the user explicitly requests an architecture revision.

---

# 3. Recommended Tool Stack

## INSTALL / ENABLE NOW

### A. Context Mode
Repository:
`https://github.com/mksglu/context-mode`

Purpose:
Reduce context consumed by large tool outputs, searches, logs, file processing, and repeated session state.

Why this project benefits:
- the Studio will eventually query many files, metadata rows, logs, and experiments;
- raw MCP/Bash/file output should not flood Claude's main context;
- the architecture already requires selective retrieval, so this complements it.

Important:
Context Mode's session database is **NOT canonical Studio memory**.
The Studio SQLite/canonical files remain source of truth.

Install in Claude Code:

```text
/plugin marketplace add mksglu/context-mode
/plugin install context-mode@context-mode
```

Then restart Claude Code or run:

```text
/reload-plugins
```

Verify:

```text
/context-mode:ctx-doctor
/context-mode:ctx-stats
```

### Required A/B test

Do not assume advertised savings equal this project's savings.

Before using Context Mode permanently:

1. Run 3 representative development/retrieval tasks without Context Mode.
2. Run comparable tasks with Context Mode.
3. Compare:
   - context usage,
   - number of tool calls,
   - compactions,
   - Claude mistakes caused by missing context,
   - wall time.
4. Keep it only if it materially improves the Studio workflow.

If the full hook-based plugin causes instability, test MCP-only mode instead:

```bash
claude mcp add context-mode -- npx -y context-mode
```

---

### B. ccusage
Repository:
`https://github.com/ccusage/ccusage`

Purpose:
Measure Claude Code token/cost trends from local Claude logs.

This tool does NOT reduce tokens by itself.
It is the measurement layer used to determine whether other optimizations actually work.

Use on demand:

```bash
npx ccusage@latest claude daily
npx ccusage@latest claude session
npx ccusage@latest claude monthly
```

Use session comparisons before/after major tooling changes.

Do NOT treat ccusage estimates as authoritative subscription billing numbers.
Known edge cases have existed around cached/subagent/live usage reporting.

### Statusline policy

Do NOT enable a continuously spawning `npx ccusage statusline` by default.

Reason:
historical issues reported unnecessary process/CPU overhead from statusline execution.

If a statusline is later desired:
- install/run ccusage directly rather than repeatedly bootstrapping through `npx`,
- test CPU/process behavior first,
- keep the statusline optional.

---

### C. Anthropic Skill Creator
Upstream:
`https://github.com/anthropics/skills`

Purpose:
Create and **measure** Studio-specific skills.

First check whether the current Claude Code installation already exposes Skill Creator.
Do NOT install a duplicate copy if it is already bundled/available.

Use Skill Creator for:

```text
select-references
higgsfield-prompt-audit
revise-generation
import-visual-qc
optimization-audit
```

Every important Studio skill should have eval cases.

Do not accept a Skill merely because its prose looks good.

For each Skill, compare:
- skill enabled vs disabled,
- trigger reliability,
- output correctness,
- token overhead,
- unnecessary verbosity,
- failure rate.

---

### D. Official Higgsfield Skills — UPSTREAM REFERENCE
Repository:
`https://github.com/higgsfield-ai/skills`

Purpose:
Current Higgsfield platform/model/CLI knowledge.

IMPORTANT:
The Studio's current MVP uses manual Higgsfield generation.
Therefore do **not** make automatic Higgsfield execution the default.

Recommended setup:

Clone/update the repository as an upstream reference outside `.claude/skills/`:

```bash
git clone --depth 1 https://github.com/higgsfield-ai/skills.git vendor/higgsfield-official-skills
```

If already cloned:

```bash
git -C vendor/higgsfield-official-skills pull --ff-only
```

Why vendor/reference instead of active global plugin:
- prevents accidental model routing or paid generation;
- avoids giving upstream workflow rules authority over the Studio's locked presets;
- allows Claude to inspect current Higgsfield model/platform information only when needed.

The Studio's custom prompt skill may consult this repository selectively.

Never let upstream Higgsfield defaults silently override:
- a locked Studio prompt,
- Studio reference order,
- the manual generation boundary.

---

### E. Repomix — ON-DEMAND ONLY
Repository:
`https://github.com/yamadashy/repomix`

Purpose:
Create compact repository snapshots and token counts when handing code/context to another model or reviewing a bounded project subset.

Useful commands:

```bash
npx repomix@latest --compress
```

Use `.repomixignore` aggressively.

Exclude at minimum:

```text
assets/**
generations/**
qc/**
experiments/**
database/*.db
vendor/**
.git/**
node_modules/**
```

Normal Claude Code work should NOT pack the entire Studio repo into context.

Use Repomix only for:
- cross-model handoff,
- one-time architecture/code review,
- exporting a bounded code snapshot,
- measuring approximate code context size.

---

# 4. Optional Tools

## Promptfoo — Phase 2
Repository:
`https://github.com/promptfoo/promptfoo`

Purpose:
Systematic evaluation of LLM-generated prompt/planning outputs.

Use when the Studio exposes a stable prompt-generation function/CLI and you want reproducible regression tests across:
- Claude model versions,
- prompt-engine skill versions,
- reference-selection policies.

Do not use Promptfoo as a replacement for image-result QC.
It evaluates the LLM workflow; Higgsfield output quality still requires generation-result evidence.

Install only when this evaluation layer is needed.

---

## Prompt Architect — Optional / Meta-Prompt Use Only
Repository:
`https://github.com/ckelsoe/prompt-architect`

Purpose:
Analyze and restructure general LLM prompts.

Allowed use:
- improving Claude system prompts,
- subagent prompts,
- skill instructions,
- MCP tool descriptions.

Do NOT automatically apply its generic frameworks to final Seedream/Higgsfield prompts.
The Studio's tested model-specific prompt structure has higher priority.

---

# 5. Tools / Skill Packs NOT Recommended as Baseline

## Superpowers
Repository:
`https://github.com/obra/superpowers`

Do NOT install as the default Studio workflow.

Reason:
- useful software-engineering discipline,
- but public reports show substantial token/context overhead in some Claude Code workflows,
- it can add planning/review loops that are unnecessary for routine Studio production.

Evaluate only for major software refactors if needed.

---

## Huge Skill Collections

Do not bulk-install:
- hundreds of community skills,
- broad agent packs,
- overlapping prompt-engineering skills.

Why:
Skill metadata, MCP tool definitions, startup instructions, and accidental triggering all add complexity/context.

Install the smallest capability set that solves a measured problem.

---

## Community Higgsfield Prompt Packs

Examples exist for Seedance/cinematic workflows.

Do not activate them globally by default.

Reason:
many are optimized for cinematic video/Seedance rather than the Studio's current locked Seedream image workflow.

If one contains a useful technique:
1. inspect it,
2. extract the specific useful idea,
3. test that idea against the Studio baseline,
4. promote only after evidence.

Never import an entire external prompt doctrine into the canonical Studio prompt.

---

# 6. Claude Code Context Settings

## 6.1 Keep CLAUDE.md Small

Target:
`< 200 lines`, preferably substantially less.

`CLAUDE.md` should contain only:
- Studio role,
- source-of-truth rule,
- cost boundary,
- instruction to resolve canonical manifest,
- instruction to retrieve only required context,
- instruction not to duplicate vision processing.

Do NOT include:
- complete System Architecture,
- full Character Bible,
- old experiments,
- full prompt presets,
- long examples.

---

## 6.2 Do Not Import the Full Architecture

Avoid this:

```markdown
@AI_Influencer_Studio_System_Architecture_v0.2.2.md
```

inside the root `CLAUDE.md`.

Imported CLAUDE.md content loads at session startup and defeats the Studio's selective-context design.

Instead:
- store architecture normally,
- retrieve relevant sections on demand,
- use a deterministic section extractor if necessary.

---

## 6.3 Use Path-Scoped Rules

Create small `.claude/rules/` files only when their scope is clear.

Suggested:

```text
.claude/rules/
  prompts.md
  database.md
  mcp.md
```

Keep each short.

Do not create rules that duplicate canonical creative documents.

---

## 6.4 Use Subagents for Context Isolation

Use a subagent when a task would flood the main conversation with:
- filesystem exploration,
- many experiment logs,
- large code search results,
- external documentation.

Suggested subagent:

```yaml
name: studio-explorer
model: haiku
purpose: search files/metadata/history and return a compact evidence summary
```

Rules:
- no image-pixel analysis,
- no canonical promotion,
- no final prompt rewriting,
- return IDs/paths + concise findings only.

Main Claude/Sonnet keeps:
- production decision,
- prompt revision,
- canonical-state decisions.

Do NOT spawn subagents for trivial one-file tasks.

---

## 6.5 Auto-Compaction

Start with Claude Code's default/automatic compaction behavior.

Do not increase the context window just because a larger window exists.

Measure actual Studio sessions first.

If long sessions repeatedly accumulate irrelevant history:
- start a clean session for unrelated work,
- use subagents for large exploration,
- use Context Mode,
- compact deliberately when appropriate.

---

# 7. Token-Efficient Studio Skills

These Skills should be thin operational wrappers around the architecture, not copies of it.

## A. `select-references`

Goal:
Resolve the minimum/current validated reference set without loading unrelated history.

Implementation rules:
- receive structured ProductionRequest,
- resolve manifest/lane/preset,
- search only relevant asset metadata,
- retrieve historical evidence only when needed,
- output asset IDs + roles + confidence,
- do not load images unless explicitly delegated to a vision worker.

Target SKILL.md size:
`~50–100 lines`

Put detailed schemas in `references/` only if necessary.

---

## B. `higgsfield-prompt-audit`

Goal:
Improve or validate a Higgsfield prompt without casually rebuilding a locked baseline.

Inputs:
- selected locked prompt or candidate,
- selected provider/model,
- relevant Workflow Master section,
- optional upstream Higgsfield reference.

Checks:
- prompt length,
- duplicated constraints,
- conflicting roles,
- unnecessary wording,
- model-specific incompatibilities,
- accidental change to locked behavior.

Output:
```text
PASS
or
PATCH ONLY
```

Prefer a patch/diff over rewriting the entire prompt.

---

## C. `revise-generation`

Goal:
Convert normalized QC + user feedback into the smallest useful revision.

Never re-read every historical experiment.

Retrieve only:
- current GenerationPlan,
- current QC report,
- matching validated failure recipes.

Output:
- KEEP,
- CHANGE,
- REMOVE,
- expected effect.

---

## D. `optimization-audit`

Goal:
Run explicit baseline-vs-candidate experiments.

This Skill should use `context: fork` or an isolated subagent because optimization audits can be context-heavy.

It may challenge:
- reference count,
- reference order,
- masking,
- prompt wording.

It may NOT silently update canonical state.

---

# 8. Deterministic Scripts Instead of LLM Tokens

Whenever a task can be deterministic, use code.

Create small scripts for:

```text
prompt length counting
prompt hashing
duplicate-line/phrase checks
manifest validation
reference-order validation
file existence checks
experiment schema validation
QC schema validation
architecture section extraction
```

Claude should execute these scripts instead of repeatedly reasoning over raw text.

Recommended examples:

```text
scripts/
  prompt_check.py
  manifest_check.py
  generation_plan_check.py
  extract_md_section.py
```

This keeps large reference files out of Claude context.

---

# 9. Suggested Prompt Quality Pipeline

For a routine production request:

```text
user request
→ canonical manifest
→ lane/preset resolution
→ select-references
→ retrieve exact locked prompt when applicable
→ deterministic prompt/reference validators
→ higgsfield-prompt-audit only if change is needed
→ manual Higgsfield
→ external/manual vision QC
→ revise-generation
```

Do not invoke generic prompt-improvement skills automatically on every run.

For Optimization Audit Mode:

```text
baseline
→ hypothesis
→ isolated prompt/reference candidate
→ controlled Higgsfield test
→ normalized QC
→ compare
→ user approval
→ canonical promotion
```

---

# 10. Setup Task for Claude Code

Claude should perform the following without modifying the System Architecture:

1. Inspect existing Claude/project configuration.
2. Preserve existing files.
3. Check whether Skill Creator is already available.
4. Install Context Mode as a project/user plugin only after recording a baseline.
5. Verify Context Mode with `ctx-doctor`.
6. Add ccusage as an on-demand measurement command; do not enable its statusline automatically.
7. Clone official Higgsfield skills to `vendor/higgsfield-official-skills` as reference-only.
8. Add `.repomixignore`.
9. Review root `CLAUDE.md` and reduce it below 200 lines if necessary.
10. Ensure the full System Architecture is NOT imported by CLAUDE.md.
11. Create a `studio-explorer` context-isolated subagent.
12. Create thin Studio Skills:
    - `select-references`
    - `higgsfield-prompt-audit`
    - `revise-generation`
    - `optimization-audit`
13. Use Skill Creator to create eval cases for those Skills.
14. Create deterministic validation scripts.
15. Run a dry production-planning test with NO Higgsfield generation.
16. Record before/after token/context measurements.

---

# 11. Dry Test

Use:

> 회사에서 찍은 것처럼 자연스럽고 캐릭터 얼굴이 잘 유지되는 반신 SNS 이미지를 만들고 싶다. 기존 canonical 자료와 현재 자산에서 필요한 것만 골라 Higgsfield 생성 계획을 만들되 이미지는 생성하지 마.

Expected behavior:

```text
resolve manifest
→ load only relevant lane/preset rules
→ metadata/reference search
→ compact reference decision
→ retrieve/build prompt
→ deterministic validation
→ stop before generation
```

Failure conditions:

```text
reads all project documents
reads all experiment history
loads image pixels unnecessarily
rewrites a locked prompt without reason
invokes generic prompt frameworks automatically
invokes Higgsfield generation
```

---

# 12. Acceptance Metrics

Compare baseline vs configured Claude:

```text
main-context tokens
number of compactions
tool-output bytes/tokens entering main context
number of files unnecessarily read
time to GenerationPlan
prompt length
prompt conflict count
user corrections required
Higgsfield generations per approved image
```

Tooling should remain only when it improves measured Studio performance.

---

# 13. Source Priority for External Tool Knowledge

For tooling behavior:

```text
1. current official project repository/docs
2. current Claude Code documentation
3. reproducible local evaluation
4. active issue/discussion evidence
5. GitHub popularity
```

Stars are an adoption signal, not proof of quality.

---

# 14. Final Recommended Baseline

Keep active:

```text
Claude Code
Studio project Skills
Context Mode (only if A/B test passes)
```

Use on demand:

```text
ccusage
Repomix
official Higgsfield upstream reference
Skill Creator
Promptfoo (Phase 2)
```

Do not baseline-install:

```text
Superpowers
huge skill packs
multiple overlapping prompt frameworks
community Higgsfield prompt packs
automatic Higgsfield browser/API generation
```

The Studio's own tested prompt/reference logic must remain the authority.
