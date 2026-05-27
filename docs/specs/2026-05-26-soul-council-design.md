# /soul-council — Design Spec

**Date:** 2026-05-26
**Status:** Built — adopted 2026-05-26 (this session); command at `commands/soul-council.md`; symlinked to `~/.claude/commands/soul-council.md`. Spec is the architecture record; the command file is the executable contract.
**Topic:** A Body-invoked instrument to explicitly summon the Council chamber on a named topic.

## Problem (two levels)

- **Immediate:** The Council exists in doctrine (seed §The Council; `philosophy/the-soul.md`)
  but has no explicit invocation instrument. When the Body wants the chamber to weigh in —
  hard decision, contested design, suspected Coherent Falsehood, stress-test a plan — the
  options today are: (a) the AI informally invokes roles in-line, with no standardised
  shape; (b) the Body re-derives the convening pattern from scratch each time. Neither is
  reliable.
- **Larger system:** [[SOUL-F014]]'s dense and re-confirmed evidence base (F014 filed
  2026-05-20; re-confirmed by Tier 3a Mind dogfood SOUL-070, REF-03 2026-05-26 SOUL-065,
  and this session's Cluster 1 cluster pass) shows expansion roles (Prophet, Researcher,
  Revelator)
  structurally under-fire — contraction roles (Accountant, Skeptic, Steward) are cheap and
  feel responsible; expansion roles cost more and risk being wrong, so contraction wins by
  default. The Council exists as doctrine but its **activation** is the problem. F014's
  PRE-MORTEM established: *expansion auto-firing is intrinsically impossible* (no regex for
  "did you think big enough?"). The corollary: Body-invoked expansion must be made
  **cheap, reliable, and observable**. `/soul-council` is the explicit-invocation half of
  that response (the observability half is `/soul-roles`, deferred per default-simplicity).

## Decision (settled with the Body, 2026-05-26 beat)

1. **Body-invoked only.** No auto-fire. F014's structural insight forbids it.
2. **Distinct from `/soul-expand`.** `/soul-expand` is the pre-framing expansion gate
   (specific role-asking at the AL gate); `/soul-council` is general deliberation across
   the chamber on a Body-named topic. Sibling commands, different scopes.
3. **Three sibling instruments + one doctrine line** (the full Cluster 1 design):
   `/soul-council` (this spec), `/soul-roles` (observability — separate spec), `/soul-ask-body`
   (F037 — separate spec), counterweight discipline (doctrine line in seed). This spec
   covers only `/soul-council`; the others land separately with evidence from this one.
4. **Dogfood-first.** This session already produced two convenings under the informal
   pattern (the semi-autonomous question; the Cartographer cluster pass). Both landed
   value, not ceremony. Formalisation = standardising what already works.

## The abstraction layer

- **What varies:** the topic (Body-supplied); which Magistrates are summoned (relevant to
  topic); the convening outcome (synthesis / open question / no-action); the output
  landing (witness / finding / nothing).
- **What decides whether it varies:** Body invokes with a topic; agent picks relevant
  Magistrates with rationale; Tribunes + Censors are mandatory (per seed); the synthesis
  emerges from the role statements + tensions.
- **What cannot vary:** Tribunes always present (Skeptic, Accountant, Advocate — per seed
  §The Council: "every convening"); Censors always present (Guardian, Cartographer —
  watch the system); Body invokes (no auto-fire); Hands NOT in the chamber (Council
  deliberates, Hands produce); ceremony tripwires apply.

## The command: `/soul-council <topic>`

Steps the agent runs:

1. **Read the topic** from the Body's invocation. If absent, ask once; do not invent.
2. **Pick the relevant Magistrates** for this topic. Name each with a one-line rationale
   ("Archaeologist: recovers prior work on X" / "Prophet: reads where this is heading").
   Default-simplicity: 2–5 Magistrates, not all 8 unless the topic genuinely spans.
3. **Walk the chamber** sequentially. Each role contributes one short statement (1–4
   sentences). Order suggested: Magistrates → Tribunes → Censors. The agent embodies
   each role distinctly; roles are PERSPECTIVES, not chatbot personas — they argue from
   their characteristic concern.
