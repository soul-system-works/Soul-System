```
AMENDMENT ID:    SOUL-A001
DATE:            2026-05-19
WITNESS IDS:     SOUL-001..007 as accumulated context; gap surfaced by Body
                 during Decision 5 finalization (Archivist folder structure work)
WHAT CHANGES:    Add `## Log Location and Lifecycle` section to
                 operations/witness-log-format.md codifying three phases:
                 Active / Archived / Retired. Steward operates rotation.
                 Cadence project-dependent, not time-fixed. Retirement rare,
                 deliberate, git-preserved.
WHERE IN SOUL:   operations/witness-log-format.md — Log Hygiene area, expanded
                 with new section. The change is to the operational doctrine
                 layer (operations/), not philosophy/the-soul.md. "The Soul"
                 in the Amendment system is interpreted broadly to include the
                 operational doctrine layer.
QUESTION ONE:    Evidence — Body raised the file-lifecycle gap during Decision
                 5 finalization. Existing doctrine ("Entries are never deleted.
                 Resolved entries are marked Resolved, not removed.") addressed
                 entry-level rules but was silent on file-level lifecycle. The
                 7-entry log will scale; without policy it becomes noise,
                 abandoned, or requires heroic maintenance. Body's mental model
                 (write → archive → cleanup, history reconstructable) operates
                 at a longer timescale than existing doctrine addressed.
QUESTION TWO:    Necessity — current doctrine cannot answer "when does the active
                 log rotate?" or "can old archives ever be removed?" Without
                 file-level lifecycle, the witness log practice does not survive
                 long-running projects.
QUESTION THREE:  Coherence — extends, does not contradict. Entry-level
                 never-delete survives intact. File-level lifecycle is new
                 territory the doctrine had not yet mapped. No contradiction
                 found.
ACCEPTED BY:     Judge
FILED BY:        Archivist
```

---

## Council Convening Summary

**Convened:** 2026-05-19 during Decision 5 finalization.

**Voices heard:** Archaeologist, Steward, Cartographer, Prophet, Skeptic, Advocate, Judge.

**Key tensions resolved:**
- Doctrine's "never delete" vs. Body's "eventually clean up" — resolved by distinguishing entry-level from file-level rules.
- Distinction between Archive and Retirement — Archive is in-repo read-only; Retirement is removed-from-working-repo with git preserving history.
- Cadence — project-dependent triggers, not time-based schedules. Steward judges.

**Why not just a Finding:** This extends doctrine in a substantive way. File-level lifecycle was undefined; this defines it. Three Amendment Questions pass cleanly. Filing as Finding would leave the doctrinal gap open.

**Significance:** First Amendment filed in the Soul System's own Council process. Dogfood signal — the Amendment mechanism is validated by use, not just documented in council-synthesis.md.

---

## The Specific Change

Added the following section to `operations/witness-log-format.md`, placed after `## Log Hygiene`:

```markdown
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
```
