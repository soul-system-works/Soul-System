# Idea Inbox — Design Spec

**Date:** 2026-05-20
**Status:** Approved in brainstorming — pending implementation plan
**Topic:** A lightweight, forward-looking idea-capture mechanism for the Soul System.

## Problem (two levels)

- **Immediate:** the Body has no seamless way to capture future ideas as they
  arise, in a structure that can mature over time and be worked by Council roles.
- **Larger system:** the Soul System is a "good ratchet, poor engine"
  (SOUL-F001 / SOUL-F014) — strong at contraction/verification, weak at
  expansion/possibility. The idea inbox is the *persistence* half of the
  expansion engine: where forward possibilities live and mature, feeding
  Findings / Amendments / work.

## Decisions (settled in brainstorming)

1. An idea is a **lighter, upstream artifact than a Finding** — raw, pre-Council,
   unprioritized — that **graduates** into a Finding/Amendment/work when it earns it.
2. **Minimal at capture, enriched later** — capture stays frictionless; structure
   accrues as the idea matures.
3. **Maturation is manual in v1** (Body-initiated). No background automation.
4. **Form: a single append-only `ideas.md` at the project root** (the forward twin
   of `witness.md`) + a `/soul-idea` capture command. Not a per-file directory;
   not an extension of `findings/`.
5. **No new role.** The Archivist tends it; the Prophet is the primary worker;
   Researcher/Revelator develop on demand.

## The artifact: `ideas.md`

Location: project root (parallel to `witness.md`). Self-documenting header — the
format lives with the artifact; no separate operations file (docs-near-code).

Entry, **minimal at capture**:

```
ID:        SOUL-I001
WHEN:      2026-05-20
IDEA:      <one line — the raw thought>
STATUS:    Raw
```

Enrichment (accrues later, all optional):

```
WHY:       <why it might matter>
PRIORITY:  low | medium | high       (set when the Body actually cares)
DEVELOP:   <who/what could flesh it out — Prophet / Researcher / Revelator / /soul-expand>
NOTES:     <research / development notes, accruing>
```

- **ID scheme:** `[PROJECT-CODE]-I###` (e.g. `SOUL-I001`) — parallels `-F`
  (finding) and `-A` (amendment).
- **Lifecycle (STATUS):** `Raw → Maturing → Graduated [to <ID>] | Dropped`.
  Never deleted — `Dropped` stays on the record (like Resolved witness entries).

## Capture: `/soul-idea`

`/soul-idea <text>` appends a minimal `Raw` entry (next id, today's date, the
text) to `ideas.md`. The file is the source of truth; the command is a
convenience writer; hand-editing always works. Lives in `commands/` (and
`~/.claude/commands/`), like `/soul-init`, `/soul-verify`, `/soul-expand`.

## Maturation & graduation (manual, v1)

The Body picks an idea, sets `PRIORITY`/`DEVELOP`, and runs `/soul-expand`, a
research subagent, or a Council role; `NOTES` accrue. When ripe, **graduate**:
create a Finding (`SOUL-F###`), set the idea's `STATUS: Graduated [to SOUL-Fxxx]`.

## Ownership (no new role)

- **Archivist** — tends the file (hygiene, never-delete, graduation bookkeeping).
- **Prophet** — primary worker; reads the backlog for trajectory / ripeness.
- **Researcher / Revelator** — develop ideas on demand.

## Doctrine touch (minimal)

- `operations/CLAUDE.md`: a one-line pointer to `ideas.md` plus the synthesis-
  hierarchy note —

  ```
  WITNESS (what happened, backward) ─┐
                                      ├─→ FINDING → AMENDMENT
  IDEAS   (what might, forward)     ─┘
  ```

- `README.md` structure list: add `ideas.md`.

## Out of scope (v1)

- Background subagents working the backlog autonomously.
- A `/soul-ideas` review-pass command (Prophet/Cartographer survey of the backlog).
- Auto-prioritization.
- The generative **Dreamer** role (filed separately — see Related).

The structure leaves room for all of these; none is built until the inbox has
real traffic (YAGNI; the activation-gap lesson — do not build heavy machinery
before the light thing proves useful).

## Success criteria

- Capturing an idea is one command or one line — near-zero friction.
- An idea can mature (enrichment accrues) and graduate to a Finding, with the
  full trail preserved.
- The whole backlog is visible at a glance (one file) and ripe ideas are findable.
- No new role; no new heavy artifact type; one new file (`ideas.md`) + one command.

## Related / deferred

- **SOUL-F017 (to file): is there a missing *generative* role (The Dreamer)?**
  Prophet *extrapolates* trajectory, Revelator *reveals* what is already true,
  Researcher *acquires* existing knowledge — none *invent*. The generative seat
  may be the real missing engine-role (the heart of F014). Decided on its own
  merits with evidence, not bolted onto this sugar feature.
