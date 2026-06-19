# SOUL-F059 — A comparison's feasibility is the INTERSECTION of its inputs, not the existence of each

```
FINDING ID:      SOUL-F059
DATE:            2026-06-19
WITNESS IDS:     VOY-039 (reference project: VOYAGER-OS — the first synergistic-fusion
                 worked example; the design passed every "does the data exist" check yet
                 the marquee predictor lane was structurally excluded from the test).
WHAT:            A pre-build feasibility check that confirms each input EXISTS can still
                 green-light a dead measurement, because the test actually needs the inputs
                 to OVERLAP in the dimension the method compares on. In VOYAGER the prior
                 doctrine (VOY-007 / M18: "measure n before building" — don't design a
                 backtest whose data isn't there) had matured to a real discipline: name
                 the >=2-lane question, then verify the predictor lanes exist before
                 designing. It passed: the predictor lane (ITAAC construction, 371 obs, the
                 lane built precisely to LEAD reactor startup) existed, and the oracle
                 (reactor power, 15 yr) existed. The test still could not run as intended —
                 the power feed is a rolling 365-day record, so captured power began 2024
                 while ITAAC ended 2022-12. Both inputs existed; they did not co-exist IN
                 TIME within the horizon window, so the strongest predictor could NEVER
                 enter the comparison. The verdict (REJECTED) was partly an artifact of the
                 non-overlap, not of the hypothesis. Lesson: the feasibility precondition of
                 a comparison is the INTERSECTION of its inputs over the axis the method
                 keys on (here, time), not the marginal existence of each. Extend the
                 pre-build check accordingly: don't ask "does each piece exist?", ask "do
                 the pieces overlap where the method will join them?" — and measure that
                 overlap before designing, the same way you measure n.
                 SECONDARY (reinforcement, not new): the same session's adversarial review
                 caught a test-vs-impl contradiction INTERNAL to the plan (a precision
                 metric defined two incompatible ways across a test and its implementation)
                 that the author's own pass had green-lit — a fresh instance of "review
                 before merge catches what self-passes don't" ([[SOUL-F048]]).
WHY NOT YET AMENDMENT:  Single instance, single reference project. The corrective is a
                 natural extension of an existing discipline (measure-before-build) rather
                 than a new mechanism, so it may not need its own doctrine line — the open
                 question is whether "verify intersection, not just existence" is a distinct
                 enough failure mode to name, or whether it folds into measure-before-build
                 as a worked clarification. Needs: a second instance, ideally on a NON-time
                 axis (e.g. two datasets that both exist but share no entity keys, or no
                 unit of analysis), to show the lesson is about intersection-in-general and
                 not a time-specific quirk of rolling-window feeds.
FILED BY:        VOYAGER-OS adopter project, per the I014 upstreaming obligation (Soul-meta
                 lesson owed at a milestone boundary; domain result stays home in
                 findings/2026-06-15-vogtle-phase-fusion-worked-example.md).
RELATED:         [[SOUL-F047]] (asserted-vs-executed — a feasibility check that PASSES on
                 paper but fails on execution is the same family: the check measured the
                 wrong thing), [[SOUL-F048]] (mechanical/review sweep catches reasoning-pass
                 residual — the secondary catch above).
STATUS:          Open
```