4. **Surface tensions** where role positions disagree. Name each tension explicitly:
   "Skeptic vs Advocate: skeptic says X is unsafe; advocate says X is what the Body needs."
5. **Synthesise** — propose a way forward that accounts for the tensions, or explicitly
   name "the chamber cannot resolve this; Body decides Y."
6. **Body decision** — accept synthesis, reject, redirect, or refine.
7. **Land output** (mandatory):
   - **Witness entry** — always. Records the convening at the SUMMARY level: topic,
     roles named, synthesis one-liner, Body decision, pointer to the detail file
     (`councils/SOUL-CCC-<topic>.md`). ID via I027 re-read-verify protocol. Rationale:
     witness average is ~31 lines/entry (measured 2026-05-26: 79 entries / 2442 lines);
     a 7–10 role convening is materially larger (3–5x) and would pollute witness
     scannability if inlined.
   - **Convening detail file** — `councils/SOUL-CCC-<topic>.md`. Full role
     statements, tensions, synthesis, Body decision recorded with no compression.
     CCC is the witness ID (one-to-one mapping). Witness pointer keeps the durable
     record scannable; detail file keeps the convening reproducible.
   - **Finding** — IF the convening surfaced a graduation-worthy gap, Body invokes
     `/soul-finding` (separate command, separate Body decision per I024 anti-inflation).
     The convening does NOT auto-graduate.

### Flag variants (open — Tier 3 may add)

- `/soul-council --full <topic>` — full chamber (all 8 Magistrates + Tribunes + Censors).
  For heavy decisions. Costs more; reserved for the convening that earns it.
- `/soul-council --consult <role> <topic>` — add a Panel of Experts consult to the
  chamber. For domain-specific decisions where a Magistrate hits its competence edge.

## Default chamber

Per seed §The Council:

**Always present (mandatory):**
- **Tribunes** (3 roles): Skeptic, Accountant, Advocate. Seed says: "every convening."
- **Censors** (2 roles): Guardian (watches the roles), Cartographer (watches the map).

**Topically selected (default 2–5):**
- **Magistrates** (8 available): Archaeologist, Seer, Archivist, Prophet, Revelator,
  Researcher, Steward, Emissary. Agent picks based on topic relevance with rationale.

**Never in the convening:**
- **Hands** (Architect, Craftsman, Artificer). They produce under the Body, answerable
  to the Council but not OF it. They receive the synthesis; they do not deliberate it.

This means a default convening = 5 mandatory + 2–5 selected = **7–10 roles total**, not
the full 13. The `--full` flag adds the unselected Magistrates.

## Failure-mode guards

| Failure | Guard |
|---|---|
| **Ceremony** — invoked for trivial work | Per seed §Naming Roles in the Moment: most role work is silent. /soul-council is for moments visibility changes what happens. If invoked for routine work, Steward flags it in the witness entry. |
| **Rubber-stamping** — invoked AFTER Body decided | Witness entry must record the Body's pre-existing position; if synthesis just confirms it without surfacing tension or alternatives, Guardian flags "rubber-stamp" in output. (Guardian, not Skeptic — Guardian watches the chamber's integrity per seed; a Tribune flagging its own convening as ceremony is a self-reference loop.) |
| **Role-set theatre** — full chamber every time | Default is 7–10 roles, not 13. Invoking `--full` requires a topic warranting it; otherwise default-simplicity holds. |
| **Output collapse** — convening with no actionable output | Witness entry must end with either a synthesis OR "chamber unable to resolve; Body decides." Silent dissolution is not allowed. |
| **Personification drift** — roles become chatbot personas | Roles are PERSPECTIVES (per seed). Each role's statement must argue from its characteristic concern, not its "personality." Skeptic argues skepticism, not "Skeptic the character says..." |
| **Inflation** — convening becomes default for normal questions | Same anti-inflation discipline as `/soul-finding`: convening is EARNED, not casual. Casual deliberation = role-naming-in-the-moment, no /soul-council invocation needed. |

## Dogfood reference

Two convenings in this session (2026-05-26) under the informal pattern that this spec
formalises:

