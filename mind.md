# The Mind — Soul System

Project-scoped compressed-rules artifact (lens-layer; spec at
`docs/specs/2026-05-26-the-mind-design.md`). Always-on via `@mind.md`;
maintained by `/soul-distill`. Doctrine here; obligations in the records.

## Rules (generators)

Rules produce decisions; source citations are anchors.

1. **Understand the abstraction before touching the instantiation.** Name what
   varies, what decides variation, what cannot vary — BEFORE building. *Source:*
   First Principle, `operations/CLAUDE.md`. *Triggers:* every non-trivial build.

2. **Default simplicity; complexity earns its place through evidence.** Propose
   the simpler structure first. Three similar lines beat a premature abstraction.
   *Source:* `feedback_default_simplicity`. *Triggers:* every design fork.

3. **Anchor every absolute claim with a valid external reference.** Name the
   anchor, why it's trusted, how it could be wrong. Internal coherence is not
   truth. **Count / historical / scope claims: anchor at WRITING time, not just
   review** — a scope claim ("which files, which parse, the N sites that matter")
   is a count-like claim that slips past prose coherence and survives into
   corrections. *Source:* A010, F015, F028, F040, SOUL-103, SOUL-104, SOUL-105.

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

10. **Docs live near the code.** Markers, docstrings, names over operations
    files. *Source:* `feedback_docs_live_near_code`; A014.

11. **Two parties reading the same record must arrive at the same meaning.**
    Coherence under independent reading is the durability test for any artifact.
    *Source:* `operations/CLAUDE.md` opening.

12. **Public-facing artifacts are canonical when they disagree with the seed.**
    The seed implements public artifacts (README, AGENTS.md); when divergence
    is found, the public artifact wins. *Source:* A016, SOUL-099.

## Tensions (rules that pull against each other)

The tension names the recurring case-by-case decision; do not pick a side.

- **Default-simplicity ↔ outward-reach.** Contract by default vs expand actively.
  F014: contraction roles auto-fire (Accountant, Skeptic, Steward), expansion
  roles need Body invocation. The project keeps re-discovering this.

- **Earned-graduation ↔ upstream-obligation.** Findings must be earned (I024)
  AND reference projects owe Soul-meta findings upstream (I014). Resolution:
  lower friction on the duty, preserve the earning (Body still decides).

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

Examples whose handling shows the boundary between rules.

- **F031 vs F030 — the visual gate.** F030: gate fired ~3× and deferred each
  time (no recipe → "GAP → not eyeballed" became the default). F031: gate
  DISCHARGED — agent rasterized polygons BEFORE writing Modelica, caught a
  self-intersecting turbine polygon. **Disambiguating rule:** the recipe IS the
  activation mechanism. Doctrine without instrument is posture.

- **Anchor discipline, four faces (F015 → F028 → F040 → SOUL-103/104/105).**
  EXISTENCE (must name one — F015); VALIDITY (the anchor itself can be wrong —
  F028); SCOPE (the claim's reach can be under-examined — F040 wrong-scope grep;
  SOUL-104 audit missed docs/specs/; SOUL-105 a scope-slip INSIDE a slip-
  diagnosis); TIMING (count / historical / scope claims slip past prose coherence
  and survive INTO the correction — anchor at WRITING time; SOUL-099 "SECOND"→
  FOURTH /soul-council count, SOUL-103). Each face catches the prior's residual.

- **A008 vs A009 — handoff topology.** A008 prescribed hermetic context for
  subagents (FANOUT). A009 refined: self-contained for *restart* correctness,
  not for hermeticism. The handoff must reproduce the work without the original
  context; it doesn't shield the worker from related context.

- **`/soul-idea` vs `/soul-finding` — the capture ratchet.** Same shape
  (append-record), different friction. Idea: frictionless. Finding: requires
  Body's explicit graduation. The friction differential preserves what each
  artifact *means*.

- **Seed (~263 lines, always-on) vs `philosophy/the-soul.md` (~710 lines,
  on-demand).** Same doctrine; different position in the description budget.
  SOUL-033 evidence: gates survive context reduction; expansion/breadth doesn't.

## Incompressible residual (named, not forced)

Knowledge that doesn't reduce to rules; force-fit is the failure mode.

- **The specific dogfood histories.** Each registered project (see `registry/`)
  is a path-dependent evidence set; the Mind encodes their *lessons* (rules
  above), not their *particulars*. Sources of truth: `registry/`, `witness.md`,
  `findings/`.

- **The version trajectory.** History, not rules. The *why* is in the rules
  above; the order and timing aren't.

- **The Body's specific user-memory.** Drift-correction notes; lives in
  `~/.claude/.../memory/`; not Soul-internal.

- **Active uncertainty.** F014 activation, I011 token economics. No rule has
  crystallized; listing them as rules would be false certainty. `findings/open/`
  + `ideas.md` carry the open-ness.

- **The Council role descriptions.** The roles ARE the rules' executors but
  their full character (Archaeologist vs Steward tension; Skeptic vs Craftsman)
  doesn't reduce to one-liners without losing the *flavor* that makes them
  invocable. They stay in the seed and `the-soul.md`.

---
**Last distilled:** 2026-05-28 (light refresh, SOUL-104→106 — Rule 3 timing
clause extended to SCOPE claims; anchor-discipline + SOUL-099 count-slip cases
merged into one four-face case (shrinks); gap-only review rule deferred at
N=2. Prior: 2026-05-27, SOUL-098→103).
