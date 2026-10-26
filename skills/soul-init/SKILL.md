---
name: soul-init
description: Bring the current project under the Soul System, or check one that already is — wires a live contract reference into the host's project instructions, keeps the project's record (in git, local, or a Soul vault behind a `.soul` link), repairs what broke on this machine, and asks only the decisions never answered, remembering every answer in `.soul/init.md`.
disable-model-invocation: true
---

# /soul-init — bring a project under the Soul, or check one that is

**Codex:** Read [the host integration](../../operations/codex.md) before
following this workflow. Its Codex procedures replace Claude-specific loading,
instruction-file, tool, and invocation mechanics; the shared workflow follows.

Every run is the same three moves: **status** (what is set), **questions** (only
decisions never answered), then **carrying out** the answers and the repairs (what
broke on this machine, fixed from answers already given). A fresh project gets a few short rounds; a
project already set up usually gets none. `tools/init-status.py` works out the
state and holds the question wording; this skill carries out the answers.

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
   `items` (each with an `action`: none · repair · ask · stop) and `rounds` ARE the
   plan. Do not work the state out yourself, and ask nothing that is not in its list.

2. **Stop items first.** Show each one's `detail` and end the run there: TWO COPIES
   (which record is current is the owner's call — do not scaffold or link until they
   decide); a vault named on this machine but not cloned, or a `.soul` link pointing
   at a missing folder (clone the vault there first — scaffolding would make a second
   record the vault then refuses).

3. **Questions, round by round**, in `rounds` order — one `AskUserQuestion` call per
   round (up to four questions). Show each question's `text`, and each option's
   `label` and `description`, **word for word**; add "(Recommended)" only to the
   option at index `recommended` (null: none); `multi: true` allows several. Never
   reword, add or drop an option (one exception: `vault-link` below). After a
   single-question round (`vault-link`, `import`, `existing-store`, `public`), record
   the answer and run `status` again before the next round — those answers change the
   later questions (a public repo changes the record and names wording). *Link it* is
   carried out at once (link, then record `link`), and the new status may list
   repairs from answers the vault already holds; they join step 4. **`vault-link`
   *Not now* ends the run**: the vault holds this project's record, so until it is
   linked nothing else can be set up here (the tool lists no other round and `record`
   refuses; a local record would be a second copy). Say so; the next run asks again.
   Without the prompt tool (`claude -p`), list the questions and stop — never guess
   an answer.

4. **Carry out the repairs and answers, in this order**, recording each answer with
   `python3 <root>/tools/init-status.py record . <key> <value>` (the option's
   `value`; an extras member ticked is `yes`, unticked `no`; the history scan is
   recorded as `clean <sha12>`, `findings <sha12>` or `declined`). A `no` is final
   until `revisit`; `layout` keeps its own list. Mechanics are in the next section.
   1. **Line endings first** (a yes, or a repair), while nothing else has touched
      tracked files: `eol.py fix` refuses when tracked files have other edits.
   2. **The files:** `import` (create `CLAUDE.md`; add the line; or rewrite an import
      whose path no longer exists — e.g. a plugin version folder an update removed —
      to `<root>`), `existing-store`, `record` (the scaffold and `.gitignore` lines,
      or the fix a disagreeing record's detail names), `mind`, `hand-hooks` (install
      the missing ones; rewrite a Soul hook whose plugin path is gone), the `names`
      file.
   3. **`stage`**, after the record exists (it ends in a witness entry).
   4. **The vault move**, if that was the answer, so the stage entry and the names
      file move with the record.
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
   - the import is pinned to a plugin version (the version-pin guard);
   - `CLAUDE.md` itself is gitignored: a fresh clone loads no contract — a choice,
     not a gap; let the owner confirm;
   - gitleaks missing: the credential check is not running until it is installed;
   - a public repo with a GitHub remote (no remote: say nothing): whether push
     protection is on —
     `gh api repos/<owner>/<repo> --jq .security_and_analysis.secret_scanning_push_protection.status`;
   - the record moved into the vault: commit and push the vault.

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

**`public`** — asked only when `gh` cannot tell (no remote, not GitHub) and the
record or names question needs it; it changes their wording. The old step said
"otherwise ask the Body" (SOUL-202).

Why the record question is asked, never assumed: a record outside git exists in one copy, on one
disk, with no history, and does not travel when the repo is cloned or used from a
second machine; two of six adopting projects had their record gitignored, one by
drift, in a plugin that gets submoduled (2026-08-20 retrospective). In a public
repo the question says a tracked record is public and recommends nothing — the
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

