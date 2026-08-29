# SOUL-F068 — Four defects in `/soul-init`, each found by running it somewhere it half-worked

```
FINDING ID:      SOUL-F068
DATE:            2026-08-28
KIND:            Implementation defects in a shipped skill — small, concrete, no
                 judgment calls. Grouped because they share one cause: the skill
                 assumes the common case and says nothing about the others.
REFERENCE PROJECT: Two projects:
                 (1) A notes project that had never been initialised — three of
                     the four defects.
                 (2) PLANT-BOP — the fourth.
WITNESS IDS:     SOUL-183.
STATUS:          Open — graduated by the Body 2026-08-28. Each fix is small enough
                 to apply directly once the Body says which.
RELATED:         SOUL-F038 (silent import failure under `claude -p`), v2.1.0's
                 init rework, v2.1.1's wiring-check sentinel.
```

## Defect 1 — a project with no record has nowhere to put a lesson, and nothing says so

`/soul-handoff` step 1 says to flush anything witness-worthy to `witness.md`. In a
project that never ran `/soul-init`, there is no `witness.md`. The instruction has no
branch for that case, so the material stayed in the cursor: a GOTCHAS block rode four
or more cursors, surviving only because each session happened to copy it forward.

Fix shape: step 1 detects the absent store and either offers `/soul-init` or names a
fallback. Today it silently has nowhere to go.

## Defect 2 — the wiring sentinel has no correct answer when the project has no config

`/soul-resume` step 0 asks the session to prove the contract loaded by answering a
question only the contract contains. In a project with no `CLAUDE.md` at all, the
contract legitimately did not load — but the check has no "correctly not loaded"
outcome, only pass and alarm. A true negative reads as a failure.

Fix shape: name the no-config case as a legitimate NOT-LOADED state with its own
one-line report, distinct from "the import broke."

## Defect 3 — git has three places to hide an ignore rule and init checks one

`/soul-init` step 3b looks in `.gitignore`. In one project the record directory was
ignored via `.git/info/exclude`, which the skill never reads, so it reported the
record as tracked when git was ignoring it. `git check-ignore -v <path>` answers the
real question — which file, which line, which rule — in one call, for all three
locations at once.

Fix shape: replace the file read with the command. Strictly better and shorter.

## Defect 4 — an init session leaves no cursor

A session that ran `/soul-init` wrote no handoff, so the next session loaded a cursor
two sessions old while the wiring check reported everything green. Creating a
project's stores is exactly the kind of session whose state the next one needs.

Fix shape: init ends by writing or updating the cursor, or says explicitly that it
did not.

## Common cause

All four are the same omission: the skill describes the ordinary path and is silent
on the edge, so a session hits the edge and either invents a resolution or reports a
false green. None needs a design decision — only a sentence each.
