---
description: List every /soul-* command with when it fires. Read the commands/ directory at runtime so the list stays current as commands are added or removed. Quality-of-life utility — does not change project state.
---

# /soul-help — list the soul commands

A read-only roster. Reads the commands directory at runtime so this stays current
without manual maintenance — adding a `commands/soul-<name>.md` makes it show up
here on next invocation; removing one makes it disappear.

## What to do

1. **Find the commands directory.** Prefer the live source — `commands/` at the
   Soul System repo root (the `@import` source if `CLAUDE.md` points there;
   otherwise the symlink target of `~/.claude/commands/soul-help.md`). Fall back
   to `~/.claude/commands/` listing if the repo path can't be resolved.

2. **List every `soul-*.md`** in alphabetical order. For each:
   - Command name: filename without `.md`, prefixed with `/`.
   - One-line summary: the `description:` from frontmatter, **first sentence only**
     (truncate at the first `. ` to keep one line per row).

3. **Present as a compact table:**

   ```
   /soul-init       — Initialize project as a Soul dogfood (creates CLAUDE.md with seed import).
   /soul-resume     — Pick up where the last session left off (reads .soul/handoff.md).
   /soul-handoff    — Write a thin handoff cursor for the session boundary.
   /soul-tasks      — Refresh the task tracker, present a tiered now/next/later list.
   /soul-idea       — Capture a forward-looking idea (low ceremony).
   /soul-finding    — Scaffold a graduated finding (the Body decides graduation).
   /soul-skill      — Capture verified tool know-how as a governed skill.
   /soul-explain    — Read-only explanation of current state.
   /soul-verify     — Pre-completion verification gate (Body-invoked).
   /soul-expand     — Pre-framing expansion gate (Body-invoked).
   /soul-help       — This list.
   ```

   The example shows the SHAPE — generate from the actual directory each time.

4. **End with two pointers** (one line each):
   - `Full philosophy: philosophy/the-soul.md — consult on demand, not auto-loaded.`
   - `Open findings: findings/open/ · Ideas: ideas.md · Witness: witness.md`

## What not to do

- **Do not hand-curate the list.** Generate from the directory each run, so adding
  or removing a command keeps the help honest without a separate update step.
- **Do not invent commands** that don't have a file. Only list what is on disk.
- **Do not show full descriptions.** One line per command. The full doc is
  one `Read` away.
- **Do not change project state.** Read-only; no writes, no commits.

---

**Source:** Built by the Artificer for SOUL-I015 (a roster utility — the smallest
useful onboarding aid). Generates from the live directory so it cannot drift from
reality. **Adopted:** 2026-05-26. **Status:** active.
