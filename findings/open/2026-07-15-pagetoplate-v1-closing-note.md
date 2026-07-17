# Closing note — PageToPlate v1 build (2026-07-14 → 15)

Upstream observations owed at milestone per the project contract. System-level
lessons only; domain lessons stay home in PageToPlate's record.

**Context:** ~30-task app build executed subagent-per-task (orchestrator + 14
agent dispatches), two owner demo checkpoints, per-task commits, TDD on all
logic. Shipped: 126 unit tests, Playwright E2E, deployed PWA.

## Observations about the system itself

1. **Force-comments carried the record where instruments couldn't.** Headless
   subagents can't invoke /soul-capture; contract clause 5's fallback (decision
   comments at the code site + handoff reports) was exercised ~10 times and was
   sufficient — the orchestrator distilled agent reports into witness entries at
   session end. No capture was lost, but the distillation step is a single point
   of failure if the orchestrating session dies before writing witness.md.

2. **A flagged defect with no owner reached the Body** (PageToPlate P2P-004): an
   agent's report explicitly flagged a missing dark-theme token at Milestone A;
   no task adopted the flag; the owner hit it at the first demo. Agent reports
   that flag issues need a mechanism that converts flags into scheduled work —
   a note in a report is not a gate.

3. **The completion gate (Stop hook) drove real verification both times it
   fired.** First fire: plan-only turn, gate produced an honest "nothing built
   yet" line. Second fire: it prompted the orchestrator to personally rasterize
   and inspect the production build rather than rely on subagent eyes — which
   caught a real cosmetic defect (empty-state message) that 126 passing tests
   and a green E2E had not.

4. **Per-task commits made session-death cheap.** A subagent was killed mid-
   milestone by a session limit after ~106k tokens of context-reading with zero
   file writes; the clean tree meant a fresh dispatch lost nothing but the spent
   tokens. Cost pattern worth knowing: agent briefs that front-load large
   reading lists burn budget before producing anything durable.

5. **Owner checkpoints beat spec fidelity twice.** Two handoff-design elements
   (card ruling, rejected-only regenerate) were overridden by the owner at first
   contact with the running app. The checkpoint cadence (demo at hero-flow, demo
   at feature-complete) caught both at the cheapest possible moment.
