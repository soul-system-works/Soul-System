# The Mind — design

**Date:** 2026-05-26
**Status:** draft (sections approved in brainstorm; Body to review the written spec)
**Ideas:** SOUL-I026 (the proposal). Related: SOUL-I011 (experiment harness),
SOUL-033/034 (description budget), SOUL-F014 (expansion gap), SOUL-I025 (GUI access).
**Tier 1 artifact:** `docs/experiments/2026-05-26-mind-tier1-candidate.md`.
**Tier 2 evidence:** captured inline in this spec (held-out A/B on `/soul-witness?`).

---

## Problem (two levels)

**Immediate.** Long Soul sessions accumulate declarative noise — facts, summaries,
descriptions that degrade through paraphrase. There is no project-scoped artifact
that holds the **rules that would generate** the project's recurring decisions,
distinct from the records that store them. A new session orients by reading
witness/findings, which carries cost and is subject to drift.

**Larger.** This is the **information-theory question turned on the Soul itself**:
the best representation of something is not a description but the shortest set of
rules that would reproduce it (Kolmogorov complexity / MDL). Memorized answers
degrade; *understanding* — encoded as generators — reproduces. The Soul System
already does this at the system level (each amendment IS a compressed rule
distilled from accumulated witness evidence). The Mind asks whether the same
witness → rule loop, applied **per-project**, beats the drift of long sessions.

These two levels are coherent: the immediate need (compressed orientation
artifact) IS an instance of the larger principle (rules > descriptions).

---

## Abstraction layer

- **What varies:** the Mind's content, the cadence of distillation, the budget,
  the schema's evolution.
- **What decides variation:** empirical evidence (Tier 1 artifact + Tier 2 A/B
  + ongoing deployment validation). Not picked from above.
- **What cannot vary (the invariants):**
  1. **Necessity is established before instrument.** Tier 1 (hand-craft) + Tier 2
     (A/B) precede Tier 3 (build) — already executed in the brainstorm and the
     evidence ratified the lens-layer design.
  2. **The Mind is a lens, not a replacement.** Doctrine compresses to the Mind;
     specific obligations stay in the records. This boundary is the difference
     between the Mind succeeding and the Mind drifting into being a renamed
     record. Tier 2 evidence is the anchor for this invariant.
  3. **Generation couples with retirement.** The Distiller ships with the four
     shrinkage-invariant checks AND the six failure-mode guards from creation.
     Default-deny growth.
  4. **The Body owns curation.** `/soul-distill` produces a draft Mind update;
     never auto-commits. Mirrors `/soul-skill`'s draft-for-curation pattern.
  5. **Reproduction is the success measure.** The Mind is *for* enabling agents to
     produce coherent next-work reading it alone (+ seed). If that test fails, no
     amount of internal coherence saves the design (anti-Coherent-Falsehood A010).

---

## Tier 2 evidence (the empirical floor)

Held-out A/B run during the brainstorm (witness entry pending). Question: *should
`/soul-witness` be built?* Two subagents, identical prompt, identical response
template, both inheriting the @-imported seed; difference was the additional
context:

| Dimension | Arm A (full record) | Arm B (Mind-only) |
|---|---|---|
| Tokens | 42,476 | 25,072 (**~41% cheaper**) |
| Tool uses | 12 (record reads) | 1 (the Mind file) |
| Wall clock | 68 sec | 19 sec |
| Direction | Conditional YES (scaffolder) | Conditional NO (case unearned) |
| Reasoning surface | Specific IDs (SOUL-067, A001, I014/I023) | Mind rules + tensions + contrast case |

**The arms disagreed on direction. That disagreement is the most informative
datum.** Arm A pulled obligation-specific facts (the SOUL-A001 witness lifecycle,
the SOUL-I014 upstream-route obligation) that genuinely live outside the Mind's
four buckets — they're in the incompressible residual. Arm B leaned on
doctrinal rules + tensions and arrived at the Steward-flavored answer.

**Verdict.** The Mind handles doctrinal reasoning faithfully and ~41% cheaper.
It does NOT handle obligation-specific reasoning. The Mind is therefore a
**third layer** in the doctrine stack, between the seed and the records — not a
replacement for either.

---

## Architecture — the lens layer

```
SEED (operations/CLAUDE.md, ~200 lines, ALWAYS-ON)
    Universal Soul doctrine: First Principle, gates, Council roles, primary
    failure modes. Same for every adopting project.
                          ↓ @-import in project CLAUDE.md
MIND (mind.md at project root, ≤200 lines target, ALWAYS-ON) — NEW
    Project-specific compressed rules + tensions + invariants + contrast cases,
    + incompressible residual. Distilled from this project's accumulated record.
    Maintained by the Distiller. Test: produces coherent doctrinal reasoning
    from itself + seed alone.
                          ↓ reference, do not duplicate
RECORDS (witness.md, ideas.md, findings/, amendments/)
    Full project history. ON-DEMAND. Source of truth for specific obligations
    the Mind cannot compress without becoming a renamed record (SOUL-A001
    lifecycle, SOUL-I014 upstream route, etc. — Tier 2 evidence).
```

