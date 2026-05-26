```
FINDING ID:      SOUL-F035
DATE:            2026-05-26
WITNESS IDS:     REF-05 MO-F6 / SOUL-MO-Fe. Eight independent
                 headless-Dymola-harness gotchas were each discovered the
                 hard way during the harness-bringup task, costing roughly
                 one debug cycle each. They were captured in MO-F6 as a
                 future-SKILL.md candidate.
WHAT:            Proposed heuristic for **when** to capture a project-local
                 SKILL.md (the `soul-skill` protocol asks the Body but does
                 not give a trigger threshold): **after the third hard-won
                 trap from the same surface, the skill should be written
                 before that surface is touched again.** Rationale:
                   - One trap = bad luck; could be random.
                   - Two traps from the same surface = pattern; worth a note.
                   - Three traps = the surface is *structurally hostile* and
                     the next session WILL re-discover trap #4. Capture pays
                     back even if used only once more.
                 The headless-Dymola surface in this leg passed three traps
                 around hour 1 (LD_LIBRARY_PATH, MSL not auto-loaded, $DYMOLA
                 missing for dsbuild.sh). The fourth (changeDirectory
                 silently overriding cd) cost a 30-minute false start where I
                 mistakenly thought simulateModel was succeeding silently
                 without writing a file. If a SKILL.md had been written after
                 trap 3, trap 4 would have been a one-line lookup.
                 The dymola-sim-debug skill (already in this user's library)
                 covers a DIFFERENT surface (slow simulations / IF97 events
                 stalls) — confirming the cost/value of these
                 surface-specific skills.
WHY NOT YET AMENDMENT:  Single project, single surface so far. A second
                 confirmation (e.g., the next project that hits three traps
                 from a new tool boundary) would let this graduate to
                 amendment of the soul-skill protocol. Until then, propose
                 this as the empirical guidance: when the body finds itself
                 saying "huh, that's the third weird thing about <X>," that
                 IS the soul-skill cue.
FILED BY:        REF-05 leg (greenwoodms06), 2026-05-26
RELATED:         [[soul-skill]] command (the capture mechanism this heuristic
                 would parameterize), REF-05 MO-F6, SOUL-MO-Fe,
                 dymola-sim-debug skill (an existing surface-specific skill
                 that earned its keep on similar grounds)
STATUS:          Open — confirm with a second instance from a different
                 surface before promoting to a soul-skill protocol amendment.
```
