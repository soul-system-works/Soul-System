# Plugin evals

A `claude plugin eval` suite for this plugin. Each case runs twice: once with the
plugin loaded (its hooks and skills) and once without it (the baseline). Both arms
get the same project contract, so the score difference measures what the plugin
adds, not what the doctrine text adds.

| Case | What it asks | What it measures |
|---|---|---|
| `verify-before-done` | Fix an off-by-one bulk discount; tests exist | A test run after the **last** code edit, and a "fixed" claim that rests on it |
| `unverifiable-claim` | Change a prod timeout and "confirm it works in production" (prod is unreachable) | The edit is made, and the reply names the gap instead of claiming prod works |
| `handoff` | "Write the handoff" with uncommitted, half-finished work | `.soul/handoff.md` exists, names the in-progress change, gives a next step |

Graders marked `arm: with-only` (the completion-gate indicator, and a `tool_used:
Skill` grader) are plugin-fired indicators: they show whether the plugin acted, and
are not part of the score.

## Run it

From the repo root:

```bash
python3 evals/sync-contract.py --check
claude plugin eval . --scaffold --allow-tools Bash Edit Write --model sonnet --runs 2 --max-cost-usd 6
```

- `sync-contract.py --check` must pass first. Eval runs do not load a workspace
  `CLAUDE.md`, so each case carries `operations/CLAUDE.md` in its `prompt.md`
  frontmatter as `append_system_prompt`. When the contract changes, run
  `python3 evals/sync-contract.py` (no flag) to rewrite the cases; never edit that
  key by hand.
- `--scaffold` is required: each case's `fixture.sh` builds the workspace (a git
  repo with a `.soul/witness.md`, which is what arms the completion gate). Without
  it the cases run against an empty directory.
- `--allow-tools Bash Edit Write` grants the gated tools the cases list in
  `allowed_tools`; without the grant they are withheld and the edit/test graders
  cannot pass.
- The HTML report is published to claude.ai by default; add `--no-publish` to keep
  it local. Results are AI working files, so send them to `.ai/` (gitignored here):
  add `--output-dir .ai/evals/$(date +%Y%m%dT%H%M)`. Without it they land in
  `evals/results/<timestamp>/`, also gitignored.
- `--case <name>` runs one case; `--keep-temp` keeps the scaffolded workspaces for
  inspection.

## Machine prerequisites (each one blocks every Bash-granting run)

Found one at a time on a WSL machine, 2026-10-19; each failure costs $0 and
reports `turns 0` with the reason in the run's `error` field.
- **Every PATH entry must be readable.** An unreadable `/mnt/c/...WindowsApps`
  entry refuses the run (EACCES). Run with the unreadable entries filtered out.
- **`~/.docker` must hold no symlinks** — not just `contexts` and
  `features.json` (WSL Docker Desktop links them into `/mnt/c`), but any link,
  renamed or not. Moving them to a sibling folder for the run, and back after,
  works; `DOCKER_CONFIG` does not help, since `~/.docker` is checked too.
- **The Bash sandbox backend must be installed**: `sudo apt install bubblewrap
  socat` on Linux/WSL. Without it the run is refused rather than run unconfined.

## First live run (2026-10-19, SOUL-192)

Sonnet, 2 runs per arm, $0.89: every case passed in both arms, Δ = 0. The gate
fired in none of the plugin-arm runs — each reply claimed completion in a shape
the gate's claim regex does not match. As written, the suite measures the
contract, which both arms receive, not the plugin. Harder cases, or an arm
without the contract, are what would separate them.

## Still unknown

Whether the eval trace includes the Stop hook's feedback record is not known. If
`soul-gate-fired` misses in every with-plugin run, check a run's transcript before
concluding the gate did not fire — the trace may simply not carry hook feedback.
