```
FINDING ID:      SOUL-F016
DATE:            2026-05-20
WITNESS IDS:     REF-08 (zero in-code markers across ~7k+ lines; honesty lives
                 entirely in docstrings — "calibrated", "approximation", "not
                 production"); FANOUT-007 (handoff style cues); A006 (docstrings
                 blessed as a channel)
WHAT:            Markers and docstrings are not interchangeable honesty channels;
                 they serve different purposes, and projects consistently choose
                 docstrings and skip markers entirely. The distinction worth
                 naming: a MARKER (TODO/FIXME/DEBT/HACK) flags UNFINISHED BUSINESS
                 — work that should still happen. A docstring/NOTE flags a STANDING
                 LIMITATION — a deliberate, accepted property that is not going to
                 change. REF-08 had many standing limitations (correctly in
                 docstrings) and, plausibly, some unfinished business that never
                 got a marker.
WHY NOT YET AMENDMENT:  Refines A006. Cheap. The risk: if markers are always
                 skipped, deferred work goes untracked (no greppable "still to
                 do"). Council to decide whether to (a) clarify the marker =
                 unfinished / docstring = standing-limitation split, and (b)
                 whether unfinished business specifically still warrants a marker.
FILED BY:        Archivist
RELATED:         [[SOUL-A006]], [[SOUL-F004]] (the original markers-vs-docstrings)
STATUS:          Open
```
