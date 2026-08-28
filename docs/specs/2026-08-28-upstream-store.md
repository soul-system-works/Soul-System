# The upstream store — a durable, silent home for project→system lessons (Soul System → 2.3.0)

**Status:** applied 2026-08-28 (v2.3.0), fresh-context reviewed, 15 findings
applied. **Register:** plain.

## The problem, in one paragraph

A project that imports the Soul contract sometimes learns something about the Soul
System itself — a command that misfired, a gate that helped or got in the way, a
doctrine sentence that did not survive contact. Since v2.1.1 (2026-08-20) the only
place to put that is the `OWED UPSTREAM` field of `.soul/handoff.md`. That file is
gitignored and rewritten from scratch every session, so a parked lesson is one
careless `OWED UPSTREAM: none` away from being gone forever. v2.1.1 could not make
the storage durable, so it made the session **shout** instead: carry it forward, and
if an entry has ridden three cursors, say so in the field and tell the Body.

The shouting works — it is how the sixteen stranded RSF items became visible. But it
fires in the adopting project's session, where the owner can do nothing about it, and
it reads as a request to contribute upstream when it is actually a data-loss alarm.
An adopter who never intends to contribute gets nagged anyway. **Body's call,
2026-08-28: stop showing it.**

Silencing the alarm alone would make things strictly worse — the hazard it guards is
real. Make the storage durable and the alarm becomes unnecessary; the silence then
comes for free, and correctly.

## What is actually out there (measured 2026-08-28)

**Twenty-five** `.soul/handoff.md` files exist under `/mnt/d` and `/home/fig` at depth
≤ 6. Seven carry a non-empty `OWED UPSTREAM` block; this repo's own says `none from
this repo`; the rest carry none. Total payload: **216 non-blank lines** across the
seven.

An earlier draft said "nineteen projects on this machine" and "~230 lines". Both were
wrong, and wrong in the way this repo has a record of: a **confident count from an
unstated — here, mis-stated — scope**. Nineteen was a depth-2 sweep of three parent
directories presented as "on this machine"; six nested adopting projects were outside
it. ~230 came from per-project sizes each inflated by exactly 2 (a `grep -n` span
counted as content). Kept visible rather than silently corrected — the same reason the
falsified size prediction below is kept.

**Names deliberately omitted from this file:** every real filesystem path, and the
client codebase among the seven. Public main anonymises reference projects (mind 5c).
Project codes already public on main (`RSF`, `SENSA-###`) are used where they aid
precision; the omission claim covers paths and the client project, not every string.

## Decisions this plan implements

1. **A durable store: `upstream.md`.** Append-only, same handling as `witness.md`.
   Location follows the project's existing record layout — `.soul/upstream.md`, or
   the project root if that is where `witness.md` and `ideas.md` already live.
   Detect, never assume (the Stores rule).
2. **Not scaffolded at init.** The file is created on first append and not before.
   Precedent: v2.1.0 removed the `findings/` scaffold because three projects carried
   permanently empty directories that told them a store existed when it did not.
   Twelve of nineteen projects here have nothing owed upstream and should get no file.
3. **The cursor field is deleted, not moved.** `OWED UPSTREAM` disappears from the
   `/soul-handoff` template. The carry-forward clause about it and the three-cursor
   escalation go with it — both existed only to compensate for volatile storage.

   **A predicted reduction that did not happen — measured twice.** The draft of this spec
   claimed `/soul-handoff` would lose ~14 lines and the contract ~3. After the edits:
   `/soul-handoff` 121 → 122, contract 81 → 81. After the fresh-context review's fixes:
   `/soul-handoff` 121 → **140**, contract 81 → **82** (5506 → **5597** bytes), **+90
   lines** across nine files. The always-on cost went slightly UP. Deleting the nagging
   removed about nineteen lines; *stating* that a session must not nag cost about as
   many, and the review then added a one-time upgrade check, a tracking rule and a
   stronger repo guard on top. The reduction here is **behavioural, not textual** — an
   adopting project's session stops emitting the escalation, and that is the whole win.
   The original claim is left visible above rather than quietly rewritten, because "this
   simplifies things" is exactly the kind of prediction that goes unchecked once a change
   ships.

4. **The visibility rule, stated as doctrine so it cannot drift back:** at most ONE
   short clause when something is appended — *"noted upstream: `git checkout --` is
   not a sabotage undo."* Never a count, never a reminder, never an escalation, never
   an unprompted mention in a domain project. The obligation stays; the nagging ends.
5. **Reporting moves to where someone can act on it.** `/soul-next`, and only when run
   in the Soul System repo, reports how many unmined entries the registered projects
   hold. That is the seat where a mining pass can actually be run.
6. **No ids.** Entries are dated headings, not numbered records. Numbering invites a
   scheme, a scan, and the `SOUL-F001` collision trap that v2.1.1 had to fix by hand.
   An entry is identified by its date and title; mining stamps it in place.

