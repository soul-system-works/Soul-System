---
name: soul-delegate
description: Turn on plan-step delegation for this session — each plan step carries a Tier (deep / routine / review) and a Done-when check; routine and review steps may go to another model (a subagent, a local model through Ollama, Codex), and the main session re-runs every check itself and records the observed result. Owner-invoked. `/soul-delegate off` turns it off; `/soul-delegate tiers` shows or edits the tier table.
disable-model-invocation: true
---

# /soul-delegate — hand plan steps to other models, keep the check at home

**Codex:** Read [the host integration](../../operations/codex.md) before
following this workflow. Its Codex procedures replace Claude-specific loading,
instruction-file, tool, and invocation mechanics; the shared workflow follows.

`/soul-delegate` turns it on for this session · `/soul-delegate off` turns it off ·
`/soul-delegate tiers` shows the tier table and edits it on request.

**What this is — and is not.** Not a router. The main model is whatever the session
was launched with (Anthropic, Claude Code pointed at Ollama, a `/model` switch); this
skill cannot change it. What it changes is how a plan's steps are handed off: routing
lives in the plan, one step at a time, and the Soul part is the contract's rule 4 —
the main session never takes a worker's word that a step is done. It re-runs the
step's check itself and records what it observed. Routing tools that do more already
exist (the Codex plugin, consult/review tools, request proxies); use them alongside.
*Why this shape:* SOUL-I066 — a prior-art check found routing mostly built elsewhere
and listed four gaps. The owner kept two (the tier table, and the record of who did
the work and whether its check passed when the main session ran it) and left two out
as routing jobs: one on/off switch across providers, and routing that adapts to the
launched main model.

## On (no argument)

1. **Load the tier table.** Rows in the project's `.claude/soul-tiers.md` override
   rows in `~/.claude/soul-tiers.md`. (It lives under `.claude/`, not `.ai/`, because
   it changes behaviour and `.ai/` must stay safe to delete.) With neither file, use
   this Claude-only default:

   | Tier    | Goes to                                                     |
   |---------|-------------------------------------------------------------|
   | deep    | the main session                                            |
   | routine | a subagent on `sonnet` (or `haiku` for mechanical work)     |
   | review  | a fresh-context subagent (`diff-reviewer` if defined)       |

   If `codex` is on PATH, or `ollama list` shows a model, **say so in one clause** —
   review could go to a different model family, routine to a local model — but do
   not change the table; it is the owner's (`/soul-delegate tiers`).
2. Say ONE line: `Delegation on — deep → … · routine → … · review → …`.
3. For the rest of the session, apply the convention below whenever a plan is
   written or executed, whichever planning skill wrote it.

## The plan-step convention

Each step carries two lines:

```
Tier: deep | routine | review
Done when: <a command the main session can run; exit 0 means done>
```

- **No runnable check → `Tier: deep`.** A step whose result can only be judged by
  reading it stays with the main session. The check is what makes handing a step to
  a weaker or cheaper model safe.
- Design, unclear requirements and hard debugging are `deep`.
- A delegated step goes out as a **self-contained brief**: goal, files, constraints,
  and the Done-when line. The worker sees nothing else of this session. The brief
  also says: *do not write the project's record files* (`witness.md`, `ideas.md`,
  `mind.md`, `.soul/`).

## Dispatch — existing commands only

- **Same provider as the main session:** a subagent (Agent tool) with a model alias.
  In a session launched on Ollama the aliases point at whatever local models the
  launch environment set, and cannot be remapped mid-session (per Claude Code's docs;
  untested under `ollama launch`).
- **Local model** (run as written in SOUL-201):
  `MAX_THINKING_TOKENS=4000 CLAUDE_CODE_MAX_OUTPUT_TOKENS=8000 ollama launch claude --model <tag> -- -p "<brief>" --permission-mode acceptEdits --allowedTools "Bash(<check program and fixed args> *)" --output-format json`.
  The `--allowedTools` entry matters: under `acceptEdits` alone the worker's own
  check command was blocked (SOUL-200); with the prefix form above it ran (SOUL-201).
  The two caps are a precaution — whether Ollama honours a thinking budget is not
  known.
