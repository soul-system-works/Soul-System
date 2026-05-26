```
FINDING ID:      SOUL-F032
DATE:            2026-05-26
WITNESS IDS:     REF-05 CLOSEOUT.md, SOUL-MO-Fb. The third
                 paradigm-triangulation leg (netflow Python → REF-04
                 MTK → REF-05 Dymola) completed slices 1–6 + FINDINGS
                 + upstreaming in hours instead of the ~2-week wall-clock the
                 second leg consumed.
WHAT:            Soul-System ceremony (CONTEXT.md + ADR + light prior-art sweep
                 + slice-and-verify pattern) **compresses on repeated use** when
                 the prior leg(s) are inherited rather than rerun. Concrete
                 levers that paid back:
                   (a) Priors cited from the prior leg's CONTEXT.md / FINDINGS.md
                       instead of re-discovered ("light sweep, agreed at
                       grilling, documented as known priors").
                   (b) The slice ladder + per-slice verification pattern
                       transferred directly — the ADR could lean on the prior
                       leg's parallel ADR rather than start from zero.
                   (c) Re-measurement of the prior leg's reference (SOUL-F-d
                       guardrail) took 30 s, confirmed stability, and let this
                       leg compare apples-to-apples without restating the
                       calibration.
                 This is the dogfood paying back its own compounding value —
                 the Nth Soul-instance benefits STRUCTURALLY from the prior
                 N-1, not only thematically.
WHY NOT YET AMENDMENT:  Two data points (Julia → Modelica). A third
                 triangulation leg on a DIFFERENT physics domain would confirm
                 the compression mechanism is not domain-bound. Likely belongs
                 in operations/reference-projects.md as a recipe for "how to
                 carry a dogfood into a sibling project."
FILED BY:        REF-05 leg (greenwoodms06), 2026-05-26
RELATED:         [[SOUL-F012]] (loaded text ≠ live behavior — the lesson here is
                 the *opposite* direction: when prior leg outputs are loaded
                 AND inherited as decisions, ceremony compresses; F012 is when
                 doctrine is loaded but not executed),
                 REF-04 HANDOFF.md (the reference-project owes a closing
                 finding and upstreaming — exactly this pathway),
                 REF-05 CONTEXT.md §1 + §6
STATUS:          Open — confirm with a third triangulation on a different
                 physics domain before promoting to amendment.
```
