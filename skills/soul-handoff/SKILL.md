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

**When it runs itself (SOUL-A032).** The session runs this unasked — no question
first — when the cursor is stale: about 100,000 tokens of new conversation since it
was last written, or a summary (compaction) since. Soul's hooks notice: a Stop hook
(`hooks/upkeep.py`) blocks the stop once and asks for the refresh, and after a
summary the session-start line says to re-read the cursor. A summary counts only when
at least half the step or 50,000 tokens, whichever is higher, came between the last
write and the summary: one minutes after a refresh asked for a second with almost
nothing new (an adopting project's upstream note, 2026-11-16). A
count of commits was not used: "some agents/processes commit a lot and others not so
much" (the Body). It stays quiet in a project with no cursor yet, and when
`.soul/init.md` holds `upkeep: off` (the owner's opt-out, asked once by
`/soul-init`). The hooks are Claude Code's; elsewhere (Codex), refresh it unasked
after a summary or a long stretch of work. A run that started itself does every step
below, then reports in step 5.

**Headless runs too.** The Stop check fires under `claude -p` (seen in a live trial,
2026-11-12; the amendment had guessed hooks might not). A long headless run in a Soul
project with a cursor is blocked once per 100,000 tokens, and its final result text
becomes the refresh line, not the run's answer. A measurement arm or scripted run that
must not be steered: record `upkeep: off`, or run without the plugin —
`tools/dispatch.py` starts its workers with `--setting-sources ""`, which skips the
settings that switch the plugin on. Writing the cursor before a long unattended run
(above) still holds.

A long unattended run also keeps a short **decisions log** at
`.ai/runs/<date>-<run>-decisions.md` (`<run>` a short lowercase hyphenated slug):
each choice it made on its own, the reason, and which numbers it re-checked. The
pre-run cursor names that path (in NEXT STEP or OPEN GATES), so a later
`/soul-debrief` can find it (SOUL-I086).

## What to do

1. **Flush volatile → durable** (the real work — do this first):
   - Is the current abstraction layer recorded in a spec/ADR? If it is live and unwritten, record it.
   - Any witness-worthy moment this session not yet in `witness.md`? Any new idea
     not captured in `ideas.md` (minimal)? Capture it through `/soul-capture`
     (id scan, re-read-verify): **append it at once, with no mark — it counts as
     accepted** (*Who fires this* there). Do not hold it for a go: this step usually
     runs as the Body leaves, and the cursor's old content is replaced, so a held draft
     is discarded (F065).
   - **List every entry the model added this session** — mentioned in chat already
     or not, the ones just added here included — in the cursor's `NEW ENTRIES` field
     (step 2); step 5 names them in one line. Every one, so the list is the same
     whoever reads it and still holds after an unattended run. Nothing is scanned
     for and nothing waits for an answer: the Body's no is the only thing that
     changes an entry (`/soul-capture`).

     **Why no mark (SOUL-A031, from SOUL-I085):** entries used to be appended
     marked `unconfirmed` and ratified one by one later — an extra step and an
     extra commit each. The Body: "should be autoratified with opt out. this way it
     isn't an extra commit or extra step."
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
   upstream: a system lesson goes in through `/soul-capture witness`, appended as in
   step 1 (or `/soul-capture finding` if the Body graduates it). Skip the rest of
   1b, and never create an `upstream.md` here (SOUL-187).

   **The test is a lookup, not a judgement: name the file that would change.**
   The surface is small and you can read it — your `CLAUDE.md` imports the contract
   from the installed plugin, and the rest of it sits beside that path: the contract
   `operations/CLAUDE.md`, every `skills/*/SKILL.md`, a doc in `operations/` or
   `docs/` (witness-log format, completion gate, …), a `tools/*` helper, and the
   hooks `hooks/pre-completion-verify.py`, `upkeep.py`, `secret-guard.py` and
   `codex.py`. Name one of those, or it is not upstream,
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

1c. **Is the Mind due?** If `mind.md` exists and the record has grown past
   `/soul-distill`'s growth signal since its `Last distilled` stamp (about 15+ new
   witness entries, or a finding closed or an amendment accepted), run
   `/soul-distill` now — by itself, at most once a day, and not with
   `upkeep: off` (then name it as due in step 5 instead). It applies its minor
   changes and holds its major ones; its one line joins step 5's report, and held
   changes go in OPEN GATES.
