# The Mind — Soul System

This is the project-specific compressed-rules artifact for the Soul System repo
(per the lens-layer architecture in `docs/specs/2026-05-26-the-mind-design.md`).
Always-on (loaded after the seed via `@mind.md` in `CLAUDE.md`). Maintained by
the Distiller (`/soul-distill`). Holds **doctrine** — rules that apply across
contexts; specific obligations stay in the records. When you need an obligation-
specific fact (a lifecycle, an upstream route, a particular witness), consult the
cited record. The Mind names the rule; the record carries the specifics.

## Rules (generators)

A rule produces decisions, not a description of one. If removing it would change
what the project does next, it belongs here. Source citations are anchors.

1. **Understand the abstraction before touching the instantiation.** Name what
   varies, what decides variation, what cannot vary — BEFORE building. *Source:*
   First Principle, `operations/CLAUDE.md`. *Triggers:* every non-trivial build.

2. **Default simplicity; complexity earns its place through evidence.** Propose
   the simpler structure first. Three similar lines beat a premature abstraction.
   *Source:* `feedback_default_simplicity`. *Triggers:* every design fork.

3. **Anchor every absolute claim with a valid external reference.** Name the
   anchor, name *why* it's trusted, and *how* it could be wrong. Internal
   coherence is not truth (Coherent Falsehood). *Source:* A010, F015, F028, F040.

4. **Generation couples with retirement.** Every instrument that creates
   artifacts (skills, findings, ideas, amendments) ships with a retire handle.
   *Source:* SOUL-033; `/soul-skill`'s `soul-status` field.

5. **Never always-on past the description budget.** Auto-loaded doctrine has a
   hard token budget. Lensed always-on; depth on-demand. *Source:* SOUL-033/034
   — the @-import was dropped, gates survived, expansion didn't.

6. **The gate fires where the failure mode happens, not where it's named.**
   Doctrine that describes a check but doesn't position the check at the failure
   moment doesn't fire. The recipe IS the activation. *Source:* F012, F030, F031.

7. **Findings are earned; ideas are cheap.** `/soul-idea` is frictionless capture
   (forward possibilities); `/soul-finding` is a scaffolder *over a graduation the
   Body has decided* (backward witness → finding). No auto-graduation. *Source:*
   I024 resolution.

8. **Reference projects owe upstream Soul-meta findings.** A project that
   @-imports the seed must send its Soul-System-level lessons home — non-optional.
   *Source:* seed §Reference Projects, I014.

9. **Symlinks beat copies for evolving instruments.** Live-reference distribution;
   command drift is structurally impossible. *Source:* F029.

10. **Docs live near the code.** Structural markers, docstrings, names over
    operations files. Operations files must earn their keep. *Source:*
    `feedback_docs_live_near_code`; A014 (sub-class footer).

11. **Two parties reading the same record must arrive at the same meaning.**
    Coherence under independent reading is the durability test for any artifact.
    *Source:* `operations/CLAUDE.md` opening.

## Tensions (rules that pull against each other)

Knowing the *tension* is more useful than picking a side; the tension names a
recurring decision the project has to make case-by-case.

- **Default-simplicity ↔ outward-reach.** Contract by default vs expand actively.
  F014 lives here: contraction roles auto-fire (Accountant, Skeptic, Steward),
  expansion roles need Body invocation. The project keeps re-discovering this.

- **Earned-graduation ↔ upstream-obligation.** Findings must be earned
  (anti-inflation, I024) AND reference projects owe Soul-meta findings upstream
  (I014). Resolution shape: lower friction on the duty (a scaffolder), preserve
  the earning (Body still decides the graduation).

- **Self-contained handoff ↔ context isolation.** A handoff is self-contained for
  restart correctness, NOT for hermetic context. Resolution: A009 refined A008.

- **Activation in code ↔ activation in doctrine.** A gate's text presence ≠ its
  firing. The hook + symlinked commands are the activation; doctrine alone isn't.
  *Source:* F012 family. Open: F014 has no obvious instrument.

- **Cheap capture ↔ inflation risk.** `/soul-idea` cheap; `/soul-witness`
  deferred; `/soul-finding` is a scaffolder, not an inbox. The ratchet stays
  meaningful only if next-tier graduations cost something.

