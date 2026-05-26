```
FINDING ID:      SOUL-F033
DATE:            2026-05-26
WITNESS IDS:     REF-05 MO-F1 / MO-F4 / SOUL-MO-Fd. Three slices
                 (steady 1+3, transient 5+6) verified conservation invariants
                 at float64 noise (≤1e-13 K) with no hand-written residual.
                 The netflow Python plugin (1342 LOC) carries multiple
                 conservation tests to verify its hand-assembled sparse
                 residuals do the same job.
WHAT:            **Concrete data point reinforcing the 2026-05-20 Council
                 verdict that pivoted netflow toward Modelica/MTK.** The
                 acausal across/through connector + `connect()`-emitted
                 conservation pattern makes an entire class of bugs
                 **structurally impossible** rather than merely caught by
                 tests:
                   - Kirchhoff's current law at each node is emitted by the
                     compiler from connect() statements; the model author
                     never writes Σf = 0.
                   - Stream connectors (Franke 2009) emit the upwind enthalpy
                     bookkeeping; the author never writes `if m_flow > 0 then
                     in else out`.
                   - Adding storage (HeatCapacitor on a port) extends the
                     algebraic system to a DAE *without touching the
                     surrounding component contracts* — verified empirically
                     in slice 1 → slice 5.
                 netflow's project required a layered test suite to validate
                 its hand-rolled equivalents and had documented "test the
                 conservation property explicitly" obligations; Modelica
                 removes the obligation entirely because the bug cannot be
                 introduced. The Modelica leg now supplies the Modelica-side
                 numbers that the Council's pivot decision was *predicting*
                 in 2026-05-20 without yet having measured.
WHY NOT YET AMENDMENT:  This is corroboration of a prior decision, not a new
                 doctrine. Belongs in the rationale trail of the pivot
                 decision (operations/ or philosophy/the-soul.md "Multiverse
                 Warning" example), and as a concrete recommendation cue:
                 *prefer connect()-emitted conservation over hand-rolled
                 residuals when the physics is reducible to across/through
                 with a single conserved flux per node.*
FILED BY:        REF-05 leg (greenwoodms06), 2026-05-26
RELATED:         REF-04 HANDOFF.md §1 (the pivot rationale this
                 amplifies), REF-04 MTK-F1 / MTK-F7 (the MTK side of
                 the same point), [[SOUL-F012]] (the difference between
                 doctrine that is loaded vs lived — here Modelica makes the
                 doctrine *structural*, the strongest form of "lived"),
                 REF-05 MO-F1, MO-F4, SOUL-MO-Fd, ADR-0001
STATUS:          Open — corroborates an active prior decision; promote to
                 explicit guidance in the Soul External-Skills table or in
                 a recipe doc.
```
