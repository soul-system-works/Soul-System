# Contract reasons — why the trimmed rules say what they say

`operations/CLAUDE.md` (v3.0) keeps rules 1–8 word for word and states rules 9–10 and
the closing sections in short form. This page holds what the short form left out: the
full v2 wording, with the measurements and incidents behind each rule. A rule kept
without its incident gets reinterpreted under pressure (F053/A020), so the incidents
live here rather than nowhere. Sessions need only the contract; read this when a
rule seems wrong, or before changing one.

**Why the contract was trimmed (v3.0, 2026-10-21):** the 2026-10-21 benchmark campaign
(soul-benchmark `experiments/2026-10-21-campaign/REPORT.md`; witness SOUL-213) found a
five-minute CLAUDE.md tied Soul on every quality endpoint and cost less, and a
breakdown of one-off sessions (Soul-System `.ai/plans/2026-10-22-slim-soul-v3.md`, from
the session transcripts) put most of Soul's extra cost in the contract and skill listing
loaded into every session. v3.0 cuts the contract by a third (1,041 → 698 words; the
skill listing is unchanged). Tested before release on Sonnet 5.5
(`experiments/2026-10-21-slim-soul/RESULT.md`): quality tied, chain cost −18%, one-off
cost −2%. The same test withdrew the premise that handing the owner the decision is
Soul's edge: a careful CLAUDE.md did it 5/5, both Soul versions 2/5 (SOUL-214).

**What changed in wording, not just length:**

- Rule 9 now says *how* to be brief (answer first, short plain sentences, one topic,
  stop) instead of only *that* — the Body's ask (2026-10-21): shorter replies, with
  `/soul-explain` for more.
- Rule 10's bottom line is a list when there is more than one item, each marked by who
  acts next: 🙋 your call · 🤖 I'll fix · ✅ no action — the same three action labels
  v2 required in prose ("your decision / I should fix it / no action, watch only"),
  made visible. Symbols chosen by the Body, 2026-10-21.
- The `plain` register is defined as "write for a smart reader who is new to the
  project" — the Body asked for clearer, less jargony replies without wording that
  talks down to the reader (2026-10-21).

**Rule 4's stopping clause (v3.1, 2026-10-22).** Rule 4 said how to verify but never
when verifying is enough, and every rule that touches review pushed one way. An adopting
project (MODEL-TEST, upstream note 2026-10-22) measured it: a cleanup PR planned as "one
implementer, one review" ran 1 build, 4 fix batches and full-size fresh-context reviews
(4 complete, a 5th still running when the note was written; 0.5–1.9 h each). Round 1
found the defects the plan targeted; rounds 2 and 3 each found one user-visible defect,
both introduced by the previous round's fixes; the remaining findings were planted bugs
no test caught, or wording — each treated as blocking, so each round opened the next.
This repo's 2.7.0 also ran three rounds, though its rounds found data-loss and secret
defects that the clause would still reopen for. The owner reports the
slowdown across all projects since about 2026-10-19 (A027's rule-4 wording); the model
changed in the same window, so the cause is not isolated. Reviewing corrections stays
right — rounds 2–3 show fixes do carry defects — what was missing is proportion and a
stop. The review of the first draft widened two words: "user-visible defect" became "real
defect (wrong output, data loss, security)", since a latent wrong result nobody has seen
yet is still a defect; and "what it touches" became "anything whose output it can
change", since MODEL-TEST's defects surfaced downstream of the fixed lines. **What would
make it wrong:** within a few PRs under it, a real defect ships that a full-size
correction review would have caught and the scoped one did not.

## The v2 wording, kept whole

(Where the text below says "sessions need only this page", it means the contract,
`CLAUDE.md` beside this file.)

9. **Answer at the size of the ask.** A one-line question gets a one-to-three-
   sentence answer. Lead with the answer and stop: no restating the question, no
   reasoning that did not change it, no closing RECAP re-narrating what was just
   said, no pre-empting follow-ups. (A recap is not the one-line verdict rule 10
   requires — that line states the answer, not the path, and is exempt here.) Structure — headings, tables, bold-label lists — is for
   genuinely multi-part content; on a short answer it is length, not clarity. This
   rule carries a number because the adjective did not work: the register line had
   said "keep responses concise" since 2026-06-10, and at 2026-08-07 the median
   reply still ran 2,537 chars across 908 turns, with 72% of sub-80-character
   questions drawing back over 1,500 (SOUL-I054). Applies under either register.
10. **Land the verdict.** Short is not clear — a well-sized, precisely sourced
    reply can still leave the Body unable to tell what the answer was (SOUL-174).
    Any reply that investigated, measured, or diagnosed something ends with ONE
    line carrying the verdict and its consequence: `— Bottom line: <answer>;
    <what it means for you>` (any dash, ASCII `-` included). A verdict is not a
    recap — it states the answer, not the path to it, and it is the one closing
    line rule 9 does not ban. If the reply cannot be reduced to such a line, it
    has not reached a finding yet; say that instead. Three riders: every finding
    names its **action** — your decision / I should fix it / no action, watch
    only — because a precisely described defect with no action label is not yet
    an answer; when one reply covers **more than one question, each gets its own
    named verdict** rather than one woven narrative, since a reader cannot
    separate two subjects mid-flow and will carry away whichever impression
    landed last; and a report of reviewed work says **what reached the
    artifact**, not what review caught in drafts.

**Stores** — THIS project's, never the Soul System source repo. In `.soul/`, or at
the project root if that is where they already live (both valid; detect, never
assume): `witness.md` (append-only, sequential IDs, re-read before appending) ·
`ideas.md` · `upstream.md` (append-only; system-level lessons, created when there is
a first one) · `mind.md` once earned. `findings/` and `amendments/` are the Soul
System's own stores and are not scaffolded locally. Forward view:
`/soul-next`. Maintenance: `/soul-distill` (propose it when the record has grown;
the owner confirms — it keeps this page within budget).

**Working files** — plans, drafts, review output, eval results, scratch — go in
`.ai/` (created on first use, safe to delete), never in `docs/`, the root or source
folders. Promoting one to project content is the owner's call; project content
never links into `.ai/`.

**Register** defaults to `plain` — use a Soul or project term only when it earns
its place, gloss it on first use, introduce vocabulary gradually. Vocabulary only;
LENGTH is rule 9 either way. Override with a `**Register: fluent**` line in the
project's own CLAUDE.md. The default lives here because a copy written into a
project at init never receives an upgrade.

**Stage** (optional): a project declares `prototype` / `pre-release` / `released`
in its own CLAUDE.md via `/soul-stage`, and the block beneath says what may be
broken and what must be kept; undeclared means released — protect what others
may depend on, ask before breaking it (rule 7), and offer `/soul-stage` to record
the answer.

**Projects importing this contract** owe their Soul-System-level lessons upstream,
plus a closing note at milestones. The test is a lookup, not a judgement: **name the
file in this system that would change** — the contract, a skill, doc, tool or hook.
Cannot name one? It is a domain lesson and it stays home (26% of the first mining
pass's notes failed this having passed a vaguer "is it about the system?" test). If
you can, append it to `upstream.md` as it happens; the Soul System collects on a
periodic pass. Never write into that repo from here. Say ONE short clause when you
append and nothing more — no counts, no reminders, no mention at all in a session
that appended nothing.

The thinking behind this system — its history, roles, and the measurements that
shaped it — lives in `philosophy/the-soul.md`. It is written for human readers;
sessions need only this page.
