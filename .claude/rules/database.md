# Database / Canonical State Rules

Scope: any work touching the canonical manifest, SQLite asset DB, or experiment logs.

- The canonical manifest + SQLite DB (Architecture §50) is the source of truth for asset IDs,
  lanes, presets, and character masters — not chat history, not memory.
- Context Mode's session database (if installed, see `.claude/SETUP_STATUS.md`) is a context
  cache only. It is never canonical Studio memory and must never be treated as a source for
  asset IDs, presets, or approvals.
- Don't duplicate DB rows or experiment logs into the conversation. Query for the specific
  IDs/fields needed and return a compact result.
- Canonical promotion (marking a candidate/preset as approved/locked) is a decision only the
  user makes explicitly. No skill or subagent may perform it silently.
