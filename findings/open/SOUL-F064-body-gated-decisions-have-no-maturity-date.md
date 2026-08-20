# SOUL-F064 — A Body-gated decision is a standing IOU with no maturity date

```
FINDING ID:      SOUL-F064
DATE:            2026-08-20
KIND:            Doctrine gap — a class of deliberately-deferred decision that
                 the system creates and then never resurfaces.
REFERENCE PROJECT: Two independent instances in different instruments.
                 (1) PLANT-BOP — an upstream closing note delivered 2026-08-18
                     (findings/open/2026-08-18-thermal-model-project-closing-note.md,
                     observation 1).
                 (2) Cross-project — the six-project retrospective, 2026-08-20,
                     covering every project importing this contract.
WITNESS IDS:     SOUL-178 (the retrospective's release pass); the closing note
                 itself is the primary record for instance (1).
STATUS:          Open — graduated by the Body 2026-08-20. No fix adopted; the
                 candidate mechanisms below are unevaluated.
```

## What the two instances share

**Instance 1 — a gate deliberately kept strict.** A project ran two
content-fingerprint gates. One was deliberately stricter than the other — "any
difference counts" — a recorded, Body-gated decision, correct when made. Months
later the Body locked a documentation-editing phase whose every edit would trip
that gate, holding the whole suite red for the phase's duration and training the
eye to wave through a failing gate: the exact failure that project's own doctrine
names. Nothing surfaced the conflict — not the gate, not the planning pass that
locked the phase. It was caught incidentally, when an adversarial-questioning
skill was invoked on an unrelated scope decision and one frontier question
happened to intersect it.

**Instance 2 — a store only the Body may open.** Amendment A022 forbids a session
from self-invoking `/soul-capture finding`: graduation is the Body's explicit,
earned act. Correct as written — it is what stops findings inflating. But across
six projects and three-plus months, **zero findings were produced**, against 62 in
this repo over the same period. Three of those projects carried scaffolded, empty
`findings/open/` and `findings/closed/` directories the whole time. No session was
wrong; each correctly declined to self-invoke. The gate was simply never opened,
and nothing existed to notice that.

## The shape

A decision of the form *"strict / deferred / Body-only for now, revisit on the
Body's call"* is a **standing IOU with no maturity date**. It is correct at the
moment it is made, it records itself properly, and then nothing ever brings it
back for re-decision. It does not decay into wrongness loudly; it decays into
being *never revisited*, which looks identical to being fine.

The two instances differ in every surface detail — one is a build gate in a
domain project, one is a capture instrument in this system's own doctrine — and
are identical in structure. That is what makes it a finding rather than two
incidents.

## Why the existing instruments do not catch it

- **The witness log** records what happened, not what has *stopped* happening. A
  gate that never fires writes nothing.
- **The Mind** carries rules that generate decisions. A dormant deferral generates
  none, so distillation drops it.
- **The handoff cursor** carries what is live. A deferral that nobody is working
  on is by definition not live, so it falls out of the cursor within a session or
  two — and `[inherited]` marking (A023) applies to *pointers*, not to decisions.
- **`/soul-next`** looks forward from the current state; it does not sweep backward
  over settled calls.

The gap is structural: every instrument is oriented toward activity, and this
failure mode is defined by the absence of activity.

## Candidate mechanisms — unevaluated, listed not recommended

1. **A maturity field.** A Body-gated decision records what would make it worth
   revisiting — an event, a count, a phase change — rather than a date. Cheap to
   write; unknown whether anything would ever read it.
2. **A collision sweep at plan-lock.** When a new plan is locked, some instrument
   checks it against the open Body-gated decisions. This is what would have caught
   instance 1; an adversarial-questioning pass caught it by luck instead.
3. **Periodic mining instead of a trigger** (see SOUL-I058). Push waited for
   someone to notice; one pull pass surfaced eleven candidates in an afternoon.
   Instance 2 is precisely a trigger nobody pulled, so a scheduled sweep is the
   direct answer to it — and this finding was itself produced by such a pass.
4. **Do nothing, and accept it.** The honest option. Both instances were caught
   eventually, at moderate cost, by adversarial passes that exist for other
   reasons. A mechanism that fires rarely and is read rarelier may cost more than
   the failure.

## What would make this finding wrong

If a third instance is found where the deferral *was* resurfaced by an existing
instrument, the gap is narrower than stated and the claim needs rewriting. If the
zero-findings result turns out to have a different cause — the store being wrong
for domain projects rather than the gate being unopened — then instance 2 is
evidence for removing the store, not for a maturity mechanism. The v2.1.0 release
already removed `findings/` from what `/soul-init` scaffolds on exactly that
reading, which means **instance 2's fix and this finding's premise are in
tension**. That tension is unresolved and is the first thing to test.

---
**Filed by:** the six-project retrospective pass, 2026-08-20. Graduated on the
Body's explicit call — the first use of the A022 graduation gate in any project
in four months, which is itself a small datum for instance 2.
