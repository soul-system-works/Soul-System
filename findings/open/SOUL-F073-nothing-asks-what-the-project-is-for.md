# SOUL-F073 — The contract protects the record and never asks what the project is for

```
FINDING ID:      SOUL-F073
DATE:            2026-08-28
KIND:            Scope observation — a whole dimension the system does not ask
                 about, noticed by a project that supplied its own answer.
REFERENCE PROJECT: NAV-TOOL — "The contract protects the record; nothing asks
                 'toward what?' A project-level direction statement had no Soul
                 home; this project wrote one as a docs page and the owner
                 ratified it in one exchange. Worth a store or a `/soul-init`
                 prompt." Second cursor.
WITNESS IDS:     SOUL-184.
STATUS:          Open — graduated by the Body 2026-08-28. ONE project, one
                 instance. It survives the entry test because it names
                 `/soul-init`; it has not been corroborated.
RELATED:         `/soul-init`, `/soul-stage` (v2.2.0 — the precedent: a dimension
                 the contract did not have, added because owners kept supplying it
                 by hand), SOUL-I061.
```

## The observation

The system is not blind to the future — `ideas.md` holds what might be worth doing,
the cursor holds a NEXT STEP, and `/soul-next` proposes actions. But every one of
those is derived from the record: what happened (`witness.md`), what a later session
could not re-derive (`mind.md`), what this project learned about the system
(`upstream.md`). Direction is inferred from where the project has been, never stated.

Nothing anywhere asks what the project is *for*. A session can be fully wired,
fully verified, and pointed somewhere the owner did not intend, and no instrument in
this system would notice — the contract's guarantees are all about the honesty of
the record, not its aim.

## The precedent that makes this credible, and the one that makes it doubtful

**For:** `/soul-stage` exists because owners kept writing the same rule by hand in
their own `CLAUDE.md` files — two projects, two wordings, no shared source. This is
the same shape one step earlier: a project wanted something the contract does not
have, wrote it by hand as a docs page, and the owner ratified it immediately.

**Against:** one project is not two, and "the owner ratified it in one exchange" is
also evidence that the ad-hoc route WORKED. A docs page the owner approves may be the
right answer, with the system correctly staying out of it. `/soul-stage` had two
independent hand-written instances before it was built; this has one.

## What needs deciding

1. Does the system take a position on project direction at all, or is this
   deliberately out of scope?
2. If it does: a store, a `CLAUDE.md` block like the stage's, or a single
   `/soul-init` prompt whose answer lands in the project's own `CLAUDE.md`?
3. Does it wait for a second independent instance, as `/soul-stage` effectively did?
