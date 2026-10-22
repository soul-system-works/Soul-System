---
name: soul-init
description: Initialize the current project as a Soul System project — wires a live contract reference into the host's project instructions, loads an existing Mind if there is one, and scaffolds the project's local record after asking whether that record goes in version control, stays local, or (when this machine names a Soul vault) lives in the vault behind a `.soul` link.
disable-model-invocation: true
---

# /soul-init — load the Soul System into the current project

**Codex:** Read [the host integration](../../operations/codex.md) before
following this workflow. Its Codex procedures replace Claude-specific loading,
instruction-file, tool, and invocation mechanics; the shared workflow follows.

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
(step 0) is what catches it afterwards. **Headless runs never get the dialog**:
under `claude -p` this home-relative import did not load in 3 of 3 sentinel runs
while an in-project copy did (2026-10-19, Claude Code 2.1.303). So tell the Body
too: automated runs need the contract passed explicitly —
`--append-system-prompt-file <root>/operations/CLAUDE.md` (the SOUL-F038 fix).
Do not vendor a copy into the project; a copy never receives contract upgrades.

VERIFY before writing: the chosen root must contain `operations/CLAUDE.md`
(resolve symlinks to an absolute path first, e.g. `realpath`). If it does not,
say so and ask the Body where the Soul System lives — never write an import
line you have not verified resolves.

## What to do

1. Determine the current working directory (the project root). Do not search upwards; use the directory the session was started in.

