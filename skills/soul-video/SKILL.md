---
name: soul-video
description: Operate the explainer-video pipeline in one of four modes — script (SKILL.md → script.md draft, Body-gated), storyboard (script.md → storyboard.yaml, linted, Body-gated), render (pure-code wrapper, no LLM), status (staleness report). The mode token is the first arg. Spec and schema live in docs/video-pipeline.md. Body-invoked only.
disable-model-invocation: true
---

# /soul-video — explainer-video pipeline

`/soul-video <mode> <video-id>` where **mode** is `script`, `storyboard`, `render`,
or `status`. The spec — storyboard schema, timing constants, staleness model,
decision ledger — is `docs/video-pipeline.md`; read it before modes `script` and
`storyboard`. If no mode is given, **ask** — do not guess the stage.

A `<video-id>` resolves to a source directory: `skills/<video-id>/video/` for
single-skill videos, `videos/<video-id>/` for multi-source ones (intro,
philosophy, handoff-resume).

**Rules shared by every mode:**

- **Audience** (ledger Q1): a developer who just found Soul System, deciding
  whether to adopt it. Orient; don't teach mechanics.
- **Silent.** On-screen text carries all the meaning. Design for reading speed.
- **Read the declared inputs — never memory.** A script written from
  assumptions about what a skill does is fabrication with extra steps.
- **Never fabricate terminal content** (ledger Q2/Q13). Every `terminal` scene
  replays committed text from a real run. No real run, no scene.
- **No real project or client names, anywhere** (ledger Q8; SOUL-169/175).
  The human gates are primary; `lint.py`'s denylist scan is the backstop.
- **One idea per scene.** Over budget → cut scenes. Holds never shrink below
  the computed minimum.
- **Approval is a commit.** Nothing advances a stage until the Body has
  approved the previous artifact (told the session to commit it, or committed
  it themselves).

## Mode `script` — stage 1 (LLM, Body-gated)

1. Read `docs/video-pipeline.md`, then read **all** of the video's declared
   source inputs in full (for a skill video: that skill's `SKILL.md`).
2. Draft `<source-dir>/script.md`:

   ```markdown
   # Script — <video-id>
   Format: skill | overview · Audience: prospective adopter
   Sources read: <paths>

   ## Beat 1 — <name> (<suggested scene type>)
   On screen: "<the verbatim text the viewer reads>"
   Intent: <one line — what this beat does to the viewer>

   ...more beats...

   Captures needed at storyboard stage: <real runs to collect, or "none">
   Estimated runtime: ~<n>s (BASE_HOLD + WORD_RATE × words, per timing.py)
   ```

3. Skill format: aim for 5–8 beats, ≤60s estimated. Overview: ≤180s,
   chapter groupings named. Over budget → cut beats now, at the cheap stage.
4. **Show the draft and hold.** The Body approves, edits, or rejects. Do not
   start the storyboard in the same breath.

## Mode `storyboard` — stage 2 (LLM, Body-gated)

1. Read the **approved** `script.md`. Not approved (uncommitted, or the Body
   hasn't said so) → stop and say what's missing.
2. Collect captures the script calls for: a real run frozen as text (VHS
   `.ascii` or a verbatim transcript excerpt), stored under
   `<source-dir>/captures/`. Collect them *with* the Body — never synthesize.
3. Draft `<source-dir>/storyboard.yaml` against the schema in
   `docs/video-pipeline.md`. Omit `hold` unless a scene genuinely needs more
   air than the computed minimum; give every scene a stable `id`.
4. Lint it: `~/.cache/soul-video/venv/bin/python videos/render/lint.py
   <storyboard>`. Fix failures before presenting.
5. **Show the draft plus the lint report** (per-scene holds, total runtime)
   and hold for the Body.

## Mode `render` — stage 3 wrapper (pure code, NO LLM decisions)

Run: `~/.cache/soul-video/venv/bin/python videos/render/render.py
<source-dir>/storyboard.yaml`. Report the output path, sha256, and duration.
This mode makes no content choices — if the render fails, fix the pipeline or
return to `storyboard`; never patch content ad hoc to make rendering pass.

## Mode `status` — staleness report

Run: `python3 tools/video-staleness.py` (arrives with Phase 3; until it
exists, report which videos have manifest entries and which sources changed
since, from `videos/manifest.json` + git). Report per video: FRESH /
RENDER-STALE (re-render autonomously OK) / SCRIPT-STALE (both human gates
re-run).

## What not to do

- Do not write a script from what you assume a skill does — read its file.
- Do not invent, embellish, or "clean up" terminal output. Verbatim or absent.
- Do not shrink holds to fit a budget — cut content instead.
- Do not run two gates in one turn; each approval is the Body's separate act.
- Do not commit — the Body owns the commit moment.

---

**Source:** `docs/video-pipeline.md` (Phase 1 design, 2026-08-14, ledger
Q1–Q13). Stage templates here ARE the version-controlled prompt templates the
brief required. **Status:** pilot (soul-capture) in progress.
