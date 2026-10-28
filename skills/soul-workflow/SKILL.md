---
name: soul-workflow
description: Run a named workflow across models — `build-verify` (another model implements a step in its own worktree, the recorder runs the check confined, read-only reviewers report findings (by default a fresh Claude, and Codex when it is installed), at most two repair rounds) or `review` (the reviewers alone, on a diff). Roles (harness + model, e.g. Claude, Codex, a local Ollama model) come from a roles table; this session keeps judgment and the record, and never takes a worker's word. Owner-invoked. `/soul-workflow roles` shows or edits the roles table.
disable-model-invocation: true
---

# /soul-workflow — other models do the work, this session keeps the judgment

**Codex:** Read [the host integration](../../operations/codex.md) before
following this workflow. Its Codex procedures replace Claude-specific loading,
instruction-file, tool, and invocation mechanics; the shared workflow follows.

`/soul-workflow build-verify` · `/soul-workflow review` · `/soul-workflow <name>` (a custom workflow) · `/soul-workflow list` · `/soul-workflow roles [<name>]`

## In short — when and how to use it

**Use `build-verify`** when a piece of work can be written down as a brief with a
command that proves it is done (tests pass, a build succeeds). Another model does it
in its own copy of the repo; this session checks the result and has it reviewed.
**Use `review`** for a second and third opinion on a diff — your own, or a branch —
instead of pasting it into another tool by hand.
**Skip both** for one-line edits, design questions, and anything only a reader can
judge: those stay in this session.

What happens, every time:

1. This session says, in one line, which model does what
   (`implementer → claude:sonnet · reviewers → claude:opus + codex:default`), read
   from `dispatch.py roles --workflow <name>`. Say "use X for this" to override any
   of it.
2. Workers start with a written brief and no conversation. They load no Soul record
   or project instructions (they can still read files in their worktree): each runs
   as its own process with those switched off (SOUL-I080 step 1 probe, 2026-10-27),
   and with an allowlisted environment, not this session's.
3. Workers run inside a sandbox. A Claude worker has a full shell, but the operating
   system lets that shell write only in its own worktree, gives it no network, and
   hides credential folders (`~/.ssh`, `~/.claude`, `~/.codex`, the vault …) from
   it; its Write and Edit tools are allowed only inside the worktree. On Linux and
   WSL the sandbox needs `bubblewrap` and `socat`; without them the dispatch tool
   refuses to start a Claude worker or reviewer, and a sandbox that cannot start
   fails the run rather than letting it run unconfined. Codex workers use Codex's
   own `workspace-write` sandbox. The checks that run a worker's code are confined
   too: the dispatch tool's selection check and the recorder's run
   (`delegation-check.py record --confine`) run under bubblewrap — only the folder
   they check writable (its `.git` and `.soul` read-only), no network, the same
   folders hidden. Native Windows is not supported.
4. Nothing is called done on a worker's word. Every check runs confined and is
   recorded by the recorder, which the dispatch tool or this session launches; this
   session reads every patch before applying it, and `accept` re-runs the check on
   this checkout.
5. You get one report: what changed, which checks ran and passed, what each
   reviewer found and what was done about it, and what is still open.

**Inside a workflow run, its roles do the implementing and the reviewing.** Hand
those steps to `dispatch.py`, never to this session's own subagents (the Agent tool),
whatever a CLAUDE.md delegation rule says about implementers or reviewers: the owner
chose this workflow's roles by invoking it, and only dispatched work runs sandboxed,
gets its check re-run and lands in `stats`. Other help — searching the code, reading
a long log, looking something up — may still use subagents as usual. Outside a
workflow run nothing here applies, and the session delegates as it normally would.
(The owner's call, 2026-10-28: two delegation systems side by side, with the
expensive one automatic, was the concern.)

## The roles table

