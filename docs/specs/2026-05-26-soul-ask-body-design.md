# /soul-ask-body — Design Spec

**Date:** 2026-05-26
**Status:** Draft — Cluster 1 design beat, third sibling (after /soul-council and
/soul-roles). Body picked shape **(β) + (γ)** after clarification: Body-invoked check
**plus** doctrine line. Spec content is draft pending Body review.
**Topic:** A Body-invoked pre-delegation check that surfaces pending Body-only inputs,
paired with a doctrine line requiring AI to name those dependencies before pushing past
them.

## Problem (two levels)

- **Immediate:** [[SOUL-F037]] names four kinds of input the Body is the only viable
  source for: heuristic hints, strategic intent, preference, private knowledge. The
  AI's default of "barrel ahead autonomously" mishandles kinds 1–3 (confidently-wrong
  work) and mishandles kind 4 (fabrication or omission). Two F037 instances showed
  this in the wild — REF-02 M8 (AI declared cross-validation "infeasible"; Body said
  "probe wayback"; result became 16/16 agreement) and REF-02 M9 (AI sketched
  HFIR-only architecture; Body said "vast number of facilities"; reframed the ADR).
- **Larger system:** The activation asymmetry F014 documented for *expansion roles*
  has a knowledge-axis analog: the AI cannot auto-detect when a Body-only input is
  needed any more than it can auto-detect when scope is too small. Same structural
  problem; same shape of fix — explicit Body invocation for the cheap pre-emptive
  check, plus doctrine for the recommendation-time discipline.

## Decision (settled with the Body, 2026-05-26 beat)

Two-part shape, **(β) + (γ)** per Body's choice:

1. **(β) Body-invoked check** — `/soul-ask-body` is typed by the Body, typically
   before authorizing autonomous work or at a decision point. AI surveys its current
   state and surfaces pending Body-only questions categorized by F037's four kinds,
   or reports "no Body-only inputs needed at this scope."
2. **(γ) Doctrine line** — a small addition to `operations/CLAUDE.md` requiring AI to
   name Body-only dependencies explicitly before issuing recommendations that depend
   on them.

The two halves cover different moments:

- **(β) covers pre-delegation** — the gate before autopilot, before scope authorization.
- **(γ) covers recommendation-time** — at the moment the AI is about to ship advice
  that depends on something only the Body knows.