2. Check whether `CLAUDE.md` already exists in that directory.
   - **If it exists:** read it. If it already contains an import line ending in `/operations/CLAUDE.md` (any root — a prior install may have used a different path), note "import already present" — **do not stop; continue to steps 3–3e** to ensure the record scaffold, the git-tracking answer and the Mind import are all in place (soul-init is idempotent: it backfills a missing record for an already-imported project). If it exists but does not contain that line, report the existing contents and ask the user whether to append the import line or leave it alone. Do not overwrite without explicit confirmation.
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

   **First, does this machine name a Soul vault?** Run
   `python3 <derived-root>/tools/vault.py where`. A vault is one private git repo
   holding every project's record, each reached by a `.soul` link (SOUL-I079).
   - **Exit 1, none named:** skip the rest of this paragraph — everything below
     runs exactly as it did before vaults. (If the owner asks for one: they create
     the private repo and clone it — on WSL, onto a Windows drive — then run
     `vault.py init <clone> --register`.)
   - **Exit 3, named but not there:** stop and tell the owner to clone the vault to
     that path first. Do not scaffold — on a new machine that makes a second record
     the vault then refuses.
   - **A vault named:** run `python3 <derived-root>/tools/vault.py check .` and
     branch on its line:
     - *lives in the vault* — skip the tracking question and 3b's `.gitignore`
       lines; continue at 3b's secret-guard setup.
     - *BROKEN* — never scaffold, never remove the link. If the vault holds the key
       the link names, re-link: `vault.py link . --key <that key> --label <the
       label in its project.md>`. Otherwise tell the owner to clone the vault so
       the link's target exists.
     - *TWO COPIES* — stop. Show both; which is current is the owner's call. Do not
       scaffold or link until they decide.
     - *the vault holds a record … nothing links to it* (a fresh clone, a new
       machine) — offer that re-link before anything else, so step 3b finds the
       record instead of scaffolding an empty second one.
     - *not linked* — the question below gets a third answer: **in the vault**
       (`<vault path>`) — private, kept with every other project's record, and
       invisible to this repo's git. If chosen, ask the **label** at once (the list
       in step 3f): a *restricted* project never goes in the vault, so say so and
       ask the two-answer question instead. The move itself is step 3f.

   **Is the repo public?** Check before asking — `gh repo view --json
   visibility` when a remote exists and `gh` is available; otherwise ask the Body.
   If it is public, say so in the question: **a tracked record in a public repo is
   public** — every witness entry, idea and Mind line, readable by anyone — and ask
   with no default. The question used to argue only for tracking and never asked
   (MODEL-TEST's upstream note, mining pass 2, SOUL-202).

   > "Keep this project's Soul record (witness, ideas, Mind) in version control? [Y/n]"

   For a public repo, the same question with no default shown — `[y/n]` — and the
   public consequence stated in it.

   **Default yes** for a private repo, and say why in one line when asking: a
   record outside git exists in exactly one copy, on one disk, with no history — and if this repo is
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
   absent; never overwrite an existing one. **Look for an existing store first, not
   only at the root and in `.soul/`** — `git ls-files '*ideas*.md' '*witness*.md'`
   (or a `find` for untracked files) also finds one under `docs/` (e.g.
   `docs/ideas.md`). If one exists, do not
   scaffold a second: ask the Body whether it is the record, and if so write the
   `.soul/` file as a one-line pointer to it (`Ideas live in docs/ideas.md —
   append there.`) instead of an empty store. MODEL-TEST's `docs/ideas.md` was
   missed and a second store scaffolded (mining pass 2, SOUL-202).

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
   - **In the vault** — write no `.gitignore` lines; step 3f hides the link in
     `.git/info/exclude`, which never leaves this machine.

   **Existing projects keep their layout.** If `witness.md` or `ideas.md` already
   exist — at the project root, under `.soul/`, or wherever the search above found
   them — those files ARE the record.
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

   **Secret guard** (`operations/secret-guard.md`, SOUL-I070) — **experimental**. In
   Claude Code the plugin already checks the AI's commits and pushes — git runs the
   check through its own hooks for every git the session runs (credentials block,
   private names warn). Set up its inputs and the commits it cannot see, using step 3's
   public/private answer:

   - **Private names — ask once.** "Any names that must not appear in this repo —
     clients, employers, people, a work email? One per line; `Name => TOKEN` suggests
     a replacement." For a public repo say it firmly: a name committed here is public.
     Write the answers to `.soul/private-names.txt` and add that path to `.gitignore`
     (already covered if `.soul/` is ignored whole). None: write nothing. Names that cut
     across projects go in `~/.claude/soul-private-names.txt` instead — say so.
   - **Hand commits — offer, not default.** Commits and pushes made outside an AI
     session run the repo's own hooks only. On yes, install three hooks — `pre-commit`,
     `commit-msg`, `pre-push` — in the directory printed by
     `python3 <derived-root>/hooks/secret-guard.py --own-hooks-dir` (it follows
     worktrees, submodules and a repo or global `core.hooksPath`; do NOT use
     `git rev-parse --git-path hooks`, which inside a session answers the plugin's own
     wrapper directory). For each, if a file is already there, do not overwrite it — it
     belongs to the owner or another tool (git-lfs, carried by five adopting projects,
     installs `pre-push`); say which hook was skipped and that hand commits/pushes are
     not checked at that step. Otherwise write it executable, with `<derived-root>`
     chosen by the version-pin guard above and `<hook>` replaced by the hook's name in
     all three places. It fails open, loudly, when the plugin path is gone (an update or
     a machine move), and stays quiet when a session's wrapper has already run the
     check for the same commit (it chains to this hook):
     ```sh
     #!/bin/sh
     # Soul System secret check (<hook>), installed by /soul-init (operations/secret-guard.md).
     guard="<derived-root>/hooks/secret-guard.py"
     if [ ! -f "$guard" ] || ! command -v python3 >/dev/null 2>&1; then
       echo "Soul secret check NOT running — plugin path missing; re-run /soul-init to repair the hook" >&2
       exit 0
     fi
     python3 "$guard" --hand-hook <hook> "$@"
     rc=$?
     [ "$rc" -eq 3 ] && exit 1
     [ "$rc" -ne 0 ] && echo "Soul secret guard failed (exit $rc) — this git <hook> was NOT checked" >&2
     exit 0
     ```
   - **Codex in use?** Say in one line that the guard is an opt-in there: the
     `shell_environment_policy` lines in `operations/secret-guard.md` (Codex's
     SessionStart context prints them with this machine's folder).
   - **History sweep — offer once.** `gitleaks git --redact --no-banner`, results to the
     owner. Rewrite nothing: a found credential is rotated first, and any rewrite is the
     owner's separate call (it runs on a native Linux filesystem, not a `/mnt` drive, and
     a rewritten-away commit stays fetchable by SHA on GitHub).
   - **gitleaks missing** (`command -v gitleaks`): say the credential check is not
     running until it is installed.
   - **Public repo: push protection.** Tell the owner whether it is on —
     `gh api repos/<owner>/<repo> --jq .security_and_analysis.secret_scanning_push_protection.status`
     (no value: say unknown). GitHub turns it on by default only for personal public repos
     created since 2024-03; user-level push protection is on by default for pushes to
     public repos.

   Skip `amendments/` **and `findings/`** — both are records of changes to *the
   Soul*, governed by `operations/amendment-process.md`, and they go upstream, not
   local. Scaffolding `findings/` locally produced 0 artifacts across 6 projects in
   3+ months while leaving two permanently empty directories in each; init used to
   create them and no longer does (2026-08-20).

3c. **Wire an existing Mind.** Before reporting, check whether the project already
   has a `mind.md` (at `.soul/mind.md` or the project root). If it does, add the
   matching import line directly after the contract import, and say you did. **Write
   the path relative to the file the line goes into**, since `@` paths resolve
   against the importing file (verified above): from a root `CLAUDE.md`,
   `@.soul/mind.md` or `@mind.md`; from `.claude/CLAUDE.md`, `@../.soul/mind.md` or
   `@../mind.md`. This step used to write `@.soul/mind.md` regardless, which points
   at `.claude/.soul/mind.md` when the contract import lives in `.claude/` —
   MODEL-TEST's Mind went unloaded that way (mining pass 2, SOUL-202).

   A Mind is always-on by design and does nothing whatsoever unless something
   imports it. Nothing in this skill used to check, so a project could distill a
   Mind and never load it: one adopting project has carried a 164-line Mind that
   no file imports, and another project's own record names the failure exactly —
   *"a deployed Mind that nothing loads is inert."* Checking costs one `ls`.

3d. **Offer the development stage — once, skippable — after the record exists.**
   Whether `CLAUDE.md` was just created or already existed, if no line in it starts
   `**Stage:`, open the `soul-stage` skill's own selection: read
   `<derived-root>/skills/soul-stage/SKILL.md` and follow its step 1 as a bare run —
   it reports the current state ("no stage declared", or a hand-written `**Phase:`
   block if one exists) and offers *Just looking* / prototype / pre-release /
   released with their descriptions. *Just looking* is the skip: say so, and
   continue to step 3e (which itself applies only to an already-initialized project). This step sits after 3b on purpose — a chosen stage ends in a
   witness entry, and until 3b has run there is no witness log to append to (the
   2.2.0–2.2.2 order had it before the scaffold; found by fresh-context review,
   2026-08-26, before any init ran it). Do not copy the skill's text or its
   question here — a copy written at init never receives an upgrade, the same reason
   the register default lives in the contract. **Skip writes nothing**: no line
   means released-grade caution, which is the contract's default. A chosen stage
   continues in that skill — its screen, block and witness entry — and lands the
   block directly under the Register line, or under the import when there is no
   Register line.

   *Evidence for asking here:* two adopting projects had the owner state "no
   backwards compatibility — this is beta" by hand on consecutive days
   (2026-08-24/25) — into two different always-on files, in two wordings, with no
   shared source.

3e. **Already initialized only: offer to move AI working files into `.ai/`.** Skip
   this step entirely for a fresh project. On the "import already present" path, run
   `python3 <derived-root>/tools/layout-cleanup.py scan <project>`. It flags only text
   files whose name or folder marks them as working material (plans, handoffs,
   reviews, scratch, stray `.soul/` files) — never code, tests, user docs or ADRs. No
   candidates: say nothing. Otherwise show its grouped dry run and ask per group with
   AskUserQuestion: *move to `.ai/`* / *leave* / *it is project content* / *decline
   all*. Decline all runs `decline <project>`, which changes nothing but the
   remembered list in `.soul/layout.json`. Otherwise write the answers to a plan file
   outside the project (`{"<path>": "move|leave|content"}`, paths from `scan --json`)
   and run `apply <project> --plan <file> --dry-run` first. A file it says project
   content links to is usually project content: put that file to the owner on its
   own before applying, since project content must never link into `.ai/`. Then run
   `apply` without `--dry-run`; any "project content now links into .ai/" line it
   still prints is an open gap — report it as one: drop the link or promote the
   file, the owner's call. Never add a path the scan did not flag. *Why:* project content, the
   durable record (`.soul/`) and AI working files (`.ai/`, safe to delete) each have
   one home.

3f. **Vault answer only: move the record into the vault.** Last, so the steps
   above have written everything into the record first. The label was asked in
   step 3, from this list:
   - **Label** — *public* (anyone may read it), *private* (yours), *confidential*
     (someone else's material, e.g. an employer's or client's — before an
     employer-hosted project moves, the owner decides whether a personal vault may
     hold it), *restricted* (closed or controlled; never in the vault, and the tool
     refuses it too).

   Ask the rest:
   - **What it contributes to** — free-form tags (e.g. `research, tools`); may be
     empty.
   - **Key** — the project's folder name in the vault; default the repo's name. The
     key, not the path, names the folder, so it survives the project moving.

   Run `python3 <derived-root>/tools/vault.py link . --key <key> --label <label>
   --contributes <tags> --dry-run`, show its lines, and on the owner's yes run it
   without `--dry-run`. What it does, so you can explain it: a root-layout record
   (`witness.md` at the root) moves into `.soul/` first and a `@mind.md` import is
   repointed to `@.soul/mind.md`; `.soul/` is copied into
   `<vault>/projects/<key>/soul/` and every file's hash compared; `.soul/` is
   replaced by a link, and compared again through it. On WSL with the project on a
   Windows drive the link is a Windows junction: Windows tools cannot follow a
   WSL-made symlink, so the vault must be on a Windows drive too. It adds `.soul` to
   `.git/info/exclude` and the vault to `.claude/settings.local.json`
   `permissions.additionalDirectories`, without which Claude Code refuses writes
   through the link. All three came from the I079 link test (2026-10-22).

   **If it prints STILL TRACKED, recommend `git rm --cached` of those files and a
   commit, now.** Until then, a git reset, stash, restore or checkout puts the old
   committed copy back in place of the link, writes go to that stale copy, and the
   vault falls behind — `check` reports it as TWO COPIES. Say too that the old copies
   stay in history: moving a record is not redaction (mind item 6d).
   The vault's own `.gitignore` keeps `private-names.txt` and `events.jsonl` out of
   the vault repo, so the private-name list does not travel to another machine —
   say so; the owner re-enters it there.

   **If `link` refuses or fails, the record stayed in the project.** Write 3b's
   `.gitignore` lines for whichever of step 3's two other answers the owner now
   picks — a record must never be left neither tracked nor ignored, where one
   `git add -A` commits it.

4. After creating or confirming the file, report:
   - The absolute path of the `CLAUDE.md` you wrote or found.
   - That the next Claude Code session opened in this directory will load the project contract (`operations/CLAUDE.md`) by import. The philosophy (`philosophy/the-soul.md`) is NOT imported — it is the human-facing book, read on demand (A021).
   - A one-line reminder: the philosophy will only take effect from the *next* session — the current one is already loaded.
   - **Mention the optional Mind layer**: once the project has accumulated enough record-evidence to warrant compression, run `/soul-distill` to create a project-scoped `mind.md`, then add a second import line after the contract import to load it always-on (path relative to that file, as in 3c). Skip on day-1 — the Mind is earned, not seeded.
   - **If the project's `CLAUDE.md` is itself gitignored**, say so plainly: the wiring is machine-local, and a fresh clone of this repo loads no contract at all. That can be a deliberate choice — say it is a choice, not a gap, and let the Body confirm.
   - **If a stage was declared**, say which, and that its rules take effect from the
     next session; if skipped, say that `/soul-stage` declares one later and that
     until then the project is treated as released.
   - **If the record moved into the vault**: the next session will ask, once, to
     load files from outside the project. Approve it — that is what loads the Mind
     through the link; declining disables it with no second dialog, and
     `/soul-resume`'s Mind check is what notices (the link test: a SessionStart hook
     cannot carry the Mind instead, its output is cut to ~2KB). And the vault counts
     as kept only once it is committed and pushed.