`python3 <root>/tools/dispatch.py roles` prints the table this session will use and
where each row came from (`<root>` is two levels above this skill's directory).
Rows in the project's `.claude/soul-roles.md` replace the global
`~/.claude/soul-roles.md` rows of the same role; with neither, a built-in default
applies. Under `.claude/`, not `.ai/`: it changes behaviour, and `.ai/` must stay
safe to delete.

```
| role        | harness       | model            | settings      |
|-------------|---------------|------------------|---------------|
| implementer | claude        | sonnet           | rung=1        |
| implementer | claude        | opus             | rung=2        |
| reviewer    | claude        | opus             |               |
| reviewer    | codex         | default          |               |
```

- **Harnesses:** `claude` (Claude Code, your Claude login), `claude-ollama` (Claude
  Code driving a local Ollama model — give the exact installed tag, e.g.
  `qwen3.8:27b-q8_0`), `codex` (Codex CLI, your ChatGPT login), `codex-ollama`.
- **Several rows of one role are its ladder,** tried in `rung` order. A local model is
  just a row; whether it is good enough is the owner's call, not this skill's.
- **Settings:** `rung=`, `n=` (best-of-n: n tries, the check picks; default 1),
  `timeout=` (seconds per try; default 1800), `effort=` (reasoning effort, a word:
  `low medium high xhigh max` for `claude` rows, `minimal low medium high xhigh` for
  `codex` rows; unset, the harness's own default).
- **A `codex` row with model `default` runs Codex's own default model and effort,**
  not your `~/.codex/config.toml` — workers skip user config. Seen 2026-10-28:
  codex-cli 0.163.0 ran `gpt-6.1-sol` with effort unset. For any comparison, name
  both: a model, and `effort=`.
- **The host is not a row.** It is whatever you started this session with. A
  `claude` row still reaches Anthropic from a session launched on Ollama — the
  dispatch tool clears the inherited Ollama variables.

A custom workflow file may carry its own `## Roles` table for that workflow alone
(see Custom workflows). So **every `dispatch.py roles`, `run` and `review` call a
workflow run makes passes `--workflow <name>`** — the workflow being run, built-ins
included (`--workflow build-verify`, `--workflow review`; a built-in has no file, so
it gets the shared table). `--workflow` also puts the name in `result.json`,
`review.json` and the dispatch record.

`/soul-workflow roles`: show the shared table; on request, ask which file (global or
this project's) and write the change there. `/soul-workflow roles <name>`: show
`dispatch.py roles --workflow <name>`, the table that workflow will use, each row
with its source (`workflow (<file>:<line>)`, `project`, `global` or `built-in`).

## build-verify

### 1 · Settle the work first

Each piece of work needs a **Done when** line: one command this session can run,
exit 0 meaning done. No runnable check → it is not delegable; do it here. Unclear
requirements are the owner's (contract rule 7): ask before dispatching, not after.
A step may name its role (`Role: implementer`); otherwise the implementer ladder's
lowest rung takes it.

### 2 · Write the brief

The worker sees only this. A good brief is the largest lever there is on a cheaper
model's result (the I080 scans: a written handoff let a cheaper fixer match the
best single model). Write it to a file under `.ai/` with:

- **Goal** — what must be true when it is done, in plain words.
- **Files** — where to look and what to change; what not to touch.
- **Constraints** — style to match, behaviour to keep.
- **Done when** — the exact command.

The dispatch tool appends the worker rules itself (never write the Soul record; run
the check; report what was not run).

### 3 · Dispatch — one call per round

```
python3 <root>/tools/dispatch.py build-verify --workflow <name> \
  --brief <brief> --check "<Done-when command>" --run-id <id>
```

`<name>` is the workflow being run: `build-verify` here, a custom workflow's own name
when its steps use this one. Run it in the background: workers take minutes (a local
model's first call took 227 s, SOUL-200). It does a whole round's mechanics in one
call, so this session spends its turns on judgment, not plumbing: round 1 of the
workflow-value test (soul-benchmark `experiments/2026-10-28-workflow-value/RESULT.md`)
cost 3.3× plain Claude Code for the same quality, because the host spent 32 turns
(plain: 8) launching runs, reading result files, re-running checks and recording
tallies. One call:

- **climbs the implementer ladder** from the lowest rung: two attempts per rung, the
  second with the first one's failure added to the brief; the first winner stops it.
  A try wins when it finished cleanly, changed something and passed its check, and
  among those changed the fewest lines (`n=` above 1: best-of-n, which needs
  bubblewrap). A try that touched the Soul record never wins.
- **runs the winner's check through the recorder** (`delegation-check.py record
  --confine`, launched as its own process): confined, and recorded with the round,
  rung and run id. A recorded failure counts as that attempt failing.
- **runs every reviewer** read-only on the winner's patch, in the winner's worktree.
- **writes `bundle.md`** (and prints it): status, the winning row, the recorded check,
  the patch, the findings numbered `F1…`, the cost, and the next commands.

It exits 0 for a winner recorded passing, 1 for no winner, 2 when the recorder
refused or could not run the check, or the call was refused (without bubblewrap it
is refused before any worker starts).

Every dispatch takes its own run id, all from one `<id>`: `<id>-k<rung>-a<attempt>`
for the first round's attempts, `<id>-r<round>` for a repair round (its attempts
`<id>-r<round>-k<rung>-a<attempt>`), `<id>-rev<round>` for each round's review. A run
id that already holds a result is refused, so evidence is never overwritten; one
`clean --family` removes them all (step 7).

### 4 · Check — read the bundle, the patch first

Read `bundle.md`, and in it the **patch** first: you, not the worker's report, say
what changed. The check in the bundle was run by the recorder — the instrument the
worker did not make — under bubblewrap (`--confine`) in the winner's worktree; that
recorded result is the observed check, so do not re-run it each round. `accept`
runs it once more on this checkout (step 7).

- **Winner recorded passing** → step 5.
- **No winner** → every rung's two attempts failed: bring it to the owner with the
  evidence (or, if the owner says so, do it here).
- **Check not recorded** → the recorder refused or could not run the check; its
  output is in the bundle. Bring it to the owner.

### 5 · Weigh the findings

Each reviewer's findings are in the bundle as `F<n> [<harness>:<model>] <text>`. **A
finding is a claim, not a verdict.** Weigh each against the patch, and open a file
only when the patch cannot settle it; accept a finding only when you can see the
defect. Two reviewers from different model families catch different errors — but the
evidence for that is one planted-error study, so it stays an experiment the records
decide. Write the ids you accept to a file, one per line, each with your note
(`F2: the loop skips the last page`). The next call (`--repair-of` or `accept`)
records each reviewer's tally from that file; do not record them by hand.

### 6 · Repair — at most two rounds

Accepted findings and a round below 3 →

```
python3 <root>/tools/dispatch.py build-verify --repair-of <prev> --accepted <file>
```

`<prev>` is the previous round's family run id: `<id>` after round 1, `<id>-r2` after
round 2. It commits the candidate on its own worktree branch — the patch you read,
never what the checks left behind in the worktree — then records the previous
round's tallies, and writes a new brief: the original plus each accepted finding as
the reviewer wrote it (with its failure scenario) and your note. Then it runs step
3's round again from the candidate, not from the original base, starting at the rung
that produced the candidate (not the bottom of the ladder). Back to step 4 with the
new bundle. Round 3 is the last: still failing after it → stop and hand the owner the
candidate, the evidence and the open findings; the tool refuses a fourth round.

### 7 · Accept

```
python3 <root>/tools/dispatch.py accept --run-id <final round's family run id> \
  [--accepted <file>]
```

Only after reading the final patch, and in the background like step 3: its spot
check runs the whole check with the row's timeout, and a foreground call cut off at
120–600 s would stop it after the patch is applied. Run it for the git top level of
this checkout (a subfolder is refused). It applies the COMBINED change from the
original base — never only the last round's patch, which after a repair is against
the committed candidate, not your branch. It is built from the stored patches you
read, never from what the checks left in the worktree: the final round's base plus
its patch, then `git diff --binary --cached <original base>`; then `git apply
--check` and `git apply` on this checkout (nothing is applied when the check fails).
Then it records the final round's tallies, re-runs the check on this checkout through
the recorder with `--confine` (the spot check), and removes every worktree and branch
the run made (`clean --run-id <id> --family`). Exit 1: the spot check failed and the
patch stays applied — it prints the `git apply -R` that undoes it. Exit 2 after
applying: the patch stays applied but the recorder refused or could not run the
check, so nothing was recorded — bring it to the owner.

### 8 · Report

One reply: what changed; each check, as recorded, with its result; each reviewer's
findings — accepted (fixed in round N) or rejected (why); what is still open; what
was not run; the cost from the bundle. End with the contract's bottom line. If the
run taught something a later session could not re-derive (a role that keeps failing,
a reviewer that adds nothing), offer a witness entry.

### Building blocks: `run` and `review` by hand

A custom workflow that needs less than a whole round — one attempt, no escalation, no
review — uses the two building blocks `build-verify` is made of, and records the check
itself. Read the patch before the check runs: the check runs the worker's code.

```
python3 <root>/tools/dispatch.py run --role implementer --workflow <name> \
  --brief <brief> --check "<Done-when command>" --run-id <id>-k<rung>-a<attempt> [--rung K]
python3 <root>/tools/delegation-check.py record --step "<step>" \
  --worker implementer:<harness>:<model> --check "<Done-when command>" \
  --cwd <winner worktree> --confine --workflow <name> --role implementer \
  --rung <K> --round <R> --run-id <run id>
python3 <root>/tools/dispatch.py review --role reviewer --workflow <name> \
  --brief <brief> --diff <patch> --workdir <winner worktree> --run-id <id>-rev<round>
python3 <root>/tools/delegation-check.py review --run-id <id>-rev<round> \
  --reviewer <harness>:<model> --raised <N> --accepted <M>
```

`run` prints a result with each try's patch, its check result and the winner; a try
flagged `record_touched` changed the Soul record: reject it. `--confine` refuses
(exit 2, nothing recorded) where there is no bubblewrap. `--workdir` makes the
reviewers read the candidate's files, not this checkout. To apply by hand: from the
final worktree, `git -C <worktree> add -A && git -C <worktree> diff --binary --cached
<original base> > <file>`, read it, `git apply <file>` here, re-run the check through
the recorder with `--cwd` this checkout, then `dispatch.py clean --run-id <id>
--family`.

## review

1. Make the diff file: your working changes (`git diff HEAD` plus untracked files)
   or a branch (`git diff <base>...<head>`). For a branch, also make a worktree of
   `<head>` (`git worktree add --detach .ai/worktrees/<id>-head <head>`) and pass it
   as `--workdir`, so the reviewers read the branch's files, not this checkout's.
   Write a short brief: what the change is for, what it must not break.
2. `dispatch.py review` as in build-verify's building blocks (`--workflow review`,
   `--run-id <id>-rev1`); weigh each finding; record the tallies
   (`delegation-check.py review`, as there). `dispatch.py clean --run-id <id> --family` removes
   the `<id>-head` worktree afterwards.
3. Report the findings you accept, those you reject and why. Review makes no edits;
   fixing is a separate step the owner chooses.

## Custom workflows

`/soul-workflow list` runs `python3 <root>/tools/dispatch.py workflows`: the two
built-ins and every workflow file it finds, with each one's description. A project's
`.claude/soul-workflows/<name>.md` replaces a global `~/.claude/soul-workflows/<name>.md`
of the same name; a file cannot take a built-in's name (the owner's choice, 2026-10-28).

`/soul-workflow <name>` with a name that is not built in: find it in that listing,
read the file, and follow its steps. A file the listing marks *ignored* is not run —
say why. A workflow file is a short Markdown file:

```
---
name: quick-fix
description: one try at the lowest rung, the reviewers once, no repair round
---

1. Settle the work and write the brief (build-verify steps 1–2).
2. Dispatch `implementer`, lowest rung, one attempt, and record its check (the
   building blocks `run` and the recorder; read the patch first).
3. Review with `reviewer` (the building block `review`); weigh the findings
   (build-verify step 5).
4. No repair round: report (build-verify step 8) with the accepted findings as open
   items for the owner to decide.
```

A file may leave building blocks out — no review, no repair, one attempt only — and
the report says what was left out ("no review ran"). When a file's attempts run out
and the check still fails, stop and bring it to the owner; do not go further up the
ladder than the file allows. Record its runs with `--workflow <name>`. *Ignored*
means the file has a built-in's name or a name that is not lower-case letters,
digits and `-`.

Its steps name build-verify's steps by number — settle (1), brief (2), dispatch (3),
check (4), review (5), repair (6), accept (7), report (8) — and roles from the roles
table. Step 3 is one whole round (the ladder, the recorded check, the reviewers); a
step that wants less — one attempt, no escalation, no review — uses the building
blocks `run` and `review` by hand instead (end of build-verify). A role the file names but `dispatch.py roles --workflow
<name>` lacks: stop and ask the owner for a row. A copy to start from:
`<root>/skills/soul-workflow/templates/quick-fix.md`.

**A workflow's own models.** A workflow file may hold an optional `## Roles` section:
a table in the roles-table format, read only for that workflow (`--workflow <name>`),
with the same checks (an error names the file and line). For each role, the first of
these that names it supplies ALL of that role's rows: the workflow file's `## Roles`,
then the project's `.claude/soul-roles.md`, then the global `~/.claude/soul-roles.md`,
then the built-in default. Roles the section does not name keep their shared rows.
A table inside a ``` fence or an HTML comment is not read. `/soul-workflow roles
<name>` shows the result.

**What no workflow file can change** — these hold whatever a file says, and a step
that would break one is skipped and named in the report:

- every check runs confined and recorded by the recorder, launched by the dispatch
  tool or this session — never a worker's word, even when a file leaves the review
  out; this session reads every patch before `accept`, and `accept` re-runs the
  check on this checkout;
- workers get only the brief, run sandboxed, and never write the record;
- a reviewer's finding is a claim this session checks;
- unclear requirements go to the owner before anything is dispatched;
- at most two repair rounds without the owner (a file may allow fewer).

A workflow file is instructions, and only the owner writes them. A step outside these
building blocks — reaching the network, pushing, touching another project, anything
with credentials — waits for the owner's yes, whatever the file says.

## Seeing how roles do

`python3 <root>/tools/delegation-check.py stats` — every dispatch per role and model
(runs, won, timeouts, minutes); per role and model, the checks the recorder ran
(passed, failed, highest rung reached); per reviewer, findings raised and accepted.
This is how a role earns its row or loses it: a role that rarely wins or keeps timing
out, a rung that always escalates, or a reviewer whose findings are never accepted,
is a row to change.

## What not to do

- Do not report a step done because a worker said so — only an observed check counts.
- Do not let a reviewer's verdict stand in for your own reading of the finding.
- Do not let a worker write the record; do not paste the record into a brief.
- Do not spend more than two repair rounds without the owner.

## Not yet known

- Model quality on real work, for any row. The records will show it; benchmarking
  models is SOUL-I083's job, not this skill's.
- `codex-ollama` rows: not yet run end to end.
- Hosts other than Claude Code: Codex as host follows `operations/codex.md`; other
  harnesses are workers only in v1.

---

**Source:** SOUL-I080 (2026-10-27) — discussed and grilled with the Body (23 decisions
in its entry); replaces `/soul-delegate` (SOUL-I066), whose Done-when lines and
recorder it keeps. Isolation of workers: probe of 2026-10-27 (v3.7.0 plan, step 1).
**Adopted:** v3.7.0. **Status:** experimental — the roles, the ladder, the two
reviewers and the repair budget are defaults the records are meant to test.
