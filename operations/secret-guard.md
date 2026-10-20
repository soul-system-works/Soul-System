# The Secret Guard (experimental)

git itself checks every commit and push the AI makes in a Soul project. Credentials
**block**; private names **warn**. Code: `hooks/secret-guard.py`; fence:
`hooks/test_secret_guard.py`; design: `docs/specs/2026-10-20-secret-guard.md` (SOUL-I070).

**Experimental** (the owner's call, 2026-10-20): it changes how git finds its hooks for
the whole session. Expect rough edges, and read "Not covered" before relying on it.

The leaks in this system's own history came through text the AI wrote, not code: real
project names in record entries and in a commit subject (SOUL-169, SOUL-175, SOUL-178),
and a work email in commit author metadata (SOUL-151). The by-hand pre-push name scan
(mind item 6c) missed twice. Secret scanning itself is a solved problem, so the guard
wires in `gitleaks` and owns only what scanners miss: AI-written commit text and the
owner's private-name lists.

**Install gitleaks 8.19.0 or later** — the guard calls the `gitleaks git` subcommand,
added in v8.19.0 (2024-09-14; it replaced `detect`/`protect`). Tested with 8.30.1. Any
of (gitleaks README): a release binary from github.com/gitleaks/gitleaks/releases placed
on `PATH` (for example `~/.local/bin/gitleaks`), `brew install gitleaks`, or a source
build (`make build`). The Docker image does not serve: the hook needs a `gitleaks` on
`PATH`. Without it the credential check does not run and every commit says so.

**Needs git 2.31 or later** (environment config, `GIT_CONFIG_COUNT`, arrived in 2.31;
the wrappers also use `git config --show-scope`, 2.26).

## How it runs

git looks for its hooks in `core.hooksPath` when that is set. The guard sets it, for
every git the session runs, through git's environment config (`GIT_CONFIG_COUNT`,
`GIT_CONFIG_KEY_n`, `GIT_CONFIG_VALUE_n`).

### Claude Code

A `SessionStart` hook (`hooks/hooks.json`), when the session starts in a Soul project or
in a subfolder of a Soul repo:

