---
name: soul-discuss
description: Explore an idea or topic with the Body as a knowledgeable coworker, not a yes-man — offer a clarify round when the idea is thin, set rivals beside it, give the strongest objection before the pros, scan a few cited sources, hold a stated lean unless a new fact or argument arrives, and close each round with a block the idea's entry can keep. Run it when the Body asks for it, on an idea entry or a general topic. Otherwise only propose it, and run it on the Body's yes: when the Body brings a new idea to explore, or moves to build an idea that has not been discussed.
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

The skill does not rely on being told to be honest. Its steps make agreement
visible and costly instead: rivals on the table, the objection first, a lean that
must name its reason to move.

## What to do

1. **Find the target.** An idea ID → read its entry in **this project's** ideas
   store (`.soul/ideas.md` or `ideas.md` at the root — detect, never assume; never
   the copy shipped inside the Soul plugin, as `/soul-capture` warns), including any earlier
   `DISCUSSED:` / `ROUND n:` fields, so this round builds on the last. A general
   topic → no entry needed. Look up every fact you can (the record, the code, files,
   what is installed) before asking the Body anything.

2. **Offer a clarify round when the idea is thin** — when its problem, its reasons,
   or what it would change are unstated. A few numbered questions, each with your
   guess so "yes" is cheap; always ask why the Body thinks it is valuable. The Body
   may skip it. An idea that needs a full design-tree interview → suggest grilling
   instead (e.g. Pocock's `grilling` skill, if installed). (Hand trial, 2026-10-22: the first round weighed the Body's aims before
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
   sources · lean · deeper research (worth it / not) · next step — plus, after a
   clarify round, the Body's answers in their own words. The reply still ends with
   the contract's bottom line; the block sits above it. On the Body's yes, write
   the block into the idea's entry — `DISCUSSED:` for round 1, `ROUND 2:`,
   `ROUND 3:` … after. If its `STATUS` is `Raw` or missing, set `STATUS: Maturing`
   (being developed, not ready to build); any other `STATUS` (Built, Graduated,
   Parked …) stays as it is. An entry with no
   `STATUS:` line, or `Raw`, has not been discussed. A topic with no entry gets
   the block only; offer `/soul-capture idea` if it should be kept.

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