2. **Update `.soul/handoff.md` in place — one cursor, never appended to** (create
   `.soul/` if missing). Edit only the fields that changed (the Edit tool); rewrite the
   whole file with Write only when most of it changes or there is no cursor yet. Either
   way the result is one current cursor: a stale line is replaced or removed, never
   kept beside its successor. Every run rewrites the header date and `NEW ENTRIES`
   (this run's entries, or "none" — an old list left in place would be announced
   again), and re-marks every pointer `[read]` or `[inherited]`. A full rewrite each time re-typed about 100 unchanged
   lines and the cursor grew 132 → 146 lines in a day (an adopting project's upstream
   note, 2026-11-16), and it fills the owner's terminal (SOUL-I094):
   ```
   # Handoff cursor — [date]
   NEXT-SESSION FOCUS: [from the argument, if given; the Body's own words for a topic
                        are quoted with what they referred to, or "referent
                        unknown — ask" (step 3)]
   WHERE WE ARE:       [one short paragraph — no count that goes stale; write the
                        command that produces it instead (step 3)]
   LIVE AL:            [current abstraction layer if mid-flight — what varies / decides /
                        can't vary; else "none open"]
   OPEN GATES:         [any gate mid-evaluation, each [read]; else "none"]
   NEXT STEP:          [the immediate next action — the cursor] [read]
   NEW ENTRIES:        [ids of every entry the model added this session (step 1);
                        else "none"]
   POINTERS (reference, do not duplicate; mark provenance on every entry):
     - witness tail:   last entries in witness.md ([ids]) [read]
     - ideas:          ideas.md ([ripe ids]) [read]
     - tasks:          [open task ids / subjects] [read|inherited]
     - specs/ADRs:     [relevant paths] [read|inherited]
     - debrief:        newest line of .ai/debriefs/INDEX.md, if any [read]
   SUGGESTED ROLES / SKILLS: [for the next session]
   ```

   **The cursor is replaced, never accumulated — which makes step 1 load-bearing.**
   One cursor, one file. **Check, do not assume, whether the old one survives.**
   - **Vault link** (`.soul` is a link: `test -L .soul`) — this case replaces the two
     below for the cursor, and the `.gitignore` offer does not apply. Git refuses a
     path through the link ("pathspec … is beyond a symbolic link"), so check in the
     repo that holds the target, `<vault>/projects/<key>/soul` (where `.soul`
     resolves): the old cursor survives only if `git -C <vault> ls-files --
     projects/<key>/soul/handoff.md` lists it AND `git -C <vault> diff --quiet --
     <that path>` exits 0 (committed, with no edits since). After writing the new
     cursor, run `python3 <root>/tools/vault.py sync .` (`<root>` is two levels above
     this skill's base directory): it commits only this project's vault folder, under
     the vault's lock, and pushes only when the vault's server has not moved. Say in
     one line what it printed.
     **What sync's exit means** (same text in `/soul-init` and `/soul-handoff`). Exit 0:
     on the server ("already on the server; this vault's copy is behind" too). Exit 2
     with `NOT PUSHED`: committed in the vault, safe on this machine, not on the
     server — say why (its line names it). If the server has newer commits, merging
     them is a deliberate step — the Body's, or a session's when no other session is
     writing in the vault, with the commands that line names (not a bare `git pull`:
     it fails on diverged branches) — then sync again. Any other exit 2 (no `NOT
     PUSHED` in its line): nothing was committed; report its line. Exit 4: a running sync holds the lock — nothing is
     committed; say so, and sync again once it finishes. Or the lock "looks stale" —
     give the Body its removal step word for word (remove that file once they have
     checked no git runs in the vault); never remove it yourself.
     The merge is not part of the handoff. Three adopting projects and this repo hit
     the error (mining pass 3, SOUL-233/234).
   - **No link:** run `git check-ignore -v .soul/handoff.md` — one call that sees
     `.gitignore`, `.git/info/exclude` and the global excludes alike (F068 defect 3);
     then one of these two:
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
   unanswered. (`NEW ENTRIES` is never carried: it is written fresh for each cursor,
   and an entry needs nothing from the Body to stay. An old cursor's `UNCONFIRMED`
   field is dropped the same way: those entries are treated as accepted, and a mark
   left on them is harmless text — do not remove it.) **An inherited OPEN GATES or
   NEXT STEP obligation is checked in this session — the one that inherits it — or
   dropped, and the cursor says which;**
   checked, it carries `[read]`. It is not carried `[inherited]` to a later cursor
   (confirmed by the Body, 2026-10-19). A carried pointer keeps its mark:
   checked this session, it becomes `[read]`; otherwise it stays `[inherited]`
   (step 3).

   **Size check before writing:** if the draft exceeds ~150 lines, it is carrying
   record, not cursor. Flush the excess to `witness.md` and point at it instead.

   **`[inherited]` expires.** A pointer carried `[inherited]` across three
   consecutive cursors must be verified this session or dropped — say which. An
   OPEN GATES or NEXT STEP obligation gets no three-cursor grace (carry-forward,
   above). The marking convention (A023) names unverified
   claims but nothing made them expire, and the 472-line cursor carried fifteen of
   them, one explicitly "carried as [inherited] for several cursors and STILL
   true."

3. **Mark provenance (A023/F061; extended past POINTERS by F067):** every POINTERS
   entry carries `[read]` — this session opened, checked or established it — or
   `[inherited]` — carried from a prior cursor or from memory, unverified. Every
   OPEN GATES item and the NEXT STEP carry `[read]` (step 2's carry-forward). A
   cursor pointer is a claim, not a fact: an
   unmarked or `[inherited]` pointer once propagated a false "the ADR is not on
   disk" into a Body decision (F061; cost to check was one `ls`). The obligations
   are claims too: MODEL-TEST carried an unmarked NEXT STEP obligation forward
   false twice — inside the three-cursor expiry, which is why an inherited
   obligation is checked at once rather than given a pointer's three cursors
   (F067; mining pass 2, SOUL-202). Never upgrade an
   item to `[read]` without checking it this session. Where a **cross-repo pointer
   is load-bearing**, prefer removing the seam (move the artifact in; add a
   red/green check) over annotating it.

   **The focus keeps what the Body's words pointed at.** When NEXT-SESSION FOCUS
   uses the Body's own words for a topic ("the new layout", "that drawing"), quote
   them **and** say what they referred to — a file, a drawing, an earlier turn — so
   the next session can find it. If you cannot tell, write "referent unknown — ask".
   A LEARN-APP cursor's focus kept the Body's words but lost what they referred to
   (upstream mining, 2026-11-12). Related to
   SOUL-F075 (a quote not tied to an owner turn); this does not close it.

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
   should read `.soul/handoff.md` first. A run that started itself says one line
   instead — *"☀  cursor refreshed (about 110k tokens since the last)"* or *"☀  cursor
   refreshed (a summary happened)"* — adds "to turn this off: /soul-init revisit
   upkeep" when the hook's reason asked for it. The reply before the refresh stays the
   answer: do not restate, shorten or replace it. If the refresh interrupted work in
   progress, go back to it after the line (the hook's text and this step say the same
   since 3.13.2; before, "then stop" and "goes back to the work" disagreed, and twice
   the answer the owner was waiting for became the one line). **Then name the `NEW ENTRIES` in one
   line** — *"☀  Added THERMAL-231, THERMAL-I086 — say no to strike any."* No question;
   silence keeps them. A "no" is recorded the way `/soul-capture` says (*Who fires this*).

   **The sun mark.** `☀  ` (U+2600 and two spaces) starts every line that reports
   something the Soul did on its own — this refresh, a Mind refresh or its held
   changes (`/soul-distill` step 8), a capture the model started (`/soul-capture`) —
   and nothing else, so those lines can be told at a glance from an answer to what
   was asked. The Body, 2026-11-13: "when the soul-system does some auto thign like
   update the mind or soul-handoff is there a little sun symbol that can preceed it?"
   Two spaces, not one: with one the Body saw the sun touch the word ("sunmark is
   good but needs a space before the first word", the same day).
   A line the Body asked for (a `/soul-handoff` they typed, a witness entry they
   dictated) carries no mark.

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

History and the reasons behind changes: [HISTORY.md](HISTORY.md).
