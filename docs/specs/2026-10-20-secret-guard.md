# Secret guard — credentials and private names checked when the AI commits (v1)

**Status:** approved design, 2026-10-20 — the Body's grilling session (SOUL-I070
records the approval; the Body chose to build before the machine move). Ships as
**experimental** (the Body's decision after the third review, 2026-10-20).
**Scope:** one hook script shared by Claude Code and Codex, two plain-text name
lists, additions to `/soul-init`, one operations doc. No contract line.

## Why

Leaks in this system's own history came through text the AI wrote, not code: real
project names in record entries and in a commit SUBJECT (SOUL-169, SOUL-175,
SOUL-178), and a work email in commit author metadata (SOUL-151). The by-hand
pre-push name scan (mind item 6c) missed twice (SOUL-178; SOUL-185 nearly passed
nine names). No registered project runs a secret scanner, and the plugin's only
Claude hook fires at Stop, after the commit. Secret scanning is a solved problem
(gitleaks, GitHub push protection), so the Soul System wires one in and owns only
what those miss: AI-written commit text and the owner's private-name lists.

SOUL-175 recorded the Body declining a mechanical forbidden-strings guard in favour
of review. That ruling stands for names: names WARN, they never block. Credentials
block.

## What it checks, and when

~~The check runs when the AI is about to run `git commit` or `git push` (Claude Code
`PreToolUse` on Bash; the Codex adapter's existing `PreToolUse` Bash hook), in
Soul-governed projects only (the gate's `_is_soul_project`).~~ — superseded: see
"Mechanism changed (2026-10-20)" below. git now runs the check from its own hooks.

| What | Source | Repos | On a hit |
|---|---|---|---|
| Credentials in staged changes (commit) or in commits not yet on the remote (push) | `gitleaks git` | all Soul repos | **block** |
| Credentials in the commit message (commit), and in outgoing commits' and annotated tags' messages (push) — added after the fourth review | `gitleaks stdin` | all Soul repos | **block** |
| A ref that names a blob or tree (a tag to one, a raw object id): content NOT scanned — after the ninth review, by the Body's decision | — | all Soul repos | NOT checked line |
| Private names in staged changes, the commit message, or outgoing commits' diffs and messages | the name lists | public Soul repos only | warn |
| Commit author email on a name list | `git var` identities / outgoing commits' author and committer | public Soul repos only | warn |
| A name-list file staged for commit | path match | all Soul repos | warn |

"Public" = `gh repo view --json visibility` says PUBLIC, cached per repo for the
session; if `gh` is unavailable or fails, treat the repo as possibly public and run
the name checks (fail toward checking).

## Mechanism changed (2026-10-20)

The first build ran the check from `PreToolUse` by parsing the AI's Bash command to
predict what git would commit or push. Two fresh-context reviews broke that prediction
repeatedly — `cd` inside `( )` or `$( )`, `GIT_DIR` / `--git-dir` / `pushd`, a trailing
`#` comment, backslash-newline, a quoted `<<EOF`, git aliases, `gh repo create --push`,
and a time-out that dropped a credential already found. The Body approved replacing
prediction with git itself running the check:

- At session start the plugin writes a stable, read-only folder of git hook wrappers
  (the standard hook names, so repos' own hooks — git-lfs — still run by chaining) and
  points `core.hooksPath` at it for every git the session runs, through git's
  environment config (`GIT_CONFIG_COUNT` / `_KEY_n` / `_VALUE_n`). Claude Code: via
  `$CLAUDE_ENV_FILE` from a `SessionStart` hook, which then verifies the result.
- `pre-commit` (and `pre-applypatch`, for `git am`) scans the staged changes,
  `commit-msg` the message, `pre-push` the commits git says it is sending. A credential
  stops git before the repo's own hook runs.
- Third review (2026-10-20), the Body's decisions: **Codex is an opt-in** — a
  `PreToolUse` command rewrite was built and dropped, because Codex's exec policy then
  judges the rewritten script as one command (the owner's own prefix rules stop
  matching) and a POSIX prefix breaks every command on Windows; the owner sets the three
  variables in Codex's `shell_environment_policy.set` instead. **No
  `reference-transaction` / `post-index-change` wrappers** — a wrapper per call nearly
  tripled a rebase and a tag fetch on /mnt/d — so a repo's own hooks of those names do not
  run inside AI sessions. **Experimental** status.
- The command parser, the pending-index replay, the after-command check and the
  `PostToolUse` entries are gone. What stays from command text is a warn-only notice for
  hook bypasses (`--no-verify`, `core.hooksPath` or `GIT_CONFIG_*` on the command line).
- Also changed in the rebuild: name matching is whole-word for **every** entry (one
  NAME-MAP identifier sits inside a common English word in this repo's tracked files);
  `#` starts a comment only at the start of a line; a missing gitleaks is said on every
  hook run, with one event per repo per session; no NAME-MAP name is ever printed (a word
  containing one becomes its REF token).
- `/soul-init`'s optional hand-commit hook becomes three (`pre-commit`, `commit-msg`,
  `pre-push`), placed in the repo's own hooks folder, never overwriting an existing one.

- Fourth review (2026-10-20), the Body's decisions: **credentials in messages are
  scanned** (commit message at `commit-msg`; outgoing commit and annotated tag messages at
  `pre-push`, following tags that point at tags), and **a first push to a new remote keeps
  the block** on old history, with a message that says so. Current rule (sixth and
  seventh reviews): a remote's tracking refs are used only for a remote with exactly one
  url and no pushurl other than it (by name), or when a push by URL equals a remote's
  first url as `git remote get-url` reports it; anything else is a first push.
- `PreToolUse` on Bash (both hosts) re-checks the wrapper folder before every command —
  reinstalling it, with a one-line notice, when missing or modified — and gives two
  warn-only notices: hook bypasses, and hook installers run inside a session.

Built beyond this design (each in `operations/secret-guard.md`): `!` allowed-phrase lines
in the name lists; scope through the session's own folder (`SOUL_GUARD_CWD`) and from a
subfolder of a Soul repo; `--own-hooks-dir`; the per-run time budget and its
`SOUL_GUARD_BUDGET` override; notices for a `.gitleaksignore`/`.gitleaks.toml` that differs
from HEAD and for `$GITLEAKS_CONFIG`; one wrapper folder per plugin copy; Codex's
SessionStart reading the Codex config files for the opt-in.

Doctrine and the full coverage list (including what is not covered and what is unknown):
`operations/secret-guard.md`.

## Name lists

- `~/.claude/soul-private-names.txt` — user level (beside `~/.claude/soul-tiers.md`),
  outside every repo. Names that cut across projects: clients, employers, work email.
  Created empty with a header comment the first time the hook runs without it; the
  hook says so in one line.
- `.soul/private-names.txt` — optional, per project, gitignored by `/soul-init`. Not
  `.ai/` (that folder is safe to delete; this list must persist). `/soul-migrate`
  carries it as a gitignored record file.
- In the Soul System repo only: column 2 of `registry/NAME-MAP.md` (backticked
  identifiers), the automated form of mind item 6(c). The file itself is unchanged.

Format: one entry per line; a line starting `#` is a comment (a later `#` belongs to the
entry); blank lines ignored. Match is literal, case-insensitive and whole-word for every
entry (letters and digits make words; anything else separates them). An optional `=>`
column names a replacement (`Acme Corp => CLIENT-A`) that the warning suggests.

## Overrides and failure

- A credential false positive is cleared only by the owner approving an entry in
  `.gitleaksignore` (gitleaks' own fingerprint file, committed, so it is visible in
  review). The AI never adds one on its own (rule 8). The block message says this.
- gitleaks missing: never pass silently. Allow the command, say plainly
  "credential scan NOT running — gitleaks not installed" on every hook run, and append
  `soul.secret_guard.unavailable` to `.soul/events.jsonl` once per repo per session.
- Findings never print a secret's value (gitleaks `--redact`); name warnings print
  the matched list entry and where it occurred, not surrounding lines.

## `/soul-init` additions

- Ask once for private names → write `.soul/private-names.txt` (skip if none), add
  it to `.gitignore`. Firmer wording when the repo is public.
- Offer, not default: install the same check as three git hooks — `pre-commit`,
  `commit-msg`, `pre-push` — for commits and pushes made by hand, in the repo's own hooks
  folder (`secret-guard.py --own-hooks-dir`). Do not overwrite an existing hook (five
  projects carry git-lfs hooks); say so and skip that one. They fail open loudly when the
  plugin path is gone, and skip a second run when a session's wrapper already checked.
- Codex in use: one line pointing at the `shell_environment_policy` opt-in.
- Offer a one-time history sweep (`gitleaks git --redact`), results to the owner;
  nothing is rewritten (history surgery follows mind items 6(b)/(d)).
- Public repo: tell the owner whether repository push protection is on (GitHub turns
  it on by default only for personal public repos created since 2024-03; user-level
  push protection is on by default for pushes to public repos).

## Not in scope

A contract line; content scanning for personal information beyond the lists;
history rewriting; scanning commits made outside AI sessions (the optional git hook
and GitHub push protection cover those).

## Anchors

gitleaks v8.30.1 (`gitleaks git --pre-commit --redact --staged` is the upstream
pre-commit entry, `.pre-commit-hooks.yaml`). GitHub: secret scanning and push
protection free on public repos; on by default for new personal public repos since
2024-03-11 (GitHub changelog); user push protection on by default. Wrong if GitHub
changes those defaults — re-check before relying on them.
