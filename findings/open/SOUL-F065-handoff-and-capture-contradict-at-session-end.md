# SOUL-F065 — Two shipped instructions give opposite orders at session end

```
FINDING ID:      SOUL-F065
DATE:            2026-08-28
KIND:            Doctrine contradiction — two shipped files, both in force at the
                 same moment, telling a session to do opposite things.
REFERENCE PROJECT: Three independent projects, none able to see the others'
                 records, reported the same collision:
                 (1) dvs-nav — "S71 appended #47 and #48 under the handoff's
                     instruction and said so both times." Fifth cursor.
                 (2) NeuroSiteWatch — "This session again resolved it by
                     appending (W022, I023-I025) and reporting prominently,
                     because the cursor is destroyed on replacement and a held
                     draft would be lost. Wants a doctrine ruling." Second cursor.
                 (3) A third project — same collision, fourth ride, same
                     resolution.
WITNESS IDS:     SOUL-183 (the mining pass that surfaced all three).
STATUS:          Open — graduated by the Body 2026-08-28 from the first upstream
                 mining pass. Fix not adopted; the ruling below is a candidate.
RELATED:         SOUL-A022 (capture is the Body's call), SOUL-I062 / v2.3.0
                 (the store these three notes were parked in).
```

## The collision

`/soul-handoff` step 1 says of a witness-worthy moment: **"Add it."**
`/soul-capture` says of idea and witness modes: **draft the entry and hold for the
Body's confirmation before appending** (A022).

Both are in force at the end of a session. When the Body is present the conflict is
invisible — the session asks and gets an answer in seconds. When the Body has walked
away, which is exactly when `/soul-handoff` runs, the two instructions decide
opposite things about the same paragraph.

## Why every instance resolved the same way, and why that is not a fix

All three projects appended and then said so prominently. Their stated reason is
identical and correct: **the cursor is replaced wholesale, so a held draft is
destroyed rather than deferred.** Holding is not "wait for approval" at session end;
it is "discard."

That is three sessions independently reasoning past a shipped instruction because
following it would lose the work. A rule that every instance overrides is not
governing; it is generating apologies. Each of the three wrote an explanation of the
override into its own record — the drift documenting itself.

## What the ruling has to settle

1. Does `/soul-handoff`'s "add it" override A022's hold at session end, or does the
   hold override and the material goes somewhere durable-but-unratified?
2. If append wins: is the entry marked as unratified, and does the Body ever see a
   list of what was appended without them?
3. If hold wins: **where does a held draft live**, given that the only file the
   session is about to write is the one that gets replaced?

Question 3 is the one that makes this a real gap rather than a wording clash. As of
v2.3.0 there is now a durable, append-only place in every project (`upstream.md`)
and an append-only witness log — so "hold" finally has somewhere to hold. The gap
predates that and was never re-examined after it.

## Cost of leaving it

Three projects, five/four/two rides each, all resolving it by override. The record
each of them keeps now contains a paragraph justifying a rule violation that the
system asked for.
