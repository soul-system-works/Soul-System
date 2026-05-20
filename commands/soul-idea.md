---
description: Capture a forward-looking idea into the project's ideas.md inbox with near-zero ceremony. Minimal at capture; enrich later.
---

# /soul-idea — capture a forward possibility

Append a new idea to `ideas.md` at the project root (the forward twin of the
Witness log). Minimal at capture — just the thought; enrichment accrues later.

## What to do

1. Read `ideas.md` in the current project root. If it does not exist, create it
   with the standard header and a `## Ideas` section (see the Soul System repo's
   `ideas.md` for the format).
2. Determine the next idea ID: `[PROJECT-CODE]-I###`, incrementing the highest
   existing `-I` number. Project code comes from the file header (default to the
   project's witness-log code).
3. Append a minimal entry:
   ```
   ID:        [CODE]-I###
   WHEN:      [today's date, YYYY-MM-DD]
   IDEA:      [the user's idea text, one line]
   STATUS:    Raw
   ```
4. Report the ID assigned and confirm capture. Do NOT add WHY/PRIORITY/DEVELOP
   unless the user already supplied that detail — capture is meant to be
   frictionless.

## What not to do

- Do not develop, evaluate, or act on the idea. Capture only. Maturation is a
  separate, later, Body-initiated step.
- Do not create a Finding. Ideas graduate to Findings only when they earn it,
  deliberately.
- Do not reorder or edit existing entries.

---

**Source:** Built by the Artificer for the idea-inbox design
(docs/specs/2026-05-20-idea-inbox-design.md). The forward twin of the Witness
log; capture half of the expansion engine (SOUL-F001/F014). **Adopted:**
2026-05-20. **Status:** active.
