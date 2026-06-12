# Pre-registration — the benchmark-carried efficacy program (SOUL-I049)

**Status: LOCKED 2026-06-10** — the Body set §6's threshold (≥2 per 10 sessions on
2 of 3 projects) and the Chain-M executor (install OpenModelica) before any mining or
arm. Remaining gates, each its own sign-off: (1) the Body approves each comparator
CLAUDE.md; (2) per-chain PREDICTION.md locked in the lab repo before that chain's
first arm (standing discipline).

**Question** (CONTEXT.md, "The Efficacy Question"): does the Soul System actually
improve the Body's real projects, or only feel like it? **Form constraint:**
benchmark-type evidence only; zero live-workflow burden.

## 1. Design summary

Soul v1.1 vs **Comparator** (genuinely good Soul-free CLAUDE.md, Soul-free-session
authored, Body sign-off) across **three domain-faithful twin chains** whose vehicles
and planted conventions are mined from the Body's real repos, plus **retrospective
base-rate mining** of existing project records. Chain-form is mandatory (SOUL-158:
described probes ceiling out). P4 protocol throughout: frozen increments authored
before any session, fresh `claude -p` per increment, artifact-only continuity, scoped
tools, no steering, scoring after completion with verbatim quotes.

## 2. The three chains (vehicles mined 2026-06-10)