3. **NOT (α).** AI-invoked-at-detection was rejected: it hits the same activation
   problem F014 documented (no reliable mechanical detection of "this is a Body-only
   question"). The doctrine line (γ) does the recommendation-time work without
   pretending the detection is automatic.
4. **Sibling of /soul-council and /soul-roles** — completes the Cluster 1 instrument
   suite. Different from /soul-council (which convenes the chamber for deliberation)
   and /soul-roles (which observes role-firing). This one surfaces *Body-only
   knowledge gaps* specifically.
5. **Pairs naturally with the Scope Manifest pattern** (this session's semi-autonomous
   forward-motion shape). Before authorizing a manifest: `/soul-ask-body`, flush any
   Body-only questions, then authorize.

## The abstraction layer

- **What varies:** the scope (whole session / a specific finding / a specific decision
  about to be made); the number of pending questions; the kinds (1–4) surfaced.
- **What decides whether it varies:** the Body's scope argument; the agent's honest
  read of its current state.
- **What cannot vary:** Body-invoked (no auto-fire — same structural reason as
  /soul-council and /soul-expand); output is questions OR "none pending"; F037's
  four-kind taxonomy is the framing; honest about uncertainty (the agent may not
  know what it doesn't know — own that explicitly).

## (β) The command: `/soul-ask-body [scope]`

Steps the agent runs:

1. **Parse scope** (optional argument):
   - Default: current active work (the live AL, in-flight task, named upcoming
     decision).
   - `for <finding-id>` — scope to a specific finding's resolution.
   - `for next <N> turns` — scope to immediately upcoming work.
   - `for session` — broader survey across the session's open threads.
2. **Survey the agent's current state.** Honestly read the work-in-progress and
   identify points where one of the four kinds is load-bearing:
   - **Kind 1 (heuristic):** "Am I about to declare something infeasible / not
     found / done based on a search that the Body might know to extend?"
   - **Kind 2 (strategic intent):** "Am I making design choices whose right answer
     depends on multi-step direction I haven't been told?"
   - **Kind 3 (preference):** "Are there multiple technically-valid paths where my
     choice is actually the Body's call?"
   - **Kind 4 (private knowledge):** "Am I assuming things about data / org /
     in-flight context I can't actually see?"
3. **Compose the questions** — each tagged with its kind, with the SPECIFIC context
   that surfaced it. Generic questions are not allowed; concrete decisions only.
4. **Surface to Body.** Structured prompt; one question per kind at most by default
   (avoid flooding); use `AskUserQuestion` tool or equivalent if interactive.
5. **OR report "no pending Body-only inputs at this scope"** with a one-line caveat
   on what was surveyed and what may have been missed. Honesty about the survey's
   completeness is mandatory.
6. **Body answers.** Each answer is recorded:
   - As an explicit decision in the witness (a short SOUL-XXX entry referencing the
     /soul-ask-body invocation and the answers).
   - As context the AI uses immediately for the work in scope.
7. **No graduation.** /soul-ask-body does NOT create findings or amendments. Its
   output is witness-level capture only.

### Output example (sketch — final format settled at build)

```
/soul-ask-body for next 3 turns

Surveying current state...

3 pending Body-only inputs detected:

[Kind 2 — Strategic intent]
  Context: I'm about to draft an ADR for the F038 amendment.
  Question: should the rule scope to `claude -p` specifically (per Probe 2's
  3/3 interactive clean) or stay broader ("any @-import-based experiment
  harness")? The narrower rule is empirically supported now; the broader
  rule survives further interactive evidence collapsing.

[Kind 3 — Preference]
  Context: I'm about to decide where the F038 doctrinal fix lands.
  Question: operations-level rule (lighter footprint, in the
  measurement-method or harness doc) vs Mind/seed line (heavier footprint,
  always-on)? Both technically valid.

[Kind 1 — Heuristic]
  Context: Searching for a precedent in `operations/` for how other
  intermittent-failure findings landed their fixes.
  Question: am I missing a related precedent you remember? I scanned F028
  and F036 family but may have missed adjacent ones.

(Nothing surfaced for Kind 4 in this scope.)

Body answers each? Or skip?
```

## (γ) The doctrine line — added to `operations/CLAUDE.md`

Proposed location: under §The Mandatory Gates, as a new gate (or under
§Capturing Ideas if more natural — Body decides).

Proposed wording (terse, in the seed's voice):

> **Before issuing a recommendation that depends on Body-only input:**
> Name the dependency explicitly. Body-only inputs are heuristic hints, strategic
> intent, preference between technically-valid paths, or private knowledge — see
> SOUL-F037. Default to *asking* (via `/soul-ask-body` or inline question); do not
> push harder on available evidence as a substitute for asking. The AI cannot
> reliably auto-detect when a Body-only input is needed (same structural problem as
> SOUL-F014 expansion); the discipline is to surface the dependency at
> recommendation-time when it is recognised, not to pretend the detection is
> automatic.

Alternative shorter version (if Body prefers):

> **Body-Input Obligation:** When a recommendation depends on Body-only input
> (heuristic / intent / preference / private — see SOUL-F037), name the dependency
> and ask, do not push harder on available evidence as a substitute.

Decision on wording: Body's call at the doctrine edit step.

## Failure-mode guards

| Failure | Guard |
|---|---|
| **Over-asking** — surface every micro-decision as a Body-only question | Concrete-decisions-only rule. Surveys must name SPECIFIC questions tied to SPECIFIC in-flight work; generic "do you have any thoughts?" is not allowed. |
| **Under-asking** — agent misses the Body-only nature of a question | Honest survey requires explicit "I may have missed X" caveat. The agent acknowledges its own detection limits. (γ) doctrine fires AGAIN at recommendation-time, providing a second chance. |
| **Faux questions** — questions phrased to elicit confirmation of agent's preferred answer | Questions must present alternatives neutrally, no leading phrasing. Skeptic role implicit at compose-time. |
| **Ceremony** — invoked routinely as theatre | Same as /soul-council guard: if invoked for trivial work, Steward flags it. Default scope ("next 3 turns" / specific finding) keeps it bounded. |
| **Body-input pollution** — Body answers in passing, AI forgets to record | Step 6 is mandatory: witness entry referencing the invocation + the answers. Verifiable; future Cartographer can trace what was asked. |
| **Detection-problem creep** — temptation to make this auto-fire | Same answer as F014: NO. The doctrine line (γ) is the recommendation-time discipline; (β) is the pre-delegation check; neither auto-detects, both rely on explicit invocation/discipline. |

## Dogfood reference

- **F037's two REF-02 instances** (M8 Wayback, M9 multi-facility) are the empirical
  precedent. In both cases, the Body interjected manually; this instrument codifies
  that interjection as a pre-emptive check.
- **This session's design beat** demonstrated the pattern: at each fork, I surfaced
  options and asked the Body to pick rather than barrelling ahead. That's (γ) in
  practice — naming the dependency on Body preference and asking.

## Open questions

- **Q1. Where does (γ) doctrine line land?** §The Mandatory Gates (gate-level rigor)
  or §Capturing Ideas adjacent (lighter framing) or a new §Body-Input Obligation?
  Body picks at the edit step.
- **Q2. Bundle (γ) with the counterweight discipline line?** Both are activation-axis
  doctrines from this beat. Could be one §Activation Disciplines section in the seed
  or two separate lines. Default-simplicity says: try as two terse lines first; bundle
  if they read more clearly together.
- **Q3. AskUserQuestion tool dependency?** (β) uses `AskUserQuestion` for structured
  prompting when interactive. Acceptable dependency; fallback for non-interactive
  modes is plain prose questions in output.
- **Q4. Should answers feed back into ideas.md / findings/?** No at MVP — witness-only.
  If a Body answer reveals a load-bearing pattern, that's a separate `/soul-finding`
  Body decision.

## Tier 3 — validation plan

After build:

- **Tier 3a — F037 instance simulation.** Take the REF-02 M8 / M9 scenarios. If the
  AI ran `/soul-ask-body` at the analogous moment, would it have surfaced the
  Wayback heuristic or the multi-facility intent? Walk the simulated scenarios; if
  the survey misses both, the survey method needs sharpening.
- **Tier 3b — Scope Manifest pairing.** Use `/soul-ask-body` before authorizing the
  next Scope Manifest (e.g. for `/soul-roles` Tier 3 runs). Does it surface real
  pre-delegation questions, or does it return "none pending" trivially? Either
  outcome is informative.
- **Tier 3c — doctrine fire-rate.** Over 10 recommendation-shaped outputs after (γ)
  lands, how often does the AI actually name a Body-only dependency? If never, the
  doctrine isn't firing (F012 family); if always, it's ceremony. Healthy band is
  some-but-not-all.

## Build dependencies

- (β) command depends on: existing AskUserQuestion tool; witness.md write capability;
  the four-kind taxonomy as a parsable enum.
- (γ) doctrine: pure text edit in `operations/CLAUDE.md`. No code.
- No new substrate.

## Discharges (when shipped)

- [[SOUL-F037]] — directly (the instrument candidate it named, in the (β)+(γ) shape).
- [[SOUL-F014]] — knowledge-axis partial (the Body-Input Obligation is the knowledge
  analog of the counterweight discipline for scope/roles; together they discharge
  the broader activation problem on two axes).
- [[SOUL-A010]] — adjacent (Anchor Obligation: claims need external anchors; this
  finding says SOMETIMES the external anchor lives in the Body's head, and the right
  move is to ask).

## Open residuals (named, not promised)

- Counterweight discipline doctrine line (F014's ROLE ECONOMICS) — separate spec /
  edit, pairs with (γ) above.
- A third instance of F037 from a non-REF-02 project would graduate F037 from
  finding → amendment, and could absorb this instrument's status. Watch and capture.
- Kind 4 (private knowledge) has not yet been observed in the wild; (β) surveys it
  by category but cannot detect when it's needed. Open per F037.

---

**Designed:** 2026-05-26 (Cluster 1 design beat, third sibling).
**Adopted:** pending Body review.
**Built:** TBD.

**Source:** Designed alongside /soul-council and /soul-roles in the Cluster 1 design
beat. Shape (β)+(γ) chosen by Body after clarification (Shape (α) AI-invoked rejected
on the same activation-detection grounds as F014's auto-fire-impossible insight).
Anchored in [[SOUL-F037]] (the failure pattern + the instrument candidate);
[[SOUL-F014]] (the structural insight reused on the knowledge axis); the two REF-02
instances as empirical precedent.