## What not to do

- Do not copy any Soul System *doctrine* files into the project (the seed, philosophy, operations). The whole point is that the philosophy stays in one canonical location and is referenced by import. (Scaffolding the project's own empty record stores in step 3b is not copying — it is establishing *this* project's record.)
- Beyond the import line and the empty record scaffold, do not write project content. (The one exception: step 3e's link repointing, after the owner chose the moves.) If the user wants project-specific context, that belongs in a separate file or below the import line — `/soul-init` adds only the import + the empty record.
- Do not classify files yourself in step 3e: move only what the layout scan flagged and the owner chose to move, and never delete one.
- Do not modify the Soul System repo from this command. It is read-only as far as `/soul-init` is concerned.

---

**Source:** Built by the Artificer as the Soul System's bootstrap command (the `@import` installer). Brought into the repo and put on the symlink (live-reference) distribution model under [[SOUL-F029]] — it previously lived only in `~/.claude/commands/`, the source-of-truth gap that finding names. **Adopted:** 2026-05-19 (repo-canonical 2026-05-22). **Status:** active.
**NOTE:** the former machine-local root path (the F029 portability wrinkle) was retired by SOUL-A022 — the root now derives from the skill's own location, which also makes the plugin a complete install path.
**Amended:** 2026-10-19 (mining pass 2, SOUL-202) — step 3 checks repo visibility before the tracking question; 3b finds an existing store outside root/`.soul/` (e.g. `docs/`) before scaffolding; 3c writes the Mind import relative to the importing file (extends F068).
**Amended:** 2026-10-20 (v2.10.0, SOUL-I070) — step 3b sets up the experimental secret guard: the project's private-name list (gitignored); optional hand-commit hooks (`pre-commit`, `commit-msg`, `pre-push`) placed in the repo's own hooks directory (`--own-hooks-dir`, since a session points `core.hooksPath` at the plugin's wrappers), never overwriting an existing hook, failing open loudly when the plugin path is gone, and not re-running a check the session's wrapper already ran; a one-line Codex opt-in pointer; a history-sweep offer; and push-protection status for public repos.
**Amended:** 2026-10-22 (v3.4.0, SOUL-I079) — the vault: step 3 checks for a vault named on this machine, re-links a record the vault already holds, and offers "in the vault" as a third answer; step 3f moves the record and links it (`tools/vault.py`); step 4 tells the owner to approve the one-time outside-files dialog and to push the vault.
