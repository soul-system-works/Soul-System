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

## When to run it

At session end — and **before any long unattended run the context may not
outlive** (a batch job, a sweep, an overnight agent), not only at the end. Flush
first, then write the cursor with what is running, in which configuration, what
its result decides, and the next step for each outcome. A context lost mid-run
takes with it everything not yet flushed (PLANT-BOP's upstream note; mining pass 2,
SOUL-202).

## What to do

1. **Flush volatile → durable** (the real work — do this first):
   - Is the current abstraction layer recorded in a spec/ADR? If it is live and unwritten, record it.
   - Any witness-worthy moment this session not yet in `witness.md`? Any new idea
     not captured in `ideas.md` (minimal)? Capture it through `/soul-capture`
     (id scan, re-read-verify), and **append it marked `unconfirmed — owner to
     ratify`** — whether or not the Body seems to be there: this step usually runs
     as they leave, and an answer may never come. Do not hold it for a go first: the
     cursor is replaced wholesale, so a held draft is discarded. Write the cursor
     (step 2) with the drafts listed as unconfirmed, THEN show them (step 5); a
     "go" then removes the mark.
   - **Collect the marks into the cursor.** Scan `witness.md` and `ideas.md` for
     `unconfirmed — owner to ratify` and list every entry that still carries it —
     this session's and any earlier one not yet ratified — in the cursor's
     `UNCONFIRMED` field. That field is written here and only here: `/soul-capture`
     never writes the cursor by hand (rule 6), it leaves the mark for this scan.

     **F065 is ruled (SOUL-202):** this step and `/soul-capture` used to give
     opposite orders at session end — "add it" here, "draft and hold" there. Both
     now say: append marked unconfirmed, list it in the cursor, put it to the Body.
     Four sessions in four projects had already appended rather than held, and
     said so.
   - Is the task tracker current? Update it.
   - Any counter-default fence relied on this session? Verify its **force** — the incident
     and the explicit negation, not just the rule — lives in a durable record at the site
     of future temptation. A rule handed off without its incident gets reinterpreted under
     pressure, and the drift documents itself (F053/A020).
