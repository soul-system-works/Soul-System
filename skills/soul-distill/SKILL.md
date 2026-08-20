---
name: soul-distill
description: Refresh the project's Mind — compress the accumulated record (witness + findings + ideas + amendments) into mind.md as the slim form (A021) — this project's unguessables only, the things a later session cannot re-derive. Produces a draft for curation; never auto-commits. The Distiller's instrument. Use when the Body asks, OR propose it proactively when the record has grown materially since the Last-distilled stamp (~15+ new witness entries, or any finding closure / accepted amendment) — ask first, run on the Body's yes (A022).
---

# /soul-distill — refresh the Mind

The project's accumulated record (witness, findings, ideas, amendments) has been
growing. This command compresses it into `mind.md` — a project-scoped, always-on
artifact holding this project's **unguessables** — the facts, traps and
conventions a later session cannot re-derive — distinct from the records that
store what happened and the contract that carries doctrine.

**The verdict this is built on (SOUL-I026 Tier 2):** the Mind is a *lens layer*,
not a replacement. It holds this PROJECT's generators — rules that produce its
recurring decisions — while **obligations** (specific commitments at specific
times) stay in the records. It does NOT hold *system* doctrine: rules that apply
to any Soul project live in the contract and arrive by import, and restating them
here pays the always-on cost twice (A021; step 3). The word "doctrine" used to
appear here unqualified, which read as a licence to carry exactly what A021
moved out.
Tier 2 evidence: Mind-only reasoning was ~41% cheaper than full-record on
doctrinal questions; arms disagreed on obligation-shaped questions exactly where
the residual lives.

**Model-proposable, Body-confirmed (A022).** The original manual-fire-only stance
deferred automation "until the manual cadence proves insufficient" — the Body's
v2.0 review declared it so ("not clear WHEN I should use these"). The model now
watches a simple growth signal and PROPOSES; the Body's yes is still the trigger,
and the draft-for-curation / never-auto-commit discipline is unchanged.

**The growth signal:** material record activity since the `Last distilled` stamp
in `mind.md` — as a guideline, ~15+ new witness entries, or any finding closure
or accepted amendment. Event-anchored, not calendar-anchored. No `mind.md` yet?
Then the signal is the first accumulation that would fill one (see /soul-init's
"the Mind is earned" note).

## What to do

