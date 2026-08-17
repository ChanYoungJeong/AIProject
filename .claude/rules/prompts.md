# Prompt Rules

Scope: any work touching a Higgsfield prompt (locked preset or candidate).

- A locked preset prompt (Architecture §48, e.g. `NAT_v1.4.3`) is authoritative for its lane
  only. Do not silently change it and do not let it redefine an unrelated lane/preset.
- Prefer a patch/diff over a full rewrite. Use `.claude/skills/higgsfield-prompt-audit` before
  changing a locked prompt.
- Respect the model's `max_prompt_length` (see the lane's `lane_policy.yaml` / manifest entry).
- Use `scripts/prompt_check.py` for length and duplicate-phrase checks instead of eyeballing it.
- Every GenerationPlan must record the prompt hash it used (Architecture §53) — don't hand-wave
  "the same prompt as last time."