1. writes the hook wrappers (below) into a read-only folder;
2. appends a few lines of shell to `$CLAUDE_ENV_FILE`, which Claude Code runs before each
   Bash command. The lines add one entry at the next free `GIT_CONFIG_COUNT` index (a
   count already set is respected; leading zeros are stripped; a count that is not a
   number is left alone and that command prints "NOT armed for this command"), add
   nothing when they run again, and arm only while the folder exists. They also export
   `SOUL_GUARD_SESSION` and `SOUL_GUARD_CWD` (the session's folder, used for scope);
3. **checks the result**: it runs the env file in a subshell and asks git for
   `core.hooksPath`. If git is older than 2.31, there is no env file, or git does not
   answer with the folder, it says "Soul secret guard NOT armed — <reason>".

`PreToolUse` on Bash re-checks the folder before every command (a couple of dozen small
reads). If a wrapper was changed or the folder is gone, it reinstalls it and says so in
one line. It also gives two warn-only notices (below).

### Codex — opt-in

Codex has no env file, and a command rewrite is not used (it was built and dropped: Codex
judges a rewritten command as one script, so the owner's own command rules — such as a
forbidden `git push --force` — stop matching, and on Windows a POSIX prefix breaks every
command). To arm the guard under Codex, the owner adds this to `~/.codex/config.toml`,
with the folder Codex's SessionStart context prints (`$PLUGIN_DATA/soul-guard-hooks-<id>`):

```toml
[shell_environment_policy]
set = { GIT_CONFIG_COUNT = "1", GIT_CONFIG_KEY_0 = "core.hooksPath", GIT_CONFIG_VALUE_0 = "<folder>" }
```

Codex's config docs ("Shell environment policy") say `set` is applied after the automatic
`KEY`/`SECRET`/`TOKEN` exclusions and after custom exclusions, so `GIT_CONFIG_KEY_0`
survives; an include-pattern allowlist (`filters` with `"include"`, or `include_only`)
can still remove it — add the three names there if you use one. Same order in the source
(codex-rs `protocol/src/shell_environment.rs`, read 2026-10-20). Wrong if Codex changes
that order. If the shell Codex starts already has `GIT_CONFIG_COUNT` set, this replaces
it. It applies to every Codex session, Soul project or not; outside Soul repos the
wrappers only run the repo's own hooks. Untested inside a live Codex session; the fence
checks that these three variables arm git. Without the opt-in, Codex's SessionStart
context says "NOT armed under Codex" and prints the snippet. Codex's `PreToolUse` gives
the same notices as Claude Code's, and never rewrites, allows or blocks a command.

**The opt-in is unconditional.** git, under Codex, then looks for hooks only in that
folder, in every repo. If the folder is gone (plugin data wiped, or the plugin
uninstalled with the config left behind), git under Codex runs **no hooks at all** —
not the guard, and not any repo's own hooks (git-lfs included). After a plugin update
the folder name changes (it is per plugin copy, below): the old folder keeps working
until the old plugin copy is deleted, then each guarded hook says "plugin path missing";
SessionStart says "NOT armed under Codex" with the new folder to put in the config.
**To undo the opt-in**, remove the three entries (`GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_0`,
`GIT_CONFIG_VALUE_0`) from `set` in `~/.codex/config.toml` — do this before uninstalling
the plugin.

### The wrappers

One folder per plugin copy: `$CLAUDE_PLUGIN_DATA/soul-guard-hooks-<id>`, where `<id>` is
a short hash of the plugin copy's own folder (Codex: `$PLUGIN_DATA/…`; neither set:
`~/.claude/…`), with a `plugin-root` file naming that copy. Per copy because two copies —
a plugin update while another session stays open — sharing one folder rewrote each
other's pointer on every command (fourth review); separate folders cannot. **Read-only** after install, so a hook installer run inside a session
fails loudly instead of overwriting a wrapper. Each wrapper is marked as the plugin's
(line 2); install replaces or removes only marked files.

Once `core.hooksPath` is set git runs hooks only from there, so each standard hook name
that git runs on this side of a commit or push has a wrapper — five adopting projects
carry git-lfs `pre-push` and `post-*` hooks. Each wrapper:

1. For `pre-commit`, `pre-applypatch`, `commit-msg` and `pre-push` only: runs
   `secret-guard.py --git-hook <name>`. A credential stops git (exit 1) **before** the
   repo's own hook runs. If the plugin folder or `python3` is gone it prints "Soul secret
   check NOT running — plugin path missing; re-run /soul-init or restart the session" and
   carries on.
2. Then **always** runs the repo's own hook with the same arguments and input (`pre-push`
   gets git's ref lines on stdin), and git sees that hook's exit status. "The repo's own
   hook" is the last `core.hooksPath` set in the repo, global or system config — not the
   one the guard set — or else `<git-common-dir>/hooks`. A marked wrapper found there is
   never run (a copied wrapper would call itself).

**No wrapper, on purpose** — so a repo's own hook of these names does **not run inside AI
sessions**:

