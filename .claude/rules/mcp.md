# MCP / Tool Output Rules

Scope: any MCP server call, Bash command, or file read that can return large output.

- Route large/raw results (search hits, logs, metadata dumps, file listings) through
  `.claude/agents/studio-explorer.md` rather than pulling them directly into main context.
- Ask for the narrowest query the tool supports (specific IDs, filters, line ranges) before
  falling back to a broad read.
- Summarize before reporting back to the user; don't paste raw tool output wholesale unless
  the user asked to see it.
- Vision/image tool calls follow the staged QC policy in Architecture §52.1 — deterministic
  checks first, deep multi-reference comparison only for shortlisted candidates or disputes.
