---
name: soul-handoff
description: Write a thin Soul-native handoff cursor (.soul/handoff.md) so the next session resumes without re-deriving state. Flushes volatile state into the durable records first; leans on /compact for the prose recap.
---

# /soul-handoff — hand off to the next session

**Codex:** Read [the host integration](../../operations/codex.md) before
following this workflow. Its Codex procedures replace Claude-specific loading,
instruction-file, tool, and invocation mechanics; the shared workflow follows.

Produce a thin handoff **cursor** so a fresh session resumes where this one left off —
without re-deriving the abstraction layer, open gates, or witness state. The durable
records (`witness.md`, `ideas.md`, `findings/`, specs/ADRs, the task tracker) remain the
source of truth; the cursor only **references** them and holds the thin volatile delta.
Lean on `/compact` for the prose recap — do **not** reproduce the transcript here.

Optional argument: a short description of what the next session is for — let it focus the cursor.

## What to do

1. **Flush volatile → durable** (the real work — do this first):
   - Is the current abstraction layer recorded in a spec/ADR? If it is live and unwritten, record it.
   - Any witness-worthy moment this session not yet in `witness.md`? Add it.
   - Any new idea not captured? Append it to `ideas.md` (minimal).
   - Is the task tracker current? Update it.
   - Any counter-default fence relied on this session? Verify its **force** — the incident
     and the explicit negation, not just the rule — lives in a durable record at the site
     of future temptation. A rule handed off without its incident gets reinterpreted under
     pressure, and the drift documents itself (F053/A020).
1b. **Did this session learn something about the Soul System itself?** Apply the
   test BEFORE writing anything — the append instruction used to come first, and a
   session reading top-down appended and then met the gate (fresh-context review,
   2026-08-28).

   **The test is a lookup, not a judgement: name the file that would change.**
   The surface is small and you can read it — your `CLAUDE.md` imports the contract
   from the installed plugin, and the rest of it sits beside that path: the contract
   `operations/CLAUDE.md`, the ten `skills/*/SKILL.md`, and
   `hooks/pre-completion-verify.py`. Name one of those, or it is not upstream,
   however sharp the lesson.

   Two cautions, both measured. (a) The old test asked the *category* question —
   "is this about the Soul System?" — and a good general lesson feels systemic at
   session end. On the first mining pass, **12 of 47 parked notes (26%) were sound
   engineering lessons with no Soul file to change.** (b) The lookup fails the other
   way too: `operations/CLAUDE.md` is a plausible answer to almost any
   doctrine-shaped lesson, so naming it is not enough — say what in it would change.
   And if you are running under `claude -p`, where cross-project imports fail
   silently and get confabulated (F038), you cannot see the surface at all: say so
   rather than naming a file you did not read.

   **If it passes:** append it to `upstream.md` (beside `witness.md`; create the
   file if absent), in the project's own words, under a dated `### ` heading. Do
   **not** write into the Soul System repo from here — a project usually holds only
   the read-only installed plugin, never the working repo. Then say **one short
   clause** and nothing more; see *What not to do*.

   **If it fails, it is not rubbish — say where it goes**, and note that all three
   destinations can be absent in a project that never ran `/soul-init` (F068 defect
   1); when they are, say so rather than dropping the lesson:
   - it happened once and has a story → `witness.md`
   - a convention a later session could not re-derive → **`witness.md` first, then
     propose it for `mind.md` at the next `/soul-distill`.** Never write `mind.md`
     directly: a distill rewrites that file whole from witness + ideas and prunes
     anything without an anchor, so an entry placed straight into it is deleted at
     the next distill with no trace (fresh-context review, 2026-08-28).
   - a standing rule every session must follow → **propose** a line for this
     project's own `CLAUDE.md`; do not write it. Every other write to that file in
     this system is owner-gated, and this step runs when the owner has walked away.

   **This step adds material to the "write it down" path while SOUL-F065 is open
   and unruled** — F065 is exactly the collision between this instruction and
   `/soul-capture`'s "draft and hold". Stated rather than left to be discovered.

   **Tracking follows the record.** `upstream.md` is tracked if `witness.md` is, and
   gitignored if the record is — the same choice `/soul-init` already made. On the
   run that CREATES the file, say which it will be in that one clause, and if the
   notes name a client, a vendor or anything else the repo does not already publish,
   gitignore it instead and say so. Unlike the cursor it replaced, this file can land
   in a tracked repo root, so the choice has to be made once rather than by default.

