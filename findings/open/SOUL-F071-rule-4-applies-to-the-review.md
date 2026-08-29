# SOUL-F071 — Rule 4 governs the work and is not read as governing the review of it

```
FINDING ID:      SOUL-F071
DATE:            2026-08-28
KIND:            Doctrine gap — an existing rule whose scope stops one step short
                 of where its own reasoning leads.
REFERENCE PROJECT: (1) SENSOR-VIEW — "a fresh-context reviewer that EXECUTES a
                     proposed failure sequence turns 'latent hazard' into
                     'proven': twice today [i.e. in one day] the reviewer ran the scenario (a
                     three-test order; a git probe) where the author had reasoned
                     about it, and BOTH must-fixes came from that. Rule 4 applies
                     to the REVIEW as much as to the work."
                 (2) This repo, 2026-08-28 — the v2.3.0 reviewer reproduced two
                     silent data-loss paths on synthetic cursors rather than
                     arguing they existed; both were release-blocking, and the
                     reproductions are what made them undeniable rather than
                     debatable. Recorded in SOUL-183.
WITNESS IDS:     SOUL-183, SOUL-184.
STATUS:          Open — graduated by the Body 2026-08-28. Note the evidence base
                 is TWO instances, one of them this repo's own; thinner than
                 F070's seven and recorded as such rather than inflated.
RELATED:         Contract rule 4, SOUL-F047 (asserted vs executed verification),
                 SOUL-F064.
```

## The gap

Rule 4: *nothing is done until verified by execution. If you cannot run it, name
exactly what is unrun and hand it forward.* It is written about the work. Review is
the one activity in this system that routinely produces claims — "this could fail
when X" — and hands them straight to a decision, and nothing asks the reviewer to
meet the same bar.

A reasoned hazard and a demonstrated one are treated identically by everything
downstream, but they are not the same evidence. The author of the change has already
reasoned about the code and concluded it was fine; a reviewer who only reasons is
running the same instrument a second time. A reviewer who *executes* is running a
different one.

## What the two instances share

In both, the reviewer's must-fix findings were the ones it had made fail. In this
repo's instance the difference was decisive in a specific way worth recording: one
of the two paths (a field-boundary pattern truncating a block) was invisible to the
losslessness check written to catch exactly that class, because that check inspected
only what it had already extracted. No amount of reading would have surfaced it; the
synthetic cursor did, in one run.

## Candidate wording

Rule 4 gains: *a review is work. A reviewer's hazard is a claim until it has been
made to happen — reproduce it, or mark it as unreproduced and say so.*

Cheaper alternative if the contract should not grow: put it in the review guidance
rather than rule 4, since the contract is always-on text in every adopting project
and this concerns one activity.

## Honest limits

Two instances is thin, and one of them is this repo reviewing itself, which is not
an independent observation. What raises it above an anecdote is that the mechanism
is named and checkable: in both cases the findings that changed the outcome are
exactly the subset the reviewer executed.
