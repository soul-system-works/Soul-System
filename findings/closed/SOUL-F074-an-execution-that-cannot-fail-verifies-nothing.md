# SOUL-F074 — An execution that cannot fail verifies nothing

```
FINDING ID:      SOUL-F074
DATE:            2026-10-19
KIND:            Doctrine gap — a rule satisfied by its letter (something ran)
                 while its purpose (the claim was tested) is not met.
REFERENCE PROJECT: Eight upstream entries from five projects, read in the second
                 upstream mining pass (SOUL-202):
                 (1) MODEL-TEST, 2026-09-04 — rule 4 made the session
                     RUN a check, not write one that could fail: the check tested
                     a proxy for the property, and a skip in it was wider than the
                     failure it guarded.
                 (2) MODEL-TEST, 2026-09-04 (addendum to an entry on
                     suggested fixes) — a random-input test whose generator never
                     reached the regime where the code fails.
                 (3) MODEL-TEST, 2026-09-16 — a sound check reported
                     green through a pipe whose exit status could not fail; the
                     verdict was read from the pipe, not from the check's output.
                 (4) SENSOR-VIEW, 2026-09-01 — sabotaging what a code comment
                     called load-bearing disproved the comment's stated reason:
                     rule 4 reaches a stated reason, not only a missing guard.
                 (5) SENSOR-VIEW, 2026-09-01 — a test that reads source text
                     passed while the code it guarded was dead; and running one
                     side of a seam was not running the feature.
                 (6) SUB-K, 2026-09-08 — the instrument that made
                     the artifact also verified it; rule 4 says nothing about
                     instrument independence.
                 (7) PLANT-BOP, 2026-09-10 — the completion gate's check 4 proves
                     an image renders, not that what it shows is true.
                 (8) GAME-THERMAL, 2026-09-01 — check 4's "rasterized and
                     inspected" passed while the visual claim was false; the
                     project's remedy was a same-id A/B, not reading a shape.
                 (7) and (8) are independent reports of one defect.
WITNESS IDS:     SOUL-202 (mining pass 2 and the Body's rulings), and the eight
                 upstream entries above.
WHY NOT YET AMENDMENT:  n/a — escalated into SOUL-A027 at graduation.
FILED BY:        SOUL-202 — the mining-pass-2 triage (a read-only Claude agent)
                 proposed the cluster; the Body graduated it.
STATUS:          Graduated by the Body 2026-10-19 (SOUL-202, "yes to all").
                 Closed the same day — SOUL-A027 accepted and applied (rule 4's
                 clause; completion-gate check 4 and the hook's line 4).
RELATED:         completion-gate.md check 0 (A019), SOUL-F047, SOUL-F071,
                 SOUL-F070, witness SOUL-156, SOUL-160/161, SOUL-178.
```

## The gap

Rule 4 says nothing is done until verified by execution. All eight entries ran
something, and each run could not have come out the other way: it measured a proxy
(1, 5), never visited the failing inputs (2), read the verdict off a carrier that
always succeeds (3), checked a reason nobody had tested (4), or used the same
instrument that produced the thing (6, 7, 8). The rule's text is met in every case.
Its point, that the claim met something able to refute it, is met in none.

## The shape the eight share

A verification is evidence only about the property it can fail on. The entries
separate into four ways that property drifts from the claim:

- **A proxy instead of the property** — (1), (2), (4), (5). The check asserts
  something adjacent: that source text is present, that some inputs pass, that the
  code still runs with the guard removed.
- **The verdict read from the carrier, not the artifact** — (3). A pipe, wrapper or
  runner reports its own success.
- **The maker as checker** — (6), (7), (8). Rendering an image through the same
  library that drew it shows the image exists. It does not show the schematic's
  topology is right, or that the feature is present.
- **A partial run reported as the run** — (5). One side of a seam executed; the
  report said the feature did.

## Existing cover, all partial

- **completion-gate.md check 0 (A019)**: "an exit code is not artifact-validity;
  judge from content". It covers (3), but only at the gate, and the gate rarely fires
  on current models (mind item 5). It never reached rule 4.
- **SOUL-F047**: an asserted check is not an executed one. This finding is the next
  step: an executed check that could not fail is not a verification either.
- **SOUL-F071**: a review is work under rule 4. (6) generalises its mechanism. The
  author re-running their own reasoning, or the maker re-running its own instrument,
  is the same instrument twice.
- **This repo's own record** says the same about experiment harnesses (mind items 3
  and 6(d)): SOUL-156(b), where sweeps reported exit 0 while 33 outputs were stubs;
  SOUL-161, where empty prompts were invisible to exit codes and caught by content;
  SOUL-160, where the hook's self-scoping tested a proxy (the substring "soul") for
  the property (a Soul-governed project); SOUL-178, where a ref-scan recorded a
  redaction as complete that it could not see, and the probe meant to settle it
  first tested `head`'s exit code. All four stayed doctrine for harnesses. None
  reached the contract.

## The fix adopted (SOUL-A027)

Rule 4 gains one clause: the execution is *of the property itself, read from the
artifact, by an instrument that did not make it*, and *a partial run leaves the rest
unrun*. Check 4 and the hook's line 4 gain: rendering proves the image exists, not
that what it shows is true. Check content claims against their source, or name the
gap.

**Not adopted** (left as candidates, no ruling asked): (5)'s rule-1 half, that the
guarding test executes the decision and a text-only guard says so; and (2)'s
remedy, that a random test's inputs are chosen to attack the property. The rule-4
clause covers both in principle. Neither has its own wording in the contract.

## Honest limits

Three of the eight come from one project, on two days. The five-project spread is
what makes this a pattern rather than one project's style. Every instance here was
read through the mining triage's one-line summaries, not re-read at its source in
the adopting project's `upstream.md`.
