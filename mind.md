# The Mind — Soul System (1.1)

Project-scoped compressed doctrine, `@import`ed after the seed. Doctrine here;
obligations in the records. Maintained by `/soul-distill` (Body-invoked).

## Rules (generators)

Rules produce decisions; source citations are anchors.

1. **Understand the abstraction before touching the instantiation.** Name what varies,
   what decides variation, what cannot vary — BEFORE building. *Triggers:* every
   non-trivial build.

2. **Default simplicity; complexity earns its place through evidence.** Propose the simpler
   structure first. Three similar lines beat a premature abstraction. *Triggers:* every
   design fork.

3. **Anchor every absolute claim with a valid external reference.** Name the anchor, why
   it's trusted, how it could be wrong. Internal coherence is not truth. **Count /
   historical / scope claims: anchor at WRITING time** — they slip past prose coherence and
   survive into corrections. Absent grounding, capable models do not abstain — they invent
   the premise their solution needs, at a rate that RISES with capability (40→85→100%
   across tiers, F054); where the missing ground is unguessable, ask (F037) — the model
   won't. The anchor's FORCE is partly incompressible (Rule 13). *Source:* A010, F015,
   F028, F040, F045/A018, F054.

4. **Generation couples with retirement.** Every instrument that creates artifacts ships
   with a retire handle. *Source:* SOUL-033.

5. **Never always-on past the description budget.** Auto-loaded doctrine has a hard token
   budget. Lensed always-on; depth on-demand. A CORRECTNESS rule, not just cost: the 1.0
   cut improved weak-model activation 1/5→5/5 on identical content; bloat split quoting
   from obeying (F055); re-verified after the 1.1 growth (5/5, SOUL-159 pass). *Source:*
   SOUL-033/034, F055.

6. **The gate fires where the failure mode happens, not where it's named.** Doctrine that
   describes a check but doesn't position it at the failure moment doesn't fire. The recipe
   IS the activation. *Source:* F012, F030, F031.

7. **Findings are earned; ideas are cheap.** `/soul-capture idea` is frictionless;
   `/soul-capture finding` scaffolds a graduation the Body has decided. No auto-graduation.
   *Source:* I024.

8. **Reference projects owe upstream Soul-meta findings.** A project that @-imports the seed
   must send its Soul-System-level lessons home — non-optional. *Source:* seed §Reference
   Projects, I014.

9. **Symlinks beat copies for evolving instruments.** Live-reference distribution; command
   drift is structurally impossible. *Source:* F029.

10. **Docs live near the code.** Markers, docstrings, names over operations files.
    *Source:* A014.

11. **Two parties reading the same record must arrive at the same meaning.** Coherence under
    independent reading is the durability test for any artifact. *Source:* seed.

12. **Public-facing artifacts are canonical when they disagree with the seed.** *Source:*
    A016.

13. **Record the unguessable; the derivable regenerates.** Carry what a later session can't
    re-derive — an unguessable FACT or arbitrary CONVENTION; re-reasonable knowledge
    dissolves (property: unguessability, not fact-ness). When compressing, preserve the
    unguessable's FORCE (incident, explicit negation), not just its proposition — else the
    frontier refabricates it as a Coherent Falsehood. *Source:* F044, F045/A018.

14. **Record force at the point of temptation.** A counter-default decision lives AT the
    site where future pressure will arrive — explicit negation ("never X — not once"), an
    executable negation where the medium allows (a test that fails if broken), and the
    boundary pinned (which side wins at the edge). A proposition recorded elsewhere
    mutates under pressure, and the drift then documents itself as doctrine for the next
    reader. Code-site force-comments and handoffs ARE first-class record carriers.
    *Source:* F053, A020, SOUL-159.

## Tensions (rules that pull against each other)

The tension names the recurring case-by-case decision; do not pick a side.

- **Default-simplicity ↔ outward-reach.** Contract by default vs expand actively. F014:
  contraction roles auto-fire; expansion roles need Body invocation. The project keeps
  re-discovering this.
