# Soul Self-Ablation — Hard-Regime Test (b) — Design

**Status:** draft — pending Body sign-off. **Project code:** SOUL.
**Idea:** [[SOUL-I040]] (umbrella); matures [[SOUL-I011]] (harness).
**Gates:** [[SOUL-F042]] (`WHY-NOT-YET-AMENDMENT` is literally this spec).
**Author:** Architect + Researcher + Skeptic, from the SOUL-108 handoff.
**Prior:** `docs/specs/2026-05-28-soul-self-ablation-harness-design.md` (D1–D7,
the proven method); `docs/experiments/2026-05-28-self-ablation-slice-1.md`
(A0–A10 + consistency, the moderate-task convergence).

---

## Problem (two levels)

**Immediate.** [[SOUL-F042]] converged on *moderate* tasks against a *careful,
consistent* Claude baseline: roles/gates change the **FORM** of work
(legibility/auditability), not the **SUBSTANCE** (the model already reasons that
way) or the **RELIABILITY** (already 5/5). The one regime that could overturn
this is **untested**: *hard* tasks where baseline carefulness plausibly breaks —
there a role might catch what the baseline misses (substance) or close an
intermittency the baseline has (reliability). This test gates whether F042
becomes an amendment.

**System it lives in.** This is the VALIDATE/PRUNE phase asking its sharpest
question: *is the per-role value claim regime-dependent?* The answer decides how
roles are **described and justified in doctrine** — as behavior-lifting, or as
legibility scaffolding. And (Body's expansion question) it decides whether there
is a **publishable contribution** here, and of what shape.

**Truth-seeking stance (Body, Emissary integrity — binding on this whole test).**
The goal is the *truth* of the system's value, present and future — **not** to
make the system look good. The experiment must be designed so a **null result is
a first-class, valued outcome**: if (b) finds the roles/gates add nothing even in
the hard regime, that is a real finding (it graduates F042 to an amendment and is
*itself* publishable — a documented null on a self-applied doctrine layer). Every
design choice below that could bias toward a positive result (task cherry-picking,
unequal compute, lenient scoring) is therefore a **threat to the result's value**,
not just its rigor. We do not force it to be good. We find out what it is.

---

## What the field already establishes (Researcher — anchors, not memory)

The literature strongly **corroborates F042's direction**, which sharpens both
the test design and the novelty boundary:

- **Personas/roles don't reliably help accuracy, sometimes hurt** — *When "A
  Helpful Assistant" Is Not Really Helpful* (arXiv 2311.10054); *Persona is a
  Double-edged Sword* (2408.08631).
- **Single-agent matches/beats multi-agent under equal compute** — *Single-Agent
  LLMs Outperform MAS … Under Equal Thinking Token Budgets* (2604.02460);
  *Single-agent or Multi-agent? Why Not Both?* (2505.18286). Reported MAS gains
  are "better explained by compute and context effects than architecture."
- **Agent ablation by removal is an established method** — *Agents that Matter:
  Optimizing Multi-Agent LLMs via Removal-Based Attribution* (2605.27621); it
  finds agent contributions to **accuracy vs ethics are decoupled** (adjacent to
  our form/substance/reliability split).
- **The legibility-value claim is itself partly known** — "agentic orchestration
  improves reliability and interpretability rather than raw accuracy"
  (TRiSM, 2506.04133; *Auditable Agents*, 2604.05485).

**Two consequences.**
1. *"Roles don't add substance on moderate tasks"* is **not novel on its own** —
   it would be scooped. Do not frame any paper around it.
2. The field hands us a **mandatory confound control we did not have in slice 1:
   equal-compute / token-budget normalization** (see C1). The with-role arm
   carries extra system-prompt tokens; an unnormalized win could be pure compute.

---

## The crux: regime ordering (recommendation)

Body asked "1 then others — your recommendation?" **Yes — buried-trap /
adversarial first, then long-horizon, then the two deep follow-ups.** Reasoning:

1. **Buried-trap / adversarial — FIRST.** Cleanest signal: a planted defect is
   **caught or not** (binary), so the metric resists the compute confound — more
   tokens don't manufacture a catch of a specific planted trap the way they can
   inflate a fuzzy quality score. Highest signal-to-confound ratio; fastest to
   score. This is the right tracer for the hard regime.
2. **Long-horizon / multi-constraint — SECOND.** This is where the field
   *predicts* scaffolding helps most (benefits grow as the base task strains the
   model). Strong test of the **reliability** axis (does a gate sustain a
   discipline the baseline drops mid-task?). But it is the regime *most* exposed
   to the compute confound — so it requires C1 strictly.
3. **Role's unique blind-spot (backlog #5) — THIRD.** Most diagnostic per role,
   slowest (one bespoke design per role). Do after we know the regime axis exists.
4. **Full-seed-minus-role (backlog #3) — FOURTH.** True integration ablation;
   answers "does a role matter *within* the layer even if modest alone?" Deferred
   — it is a different question (integration, not regime) and belongs after (b).

Start narrow (default-simplicity): **one regime, a tracer pair, C1 in place from
arm one.** Widen only when the tracer shows the design holds.

---

## Method (inherits the proven harness; deltas only)

Unchanged from slice 1 (do not re-derive): isolated
`claude -p "<task>" --append-system-prompt-file <lens/gate>` from a clean
`/tmp` working dir; bare arm = same task no `--append`; verbatim sentinel as a
separate first step to confirm loading; per-arm output files + hand-maintained
manifest; **self-contained prompts** (paste artifacts in-prompt — the empty-dir
confound bit 3× and must not recur); re-run on the transient "thinking blocks"
API error.

**New deltas for the hard regime:**

### C1 — Equal-compute control (NON-NEGOTIABLE, new)
The field's #1 ablation confound. For every arm pair:
- **Measure** tokens (input system-prompt + output) per arm; record in manifest.
- **Normalize the comparison**: the bare arm gets a length-matched neutral filler
  system prompt (same token budget as the role lens, content-free) OR we cap/match
  output budget. At minimum, **report** per-arm tokens so a reviewer can see the
  win is not a compute artifact. A "substance" verdict that vanishes under
  equal-compute is **not** substance.

### C2 — Difficulty validation (the hard part — task design)
A task only tests the hard regime if the **bare baseline plausibly fails it.**
Before scoring an arm pair, validate difficulty:
- Run the bare arm **N≥3** on the candidate task. If it already succeeds 3/3, the
  task is *not* hard for this model — discard or sharpen it. We need tasks in the
  **baseline-fragile** band (fails sometimes or subtly), not the impossible band
  (fails always — then no role helps either) nor the easy band (slice-1 territory).
- This is where care goes. A hard-regime claim is only as good as the evidence the
  baseline genuinely breaks.

### C3 — Trap taxonomy (for regime 1)
Planted defects of distinct kinds so a "catch" maps to a role: a hidden
contradiction (Skeptic), a swallowed constraint (Accountant), a plausible-but-
false premise / coherent falsehood (Emissary/Anchor), a buried long-range
dependency (Prophet), a silently-dropped requirement under length (completion
gate). One trap per task; label which role *should* catch it.

---

## Metrics and verdict

Per arm pair, three axes (matching F042's decomposition):
- **SUBSTANCE** — did the role arm catch/solve what the bare arm missed? (binary
  per trap for regime 1; rubric delta for regime 2) — **only counts under C1.**
- **RELIABILITY** — over N runs, does the role arm succeed at a *higher rate* than
  the bare arm? (the slice-1 consistency method, now on fragile tasks).
- **FORM** — legibility/naming delta (expected to persist; the moderate-task baseline).

**Graduation logic (from F042):**
- Hard regime **also** form-not-substance → F042 → **amendment** reshaping how
  roles are justified in doctrine (legibility framing, not behavior-lifting).
- Roles **do** add substance/reliability when the baseline breaks → conclusion is
  **regime-specific**; F042 stays scoped; doctrine gains a "roles earn their
  substance in the hard regime" rule. **This is the more publishable outcome.**

---

## Publication strategy (Body's expansion question — Prophet + Researcher)

**Body decision (2026-05-28): run (b) first as internal validation; decide
publication after.** (b) is scoped as honest internal truth-finding — *does our
own system add value in the hard regime?* — not as a paper-shaped experiment. The
map below is a **parking lot** to revisit once we have the regime result; it does
NOT shape (b)'s design (which is governed by the Truth-seeking stance above).

**Sequencing (Body): hand-built internal tasks first (option 1), existing public
benchmarks later (option 2).** Rationale: the internal hand-built path is the
*more honest / harder* bar — we control the trap and can tell exactly what was
caught vs missed, and we can iterate the system against it. Public benchmarks
"will likely be positive" by comparison and are easy to flatter ourselves with;
they come *after* we have internally established (or failed to establish) value.
If after all of it the system improves nothing, that null is the result — and
there may still be things worth mining from it.

**Parking lot — if we later pursue publication.** Test against EXISTING
benchmarks then (not build our own first): multi-hop (MuSiQue, FRAMES — used by
the equal-compute papers, directly comparable), SWE-bench-style defect tasks,
GAIA (long-horizon). "Propose our own benchmark" is a *secondary* contribution
only if no existing set isolates the **regime axis**.

**What is NOT novel (do not lead with it):** "roles/personas don't add accuracy"
— established (2311.10054, 2604.02460). **What is open / defensible:**
1. **The regime-transition result** — *at what task difficulty does scaffolding
   flip from form-only to substance-adding?*, measured under equal-compute. The
   field says benefits appear in harder regimes but has not mapped the transition.
2. **The self-ablation methodology** — a *living doctrine system measuring its own
   components* (closest neighbor: removal-based attribution, 2605.27621 — but on
   external MAS, not a self-applied doctrine layer).
3. **The form / substance / reliability decomposition** as distinct value axes
   (neighbor: accuracy-vs-ethics decoupling in 2605.27621).

**Honest risk (Skeptic):** the strongest neighbor papers are very recent (2604–
2605, i.e. weeks old). Novelty is real but the window is closing; a publication
path should move while (b) runs, not after. **Body-Input dependency:** whether to
actually pursue arxiv is a strategic call only the Body makes — this section is the
*map*, not a decision.

---

## First run — vertical tracer (mirrors D7)

1. **Hand-build one** regime-1 trap task (C3), self-contained (artifact pasted
   in-prompt). Validate difficulty (C2): bare arm N≥3, confirm it misses/glosses
   the trap at least intermittently. (Public-benchmark items = a later phase, per
   Body sequencing.)
2. Run the with-role arm (the role that *should* catch the trap), sentinel-gated,
   under C1 (length-matched bare). N≥3 each.
3. Score the three axes. If the design holds (clean catch-vs-miss signal, compute
   controlled), widen to a small trap battery; if confounded, fix design before
   widening.

## Non-goals / deferred
- No orchestrator automation until the battery earns it (default-simplicity; held
  since slice 1).
- No doctrine mutation in this run — output is a curation-ready package; Body
  judges (D1 autonomy boundary unchanged).
- Full-seed-minus-role (#3) and per-role blind-spot battery (#5) are later phases.
- Building a published benchmark is out of scope for (b) itself.

## Open questions / risks
- **Difficulty band is narrow** (C2): too easy = slice 1; too hard = nothing
  helps. Finding baseline-fragile tasks for a frontier model is the real work.
- **Equal-compute control design** (C1): length-matched filler vs output-cap —
  which is the fairer normalization? Resolve at tracer time.
- **Benchmark licensing / contamination**: a public benchmark may be in the
  model's training data — verify before trusting a "baseline fails" signal.

---
**Source:** Field map retrieved 2026-05-28 — arXiv 2311.10054, 2408.08631,
2604.02460, 2505.18286, 2605.27621, 2506.04133, 2604.05485. **Reinforced by:**
[[SOUL-F042]] convergence; slice-1 method findings. **Sub-class:** PROCEDURE.
**Adopted:** 2026-05-28 (draft). **Status:** active — Body signed off on regime
order, hand-built-first sequencing, run-(b)-first, and the Truth-seeking stance.
**Open question:** does a baseline-fragile difficulty band exist for this model
that is hard enough to break carefulness yet not so hard that no role helps?