1. **Semi-autonomous question convening.** Topic: how to move forward semi-autonomously
   without violating the Body-as-inhabitant invariant. 8 roles named (Architect, Artificer,
   Skeptic, Accountant, Advocate, Steward, Guardian, Prophet). Tensions surfaced
   (autonomy ↔ Body-as-inhabitant; build infra ↔ default simplicity; scope discipline
   ↔ adaptive useful work). Synthesis: Scope Manifest pattern. Body approved with
   redirection. Outcome: dogfooded on F038 scope-probe in the same session; tripwire
   fired correctly. Pattern validated.
2. **Cartographer cluster pass.** Topic: how does the project move forward across many
   open threads with natural groupings. Cartographer-led (per seed §The Cartographer:
   "holds the map of covered/adjacent/unknown"). Output: cluster map (5 clusters,
   ripeness rating, batch-resolution candidates). Body picked Cluster 2 then Cluster 1.
   Pattern: same shape, single-role lead, lighter convening.

Both confirm: tight statements, named tensions, synthesis, Body decision = the working
shape. This spec encodes that shape.

## Open questions

- **Q1. `--full` flag — needed at MVP?** Probably not. Default 7–10 is rich enough for
  most convenings. Add `--full` only after evidence of a topic the default missed.
- **Q2. Convening output — RESOLVED at design time (2026-05-26 review pass).** Two
  artifacts per convening: a short witness pointer (topic + synthesis 1-liner + Body
  decision + path) AND a detail file at `councils/SOUL-CCC-<topic>.md`. Driven by
  measurement: average witness entry 31 lines; a 7–10 role convening with tensions
  and synthesis would balloon a single witness entry to ~3–5x that, polluting
  scannability of the durable record. The pointer/detail split keeps witness lean
  and convenings reproducible.
- **Q3. Auto-detection of "this is a /soul-council moment"?** No — F014's structural
  insight applies here too. Body invokes. (Future: maybe a hook surfaces "this looks like
  council territory" without invoking — observability without auto-fire. Defer.)
- **Q4. Interaction with `/soul-expand`?** `/soul-expand` is the pre-framing gate;
  `/soul-council` is general deliberation. Both Body-invoked; not redundant. A topic
  might use both: `/soul-expand` at the AL gate, `/soul-council` later when a tension
  arises during the work.

## Tier 3 — validation plan

After build:

- **Tier 3a — dogfood on a real Soul question.** Use `/soul-council` on the next
  unresolved Cluster 1 sibling (e.g. the `/soul-roles` design itself) or on a Cluster 1
  question this beat surfaces. Compare against the informal pattern.
- **Tier 3b — ceremony check.** Track invocation count and outcome value over the first
  10 uses. If >50% are "rubber-stamp" or "no actionable output," the instrument is
  over-fired and needs scoping.
- **Tier 3c — discharge check.** Does usage actually move F014, F006, I030? Witness
  evidence required.

Failure-mode guards above are the immediate checks; Tier 3 is the empirical follow-up.

## Build dependencies

- Existing infrastructure: `/soul-witness` (output landing), `/soul-finding` (graduation),
  I027 re-read-verify protocol (witness ID).
- No new infrastructure required. This is a coordination instrument, not a substrate one.

## Discharges (when shipped)

- [[SOUL-I030]] — directly (the instrument it captures).
- [[SOUL-F014]] — partial (the Body-invoked half of expansion activation; observability
  half pending `/soul-roles`).
- [[SOUL-F006]] — partial (the Council can now be summoned at session end if Body wants;
  the auto-trigger question stays open).

## Open residuals (named, not promised)

- `/soul-roles` spec — separate, follows this one.
- `/soul-ask-body` spec — separate (F037).
- Counterweight discipline doctrine line — owned by [[SOUL-A012]] §Activation Disciplines.
- The auto-fire question for expansion — explicitly deferred per F014.

---

**Status when this spec lands:** Draft. Body reviews; iterate; then build session.
**Designed:** 2026-05-26 (Cluster 1 design beat).
**Adopted:** pending Body review.
**Built:** TBD.

**Source:** Designed in response to Cluster 1 design beat 2026-05-26 (Cartographer cluster
pass identified the cluster; Body authorized lead instrument /soul-council). Anchored in
[[SOUL-I030]] (raw idea); [[SOUL-F014]] (the structural insight); the seed's §The Council
(role doctrine); the two in-session dogfood convenings (empirical pattern).
