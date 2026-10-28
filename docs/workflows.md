# Working with other models — `/soul-workflow`

`/soul-workflow` lets other models do pieces of work — a smaller Claude, Codex, or a
model running on your own GPU — while the session you are talking to keeps the
judgment. It writes the task down for the other model, has it work in a separate
copy of your repo, checks the result itself, has it reviewed, and brings you one
report. You stop copying prompts between tools by hand.

```
 YOU ──▶ this session (whatever you started: Claude Code, any model)
          │  /soul-workflow build-verify
          ├─ brief ──▶ IMPLEMENTER   own copy of the repo · sees only the brief · sandboxed
          ├─ runs the "done when" check itself, in a locked-down box
          ├─ diff ───▶ REVIEWERS     read-only · fresh Claude, and Codex if installed
          ├─ real defect? → back to the implementer (at most 2 rounds)
          ▼
         one report to you: what changed · what was checked · what is still open
```

## Before you start (once per machine)

- **Linux or WSL:** `sudo apt install bubblewrap socat`. Workers run inside a sandbox
  that needs both; without them `/soul-workflow` refuses to start a worker rather
  than run it unprotected. macOS has its sandbox built in (untested). Native Windows
  is not supported.
- **Codex (optional):** installed and logged in (`codex login`) adds Codex as a
  second reviewer, on your ChatGPT plan rather than your Claude usage.
- **A local model (optional):** Ollama running, with the model pulled
  (`ollama list` shows the exact tag to use).

## Quick start

1. Have a piece of work that a command can prove done — tests pass, a build
   succeeds. ("Fix the off-by-one in pager.py. Done when: `pytest -q tests/test_pager.py`.")
2. Type `/soul-workflow build-verify` and describe it, or point at a plan step.
3. Wait for the report. The session tells you up front which model does what; say
   "use X for this" to change it.

For a second opinion on a change you already made, type `/soul-workflow review`.

## The two built-in workflows

**`build-verify`** — *another model makes the change.*
Use it for work you can describe and check with a command. Not for design questions
or anything only a person can judge by reading — those stay in your session.
What happens: the work is written up as a short brief; the implementer makes the
change in its own copy of the repo; this session re-runs the check itself (a worker
saying "tests pass" never counts); the reviewers read the change and report problems;
each problem is checked against the code before it is believed; real ones go back to
the implementer, at most twice; then you get the report. If the cheapest implementer
fails twice, the next one up the list takes over.
What you get: the change ready to apply, the check results, the reviewers' findings
(accepted or rejected, with why), and what is still open.

**`review`** — *a second and third opinion, no changes.*
On your uncommitted work or on a branch. The reviewers read it, read-only, and report;
this session weighs each finding and tells you which hold up. Fixing is your call.

## Who does what — the roles table

Each role (implementer, reviewer, or any name you choose) is a **harness** (`claude`,
`claude-ollama`, `codex`, `codex-ollama`) plus a **model**. `/soul-workflow roles`
shows the table in use. With no table, the default is:

```
| role        | harness | model   | settings |
|-------------|---------|---------|----------|
| implementer | claude  | sonnet  | rung=1   |
| implementer | claude  | opus    | rung=2   |
| reviewer    | claude  | opus    |          |
| reviewer    | codex   | default |          |   ← only if Codex is installed
```

Change it by writing your own table to `~/.claude/soul-roles.md` (every project) or a
project's `.claude/soul-roles.md` (that project only; it replaces a role's rows from
the global file). Several rows of one role are its **ladder**: tried in `rung` order.
One custom workflow can also have models of its own: see *Different models for one
workflow* below.

Try the local GPU first, then Claude:
```
| implementer | claude-ollama | qwen3.8:27b-q8_0 | rung=1 n=3 timeout=3600 |
| implementer | claude        | sonnet           | rung=2                  |
```
Everything local:
```
| implementer | claude-ollama | qwen3.8:27b-q8_0 | rung=1 |
| reviewer    | claude-ollama | qwen3.8:27b-q8_0 |        |
```
Settings: `rung=` (ladder order), `n=` (best of n: n tries, the check picks the
winner — cheap on your own GPU), `timeout=` (seconds per try; default 1800). Whether
a model is good enough is your call; the records below show how each one does.

## What keeps it safe

- **Workers see only the brief.** Not your conversation, not your project's notes or
  instructions, not your Soul record.