2. **Write `.soul/handoff.md` — REPLACING the previous cursor, not appending to it**
   (create `.soul/` if missing):
   ```
   # Handoff cursor — [date]
   NEXT-SESSION FOCUS: [from the argument, if given]
   WHERE WE ARE:       [one short paragraph]
   LIVE AL:            [current abstraction layer if mid-flight — what varies / decides /
                        can't vary; else "none open"]
   OPEN GATES:         [any gate mid-evaluation; else "none"]
   NEXT STEP:          [the immediate next action — the cursor]
   POINTERS (reference, do not duplicate; mark provenance on every entry):
     - witness tail:   last entries in witness.md ([ids]) [read]
     - ideas:          ideas.md ([ripe ids]) [read]
     - tasks:          [open task ids / subjects] [read|inherited]
     - specs/ADRs:     [relevant paths] [read|inherited]
   SUGGESTED ROLES / SKILLS: [for the next session]
   ```

   **The cursor is replaced, never accumulated — which makes step 1 load-bearing.**
   One cursor, one file. The previous cursor is **gone**: it is gitignored under
   both `/soul-init` branches, so there is no copy in git history and no copy
   anywhere else. Nothing in the cursor survives except what step 1 flushed into
   `witness.md` / `ideas.md` first. Read that sentence as a hazard, not a
   reassurance — an earlier draft of this rule claimed the old cursor "lives in git
   history", which is false and would have licensed overwriting an unflushed
   decision (caught by fresh-context review, 2026-08-20).

   The rule is stated because its absence produced drift: with nothing said, five of
   six projects replaced and one appended, reaching four stacked generations, 472
   lines and 31 KB — three times the size of that project's own Mind.

   **CARRY FORWARD anything still owed.** Before writing, read the OLD cursor and
   move any unfinished obligation into the new one — an open gate, a `[inherited]`
   claim not yet expired, a Body call still unanswered.

   **FIRST, the one-time upgrade check.** If the old cursor still carries an
   `OWED UPSTREAM` field (any cursor written before v2.3.0), **move its contents
   into `upstream.md` before writing the new one.** The new template has no such
   field, so replacing the cursor without moving it destroys the only copy — the
   cursor is gitignored, as this step says two paragraphs down. Once moved, the
   field never comes back.

   After that check, anything owed upstream is no longer in this file: it lives in
   `upstream.md`, which is durable and append-only, so a cursor rewrite cannot
   destroy it. That is the whole reason the field was removed (v2.3.0). The check
   above exists because the sentence you just read is false for exactly one cursor
   per project — the last one written under the old rule (fresh-context review,
   2026-08-28).

   **Size check before writing:** if the draft exceeds ~150 lines, it is carrying
   record, not cursor. Flush the excess to `witness.md` and point at it instead.

   **`[inherited]` expires.** A pointer or open gate carried `[inherited]` across
   three consecutive cursors must be verified this session or dropped — say which.
   The marking convention (A023) names unverified claims but nothing made them
   expire, and the 472-line cursor carried fifteen of them, one explicitly
   "carried as [inherited] for several cursors and STILL true."

3. **Mark pointer provenance (A023/F061):** every POINTERS entry carries `[read]` — this
   session actually opened it — or `[inherited]` — carried from a prior cursor or from
   memory, unverified. A cursor pointer is a claim, not a fact: an unmarked or
   `[inherited]` pointer once propagated a false "the ADR is not on disk" into a Body
   decision (F061; cost to check was one `ls`). Never upgrade a pointer to `[read]`
   without opening it this session. Where a **cross-repo pointer is load-bearing**,
   prefer removing the seam (move the artifact in; add a red/green check) over
   annotating it.
4. Keep it **thin**: references, not duplicates. Nothing the durable records already hold gets copied in.
   **Self-contained for correctness, not hermetic (A009):** the cursor + the records it points
   to must reproduce the work without the original session's context — but it does not shield
   the next session from the surrounding repo; a worker may still read sibling files for
   consistency. A vague handoff is the named cause of duplicated work and gaps.
5. Report that the cursor was written, and remind the Body that the next session should read `.soul/handoff.md` first.

## What not to do

- Do **not** reproduce the conversation transcript or reimplement summarization — that is `/compact`'s job.
- Do **not** duplicate content that already lives in the durable records — point to it.
- Do **not** write the cursor to a tracked path; `.soul/handoff.md` is gitignored runtime state.
- Do **not** nag about `upstream.md`. One short clause when something is appended —
  *"noted upstream: `git checkout --` is not a sabotage undo"* — and nothing else,
  ever. No running count, no "these have not been collected", no reminder that the
  project owes anything, no mention at all in a session that appended nothing. The
  obligation is real; the pestering is not. Its predecessor was a field in this
  cursor that escalated at three uncollected rides, and it fired in the one seat —
  the adopting project's session — where the owner could do nothing about it
  (2026-08-28, the Body's call; SOUL-I062). Reporting belongs to `/soul-next` run
  in the Soul System repo, which is where a mining pass can actually be run.

---

**Source:** Built by the Artificer for the handoff design
(docs/specs/2026-05-21-soul-handoff-design.md); grows only the Soul delta, leaning on
`/compact` + the durable records (SOUL-I007). Pocock's handoff skill informed the
"reference, don't duplicate" principle. **Amended:** SOUL-A023 (2026-07-16) — pointer
provenance marks, from F061 (a cursor pointer propagated a false claim into a Body
decision). **Amended:** 2026-08-28 (v2.3.0) — `OWED UPSTREAM` leaves the cursor for a
durable `upstream.md`; the carry-forward clause, the three-cursor escalation and all
other nagging go with it (SOUL-I062;
`docs/specs/2026-08-28-upstream-store.md`). **Amended:** 2026-08-28 (v2.3.1) — the
name-the-file test and the routing for what fails it, from the first mining pass
(26% misfiled), and its routing for what fails it. **Adopted:** 2026-05-21. **Status:** active.
