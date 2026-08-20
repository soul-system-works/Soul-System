---
name: soul-init
description: Initialize the current project as a Soul System project — creates a CLAUDE.md with the contract import, wires an existing Mind if there is one, and scaffolds the project's local record (.soul/ideas.md, .soul/witness.md) after asking whether that record goes in version control.
disable-model-invocation: true
---

# /soul-init — load the Soul System into the current project

**Derive the Soul System root from this skill's own location (A022).** The harness
states this skill's base directory when it loads; the root is two levels up
(`<base>/../..` — this file lives at `<root>/skills/soul-init/`). That resolves
correctly for every distribution model: a symlinked skill resolves through the
symlink to the cloned repo (the SOUL-F029 model); a plugin-installed skill
resolves to the plugin's installed copy, which ships the whole repo — making
**plugin install + `/soul-init` a complete setup with no clone**.

**Version-pin guard (measured on the first live install):** a plugin-cache root
looks like `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` — that
path DIES at the next plugin update (new version directory), and a dead
`@import` fails silently (the F038 failure mode). When the derived root matches
that pattern, prefer the UNVERSIONED marketplace clone —
`~/.claude/plugins/marketplaces/<marketplace>/` — if it contains
`operations/CLAUDE.md`; it is updated in place and survives updates. If only
the versioned path exists, use it but TELL the Body: "this import is pinned to
plugin version <v>; re-run /soul-init after plugin updates."

**Write the path home-relative when it sits under the home directory.** Verified
against Claude Code's memory documentation (2026-08-20): CLAUDE.md `@` imports
accept absolute and relative paths, resolve relative paths against the importing
file, and support the `~/` form — they do **not** expand environment variables,
so there is no `${CLAUDE_PLUGIN_ROOT}` option here. So after deriving and
verifying the root, replace a literal home prefix with `~`:
`/home/<user>/.claude/plugins/...` → `@~/.claude/plugins/...`. Same file, but the
line no longer names one machine's user, which matters the moment the project is
cloned, shared, or opened by anyone who is not the Soul System's author. Five of
six adopting projects carry the hard-coded form (2026-08-20 retrospective); they
work only on the machine that wrote them.

**Warn about the external-import dialog.** An import that resolves outside the
working directory is "external", and Claude Code shows a one-time approval dialog
listing it. Per the documentation: *"If you decline, the imports stay disabled and
the dialog doesn't appear again."* Tell the Body this in step 4 — a single
mis-click permanently silences the contract in that project, and the failure looks
exactly like a session that simply ignores doctrine. `/soul-resume`'s wiring check
(step 0) is what catches it afterwards.

VERIFY before writing: the chosen root must contain `operations/CLAUDE.md`
(resolve symlinks to an absolute path first, e.g. `realpath`). If it does not,
say so and ask the Body where the Soul System lives — never write an import
line you have not verified resolves.

## What to do

1. Determine the current working directory (the project root). Do not search upwards; use the directory the session was started in.

2. Check whether `CLAUDE.md` already exists in that directory.
   - **If it exists:** read it. If it already contains an import line ending in `/operations/CLAUDE.md` (any root — a prior install may have used a different path), note "import already present" — **do not stop; continue to steps 3–3c** to ensure the record scaffold, the git-tracking answer and the Mind import are all in place (soul-init is idempotent: it backfills a missing record for an already-imported project). If it exists but does not contain that line, report the existing contents and ask the user whether to append the import line or leave it alone. Do not overwrite without explicit confirmation.
   - **If it does not exist:** ask one question — "Response register: plain or
     fluent?" (default **plain** if the user has no preference) — then create it
     containing the import line, plus a Register line ONLY if the answer was
     `fluent`:
     ```
     @<derived-root>/operations/CLAUDE.md
     ```
     ```
     @<derived-root>/operations/CLAUDE.md

     **Register: fluent** — full Soul vocabulary.
     ```
     **Write nothing for `plain`.** Plain IS the contract's default, and the
     contract arrives by import, so it stays current. A copied default does not:
     every register block written into a project at init still carried wording the
     contract had retired for being measurably ineffective. Only the OVERRIDE gets
     written locally — one line, because it differs from the default and therefore
     has to live where the difference is (SOUL-I050 kept; the duplication removed
     in v2.1.1 after fresh-context review found the contract and init both
     carrying the same default, always-on).

3. **Ask the one question that cannot be defaulted: does the record go in git?**

   > "Keep this project's Soul record (witness, ideas, Mind) in version control? [Y/n]"

   **Default yes**, and say why in one line when asking: a record outside git
   exists in exactly one copy, on one disk, with no history — and if this repo is
   ever cloned, submoduled, or worked on from a second machine, the lessons do
   not travel with it. A `no` is a legitimate choice (private or client-sensitive
   projects) but it must be a chosen one. Record the answer; step 3b writes it
   into `.gitignore`.

   *Evidence for asking rather than assuming:* two of six adopting projects had
   their record gitignored, one deliberately and one apparently by drift, and the
   drifted one is a plugin that gets submoduled — the case where the loss bites
   hardest (2026-08-20 cross-repo retrospective).

