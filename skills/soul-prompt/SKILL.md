---
name: soul-prompt
description: Rewrite a rough shorthand prompt into a well-formed, project-informed one and hand it back as an artifact to copy, edit, or run. Generated in a FRESH context that never saw this conversation, because the working session has already decided what the prompt means and cannot be a neutral reader of it. Invoked by the Body only; never acts on the prompt it produces.
disable-model-invocation: true
---

# /soul-prompt — rough prompt in, project-informed prompt out

`/soul-prompt [--handoff] <rough text>`

The Body writes terse prompts. A terse prompt is usually fine, but it under-names
the things a project already knows — the real file, the ID, the convention that
makes one obvious-looking choice wrong. This turns the shorthand into a prompt
that carries those, and hands it back as text to copy, edit, or run.

**The whole design rests on one point: the improver must not be this session.**
By the time the Body types `/soul-prompt`, the working session has already formed
a reading of what they meant. Ask it to restate the prompt and it returns its own
existing interpretation with better grammar — it cannot surprise the Body, because
the surprise is exactly what it already quietly resolved. So the rewrite happens in
a context that never saw the conversation. What it gets instead is the project's
doctrine, which is the durable version of the same knowledge and carries none of
the session's momentum.

**This is not the multi-agent synthesis SOUL-119 warned off.** That finding is about
splitting *judgment* across agents and losing it in the merge. Here there is one
agent, one pass, and nothing to synthesize — the subagent exists for **context
isolation**, not for parallelism or extra opinions. Its output is returned verbatim,
never merged.

## What to do

1. **Parse the invocation.** Everything after the flags is the rough text, verbatim —
   do not clean it up before passing it on. Typos and fragments are signal about what
   the Body actually cares about. `--handoff` adds `.soul/handoff.md` to the brief
   (what is in flight); it is the clean substitute for the conversation, because it is
   a written record rather than this session's live interpretation.

2. **Skip the subagent only for a genuinely mechanical instruction** — one unambiguous
   action on one named target ("add a trailing newline to mind.md"). Reply
   `Clear as written — nothing to resolve. Say go.` and stop. Keep this bar high: when
   in doubt, spawn. A wasted subagent costs a few thousand tokens; a rewrite the Body
   needed and did not get costs a whole misdirected task.

3. **Resolve the doctrine paths.** Read the project's root `CLAUDE.md` (small) and take
   the absolute paths from its import lines — typically `<soul-root>/operations/CLAUDE.md`
   and a project-local `mind.md`. Pass **paths**, not pasted content: the subagent reads
   them itself, which keeps them out of this session's context and makes a bad path fail
   loudly instead of silently. That is the SOUL-F038 lesson applied — an `@`-import into
   a foreign context can vanish and get confabulated at ~43%; an explicit `Read` either
   returns the file or errors.

   If the project has no Soul import (a non-Soul project), fall back to whatever project
   context exists — `CLAUDE.md`, `AGENTS.md`, `README.md` — and say in the reply that the
   doctrine was not found, so the Body knows the artifact is less informed than usual.

4. **Spawn ONE subagent** with the brief below. Do not spawn more, and do not answer the
   rough prompt yourself while waiting.

5. **Print what comes back, verbatim, in a fenced block**, then one line:
   `Say go to run it, or copy and edit.` Nothing else — no commentary on the artifact, no
   preview of how the work would go. Commentary is this session's interpretation leaking
   back in through the side door, which is the thing the separation exists to prevent.

6. **Check the sentinel.** The artifact ends with a footer naming the Mind's
   last-distilled date. If it is missing or wrong, the doctrine did not arrive — say so
   plainly and offer to re-run, rather than passing off an uninformed rewrite as an
   informed one.

7. **Stop.** Do not begin the work. If the Body says go, run the artifact as the prompt —
   at that point they have approved it, and execution by this session is fine.

## The brief

Give the subagent this, filled in. It is self-contained by design — the subagent has
no conversation to fall back on, which is the point.

> You are rewriting one rough prompt into a well-formed one. You have deliberately not
> been given the conversation it came from, so that you read it as written rather than
> as someone already decided it should be read.
>
> **First, read these files** with the Read tool — they are this project's doctrine:
> `<contract path>`, `<mind path>`<, `.soul/handoff.md` if `--handoff`>. If any read
> fails, stop and report which one; do not proceed on a guess.
>
> **The rough prompt, verbatim:** `<rough text>`
>
> **Your job:** return the prompt the Body should have written, given what the doctrine
> says about this project. Name the real files, IDs, and conventions that bear on the
> task. Surface a convention that would make an obvious choice wrong.
>
> **Preserve intent — improve specificity, not scope.** The commonest way this goes
> wrong is adding tasks the Body never asked for: a research step, an approval gate, a
> refactor "while we're in there." If you think something is missing, it goes in
> `Assumed` as a question, never into the task as an instruction. A rewrite that grows
> the job is not an improvement, it is a different request.
>
> **Do not restate obligations the receiving session already loads.** It reads the same
> contract you just did. Padding the prompt with "verify by execution" teaches the
> system that obligations ride on prompts rather than on structure, which is precisely
> backwards here.
>
> **Cost guard — this is a prompt rewrite, not an investigation.** Never bulk-read the
> record stores (`witness.md`, `ideas.md`, `findings/`, `amendments/`); on this project
> they run to roughly 300k tokens. A targeted grep for a named ID, then a few lines
> around the hit, is the whole allowance. Stay under about five tool calls; if the task
> genuinely cannot be specified without deeper reading, say so in one line and return
> what you have.
>
> Return only the artifact in the shape below, and nothing else — no preamble, no
> explanation of your reasoning.

## The artifact shape

```
<Task — one paragraph, imperative, with the real names, paths, and IDs in it.>

Files: <concrete paths>
Check against: <what to compare with, if anything>

Done when: <a check that can actually be run>

Conventions in play: <only if a real one bears — the branch rule, the anonymization
rule, a schema. Omit this line entirely when none applies; an empty ceremonial
heading trains the reader to skip the section on the day it matters.>

Assumed: <bullets for anything guessed, and any addition the Body did not ask for,
phrased so it can be corrected in a few words. This is the honesty channel — an
assumption that only lives in the task paragraph is a decision made on the Body's
behalf without telling them.>

[doctrine: <the Last-distilled date from the Mind you read>]
```

## What not to do

- Do **not** answer, plan, or begin the rough prompt. This produces a prompt; it is
  not a work instrument.
- Do **not** rewrite it in this session "to save a subagent." The saving is the
  contamination — see the framing above.
- Do **not** pass the conversation into the brief. If the subagent needs project state,
  that is what `--handoff` is for.
- Do **not** edit or improve the returned artifact. Print it verbatim; the Body edits it.
- Do **not** let the subagent explore the record. The guard in the brief is the load-
  bearing line for cost.

---

**Source:** Built 2026-08-12 at the Body's request after an in-session pressure-test.
The first draft was an in-session read-back (restate the task, ask 1–3 forked
questions); the Body rejected it on two counts — it duplicated the external `grilling`
skill, and it kept the improver inside the session that had already decided what the
prompt meant. The separate context is the load-bearing idea, and it is what the Body's
manual workflow (paste into a blank session, edit, bring back) was already doing by
hand; this keeps that separation and adds the project doctrine the blank session lacked.
Measurement of whether the project-informed rewrite beats the blank-session one was
raised and the Body declined it as unnecessary (contract rule 8 — said out loud, not
silently). No finding or idea ID yet. **Status:** draft, unproven in use.
