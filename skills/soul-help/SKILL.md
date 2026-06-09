---
name: soul-help
description: A short intro to the Soul System — what it is, the core gates, the commands, and where the durable record lives. The onboarding entry point ("--help" for the Soul). Reads skills/ at runtime so the list stays current.
disable-model-invocation: true
---

# /soul-help — what the Soul System is

A short, plain-language intro for someone new to this project (or a returning Body who
wants the lay of the land). Not a deep philosophy dump — point to depth, don't recite it.

## What to do

1. **One-paragraph what-it-is.** The Soul is a living philosophy that loads into every
   session (the seed `operations/CLAUDE.md` + the distilled `mind.md`) plus a durable record
   that accumulates across sessions (`witness.md`, `findings/`, `ideas.md`, `amendments/`).
   The seed orients; the record remembers what a later session couldn't re-derive. Full
   philosophy on demand: `philosophy/the-soul.md`.

2. **The core gates** (one line each): understand the abstraction before building (the AL
   gate); frame at two levels; explain existing state before changing it; verify against
   reality before calling done (fires automatically as a Stop hook); anchor every absolute
   claim with a valid external reference.

3. **The commands.** Read `skills/` at runtime and list each `soul-*/SKILL.md` with a one-line
   "when it fires" (the first sentence of its `description:`, ~100 char cap) — so this can't
   drift from what's on disk. (The `/soul-*` instruments are Claude Code **skills**; invoked
   the same way — `/soul-capture`, etc.) As of 1.0 the core is: `soul-init` (set up a project),
   `soul-capture <idea|witness|finding>` (write to the record), `soul-handoff` /
   `soul-resume` (continuity across sessions), `soul-explain` (describe the present;
   `council` mode for a multi-lens read), `soul-next` (what to do next), `soul-distill`
   (refresh the Mind).

4. **Where the record lives:** `witness.md` (observations, append-only) · `findings/`
   (earned patterns) · `ideas.md` (forward possibilities) · `amendments/` (doctrine
   changes).

Keep it skimmable. Quiet and clear (SOUL-I008) — an intro, not a manual.

## What not to do

- Do not recite the full philosophy — point to `the-soul.md`.
- Do not hand-curate the command list from memory — generate from `skills/` so it can't
  drift; only list what is on disk.
- Read-only; no writes, no commits.

---

**Source:** Built by the Artificer for SOUL-I015 as a command roster; reframed at the Cut
(→1.0, 2026-06-08) into a Soul-System intro / onboarding entry point. Generates the command
list from the live directory so it cannot drift. **Status:** active.