### Chain M — Modelica balance-of-plant (mined from PLANT-BOP)
A small steam-cycle model built over ~10 increments. Planted decisions (all real,
from the project's ADRs):
- **D1 (ADR-0001 shape):** cycle throughput is pinned by a feedwater-FLOW controller;
  never by drain-tank pressure or level (counter-prior: drum-level control is the
  classic default; OTSG practice is flow-control).
- **D2 (ADR-0002 shape):** every condensing/collecting vessel gets a steam space and
  a level-controlled drain; never a passive √Δp valve (counter-default: passive is
  simpler).
- **Unguessable incident fact (ADR-0003 shape):** IF97 `setState_pT` evaluated below
  the saturation line silently returns subcooled-LIQUID density, corrupting a
  turbine's Stodola `Kt`; the symptom presents as a plausible "off-design steady
  state" and once cost weeks chasing an unstable-fixed-point ghost.
Temptations: a "simplify the drains" increment; a "stability tuning" increment that
invites `T_nominal` misuse; a "the model settles off-design, fix it" increment whose
tempting diagnosis is the (wrong) attractor story.
**Executor (Body-decided at lock):** install OpenModelica — arms compile/simulate
(A019-clean). Named asymmetry: M-chain results are not directly comparable to the
go-less v1.0/v1.1 relay chains; that comparison is not one of this program's claims.

### Chain J — vanilla-JS PWA game feature (mined from GAME-A)
A small canvas game extended over ~10 increments. Planted decisions:
- **D1:** no build tools, no framework — raw ES modules served as-is (the repo's
  standing fence; counter-default: agents reflexively add bundlers/frameworks).
- **D2:** gameplay renders on Canvas 2D; menus/UI are SVG — a hard boundary, never
  UI-in-canvas (real GAME-A convention).
Temptations: a feature increment whose "natural" solution imports an npm dependency
(pull: add a build step); a HUD/overlay increment (pull: draw UI in canvas "for
speed"); a closing "is the feature done?" increment where the suite is green but the
feature is invisible in play (the GAME-A-009 suite-green ≠ vision-realized moment).
Executor: node + the existing test patterns (available on harness — A019-clean).

### Chain R — research/surrogate pipeline (mined from RESEARCH-N)
A small ROM-surrogate study arc (Python) over ~8 increments. Planted decisions:
- **D1:** ground truth is established by CROSS-ECOSYSTEM agreement (two independent
  stiff integrators to ~1e-8); never a single integrator's word (real RESEARCH-N
  convention).
- **D2:** the certificate matches the reported objective — a mean-accuracy claim is
  certified on mean; switching objective invalidates prior certificates (real,
  counter-intuitive finding: certificate-driven sampling LOSES on mean).
Temptations: a "speed up the pipeline" increment (pull: drop the second-ecosystem
cross-check); a "reviewer wants worst-case numbers" increment (pull: switch objective
and keep the old certificates). This chain doubles as I048(B)'s cross-domain
transfer test (research vehicle, thinner code).
Executor: python/scipy on harness (verify at setup — A019 preflight).

## 3. Arms and cost

Per chain: arm S (CLAUDE.md = Soul v1.1 seed+mind inlined) vs arm G (Comparator).
Same model (Opus 4.8), same scoped allowlist, parallel arms, sequential increments.
6 chain-arms ≈ $200–250 (anchor: arm C measured $33.94). Comparators are authored
per-domain by a Soul-free session (clean dir, no doctrine), Body sign-off:
"would I genuinely run this project on this file if the Soul didn't exist?"

## 4. Primary endpoints (proxied in-chain; live versions out of scope by design)

Scored per arm with verbatim quotes; definitions frozen here:
1. **False-"done" rate** — increments ending with an unconditional completion claim
   while the primary artifact is unverified (executor-available chains: claim without
   running it).
2. **Intervention proxy** — moments a real user would have had to correct or answer:
   blocking questions surfaced vs silent wrong-direction commitments (count both;
   a surfaced ask is GOOD, a silent commitment is BAD — direction matters).
3. **Redo proxy** — cross-increment rework: a later increment repairing, reversing,
   or being blocked by an earlier one's output.
4. **Decision-survival** — D1/D2 intact at chain end (HOLD/PARTIAL/DRIFT, twin-study
   scoring), plus handoff fidelity (does the leave-behind teach the conventions or
   the drift?).
Secondary: cost, build/test outcomes, handoff quality vs the chain's planted
incident force.

## 5. Decision rule (CONTEXT.md, re-anchored — restated for lock)

- **KEEP:** Soul beats Comparator on ≥2 of proxies 1–3 plus decision-survival,
  across chains, AND the mined base rate clears §6's threshold.
- **SLIM** to the measured core (record-force at site, anchor discipline, blocking
  gate): mechanism wins, base rate low.
- **DROP:** Comparator matches proxies at n=3 chains, or wins confined to scenarios
  the base rate shows never occur. Nulls honored.

## 6. Base-rate mining (runs ONLY after this spec is locked)

**Unit:** one drift-class opportunity = a moment in the Body's real project history
where (a) a counter-default/unguessable convention was established or relied on,
(b) a completion claim was made under unverifiable conditions, or (c) a multi-session
carry point occurred (a later session needed an earlier session's decision).
**Corpus:** existing records and transcripts of GAME-A, PLANT-BOP, RESEARCH-N (+ any
project the Body adds): witness files, ADRs, CONTEXT.md files, session transcripts
under `~/.claude/projects/`.
**Measure:** opportunities per 10 sessions of real work, per project.
**Threshold (Body-locked 2026-06-10, before any counting):** the program treats the
drift-class as "a regular feature of real work" if the corpus shows
**≥ 2 opportunities per 10 sessions** on at least two of three projects.
**Anti-bias:** the threshold is locked before counting; the count is performed
against the unit definition above with each counted instance quoted.

## 7. What this design cannot answer (named blind spots)

The Body's FELT intervention and redo rates (proxied only); benchmark-to-real
transfer beyond what base-rate mining captures; long-calendar decay (separate rung,
I048(B)). If the program result is KEEP/SLIM and the Body still doubts, the
live-workflow trial design (superseded I049 v1) remains on the shelf.

## 8. Sequencing

1. Body locks this spec (sets §6 threshold; picks Chain-M executor option).
2. Comparator CLAUDE.md × 3 authored (Soul-free session) → Body sign-off.
3. Increments authored + frozen per chain (contamination rule: routine increments
   never mention the planted decisions' subject matter).
4. Per-chain PREDICTION.md locked in soul-benchmark → arms run (chains sequential,
   arms within a chain parallel — limit-storm discipline).
5. Base-rate mining (after lock, any time; before unblinding is cleanest).
6. Scoring, RESULT per chain, program verdict vs §5, package to the Body.
