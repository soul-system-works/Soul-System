---
name: soul-resume
description: Resume a Soul session from the handoff cursor (.soul/handoff.md) — load the cursor and the durable records it points to, restate where we are, and continue from the next step. The twin of /soul-handoff.
disable-model-invocation: true
---

# /soul-resume — pick up where the last session left off

**Codex:** Read [the host integration](../../operations/codex.md) before
following this workflow. Its Codex procedures replace Claude-specific loading,
instruction-file, tool, and invocation mechanics; the shared workflow follows.

Resume from the handoff cursor without re-deriving state. The durable records are the
source of truth; this loads them and continues.

## What to do

0. **Wiring check — one line, before anything else.** The system's failure mode
   for "you are not actually wired in" has been silence, so say it out loud:

   - **Contract loaded?** State, from context alone and WITHOUT opening any file:
     how many numbered rules the contract has, and what rule 3 requires. A sentinel
     must ask for something this skill does not itself contain — an earlier version
     asked you to quote rule 10's name and printed that name in this very file, so a
     session whose import had silently failed could read the answer here and pass
     (caught by fresh-context review, 2026-08-20). Do not add the answers to this
     file; that re-breaks it.
     If you cannot answer, the `@import` did not resolve: it names a path that does
     not exist on this machine, or the external-import approval dialog was declined
     once and will not ask again, or this is a `claude -p` run where cross-project
     imports fail silently and get confabulated (SOUL-F038). Say which, and do not
     proceed as if doctrine were loaded. Confabulation is the expected failure —
     a plausible answer that is wrong reads exactly like a correct one, so if you
     are not certain the text is in context, treat that as a NO.
   - **Stores found?** Name where they are — project root or `.soul/`. Both are
     valid; a project with neither has never been initialized.
   - **Gate armed?** Check exactly what the hook checks — `_is_soul_project()` in
     `hooks/pre-completion-verify.py`, which scopes on **`witness.md` or
     `.soul/witness.md`, or a specific Soul marker in `CLAUDE.md`,
     `.claude/CLAUDE.md`, `AGENTS.md`, or `AGENTS.override.md`**.
     Nothing else counts. In particular `.soul/events.jsonl` proves only that the
     gate fired at some point in the past, NOT that it still scopes — a project that
     later deleted its `CLAUDE.md` keeps a stale event log and would report armed
     while running ungated, which is the exact failure this check exists to end.
   - **Mind loaded?** Only if a `mind.md` exists (`.soul/` or root): state one of
     its items from context alone, WITHOUT opening it. Cannot → it is not loaded:
     nothing imports it, or the import path is wrong. An `@` path resolves against
     the file that holds it, so `@.soul/mind.md` written into `.claude/CLAUDE.md`
     points at `.claude/.soul/mind.md` — MODEL-TEST's Mind sat unloaded
     that way, invisible to the checks above (mining pass 2, SOUL-202). Same
     confabulation caution as the contract sentinel. No `mind.md`: say nothing.

   Report only what is BROKEN — one line, and the repair is `/soul-init`, which is
   idempotent and backfills whatever is missing. All green: say "wiring ok" and
   move on. Do not recite passing checks (the SOUL-055 gap-only discipline).

   *Why this exists:* one adopting project relocated its record into `.soul/` and
   dropped its `CLAUDE.md`, matching neither arm of the completion hook's scoping
   predicate. It ran with the verification gate disabled for three months while
   remaining the second-heaviest record user in the set, and nothing ever said so
   (2026-08-20 cross-repo retrospective). The predicate is fixed; this check is
   what makes the *next* wiring failure visible instead of silent.

1. **Read `.soul/handoff.md`** (the cursor). If it does not exist, fall back: read the
   `witness.md` tail, `ideas.md`, the Mind, and the task tracker (plus `findings/`
   only in the Soul System repo — domain projects have none); report the
   state; and ask the Body for direction.
2. **Resolve every pointer the cursor names** (A023/F061), in priority order — witness
   tail, ripe ideas, the task tracker, the named specs/ADRs. Actually
   read what resolves, so the durable state is in context; don't just glance at the
   cursor. When a named path or artifact **cannot be found, report the miss explicitly**
   ("cursor names X; X not found") — a miss is a signal worth surfacing, never a silent
   skip. The pointer most in need of resolution is exactly the one that doesn't resolve.
   Treat `[inherited]` pointers, OPEN GATES and NEXT STEP items (and any unmarked ones
   from older cursors) as claims to verify before repeating them to the Body — a cursor
   entry is a claim, not a fact (F067).

   **Then list what landed after the cursor** — `git log --since=<cursor date>
   --oneline`, plus record entries (witness, ideas) newer than the cursor's witness
   tail — and say "the cursor does not know about X" for each that bears on its
   claims. A date-only `--since` also lists that day's earlier commits; over-listing
   is the safe direction. Resolving pointers proves they exist, not that nothing
   moved since: the owner pushing in between is a recorded staleness route (F067),
   and SENSOR-VIEW found a resume blind to what landed after its cursor (mining
   pass 2, SOUL-202).
3. **Restate, in 2–3 lines:** where we are · the live design frame (if any) · the
   next step · and, if a line in the project's CLAUDE.md starts `**Stage:`, the
   stage in one phrase ("stage: pre-release since 2026-08-26"). Say nothing about
   stage when there is no line — absence is the default, not a gap. Under a
   `plain` register (the project CLAUDE.md's Register line), say "the current
   design frame" rather than "the LIVE AL"; plain language throughout.

   **Then name every `UNCONFIRMED` id the cursor lists** — entries appended while
   the Body was away (F065) — and ask the Body to ratify each. Yes → remove the
   `unconfirmed — owner to ratify` mark. No → the entry stays and says so,
   corrected forward: a witness entry's `STATUS` records the no; an idea gets
   `— declined by the Body <date>` appended (`/soul-capture`, *Who fires this*).
   No answer → leave the mark; the next `/soul-handoff` lists it again.
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
handoff (SOUL-I007). **Amended:** SOUL-A023 (2026-07-16) — resolve-and-report-misses,
from F061 (the unresolvable pointer is the one most in need of resolution).
**Amended:** 2026-10-19 (mining pass 2, SOUL-202) — step 0 gains the Mind-loaded
check; step 2 treats inherited gates/next steps as claims (F067) and lists what
landed after the cursor; step 3 puts the cursor's `UNCONFIRMED` ids to the Body
(F065). **Adopted:** 2026-05-21. **Status:** active.
