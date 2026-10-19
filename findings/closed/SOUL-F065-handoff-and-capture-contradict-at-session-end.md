# SOUL-F065 — Two shipped instructions give opposite orders at session end

```
FINDING ID:      SOUL-F065
DATE:            2026-08-28
KIND:            Doctrine contradiction — two shipped files, both in force at the
                 same moment, telling a session to do opposite things.
REFERENCE PROJECT: Three independent projects, none able to see the others'
                 records, reported the same collision:
                 (1) NAV-TOOL — "S71 appended #47 and #48 under the handoff's
                     instruction and said so both times." Fifth cursor.
                 (2) SITE-WATCH — "This session again resolved it by
                     appending (W022, I023-I025) and reporting prominently,
                     because the cursor is destroyed on replacement and a held
                     draft would be lost. Wants a doctrine ruling." Second cursor.
                 (3) A third project — same collision, fourth ride. Its note
                     records ONLY the collision: no append, no override, no
                     explanation. Do not read it as a third instance of the
                     override (corrected 2026-08-28 by fresh-context review; the
                     first draft of this finding and the commit message at
                     40311b9 both said "same resolution", which the record does
                     not support).
WITNESS IDS:     SOUL-183 (the mining pass that surfaced all three).
STATUS:          Closed 2026-10-19 — ruled by the Body (SOUL-202); amendment
                 SOUL-A028 accepted and applied in v2.8.0.
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

**Two of the three** appended and then said so prominently. Their stated reason is
identical and correct: **the cursor is replaced wholesale, so a held draft is
destroyed rather than deferred.** Holding is not "wait for approval" at session end;
it is "discard." The third project recorded the collision and nothing else — it is
evidence that the conflict is noticed independently, not evidence of a third override.

Two sessions in different projects independently reasoned past a shipped instruction
because following it would lose the work, and each wrote the justification into its
own record. A rule that its instances override is not governing; it is generating
apologies. Two of three is still the strongest signal in the pass, and stating it as
three of three — which the first write-up did — would have made the entry's central
claim unsupported by its own sources.

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

Three projects, five/four/two rides each; two of the three resolved it by override. The records of those two now contain a paragraph justifying a rule
violation the system asked for.

## Ruled 2026-10-19 (SOUL-202)

**Ruling (the Body, "yes to all" on the mining-pass-2 recommendations).** When the
Body is away, a capture **appends**. The entry is marked `unconfirmed — owner to
ratify` and listed in the cursor, so the Body sees what was appended without them.
This answers questions 1 and 2 above. Question 3 (where a held draft lives) falls
away, because nothing is held. Reason: the record is append-only and corrected
forward, so a wrong entry costs little, and a held draft lost with the cursor cannot
be recovered.

**New reports of the collision (mining pass 2):** SENSOR-VIEW (2026-09-01): "hold for
confirmation" has no branch for an autonomous run the Body authorized. SUB-K
(2026-09-03): "hold" has nowhere durable to hold. That
entry's further claim, that the cursor has no copy in git history, is false in at
least one project, GAME-THERMAL, which tracks its cursor.

**Where the fix lands:** A022's block in `skills/soul-capture/SKILL.md` and step 1 of
`skills/soul-handoff/SKILL.md`. Those changes are made separately from this record.
