---
name: soul-init
description: Bring the current project under the Soul System, or check one that already is — wires a live contract reference into the host's project instructions, keeps the project's record (in git, local, or a Soul vault behind a `.soul` link), repairs what broke on this machine, and asks only the decisions never answered, remembering every answer in `.soul/init.md`.
disable-model-invocation: true
---

# /soul-init — bring a project under the Soul, or check one that is

**Codex:** Read [the host integration](../../operations/codex.md) before
following this workflow. Its Codex procedures replace Claude-specific loading,
instruction-file, tool, and invocation mechanics; the shared workflow follows.

Every run is the same three moves: **status** (what is set), **the plan** (every
decision never answered, shown at once with what Soul would do), then **carrying out**
the answers and the repairs (what broke on this machine, fixed from answers already
given). A fresh project gets one dialog; a project already set up usually gets none.
`tools/init-status.py` works out the state and holds every word the owner is shown;
this skill carries out the answers.

*Why a plan first* (SOUL-I092, the owner, 2026-11-12): "a person should be presented
with reasonable options and they should understand where their choices will lead and
not have to guess on when the setup will end." Until v3.13.0 a fresh project met three
picker screens, the vault's questions appeared only after it was picked, and the owner
asked twice what the "public" question did. So the whole setup is shown before anything
is written, every line says what the thing is, and the end is always the plan.

*Why this shape* (SOUL-I082, the owner, 2026-10-26): "it does the work correctly,
but the options that the user has to specify are not clear. Sometimes they seem kind
of strange, or if I've already initialized a project, it's unclear if I needed to
answer those certain questions again." Three exported runs showed it: re-runs
re-asked private names, hooks and the history scan, because "ask once" kept no
record; and each session worded its questions its own way.

## The Soul System root

**Derive it from this skill's own location (A022).** The harness states this
skill's base directory when it loads; the root is two levels up (`<base>/../..`).
That resolves for every distribution model: a symlinked skill resolves through the
symlink to the cloned repo (SOUL-F029); a plugin-installed skill resolves to the
plugin's installed copy, which ships the whole repo — so **plugin install +
`/soul-init` is a complete setup with no clone**. Below, `<root>` is that path.

**Version-pin guard (measured on the first live install):** a plugin-cache root
looks like `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` — that path
DIES at the next plugin update, and a dead `@import` fails silently (F038). When the
root matches that pattern, prefer the UNVERSIONED marketplace clone —
`~/.claude/plugins/marketplaces/<marketplace>/` — if it contains
`operations/CLAUDE.md`; it is updated in place. If only the versioned path exists,
use it but TELL the Body: "this import is pinned to plugin version <v>; re-run
/soul-init after plugin updates." Wherever a path is written into the project (the
import line, the hook script), `<root>` means the root this guard chose.

