---
name: soul-explain
description: On-demand, read-only explanation of the current state or what was just shared — describe without deciding, re-planning, or proposing new options. The `council` mode gives a multi-lens read (Skeptic/Advocate/Accountant angles, single pass). Use when the Body wants understanding, not action.
disable-model-invocation: true
---

# /soul-explain — describe, don't decide

You have been asked to EXPLAIN, not to act. Produce a clear description of the
target — the thing just shared, the current state, or a named item — as a
read-only lens. This is the deliberate, invokable form of "just tell me what's
going on" (the verbosity/clarity concern, SOUL-I008; the calibration the
clarification-drift memory asks for). Its twin is `/soul-next` (forward action);
this one only illuminates.

## What to do

1. **Parse arguments** (all optional):
   - `<target>` — what to explain. If absent, take the obvious referent (the
     last thing shared, the current state of the work). If genuinely ambiguous,
     ask.
   - `--depth=low|medium|high` — verbosity axis. Default: `medium`. `low` =
     two or three sentences naming the substance; `medium` = a paragraph or
     short list, abstraction named only when it aids understanding; `high` =
     full context, anchors, related records, what varies / what is load-bearing.
   - `--no-jargon` — every domain-specific term is either replaced with a plain
     equivalent or defined inline on first use. No bare acronyms; no Soul-System
     vocabulary (Witness/Council/Mind/Finding/etc) without a one-clause gloss.
   - `--eli5` — preset shortcut: equivalent to `--depth=low --no-jargon` AND
     prefer concrete analogies over abstract framings. For when the Body wants
     the cleanest possible read.
   - `council` — multi-lens mode. Describe the target through several Council
     lenses in a SINGLE pass (e.g. Skeptic: what's the unexamined assumption?
     Advocate: what does the end user live with? Accountant: what's the real
     cost/constraint? Steward: what no longer serves?). Pick the 2–4 lenses that
     fit the target. This is the surviving value of the retired `/soul-council` —
     sense-making, not decision-forcing. **One agent, one pass, lenses not
     subagents** (avoids the lossy multi-agent synthesis, SOUL-119). The lens
     roster lives in `philosophy/the-soul.md`. Still read-only: describe from each
     angle; do not decide or recommend.

2. **Identify the target** per the parsed `<target>` (or the obvious referent).
3. **Explain it plainly** under the parsed depth/jargon constraints. What it is,
   why it is the way it is, what it means. Draw on the durable records (witness,
   `ideas.md`, `findings/`) and the code when relevant. **Seer / Revelator:** say
   what the record actually means, free of present bias — surface what is there,
   not what you would do about it.
4. **Match output to the flags.** If `--depth=high`, name the abstraction (what
   varies, what is load-bearing) explicitly. If `--depth=low` or `--eli5`, omit
   the abstraction layer entirely unless it IS the explanation.

## What not to do (the read-only contract)

- Do **not** change the plan, propose new options, or recommend next steps. That
  is `/soul-next`' job and the opposite failure here.
- Do **not** edit anything or take action. Explanation only.
- If answering a clarifying question, answer **within the existing frame**; at
  most restate the EXISTING options — never invent new ones ([[clarification-drift]]).
  If you believe the frame itself is wrong, say so explicitly rather than silently
  shifting it.
- Do not pad with ceremony or role announcements. Quiet and clear (SOUL-I008).

---

**Source:** Built by the Artificer for SOUL-I012. The read-only twin of
`/soul-next`; the explicit form of smart-by-default description. Addresses the
verbosity concern (SOUL-I008) and enforces the [[clarification-drift]] stance
(describe, don't drift the plan). **Adopted:** 2026-05-21. **Status:** active.
