# The Witness Log

The Witness has one obligation — accuracy.

This log is not a journal. It is not an analysis. It is not a place for opinion,
interpretation, or recommendation. Those belong to the Council.

The Witness records what was. Nothing more.

If an entry takes more than five lines something has gone wrong.
If an entry contains the word "should" the Witness has stopped witnessing.
If an entry explains why something happened the Council has been spoken for
before it was consulted.

Write what happened. Where. When. What kind of thing it was.
What it cost, or that the cost is not yet known.
Whether it is still open.

That is all.

---

## Entry Format

```
ID:           [project-code]-[sequential number] e.g. THERMAL-001
WHEN:         [timestamp or project phase] e.g. 2026-05-15 / Session 3 / Implementation Phase
WHERE:        [location in the work — file, method, module, library, document section,
               conversation phase. As specific as context allows.]
              e.g. HeatTransfer.cpp > computeRadiation() > Stefan-Boltzmann constant
WHAT:         [factual description. Two sentences maximum. No interpretation.]
TYPE:         [one of the following]
                - Failure Mode        [name the specific failure mode if known]
                - Obligation Skipped  [name which obligation]
                - Felt Wrong          [unresolved — something noticed, not yet named]
                - Unnamed Tension     [two forces in conflict, not yet resolved]
                - Universe Contradiction [assumption met reality and lost]
                - Multiverse Signal   [evidence the assumed Universe may be wrong]
                - Council Note        [observation for a specific Council role]
CONSEQUENCE:  [damage before named / cost of correction / or: unresolved]
STATUS:       [Open / Resolved / Escalated to Council]
```

---

## Example Entries

---

```
ID:           THERMAL-001
WHEN:         2026-05-15 / Session 1 / Problem Definition Phase
WHERE:        Conversation — problem framing, before any code
WHAT:         Solution proposed before constraints were established. Full physics ODE
              system suggested before fitness for purpose was discussed.
TYPE:         Failure Mode — Premature Sophistication
CONSEQUENCE:  One session lost. Required full reframe to lumped time-constant approach.
STATUS:       Resolved
```

---

```
ID:           THERMAL-002
WHEN:         2026-05-15 / Session 1 / Implementation Phase
WHERE:        ThermalSensor.cpp > updateTemperature()
WHAT:         Convection and radiation terms absent from initial implementation.
              Conduction only. No coverage check performed before proceeding.
TYPE:         Failure Mode — Partial Domain Coverage
CONSEQUENCE:  Required revision pass. Scope of heat transfer domain not mapped at outset.
STATUS:       Resolved
```

---

```
ID:           THERMAL-003
WHEN:         2026-05-15 / Session 2 / Validation Phase
WHERE:        HeatTransfer.cpp > computeRadiation() > Stefan-Boltzmann constant
WHAT:         Equation used but not verified against domain source before implementation.
              Validation only performed after human requested it.
TYPE:         Obligation Skipped — Universe must be consulted before work is called complete
CONSEQUENCE:  Unknown until validation run. Habit pattern: validation treated as optional.
STATUS:       Escalated to Council
```

---

```
ID:           THERMAL-004
WHEN:         2026-05-16 / Session 3 / Architecture Review
WHERE:        ThermalSystem.h — class structure
WHAT:         Something about the inheritance pattern feels wrong. Cannot articulate yet.
              Compiles and runs correctly. The feeling persists.
TYPE:         Felt Wrong
CONSEQUENCE:  Unresolved
STATUS:       Open
```

---

```
ID:           THERMAL-005
WHEN:         2026-05-16 / Session 3 / Architecture Review
WHERE:        ThermalSystem.h — class structure
WHAT:         THERMAL-004 resolved. Inheritance pattern assumes single heat source.
              System requirements allow multiple. Abstraction layer was not completed
              before implementation began.
TYPE:         Failure Mode — Defaulting to Instantiation Layer
              [resolves THERMAL-004]
CONSEQUENCE:  Refactor required. Estimated one session.
STATUS:       Escalated to Council
```

---

## Entry Types — Reference

| Type | Who Acts On It |
|---|---|
| Failure Mode | Council — Prophet, Guardian |
| Obligation Skipped | Guardian, Judge |
| Felt Wrong | Leave open until it resolves or is named |
| Unnamed Tension | Council — Revelator, Skeptic |
| Universe Contradiction | Emissary, Panel of Experts |
| Multiverse Signal | Judge — stop and convene Council immediately |
| Council Note | Address to the specific role by name |

---

## Council Note Format

When a Witness entry is specifically addressed to a Council role,
add the role name to the WHERE field and a direct address in WHAT.

```
ID:           THERMAL-006
WHEN:         2026-05-16 / Session 3
WHERE:        [Cartographer] — ThermalSystem domain boundary
WHAT:         Fluid thermal behavior has appeared at the edge of current scope.
              Current map covers solid body heat transfer only. Boundary not yet mapped.
TYPE:         Council Note — Cartographer
CONSEQUENCE:  Unknown. May require Multiverse assessment.
STATUS:       Open
```

---

## Log Hygiene

The Archivist maintains the log. The Archaeologist reviews it periodically.
The Guardian watches for patterns — the same WHERE appearing repeatedly,
the same TYPE recurring, Obligations Skipped under the same conditions.

**Entries are never deleted.** Resolved entries are marked Resolved, not removed.
The record of what went wrong and how it was corrected is as valuable
as the record of what is currently open.

**The log is not a performance review.** It is evidence for the Council.
Entries that reflect poorly on the session are the most important entries.
A log with no failures is a log that stopped witnessing.

---

## Log Location and Lifecycle

The active witness log lives at the project root as `witness.md`. One file,
append-only, chronological. Entries are added, never modified (except `STATUS`
updates).

The log moves through three phases. Cadence is project-dependent — never time-fixed.

**Active** — `witness.md` at project root. Append-only. Recent context.

**Archived** — `witness/<name>.md`. Triggered when the Steward judges the active
log impedes navigation, or when a natural phase ends (milestone, release,
doctrine amendment). Resolved entries move out of active; Open entries stay.
Archive names follow the project's rhythm — `witness/dogfood.md`, `witness/v1.md`,
`witness/2026-Q2.md` — Steward's call. Archive files are read-only once written.

**Retired** — archived files moved out of the working repo (or pruned). Reserved
for long timescales (project completion plus years, organizational change,
doctrine evolution making old entries reference outdated structures). Git
history preserves what was there. Default is to keep archives indefinitely;
retirement is deliberate and rare.

This preserves the witness record where it's needed, sheds noise where it
isn't, and never makes evidence irretrievable while git history exists.

---

## Naming Convention

`[PROJECT-CODE]-[NNN]`

Project codes are short, consistent, and defined at session start.
Sequential numbers never reset within a project.
Cross-references between entries use the full ID: `[resolves THERMAL-004]`

---

*The Council will refine this format as evidence accumulates.*