- **Doctrine completeness ↔ description budget.** The seed must orient new agents
  AND stay under the always-on budget. SOUL-033 resolved with lensed roles +
  on-demand depth.

## Invariants (cannot vary without breaking the project)

- **The Body is the inhabitant; the AI is the instrument.** The Body bears
  responsibility; the AI is the tool. Reversing this is the deepest failure.

- **The Soul is not overridden by urgency or pressure.** When the Judge wants to
  override a gate, *name the Judge explicitly*. Silent override is Ad Hoc
  Methodology wearing autonomy's mask.

- **Internal coherence is not truth.** Coherent Falsehood (A010) — a claim
  passing every internal check while false against reality. External anchor
  required for absolute claims.

- **Local tests are not global correctness.** Verification ≠ validation (A005).
  The global invariant the WHOLE must satisfy is the check that matters.

- **The witness log is append-only with sequential IDs.** Concurrent writers must
  use the re-read-verify protocol (I027). Silent ID-clobber is forbidden.

## Contrast cases (disambiguating examples)

A small set of examples whose handling shows the boundary between rules. These
are the seed examples for the project's own continued judgment.

- **F031 vs F030 — the visual gate.** F030: gate fired ~3× and deferred each
  time (no recipe → "GAP → not eyeballed" became the default). F031: gate
  DISCHARGED — agent rasterized polygons BEFORE writing Modelica, caught a
  self-intersecting turbine polygon. **Disambiguating rule:** the recipe IS the
  activation mechanism. Without a one-step capture method, visual obligation
  reverts to deferral. Doctrine without instrument is posture.

- **F015 → F028 → F040 — three layers of anchor discipline.** F015 secured
  EXISTENCE (must name one); F028 secured VALIDITY (the anchor itself can be
  wrong); F040 specializes both for RETIRE claims (grep with wrong scope is
  an INVALID anchor). Each layer catches the prior's residual.

- **A008 vs A009 — handoff topology.** A008 prescribed hermetic context for
  subagents (FANOUT). A009 refined: self-contained for *restart* correctness,
  not for hermeticism. The handoff must reproduce the work without the original
  context; it doesn't shield the worker from related context.

- **`/soul-idea` vs `/soul-finding` — the capture ratchet.** Same shape
  (append-record), different friction. Idea: frictionless. Finding: requires
  Body's explicit graduation. The friction differential preserves what each
  artifact *means*.

- **Seed (~260 lines, always-on) vs `philosophy/the-soul.md` (~710 lines,
  on-demand).** Same doctrine; different position in the description budget.
  SOUL-033 evidence: gates survive context reduction; expansion/breadth doesn't.
  So gates always-on, depth on-demand.

## Incompressible residual (named, not forced)

Some accumulated knowledge doesn't reduce to rules — try to compress it and you
lose load-bearing information. Honesty about the residual is part of the Mind's
discipline; force-fitting everything into rules is itself the failure mode.

- **The specific dogfood histories.** REF-09, REF-04, REF-03,
  REF-01, blog, REF-02. Each is a path-dependent evidence set. The Mind
  can encode their *lessons* (rules above) but not their *particulars*. For
  particulars, the witness log and findings remain the source of truth.

- **The version trajectory.** 0.1.0 → 0.5.0 is a history, not a rule-set. The
  *why* of each version is encoded above; the order and timing aren't.

- **The Body's specific user-memory.** Drift-correction notes, individual
  preferences — live in `/home/fig/.claude/.../memory/` and are valuable but
  not Soul-internal rules.

- **Active uncertainty.** F014 activation, I011 token economics — open
  questions where no rule has crystallized. Listing them as rules would be
  false certainty. They live in `findings/open/` and `ideas.md` where their
  open-ness is honest.

- **The Council role descriptions.** The roles ARE the rules' executors but
  their full character (Archaeologist vs Steward tension; Skeptic vs Craftsman)
  doesn't reduce to one-liners without losing the *flavor* that makes them
  invocable. They stay in the seed and `the-soul.md`.

---
**Last distilled:** 2026-05-27 (refresh after the Soul-Console v1 audit arc; A014/A015/F040 absorbed; three-layer anchor pattern named; I026 residual pruned post-Mind-ship; witness SOUL-095).
