# `/soul-migrate` — move a project to another computer (v1, Fast)

**Status:** approved design, 2026-10-19 — the Body's grilling session on SOUL-I067
(I067's entry records the approval).
**Scope:** one project-invoked skill with a pack side and a receive side, and one
small helper. Fast mode is built; Standard and Thorough are written guidance only.
Machine-level state is out (SOUL-I068, deferred).

## Why

Moving to a new computer loses what git does not carry: gitignored records
(`witness.md`, `.soul/`), `.ai/` working files, untracked inputs, uncommitted work,
local branches and stashes, and the project's Claude memory folder (kept outside the
repo, under a name derived from the project's path). An adopting project (NAV-TOOL)
piloted a migration skill; its lessons shape this one. The Body asked for the
lightest version that works — the AI running the move can cover gaps — so v1 keeps
the pilot's two load-bearing ideas (verify every file on arrival; never overwrite on
placement) and leaves its archive/split/encrypt/snapshot machinery out.

## How it is used

Per project, in that project's own session:

1. `/soul-init` — tidies the record layout (its step 3e moves stray working files
   into `.ai/`). `/soul-migrate` checks this and asks; it never embeds it.
2. `/soul-migrate` — the pack side. One round of questions, one approval box, one zip.
3. Carry the zip. On the new computer, with the plugin installed:
   `/soul-migrate receive <zip>` in a fresh session.

Works in a repo that is not a Soul project: it packages what is there and offers
`/soul-init` (or a CLAUDE.md / AGENTS.md) as one question — never creates them unasked.

## Pack side (Fast)

1. **Wiring check.** Soul project with a current layout → continue. Layout not
   current → one line: "record layout not current — run `/soul-init` first?" Not a
   Soul project → note it; offer setup once.
2. **Inventory** (`migrate.py inventory`, read-only):
   - git: HEAD, every local branch (flag ones with no upstream), stashes (a bundle
     carries only the newest stash — more than one → offer to turn them into
     branches), other worktrees (their uncommitted files are not carried — warn),
     submodules, LFS (flagged, not packed), the remote URLs;
   - uncommitted changes (tracked) and untracked + ignored files, grouped, with sizes;
   - **rebuildable** groups (`node_modules`, `.venv`, `__pycache__`, `dist`, `build`,
     framework build dirs) with the command that rebuilds each, from its lock file;
   - **credential-like** paths (`.env*`, keys, `*credentials*`, token files,
     `.claude/settings.local.json`, …) — names only, never packed unless the owner
     force-includes one; passwords in remote URLs are stripped;
   - the project's **Claude memory folder**, found by the `cwd` recorded in the
     transcripts under `~/.claude/projects/*/` — never by decoding a folder name
     (hyphenated paths decode wrongly: 26 of 47 folder names on the 2026-10 machine
     decoded to a path that does not exist — counted while building this, 2026-10-19);
   - **dependencies by name**: enabled plugins, global skills and agents the project's
     instructions mention, project-local `.claude/` and `.codex/` content, tools the
     project's scripts call (`node`, `python3`, …).
3. **One round of questions:** commit uncommitted work first? (recommended; the owner
   commits) · untracked files: all / pick / none · rebuildable folders: leave out
   (default) / include · output folder (suggest the Downloads folder when it can be
   found; fallback `<project>/.ai/migrate-out/`, which the packer always skips) ·
   the one smoke check to run on arrival (e.g. the test command).
4. **Approval box** — one plain summary of exactly what will be packed, left out and
   rebuilt, sizes, credentials found, memory folder, dependencies and output path.
   Approve / change / cancel. Nothing is written before approve.
5. **Witness entry** (Soul projects): what is being moved, what is left out, and why
   — written before packing so it travels.
6. **Pack** (`migrate.py pack`): one plain zip holding
   `repo.bundle` (`git bundle --all`) · `worktree.patch` (uncommitted tracked changes,
   if any) · `files/` (approved untracked/ignored files) · `memory/` · `RECEIVE.md`
   (rendered receiving instructions: old path, remote URLs, rebuild commands, smoke
   check, dependency list) · `manifest.json` (sha256 and size of every member, and the
   project metadata). Prints the zip's sha256 — carry it separately if you want an
   integrity check that does not live on the same medium.
7. Nothing is pushed, published, deleted or reset. The source stays as it was.

The zip is not encrypted. Credential-like names are left out — a name list, not a
content scan — and passwords are stripped from remote URLs; records can still hold
private material — treat it as private, and encrypt it yourself if the carrier needs it.

## Receive side

1. `migrate.py verify <zip>` — every member's hash against the manifest; the zip's
   sha256 against the carried one if given. Any mismatch stops.
2. Ask for the new project path (suggest the old one). It must not exist, or be empty.
3. `migrate.py place <zip> <path>` — clone from the bundle, recreate every branch,
   set the remotes back to the recorded URLs, apply `worktree.patch`, restore `files/`
   with no overwrite (stop on conflicts, path traversal, case collisions, symlinks
   that escape the project).
4. **Memory:** place `memory/` under `~/.claude/projects/<key>/memory`, where `<key>` is
   derived from the new path. The rule is not documented; observed on the 2026-10
   machine, every character other than letters and digits becomes `-` (the branch's
   review counted 17 folders with a recorded `cwd` fitting it, one with a `_`; `.`
   and spaces unobserved),
   so the step ends by asking the owner to open a session in the new
   path and confirm the memory loaded; if not, move it to the folder that session
   created.
5. **Dependencies:** check each name; list what is missing. Missing is reported, not
   a restore failure.
6. **Rebuild** with the recorded commands, after confirming them.
7. **Smoke check** — run it; record the result. A skipped or failed check is not a pass.
8. **Witness entry** with the five milestones kept separate — prepared · transferred ·
   restored · workflow checked · owner accepted. Retiring the source is the owner's
   call, later.

## Standard and Thorough (guidance only, no code)

| | adds to Fast |
|---|---|
| Standard | external documents and shared tools the selected workflows use; representative workflow checks; settings reconciliation |
| Thorough | a recursive dependency audit; historical worktrees and outputs; private histories as references; output comparison against recorded results |

Depth changes discovery, never the integrity checks. Never silently upgrade Fast.

## Pilot lessons kept (prose; the pilot's private detail stays with it)

- Classify by recoverability, not by git-ignore status: ignored is not disposable.
- Git recovery is more than a default-branch clone (branches, stashes, worktrees,
  submodules, LFS).
- The owner's current selection wins over any earlier inventory.
- Show where files will land before writing anything; staging approval is not
  overwrite approval.
- A self-contained receiving prompt must survive a fresh agent — the pilot's owner
  lost the destination thread once.
- A check that only finds an output folder has not checked anything; record what ran.
- Record time spent in discovery, copy and verification, so the next move can be
  judged against this one.

## Out of v1

Encryption, split volumes, database snapshots, history exports, a machine mode
(SOUL-I068), direct-directory transfer, rewriting paths inside files (the arrival
session handles each case), native Windows (POSIX only: Linux, macOS, WSL).

## Done when

`tools/test_migrate.py` passes, including a round trip in temp directories: a repo
with two branches (one unpushed), a stash, an uncommitted edit, an untracked file, an
ignored record file, a rebuildable folder and a fake memory folder is packed, verified,
placed at a different path, and compared — tree, branches, remotes, patch applied,
memory placed, rebuildable folder absent and listed. Then the live trial (an
adopting project the Body chose) runs pack here and receive on the new computer.
