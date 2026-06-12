---
name: soul-resume
description: Resume a Soul session from the handoff cursor (.soul/handoff.md) — load the cursor and the durable records it points to, restate where we are, and continue from the next step. The twin of /soul-handoff.
disable-model-invocation: true
---

# /soul-resume — pick up where the last session left off

Resume from the handoff cursor without re-deriving state. The durable records are the
source of truth; this loads them and continues.

## What to do

1. **Read `.soul/handoff.md`** (the cursor). If it does not exist, fall back: read the
   `witness.md` tail, `ideas.md`, open `findings/`, and the task tracker; report the
   state; and ask the Body for direction.
2. **Load the pointers the cursor names**, in priority order — witness tail, open
   findings, ripe ideas, the task tracker, the named specs/ADRs. Actually read them so
   the durable state is in context; don't just glance at the cursor.
3. **Restate, in 2–3 lines:** where we are · the live design frame (if any) · the
   next step. Under a `plain` register (the project CLAUDE.md's Register line), say
   "the current design frame" rather than "the LIVE AL"; plain language throughout.
4. **Continue from the NEXT STEP** — but if it is a non-trivial build or a decision the
   Body should make, confirm first rather than diving in (explore before execute).

## What not to do

- Do **not** re-read the whole prior conversation or re-derive the abstraction layer —
  the cursor plus the durable records ARE the resume.
- Do **not** silently change the plan the cursor records; if you think it should change,
  say so explicitly.
- Do **not** treat a missing cursor as an error — fall back to the durable records.

---

**Source:** Built by the Artificer as the twin of `/soul-handoff`
(docs/specs/2026-05-21-soul-handoff-design.md); the resume half of the context-limit
handoff (SOUL-I007). **Adopted:** 2026-05-21. **Status:** active.