**Write the import path home-relative.** CLAUDE.md `@` imports accept absolute and
relative paths, resolve relative ones against the importing file, and support `~/`;
they do **not** expand environment variables, so there is no `${CLAUDE_PLUGIN_ROOT}`
option (Claude Code's memory documentation, verified 2026-08-20). So replace a
literal home prefix with `~`: `/home/<user>/.claude/plugins/...` →
`@~/.claude/plugins/...`. Five of six adopting projects carried the hard-coded form
and worked only on the machine that wrote them (2026-08-20 retrospective).

**VERIFY before writing:** the chosen root must contain `operations/CLAUDE.md`
(resolve symlinks first, e.g. `realpath`). If it does not, say so and ask the Body
where the Soul System lives — never write an import line you have not verified.

**The external-import dialog.** An import that resolves outside the project is
"external", and Claude Code shows a one-time approval dialog. Per the
documentation: *"If you decline, the imports stay disabled and the dialog doesn't
appear again."* One mis-click silences the contract for good, and it looks exactly
like a session that ignores doctrine (`/soul-resume` step 0 catches it). **Headless
runs never get the dialog**: under `claude -p` this import did not load in 3 of 3
sentinel runs (2026-10-19, Claude Code 2.1.303); automated runs need
`--append-system-prompt-file <root>/operations/CLAUDE.md` (SOUL-F038). Do not
vendor a copy into the project; a copy never receives contract upgrades.

## What to do

Work from the directory the session started in; do not search upwards. **Run
quietly:** between questions, say nothing about the steps you are taking ("Round 4",
"recording the answers") — speak to ask, to put a tracked-file change to the owner,
or to report a problem. The tool calls already show the work.

0. **`/soul-init revisit [key ...]`** — run `python3 <root>/tools/init-status.py
   revisit . [key ...]` first (no key: every answer), say what it forgot, and in
   step 1 add `--ask <key>` for each named key: an answer read from the files (a
   tracked record, a Stage line) stays set otherwise, and `--ask` is the way back
   (e.g. moving a git record into the vault).

1. **Status.** Run `python3 <root>/tools/init-status.py status . --json`. Its
   `items` (each with an `action`: none · repair · ask · stop), its `rounds` and its
   `plan` ARE the plan. Do not work the state out yourself, and ask nothing that is
   not in them.

2. **Stop items first.** Show each one's `detail` and end the run there: TWO COPIES
   (which record is current is the owner's call — do not scaffold or link until they
   decide); a vault named on this machine but not cloned, or a `.soul` link pointing
   at a missing folder (clone the vault there first — scaffolding would make a second
   record the vault then refuses).

3. **Questions — hold every answer until the owner says go.** Nothing is recorded
   and nothing is written before that; the dialog's own words promise it. Show every
   question's `text` and every option's `label`, `description` and `preview` **word
   for word**; add "(Recommended)" only to the option at index `recommended` (null:
   none); `multi: true` allows several. Never reword, add or drop an option.
   1. **`rounds`, in order**, one `AskUserQuestion` call each: the single questions
      whose answer shapes the setup (`vault-link`, `import`, `existing-store`,
      `sidecar`, `layout`) and any key the owner asked to revisit (step 0). Hold the
      answers. Two of them are orders, not answers, and are carried out at once:
      `vault-link` *Link it* (link, then record `link`) and `sidecar`'s *Move it to the
      vault* (the vault steps below, then record `move`); run `status` again after
      either — it may list repairs from answers the vault already holds, and they join
      step 4. **`vault-link` *Not now* ends the run**: the vault holds this project's
      record, so until it is linked nothing else can be set up here (the tool gives no
      plan and `record` refuses; a local record would be a second copy). Say so; the
      next run asks again.
   2. **The plan**, when `plan` is not null. Print `plan.text` as it is — it is
      Markdown (bold names, the chosen setting as inline code), so never inside a code
      block. When the plan has a
      line-endings line whose count is above 0, print `python3 <root>/tools/eol.py
      check .`'s list of files first — some may need Windows line endings on purpose
      (`.eml`, `.ics` fixtures). Then show `plan.screen` in ONE `AskUserQuestion` call;
      the plan rides in the first option's preview, so it stays in view while the
      owner chooses (seen in a live mock, 2026-11-12). That box is small — about the
      terminal's height less 26 lines — and cuts the rest with "N lines hidden", so
      the tool keeps the plan to two short lines an item (the owner's first trial,
      2026-11-13: "i also see a \"3 lines hidden\" message"); the copy printed in
      chat is the one a short terminal can always read.
      - `use` → go. Record the held single answers, then each `plan.go` pair, then
        the record answer **last** — the one given in this dialog, which overrides a
        `record` pair in `plan.go`. `plan.todo` (the history scan) is carried out in
        step 4.
      - `modify` → ask `plan.change_rounds`, one call per round; hold the answers; run
        `status . --json --choose KEY=VALUE` once with every held answer (a safety
        check ticked is `yes`, unticked `no`; the record answer too, when it was
        given), and show the new plan the same way. Its first option now reads "Use
        this setup".
      - `explain` → print `python3 <root>/tools/init-status.py explain .` as it is
        — Markdown again (an icon and a bold name for each item, a bullet for each
        choice), never inside a code block and never reflowed into paragraphs — and
        `plan.more` (the link, and the same page's path on this machine), then show
        the plan again.
      - `not-now` → record nothing and write nothing; say "Nothing was set up. Run
        /soul-init again when you are ready." and stop.

      A record answer given beside `modify` or `explain` is kept with `--choose
      record=<value>`, so it is not asked twice.
   3. **Record = vault:** the two vault steps (below) come now, before anything is
      carried out. *Cancel* there returns to the plan with the record line waiting.
   4. **After go:** *Type them* (names) asks for the names, and *Released* (stage)
      continues in `/soul-stage`, both as before.

   With no plan and only `rounds` (a set-up project asked one thing), the answer is
   the go: record it and carry it out. Without the prompt tool (`claude -p`), print
   `plan.text` and each question with its options, and stop — never guess an answer.

4. **Carry out the repairs and answers, in this order**, recording each answer with
   `python3 <root>/tools/init-status.py record . <key> <value>` (`plan.go`'s pairs
   exactly as given; for a question from `rounds`, the option's `value`; the history
   scan is recorded after it runs, as `clean <sha12>`, `findings <sha12>` or
   `triaged <sha12>`, and as `declined` when it was not chosen).
   A `no` is final until `revisit`; `layout` keeps its own list. Mechanics are in the
   next section.
   1. **Line endings first** (a yes, or a repair), while nothing else has touched
      tracked files: `eol.py fix` refuses when tracked files have other edits.
   2. **The files:** `import` (create `CLAUDE.md`; add the line; or rewrite an import
      whose path no longer exists — e.g. a plugin version folder an update removed —
      to `<root>`), `existing-store`, `record` (the scaffold and `.gitignore` lines,
      or the fix a disagreeing record's detail names), `mind`, `hand-hooks` (install
      the missing ones; repair a Soul hook as its detail says), the `names`
      file.
   3. **`stage`**, after the record exists (it ends in a witness entry).
   4. **The vault move**, if that was the answer, so the stage entry and the names
      file move with the record; then `vault.py sync .` (below).
   5. **One commit**, when the record is in git: what this run wrote — the record
      files, `.gitignore`, the `CLAUDE.md` lines, the stage block — named in the
      report (the owner chose git; a record neither committed nor ignored is one
      `git add -A` from an accidental commit).
   6. **The history scan last**, so it covers every commit this run made.

   A repair that changes tracked files the owner did not choose (untracking a
   record) is put to the owner first, in one line, with the detail as the reason.

5. **Check.** Run `status` again. Nothing should be left to repair or ask; if
   something is, say what and why.

6. **Report — short.** "Done." and one line per change (a file written, hooks
   installed, a commit with its hash). Nothing changed: "All set — nothing changed."
   and stop; do not list the checks that passed (the gap-only rule, SOUL-055). Then
   only the notes that ask something of the owner, one line each:
   - after "Use default setup": what was taken by default (the stage left unset, no
     private names, upkeep on, line endings fixed, hooks and the history scan not set
     up — only the ones that applied), and that `/soul-init revisit <key>` changes any;
   - a vault with no remote: `vault.py sync .` printed `NOT PUSHED` — the vault is one
     copy on this disk until it has a private remote;
   - the import is pinned to a plugin version (the version-pin guard);
   - `CLAUDE.md` itself is gitignored: a fresh clone loads no contract — a choice,
     not a gap; let the owner confirm;
   - gitleaks missing: the credential check is not running until it is installed;
   - a public repo with a GitHub remote (no remote: say nothing): whether push
     protection is on —
     `gh api repos/<owner>/<repo> --jq .security_and_analysis.secret_scanning_push_protection.status`;
   - the record moved into the vault: what `vault.py sync .` printed — `NOT PUSHED`
     means committed on this machine but not yet on the vault's server.

   **The outside-files dialog goes in the bottom line on the run that wrote the
   import or moved the record into the vault** — as its own 🙋 item ("approve the
   outside-files dialog the next session shows; declining turns it off for good"),
   not only in the body. A session once never told the owner about it at all
   (SOUL-218); a required bottom-line item is harder to drop than a bullet. On a
   re-run that wrote neither, leave it out: the dialog has already been shown.

   *Why short:* the owner, on the v3.6.0 live trial (2026-10-26): "is soul-init,
   logs are still pretty verbose and i'm not sure as a user i wound understand what
   most of it means." The `claude -p` note, the Codex opt-in and the Mind layer live in
   `docs/using-the-soul.md`, not in every report.

## How each answer is carried out

**`import`** — the contract import. No `CLAUDE.md`: create it holding only the
import line, `@<root>/operations/CLAUDE.md` (home-relative). An existing `CLAUDE.md`
without it is the owner's file: on *Add it*, put the line at the top and change
nothing else; *Leave it* writes nothing. The wording is plain by default and the
contract carries that default, so nothing else is written (the `fluent` register
was dropped in v3.6.0, SOUL-A030).
**Wiring in `CLAUDE.local.md`** (status names it as the importer): write the Mind
import and the Stage block there too, never into a tracked `CLAUDE.md` — in a repo
going public that would publish them (mining pass 3, SOUL-234). First run `git
check-ignore -q CLAUDE.local.md`: not ignored, it may be tracked and public — say so
and ask before writing there.

**`record`** — where the record lives; `.gitignore` lines to match:
- *git*: ignore only the volatile runtime state, never the record —
  ```
  # Soul System runtime state (cursor, event log) — never the record itself
  .soul/handoff.md
  .soul/events.jsonl
  ```
  then commit the record files and `.gitignore` (the owner chose git; a record that
  is neither committed nor ignored is one `git add -A` from an accidental commit).
- *local*: ignore the whole directory, `.soul/`.
- *vault*: no `.gitignore` lines; the vault move (below) hides the link in
  `.git/info/exclude`, which never leaves this machine.

**Visibility** is read, never asked (v3.13.0). The tool takes GitHub's answer when the
repo has a GitHub remote, or a `public:` line an older run recorded. The question it
replaced wrote nothing and was not understood — the owner asked twice what it did
(SOUL-I092) — so its meaning now sits on the record options: the git option says who
can read the log. In a repo known to be private the tool suggests git; otherwise it
suggests nothing and the record line waits. This reverses "repo visibility before the
tracking question" (mining pass 2, SOUL-202); what that rule guarded — a question that
once argued only for tracking — is kept by the git option's wording.

Why the record question is asked, never assumed: a record outside git exists in one copy, on one
disk, with no history, and does not travel when the repo is cloned or used from a
second machine; two of six adopting projects had their record gitignored, one by
drift, in a plugin that gets submoduled (2026-08-20 retrospective). So the plan never
fills this line in by itself unless the repo is known to be private: with the repo
public, or its visibility unknown, the git option says a tracked record can be read by
whoever can read the repo, nothing is suggested, and the line waits for an answer — the
question once argued only for tracking (MODEL-TEST's note, SOUL-202).

**Tracking is a `.gitignore` edit, never a file move.** A record untracked because
a broad `.soul/` rule swept it up is fixed by narrowing that rule and committing the
record where it sits. A live run once read older wording as requiring a move to the
root and proposed one (2026-08-20); moving a record costs a rewrite of every path
that points at it and buys nothing.

**The scaffold** (a fresh record) — under `.soul/`, so the other commands have a
local target (the record is THIS project's, **never** the Soul System repo's).
Create what is absent; never overwrite. `.soul/ideas.md` — a header `# Ideas —
<this project>`; `.soul/witness.md` — a header naming it this project's Witness log
and its ID code, the folder name in capitals (`# Witness log — <project> · IDs
<CODE>-001, <CODE>-002, …`; format: `operations/witness-log-format.md`), so the
first entry does not have to ask for one (found in the v3.6.0 live trial). **Existing projects keep their
layout**: stores at the root or under `.soul/` ARE the record — leave them where
they are; the gate scopes on either (`hooks/test_scope.py` cases 5 and 7). Skip
`amendments/` and `findings/`: those record changes to the Soul and go upstream;
scaffolding them produced 0 artifacts across 6 projects in 3+ months (2026-08-20).

**`existing-store`** — a store outside root and `.soul/` (e.g. `docs/ideas.md`). On
*Use it*, write the `.soul/` file as a one-line pointer (`Ideas live in
docs/ideas.md — append there.`) instead of an empty store. MODEL-TEST's
`docs/ideas.md` was missed once and a second store scaffolded (SOUL-202).

**`vault-link`** and the vault steps. A vault is one private git repo that can hold
many projects' records, each reached by a `.soul` link (SOUL-I079, [ADR
0001](../../docs/adr/0001-soul-vault.md)). **The project's link is the record of which
vault it uses; the machine file names only the default vault offered next time.** The
owner, 2026-11-13: "we ask if they want a vault and which. they specify or take the
default. that's it right? it is then recorded in the links where the vault is for that
project. soul-system doesn't need to know about any others?" There are no labels and
nothing is refused: three of the four old labels changed nothing, and whose material
may go where is the owner's judgment, not the tool's (SOUL-I092 round 2). Re-link
(*Link it*, or a BROKEN repair): `python3 <root>/tools/vault.py link . --key <key>`.

The move (*In a private vault*) is two steps, asked before anything is carried out.
The move itself runs late in step 4 — after the stage entry and the names file are
written into the local record, so they move with it:
1. **Which vault** — `plan.followups["vault-which"]`, word for word. *Use {path}* is
   `plan.vault_default.path`; *Somewhere else* asks for the folder. When the chosen
   folder holds no vault yet (no `vault.md`), make one: `python3 <root>/tools/vault.py
   init <folder>`, adding `--register` when this machine names no default vault
   (`plan.vault_default.registered` is false). Relay each line it prints. If it says
   the folder was not made a git repo (it sits inside another repo, or git is
   missing), that vault cannot be synced: say so and ask this question again.
2. **Confirm** — run `vault.py link . --key <the repo's name> --vault <folder>
   --dry-run`, show its lines, then ask `plan.followups["vault-confirm"]`, its text
   taken from `template` with `{path}` replaced by the folder and nothing else changed.
   - *Add tags, then move*: ask for the tags (comma-separated), add `--tags`, and show
     the dry run again: it lists the tags as they will be written, in Obsidian's own
     form (spaces become hyphens). A refused tag is relayed word for word and asked
     again.
   - *Also move other private folders*: ask for the paths — plans, reviews, research
     folders (a project going public). Each is passed as `--also <path> …`, relative to
     the project; it lands in the vault's `soul/` at the same path, copied,
     hash-compared and only then removed here, like the record. Paths outside the
     project or inside `.git` are refused (SOUL-I081's narrow case, mining pass 3,
     SOUL-234). Show the dry run again.
   - *Cancel*: nothing moves; back to the plan.

   On *Move it*, step 4 runs the same command without `--dry-run`. The key — the
   repo's name — names the project's folder in the vault, so it survives the project
   moving; the dry run shows it. No label, key or remote is asked.

The move, when it runs: it moves a
root-layout record into `.soul/` first and repoints a `@mind.md` import; copies
`.soul/` into `<vault>/projects/<key>/soul/` and compares every hash; replaces
`.soul/` with a link and compares again. On WSL with the project on a Windows drive
the link is a Windows junction (Windows tools cannot follow a WSL symlink), so the
vault must be on a Windows drive too. It adds `.soul` to `.git/info/exclude` and the
vault to `.claude/settings.local.json` `permissions.additionalDirectories` (without
it Claude Code refuses writes through the link), then rewrites the vault's
`index.md`. All from the I079 link test (2026-10-22). **STILL TRACKED** printed:
recommend `git rm --cached` of those files and a commit, now — until then a reset,
stash or checkout puts the old copy back in place of the link and `check` reports
TWO COPIES; the old copies stay in history (moving is not redaction, mind 6d).
The vault repo keeps the project's `private-names.txt` (it travels to the next machine
with the record) and leaves out only `events.jsonl`. Any other `link` failure: run
`vault.py check .` and report its line before going on. After a move, run
`eol.py check <vault>`: a vault made before v3.5.0 may lack the line-ending rule —
if line endings were a yes, fix and commit there too.
**Commit the vault with `vault.py sync .`**, never raw git: it commits only
`projects/<key>/`, under a lock in the vault's `.git/`, and pushes only when the
vault's server has not moved. It touches nothing else in the shared vault folder, where
other sessions keep uncommitted edits; two sessions once ran git there in the same
second (mining pass 3, SOUL-234). It does not commit `index.md`, which each machine
regenerates. Exit 2 with `NOT PUSHED`: the commit is safe here, but not on the server —
its line says why (no upstream, a refused push, or the server has newer commits).
Merging those is a deliberate step, the owner's or this session's when no other
session is writing in the vault (the command its line names — not a bare `git pull`,
which fails on diverged branches), then sync again; tell the
owner. Exit 4: the lock is held — a running sync, so try again later; or it "looks
stale", and its line names the file to remove once the owner has checked no git runs
in the vault.
**`link` refuses** (exit 2): the record stayed where it was — every check runs before
anything changes, and a failed compare rolls the move back. Return to the plan with
the record line waiting again; a record must never be left neither tracked nor ignored,
where one `git add -A` commits it. **Exit 5:** the record moved and is linked, but an
`--also` path did not; its lines name each one and why, and it is back where it was —
report them, and do not ask the record question again.

**`sidecar`** — asked only when the record files are committed at the project root
and a `.soul/` beside them holding `handoff.md` or `private-names.txt` exists only on
this disk, with this machine's vault present and holding nothing for the project.
No option is recommended: whether it moves is the owner's call. *Move it to
the vault* moves `.soul/` alone; the root record stays tracked (SOUL-223, [ADR
0001](../../docs/adr/0001-soul-vault.md)). Run the two vault steps exactly as for the
vault move, adding `--sidecar` to both `link` calls (the dry run, then the real one
on *Move it*). Record `move` only after the link succeeds (like `vault-link`). *Keep
it here* is recorded `keep` and is final until `/soul-init revisit sidecar`.

**`names`** — *Type them*: write the names, one per line (`Name => TOKEN` suggests
a replacement), to `.soul/private-names.txt`; it is gitignored with the rest of
`.soul/` or by its own line — add one if the record is tracked. Names that cut
across projects belong in `~/.claude/soul-private-names.txt`; say so. The secret
guard (`operations/secret-guard.md`, SOUL-I070, **experimental**) already checks
the AI's commits in Claude Code: credentials block, private names warn.

**`hand-hooks`** — commits and pushes made outside an AI session run only the
repo's own hooks. Install `pre-commit`, `commit-msg` and `pre-push` in the directory
printed by `python3 <root>/hooks/secret-guard.py --own-hooks-dir` (it follows
worktrees, submodules and `core.hooksPath`; do NOT use `git rev-parse --git-path
hooks`, which inside a session answers the plugin's own wrapper directory). Never
overwrite an existing hook — it belongs to the owner or another tool (git-lfs,
carried by five adopting projects, installs `pre-push`); say which was skipped and
that hand commits or pushes are not checked at that step. The exception is a hook
carrying the Soul marker line below: it is Soul's own. Repair it as the status detail
says — a hook of only the template's lines is rewritten whole with the current
`<root>`; a hook merged by hand with other lines (e.g. `git lfs pre-push`) gets only
its `guard=` line rewritten, and the other lines are kept and named in one line. A
whole rewrite there would drop the merged LFS upload (mining pass 3, SOUL-234).
Otherwise write it executable, every `<hook>` replaced. It fails open, loudly, when
the plugin path is gone, and stays quiet when a session's wrapper already ran the
check. Under Windows git (Git for Windows' shell, `uname -s` MINGW, MSYS or CYGWIN)
it cannot reach the WSL guard at all, so it says that git is NOT checked and does not
suggest `/soul-init`, which cannot repair it (MODEL-LIB, 2026-11-10). A `pre-push` reads git's input once and, after the guard, runs `git lfs
pre-push` when git-lfs is installed and `.gitattributes` names `filter=lfs`: LFS
cannot install its own hook while this one holds the slot:
```sh
#!/bin/sh
# Soul System secret check (<hook>), installed by /soul-init (operations/secret-guard.md).
guard="<root>/hooks/secret-guard.py"
in=
[ "<hook>" = pre-push ] && in=$(cat; echo .) && in=${in%.}
if [ ! -f "$guard" ] || ! command -v python3 >/dev/null 2>&1; then
  case $(uname -s 2>/dev/null) in
  MINGW*|MSYS*|CYGWIN*) echo "Windows git cannot run the WSL guard — this git <hook> is NOT checked" >&2 ;;
  *) echo "Soul secret check NOT running — plugin path missing; re-run /soul-init to repair the hook" >&2 ;;
  esac
else
  printf '%s' "$in" | python3 "$guard" --hand-hook <hook> "$@"
  rc=$?
  [ "$rc" -eq 3 ] && exit 1
  [ "$rc" -ne 0 ] && echo "Soul secret guard failed (exit $rc) — this git <hook> was NOT checked" >&2
fi
if [ "<hook>" = pre-push ] && command -v git-lfs >/dev/null 2>&1; then
  case $(cat .gitattributes 2>/dev/null) in
  *filter=lfs*) printf '%s' "$in" | git lfs pre-push "$@" || exit $? ;;
  esac
