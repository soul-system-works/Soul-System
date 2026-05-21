# Stream Experiment — pre-registration (spec Step 2)

**Date:** 2026-05-21 · **Status:** pre-registered (written before any run, per the
anti-selection-bias invariant). Parent: `2026-05-21-token-economics-measurement-design.md`.

## Hypothesis (null honored)
As a project grows, **Soul-on** cost-per-task grows *sub-linearly* vs **Soul-off**,
because recorded structure (AL, witness, decisions) lets later tasks reuse earlier
reasoning instead of re-deriving it. **Null:** no slope difference (or Soul-on is
just more expensive) — methodology is overhead. Both outcomes are publishable here.

## Conditions (clean ablation)
- **Soul-off:** each task run cold — given only the task + the code-so-far. No seed,
  no gates, no records. Fresh context per task.
- **Soul-on:** each task run with the seed posture + an accumulating record handed in
  (prior tasks' AL/decisions/witness, ~a handoff cursor). Records persist between tasks.
- **Held fixed:** same model, same code-so-far at each task's start, same task text.
  The *only* variable is whether accumulated structure is present.

## Metric
- Primary: **subagent `total_tokens` per task** (the Agent tool reports it) → plot vs
  task position. Compare the two conditions' slopes.
- Counter-metric (anti-Goodhart): **completion/quality** per task (did it do the task,
  tests pass) — so "cheaper" can't win by doing less.
- Conformance (Soul-on only): did the run actually use the records, or ignore them?

## The stream (pre-registered, compounding — small ledger library)
Each task builds on the last; tasks 6–8 deliberately revisit earlier decisions, where
recorded structure should pay off most.
1. Core model: add/list ledger entries (amount, date, memo).
2. Persistence: save/load to a file.
3. Categories/tags on entries.
4. Query/filter (by date range, category).
5. Summary report (totals by category).
6. **Requirement change:** multi-currency — revisits the task-1 model.
7. **Refactor:** extract a storage module — revisits structure from tasks 1–2.
8. **Cross-cutting feature** touching tasks 1, 3, 6 (max compounding) + edge-case hardening.

## Runner
Each (task × condition) = one subagent run in an isolated worktree (sandbox). Soul-off
gets task + code; Soul-on gets task + code + the accumulated record. Capture
`total_tokens` + completion. ~8 tasks × 2 conditions = **~16 subagent runs**.

## Pitfalls pre-committed against
Pre-registered tasks (no cherry-picking) · model/seed pinned · null reported honestly ·
cost paired with completion · conformance checked · this is a single small stream (a
directional signal, not proof) — not the standalone benchmark (still gated).
