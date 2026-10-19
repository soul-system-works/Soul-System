# SOUL-F067 — Only the cursor's links carry provenance; everything else is trusted forever, including pointers at things that move

```
FINDING ID:      SOUL-F067
DATE:            2026-08-28
KIND:            Doctrine gap — a marking convention that covers one field of a
                 shipped format and not the rest, and that does not distinguish a
                 fact from a moving target.
REFERENCE PROJECT: Three independent projects:
                 (1) SENSOR-FORGE — "Cursor fields beyond POINTERS carry no provenance or
                     expiry; WHERE WE ARE was stale on arrival three times
                     (08-24, 08-25 x2) and accurate on the first arrival after it
                     was verified at write time and re-verified at resume."
                     Plus a fourth staleness route found later: origin moved under
                     a live session because the owner pushed.
                 (2) SITE-WATCH — "the 08-24 cursor's [read] pin pointer was
                     false on arrival because two later commits moved the pin.
                     [read] proves the session opened it, not that it is still
                     true; A023's marks do not distinguish anchors to immutable
                     facts from anchors to state the repo can move."
                 (3) PLANT-BOP — "the wiring sentinel ran clean; the cursor it
                     loaded was two sessions stale because a /soul-init session
                     wrote no handoff."
WITNESS IDS:     SOUL-183.
STATUS:          Closed 2026-10-19 — ruled by the Body (SOUL-202); amendment
                 SOUL-A028 accepted and applied in v2.8.0.
RELATED:         SOUL-A023 / SOUL-F061 (pointer provenance marks), SOUL-F057
                 (anchor validity hierarchy).
```

## Two distinct holes, found separately and pointing the same way

**Hole 1 — the marks stop at POINTERS.** A023 made every pointer carry `[read]` or
`[inherited]`, and made `[inherited]` expire after three cursors. `WHERE WE ARE`,
`OPEN GATES` and `NEXT STEP` carry nothing. They are written once and read as fact by
every session afterwards. One project measured it: stale on arrival three times, and
accurate the first time only after the session verified it at write time *and* the
next session re-verified it as its opening move.

**Hole 2 — `[read]` conflates two different claims.** For an immutable fact — an ADR
exists, a decision was made — `[read]` is a durable guarantee. For state the repo can
move — a commit, a branch tip, a file's current contents — `[read]` guarantees only
that someone once looked. A pointer marked `[read]` was false on arrival because two
later commits had moved what it pointed at. The mark was honest and the pointer was
wrong.

Hole 2 is the sharper one: it means a correctly-followed convention produced a false
claim, which is the same shape as F061 (the incident that created the convention).

## Candidate shape

- Extend the write-time discipline: whoever writes `WHERE WE ARE` verifies it as they
  write, and whoever resumes re-verifies it as step 0 rather than trusting it. One
  project has run this and reports it worked.
- Split the pointer mark by what it points AT, not by who read it: an anchor to an
  immutable fact keeps `[read]`; an anchor to movable state is marked as such and is
  re-read at resume, never carried.
- The third instance is a different bug in the same family and may be cheaper to fix
  directly: a session that creates stores should leave a cursor, so the next session
  does not load one two sessions old.

## Why this is not just tidiness

The cursor is how every session learns where it is. Its one field with a truth
convention is the one field that is already a link to something checkable. The fields
carrying the actual claims have none.

## Ruled 2026-10-19 (SOUL-202)

**Ruling (the Body): adopt the fix.** Three parts:
1. **Marks extend to carried obligations.** An inherited `NEXT STEP` or `OPEN GATES`
   obligation is checked in the session that inherits it, or dropped. Checked, it
   carries `[read]`. It is not carried `[inherited]` for up to three cursors the way a
   pointer may be (confirmed by the Body, 2026-10-19).
2. **Counts become commands.** A count that goes stale ("N commits unpushed") is not
   written into the cursor. The command that produces it (`git status -sb`) is
   written instead.
3. **Resume lists what landed after the cursor.** It lists commits since the
   cursor's date and record entries newer than it, and says "the cursor does not know
   about X".

**New instances (mining pass 2, three projects):** MODEL-TEST (2026-09-03): an
unmarked carried obligation in `NEXT STEP` was false twice, before the three-cursor
`[inherited]` expiry could act. NOTE-VAULT (2026-08-31): a stale
count rode in `WHERE WE ARE`, by the same "owner pushed in between" route as instance
(1). SENSOR-VIEW (2026-09-28): resume checks that pointers resolve, not what landed
after the cursor.

**Where the fix lands:** `skills/soul-handoff/SKILL.md` (steps 2 and 3) and
`skills/soul-resume/SKILL.md` (step 2), made separately from this record.
