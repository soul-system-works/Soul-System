---
description: Summon the Council chamber on a Body-named topic — walks relevant Magistrates plus mandatory Tribunes + Censors, surfaces tensions, synthesises, lands witness pointer + councils/ detail file. Body-invoked only; NOT auto-firing (per SOUL-F014). Use when the Body wants explicit multi-perspective deliberation on a hard decision, contested design, suspected Coherent Falsehood, or any moment where chamber visibility changes the outcome.
---

# /soul-council — summon the chamber on a named topic

A Body-invoked instrument for explicit Council deliberation: hard decisions,
contested designs, suspected Coherent Falsehoods, plans the Body wants
stress-tested across multiple perspectives. The chamber walks the topic; the
Body decides.

The Council exists in doctrine (seed §The Council; `philosophy/the-soul.md`).
This command makes it **enactable** — a single invocation that runs the
convening shape consistently, so the chamber's value does not depend on the
Body re-deriving the pattern each time.

The activation half of the SOUL-F014 expansion-gap response: contraction
roles fire by default and feel responsible; expansion roles cost more and
risk being wrong. F014's PRE-MORTEM established that auto-detection is
intrinsically impossible. The corollary: **Body-invoked expansion must be
made cheap, reliable, and observable.** `/soul-council` is the explicit
half; `/soul-roles` (separate spec) is the observability half.

## What this is NOT

- **Not auto-firing.** F014's structural insight forbids it. The Body
  invokes; the chamber walks.
- **Not a substitute for `/soul-expand`.** `/soul-expand` is the pre-framing
  expansion gate (specific role-asking at the AL gate); `/soul-council` is
  general deliberation across the chamber on a Body-named topic. Sibling
  commands, different scopes. A single topic might invoke both at different
  moments.
- **Not a finding scaffolder.** If the convening surfaces a graduation-worthy
  pattern, the Body runs `/soul-finding` separately. The convening does NOT
  auto-graduate (per SOUL-I024 anti-inflation).
- **Not a full chamber by default.** Default is 7–10 roles (5 mandatory +
  2–5 topically selected). The full 13-role chamber requires `--full` and
  a topic that warrants it.
- **Not for routine work.** Per seed §Naming Roles in the Moment: most role
  work is silent. `/soul-council` is for moments where visibility changes
  what happens. If invoked for trivial work, Steward flags it in the witness
  pointer.

## What to do

1. **Take the topic** from the Body's invocation. If absent, ask once; do not
   invent. The topic is the Body's; the chamber serves it.

2. **Pick the relevant Magistrates** for this topic (2–5 by default). Name
   each with a one-line rationale:
   - "Archaeologist: recovers prior work on X"
   - "Prophet: reads where this is heading"
   - "Emissary: tests against current reality"
   - …
   Default-simplicity: not all 8 unless the topic genuinely spans the whole
   field of view.

3. **Walk the chamber sequentially.** Each role contributes one short
   statement (1–4 sentences). Order suggested: **Magistrates → Tribunes →
   Censors**. Roles are PERSPECTIVES, not chatbot personas — they argue
   from their characteristic concern. Skeptic argues skepticism, not
   "Skeptic the character says…"

4. **Surface tensions** where role positions disagree. Name each tension
   explicitly: *"Skeptic vs Advocate: skeptic says X is unsafe; advocate
   says X is what the Body needs."* The tensions are what makes the
   convening worth more than a single perspective; do not bury them.

5. **Synthesise** — propose a way forward that accounts for the tensions, or
   explicitly name *"the chamber cannot resolve this; Body decides Y."*
   Silent dissolution is not allowed.

6. **Body decision.** Accept synthesis, reject, redirect, or refine. The
   chamber serves; the Body decides.

7. **Land outputs (both mandatory):**
   - **Detail file** at `councils/SOUL-CCC-<kebab-slug>.md` (CCC = the
     witness ID assigned in the next step). Full role statements, tensions,
     synthesis, Body decision. No compression — this is the durable record
     the convening can be reproduced from.
   - **Witness pointer** appended to `witness.md` — a SHORT entry (topic,
     roles named, synthesis one-liner, Body decision, path to detail file).
     Witness average is ~31 lines/entry; inline-full would balloon to 3–5x
     that and pollute witness scannability. Pointer + detail keeps the
     durable record lean.
   - **I027 protocol — re-read-verify before write.** Witness.md is the
     highest-collision record. Scan `^ID: +SOUL-\d+` right before the
     append; if your assigned ID is taken, increment and retry; three
     collisions in a row → stop and tell the Body.

