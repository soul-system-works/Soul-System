```
FINDING ID:      SOUL-F023
DATE:            2026-05-21
WITNESS IDS:     REF-02 M8 — the multi-year backtest showed FY24 at 0.989
                 daily accuracy (best of all years). Disaggregating before reporting
                 revealed the FY24 predictor revision was dated mid-FY, so its "plan"
                 already contained actuals — the number was inflated, not real. FY24
                 was excluded; the honest clean-year total dropped to 0.828. The
                 contamination was caught by per-FY / per-file kind-histogram sanity
                 checks BEFORE the figure reached an artifact. Harvested via SOUL-046.
WHAT:            A clean-looking AGGREGATE can be inflated by one contaminated
                 subgroup. Before trusting (and certainly before reporting) an
                 aggregate metric, DISAGGREGATE it and verify each component's
                 composition justifies inclusion — here, "does this year's predictor
                 actually pre-date the year, or is it secretly reading actuals?". This
                 sharpens F007 (verification != validation) with a concrete tactic:
                 even WITH ground truth, an average is internal coherence until its
                 parts are inspected. The tell is a too-good outlier (0.989 amid
                 0.69–0.95) — an anomalously good subgroup deserves the same suspicion
                 as an anomalously bad one. The value here was timing: the catch was a
                 pre-report verification step, not a post-hoc reviewer rescue.
WHY NOT YET AMENDMENT:  One strong instance (cross-refs F007's +200 K REF-08 bias as
                 the same family). Candidate guard: a "disaggregate the aggregate"
                 prompt in the completion/Universe-final gate — for any reported
                 aggregate, can you show the per-component breakdown and defend each
                 component's inclusion? Pairs with F007's global-invariant gate and
                 risks adding to the F022 completion-gate load, so the Council should
                 decide whether it folds into the existing Universe-final check rather
                 than adding a separate one. Watch for a second independent instance.
FILED BY:        Archivist (harvested from REF-02 M8; the Validation lesson
                 the M8 plan flagged alongside the Emissary one in [[SOUL-F021]])
RELATED:         [[SOUL-F007]] (verification != validation — the parent family),
                 [[SOUL-F021]] (same project; the FY24 contamination is its sibling
                 lesson), [[SOUL-F012]] / [[SOUL-F022]] (the completion gate any guard
                 would attach to), [[SOUL-A010]] (the Anchor Obligation it folds into)
STATUS:          Closed — folded into SOUL-A010 (an aggregate is internal coherence
                 until disaggregated; a claim needing an anchor), 2026-05-21 per Body.
                 Was: Open — single instance; promote toward a gate prompt if a second
                 independent project shows an inflated aggregate that disaggregation
                 would have caught.
```
