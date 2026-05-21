# Soul Handoff — Design Spec

**Date:** 2026-05-21
**Status:** Direction approved with the Body (grow-own, thin) — spec-first per
explore-before-execute; then the `/soul-handoff` command.
**Topic:** A lightweight, Soul-native session handoff at the context ceiling.

## Problem (two levels)

- **Immediate:** at the context ceiling there is no disciplined handoff — the next
  session re-derives the abstraction layer, open gates, and witness state. `/compact`
  gives a generic prose summary that *loses* the Soul-specific state.
- **Larger system:** the Soul System's value is accumulated structure (AL, witness,
  findings, ideas). A handoff is exactly where that structure should pay off — and
  where the token-economics bet (SOUL-I005) becomes visible. Carry the structure
  forward so the next session resumes without re-derivation.

## Decision (settled with the Body)

1. **Grow-own, not point-to.** The borrowed part (Pocock / generic handoff) is
   trivial; the value is all Soul-specific.
2. **Don't rebuild `/compact`.** Lean on the built-in summarizer for the prose recap;
   the handoff owns only the Soul delta `/compact` discards.
3. **Thin command, not a parallel system.** The durable records already persist most
   state; the handoff = *flush volatile → durable* + *a small cursor*.
4. **Keep Pocock's one good principle:** reference, don't duplicate.

## The abstraction layer

- **What varies:** the session content, what is mid-flight, the next-session focus.
- **What decides whether it varies:** the agent at handoff time (what is volatile vs
  already-durable).
- **What cannot vary:** the durable records remain the source of truth; the cursor only
  *references* them plus holds the thin volatile delta; nothing the records already
  hold is duplicated.

## The artifact: `.soul/handoff.md` (the cursor)

Location: `.soul/handoff.md` — **gitignored runtime state** (a per-transition cursor,
regenerated each handoff, not a durable record; `.soul/` is already ignored). Sections:

- **WHERE WE ARE** — one short paragraph.
- **LIVE AL** — the current abstraction layer if mid-flight (what varies / decides /
  can't vary).
- **OPEN GATES** — any gate mid-evaluation.
- **NEXT STEP** — the immediate next action (the cursor).
- **POINTERS** (reference, not duplicate) — witness tail, open findings, ideas inbox,
  task tracker, relevant specs/ADRs.
- **SUGGESTED ROLES / SKILLS** — for the next session.
- **NEXT-SESSION FOCUS** (optional) — from the command argument.

## The command: `/soul-handoff [focus]`

Steps the agent runs:

1. **FLUSH volatile → durable** (the real work): is the live AL recorded in a spec/ADR?
   any witness-worthy moment unrecorded? any new idea uncaptured? Record them now, so
   the durable records are current.
2. **WRITE `.soul/handoff.md`** with the sections above — references, not duplicates.
3. **Defer the prose recap to `/compact`** — do not reproduce the transcript.

## Resuming (via `/soul-resume`)

Next session: run **`/soul-resume`** — it reads `.soul/handoff.md`, loads the pointers it
names (witness tail, findings, ideas, tasks, specs), restates where we are + the next
step, and continues (pausing to confirm if the next step is a non-trivial build, and never
silently changing the recorded plan). The manual equivalent is "read `.soul/handoff.md`
and continue." **Auto-resume wiring** (a seed note "if `.soul/handoff.md` exists, read it
first") remains **deferred** — it would touch the always-loaded seed (bloat, post-C-lite);
add only if running `/soul-resume` by hand proves annoying. YAGNI.

## Out of scope (v1)

- Auto-resume / seed wiring.
- Secret redaction (Pocock's) — the cursor references durable in-repo files and dumps no
  transcript, so the secret-exposure surface is low; add if a real need appears.
- Multi-agent handoff (the lineage / fan-out case — SOUL-F019 / F011); the cursor is
  single-thread for now.

## Success criteria

- A handoff is one command; the next session resumes from `.soul/handoff.md` + pointers
  without re-deriving the AL.
- The cursor duplicates nothing the durable records already hold.
- It does **not** reimplement conversation summarization (leans on `/compact`).
- Thin: one command + one gitignored cursor file; no parallel system.

## Related

- **SOUL-I007** (the idea this graduates), SOUL-I004 (cheap capture), SOUL-I005 (token
  economics — the handoff is where it shows), SOUL-I010 (the next-step cursor overlaps).
- Matt Pocock's handoff skill (the prior art studied) and the External-Skills doctrine.