- `reference-transaction` and `post-index-change`: they fire on every ref and index
  update. With a wrapper per call, on /mnt/d a 30-commit rebase went from 11.6 s to
  30.4 s and fetching 200 tags from 4.9 s to 16.3 s (third review's measurement).
- `push-to-checkout`: its existence replaces git's own `updateInstead` worktree update.
  It costs nothing to omit: on a push to a local repository git clears
  `GIT_CONFIG_COUNT` before the receiving side runs (checked on git 2.43), so the
  receiving repo never uses this folder.

**Hook installers inside a session.** `git lfs install|update|track`, `pre-commit
install`, `lefthook install`, `husky`, or `git config … core.hooksPath` get the notice
"run hook installers outside an AI session — inside it, git's hooks path points at the
Soul guard". An installer that writes into git's hooks path hits the read-only folder and
fails; `pre-commit install` refuses on its own when `core.hooksPath` is set. Run them in
a terminal outside the session.

**Cost**, measured on /mnt/d (WSL drvfs, where the adopting projects live; 2026-10-20,
gitleaks 8.30.1, gh answering instantly; commit rows are the median of 7 runs, rebase and
fetch single runs; "session" = the env file sourced):

| Operation | Repo | Without | Session |
|---|---|---|---|
| add + commit one file | Soul repo | 0.36 s | 1.72 s |
| add + commit one file | non-Soul repo | 0.35 s | 0.92 s |
| rebase 30 commits | Soul repo | 12.05 s | 16.38 s |
| fetch 200 tags | Soul repo | 5.46 s | 5.86 s |
| git status | either | 0.11–0.12 s | 0.12 s |

A non-Soul commit still pays for Python starting twice (pre-commit, commit-msg) to check
scope. **Every Bash command** also pays for the `PreToolUse` hook, wherever the plugin is
installed (it starts Python, checks scope and, in Soul projects, the wrapper folder): the
fourth review measured 0.19–0.20 s per command on /mnt/d and 0.155 s on ext4, once, on
this machine.

### What this covers

Anything that ends in git running a hook in the session's environment: any shell form
(subshells, `cd` inside `$( )`, `pushd`, comments, line continuations, heredoc messages),
git aliases, `GIT_DIR`/`GIT_WORK_TREE`, files made by the same command, `commit -a` and
pathspecs (git hands the hook the index it will commit), `git am`, scripts and tools that
call git (`bash release.sh`; `gh repo create --push` should be covered too, because it
runs `git push`, but no test has run it). The fence drives real git through each of the
forms that broke the earlier command-parsing build.

**Scope:** a repository is checked when its top folder is a Soul project (the completion
gate's scope test), or when the session's own folder lies inside it and is one.
Elsewhere the wrappers only run the repo's own hooks.

## What it checks

| Hook | What | Source | Repos | On a hit |
|---|---|---|---|---|
| pre-commit, pre-applypatch | Credentials in the staged changes | `gitleaks git --pre-commit --staged` | all Soul | **block** |
| pre-commit, pre-applypatch | Private names in added lines and staged paths (new empty files and renames too; deletions skipped); author/committer email | the name lists | public only | warn |
| pre-commit, pre-applypatch | A name-list file staged (not when it is being deleted) | path match | all Soul | warn |
| commit-msg | Credentials in the message (the text git will keep) | `gitleaks stdin` | all Soul | **block** |
| commit-msg | Private names in the message — `#` lines too when git keeps them (`-m`/`-F` without an editor, or `commit.cleanup` whitespace/verbatim/scissors) | the name lists | public only | warn |
| pre-push | Credentials in the commits being sent: their changes | `gitleaks git --log-opts=…` | all Soul | **block** |
| pre-push | Credentials in those commits' messages and in the messages of annotated tags being pushed | `gitleaks stdin` | all Soul | **block** |
| pre-push | Private names in those commits' diffs, paths and messages; author/committer emails | the name lists | public only | warn |

**What other commit commands get checked** (git 2.43, checked by hand 2026-10-20):

- **Merge:** git runs `commit-msg`, so the merge commit's **message** is checked when it
  is made; its contents are checked at push. `pre-merge-commit` is deliberately not
  guarded: a merge (a `git pull`) brings in commits that may already be public, and
  blocking it for a remote's existing credential would break ordinary git.
- **Cherry-pick, revert, rebase:** git runs no commit hooks for them — also with
  `cherry-pick -e` and `revert -e` — so contents and messages are checked at push. The
  exception: a `rebase -i` *reword* runs `pre-commit` and `commit-msg`. (Sixth review,
  git 2.43.) Messages are checked at push either way.
- **`git am`:** the contents are checked at `pre-applypatch`; the commit messages only at
  push (git runs `applypatch-msg` there, not `commit-msg`, and the guard does not use it).

**Which commits a push sends:** for each ref line git gives the hook, the local commit
minus the remote's old tip (when this repo has it — one `git cat-file --batch-check` for
all lines); for a new branch, or an old tip this repo lacks, minus everything already on
that remote's tracking branches — but only when they describe the push target. They come
from the remote's **first** `url` (git fetches from it), while a push goes to every
`pushurl` or, with none, to every `url`. So, by name, a remote counts only with exactly one
`url` and no `pushurl` other than it; by URL, only when the URL equals a remote's first
`url` as `git remote get-url` reports it. Everything else is a **first push** (below).
Erring toward checking, as the owner decided for first pushes.
Deletions send nothing. The ranges are combined into one scan; excluding commits already
on the target remote removes nothing that is being sent. No path ever goes into the
scan's range options, so a space in a URL cannot break it. Annotated tags are followed
through tags that point at tags (up to 10 deep; deeper, or an unreadable tag object,
says NOT checked), and every tag message on the way is scanned. A ref that names a
**blob or tree** — an annotated or lightweight tag to one, the end of a tag chain, or a
raw object id pushed to a ref — is **not scanned**; the push says so in one line:
"NOT checked — <ref> points at a <blob|tree>; only commits and tag messages are scanned
on push. Do not push it until its content has been checked." (A raw id is labelled
`object <id> -> <ref>`; control characters in a name are shown as escapes.) The messages
of the annotated tags on the way are still scanned and block on a credential.
**Visibility** is judged for the URL git actually pushes to.