1. **Confirm the trigger.** Either the Body invoked this, or you are proposing:
   state the signal plainly ("N witness entries and M finding closures since the
   last distill — want me to refresh the Mind?") and WAIT for the yes. No yes,
   no distill. The cadence is still the Body's; only the noticing moved.

2. **Read the project's record AND the existing Mind.** Pull from the project root:
   - `witness.md` (tail at minimum; full if recent distill is stale)
   - `ideas.md` (full)
   - `findings/open/` + `findings/closed/` and `amendments/accepted/` — **Soul
     System repo only.** Domain projects have neither (they are upstream stores);
     there, the record is witness + ideas + the cursor's OWED UPSTREAM field.
   - `mind.md` (the previous distill, if present — used for the growth check)
   - The seed (`operations/CLAUDE.md`) — to apply the renamed-seed guard

3. **Distill into the slim form: the unguessables only.** One numbered list of
   the things a later session *cannot re-derive* from the code, the record, or
   its own reasoning. No fixed section headings — the shape follows the content.

   **The bar for an entry (F044 triage):** ask "could a fresh session reason its
   way back to this?" No → carry it. Yes → leave it out; the derivable
   regenerates on its own and only inflates the always-on cost. Each entry cites
   at least one anchor (witness ID, finding, amendment, commit).

   What that usually leaves — as guidance, never as headings to fill:

   - **Generators.** Rules that *produce* decisions, not describe them.
     Phrase-test: "do Y when Z" / "prefer Y over Z because…" = keep; "X is
     true" = description, prune.
   - **The trap and its direction.** A calibration lean, a measurement that
     returns a plausible wrong number, a tool that fails silently on this
     platform. These are the highest-value entries in the form.
   - **Path-dependent facts that contradict a strong model prior** — "this
     endpoint has NO idempotency support"; "these tokens are SINGLE-USE".
     Carry the FORCE (the incident, the explicit negation), not just the
     proposition: the incident is the load-bearing part (SOUL-A018 / F045).
   - **Conventions that live nowhere else** — a branch discipline, a name that
     must stay redacted, a directory that must never be touched with a given
     tool.

   **Doctrine does NOT go here.** Rules that apply to any Soul project live in
   the contract (`operations/CLAUDE.md`) and arrive by import; restating them in
   `mind.md` pays the always-on cost twice. This is the A021 line: the always-on
   layer is one plain contract plus this project's unguessables, and nothing else.

   > **Why slim, and why this changed (2026-08-20).** A021 (2026-06-11) shrank
   > the Soul System's own Mind to this form on measured evidence: doctrine prose
   > above the core bought no quality difference across 62+20+27 scored
   > increments while costing ~6k always-on tokens per session, and F055 makes
   > unnecessary always-on text a *correctness* risk, not merely a cost. This
   > skill kept prescribing the older four-bucket schema (Rules / Tensions /
   > Invariants / Contrast cases / Residual), so five of five consumer projects
   > distilled into a form the source repo had abandoned — one of them to 239
   > lines and 20 KB of always-on text. The Body's call, 2026-08-20: slim is the
   > path everywhere; no test arm required. **Existing four-bucket Minds are not
   > migrated** — they convert naturally at their next distill, since a distill
   > rewrites `mind.md` whole.

4. **Run the four shrinkage-invariant checks.** Before producing the draft:

   - **Line budget.** Target ≤80 lines; hard cap 120. Re-anchored 2026-08-20 to
     what the slim form actually costs: the contract is ~75 lines and this repo's
     own Mind is ~69. The old 200/300 cap was anchored to the pre-2.0 seed and let
     a 239-line, 20 KB project Mind pass unflagged — the very artifact the slim
     switch was made to prevent. Over target: cut, do not request an exception.
   - **Anchor requirement.** Every entry cites at least one anchor. Anchorless
     = description = prune.
   - **Unguessability test.** Every entry fails "could a fresh session reason
     its way back to this?" Anything that passes is derivable — cut it.
   - **Growth check.** If `mind.md` already exists, the new draft **must shrink
     or stay the same**. Growth means the Distiller failed its job; default-deny
     growth and surface to the Body for explicit sign-off ("I am consciously
     expanding because…").

5. **Run the seven failure-mode guards.** Refuse to produce a draft that fails any:

   - **Drift into summary.** Caught by the growth check (4 above).
   - **Force-fit entry.** An entry that reads like a heading being filled
     rather than a trap being recorded. The slim form has no sections to fill;
     if an entry exists to round out a shape, cut it.
   - **Renamed contract.** Per-distill check: "what's in `mind.md` that's NOT
     in `operations/CLAUDE.md`?" If trivial → Mind is redundant → **Steward
     retires** (recommend deletion, do not deploy). Under the slim form this
     guard bites harder than it used to: doctrine restated locally is the
     single most common way a Mind grows.
   - **Renamed CLAUDE.md.** Boundary: CLAUDE.md is *authored* (what the project
     is, how agents work). Mind is *distilled* (rules the project discovered
     from its own record). Different sources. If the draft overlaps heavily
     with the project's CLAUDE.md, refine to focus on the distilled-from-record
     rules.
   - **Doctrine–obligation collapse.** Per candidate entry, ask "generator
     (produces decisions across contexts) or obligation (a specific commitment at
     a specific time)?" Only generators go in the Mind; obligations stay in the
     records. And per step 3, a generator that applies to ANY Soul project is
     contract doctrine, not a Mind entry — cut it.
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

   1. **Load-bearing or renamed-contract?** Does this Mind generate decisions
      the contract alone wouldn't?
   2. **Unguessable-coherent?** A fresh agent reading the contract PLUS this
      Mind (no witness, no findings) — is it kept off the traps this project
      has already paid for? Ask about the traps, not about next-work: the slim
      form deliberately leaves doctrine in the contract and obligations in the
      records, so a Mind that could predict next-work on its own would be
      carrying material A021 moved out. Judged against the contract+Mind pair,
      never the Mind alone (SOUL-I055, closed 2026-08-20).
   3. **Anything carried that a fresh session would re-derive?** Every entry
      must fail the "could they reason back to this?" test. One that passes it
      is inflation — cut it.

   Record honest answers in the draft's commit message or the witness entry
   that follows. A failed self-test is not a draft failure; it is a flag for
   the Body to weigh during curation.

7. **Format the deployed `mind.md`.** Use this shape:

   ```
   # Project notes — <Project Name>

   [Header — two or three lines: the slim form (A021), only this project's
   unguessables; doctrine lives in the contract, obligations in the records.]

   ## Carry these (project-specific, not re-derivable)

   1. **<Short name for the trap or convention.>** The fact, its force, and
      the anchor that earned it.
   2. …

   ---
   **Last distilled:** YYYY-MM-DD against <witness tail / commit SHA>
   [+ one line naming what was compressed away to pay for anything new]
   ```

   Numbered items, not headings. If a project's Mind genuinely needs grouping,
   group it — but do not restore fixed section names, because empty sections
   invite force-fill, which is the failure the four-bucket form kept producing.

8. **Present the draft for curation — delta-first, gap-only, never commit.**
   The Body curates and commits; do not auto-commit (the curation is the earning).
   The review surface must make the *load-bearing question per entry* cheap to
   judge — the Body cannot weigh a draft buried in passing-check prose (the
   I037 pain). Apply the compact, gap-only discipline the completion gate
   already adopted (SOUL-055: "expand to the failing check only on a real gap;
   do not recite passing checks"):

   - **Show the delta, not the whole Mind.** Diff the draft against the prior
     `mind.md`. Present only **new (+)** and **changed (~)** entries;
     collapse unchanged ones to a count (`N unchanged items — expand on
     request`). First distill (no prior Mind) = everything is new;
     present in full.
   - **One load-bearing verdict per delta entry.** For each new/changed item:
     `what it prevents or generates · anchor · UNGUESSABLE? Y/N — could a fresh
     session reason its way back to this?` A "Y, they could" is a prune
     candidate — surface it for the Body to cut, do not hide it.
   - **Checks: run all, recite none.** Steps 4–6 (4 shrinkage checks, the guards,
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
  the Mind's import line from CLAUDE.md — `@mind.md` or `@.soul/mind.md`,
  whichever the project uses; witness entry naming the retirement reason).

## What not to do

- **Do not run without the Body's yes.** Proposing on the growth signal is
  encouraged (A022); running before the Body answers is forbidden. Never
  schedule or hook this — the proposal is conversational, the trigger is human.
- **Do not auto-commit.** Draft for curation; the Body owns the commit.
- **Do not let the Mind grow.** Default-deny growth (check 4 in step 4).
- **Do not manufacture entries to fill a shape.** The slim form has no buckets to
  fill, so there is nothing to force-fit; honesty about what doesn't compress
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
**Shapes:** the slim unguessables-only form (A021), the doctrine-vs-obligation
boundary, the draft-for-curation discipline. **Adopted:** 2026-05-26.
**Amended:** 2026-08-20 — schema switched from four-buckets-plus-residual to the
slim form, closing SOUL-I055; the four-bucket prescription had outlived A021 by
ten weeks and five of five consumer projects had followed it.
**Status:** active — MVP; model-proposed on the growth signal since SOUL-A022
(2026-06-12; the manual-fire-only deferral discharged by the Body's v2.0 review).
`/soul-mind` viewer, cross-project synthesis, and reproduction-fidelity
automation remain deferred.