- **Codex:** work — `codex exec -s workspace-write -C <dir> -o <file> "<brief>"`;
  review — `codex exec -s read-only …`, or the Codex plugin's `/codex:review` /
  `/codex:adversarial-review` if installed.
- **Main session in Codex, Claude tier:** `claude -p "<brief>" --model <alias> --permission-mode acceptEdits --allowedTools "Bash(<check program and fixed args> *)"`.
  Keep the brief right after `-p`: `--allowedTools` takes several values, so a
  brief placed after it is read as another tool and the call fails with no prompt.
  It needs network access, which Codex's `workspace-write` sandbox does not give by
  default — unverified; expect to approve an escalation.
- **Workers take minutes.** The first local run took 227 s (SOUL-200), past the Bash
  tool's 120 s default. Run a worker with `run_in_background`, or give the Bash call a
  timeout above its expected time.
- **A nested `claude -p` worker loads the Soul plugin if it is enabled** at user or
  project scope, so in a Soul project its own completion gate may fire and append
  events to `.soul/events.jsonl`. Those are the worker's, not the main session's.
  A worker inherits the main session's `CLAUDE_CODE_SESSION_ID`, so a worker that ran
  the recorder itself would look like the main session — another reason the brief
  forbids the record files.
- **Keep the worker's change separable:** ask the owner to commit first, or dispatch
  into a git worktree. Review with `git status` and `git diff` — new files a worker
  creates do not show in `git diff`. One worker per tree at a time.

## After every dispatched step — the check stays home

1. Read the worker's change, not its report.
2. Run the check through the recorder. It runs the command itself and appends the
   observed result to the project's `.soul/events.jsonl`:

   ```
   python3 <plugin-root>/tools/delegation-check.py record --step "<step>" \
     --worker <tier>:<tool>[:<model>] --check "<Done-when command>" \
     [--cwd <worktree>] [--reviewer <tool>[:<model>] --review-verdict pass|fail]
   ```

   Run it from the session's own directory. `<plugin-root>` is two levels above this
   skill's directory. `--cwd` is only where the check runs (a worktree, a subfolder);
   the record goes to the project found by walking up from the recorder's working
   directory to `witness.md` or `.soul/witness.md`. Outside a Soul project the check
   runs but nothing is recorded. The recorder stops a check at `--timeout` (540 s by
   default, under the Bash tool's 600 s foreground cap); give the Bash call a timeout
   above that, and run a longer check with `run_in_background` and a larger
   `--timeout`. The tool is POSIX-only (Linux, macOS, WSL). The check result is observed; a review verdict is the model's report and is
   recorded as self-reported.
3. **FAIL:** fix it in the main session or re-dispatch with the failure text. Never
   report the step done on the worker's word.
4. **Seeing the records:** `delegation-check.py list --session "$CLAUDE_CODE_SESSION_ID"`
   is the view. When the completion gate fires, its verdict event also carries this
   session's cumulative counts (`delegation: {checked, failed}`) — but the gate fires
   rarely, and a turn whose edits were all made by workers may not trip it at all.

## Off

`/soul-delegate off`: stop applying the convention and say `Delegation off.` The
records already written stay.

## Tiers

`/soul-delegate tiers`: show the effective table and where each row came from. To
change it, ask which file — the user's `~/.claude/soul-tiers.md` or this project's
`.claude/soul-tiers.md` — then write the table in the format above, one row per tier,
naming the tool and model (e.g. `routine | ollama: qwen3.8:27b`).

## Not yet known

- Whether the "on" state survives context compaction. Untested. If it drops, run
  `/soul-delegate` again; a hook is added only if a test shows it is needed.
- Open-model quality on real plan steps. One easy step has run end to end, twice
  (SOUL-200, SOUL-201); that proves the plumbing, not the quality.
- The Codex-host dispatch line and the `codex exec` lines have not been run through
  this workflow.

---

**Source:** SOUL-I066 (2026-10-19) — explored with the Body: routing lives in plan
steps; the Soul System adds the step convention and the observed-check record.
Dispatch evidence: SOUL-200, SOUL-201. **Adopted:** pending review. **Status:**
draft (branch `i066-delegation`).
