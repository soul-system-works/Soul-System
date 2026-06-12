---
name: soul-distill
description: Refresh the project's Mind — compress the accumulated record (witness + findings + ideas + amendments) into mind.md as rules / tensions / invariants / contrast cases + named incompressible residual. Body-invoked, on-demand. Produces a draft for curation; never auto-commits. The Distiller's instrument. Use when the record has accumulated enough new rule-evidence to warrant a refresh.
disable-model-invocation: true
---

# /soul-distill — refresh the Mind

The project's accumulated record (witness, findings, ideas, amendments) has been
growing. This command compresses it into `mind.md` — a project-scoped, always-on
artifact holding the **rules that would generate** the project's recurring
decisions, distinct from the records that store them.

**The verdict this is built on (SOUL-I026 Tier 2):** the Mind is a *lens layer*,
not a replacement. It holds **doctrine** (rules that apply across contexts);
**obligations** (specific commitments at specific times) stay in the records.
Tier 2 evidence: Mind-only reasoning was ~41% cheaper than full-record on
doctrinal questions; arms disagreed on obligation-shaped questions exactly where
the residual lives.

**Manual-fire only.** Auto-distillation (session-end hooks, threshold triggers)
is deliberately deferred until the manual cadence proves insufficient.

## What to do

1. **Confirm the Body invoked this.** `/soul-distill` is Body-invoked; if there
   is no explicit ask, stop. The cadence is "when the Body says it's time," not
   "after every change." Default-deny.

2. **Read the project's record AND the existing Mind.** Pull from the project root:
   - `witness.md` (tail at minimum; full if recent distill is stale)
   - `ideas.md` (full)
   - `findings/open/` + `findings/closed/`
   - `amendments/accepted/`
   - `mind.md` (the previous distill, if present — used for the growth check)
   - The seed (`operations/CLAUDE.md`) — to apply the renamed-seed guard