fi
exit 0
```

**`history-scan`** — `gitleaks git --redact --no-banner`, results to the owner,
then record `clean <sha12>` or `findings <sha12>` (HEAD's first 12 characters).
Record `triaged <sha12>` only after each hit was read and none is a real secret
(status shows "hits checked, none real"); a false match left as `findings` was later
read to the owner as possible leaked secrets (mining pass 3, SOUL-234). It is
offered once; `/soul-init revisit history-scan` runs it again. The secret guard checks
each new commit as it is made, so the one scan covers what came before the guard
(the owner chose this over re-offering after every commit, 2026-10-26, v3.6.1). Rewrite nothing: a found credential is
rotated first, and any rewrite is the owner's separate call (on a native Linux
filesystem, not a `/mnt` drive; a rewritten-away commit stays fetchable by SHA on
GitHub).

**`stage`** — *Prototype* or *Pre-release*: write that preset's block with its
defaults and its witness entry, with no further questions, as
`<root>/skills/soul-stage/SKILL.md` describes for a stage handed over by
`/soul-init`; say in one line that `/soul-stage <stage>` refines it. *Released*
continues in that skill as if it had been the argument (its screen, block and
witness entry): what outsiders rely on has no default. The block lands under the
import. The live trial asked three follow-up questions here (the next-stage
trigger, additions, a confirm) on a fresh project (2026-10-26). *Not now* writes nothing but the answer: no stage line means
released-grade caution, the contract's default. Carried out after the record
exists, because a chosen stage ends in a witness entry (the 2.2.0–2.2.2 order had it
before the scaffold; found by fresh-context review, 2026-08-26). If the tool's
detail says a hand-written `**Phase:` block exists, show it before asking. *Why ask at all:* two adopting
projects had the owner write "no backwards compatibility — this is beta" by hand on
consecutive days (2026-08-24/25), into two files, in two wordings.

**`upkeep`** — nothing to carry out but the answer (`on` or `off`). *On*, which is
also what a project that was never asked gets: the session refreshes the handoff
cursor by itself when it goes stale — about 100,000 tokens of conversation, or a
summary, since it was last written (`hooks/upkeep.py` notices) — and `/soul-distill`
runs by itself at its growth signal, applying small Mind changes and holding big ones
for the owner. Each tells the owner in one line, and a no undoes it. *Off*: neither
runs by itself; `/soul-next` reminds instead. To change it later: `/soul-init revisit
upkeep`. *Why ask once:* the owner accepts the cursor and the Mind "as created" and
wanted the stop gone, with a way out (SOUL-A032).

**`layout`** (projects already set up) — `python3 <root>/tools/layout-cleanup.py
scan <project>` flags only text files whose name or folder marks them as working
material (plans, handoffs, reviews, scratch, stray `.soul/` files), never code,
tests, user docs or ADRs. On *Review*, show its grouped dry run and ask per group:
*move to `.ai/`* / *leave* / *it is project content*. Write the answers to a plan
file outside the project (`{"<path>": "move|leave|content"}`, paths from `scan
--json`), run `apply <project> --plan <file> --dry-run`, then `apply`. `apply` adds
`.ai/` to `.git/info/exclude` when git does not ignore it and says so — relay that line;
a moved working file left unignored is one `git add -A` from a commit, in a public repo
from publication (mining pass 3, SOUL-234). A file that
project content links to is usually project content — put it to the owner on its own
first, since project content must never link into `.ai/`. Any "project content now
links into .ai/" line `apply` still prints is an open gap — report it: drop the link
or promote the file, the owner's call. Its "still names the old path: <file>:<line>"
lines are plain-text mentions (a backticked path, a code comment) that `apply` never
rewrites: relay them; hits in `witness.md` are history, expected and left alone.
*Leave them* runs `decline <project>`, which remembers the list in `.soul/layout.json`.

**`line-endings`** — the problem: a Windows git or Sourcetree with
`core.autocrlf=true` checks files out with Windows line endings; WSL git sees every
one as modified, `git add -A` commits them, and tools that write Unix endings leave
files with both. The fix is part of the default setup whenever the repo lacks the
rule file, and the plan's line says how many files it would change. When that number
is above 0, show `eol.py check .`'s list of files committed with CRLF before the plan
(step 3) — some may need CRLF on purpose (`.eml`, `.ics` fixtures), and the fix stores
them LF. When it is in the setup (`line-endings yes`), run `python3 <root>/tools/eol.py fix <repo>` for each repo the
tool's detail names (`Needs it: project`, `vault` or `both`), show its output and
commit in that repo with the line it suggests (in the vault, commit its `index.md`
change first — `vault.py sync` never commits it; these commits are plain git, outside
sync's lock, so make them while no other session is writing in the vault). With no vault the detail has no `Needs it:` line: fix the project. It refuses (exit 2, nothing changed) on staged work,
real edits it would sweep in, an untracked or edited `.gitattributes`, or files
hidden by assume-unchanged or skip-worktree: say why and leave it. Stopped partway
(exit 2 after changing something): relay its list and undo lines word for word.
Exit 1: the re-check is still not ok — show it, do not commit; the owner fixes what
it names or undoes with `git restore --staged .`.
*Why:* the owner (2026-10-26): "i have seen this on every soul project we have
worked on (and non soul). the ai typically identifies it eventually that it is just
eol issues after it checks and then fixes it. so i am trying to preempt it."
(SOUL-219: about 114 vault files and 2 project files rewritten by hand.)

**`mind`** (repair) — a `mind.md` that nothing imports does nothing (one adopting
project carried a 164-line Mind no file imported). Add the import directly after the
contract import, **relative to the file the line goes into**: from a root
`CLAUDE.md` or `CLAUDE.local.md`, `@.soul/mind.md` or `@mind.md`; from `.claude/CLAUDE.md`,
`@../.soul/mind.md` or `@../mind.md`. A fixed `@.soul/mind.md` once pointed at
`.claude/.soul/mind.md` and MODEL-TEST's Mind went unloaded (SOUL-202).

## What not to do

- Do not ask a setup decision the tool did not list, reword one, or answer one for
  the owner. The follow-ups this skill names are not new decisions: the vault's
  folder, tags and private paths, the names themselves, the layout groups, and putting
  a tracked-file repair to the owner. Do not record or write anything before the owner
  chooses to go (step 3). Do not re-ask a recorded answer — `revisit` is the owner's way back.
- Do not copy Soul doctrine (the contract, the philosophy) into the project; it is
  referenced by import so it stays current. The empty record scaffold is not a copy.
- Beyond the import line and the record, write project content only where an answer
  says to: step `layout`'s moves, `line-endings`' commit, `existing-store`'s pointer.
- Do not classify layout files yourself: move only what the scan flagged and the
  owner chose, and never delete one.
- Do not modify the Soul System repo from this command.

---

**Source:** Built by the Artificer as the Soul System's bootstrap command (the
`@import` installer). Brought into the repo under [[SOUL-F029]]; the root derives
from the skill's own location since SOUL-A022. **Adopted:** 2026-05-19
(repo-canonical 2026-05-22). **Status:** active.
**Amended:** 2026-10-19 (mining pass 2, SOUL-202) — repo visibility before the
tracking question; an existing store outside root/`.soul/`; the Mind import relative
to the importing file (F068).
**Amended:** 2026-10-20 (v2.10.0, SOUL-I070) — the experimental secret guard:
private names, optional hand-commit hooks (own hooks directory, never overwriting,
failing open loudly), the history sweep, push-protection status.
**Amended:** 2026-10-22 (v3.4.0, SOUL-I079) — the vault: check, re-link, the third
record answer, the move.
**Amended:** 2026-10-26 (v3.5.0, SOUL-218/219) — line endings (`tools/eol.py`); the
outside-files dialog in the bottom line.
**Amended:** 2026-10-26 (v3.6.0, SOUL-I082, SOUL-A030) — rebuilt as status →
questions → carrying out over `tools/init-status.py`: fixed wording, answers remembered
in `.soul/init.md`, a `no` final until `revisit`; the register question dropped.
**Amended:** 2026-11-06 (v3.11.0, mining pass 3, SOUL-234) — `vault.py sync` and
`link --also`; wiring in `CLAUDE.local.md`; `triaged` history scans; the hand pre-push
chains to Git LFS and a merged hook keeps its other lines; `.ai/` ignored by `layout`.
**Amended:** 2026-11-12 (v3.12.0, SOUL-A032) — the `upkeep` answer: on unless the
owner says off, asked once.
**Amended:** 2026-11-13 (v3.13.0, SOUL-I092) — a plan first: one dialog with the whole
setup (use, modify, explain, not now), answers held until go; the public question
dropped; the vault as two steps with no labels, a new vault made here, tags in
Obsidian's form (SOUL-I090 weighed one written round and did not take it).
