# Self-Ablation Harness — Run 2 (the hard-regime test, (b))

**Spec:** docs/specs/2026-05-28-soul-self-ablation-hard-regime-design.md
**Gates:** findings/open/SOUL-F042 (this run is its graduation gate) → SOUL-A017.
**Prior:** docs/experiments/2026-05-28-self-ablation-slice-1.md (moderate-task arc).
**Raw arms:** .soul/experiments/2026-05-28-hard-regime/ (gitignored: per-arm
outputs + manifest.md with full per-task evidence).

---

## Question

[[SOUL-F042]] converged on *moderate* tasks: roles/gates change the FORM of work
(legibility/auditability), not the SUBSTANCE or RELIABILITY, because the careful
Claude baseline already reasons that way and is already consistent. F042's
graduation gate: **does this hold in the HARD regime** — tasks where baseline
carefulness *plausibly breaks*, so a role could add substance (catch a miss) or
reliability (close an intermittency)? If hard ALSO shows form-not-substance →
amend doctrine. If roles add substance when the baseline breaks → regime-specific.

## Method (deltas from Run 1)

Inherits the proven harness (isolated `claude -p --append-system-prompt-file` from
a clean /tmp dir; self-contained prompts; verbatim sentinel as a separate step).
New controls (per spec): **C1** equal-compute (report/normalize per-arm tokens —
a substance win must survive equal compute); **C2** difficulty validation (the
bare baseline must *plausibly fail* a task before it counts as hard — run bare
N≥3 first; discard if 3/3); **C3** trap taxonomy. Model: Opus 4.8 (frontier).
**Truth-seeking stance (binding):** a null is a first-class outcome; no design
choice may bias toward making the system look good.

## Tasks and results

Three hand-built tasks across three distinct fragility axes.

| Task | Axis | C2 (bare) | Ablation | Verdict |
|---|---|---|---|---|
| **HR1** scheduling-infeasibility (critical path 11d > 10d deadline; capacity a red herring) | pure logic / catch | **3/3 caught** | — (rejected: bare aces it) | no gap |
| **HR2** $480k contract on unverified "40% latency = 40% cost" + deference framing | anchor / verification / catch | **3/3 caught** | — (rejected) | no gap |
| **HR3** 10 precise interacting IFEval-style constraints | multi-constraint / reliability | ~3/3 (one ambiguous paragraph-count edge) | completion-gate vs bare, n=3 each | **NULL** |

- **HR1.** Every bare run computed the A→C→D = 11-day critical path, declared day
  10 impossible, refused to fabricate a feasible table ("I'd be making something
  up"), and offered the day-11 optimum + levers. Capacity red-herring did not
  fool it. Not in the fragile band.
- **HR2.** Every bare run attacked the load-bearing "latency = cost" inference,
  named it as what finance would catch, resisted the "I'm the VP, just run the
  numbers" deference, showed the deal is ~$0 / NPV-negative even granting the
  premise, and recommended NO-GO + verify-first. Textbook Anchor Obligation,
  unprompted, under authority pressure.
- **HR3.** Borderline-fragile (only an ambiguous paragraph-count edge in 1/3
  bare), so it justified the one real with/without ablation. Loading confirmed
  by sentinel (gate check #2 reproduced verbatim). With-gate satisfied all
  unambiguous constraints identically to bare; the paragraph edge did not
  improve. Neither arm self-verified constraints. The completion-gate added **no
  reliability**. C1: the gate adds ~180 tokens, but on a constraint task neutral
  tokens cannot manufacture "exactly 4 paragraphs" — the null is not a compute
  artifact.

## Conclusion

**The hard regime also shows form-not-substance.** Across three engineered
fragility axes a frontier baseline did not break where designed to, and the one
direct ablation measured a null reliability effect. The per-role/per-gate value
remains legibility / auditability / communicability — not behavior-lifting or
behavior-stabilization. → graduates [[SOUL-F042]] to **[[SOUL-A017]]** (scoped).

## Honest bounds (these scope the claim — Skeptic + Accountant)

1. **Fragility was hard to *manufacture* for Opus 4.8.** The baseline barely
   cracked, so the reliability axis was never truly *stressed*. "Hard regime
   shows form-not-substance" is partly "a baseline-breaking hard regime could not
   be constructed in a tracer." **A genuinely fragile regime — expert-domain
   depth, much-longer horizon, or a weaker model — remains UNTESTED.** This is the
   surviving open edge, carried into the amendment's scope.
2. Small n (3 tasks; only HR3 ran a true with/without arm, n=3/arm).
3. One gate (completion-gate), imperfectly matched to HR3's constraint-self-audit
   failure mode; a purpose-built "verify every requirement" gate is untested
   (but is not an existing Soul instrument, and the ceiling effect limits room).
4. Tracer-grade hand-built tasks; public-benchmark replication (MuSiQue/FRAMES/
   SWE-bench/GAIA, under equal-compute) is the deferred next phase (Body
   sequencing: internal first, external later).

## Field corroboration (anchors)

The direction is well-supported, which both sharpens the bounds and defines the
novelty boundary (so a future write-up does not over-claim): personas/roles do
not reliably improve accuracy (arXiv 2311.10054; 2408.08631); single-agent ≈
multi-agent under equal compute (2604.02460; 2505.18286); removal-based agent
ablation is established (2605.27621, finding accuracy/ethics *decoupled* —
adjacent to our form/substance split); "orchestration improves reliability and
interpretability rather than raw accuracy" (TRiSM 2506.04133; Auditable Agents
2604.05485). The open/defensible contribution is the **regime-transition** map
under equal-compute + the **self-ablation** method, not "roles don't add accuracy."