3. **Distill into the four buckets + the residual.** The schema is fixed; the
   contents emerge from the record.

   - **Rules (generators).** Statements that *produce* decisions, not describe
     them. Phrase-test: "do Y when Z" / "prefer Y over Z because…" = keep;
     "X is true" = description, prune. Each rule cites at least one anchor
     (witness ID, finding, amendment, source memory).
   - **Tensions.** Where two rules pull against each other on a recurring
     decision. Name the *pull*, not the resolution — the project decides
     case-by-case.
   - **Invariants.** Non-negotiables. Violating one breaks the project.
   - **Contrast cases.** Disambiguating examples — the seed examples that
     resolve where rules collide. Each cites concrete record anchors.
   - **Incompressible residual.** Path-dependent knowledge that doesn't reduce
     to rules without losing load-bearing information. Naming the residual is
     part of the schema; **zero residual is suspicious** (likely force-fit).
     A canonical residual kind: an **unguessable fact that contradicts a strong
     model prior** (e.g. "this endpoint has NO idempotency support"; "these
     tokens are SINGLE-USE"). Such a fact is *partly incompressible* — its
     FORCE (the incident, the explicit negation), not merely its proposition, is
     the load-bearing part (SOUL-A018 / F045).

4. **Run the four shrinkage-invariant checks.** Before producing the draft:

   - **Line budget.** Target ≤200 lines; hard cap 300. Anchored to the seed's
     footprint — a second artifact of that size is the most the always-on
     budget tolerates before SOUL-033 starts biting.
   - **Anchor requirement.** Every entry in Rules / Tensions / Invariants /
     Contrast cases cites at least one anchor. Anchorless = description = prune.
   - **Generator test.** Each Rule must produce a decision (phrase-test above).
   - **Growth check.** If `mind.md` already exists, the new draft **must shrink
     or stay the same**. Growth means the Distiller failed its job; default-deny
     growth and surface to the Body for explicit sign-off ("I am consciously
     expanding because…").

5. **Run the seven failure-mode guards.** Refuse to produce a draft that fails any:

   - **Drift into summary.** Caught by the growth check (4 above).
   - **Force-fit residual.** Zero residual → must justify or admit force-fit.
   - **Renamed seed.** Per-distill check: "what's in `mind.md` that's NOT in
     `operations/CLAUDE.md`?" If trivial → Mind is redundant → **Steward
     retires** (recommend deletion, do not deploy).
   - **Renamed CLAUDE.md.** Boundary: CLAUDE.md is *authored* (what the project
     is, how agents work). Mind is *distilled* (rules the project discovered
     from its own record). Different sources. If the draft overlaps heavily
     with the project's CLAUDE.md, refine to focus on the distilled-from-record
     rules.
   - **Doctrine–obligation collapse.** Per candidate entry, ask "rule (across
     contexts) or obligation (specific commitment at a specific time)?" Only
     rules go in Mind. Obligations stay in amendments/findings/witness.
   - **Force-stripped anti-prior fact** (SOUL-A018 / F045). When a candidate
     rule rests on an unguessable fact that CONTRADICTS a strong model prior,
     do not compress away the fact's FORCE. Keep the incident and the explicit
     negation in the distilled entry, or leave the fact in the un-distilled
     records — never reduce it to the bare directive. The residual directive
     must be **imperative and loophole-free**: a clause like "unless / except /
     when appropriate" is exactly the opening a frontier model fabricates a
     false reconciling fact through (an invented idempotency key; an invented
     token TTL — each a Coherent Falsehood, A010). It must also be explicit
     enough to survive a terse reading, because a weak reader reverts to the
     prior whenever the rule is loose. Two levers, two tiers: directive-FORM
     gates the frontier (SOUL-129); prior-strength + terseness gates the weak
     model (SOUL-128).
   - **Stale.** Project-internal clock — staleness is event-anchored, not
     calendar-anchored. If material activity has accumulated since the `Last
     distilled` stamp (dozens of new witness entries, multiple finding closures,
     accepted amendments, doctrine edits), the refresh is overdue but legitimate
     — proceed. If the project has been quiet by event-count regardless of
     calendar time, surface the Steward question: is the Mind still load-bearing
     or should it retire?

5b. **Apply the measured compression rules (2.0 — these are results, not style):**

   - **Dedicated-bullet salience beats coverage** (F055): a rule a weak model must
     act on gets its OWN bullet; folding it into a paragraph took activation
     5/5 → 1/5 on identical content. Bloat also splits quoting from obeying —
     a model can cite a rule it then violates; the budget is a correctness rule.
   - **Negation + executable fence is the surviving form** (SOUL-164,
     erosion-audit): "never X" at the site plus a test that fails if broken
     survives compression 30/30; prose rationale erodes. When a distilled entry
     can point at an executable fence, point at it.
   - **Imperative, loophole-free residuals** (SOUL-128/129): "unless / except /
     when appropriate" is the gap a frontier model walks through with an invented
     reconciling fact; terseness is the gap a weak model reverts through.
   - **Anti-prior facts are partly incompressible** (F045/A018): keep the
     incident and the explicit negation, or leave the fact un-distilled — and
     NEVER fabricate an incident to give a bare rule force (the fabrication
     axis, SOUL-164: that is the model's own failure mode, not a technique).

6. **Run the three diagnostic self-test questions** on the draft:

   1. **Load-bearing or renamed-seed?** Does this Mind generate decisions the
      seed alone wouldn't?
   2. **Reproduction-coherent?** A fresh agent reading ONLY this Mind (no
      witness, no findings) — could they propose sensible next-work and predict
      the project's likely response?
   3. **Incompressible residual NAMED?** Did the four buckets force-fit content
      that should have been residual?

   Record honest answers in the draft's commit message or the witness entry
   that follows. A failed self-test is not a draft failure; it is a flag for
   the Body to weigh during curation.

7. **Format the deployed `mind.md`.** Use this shape:

   ```
   # The Mind — <Project Name>

   [Header — one paragraph: what this is, project name, always-on note,
   doctrine-vs-obligation pointer.]

   ## Rules (generators) — N items
   ## Tensions (rules that pull against each other) — N items
   ## Invariants (cannot vary without breaking the project) — N items
   ## Contrast cases (disambiguating examples) — N items
   ## Incompressible residual (named, not forced) — N items

   ---
   **Last distilled:** YYYY-MM-DD against <witness tail / commit SHA>
   ```

8. **Present the draft for curation — delta-first, gap-only, never commit.**
   The Body curates and commits; do not auto-commit (the curation is the earning).
   The review surface must make the *load-bearing question per entry* cheap to
   judge — the Body cannot weigh a draft buried in passing-check prose (the
   I037 pain). Apply the compact, gap-only discipline the completion gate
   already adopted (SOUL-055: "expand to the failing check only on a real gap;
   do not recite passing checks"):

   - **Show the delta, not the whole Mind.** Diff the draft against the prior
     `mind.md`. Present only **new (+)** and **changed (~)** entries across the
     five buckets; collapse unchanged ones to a count (`N unchanged rules —
     expand on request`). First distill (no prior Mind) = everything is new;
     present in full.
   - **One load-bearing verdict per delta entry.** For each new/changed Rule,
     Tension, Invariant, or Contrast case:
     `what it generates · anchor · LOAD-BEARING? Y/N — would removing it change
     a decision, and which one?` A "No" is a prune candidate — surface it for
     the Body to cut, do not hide it. Residual deltas use a different test:
     `does it genuinely resist compression, or is it force-fittable into a rule?`
   - **Checks: run all, recite none.** Steps 4–6 (4 shrinkage checks, 6 guards,
     3 diagnostics) still run in full — that honesty is non-negotiable. But
     present them as **one status line each, expanded only on a flag**, e.g.
     `Shrinkage: clean (169→169) · Guards: clean · Diagnostics: 1 flag →
     <flagged question + honest answer>`. A passing check is not recited.
   - This governs the *review* only; the deployed `mind.md` format (step 7) is
     unchanged.

## Retirement (Steward / never-always-on)

- The Mind carries `Last distilled` so decay is visible.
- Review on **project-internal cadence** — whenever material activity has
  accumulated (significant new witness entries, finding closures, doctrine
  amendments). Event-anchored, not calendar-anchored: still load-bearing?
  still distinct from the seed + CLAUDE.md? reproduction-coherent on recent
  decisions? (Skills review on a different — Anthropic-driven — clock; the
  two cadences are decoupled.)
- A project that stabilizes its rules and stops needing redistills has *won*;
  its Mind goes static-and-good. A project where the Mind keeps drifting toward
  obligation-collapse retires the Mind cleanly (delete `mind.md`; remove
  `@mind.md` from CLAUDE.md; witness entry naming the retirement reason).

## What not to do

- **Do not auto-fire.** Body-invoked only; cadence is earned, not scheduled.
- **Do not auto-commit.** Draft for curation; the Body owns the commit.
- **Do not let the Mind grow.** Default-deny growth (check 4 in step 4).
- **Do not force-fit the residual to zero.** Honesty about what doesn't compress
  is part of the discipline (SOUL-I026 failure mode #2).
- **Do not duplicate the seed or CLAUDE.md.** If the Mind reads as a rename of
  either, retire it.
- **Do not capture obligations as rules.** Doctrine vs obligation is the
  load-bearing boundary (Tier 2 evidence).
- **Do not silently exceed the line budget.** ≤200 target, ≤300 cap; if you
  cannot fit, prune harder before deploying.
- **Do not recite passing checks or re-show unchanged entries.** Present the
  delta + a load-bearing verdict per changed entry; surface only flagged
  checks — the SOUL-055 gap-only discipline applied to the Mind's review
  (step 8). Reciting clean checks is the I037 ceremony cost.

---

**Source:** Built by the Artificer + Architect from the SOUL-I026 brainstorm
(spec: `docs/specs/2026-05-26-the-mind-design.md`, plan:
`docs/plans/2026-05-26-the-mind-implementation.md`). Necessity established
before instrument: Tier 1 (hand-crafted candidate, 218 lines) + Tier 2 (held-out
A/B on `/soul-witness?`; Mind-only arm ~41% cheaper, arms disagreed on
direction — the disagreement is the evidence for the lens-layer architecture).
**Reinforced by:** Kolmogorov complexity / MDL (rules > descriptions),
constitutional-AI's rules-over-examples, SOUL-033 description budget,
the system-level amendment process (this is its project-level analog).
**Shapes:** the four-buckets-plus-residual schema, the doctrine-vs-obligation
boundary, the draft-for-curation discipline. **Adopted:** 2026-05-26.
**Status:** active — MVP; auto-fire, `/soul-mind` viewer, cross-project
synthesis, reproduction-fidelity automation, and plugin packaging deferred.
