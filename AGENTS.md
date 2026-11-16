# AGENTS.md — The Soul System

This repository is the source of the **Soul System**: a one-page working contract, a
durable record, and a plugin of `/soul-*` commands for human–AI work. It layers above
how you already work; it does not replace it.

**The authority is the contract, `operations/CLAUDE.md`** (the name is historical, not
a Claude-only restriction). This file only points at it; where the two differ, the
contract wins.

## First actions (any tool, at session start)

Your tool loads this file; open the rest yourself:

1. Read `operations/CLAUDE.md` — the contract; everything in force.
2. Resume from the cursor, `.soul/handoff.md`, when one exists (on Claude Code:
   `/soul-resume`).
3. Read `mind.md` (this repo's project notes) and the tail of `witness.md` (the record
   of what this project has learned).

The record stores (`witness.md`, `ideas.md`, `upstream.md`, `mind.md`) live at the
project root or in `.soul/` — check both. The commands are the skills in `skills/`,
one folder each. `philosophy/the-soul.md` is the human-facing book: read it to
understand the system, not to operate under it.

## Codex (experimental)

The same skills ship as a Codex plugin (`.codex-plugin/`, invoked as
`$soul-system:soul-*`) with a hook adapter (`hooks/codex.json` → `hooks/codex.py`).
Codex has run them live (first runs 2026-10-19). This repo's `AGENTS.md` is written by
hand: do not run `tools/codex-project.py` here. What differs from Claude Code:
`operations/codex.md`.
