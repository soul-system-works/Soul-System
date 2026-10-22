---
name: soul-discuss
description: Explore an idea or topic with the Body as a knowledgeable coworker, not a yes-man — offer a clarify round when the idea is thin, set rivals beside it, give the strongest objection before the pros, scan a few cited sources, hold a stated lean unless a new fact or argument arrives, and close each round with a block the idea's entry can keep. Use when the Body wants to explore, weigh or develop an idea (an ideas.md entry or a general topic); propose it, and run it on the Body's yes, when the Body moves to build an idea still marked Raw.
---

# /soul-discuss — contest the idea so it can mature

**Codex:** Read [the host integration](../../operations/codex.md) before
following this workflow. Its Codex procedures replace Claude-specific loading,
instruction-file, tool, and invocation mechanics; the shared workflow follows.

The Body wants an idea contested in a useful way — developed, compared with what
already exists, researched enough to judge — and only then weighed and decided. Not
validated. The nearby tools leave that gap: grilling looks inward (what does the
Body mean?), `/soul-explain council` describes from several angles but never
recommends or researches. This looks outward, then weighs (SOUL-I078).

Telling a model "don't be a sycophant" is the weakest lever: a careful file matched
Soul on asking first (SOUL-214), so wording alone buys little. The steps below are
structure that makes agreement visible and costly instead.

## What to do

1. **Find the target.** An idea ID → read its entry, including any earlier
   `DISCUSSED:` / `ROUND n:` fields, so this round builds on the last. A general
   topic → no entry needed. Look up every fact you can (the record, the code, files,
   what is installed) before asking the Body anything.

2. **Offer a clarify round when the idea is thin** — when its problem, its reasons,
   or what it would change are unstated. A few numbered questions, each with your
   guess so "yes" is cheap; always ask why the Body thinks it is valuable. The Body
   may skip it. An idea that needs a full design-tree interview → suggest grilling
   instead. (Hand trial, 2026-10-22: the first round weighed the Body's aims before
   asking why they mattered, and the Body caught it.)

3. **Reframe out loud when the answers change the question.** Say it is your
   reading. Options from earlier rounds may fall away; say which.

4. **Weigh, in this order:**
   - **Rivals first** — at least two, beside the idea: do nothing; what already
     exists (tools, standards, popular repos, this project's own instruments); and
     where it fits, a different form (a rule instead of a skill, a setting instead
     of a tool). An idea placed next to real rivals is hard to simply agree with.
   - **The strongest objection, before the pros.**
   - **A short scan** — a handful of sources, primary ones preferred, each linked.
     Say what came from a search and what from memory. End with one line:
     *"Deeper research: worth it / not, because …"* — a deeper pass is a follow-up
     the Body chooses, never run unasked. If a test would settle it faster than
     reading, say so (a test is not research).

5. **State a lean and what would change it.** Under pushback, move only for a new
   fact or argument, and name it ("moving, because …"). With no new argument, hold
   and say why. Agreeing is fine when you agree — say what convinced you.

6. **Give the concrete picture** when a lean is abstract or the Body asks — a
   folder tree, a sample file, a day in use.

7. **Before anything turns into a build plan,** ask "what are we missing?" and
   answer it: the failure modes, what existing work it touches, what cannot be
   undone.

8. **Close each round with a block:** options weighed · strongest objection ·
   sources · lean · deeper research (worth it / not) · next step. On the Body's yes,
   write it into the idea's entry — `DISCUSSED:` the first time, `ROUND n:` after —
   and move `STATUS` from Raw to Maturing (Maturing means being developed, not
   ready to build). A topic with no entry gets the block only; offer
   `/soul-capture idea` if it should be kept.

The loop is clarify → weigh → the Body corrects → weigh again. Recommend another
round when it would help; whether to take it is the Body's call.

## What not to do

- Do **not** plan or start the build. When the Body decides, hand off.
- Do **not** run deep research unasked, invent sources, or invent history.
- Do **not** flatter, pad, or restate the Body's idea back as praise.
- Do **not** copy a private name into a public record — check before writing the
  block.

---

**Source:** SOUL-I078 (the Body, 2026-10-22), shaped in discussion and trialled by
hand the same day on SOUL-I079 over several rounds. Built for v3.3.0. **Status:**
experimental — not benchmarked. Falsifier: under bare pushback (no new fact or
argument), sessions running this skill change their stated lean as often as
sessions without it.
