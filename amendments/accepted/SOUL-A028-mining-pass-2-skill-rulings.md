AMENDMENT ID:    SOUL-A028
DATE:            2026-10-19
WITNESS IDS:     SOUL-202 (the second upstream mining pass and the Body's rulings
                 on it). Findings SOUL-F065, SOUL-F066, SOUL-F067 carry the
                 analysis and the new instances from adopting projects.
WHAT CHANGES:    The skill-level half of the 2026-10-19 rulings (the contract and
                 gate half is SOUL-A027).
                 (1) F065 — /soul-capture and /soul-handoff agree on the
                 Body-away case: a model-proposed capture is appended, marked
                 `unconfirmed — owner to ratify`, and the next /soul-handoff lists
                 it in the cursor's new UNCONFIRMED field by scanning the stores for
                 the mark (capture never writes the cursor). At handoff the cursor
                 is written first and the drafts shown after; a "go" removes the
                 mark, and /soul-resume puts any left to the Body. Holding is
                 reserved for mid-session, when the Body is there.
                 (2) F066 — /soul-distill's line budget is a target, not a gate:
                 ~80 lines triggers a review that re-justifies every entry; 80–120
                 is acceptable with whole-entry cuts only and no line-shaving;
                 above 120 the Body takes the weakest cuts or raises the cap out
                 loud. Growth is always reported in lines and items, and needs no
                 sign-off when every new entry passes the anchor and
                 unguessability tests; above the 120 cap the Body decides
                 (confirmed by the Body, 2026-10-19). Force wins over
                 the budget.
                 (3) F067 — /soul-handoff extends provenance marks to carried
                 NEXT STEP and OPEN GATES obligations: an inherited one is checked
                 in the session that inherits it, or dropped, not carried up to
                 three cursors (confirmed by the Body, 2026-10-19). It
                 replaces counts in WHERE WE ARE with the command that produces
                 them; /soul-resume lists what landed after the cursor.
                 (4) Smaller fixes from the same pass: distill re-checks executable
                 anchors, requires a falsifier for prohibitions, keeps item numbers
                 stable and writes its draft to `.ai/`; handoff runs before long
                 unattended runs and checks (rather than asserts) that the cursor
                 is gitignored; init finds an existing store under `docs/`, asks
                 whether the repo is public before the tracking question, and
                 writes the Mind import relative to its file; resume checks that
                 an existing Mind actually loaded; the "name the file that would
                 change" list includes operations docs and tools.
WHERE IN SOUL:   skills/soul-capture, soul-handoff, soul-resume, soul-init,
                 soul-distill (SKILL.md each); operations/CLAUDE.md upstream
                 paragraph (the file list only).
QUESTION ONE:    Evidence — SOUL-202 records the pass; F065 had four sessions in
                 four projects append-and-say-so, F066 two projects' distills (one
                 against the cap, one over the growth check's missing unit), F067
                 three new instances in three projects.
QUESTION TWO:    Necessity — each finding names a contradiction or a hole the
                 skills left open; the Body's ruling resolves which side wins.
QUESTION THREE:  Coherence — append-only stays intact (an unconfirmed entry is
                 corrected forward, never deleted); the Body stays the authority
                 (finding graduation is never unattended; the cap above 120 is the
                 Body's); the cursor stays thin (one new field, marks are tokens).
                 What would make this wrong: a later pass showing unconfirmed
                 entries go unratified and pile up, or Minds drifting past 120
                 because the band reads as a licence.
STATUS:          Accepted 2026-10-19 by the Body ("yes to all", SOUL-202; the two
                 provisional rulings confirmed, SOUL-203). Applied in v2.8.0.