- **Workers are boxed in.** A Claude worker (including one running a local model) can
  change files only in its own copy of the repo, has no network, and cannot read
  `~/.ssh`, `~/.claude`, `~/.codex`, your vault and similar folders. A Codex worker
  uses Codex's own sandbox: it limits where Codex can write, but not what it can read.
- **Checks run boxed in too.** The check runs the worker's code, so it runs in the same
  kind of locked-down box, never with your session's permissions.
- **Nothing is "done" on a worker's word.** This session re-runs every check and
  records what it saw.
- **You decide what is unclear.** Unclear requirements come to you before any work is
  handed out; more than two repair rounds needs your yes.

## Seeing how it's going

`python3 <plugin>/tools/delegation-check.py stats` (or ask the session for the
workflow stats) shows, for each role and model: how many runs, how many produced a
winner, timeouts, minutes; the checks this session re-ran and whether they passed;
and for each reviewer how many findings it raised and how many held up. A model that
rarely wins, or a reviewer whose findings never hold up, is a row to change or drop.

## Make your own workflow

1. `/soul-workflow list` shows what exists.
2. Copy the template, `skills/soul-workflow/templates/quick-fix.md` in the plugin, to
   a project's `.claude/soul-workflows/<name>.md` (or `~/.claude/soul-workflows/` for
   all projects). The file name is the workflow's name: lower-case letters, digits
   and `-`; the built-in names are taken.
3. Edit its `description:` line and its steps. Steps are short sentences that use
   build-verify's building blocks — settle, brief, dispatch a role, check here,
   review, repair, accept, report — and role names from your roles table.
4. Run it: `/soul-workflow <name>`.

Example — a cheap fix with a second opinion and no repair rounds:
```
---
name: quick-fix
description: one try at the lowest rung, the reviewers once, no repair round
---

1. Settle the work and write the brief (build-verify steps 1–2).
2. Dispatch `implementer` at its lowest rung, one attempt.
3. Review the winner with `reviewer`.
4. No repair round: report, with any accepted findings as open items.
```

Whatever a workflow file says, the safety rules above still hold, and anything
outside the building blocks (network, pushing, another project, credentials) waits
for your yes.

## Different models for one workflow

The roles table is shared by every workflow. To give one workflow other models, add
a `## Roles` section to its file, written exactly like the roles table. For each
role, the first place that names it supplies all of that role's rows:

1. the workflow file's `## Roles` section;
2. the project's `.claude/soul-roles.md`;
3. the global `~/.claude/soul-roles.md`;
4. the built-in default.

A role the section does not name keeps its rows from the shared table. A table
inside a ``` fence or an HTML comment is not read, so an example can sit in the file
switched off. `/soul-workflow roles <name>` shows the table a workflow will use and
where each row came from.

Example — three workflows, each with the models it needs:

- **`build-verify`** (built in, no file): the shared table — say Sonnet then Opus
  implementing, a fresh Claude and Codex reviewing.
- **`quick-fix`** (`.claude/soul-workflows/quick-fix.md`): only Codex reviews; the
  implementer comes from the shared table.
  ```
  ## Roles

  | role     | harness | model   | settings |
  |----------|---------|---------|----------|
  | reviewer | codex   | default |          |
  ```
- **`security-check`** (`.claude/soul-workflows/security-check.md`): Opus implements
  and Opus alone reviews.
  ```
  ## Roles

  | role        | harness | model | settings |
  |-------------|---------|-------|----------|
  | implementer | claude  | opus  |          |
  | reviewer    | claude  | opus  |          |
  ```

## When something goes wrong

| You see | It means | Do |
|---|---|---|
| "needs bubblewrap and socat" | the sandbox can't start | `sudo apt install bubblewrap socat` |
| Ollama "model not found" | the tag isn't exact | copy it from `ollama list` |
| a try "timeout" | the work was too big or the model too slow | a smaller brief, or `timeout=` in the roles table |
| no Codex reviewer | Codex isn't on PATH | install and `codex login`, or ignore |
| "has no rung K" / a role is unknown | the roles table lacks that row | add the row (`/soul-workflow roles`) |
| a check that needs the internet fails | checks run with no network | install what it needs first, or check without the network |

## Limits today

The roles, the ladder, the two reviewers and the repair budget are starting defaults,
not proven best; the stats are how to tell. Not yet tried for real: a Codex
implementer, a local model as reviewer, `codex-ollama`, best-of-n above 1, a ladder
escalation, Codex as the host, macOS. Details: the 3.7.0 row of `SYSTEM-VERSION.md` and SOUL-I080 in `ideas.md`.
