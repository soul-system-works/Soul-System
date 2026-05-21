```
AMENDMENT ID:    SOUL-A011
DATE:            2026-05-21
STATUS:          ACCEPTED (Body-confirmed 2026-05-21; operations-scoped)
WITNESS IDS:     SOUL-F016 (markers and docstrings are not interchangeable; REF-08
                 carried honesty in docstrings with zero in-code markers across ~7k+
                 lines — standing limitations correctly so, but unfinished work
                 plausibly left untracked); refines SOUL-A006 / SOUL-F004; held as
                 "ready, separate touch" in the SOUL-048 Council synthesis.
WHAT CHANGES:    Sharpen the "Markers and Docstrings" section of
                 operations/code-markers.md with the dividing TEST — *will it change?*
                 A STANDING LIMITATION (a deliberate, accepted property that is not
                 going to change — a named approximation, a validity range,
                 "calibrated, not production") belongs in a docstring/NOTE and earns
                 NO marker. UNFINISHED BUSINESS (work that should still happen) earns a
                 MARKER even when a docstring also describes it, so it stays greppable.
                 This resolves F016's open sub-question (b): unfinished work warrants a
                 marker even in a docstring-heavy codebase.
WHERE IN SOUL:   operations/code-markers.md ("Markers and Docstrings"). Operations-
                 scoped; the-soul.md (Craftsman, L323) already delegates to this file.
QUESTION ONE (Evidence):
                 F016 / F004: projects consistently choose docstrings and skip markers
                 (REF-08: zero markers across ~7k+ lines). Standing limitations sat
                 correctly in docstrings; the risk is unfinished work buried in prose
                 with no greppable "still to do."
QUESTION TWO (Necessity):
                 A006 blessed docstrings and said "provided compromise and deferral are
                 still flagged where they live," but gave no crisp test for WHEN a
                 docstring suffices vs WHEN a marker is also owed. The will-it-change
                 test supplies it; without it, accepted limitations and unfinished work
                 blur, and deferred work goes untracked.
QUESTION THREE (Coherence):
                 Refines A006, does not contradict it. Aligns with "honest in the
                 artifact" and the docs-live-near-code preference (a greppable marker
                 travels with the code). No contradiction.
ACCEPTED BY:     Judge (operations-scoped; Body-confirmed 2026-05-21)
FILED BY:        Archivist
```
