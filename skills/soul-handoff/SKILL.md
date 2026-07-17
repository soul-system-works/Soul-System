---
name: soul-handoff
description: Write a thin Soul-native handoff cursor (.soul/handoff.md) so the next session resumes without re-deriving state. Flushes volatile state into the durable records first; leans on /compact for the prose recap.
disable-model-invocation: true
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
2. **Write `.soul/handoff.md`** (create `.soul/` if missing — it is gitignored runtime state):
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
     - open findings:  findings/open/ ([ids]) [read]
     - ideas:          ideas.md ([ripe ids]) [read]
     - tasks:          [open task ids / subjects] [read|inherited]
     - specs/ADRs:     [relevant paths] [read|inherited]
   SUGGESTED ROLES / SKILLS: [for the next session]
   ```
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
