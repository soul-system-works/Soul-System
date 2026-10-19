---
name: soul-migrate
description: Move this project to another computer — packs what git does not carry (gitignored records, `.ai/`, untracked files, uncommitted work, every branch, the project's Claude memory folder) into one zip after one round of questions and one approval box; `/soul-migrate receive <zip>` restores it on the new computer, verifies every file, rebuilds and runs one smoke check. Owner-invoked; Fast mode.
disable-model-invocation: true
---

# /soul-migrate — move a project to another computer

**Codex:** Read [the host integration](../../operations/codex.md) before
following this workflow. Its Codex procedures replace Claude-specific loading,
instruction-file, tool, and invocation mechanics; the shared workflow follows.

## In short — when and how to use it

**Use it when** a project is moving to another computer (or another folder) and you
want everything back, not just what is on GitHub: gitignored records, `.ai/`,
untracked files, unpushed branches, uncommitted work, and the project's Claude memory.

**How:**

1. In the project, run `/soul-init` first if it is a Soul project (it tidies the
   layout). `/soul-migrate` asks if it looks needed.
2. Run `/soul-migrate`. Answer one round of questions, check the summary box, approve.
   You get one zip.
3. Carry the zip. On the new computer, install the Soul plugin, open a fresh session
   and run `/soul-migrate receive <path to zip>`. It asks where the project goes,
   checks every file, restores it, rebuilds, and runs one check.

Nothing is pushed, deleted or reset on either side. The zip is **not encrypted**.
Files with credential-like names are left out (a list of names, not a scan of
contents) and passwords are stripped from remote URLs — but an uncommitted change to a
tracked file travels in the patch whatever it holds, so treat the zip as private.

Everything below is the detail the AI follows. The helper is
`python3 <plugin-root>/tools/migrate.py`, where `<plugin-root>` is two levels above
this skill's directory. It is POSIX-only (Linux, macOS, WSL). Design:
`docs/specs/2026-10-19-soul-migrate.md`.

## Pack (`/soul-migrate`)

1. **Wiring check.** `witness.md` or `.soul/witness.md` present → a Soul project. If
   working files sit loose in the root or `docs/` (plans, reviews, handoffs), say one
   line — "record layout not current — run `/soul-init` first?" — and wait. Not a
   Soul project → say so, offer `/soul-init` (or a CLAUDE.md / AGENTS.md) once, and
   continue either way. Never create those unasked.
2. **Inventory.** Run `migrate.py inventory <project> --json`. It reads; it changes
   nothing. It can take minutes on a slow or Windows-mounted disk such as
   `/mnt/d` — give the Bash call a long timeout or run it in the background. Read
   its result — do not re-derive it by hand; groups carry at most 20 sample paths,
   so list a group's folder yourself if the owner wants to pick inside it — then add two things
   it cannot see: global skills and agents the project's instructions name (read its
   `CLAUDE.md` / `AGENTS.md`), and whether the output folder has room for the zip.
   A memory folder "found by folder name" (old transcripts already cleaned up) is
   real but unconfirmed — say so in the box.