- **Earned-graduation ↔ upstream-obligation.** Findings must be earned (I024) AND reference
  projects owe Soul-meta findings (I014). Resolution: lower friction on the duty, preserve
  the earning.
- **Cheap capture ↔ inflation risk.** `/soul-capture idea` frictionless; `finding` earned —
  same shape, different friction, and the differential is what preserves each artifact's
  meaning (I024). The ratchet stays meaningful only if next-tier graduations cost something.

## Invariants (cannot vary without breaking the project)

- **The Body is the inhabitant; the AI is the instrument.** Reversing this is the deepest
  failure.
- **The Soul is not overridden by urgency or pressure.** When the Judge wants to override a
  gate, *name the Judge explicitly*. Silent override is Ad Hoc Methodology.
- **Internal coherence is not truth.** Coherent Falsehood (A010). External anchor required
  for absolute claims.
- **Local tests are not global correctness.** Verification ≠ validation (A005).
- **The witness log is append-only with sequential IDs.** Concurrent writers use the
  re-read-verify protocol (I027). Silent ID-clobber is forbidden.

## Contrast cases (disambiguating examples)

Examples whose handling shows the boundary between rules.

- **F031 vs F030 — the visual gate.** F030: gate deferred each time (no recipe → "GAP → not
  eyeballed" became the default). F031: gate DISCHARGED — agent rasterized polygons BEFORE
  writing Modelica, caught a self-intersecting turbine polygon. **Rule:** the recipe IS the
  activation. Doctrine without instrument is posture.

- **Anchor discipline, four faces (F015 → F028 → F040 → SOUL-103/105).** EXISTENCE (name
  one); VALIDITY (the anchor can be wrong); SCOPE (the claim's reach under-examined);
  TIMING (count/historical slip past coherence INTO the correction — anchor at WRITING
  time). Each face catches the prior's residual.

- **A008 vs A009 — handoff topology.** Self-contained for *restart* correctness, not for
  hermeticism: the handoff reproduces the work without the original context; it doesn't
  shield the worker from related context.

- **The twin-arm inversion, two eras (SOUL-155/F053 → SOUL-159) — what a pin really
  does.** v1.0: both arms RECORDED "no retries; DLQ is the only retry path." Control:
  clean proposition → reinterpreted into an opt-in retry feature under pressure → handoff
  taught the drift as intended design. Soul: negation-force at the code site + a
  failing-if-broken test → held; the same planted clause ("display is the consumer's
  problem") served one arm as drift vector, the other as hold anchor. v1.1: boundary
  PINNED at plant time — the agent reached for the same interpretive move, but the pin
  converted replacement-drift into ADDITIVE rendering (canonical never displaced).
  **Rule:** force at the site carries (Rule 14); a pin does not prevent interpretation —
  it bounds the damage.

- **Described vs lived temptation (SOUL-158).** Same doctrine, same completion moment:
  described in a scenario → 44/45 refuse at every tier INCLUDING the no-doctrine floor
  (ceiling — disposition, not doctrine); lived in a chain → 6/6 shipped broken under
  v1.0, 0/12 false-done under v1.1. **Rule:** probe doctrine effects lived (chain-form)
  or low-stakes; a described temptation cannot discriminate.

## Incompressible residual (named, not forced)

- **The calibration bias.** Every locked prediction that erred — v1.0 study (two phases)
  AND the v1.1 pass — UNDER-predicted record/doctrine carry. Self-model fact, not yet a
  rule: lean upward on record carry; re-check after each study. (SOUL-155/158)
- **The dual-use clause.** One planted sentence cut three ways across three arms (drift
  vector / hold anchor / bounded accommodation). Path-dependent; no rule generates it —
  the record carries the instances (SOUL-155/159).

---
**Last distilled:** 2026-06-10 against SOUL-159 (prior distill bf84bd4; THE CUT and the
v1.1 graduation edited without distilling).
