---
name: soul-init
description: Initialize the current project as a Soul System dogfood project — creates a CLAUDE.md with the seed import and scaffolds the project's local record (ideas.md, witness.md, findings/).
disable-model-invocation: true
---

# /soul-init — load the Soul System into the current project

**Derive the Soul System root from this skill's own location (A022).** The harness
states this skill's base directory when it loads; the root is two levels up
(`<base>/../..` — this file lives at `<root>/skills/soul-init/`). That resolves
correctly for every distribution model: a symlinked skill resolves through the
symlink to the cloned repo (the SOUL-F029 model); a plugin-installed skill
resolves to the plugin's installed copy, which ships the whole repo — making
**plugin install + `/soul-init` a complete setup with no clone**. VERIFY before
writing: the derived root must contain `operations/CLAUDE.md` (resolve symlinks
to an absolute path first, e.g. `realpath`). If it does not, say so and ask the
Body where the Soul System lives — never write an import line you have not
verified resolves.

## What to do

1. Determine the current working directory (the project root). Do not search upwards; use the directory the session was started in.

2. Check whether `CLAUDE.md` already exists in that directory.
   - **If it exists:** read it. If it already contains an import line ending in `/operations/CLAUDE.md` (any root — a prior install may have used a different path), note "import already present" — **do not stop; continue to step 3** to ensure the local record scaffold exists (soul-init is idempotent: it backfills a missing record for an already-imported project). If it exists but does not contain that line, report the existing contents and ask the user whether to append the import line or leave it alone. Do not overwrite without explicit confirmation.
   - **If it does not exist:** ask one question — "Response register: plain or
     fluent?" (default **plain** if the user has no preference) — then create it
     containing the import line plus the Register line:
     ```
     @<derived-root>/operations/CLAUDE.md

     **Register: plain** — keep responses concise and in plain language; use a Soul
     or project term only when it earns its place, gloss it on first use in a
     session, and introduce vocabulary gradually. (Switch by editing this line;
     other value: `fluent` — full Soul vocabulary.)
     ```
     For `fluent`, write the line as `**Register: fluent** — full Soul vocabulary.`
     For an EXISTING CLAUDE.md that lacks a Register line, offer to add one
     (same default) — per the SOUL-I050 spec, the line lives in the project's
     CLAUDE.md, never in the seed.

3. **Scaffold the project's local record** at the project root (so `soul-capture` /
   `soul-handoff` / `soul-distill` have an unambiguous *local* target — the record is THIS
   project's, **never** the Soul System source repo). Create any that are absent; never
   overwrite an existing one:
   - `ideas.md` — a one-line header `# Ideas — <this project>` (the forward record).
   - `witness.md` — a minimal header naming it this project's Witness log (append-only,
     sequential IDs per the format in `operations/witness-log-format.md`).
   - `findings/open/` and `findings/closed/` — each with a `.gitkeep`.
   Skip `amendments/` — amendments are to the Soul itself and go upstream, not local.

4. After creating or confirming the file, report:
   - The absolute path of the `CLAUDE.md` you wrote or found.
   - That the next Claude Code session opened in this directory will load the Soul Seed and the full philosophy.
   - A one-line reminder: the philosophy will only take effect from the *next* session — the current one is already loaded.
   - **Mention the optional Mind layer**: once the project has accumulated enough record-evidence to warrant compression, run `/soul-distill` to create a project-scoped `mind.md` at the project root, then add a second import line `@mind.md` after the seed import to load it always-on. Skip on day-1 — the Mind is earned, not seeded.

## What not to do

- Do not copy any Soul System *doctrine* files into the project (the seed, philosophy, operations). The whole point is that the philosophy stays in one canonical location and is referenced by import. (Scaffolding the project's own empty record stores in step 3 is not copying — it is establishing *this* project's record.)
- Beyond the import line and the empty record scaffold, do not write project content. If the user wants project-specific context, that belongs in a separate file or below the import line — `/soul-init` adds only the import + the empty record.
- Do not modify the Soul System repo from this command. It is read-only as far as `/soul-init` is concerned.

---

**Source:** Built by the Artificer as the Soul System's bootstrap command (the `@import` installer). Brought into the repo and put on the symlink (live-reference) distribution model under [[SOUL-F029]] — it previously lived only in `~/.claude/commands/`, the source-of-truth gap that finding names. **Adopted:** 2026-05-19 (repo-canonical 2026-05-22). **Status:** active.
**NOTE:** the former machine-local root path (the F029 portability wrinkle) was retired by SOUL-A022 — the root now derives from the skill's own location, which also makes the plugin a complete install path.