**First push to a new remote** — a backup mirror, `gh repo create --push`, a remote with
no tracking branches yet, a remote whose `pushurl` points elsewhere (or has two), a
remote with several `url` lines (the extra ones are push-only mirrors), or a URL that is
no remote's first `url`: nothing is known to be there, so **all history is checked** — even commits already on another remote such as a private origin — and an old
credential —
even one rotated long ago — blocks the push. That is the owner's choice (2026-10-20): the
block message says it was a first push, and the owner clears a rotated credential by
approving its fingerprint in `.gitleaksignore`.

**Public** means `gh repo view <owner/repo> --json visibility` says PUBLIC for the
remote's GitHub URL. Cached per repo and URL for the session, in a per-user folder under
the temp directory that must be owned by you and closed to others (otherwise there is no
cache and `gh` is asked each time). No `gh`, a non-GitHub URL, any `gh` error, or `gh`
not answering within 5 s counts as possibly public, so the name checks run.

**Time:** about 60 s per hook run (`SOUL_GUARD_BUDGET` overrides). A slow child is killed
with its whole process group, also on Ctrl-C or SIGTERM. On time-out the guard keeps
what it already found — a credential already found still blocks — and says what was not
fully checked.

## The name lists

- `~/.claude/soul-private-names.txt` — user level, outside every repo: clients,
  employers, work email. Created with a header comment the first time the guard runs
  without it, and the guard says so in one line.
