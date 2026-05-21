# Token-Economics Measurement Design — does the Soul System pay for itself?

**Date:** 2026-05-21
**Status:** draft (spec-first; execution begins with the resume-cost A/B, Step 1)
**Ideas:** SOUL-I005 (the claim), SOUL-I011 (the apparatus). Research: witness SOUL-051.

## Problem (two levels)

- **Immediate:** measure whether the Soul System's accumulated structure (witness,
  findings, AL records, amendments, gates) saves more tokens/effort *later* than it
  costs *up front*.
- **Larger:** this is the system's core value proposition, currently asserted, not
  measured. Believing it unmeasured is itself a **Coherent Falsehood** (SOUL-A010).
  This design is the Emissary turned on the system itself — and the "accelerator"
  the system structurally lacks (SOUL-F014).

## The central reframe (from the research)

The savings claim is a **carryover claim**: does structure recorded on earlier work
reduce the cost of later work? The "can't do the same task twice" confound cannot be
neutralized — counterbalancing assumes carryover cancels *symmetrically*, which is
false for a methodology that deliberately leaves artifacts behind (its carryover is
maximally asymmetric). **So convert the confound into the signal:** measure cost as a
function of accumulated structure / position in a task sequence, not as a treatment
effect on one task. (Prior art: DeepMind Evo-Memory, 2025 — sequential task streams
measuring experience *reuse*.)

**The null is live and honored.** Scaffold-ablation studies show methodology often
buys little; the Soul System may be net overhead. This design *tests*; it does not
confirm.

## Abstraction layer

- **What varies:** the experiment (resume-cost A/B → sequential stream → standalone
  suite); which side is measured (cost vs savings).
- **What decides variation:** the cost side is ~answered (doctrine footprint is small
  — I005 data point); the **savings side is the unmeasured half**, so the design
  targets it.
- **What cannot vary (the invariants):**
  1. **Carryover is the signal** — never assumed away.
  2. **Conformance is instrumented** — measure that gates actually fired (the
     `.soul/events.jsonl` log), never trust the "Soul" label (TDD's hard lesson).
  3. **Null-honest** — "the system is overhead" is a valid, valuable outcome.
  4. **Cost is paired with quality** — never a single metric (Goodhart); report a
     cost-vs-quality Pareto point.
  5. **No vanity metrics** — counting witness entries / findings is activity, not
     value (we are especially prone, our outputs being documents).

## Metrics (savings side)

- **Re-derivation avoided / resume cost** — tokens & turns to re-establish working
  context: cold start vs `/soul-resume`-from-handoff. The cleanest in-situ proxy.
- **Cost-per-task vs position in a task stream** — sub-linear growth (or decline)
  under Soul-on relative to Soul-off = savings.
- **Rework / defect-escape rate** on later tasks.
- **Up-front overhead** — the early-task cost penalty (the cost side of the ledger).
- **Conformance** — gate-fire counts from `.soul/events.jsonl` (did the treatment
  actually happen?).

## The sequence (cheapest → evidence-gated)

**Step 1 — Resume-cost A/B (first; near-zero cost).**
At session boundaries, measure tokens/turns to re-establish context: cold start vs
`/soul-resume` from `.soul/handoff.md`. Same accumulated state, two resume methods —
no task repetition. Capture via a new event (e.g. `soul.resume.cost`) or a manual
log. This session opened with `/soul-resume`, so the workflow already exists.

**Step 2 — Sequential task stream (the primary experiment).**
Author one ordered stream of ~8–15 distinct-but-linked tasks in an evolving
mini-project. Run twice on the same model: Soul-on (records persist between tasks) vs
Soul-off (cold each task). Measure cost-per-task and resolution vs *position*.
Pre-register the task list (anti-selection-bias); pin model/seed; report variance.

**Step 3 — Standalone benchmark project — NOT YET (evidence-gated).**
A task suite + dual runners (a "soul-bench" dogfood, like REF-09) is a
*later* investment, justified only if Steps 1–2 show a real slope. Building it first
is the Premature Sophistication / Universe Collapse the methodology exists to prevent.

## Anti-patterns (designs that fake a proof)

- Confounded single A/B (one task, Soul-on then off) — invalid; asymmetric carryover.
- Conformance illusion — the "Soul" label without measured gate-firing.
- Vanity metrics — document-count as value.
- Hawthorne / novelty — our own dogfood enthusiasm on any human-judged metric; prefer
  agent-run + objective metrics, run long enough that novelty decays.
- Selection bias — pre-register tasks.
- Goodhart — always pair cost with a quality counter-metric.

## Open questions (deferred to execution)

- Resume-cost capture mechanism: a new `.soul/events.jsonl` event vs a manual log.
- Stream task domain: a real small project vs a synthetic one.
- "Soul-off" definition: it must be a clean ablation (no seed import / gates disabled),
  not a half-measure.
- The slope threshold that would justify Step 3.

---
**Source:** Research synthesis 2026-05-21 (Researcher subagent, via the Emissary).
Anchors: carryover/counterbalancing confound (arXiv 2408.07594; 2505.03937);
savings-as-carryover design (Evo-Memory, arXiv 2511.20857); cost-vs-accuracy Pareto +
the "needlessly complex" warning (AI Agents That Matter, arXiv 2407.01502);
scaffold-ablation null (arXiv 2505.08120); TDD conformance / equivocal-payoff canon.
**Adopted:** 2026-05-21. **Status:** draft — execution begins with Step 1.