**The doctrine-vs-obligation boundary:** the Mind holds rules that apply across
contexts. Obligations — specific commitments at specific times — stay in the
records. When a Mind-reading agent hits an obligation-specific question, the
protocol is "go read `<specific record>`" — same way the seed says "consult
`the-soul.md` on demand."

**How the Mind references records.** Mind entries cite anchors inline by ID
(e.g., "the recipe IS the activation mechanism — F031 vs F030"). An agent
reading the Mind that needs more than the anchor's headline knows where to look.
This is the practical handle for the doctrine→obligation pivot: the Mind names
the rule; the cited record carries the specifics.

---

## File location and name

- **Name:** `mind.md` (matches `witness.md` / `ideas.md` — simple noun, root location).
- **Location:** project root.
- **Import:** project `CLAUDE.md` adds `@mind.md` after `@operations/CLAUDE.md`.
  Optional — projects that don't want a Mind don't add the import.
- **Soul System repo itself:** same. `mind.md` at repo root. Seeded from the
  Tier 1 candidate, pruned of inspection-only sections.

---

## Distiller cadence

**On-demand MVP** via `/soul-distill`. Body invokes when the accumulating record
warrants compression. Rule #2 (default simplicity) and Rule #4
(generation-couples-with-retirement) argue against auto-fire until manual cadence
proves insufficient.

**Deferred future ratchets** (named, not built):
- *Session-end hook* — fires automatically on Stop. Risk: churn the Mind on every
  session; the cadence should match real rule-emergence, not session boundaries.
- *Threshold-triggered* — fires when witness.md grows past N lines since last
  distill. Threshold needs to be earned empirically, not picked.

---

## Schema

```
# mind.md

[Header — one paragraph: what this is, project name, last-distilled stamp]

## Rules (generators) — items each citing at least one anchor
## Tensions (rules that pull against each other) — named pulls, with the rule
   pair they connect
## Invariants (cannot vary without breaking the project) — non-negotiables
## Contrast cases (disambiguating examples) — the seed examples that resolve
   where rules collide
## Incompressible residual (named, not forced) — what doesn't fit the four
   buckets, kept honest

---
**Last distilled:** YYYY-MM-DD against witness tail / commit SHA
```

The residual bucket is **load-bearing** — Tier 2 evidence showed that without it,
the Mind would either bloat (force-fitting) or lose honesty. Naming the residual
is part of the schema, not optional.

The Tier-1 self-test (the three diagnostic questions) moves OUT of the artifact
INTO the `/soul-distill` command — the Distiller runs the self-check after each
distill; the artifact stays pure rules.

---

## Shrinkage invariant — the Distiller's mechanical checks

Every fire, before producing the draft:

1. **Hard line budget.** Target ≤ 200 lines; hard cap 300. Anchored to the seed's
   footprint — a second artifact of that size is the most the always-on budget
   tolerates before SOUL-033 starts biting.
2. **Anchor requirement.** Every entry in Rules / Tensions / Invariants /
   Contrast cases must cite at least one anchor (witness ID, finding, amendment,
   user-memory). An anchorless entry is a description, not a generator. Prune.
3. **Generator test.** Each Rule answers "what decision does this produce?"
   Phrase-check: "X is true" = description (prune); "do Y when Z" or "prefer Y
   over Z because…" = generator (keep).
4. **Growth check.** Compare Mind size to the previous distill. **Mind must
   shrink or stay the same.** Growth = Distiller failed its job; flag to Body
   for explicit sign-off ("I am consciously expanding because…"). Default-deny.

A deeper test — **reproduction-fidelity sampling** — deferred to deployment: take
a real recent decision, ask whether the Mind alone reproduces direction. Used as
a quality signal over time, not a per-distill gate.

---

## Failure-mode guards

