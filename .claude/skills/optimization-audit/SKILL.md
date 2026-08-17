---
name: optimization-audit
description: Run an explicit baseline-vs-candidate experiment challenging reference count/order, masking, or prompt wording. Use only when deliberately testing a hypothesis against the current locked baseline, not for routine production requests.
---

# optimization-audit

Structured experimentation, isolated from main context.

Because this can pull in many experiment logs and comparison images, run it via a forked
context or an isolated subagent (e.g. `studio-explorer` for evidence gathering, or a fresh
agent for the full audit) rather than inline in the main conversation.

## Input

- The current locked baseline (preset, reference order, prompt)
- The specific hypothesis being tested (e.g. "does dropping `image3` change body-proportion QC
  scores?")
- Candidate variant(s) to test against the baseline

## Steps

1. State the hypothesis and what would falsify it before running anything.
2. Build the candidate GenerationPlan(s) — isolated from the locked baseline, never editing
   the baseline in place.
3. Require the controlled Higgsfield test to be run manually (same cost boundary as everything
   else — this skill never submits generation itself).
4. Compare normalized QC results, baseline vs. candidate, on the same dimensions.
5. Report the comparison plainly, including inconclusive/negative results.

## Output

```text
HYPOTHESIS: ...
BASELINE: ...
CANDIDATE: ...
RESULT: <comparison, most relevant QC deltas>
RECOMMENDATION: promote | reject | inconclusive — needs more samples
```

## Hard constraint

This skill may **never** silently update canonical state. A `promote` recommendation is a
proposal; the user must explicitly approve canonical promotion (see `.claude/rules/database.md`).
