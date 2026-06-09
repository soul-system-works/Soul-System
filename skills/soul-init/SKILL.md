---
name: soul-init
description: Initialize the current project as a Soul System dogfood project — creates a CLAUDE.md with the seed import.
disable-model-invocation: true
---

# /soul-init — load the Soul System into the current project

**Soul System root on this machine:** `/mnt/d/Projects/Soul-System`

If that path is wrong for the machine you are running on, edit this file and change the path above before invoking the command. (When this command is installed as a symlink to the repo — the SOUL-F029 distribution model — editing the symlink edits the repo's canonical copy.)

## What to do

1. Determine the current working directory (the project root). Do not search upwards; use the directory the session was started in.

2. Check whether `CLAUDE.md` already exists in that directory.
   - **If it exists:** read it. If it already contains the line `@/mnt/d/Projects/Soul-System/operations/CLAUDE.md`, report "already initialized" and stop. If it exists but does not contain that line, report the existing contents and ask the user whether to append the import line or leave it alone. Do not overwrite without explicit confirmation.
   - **If it does not exist:** create it containing exactly one line:
     ```
     @/mnt/d/Projects/Soul-System/operations/CLAUDE.md
     ```

3. After creating or confirming the file, report:
   - The absolute path of the `CLAUDE.md` you wrote or found.
   - That the next Claude Code session opened in this directory will load the Soul Seed and the full philosophy.
   - A one-line reminder: the philosophy will only take effect from the *next* session — the current one is already loaded.
   - **Mention the optional Mind layer**: once the project has accumulated enough record-evidence to warrant compression, run `/soul-distill` to create a project-scoped `mind.md` at the project root, then add a second import line `@mind.md` after the seed import to load it always-on. Skip on day-1 — the Mind is earned, not seeded.

## What not to do

- Do not copy any Soul System files into the project. The whole point of this setup is that the philosophy stays in one canonical location and is referenced by import.
- Do not write anything other than the single import line. If the user wants project-specific context, that belongs in a separate file or below the import line — but `/soul-init` itself adds only the import.
- Do not modify the Soul System repo from this command. It is read-only as far as `/soul-init` is concerned.

---

**Source:** Built by the Artificer as the Soul System's bootstrap command (the `@import` installer). Brought into the repo and put on the symlink (live-reference) distribution model under [[SOUL-F029]] — it previously lived only in `~/.claude/commands/`, the source-of-truth gap that finding names. **Adopted:** 2026-05-19 (repo-canonical 2026-05-22). **Status:** active.
**NOTE (machine-local):** the "Soul System root on this machine" path above is the one machine-specific datum in this command; on a new machine, edit it (or template it) — the F029 portability wrinkle, deferred.
