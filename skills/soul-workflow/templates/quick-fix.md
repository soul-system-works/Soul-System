---
name: quick-fix
description: one try at the lowest rung, the reviewers once, no repair round
---

# quick-fix — a small, cheap change with a second opinion

Copy this file to `.claude/soul-workflows/<your-name>.md` in a project (or
`~/.claude/soul-workflows/` for every project), change `name`/`description` and the
steps, and run it with `/soul-workflow <your-name>`. The steps refer to build-verify's
numbered steps in the soul-workflow skill and to roles in your roles table.

1. Settle the work and write the brief (build-verify steps 1–2). The work must have
   a Done-when command.
2. Dispatch `implementer` at its lowest rung, one attempt — no retry, no escalation
   (build-verify steps 3–4).
3. Review the winner with `reviewer` (build-verify step 5).
4. No repair round. Apply the winner only if no finding was accepted (step 7);
   otherwise leave it on its branch. Report (step 8), with any accepted findings as
   open items for the owner to decide.

<!-- Optional: this workflow's own models. Remove the comment marks around this block to
make Codex the only reviewer for this workflow; roles this section does not name keep
the rows of the shared roles table. `/soul-workflow roles <your-name>` shows the result.

## Roles

| role     | harness | model   | settings |
|----------|---------|---------|----------|
| reviewer | codex   | default |          |
-->
