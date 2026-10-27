---
name: soul-workflow
description: Run a named workflow across models — `build-verify` (another model implements a step in its own worktree, this session re-runs the check, two read-only reviewers from different model families report findings, at most two repair rounds) or `review` (the two reviewers alone, on a diff). Roles (harness + model, e.g. Claude, Codex, a local Ollama model) come from a roles table; this session keeps judgment and the record, and never takes a worker's word. Owner-invoked. `/soul-workflow roles` shows or edits the roles table.
disable-model-invocation: true
---

# /soul-workflow — other models do the work, this session keeps the judgment

**Codex:** Read [the host integration](../../operations/codex.md) before
following this workflow. Its Codex procedures replace Claude-specific loading,
instruction-file, tool, and invocation mechanics; the shared workflow follows.

`/soul-workflow build-verify` · `/soul-workflow review` · `/soul-workflow roles`

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
   (`implementer → claude:sonnet · reviewers → claude:opus + codex:default`). Say
   "use X for this" to override any of it.
2. Workers start with nothing but a written brief — no conversation, no Soul
   record, no project instructions (each runs as its own process with those
   switched off; SOUL-I080 step 1 probe, 2026-10-27).
3. Workers run inside a sandbox. A Claude worker has a full shell, but the operating
   system lets it write only in its own worktree, gives it no network, and hides
   credential folders (`~/.ssh`, `~/.claude`, `~/.codex`, the vault …) from it. On
   Linux and WSL that needs `bubblewrap` and `socat`; without them the dispatch tool
   refuses to start a Claude worker rather than run it unconfined. Codex workers use
   Codex's own `workspace-write` sandbox. Native Windows is not supported.
4. Nothing is called done on a worker's word. This session re-runs every check
   itself and records what it saw.
5. You get one report: what changed, which checks ran and passed, what each
   reviewer found and what was done about it, and what is still open.

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
  `timeout=` (seconds per try; default 1800).
- **The host is not a row.** It is whatever you started this session with. A
  `claude` row still reaches Anthropic from a session launched on Ollama — the
  dispatch tool clears the inherited Ollama variables.

`/soul-workflow roles`: show the table; on request, ask which file (global or this
project's) and write the change there.

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

### 3 · Dispatch

```
python3 <root>/tools/dispatch.py run --role implementer --brief <brief> \
  --check "<Done-when command>" --run-id <id> [--rung K]
```

Run it in the background: workers take minutes (a local model's first call took
227 s, SOUL-200). Without `--rung` it runs the lowest rung. With `n=` above 1 the
tries run one after another, each in its own worktree; the winner is a try whose
check passed, and among those the one that changed the fewest lines. It prints a
result with each try's patch, its check result, and the winner. A try flagged
`record_touched` changed the Soul record: reject that try; the others stay
eligible.

### 4 · Check it here

Read the winner's **patch**, not the worker's report. Then run the check through the
recorder, in the winner's worktree:

```
python3 <root>/tools/delegation-check.py record --step "<step>" \
  --worker implementer:<harness>:<model> --check "<Done-when command>" \
  --cwd <winner worktree> --workflow build-verify --role implementer \
  --rung <K> --round <R> --run-id <id>
```

- **Pass** → step 5.
- **Fail, or no winner** → each rung gets two attempts: the first dispatch and one
  retry with the failure text added to the brief. Both failed → the next rung
  (`--rung K+1`), again two attempts. The top rung's second failure → bring it to
  the owner with the evidence (or, if the owner says so, do it here).

Every dispatch takes its own run id — `<id>-k<rung>-a<attempt>` for the first round,
`<id>-r<round>` for a repair round: a run id that already holds a result is refused,
so evidence is never overwritten.

### 5 · Two reviews

Write the winner's patch with the brief to the reviewers:

```
python3 <root>/tools/dispatch.py review --role reviewer --brief <brief> \
  --diff <patch> --run-id <id>
```

Each reviewer works read-only and returns `FINDING:` lines. **A finding is a claim,
not a verdict.** Check each one against the code; accept it only when you can see
the defect. Two reviewers from different model families catch different errors — but
the evidence for that is one planted-error study, so it stays an experiment the
records decide. Record each reviewer's tally:

```
python3 <root>/tools/delegation-check.py review --run-id <id> \
  --reviewer <harness>:<model> --raised <N> --accepted <M>
```

### 6 · Repair — at most two rounds

Accepted defects go back to the implementer row that produced the candidate (the
rung it had reached, not the bottom of the ladder) as a new brief: the original
plus the accepted findings, each with its failure scenario. Then steps 3–5 again,
`--round 2`, then `--round 3`. Still failing after round 3 → stop and hand the owner
the candidate, the evidence and the open findings. Do not spend a fourth round
unasked.

### 7 · Accept and clean up

Apply the winner's patch to the branch you are working on (`git apply <patch>`),
run the checks here again, then `python3 <root>/tools/dispatch.py clean --run-id <id>`.

### 8 · Report

One reply: what changed; each check, observed here, with its result; each reviewer's
findings — accepted (fixed in round N) or rejected (why); what is still open; what
was not run. End with the contract's bottom line. If the run taught something a later
session could not re-derive (a role that keeps failing, a reviewer that adds nothing),
offer a witness entry.

## review

1. Make the diff file: your working changes (`git diff HEAD` plus untracked files)
   or a branch (`git diff <base>...<head>`). Write a short brief: what the change is
   for, what it must not break.
2. `dispatch.py review` as in build-verify step 5; weigh each finding; record the
   tallies.
3. Report the findings you accept, those you reject and why. Review makes no edits;
   fixing is a separate step the owner chooses.

## Seeing how roles do

`python3 <root>/tools/delegation-check.py stats` — per role and model: checks run,
passed, failed, highest rung reached; per reviewer: findings raised and accepted.
This is how a role earns its row or loses it: a rung that always escalates, or a
reviewer whose findings are never accepted, is a row to change.

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
