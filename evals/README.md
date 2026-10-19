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

## Unknown until the first live run

Whether the eval trace includes the Stop hook's feedback record is not known. If
`soul-gate-fired` misses in every with-plugin run, check a run's transcript before
concluding the gate did not fire — the trace may simply not carry hook feedback.