**`vault-link`** and the vault move. A vault is one private git repo holding every
project's record, each reached by a `.soul` link (SOUL-I079, [ADR
0001](../../docs/adr/0001-soul-vault.md)). Re-link (*Link it*, or a BROKEN repair):
`python3 <root>/tools/vault.py link . --key <key> --label <the label in its
project.md>`. The move (*In your Soul vault*) is carried out late in step 4 —
after the stage entry and the names file are written into the local record, so they
move with it — but its questions come first:
- **Label**, asked straight after the vault answer, before anything else is done —
  *public* (anyone may read it), *private* (yours), *confidential* (someone else's
  material, e.g. an employer's or client's — the owner decides whether a personal
  vault may hold it), *restricted* (never in the vault; the tool refuses it). On
  *restricted*, say so and ask the record question again with the vault option left
  out — the one change to a question this skill allows.
- **What it contributes to** — free-form tags, may be empty.
- **Key** — the project's folder in the vault; default the repo's name. The key,
  not the path, names the folder, so it survives the project moving.

Run `vault.py link . --key <key> --label <label> --contributes <tags> --dry-run`,
show its lines, and on the owner's yes run it without `--dry-run`. It moves a
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
**`link` refuses** (exit 2, nothing changed): the record stayed — ask the record
question again without the vault; a record must never be left neither tracked nor
ignored, where one `git add -A` commits it.

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
carrying the Soul marker line below whose plugin path no longer exists: it is
Soul's own, so rewrite it with the current `<root>`. Otherwise write it
executable, `<hook>` replaced in all three places. It fails open, loudly, when the
plugin path is gone, and stays quiet when a session's wrapper already ran the check:
```sh
#!/bin/sh
# Soul System secret check (<hook>), installed by /soul-init (operations/secret-guard.md).
guard="<root>/hooks/secret-guard.py"
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

**`history-scan`** — `gitleaks git --redact --no-banner`, results to the owner,
then record `clean <sha12>` or `findings <sha12>` (HEAD's first 12 characters). It is
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

**`layout`** (projects already set up) — `python3 <root>/tools/layout-cleanup.py
scan <project>` flags only text files whose name or folder marks them as working
material (plans, handoffs, reviews, scratch, stray `.soul/` files), never code,
tests, user docs or ADRs. On *Review*, show its grouped dry run and ask per group:
*move to `.ai/`* / *leave* / *it is project content*. Write the answers to a plan
file outside the project (`{"<path>": "move|leave|content"}`, paths from `scan
--json`), run `apply <project> --plan <file> --dry-run`, then `apply`. A file that
project content links to is usually project content — put it to the owner on its own
first, since project content must never link into `.ai/`. Any "project content now
links into .ai/" line `apply` still prints is an open gap — report it: drop the link
or promote the file, the owner's call. *Leave them* runs `decline <project>`, which
remembers the list in `.soul/layout.json`.

**`line-endings`** — the problem: a Windows git or Sourcetree with
`core.autocrlf=true` checks files out with Windows line endings; WSL git sees every
one as modified, `git add -A` commits them, and tools that write Unix endings leave
files with both. Before asking, show `eol.py check .`'s list of files committed with
CRLF — some may need CRLF on purpose (`.eml`, `.ics` fixtures), and the fix stores
them LF. On yes, run `python3 <root>/tools/eol.py fix <repo>` for each repo the
tool's detail names (`Needs it: project`, `vault` or `both`), show its output and
commit in that repo with the line it suggests (in the vault, commit its `index.md`
change first). With no vault the detail has no `Needs it:` line: fix the project. It refuses (exit 2, nothing changed) on staged work,
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
`CLAUDE.md`, `@.soul/mind.md` or `@mind.md`; from `.claude/CLAUDE.md`,
`@../.soul/mind.md` or `@../mind.md`. A fixed `@.soul/mind.md` once pointed at
`.claude/.soul/mind.md` and MODEL-TEST's Mind went unloaded (SOUL-202).

## What not to do

- Do not ask a setup decision the tool did not list, reword one, or answer one for
  the owner. The follow-ups this skill names are not new decisions: the vault's
  label, tags and key, the layout groups, and putting a tracked-file repair to the
  owner. Do not re-ask a recorded answer — `revisit` is the owner's way back.
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