- `.soul/private-names.txt` — optional, per project, gitignored by `/soul-init`.
- In the Soul System repo only (findings/open/, operations/CLAUDE.md and
  SYSTEM-VERSION.md at the root): column 2 of `registry/NAME-MAP.md`, backticked
  identifiers. A linked worktree reads the main worktree's map; a copy without one (a
  clone) says "NAME-MAP names are NOT checked". After a `→`, an identifier shaped like a
  codename (upper case with a hyphen, such as `PLANT-BOP` or `REF-07`) is the
  replacement side and is skipped; any other identifier there still counts as a name.
  Rows holding identifiers that do not parse as `| REF-nn | … |` are counted and
  reported. Hits show the REF id only, and the guard never prints a NAME-MAP name
  anywhere: any printed word containing one (a file path segment, a gitleaks File field,
  the repo folder's name) becomes `[REF-nn]`.

Format: one entry per line. A line starting with `#` is a comment; a `#` later in a line
belongs to the entry, so `C# Guild` stays whole. Blank lines are ignored. Matching is
literal, case-insensitive and **whole-word for every entry**: letters and digits make up
words, and anything else — space, hyphen, dot, slash, underscore — separates them. So
`Acme` matches `docs/acme-notes.md` but not `acmeist`. (Substring matching warned on
ordinary prose: one NAME-MAP identifier sits inside a common English word in this repo's
own tracked files.) An optional `=>` names the replacement the warning suggests. A line
starting `!` is an **allowed phrase**: it is masked (case-insensitively, from every list)
before names are matched, so an intentionally public phrase that contains a listed name —
a published citation, say — does not warn, while a bare use of the name elsewhere still
does:

```
# clients
Example Client Ltd => CLIENT-A
dev@employer.example
!Example Client Ltd v. State (2019)
```

A warning shows the matched entry, where it occurred (file, commit message, author email,
or which outgoing commit) and the suggested replacement — never the surrounding line.
Names never block: SOUL-175 recorded the owner choosing review over a mechanical
forbidden-strings guard, and that ruling stands.

## Overrides

- **A credential false positive is cleared only by the owner** approving its fingerprint
  as a line in `.gitleaksignore` at the repo root (gitleaks' own file, committed, so it
  shows in review). The block message prints each fingerprint. The AI never adds an entry
  on its own, and never bypasses the hook (contract rule 8). Inline `gitleaks:allow`
  comments are ignored, so editing the file being committed cannot clear a finding.
  A credential in a **message** gets a fingerprint of the form
  `message:<rule>:<16 hex>` (a hash of every line of the finding, first to last — it names
  the finding without the value; the same finding gives the same id at commit and at
  push). Rewording the message
  (`git commit --amend`, or a rebase) is usually better than approving it.
- While `.gitleaksignore` or `.gitleaks.toml` on disk differs byte-for-byte from HEAD's
  copy — untracked, ignored, skip-worktree, modified or staged — every check says so: its
  entries already apply but are not in review yet. `$GITLEAKS_CONFIG` or
  `$GITLEAKS_CONFIG_TOML` being set is reported the same way.
- A real credential: remove it from the change, rotate it, and keep it out of history.
  History surgery follows mind items 6(b) and 6(d).

## Failure modes

A credential may get through only visibly. Each of these lets git continue and says so
in one line:

- **gitleaks not installed:** "credential scan NOT running — gitleaks not installed" on
  every commit and push, plus one `soul.secret_guard.unavailable` event in
  `.soul/events.jsonl` per repo per session (per day for commits made outside a session),
  so the record shows it without one line per commit.
- **gitleaks error:** "credential scan … FAILED — NOT checked". gitleaks exits 0 when its
  own git call fails (a bad range, a corrupt index), so the guard reads its error output
  (never printing it) rather than trusting the exit code.
- **A push range it cannot resolve:** "could not resolve the outgoing commits … NOT
  checked".
- **Out of time:** "timed out — this git … was NOT fully checked"; findings so far stand.
- **Plugin folder or python3 gone:** the wrapper's "Soul secret check NOT running" line;
  the repo's own hook still runs.
- **Wrapper folder changed or missing:** reinstalled before the next Bash command, with a
  one-line notice (Claude Code; Codex's PreToolUse does the same).
- **Any guard error:** "skipped — NOT checked" (a credential already found still blocks).
- **The session could not be armed** (git older than 2.31, no `$CLAUDE_ENV_FILE`, git not
  answering with the folder after the env file runs): "Soul secret guard NOT armed —
  <reason>" at session start.

**Bypass notice.** A command that stops git running hooks or removes the setting —
`--no-verify` (git accepts it from `--no-veri`; the notice matches down to `--no-v`),
`git commit -n`, `-c core.hooksPath` on the command line, `GIT_CONFIG_COUNT` /
`GIT_CONFIG_PARAMETERS` / `GIT_CONFIG_KEY_` in the command, `unset GIT_CONFIG…`,
`env -i`, setting or unsetting any `SOUL_GUARD_*` variable (`SOUL_GUARD_BUDGET=0` makes
every check time out) — gets "Soul secret guard: this command bypasses git hooks — NOT checked" from
`PreToolUse` (both hosts). It is a warning on the command text; it cannot block, and it
can fire on a message that merely mentions such a flag.

## Not covered

- Commits and pushes after any of the bypasses above: a bypass is **visible, not
  prevented** (the notice is a warning on the command text; any mention of
  `SOUL_GUARD_` in a command draws it). The wrapper itself ignores a `SOUL_GUARD_ACTIVE`
  value set from outside: it clears it, runs the check, and sets it again — to
  `hook:folder:its own process ID` — only after the check passed. It then execs the
  repo's own hook, so a `/soul-init` hand hook skips a second run only when that ID is
  its guard's direct parent. A forged value made with `exec git` does not match (git
  then has the shell's ID, but git is the hook's parent, not the guard's) — but a forged
  value CAN match if someone guesses the hook's process ID: the sixth review did, in 1–2
  of 5 tries, on a hand commit with no session. The bypass notice is the backstop. The check uses only the parent process ID (no `/proc`); tested on Linux. On
  macOS it should behave the same. Under Git for Windows the shell's `$$` is an MSYS
  process ID that Python may not see, so a hand hook could run the check twice inside
  sessions — slower, not a hole. Both are **reasoned, not run**.
- A re-push of a commit the owner deleted on the remote, while this repo still has a
  stale remote-tracking ref holding it: the push range excludes it as "already on the
  remote". Remedy: `git fetch --prune` before pushing.
- Submodules and nested repositories inside a Soul repo: a commit inside one is checked
  only if that repository is itself in scope.
- A commit made with an editor and `--cleanup=verbatim` on the command line: git keeps
  `#` lines, but the hook cannot see the flag and strips them before the name and
  credential checks (`commit.cleanup=verbatim` in config is seen). The push check reads
  the full message, so a credential there is still caught at push.
- Codex after the opt-in's folder is gone: no hooks at all run (see the Codex section).
- **Blob and tree content pushed under a ref** (a tag to a blob or tree, a raw object id):
  said as NOT checked, never scanned. Pushing one takes deliberate plumbing
  (`git hash-object -w`, then `git tag`). Two scanners were built and dropped (owner's
  call, 2026-10-20): a printed by-hand command kept growing traps — subfolder scope, the
  tree's own attributes, a config carried in the tree, allow comments, path-only rules —
  and an in-process scan missed path-only rules (a `cert.p12` passed), could let one
  finding span two files and name the wrong one, and ran out of time and memory on many
  paths to one blob.
- **Built-up names evade the bypass notice** — it matches command text, so
  `v=SOUL_GUARD; export ${v}_BUDGET=0`, `v=GIT_CONFIG; unset ${v}_COUNT; git commit` or
  `k=core.hooks; git -c ${k}Path=/x commit` draw no notice. Only the budget case stays
  visible in the output ("skipped (GuardTimeout) — this git … was NOT checked", checked
  2026-10-20); the other two committed a key **silently** in the seventh review. For
  public repos, GitHub push protection (below) is the backstop; for private repos there
  is none beyond review.
- Sessions that started before the plugin was installed or updated: restart them.
- Codex, unless the owner opted in (above).
- git run by something other than the Bash tool (an MCP server, an IDE, an editor's git
  panel): they do not get the env file.
- Windows-side `git.exe` started from WSL: Linux environment variables reach Windows
  programs only through `WSLENV`, which the guard does not set.
- Claude Code commands run in PowerShell: per the hooks docs, PowerShell copies only plain
  assignments from the env file and never runs it, so this shell is not applied.
- A repo's own `reference-transaction` and `post-index-change` hooks, inside AI sessions.
- **Unknown:** whether subagents' Bash commands get `$CLAUDE_ENV_FILE` (the hooks docs do
  not say); the opt-in under Codex on Windows (git for Windows would get a hooks path to
  shell scripts — untested).
- Commits made outside an AI session, unless `/soul-init`'s optional hand-commit hooks are
  installed (they run the same checks from the repo's own hooks folder and stay quiet when
  a session's wrapper has already run them).

## The backstop: GitHub push protection

GitHub secret scanning and push protection are free on public repositories. Repository
push protection is on by default for personal public repos created since 2024-03-11, and
user-level push protection is on by default for pushes to public repos (GitHub changelog,
as recorded in the design spec's Anchors). Wrong if GitHub changes those defaults —
re-check before relying on them. Push protection sees only what reaches GitHub and knows
nothing of private names; the guard is the earlier, local layer.