8. **Optional graduation.** If the convening surfaced a finding-worthy gap,
   the Body invokes `/soul-finding` as a separate command (separate Body
   decision per SOUL-I024). The convening does NOT auto-graduate.

## Default chamber

Per seed §The Council:

**Always present (mandatory):**
- **Tribunes** (3): Skeptic, Accountant, Advocate. Seed: "every convening."
- **Censors** (2): Guardian (watches the chamber's integrity), Cartographer
  (holds the map of covered/adjacent/unknown).

**Topically selected (default 2–5):**
- **Magistrates** (8 available): Archaeologist, Seer, Archivist, Prophet,
  Revelator, Researcher, Steward, Emissary. Agent picks based on topic
  relevance with rationale.

**Never in the convening:**
- **Hands** (Architect, Craftsman, Artificer). They produce under the Body,
  answerable to the Council but not OF it. They receive the synthesis;
  they do not deliberate it.

Default convening = 5 mandatory + 2–5 selected = **7–10 roles**, not 13.
`--full` adds the unselected Magistrates; reserved for topics that warrant
the heavier shape.

### Optional flags (Tier 3 — add only if evidence supports)

- `/soul-council --full <topic>` — full chamber (all 8 Magistrates +
  Tribunes + Censors). For heavy decisions; reserved for convenings that
  earn it.
- `/soul-council --consult <role> <topic>` — add a Panel of Experts
  consult to the chamber. For domain-specific decisions where a Magistrate
  hits its competence edge.

## Failure-mode guards

| Failure | Guard |
|---|---|
| **Ceremony** — invoked for trivial work | Per seed §Naming Roles in the Moment: most role work is silent. If invoked for routine work, Steward flags it in the witness pointer. |
| **Rubber-stamping** — invoked AFTER Body decided | Witness pointer records the Body's pre-existing position; if synthesis just confirms it without surfacing tension or alternatives, Guardian flags "rubber-stamp" in output. (Guardian, not Skeptic — Tribune flagging its own convening is a self-reference loop; Guardian watches chamber integrity per seed.) |
| **Role-set theatre** — full chamber every time | Default is 7–10 roles, not 13. Invoking `--full` requires a topic warranting it; otherwise default-simplicity holds. |
| **Output collapse** — convening with no actionable output | Synthesis step is mandatory: either a way forward OR "chamber unable to resolve; Body decides." Silent dissolution is not allowed. |
| **Personification drift** — roles become chatbot personas | Roles are PERSPECTIVES (per seed). Each role's statement must argue from its characteristic concern, not its "personality." |
| **Inflation** — convening becomes default for normal questions | Same anti-inflation discipline as `/soul-finding`: convening is EARNED, not casual. Casual deliberation = role-naming-in-the-moment per seed, no `/soul-council` invocation needed. |

## What not to do

- Do not auto-fire. Body invokes; that is the contract.
- Do not include Hands in the chamber. They produce; they do not deliberate.
- Do not skip either output (witness pointer or detail file). Both are
  required; the pointer keeps witness lean, the detail keeps the convening
  reproducible.
- Do not skip the I027 re-read-verify protocol on the witness write.
- Do not auto-graduate the convening to a finding. That requires a separate
  Body decision via `/soul-finding`.
- Do not personify roles. Skeptic is a perspective, not a character.
- Do not invent role names. The canonical 13 are in seed §The Council.

---

**Source:** Built by the Artificer for SOUL-I030 (the raw idea) and the
SOUL-F014 expansion-gap response cluster; specced 2026-05-26 at
`docs/specs/2026-05-26-soul-council-design.md` (Cluster 1 design beat); pairs
with `/soul-roles` (observability sibling, separate spec) and SOUL-A012
§Activation Disciplines (the doctrine line for the same activation problem on
both scope and knowledge axes). The two prior informal convenings in the
session that designed this spec (SOUL-077 semi-autonomous question;
Cartographer cluster pass) and the third informal convening that ratified
this spec (SOUL-080, inaugural use of the pointer+detail shape) are the
empirical pattern this command formalises. **Adopted:** 2026-05-26.
**Status:** active — MVP. Tier 3 validation runs after first non-trivial
Body-invoked use: (a) dogfood on a real Soul question, (b) ceremony check
over first 10 invocations, (c) discharge check against F014/F006/I030.
