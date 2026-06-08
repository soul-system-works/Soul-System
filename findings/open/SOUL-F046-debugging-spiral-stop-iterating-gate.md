```
FINDING ID:      SOUL-F046
DATE:            2026-06-05
WITNESS IDS:     REF-03-011 (reference project: REF-03 — the witness lives in that repo's
                 witness.md, not here; cited as the anchoring instance)
WHAT:            A debugging loop has a point past which iterating on SYMPTOMS yields
                 diminishing returns and the correct move is to STOP and either reach for
                 the architectural root cause or involve the Body — but that point goes
                 unnoticed because each individual re-run feels cheap and responsible. In
                 REF-03-011 the agent ran ~8 headless iterations tweaking timeouts / sleeps /
                 frame-selection against an I/O-staleness flake before reaching the clean
                 root fix (dynamically detach the 4th sensor whose recording I/O was slowing
                 the flush). No single re-run was wrong; the SPIRAL was — and nothing flagged
                 it mid-loop. This is the same activation shape as SOUL-F014 (contraction is
                 cheap and feels responsible; the costly step-back under-fires) and SOUL-F037
                 (Body-input under-asked): the right corrective is intrinsically hard to
                 auto-detect, so it needs an EXPLICIT discipline firing at a named trigger —
                 e.g. "N failed same-symptom iterations → mandatory step-back: write the
                 root-cause hypothesis, or ask the Body." The seed maps "Judge in failure" to
                 the systematic-debugging / diagnose skills, but those are Surface-when
                 candidates that do not auto-fire — the same activation gap, now on the
                 debugging axis.
WHY NOT YET AMENDMENT:  One anchoring instance (REF-03-011). To graduate to doctrine it needs
                 (a) ≥2–3 more instances across different work showing the spiral recurs and
                 is not a one-off, (b) a validated TRIGGER — what counts as "same symptom,"
                 what N (3? 5?), what signal distinguishes legitimate iteration from a spiral
                 — since a too-eager gate would punish normal red-green loops (cf. tdd), and
                 (c) reconciliation with the existing systematic-debugging mapping so it adds
                 a missing ACTIVATION trigger rather than duplicating the skill's content.
                 Candidate landing once earned: an Activation Discipline sibling in
                 SOUL-A012 (a "debugging-spiral / stop-iterating" gate on the failure axis,
                 alongside the scope axis F014 and knowledge axis F037), not a new role.
FILED BY:        Skeptic/self (owned as an anti-pattern in REF-03-011), Guardian (named the
                 activation-gap kinship to F014/F037).
RELATED:         [[SOUL-F014]], [[SOUL-F037]]
STATUS:          Open
```
