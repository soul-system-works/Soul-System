---
name: soul-handoff
description: Write a thin Soul-native handoff cursor (.soul/handoff.md) so the next session resumes without re-deriving state. Flushes volatile state into the durable records first; leans on /compact for the prose recap.
---

# /soul-handoff — hand off to the next session

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
1b. **Park anything owed upstream.** Did this session learn something about the
   Soul System *itself* — an instrument that misfired, a gate that helped or got
   in the way, a doctrine sentence that did not survive contact? That is owed
   upstream under the contract, and it dies here unless it is parked where a later
   pass can find it. Put it in the cursor's `OWED UPSTREAM` field, in the project's
   own words. Do **not** try to write it into the Soul System repo from here —
   most projects cannot reach it, and a lesson parked locally is retrievable while
   a lesson not written is gone.

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
   OWED UPSTREAM:      [Soul-System-level observations, unsent; else "none"]
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
   move any unfinished obligation into the new one — an unsent `OWED UPSTREAM`
   entry, an open gate, a `[inherited]` claim not yet expired. `OWED UPSTREAM`
   especially: it is the ONLY route a project has for lessons about the system
   itself, it is collected by a pass that runs on no fixed schedule, and it lives in
   this replaced, untracked file. Writing `OWED UPSTREAM: none` when the previous
   cursor carried an unsent entry destroys it permanently. If an entry has ridden
   three cursors uncollected, say so in the field itself and tell the Body — a
   parked lesson nobody collects is the failure this field was created to fix, not
   a state to keep re-parking silently.

   **Size check before writing:** if the draft exceeds ~150 lines, it is carrying
   record, not cursor. Flush the excess to `witness.md` and point at it instead.

   **`[inherited]` expires.** A pointer or open gate carried `[inherited]` across
   three consecutive cursors must be verified this session or dropped — say which.
   The marking convention (A023) names unverified claims but nothing made them
   expire, and the 472-line cursor carried fifteen of them, one explicitly
   "carried as [inherited] for several cursors and STILL true."

   `OWED UPSTREAM` is not decoration: the field was invented by hand in a project
   that had a lesson and nowhere to send it, and adopting it verbatim is cheaper
   than inventing a worse one. Two upstream notes arrived in four months across six
   projects; the parking field is the cheap half of fixing that, and the periodic
   mining pass run from the Soul System repo is the other half.
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

---

**Source:** Built by the Artificer for the handoff design
(docs/specs/2026-05-21-soul-handoff-design.md); grows only the Soul delta, leaning on
`/compact` + the durable records (SOUL-I007). Pocock's handoff skill informed the
"reference, don't duplicate" principle. **Amended:** SOUL-A023 (2026-07-16) — pointer
provenance marks, from F061 (a cursor pointer propagated a false claim into a Body
decision). **Adopted:** 2026-05-21. **Status:** active.