1b. **Did this session learn something about the Soul System itself?** Apply the
   test BEFORE writing anything — the append instruction used to come first, and a
   session reading top-down appended and then met the gate (fresh-context review,
   2026-08-28).

   **First: are you in the Soul System repo itself?** Test it as `/soul-next` 2b
   does — `findings/open/` **and** `operations/CLAUDE.md` **and**
   `SYSTEM-VERSION.md`, all at the repo root; never "the witness log uses
   `SOUL-###`", which reads true in adopting projects too. If so there is no
   upstream: a system lesson goes in through `/soul-capture witness`, marked as in
   step 1 (or `/soul-capture finding` if the Body graduates it). Skip the rest of
   1b, and never create an `upstream.md` here (SOUL-187).

   **The test is a lookup, not a judgement: name the file that would change.**
   The surface is small and you can read it — your `CLAUDE.md` imports the contract
   from the installed plugin, and the rest of it sits beside that path: the contract
   `operations/CLAUDE.md`, every `skills/*/SKILL.md`, a doc in `operations/` or
   `docs/` (witness-log format, completion gate, …), a `tools/*` helper, and the
   hook `hooks/pre-completion-verify.py`. Name one of those, or it is not upstream,
   however sharp the lesson. (The docs and `tools/*` entries were added after three
   notes in mining pass 2 correctly named an operations doc the old list left out —
   SOUL-202.)

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
   WHERE WE ARE:       [one short paragraph — no count that goes stale; write the
                        command that produces it instead (step 3)]
   LIVE AL:            [current abstraction layer if mid-flight — what varies / decides /
                        can't vary; else "none open"]
   OPEN GATES:         [any gate mid-evaluation, each [read]; else "none"]
   NEXT STEP:          [the immediate next action — the cursor] [read]
   UNCONFIRMED:        [ids of every entry still marked `unconfirmed — owner to
                        ratify` (step 1's scan); else "none"]
   POINTERS (reference, do not duplicate; mark provenance on every entry):
     - witness tail:   last entries in witness.md ([ids]) [read]
     - ideas:          ideas.md ([ripe ids]) [read]
     - tasks:          [open task ids / subjects] [read|inherited]
     - specs/ADRs:     [relevant paths] [read|inherited]
   SUGGESTED ROLES / SKILLS: [for the next session]
   ```

   **The cursor is replaced, never accumulated — which makes step 1 load-bearing.**
   One cursor, one file. **Check, do not assume, whether the old one survives:**
   run `git check-ignore -v .soul/handoff.md` — one call that sees `.gitignore`,
   `.git/info/exclude` and the global excludes alike (F068 defect 3).
   - **Ignored** (what `/soul-init` writes under either answer): the previous
     cursor is **gone** — no copy in git history, no copy anywhere else. Nothing in
     it survives except what step 1 flushed into `witness.md` / `ideas.md` first.
     Read that as a hazard, not a reassurance — an earlier draft of this rule
     claimed the old cursor "lives in git history", which is false for an ignored
     cursor and would have licensed overwriting an unflushed decision (caught by
     fresh-context review, 2026-08-20).
   - **Not ignored:** only a committed version survives, so an uncommitted cursor
     is still lost on replacement — the flush is load-bearing either way. Treat a
     tracked cursor as the project's choice: leave the ignore rules alone, say once
     that the cursor is tracked (and, in a public repo, public), and offer adding
     `.soul/handoff.md` to `.gitignore` as the owner's call. This paragraph used to
     assert the cursor is always ignored; GAME-THERMAL's is tracked (mining pass 2,
     SOUL-202).

   The rule is stated because its absence produced drift: with nothing said, five of
   six projects replaced and one appended, reaching four stacked generations, 472
   lines and 31 KB — three times the size of that project's own Mind.

   **CARRY FORWARD anything still owed.** Before writing, read the OLD cursor and
   move any unfinished obligation into the new one — an open gate, a NEXT STEP
   obligation, a `[inherited]` pointer not yet expired, a Body call still
   unanswered. (Unratified entries need no carrying: step 1's scan finds them in the
   stores.) **An inherited OPEN GATES or NEXT STEP obligation is checked in this
   session — the one that inherits it — or dropped, and the cursor says which;**
   checked, it carries `[read]`. It is not carried `[inherited]` to a later cursor
   (confirmed by the Body, 2026-10-19). A carried pointer keeps its mark:
   checked this session, it becomes `[read]`; otherwise it stays `[inherited]`
   (step 3).

   **FIRST, the one-time upgrade check.** If the old cursor still carries an
   `OWED UPSTREAM` field (any cursor written before v2.3.0), **move its contents
   into `upstream.md` before writing the new one.** The new template has no such
   field, so replacing the cursor without moving it destroys the only copy — the
   cursor is normally gitignored (the check above). Once moved, the
   field never comes back.

   After that check, anything owed upstream is no longer in this file: it lives in
   `upstream.md`, which is durable and append-only, so a cursor rewrite cannot
   destroy it. That is the whole reason the field was removed (v2.3.0). The check
   above exists because the sentence you just read is false for exactly one cursor
   per project — the last one written under the old rule (fresh-context review,
   2026-08-28).

   **Size check before writing:** if the draft exceeds ~150 lines, it is carrying
   record, not cursor. Flush the excess to `witness.md` and point at it instead.

   **`[inherited]` expires.** A pointer carried `[inherited]` across three
   consecutive cursors must be verified this session or dropped — say which. An
   OPEN GATES or NEXT STEP obligation gets no three-cursor grace: it is checked in
   the session that inherits it, or dropped (carry-forward, above; pending the
   Body's confirmation, 2026-10-19). The marking convention (A023) names unverified
   claims but nothing made them expire, and the 472-line cursor carried fifteen of
   them, one explicitly "carried as [inherited] for several cursors and STILL
   true."

3. **Mark provenance (A023/F061; extended past POINTERS by F067):** every POINTERS
   entry carries `[read]` — this session opened, checked or established it — or
   `[inherited]` — carried from a prior cursor or from memory, unverified. Every
   OPEN GATES item and the NEXT STEP carry `[read]`: an inherited one is checked
   or dropped, never carried `[inherited]` (step 2; confirmed by the
   Body, 2026-10-19). A cursor pointer is a claim, not a fact: an
   unmarked or `[inherited]` pointer once propagated a false "the ADR is not on
   disk" into a Body decision (F061; cost to check was one `ls`). The obligations
   are claims too: MODEL-TEST carried an unmarked NEXT STEP obligation forward
   false twice — inside the three-cursor expiry, which is why an inherited
   obligation is checked at once rather than given a pointer's three cursors
   (F067; mining pass 2, SOUL-202). Never upgrade an
   item to `[read]` without checking it this session. Where a **cross-repo pointer
   is load-bearing**, prefer removing the seam (move the artifact in; add a
   red/green check) over annotating it.

   **No stale-prone numbers in WHERE WE ARE.** A count that moves without this
   session — commits unpushed, tests failing, entries pending — is not written in;
   write the command that produces it (`git status -sb`), so the next session reads
   it fresh. A NOTE-VAULT cursor carried such a count stale (F067; SOUL-202).
4. Keep it **thin**: references, not duplicates. Nothing the durable records already hold gets copied in.
   **Self-contained for correctness, not hermetic (A009):** the cursor + the records it points
   to must reproduce the work without the original session's context — but it does not shield
   the next session from the surrounding repo; a worker may still read sibling files for
   consistency. A vague handoff is the named cause of duplicated work and gaps.
5. Report that the cursor was written and remind the Body that the next session
   should read `.soul/handoff.md` first. **Then show each `UNCONFIRMED` entry** —
   the cursor already lists them, so nothing is lost if no one answers. A "go"
   removes the mark from the entry and its id from the cursor's field; a "no" is
   recorded the way `/soul-capture` says (*Who fires this*), and its id leaves the
   field too.

## What not to do

- Do **not** reproduce the conversation transcript or reimplement summarization — that is `/compact`'s job.
- Do **not** duplicate content that already lives in the durable records — point to it.
- Do **not** write the cursor anywhere but `.soul/handoff.md`, and do not assert that path is gitignored — check it (step 2).
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
(26% misfiled), and its routing for what fails it. **Amended:** 2026-10-19 (mining
pass 2, SOUL-202) — F065 ruled (append marked unconfirmed; step 1 collects every
marked entry into the new `UNCONFIRMED` field; cursor first, then show); F067's fix
(an inherited OPEN GATES / NEXT STEP obligation is checked or dropped, pending the
Body's confirmation; commands, not counts, in WHERE WE ARE); flush before a long unattended run;
`git check-ignore` instead of asserting the cursor is ignored; 1b's surface gains
`operations/*.md` and `tools/*`. **Amended:** 2026-10-21 (v2.10.1, SOUL-208) — 1b
first checks for the Soul System repo itself, where there is no upstream (SOUL-187).
**Adopted:** 2026-05-21. **Status:** active.