### Entry format

```markdown
### 2026-08-24 · `git checkout --` is not a sabotage undo

A file with uncommitted work loses it; the undo assumption came from the committed
case and nothing said so.  → SENSA-056
```

Absence of a status line means unmined — the common path costs nothing to write. The
mining pass appends one line to the entry it collects:

```markdown
**Mined:** 2026-08-28 → SOUL-I063
```

Editing a status line inside an append-only store is already the house pattern
(`witness.md` entries carry a `STATUS:` that gets resolved).

### The tracking decision (taken 2026-08-28; say so if you disagree)

**Is `upstream.md` tracked in git?** Default: follow whatever the project chose for
its record at `/soul-init` — tracked if `witness.md` is tracked, gitignored if the
project put its record under a gitignored `.soul/`. No new question at init, and
consistent with the rest of the record. **The wrinkle:** these notes sometimes name
client work (one of the seven blocks does). If you want it always-private regardless of
the project's record choice, say so and Task 1 writes that instead.

## File map

| File | Change |
|---|---|
| `skills/soul-handoff/SKILL.md` | step 1b rewritten (append, don't park); `OWED UPSTREAM` removed from the template; the carry-forward and escalation paragraphs about it deleted |
| `skills/soul-capture/SKILL.md` | finding-mode STEP 0 routes to `upstream.md`, not the cursor |
| `skills/soul-distill/SKILL.md` | line ~50: domain-project record is witness + ideas + `upstream.md` |
| `skills/soul-next/SKILL.md` | new Soul-System-only step: unmined-entry report |
| `operations/CLAUDE.md` | the Stores sentence and the "Projects importing this contract" paragraph trimmed |
| `docs/using-the-soul.md` | line ~18 updated |
| `tools/upstream-migrate.py` | **new** — dry-run-first migration of the seven cursors |
| `registry/` | refreshed against the nineteen cursors on disk (gitignored, local only) |
| `SYSTEM-VERSION.md` | v2.3.0 row |
| `skills/soul-stage/SKILL.md` | **unchanged** — its Source note cites "an adopting project's OWED UPSTREAM item", which is true history and stays |

## Tasks

### Task 0 — Branch and capture the idea
`git checkout -b v2.3.0`. Capture the idea in `ideas.md` (next id `SOUL-I062`; note
that id is also offered to the private-map-scan idea in the current cursor's Open Body
Call 6 — assign at write time, do not pre-assign). No id reservation anywhere else
(SOUL-182: the reservation has been removed three times).

### Task 1 — The store, and the migration script

Write `tools/upstream-migrate.py`. For each project path given (or read from
`registry/`):

1. Read `.soul/handoff.md`; extract the block between `OWED UPSTREAM` and the next
   **known** cursor field label. Skip if empty or the literal `none`. Project paths
   come from explicit arguments, `--registry` (default `registry/PROJECTS.txt`), or
   `--sweep <dir>`. An unrecognised column-0 label inside the field is a **refusal**,
   not a boundary: treating it as one truncates the block and leaves the remainder in
   the cursor with its own label deleted, which the next handoff then destroys — and
   the losslessness check cannot see it, because it only inspects lines inside the
   block it already extracted (fresh-context review, reproduced).
2. Detect the project's record layout (root `witness.md` vs `.soul/witness.md`) and
   choose the target path accordingly.
3. Write the block into `upstream.md` under one dated heading per item where the
   source was already itemised, preserving the project's own words verbatim. Where the
   source is unnumbered prose, one heading for the whole block, dated from the cursor.
4. Rewrite the cursor with the `OWED UPSTREAM` field removed.

**Dry-run is the default.** `--apply` is required to write. The dry run prints, per
project, the target path and a unified diff of both files. **Nothing is applied until
the Body has read the dry run** — this script's failure mode is destroying exactly the
material the change exists to protect.

Keep the original cursor text in `<project>/.soul/handoff.md.pre-2.3.0` until the Body
confirms the migration landed; delete on confirmation.

### Task 2 — `/soul-handoff`

- Rewrite step 1b: *did this session learn something about the Soul System itself?
  Append it to `upstream.md` (create it if absent) in the project's own words, and say
  one short clause about it. Do not write into the Soul System repo from here.*
- Remove `OWED UPSTREAM` from the cursor template.
- Delete the `CARRY FORWARD` paragraph's `OWED UPSTREAM` sentences and the
  three-cursor escalation. **Keep** the rest of CARRY FORWARD (open gates, unexpired
  `[inherited]` claims) and **keep** the `[inherited]` expiry rule — both are about
  pointers and are unrelated to this change.
- Delete the closing "`OWED UPSTREAM` is not decoration" paragraph; its content
  (invented by hand in a project that had a lesson and nowhere to send it; two upstream
  notes in four months across six projects) moves into the v2.3.0 changelog row so the
  incident survives its rule (F045 force preservation).
- Add the visibility rule from decision 4, in the skill's *What not to do*.

### Task 3 — `/soul-capture` finding mode

STEP 0's non-Soul-System branch: write the drafted finding into `upstream.md`, tell
the Body in one clause, stop. Steps 4–8 still do not apply. The `SOUL-F001` collision
guard stays exactly as written.

### Task 4 — Contract trim (`operations/CLAUDE.md`)

- Stores paragraph: `…a project's system-level lessons go in `upstream.md` beside the
  other stores.`
- The "Projects importing this contract" paragraph collapses from five lines to about
  two: they owe system-level lessons upstream; append them to `upstream.md` as they
  happen; the Soul System collects them on a periodic pass; do not write into that repo
  from here; domain lessons stay home.

This paragraph is always-on text in every adopting project — the trim is the reason
it is worth doing carefully.

### Task 5 — `/soul-next` reports, in this repo only

A new step, guarded on being in the Soul System repo (the same test `/soul-capture`
STEP 0 uses: this repo's `witness.md` uses `SOUL-###` and `findings/open/` exists):

> Read `registry/` for adopting-project paths. For each, count unmined entries in its
> `upstream.md` (headings without a `**Mined:**` line). If the total is non-zero,
> surface one Later-tier line: *"N unmined upstream notes across M projects →
> mining pass."*

`registry/` is gitignored, so this is a local-only capability and the paths never
reach the public repo. Refresh it in this task: it holds eight entries from
2026-06-09 against nineteen cursors on disk.

**Honest limit:** this fires only when the Body runs `/soul-next` here. There is no
scheduled collector, and this plan does not build one. That is a deliberate trade —
the durable store means an uncollected note is stale, not lost.

### Task 6 — Lifecycle page, version, changelog

`docs/using-the-soul.md` line ~18. `SYSTEM-VERSION.md` v2.3.0 row carrying the
incident from Task 2 and the seven-project measurement above.

### Task 7 — Fresh-context review before merge

`diff-reviewer` over the applied result. Five for five on releases this week (16 + 12
+ 16 findings; one a false record claim, one an ordering defect two releases old).
Non-negotiable per the current cursor's Suggested Roles.

### Task 8 — Release

Private-map name scan over the diff **and every commit message** (mind 5c) — the
migration touches a client codebase whose block may name real systems, and the
record's anonymisation tokens exist for exactly this. Merge, delete the branch, push `main` and the tag by
**explicit refspec** (SOUL-182: a branch and tag sharing a name makes a bare refspec
ambiguous). Never `--tags`. Then update the plugin cache.

### Task 9 — The live run (A019: the primary artifact gets its executor)

After release, run `/soul-handoff` in one domain project that has something owed —
the largest of the seven is the obvious one — and confirm: it appends to `upstream.md`, says one clause,
and the cursor comes back with no `OWED UPSTREAM` field and no nagging. Record the
result as the next witness entry here. A defect becomes v2.3.1.

## Verification ledger (rule 4)

| Claim | How it is verified | Status |
|---|---|---|
| 25 cursors on disk, 7 non-empty, 216 payload lines | filesystem sweep at depth ≤ 6, 2026-08-28 | **run** |
| The migration extracts and rewrites correctly | dry run, then applied to 7 projects; losslessness re-checked against the `.pre-2.3.0` backups independently of the script's own `verify()` — 47 entries, 0 lines lost, 0 entries rendering as code blocks | **run** |
| The two silent-loss paths are closed | both reproduced on synthetic cursors, both now refuse | **run** |
| `--stamp` can clear a mined entry | exercised end-to-end (one delivered item stamped; the count fell 47 → 46) | **run** |
| `hooks/test_scope.py` still 11/11 | run on this tree | **run** |
| The skills' prose changes work | fresh-context `diff-reviewer` (Task 7) — 15 findings, all applied | **run** |
| A real `/soul-handoff` under the new rules | Task 9, the live run in an adopting project | **UNRUN** |
| The one-time upgrade check (F1) fires on a pre-2.3.0 cursor | no cursor on this machine still carries the field, so it cannot be exercised here | **UNRUN — handed forward** |

Prose with no executor is the same class of risk as v2.1.0 and v2.2.0, both of which
shipped unrun and both of which needed a point release. Task 9 is the executor;
whether it runs before or after the cut is the Body's release-first call, stated out
loud either way (rule 8).

## What this plan deliberately does not do

- **No opt-out flag.** With a silent append and a file that only exists once something
  is owed, the cost to a non-contributing adopter is one short clause, once. A flag
  would be more doctrine for no gain.
- **No scheduled mining.** Named as a limit above rather than hidden.
- **No change to the completion gate, the hook, or the contract's numbered rules.**
