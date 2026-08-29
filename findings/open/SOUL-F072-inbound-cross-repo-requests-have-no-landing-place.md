# SOUL-F072 — A request sent between two projects has a departure shape and no arrival shape

```
FINDING ID:      SOUL-F072
DATE:            2026-08-28
KIND:            Format gap — one half of a two-sided exchange was worked out in
                 practice; the other half has nowhere to land.
REFERENCE PROJECT: SENSOR-FORGE — "the OUTBOUND half now has a shape: a dated file
                 in the SENDER's docs/ plus a one-paragraph paste-prompt naming the
                 file, the entry point in the receiver's tree, and 'summarise, do
                 not implement'. The INBOUND half still has no landing place; an
                 INBOUND cursor field (path + date) is the cheap fix."
WITNESS IDS:     SOUL-184.
STATUS:          Open — graduated by the Body 2026-08-28. ONE project, one
                 instance — recorded as a single-source finding.
RELATED:         SOUL-A023 (cursor pointer provenance), SOUL-F067 (cursor fields
                 have no expiry), `/soul-handoff`'s cursor template.
```

## The gap

Two projects that both import this contract can send each other work — a
verification request, a brief, a question about a shared surface. The sending side
has been worked out by use: a dated file in the sender's `docs/`, plus a short
paste-prompt naming the file, the entry point in the receiver's tree, and an
explicit "summarise, do not implement."

The receiving side has nothing. The brief arrives as a pasted message into one
session, and when that session ends there is no field in the cursor that says a
request is outstanding, where it came from, or whether it was answered. The next
session in the receiving project cannot know it exists.

## Why it is worth a record despite one source

The asymmetry is structural, not local: this system gives every project a place to
record what it decided and no place to record what it was ASKED. The proposed fix is
one cursor field carrying a path and a date, which costs nothing when empty and is
the same shape as the fields already there.

Weigh it against the opposite pressure, which is real: v2.3.0 removed a cursor field
and v2.3.1's review found the cursor's fields are already under-specified (F067).
Adding one needs to answer why it will not go stale the same way.

## What needs deciding

1. Is one instance enough to change a shipped format, or does this wait for a second?
2. If adopted: does the field expire, and who clears it — the receiving session when
   it answers, or the sender confirming receipt?