3. **One round of questions**, all together (AskUserQuestion in Claude Code):
   - Uncommitted changes → *commit first (recommended)* / *carry them as a patch*.
     Committing is the owner's action; say what would be committed.
   - Untracked and ignored files (show the groups and sizes) → *all* / *pick* /
     *none*. Gitignored Soul records are recommended whatever the answer —
     ignored is not disposable.
   - Rebuildable folders (`node_modules`, build output, …) → *leave out and rebuild
     on arrival (recommended)* / *include*.
   - More than one stash, or other worktrees with uncommitted files → offer to turn
     them into branches first; the zip carries only the newest stash and no other
     worktree's working files.
   - Output folder → suggest the Downloads folder if it can be found (in WSL,
     Windows' Downloads); otherwise `<project>/.ai/migrate-out/`. Never anywhere
     else inside the project.
   - The one smoke check to run on arrival (suggest the project's test command).
   - Memory → *carry it (recommended)* / *leave it*; when the inventory found more
     than one candidate folder, ask which one.
   - A credential-like file the owner says is safe (a false match such as
     `docs/secretary.md`) → *force-include* it; never by default.
   - An operation in progress (merge, rebase, cherry-pick) → finish or abort it
     first; its state does not travel.
4. **Approval box.** Show one plain box of exactly what will happen, then wait for
   *approve* / *change* / *cancel*:

   ```
   ┌─ soul-migrate · <project> · Fast ──────────────────────────┐
   │ git bundle      <n> commits, <b> branches (<u> unpushed)   │
   │ uncommitted     <files>                     → commit|patch │
   │ local overrides <skip-worktree files> → carried | left out │
   │ untracked       <groups>                         <size>    │
   │ left out        <rebuildable>              → <rebuild cmd> │
   │ never packed    <credential-like names, or "none found">   │
   │ memory folder   <found | found by name — unconfirmed | none> │
   │ not carried     <nested repos, submodules, LFS objects, …>  │
   │ depends on      <plugins / skills / tools by name>         │
   │ smoke check     <command>                                  │
   │ output          <path>.zip                                 │
   └──────────────────────────────── approve / change / cancel ─┘
   ```

   Nothing is written before *approve*. Sizes come from the inventory; the zip's own
   size is known only after packing.
5. **Witness entry** (Soul projects only), through `/soul-capture witness`'s format:
   what is moving, what is left out and why, and how long discovery took. Write it
   before packing so it travels.
6. **Pack.** Write the approved choices to a selection file in the output folder —
   a JSON object with `untracked` (paths or group roots), `include_rebuildable`,
   `include_credential_like`, `exclude_flagged` (local-override files to leave out),
   `memory_key` (a folder name, or `false` for no memory),
   `smoke` and `notes`; `migrate.py pack --help` lists them — and run
   `migrate.py pack <project> --out <dir> --selection <file>`. Pack checks its own zip
   (hashes, a test clone, the patches, the placement plan) and deletes it if any check
   fails. Report the zip
   path, its size and its sha256 — the owner can carry the sha256 separately (a
   message, a note) for an integrity check that does not ride on the same medium.

## Receive (`/soul-migrate receive <zip>`)

1. **Verify:** `migrate.py verify <zip> [--sha256 <carried hash>]`. Any mismatch
   stops everything.
2. **Where it goes:** read `RECEIVE.md` from the zip; ask for the new project path
   (suggest the old one). It must not exist, or be empty.
3. **Preview, then place:** `migrate.py place <zip> <dest>` shows the plan; on the
   owner's go, `--apply`. It restores every branch, the remotes, the staged and
   unstaged changes and the approved files, and stops on any conflict — leaving the
   clone it made in place, so clear the folder before a second try.
4. **Memory:** `migrate.py memory-key <dest>` guesses the memory folder's name;
   `migrate.py place-memory <zip> --key <key> --apply` puts it there. The naming rule
   is not documented, so end this step by asking the owner to open a session in the
   new project and confirm its memory loaded — if it did not, move the folder to the
   one that session created.
5. **Dependencies:** check each name in `RECEIVE.md` (plugins installed, skills and
   agents present, tools on PATH). Report what is missing; missing is not a failed
   restore.
6. **Rebuild** with the commands in `RECEIVE.md`, after confirming them.
7. **Smoke check:** run it and report the result as it came out. Skipped or failed
   is not a pass.
8. **Witness entry** in the restored project, with five separate milestones:
   prepared · transferred · restored · workflow checked · owner accepted — and the
   time each step took, so the next move can be judged against this one. Retiring
   the old copy is the owner's call, later — never part of this run.

## Deeper modes (guidance only)

Fast is the only built mode. If the owner asks for more, add the discovery and
checks below — the integrity checks never change, and never upgrade silently:

- **Standard:** external documents and shared tools the selected workflows use;
  representative workflow checks; settings reconciliation.
- **Thorough:** a recursive dependency audit; historical worktrees and outputs;
  private histories as references (never imported into the live home); output
  comparison against recorded results.

## Not in v1

Encryption, split volumes, database snapshots, history exports, moving machine-level
state (`~/.claude` settings, `~/.codex`, local models — SOUL-I068, deferred: move it
by hand), rewriting paths inside files (handle each case on arrival), native Windows.

---

**Source:** SOUL-I067 (2026-10-19) — the Body's grilling session settled the design;
an adopting project's pilot (NAV-TOOL) supplied the lessons and the placement checks.
**Adopted:** pending review. **Status:** draft (branch `soul-migrate`).
