# Tooling Setup Status

Source spec: `.md/CLAUDE_TOOLING_EFFICIENCY_PROFILE_v0.1.md`
Last updated: 2026-08-16 — see note below, most of "Not started" is now built.

## Active now (scaffolded this session)

- `CLAUDE.md` — lean root instructions, no architecture import
- `.claude/rules/{prompts,database,mcp}.md` — path-scoped rules
- `.claude/agents/studio-explorer.md` — haiku, read-only, context-isolated search subagent
- `.claude/skills/{select-references,higgsfield-prompt-audit,revise-generation,optimization-audit}/`
  — thin skill wrappers + hand-written `evals.md` eval cases each
- `scripts/{prompt_check,manifest_check,generation_plan_check,extract_md_section}.py`
  — deterministic validators
- `.repomixignore` — excludes assets/generations/qc/experiments/db/vendor/git/node_modules

All of the above were built without installing anything external or touching a
network resource. Nothing here required Skill Creator, Context Mode, or a vendor clone.

## Deferred — not installed, by user choice this session

These require pulling third-party code/hooks from GitHub. Run them yourself when ready;
nothing above depends on them.

### Context Mode (session context reduction plugin)

```text
/plugin marketplace add mksglu/context-mode
/plugin install context-mode@context-mode
/reload-plugins
/context-mode:ctx-doctor
/context-mode:ctx-stats
```

**Required A/B test before keeping it** (profile §3.A) — do not assume it helps this project:
1. Run 3 representative Studio dev/retrieval tasks without it.
2. Run 3 comparable tasks with it enabled.
3. Compare: main-context tokens, tool-call count, compactions, mistakes from missing
   context, wall time (use the metrics log below + `ccusage`).
4. Keep only if it measurably improves the Studio workflow. If the hook-based plugin is
   unstable, try MCP-only mode instead: `claude mcp add context-mode -- npx -y context-mode`.

Reminder: Context Mode's session DB is never canonical Studio memory — see
`.claude/rules/database.md`.

### Vendor reference repos (read-only, outside `.claude/skills/`)

```bash
git clone --depth 1 https://github.com/higgsfield-ai/skills.git vendor/higgsfield-official-skills
```

Re-sync later with:
```bash
git -C vendor/higgsfield-official-skills pull --ff-only
```

Only consult it selectively from `higgsfield-prompt-audit`; never let it override a locked
Studio prompt, reference order, or the manual-generation boundary (Architecture §16).

Optional, only if Skill Creator is wanted (check first whether the current Claude Code
install already bundles it — don't install a duplicate):
```text
https://github.com/anthropics/skills
```

### ccusage (on-demand measurement only — no install step needed)

```bash
npx ccusage@latest claude daily
npx ccusage@latest claude session
npx ccusage@latest claude monthly
```

Do **not** enable a continuously-spawning `npx ccusage statusline` by default (known
CPU/process overhead). If a statusline is wanted later, install ccusage directly instead of
repeatedly bootstrapping via `npx`, and test CPU behavior first.

### Promptfoo / Prompt Architect

Phase 2 / optional — install only when a stable prompt-generation function exists to test
against, or when restructuring Claude/skill/subagent prompts specifically (never applied
automatically to final Seedream/Higgsfield prompts).

## Studio implementation status (superseding the "not started" note below)

Architecture §46 items 01–12 are built and tested (`app/`, `tests/`, real data in
`canonical/` and `database/studio.db` — see `pytest -q`, currently 44 passing). This is
Studio-architecture implementation, technically out of this tooling profile's original scope,
but recorded here since the section below is now factually stale otherwise. Also live:
`canonical/gpt_bridge/` (Claude↔GPT QC and reference-generation bridges),
`canonical/prompt_lab/` (Higgsfield prompt methodology from real case evidence), and an
iterative `Image Generation/` test-loop for candidate master builds. Items 13–18
(vision/QC schema, experiment logging, memory, MCP/CLI, provider integrations) are still not
built.

### Dry test (profile §11) — now runnable, but will still stop before generation

```text
회사에서 찍은 것처럼 자연스럽고 캐릭터 얼굴이 잘 유지되는 반신 SNS 이미지를 만들고 싶다.
기존 canonical 자료와 현재 자산에서 필요한 것만 골라 Higgsfield 생성 계획을 만들되
이미지는 생성하지 마.
```

Expect: manifest resolve → relevant lane/preset only → metadata search → compact reference
decision → prompt retrieval/build → deterministic validation → **stop before generation** —
now for a real reason (`MissingFaceMaskedDerivativeError` until a masked Daily Reference is
registered) rather than a missing manifest. Fail conditions unchanged: reading all documents/
experiment history, loading image pixels unnecessarily, rewriting a locked prompt without
reason, invoking generic prompt frameworks automatically, or invoking Higgsfield generation.

## Metrics log (fill in once real sessions run)

| Date | Task | Context Mode? | Main-ctx tokens | Tool-output bytes in main ctx | Compactions | Unneeded files read | Time to GenerationPlan | Prompt length | Prompt conflicts | User corrections | Higgsfield gens / approved image |
|------|------|----------------|------------------|-------------------------------|--------------|----------------------|--------------------------|----------------|-------------------|--------------------|------------------------------------|
|      |      |                |                  |                                |              |                      |                          |                |                   |                     |                                     |

Pull token numbers from `npx ccusage@latest claude session` (or `daily`) for each session
compared. Treat ccusage numbers as directional, not authoritative billing figures.