| Failure | Guard |
|---|---|
| Drift into summary (I026 #4) | Section-5 growth check; default-deny growth |
| Force-fit residual (Tier 1 risk) | Residual bucket required in schema. Zero residual = suspicious; Distiller must justify or admit force-fit |
| Renamed seed (Tier 1 fail) | Per-distill check: "what's in `mind.md` that's NOT in `operations/CLAUDE.md`?" Trivial answer → Mind redundant → **Steward retires** |
| Renamed CLAUDE.md (Steward concern) | Boundary rule: CLAUDE.md is *authored* (what the project is, how agents work). Mind is *distilled* (rules the project discovered about itself from accumulated record). Distinct sources |
| Doctrine-obligation collapse (Tier 2 evidence) | Distiller asks per-entry: "rule (across contexts) or obligation (specific commitment, specific time)?" Only rules go in Mind |
| Stale Mind, project moved on | Steward retire protocol: event-anchored on project-internal clock — if material activity has accumulated without redistill (significant new witness entries, finding closures, doctrine amendments), OR if deployment sessions consistently produce wrong direction Mind-only, retire (`soul-status: deprecated` in header). Recalibrated from "~3 months" per SOUL-I038 two-clock model. |

**Retirement is a real outcome, not failure.** A project that stabilizes its
rules and stops needing redistills has won; its Mind goes static-and-good. A
project where the Mind keeps drifting backward toward obligation-collapse
retires it cleanly.

---

## Reproduction-acceptance criteria

| Dimension | Acceptance signal |
|---|---|
| Doctrinal coherence | Mind-only agent produces direction-coherent reasoning on questions the project's recurring rules cover |
| Anchored honesty | When Mind-only agent hits an obligation-specific question, it says *"I need to consult `<specific record>` for X"* — does not bluff |
| Token economy | Mind-only ≥ 30% cheaper than full-record on doctrinal Qs (Tier 2 floor — actual was 41%) |
| Stability | Mind shrinks-or-stays across distills (the Section-5 growth check holds in practice) |

**Initial deployment validation** after MVP ships (Soul System repo dogfood):
small Tier-2-style A/B on **2–3 held-out questions** — one obligation-shaped
(test boundary), one doctrine-shaped (test strength), one mixed. Direction-
agreement on doctrinal Q; correct "consult record" on obligation Q; token-savings
positive on ≥2 of 3.

---

## MVP build scope

**BUILD:**
1. **`commands/soul-distill.md`** — on-demand slash command. Mirrors `/soul-skill`:
   reads witness + ideas + findings + amendments + existing `mind.md`; applies
   four-buckets-plus-residual schema; runs the 4 shrinkage checks; runs the 6
   failure-mode guards; produces a draft mind.md update for Body curation; never
   auto-commits.
2. **The Soul System repo's own `mind.md`** — seeded from the Tier 1 candidate,
   pruned of inspection sections (bias warning, self-assessment, Tier framing).
3. **Project `CLAUDE.md` pattern documentation** — show how a project opts into
   the Mind layer (`@mind.md` after `@operations/CLAUDE.md`). Optional, not
   forced; soul-init may surface the option.
4. **Symlink** `/soul-distill.md` to `~/.claude/commands/` per F029.
5. **SYSTEM-VERSION bump to 0.5.0** — minor-version bump matches the
   architecture-adding scale of A003/A007.
6. **Witness entry** SOUL-068 (or next free, re-read-verify per I027) recording
   the Tier 1 + Tier 2 + spec arc.

**DEFER (named, not built):**
- Auto-fire hooks (session-end / threshold-triggered).
- `/soul-mind` viewer command — just `Read mind.md`.
- Cross-project Mind sharing / synthesis.
- Reproduction-fidelity sampling automation.
- Plugin packaging.

---

## Tier 3 — deployment validation plan

1. **Dogfood on Soul System repo first.** Run `/soul-distill` against its own
   record. Produce the deployed `mind.md`. Inspect against the Tier 1 candidate
   for drift, force-fit, residual changes.
2. **Run the 2–3 question deployment A/B** from the acceptance criteria.
3. **Dogfood on a second project.** Strongest candidate: REF-03 (SOUL-064 already
   harvested its doctrine; the Body knows the project). Emissary test against a
   different domain (UE/Unreal vs Soul-meta).
4. **Update SOUL-I026 status** based on results (Built / Built-with-residual /
   Retired-after-trial).

---

## Open questions

- **How aggressive should the Distiller be with the residual?** It's required in
  schema but its *size* isn't bounded. A 100-line residual eats the budget. The
  growth check covers TOTAL size but not residual-share. Likely a Tier-3 finding.
- **Does the Mind benefit from cross-project synthesis?** I025 (GUI access
  layer) overlaps. Deferred — needs ≥ 3 project Minds in the wild before the
  question is meaningful.
- **What if the project's `CLAUDE.md` already overlaps with the Mind?** The
  renamed-CLAUDE.md guard names the distinction (authored vs distilled) but the
  practical boundary may need refinement in deployment.
- **F014 connection.** The Mind could give the expansion gate a stable reference
  frame to expand FROM — was named in the I026 NOTES. Not designed in this spec;
  potential future integration if both prove load-bearing.

---

## What's NOT in this spec

- Auto-distillation (Voyager-style autonomous compression). The Distiller is a
  command + Claude following a spec; an AGENT that distills autonomously is a
  separate later question.
- The Mind as a memory layer for the AI's own continuity across sessions. The
  Mind is project-scoped; cross-tool / cross-session continuity is SOUL-I003.
- Quantitative compression metrics (Kolmogorov approximations beyond the line
  budget). The four shrinkage checks ARE the metric for MVP.

---

**Source:** Built by the Body + Council through the SOUL-I026 brainstorm flow.
Necessity-first discipline (Tier 1 → Tier 2 → Tier 3) was the structuring
choice; the lens-layer design crystallized from Tier 2's doctrine-vs-obligation
split evidence. **Reinforced by:** Kolmogorov complexity / MDL (Rissanen),
constitutional-AI rules-over-examples, SOUL-033 description budget evidence,
the amendment-process analogy (system-level Mind-work exists; this is the
project-level analog). **Shapes:** the entire spec. **Adopted:** 2026-05-26
(spec). **Status:** draft pending Body review → implementation via writing-plans.