3b. **Scaffold the project's local record under `.soul/`** (so `soul-capture` /
   `soul-handoff` / `soul-distill` have an unambiguous *local* target — the record
   is THIS project's, **never** the Soul System source repo). Create any that are
   absent; never overwrite an existing one:

   - `.soul/ideas.md` — a one-line header `# Ideas — <this project>` (the forward record).
   - `.soul/witness.md` — a minimal header naming it this project's Witness log
     (append-only, sequential IDs per the format in `operations/witness-log-format.md`).

   Then write the `.gitignore` lines to match the step-3 answer:

   - **Yes, track it** — ignore only the volatile runtime state, never the record:
     ```
     # Soul System runtime state (cursor, event log) — never the record itself
     .soul/handoff.md
     .soul/events.jsonl
     ```
   - **No, keep it local** — ignore the whole directory: `.soul/`

   **Existing projects keep their layout.** If `witness.md` or `ideas.md` already
   exist — at the project root OR under `.soul/` — those files ARE the record.
   Leave them exactly where they are, do not move or duplicate them, and write the
   gitignore lines against whichever paths are real. Both layouts are first-class;
   the completion gate scopes on either (`hooks/test_scope.py` cases 5 and 7).

   **Tracking is a `.gitignore` edit, never a file move.** If a project's record is
   currently untracked because a broad `.soul/` ignore rule swept it up, the fix is
   to narrow that rule to `.soul/handoff.md` + `.soul/events.jsonl` and commit the
   record where it sits. Do not offer relocation as the price of tracking — a live
   run of this skill read the older wording as requiring a move to the project root
   and proposed one (2026-08-20). Moving a record costs a rewrite of every path
   that points at it and buys nothing.

   Skip `amendments/` **and `findings/`** — both are records of changes to *the
   Soul*, governed by `operations/amendment-process.md`, and they go upstream, not
   local. Scaffolding `findings/` locally produced 0 artifacts across 6 projects in
   3+ months while leaving two permanently empty directories in each; init used to
   create them and no longer does (2026-08-20).

3c. **Wire an existing Mind.** Before reporting, check whether the project already
   has a `mind.md` (at `.soul/mind.md` or the project root). If it does, add the
   matching import line directly after the contract import — `@.soul/mind.md` or
   `@mind.md`, whichever path is real — and say you did.

   A Mind is always-on by design and does nothing whatsoever unless something
   imports it. Nothing in this skill used to check, so a project could distill a
   Mind and never load it: one adopting project has carried a 164-line Mind that
   no file imports, and another project's own record names the failure exactly —
   *"a deployed Mind that nothing loads is inert."* Checking costs one `ls`.

4. After creating or confirming the file, report:
   - The absolute path of the `CLAUDE.md` you wrote or found.
   - That the next Claude Code session opened in this directory will load the project contract (`operations/CLAUDE.md`) by import. The philosophy (`philosophy/the-soul.md`) is NOT imported — it is the human-facing book, read on demand (A021).
   - A one-line reminder: the philosophy will only take effect from the *next* session — the current one is already loaded.
   - **Mention the optional Mind layer**: once the project has accumulated enough record-evidence to warrant compression, run `/soul-distill` to create a project-scoped `mind.md`, then add a second import line after the contract import to load it always-on. Skip on day-1 — the Mind is earned, not seeded.
   - **If the project's `CLAUDE.md` is itself gitignored**, say so plainly: the wiring is machine-local, and a fresh clone of this repo loads no contract at all. That can be a deliberate choice — say it is a choice, not a gap, and let the Body confirm.

## What not to do

- Do not copy any Soul System *doctrine* files into the project (the seed, philosophy, operations). The whole point is that the philosophy stays in one canonical location and is referenced by import. (Scaffolding the project's own empty record stores in step 3b is not copying — it is establishing *this* project's record.)
- Beyond the import line and the empty record scaffold, do not write project content. If the user wants project-specific context, that belongs in a separate file or below the import line — `/soul-init` adds only the import + the empty record.
- Do not modify the Soul System repo from this command. It is read-only as far as `/soul-init` is concerned.

---

**Source:** Built by the Artificer as the Soul System's bootstrap command (the `@import` installer). Brought into the repo and put on the symlink (live-reference) distribution model under [[SOUL-F029]] — it previously lived only in `~/.claude/commands/`, the source-of-truth gap that finding names. **Adopted:** 2026-05-19 (repo-canonical 2026-05-22). **Status:** active.
**NOTE:** the former machine-local root path (the F029 portability wrinkle) was retired by SOUL-A022 — the root now derives from the skill's own location, which also makes the plugin a complete install path.
