# Video pipeline — design

Silent explainer videos for the Soul System: what each skill does, and why the
system exists. This document is the contract for the pipeline. It records the
decisions made during alignment (2026-08-14, grill session Q1–Q13) with their
reasons, so future pressure on any of them lands here.

**Deliverables — seven videos:**

| Video | Sources | Budget |
|---|---|---|
| soul-capture *(pilot)* | its SKILL.md | 20–60s |
| handoff + resume *(one paired video — twin halves of one story)* | both SKILL.md | 20–60s |
| soul-next | its SKILL.md | 20–60s |
| soul-distill | its SKILL.md | 20–60s |
| soul-prompt | its SKILL.md | 20–60s |
| intro — "what is this, how do I start" (folds in help/init/explain) | README, skills/ | ≤180s, chaptered |
| philosophy — "why this exists" *(written last)* | philosophy/the-soul.md | ≤180s, chaptered |

**Audience** (Q1): a developer who just found Soul System and is deciding
whether to adopt it. Orient; don't teach mechanics — the SKILL.md does that.
Videos embed in the README/blog and upload to YouTube.

---

## Decision ledger

Settled during alignment; do not relitigate without new evidence.

| # | Decision | Reason |
|---|---|---|
| Q1 | Audience = prospective adopter | A 20–60s silent video can orient; it cannot teach mechanics |
| Q2 | Demos: record a real run once, freeze as committed **text**; artifact before/after diffs as complement | The skills are conversational (LLM output ≠ deterministic); frozen real text keeps both "never fabricate" and "same input, same output" |
| Q3 | MP4s live on YouTube + GitHub release artifacts; the repo carries text sources only | Plugin installs clone the whole repo (`source: "./"` — no file selection); committed binaries would ship to every installer |
| Q4 | Pipeline LLM stages are skills in this repo (they ship to installers — accepted) | This repo distributes skills; the prompt templates become the skill bodies |
| Q5 | Pilot = soul-capture | Core act of the system; strongest artifact-diff demo |
| Q6 | 16:9 only; components kept center-safe | 9:16 later is a re-layout, not a re-author |
| Q7 | No music for the pilot; CC0-only if ever added | One less licensing surface; zero effect on the gates |
| Q8 | Anonymization: human gate + gitignored local denylist linter | SOUL-169/175: real names must never reach a public surface — including a committed lint list |
| Q9 | Theme tokens codified from `architecture.svg` (soft anchor — may evolve) | The one existing branded artifact; the tokens file becomes the identity |
| Q10 | Five skill videos + intro + philosophy; overviews written last | Hardest scripts benefit from having done every individual skill first |
| Q11 | Staleness check is a local `tools/` script; no CI | Repo has zero CI; release cadence is manual (branch-per-release); revisit only when rendering is proven |
| Q12 | Renderer = **Manim CE**, not Motion Canvas | Motion Canvas is abandoned (last stable 2024-12, site offline) and has no headless mode; Manim CE is active (v0.21.0, 2026-08), CLI-native, deterministic, and Python — the repo's only existing runtime dependency |
| Q13 | VHS is a **capture instrument only** — renderer draws terminal scenes from committed text | VHS video output is not byte-deterministic; its `.ascii`/text output is |

---

## Toolchain

| Tool | Role | License | Notes |
|---|---|---|---|
| Manim Community Edition (pinned in `requirements.txt`) | Stage-3 renderer: storyboard → frames → mp4 | MIT | Headless by construction (Cairo → ffmpeg, no browser). Text via Pango (`Text`/`MarkupText`) only — **no LaTeX/Typst**, so no texlive dependency |
| ffmpeg | Muxing, chapter metadata, format variants | LGPL/GPL | Invoked with `-bitexact`-class flags so output bytes are stable |
| VHS (Charm) | *Capture only*: turn a scripted real run into deterministic `.ascii` text | MIT | Never in the render path. Real Claude-session excerpts (transcript text) serve the same role |
| Python 3 + PyYAML | Renderer glue, linter, staleness checker | PSF / MIT | Matches the repo's existing python3-only culture |
| Fonts: Gelasio (Georgia-metric serif), JetBrains Mono | Theme typography | OFL | **Fetched, not committed**: `setup.py` downloads pinned-sha256 files into gitignored `videos/.fonts/`. Keeps the repo text-only and the render reproducible; Georgia itself is a Windows font and can't be redistributed |
| `adithya-s-k/manim_skill` → `manimce-best-practices` | Authoring reference when building theme/components (Phase 2) | MIT | Install at Phase 2 kickoff; not part of the render path |

Known risks, accepted: Manim has no live-preview editor (mitigation: fast
low-res preview via `-ql` during theme development); the Manim CE upstream
could slow (mitigation: version pinned; renderer is ~6 scene components, small
surface to port).

---

## Directory layout

Single-skill video sources live **next to the skill they document** — a skill
change and its video change are one diff. Multi-source videos live under
`videos/`.

```
videos/
  render/                  # stage 3 — pure code, no LLM
    render.py              #   storyboard.yaml -> .mp4 + timings.json + chapters
    lint.py                #   schema + timing + denylist checks
    setup.py               #   one-time: venv deps + pinned font fetch
    timing.py              #   THE timing constants (see below)
    theme.py               #   tokens from architecture.svg; THEME_VERSION lives here
    components.py          #   one Manim component per scene type
    requirements.txt       #   exact-pinned (==) for deterministic renders
  manifest.json            # staleness manifest, written by render.py
  intro/                   # multi-source videos: script.md, storyboard.yaml, captures/
  philosophy/
  handoff-resume/
  out/                     # gitignored — rendered mp4s land here

skills/soul-capture/video/ # single-skill videos: same three-part shape
  script.md                #   gate 1 artifact (Body-approved)
  storyboard.yaml          #   gate 2 artifact (Body-approved)
  captures/                #   frozen text of real runs (transcript / VHS .ascii)

tools/
  video-staleness.py       # reports per video: FRESH / RENDER-STALE / SCRIPT-STALE
```

Rendering runs on **ext4** (venv + Manim media dir under `$HOME`), never on
`/mnt/d` — drvfs IO is known-slow here (see mind.md 5b for the precedent).
`render.py` copies the final mp4 into `videos/out/`.

---

## Storyboard schema

The contract between the LLM stages and the renderer. YAML; one file per
video; reviewable in under two minutes. Scene `hold` is **omitted by default**
— the renderer computes the minimum from the timing constants, so the human
reviews content and order, not arithmetic. An explicit `hold` is allowed only
at or above the computed minimum (linter-enforced).

```yaml
video: soul-capture        # id, unique across the manifest
schema: 1                  # storyboard schema version
format: skill              # skill (<=60s) | overview (<=180s, chapters allowed)
inputs:                    # staleness: video is SCRIPT-STALE if any of these change
  - skills/soul-capture/SKILL.md
scenes:
  - id: hook               # stable id — anchors timings.json and future narration
    type: title
    heading: "Your session is about to forget something."
    sub: "soul-capture"
    transition: fade       # fade | cut  (default: fade)

  - id: modes
    type: bullets
    heading: "Three modes, three levels of friction"
    items:                 # revealed sequentially
      - "idea — frictionless, forward"
      - "witness — light scaffold, backward"
      - "finding — earned, scaffolded"

  - id: demo
    type: terminal
    capture: captures/capture-idea.txt   # frozen text of a REAL run (Q2/Q13)
    reveal: line           # line | block

  - id: landed
    type: code             # also used for artifact before/after diffs
    lang: markdown
    file: captures/witness-after.md
    highlight: [3, 4]

  - id: outro
    type: outro
    text: "Capture the unguessable."
    url: "github.com/soul-system-works/Soul-System"
```

Scene types (complete set for v1): `title`, `bullets`, `code`, `terminal`,
`diagram` (renders a theme-recolored SVG asset: `asset: <path>`), `outro`.
Overview storyboards may add `chapter: "<name>"` to a scene; the renderer
emits ffmpeg chapter metadata at each chapter boundary.

Reserved, ignored by the v1 renderer: `narration:` (see voiceover section).

---

## Timing rules

Constants live in `videos/render/timing.py` and nowhere else. The linter
enforces them; taste doesn't.

```
BASE_HOLD       = 1.5    # s — every scene, before any text
WORD_RATE       = 0.35   # s per word of prose (headings, bullets, outro)
CODE_BASE       = 1.0    # s — extra settle time for code/terminal scenes
CODE_LINE_RATE  = 0.6    # s per visible code/terminal line
TRANSITION_DUR  = 0.4    # s (fade); cut = 0. Not counted against hold
MAX_WORDS_SCENE = 26     # one-idea-per-scene proxy (prose scenes)
MAX_BULLETS     = 4      # per bullets scene
MAX_CODE_LINES  = 12     # per code/terminal scene
BUDGET_SKILL    = 60.0   # s — hard lint failure
BUDGET_OVERVIEW = 180.0  # s — hard lint failure
```

A storyboard over budget fails lint. The fix is cutting scenes — holds never
shrink below the computed minimum (settled in the brief; the linter makes it
mechanical).

---

## Staleness and determinism

**Determinism**: stage 3 is pure code. Same storyboard + captures + theme +
pinned environment ⇒ byte-identical mp4 (Manim's frame-stepped rendering plus
ffmpeg bitexact flags). No wall-clock recording and no LLM sit anywhere in the
render path — that property is what makes hashing meaningful.

**Manifest** (`videos/manifest.json`, written by `render.py` on success):

```json
{
  "soul-capture": {
    "storyboard": "skills/soul-capture/video/storyboard.yaml",
    "theme_version": 1,
    "hashes": {
      "skills/soul-capture/SKILL.md": "sha256:…",
      "skills/soul-capture/video/storyboard.yaml": "sha256:…",
      "skills/soul-capture/video/captures/capture-idea.txt": "sha256:…"
    },
    "output": "sha256:…"
  }
}
```

**Two levels of stale**, reported by `tools/video-staleness.py`:

- **SCRIPT-STALE** — a declared `input` (e.g. the SKILL.md) changed since the
  last render. The *meaning* may have moved: both human gates re-run (script →
  storyboard → render).
- **RENDER-STALE** — only the storyboard, captures, or `THEME_VERSION`
  changed. Re-render autonomously; no gate.

Bumping `THEME_VERSION` in `theme.py` marks every video RENDER-STALE — the
whole set re-renders under the new look with zero re-authoring. A single skill
edit marks exactly one video stale (per-skill regeneration, from the brief).

**Approval is a commit.** There is no separate approval registry: the Body
approving a script or storyboard *is* the act of committing it (or telling the
session to). Git history is the gate record.

---

## Gates and workflow

```
SKILL.md ──(1: LLM)──> script.md ──[Body approves]──(2: LLM)──> storyboard.yaml
            ──[Body approves]──(3: pure code)──> out/<video>.mp4 + timings.json
```

Stages 1–2 ship as **one skill, mode-token style** (matching soul-capture's
design language): `skills/soul-video/SKILL.md`, `disable-model-invocation:
true` (operator-invoked only, like the other utility skills).

- `/soul-video script <video-id>` — stage 1. Reads the declared inputs (never
  assumptions), drafts `script.md`, holds for the Body.
- `/soul-video storyboard <video-id>` — stage 2. Reads the approved script,
  drafts `storyboard.yaml`, runs `lint.py`, presents the lint result with the
  draft, holds for the Body.
- `/soul-video render <video-id>` — thin wrapper over `render.py` (stage 3
  itself contains no LLM).
- `/soul-video status` — thin wrapper over `tools/video-staleness.py`.

The stage-1 and stage-2 prompt templates are the corresponding sections of
that SKILL.md — version-controlled, as the brief requires.

**Anonymization gate** (Q8): `lint.py` reads `.soul/denylist.txt` (already a
gitignored directory; one name per line; case-insensitive substring match) and
scans the script, storyboard, and captures. Any hit fails the lint. A missing
denylist prints a visible warning rather than failing, so contributor machines
still lint — but the Body's machine, which has the list, is the gate that
counts. The names themselves never enter the repo. The human gates remain
primary; the linter is the backstop.

Captures of real runs are reviewed at gate 2 like everything else — they are
the highest-risk surface for both names and fabrication.

---

## Publishing

- **YouTube**: the public home; docs/blog embed from there. Upload is manual
  in Phase 2–3 (an upload skill can earn its place later).
- **GitHub release artifacts**: the durable copy — mp4s attach to the plugin
  release that shipped them (repo already versions releases; branch-per-
  release means videos ride the same train as the work they document).
- Naming: `<video-id>-t<THEME_VERSION>.mp4`. Chapters embedded for overview
  videos only.

---

## Voiceover later, without re-authoring (designed-in, not built)

- Every scene has a stable `id`; every render emits `timings.json`
  (`scene id → start, end`). A future narration stage consumes that sidecar
  and muxes an audio track post-hoc — visuals untouched.
- `narration:` is reserved in the schema now, ignored by the v1 renderer, so
  storyboards can carry narration text before any audio stage exists.
- If narration ever needs more air than the holds provide, a global hold
  multiplier in `timing.py` stretches every scene proportionally — a
  re-render, not a re-author.
- The optional music bed for the YouTube cut is the same post-hoc mux (Q7:
  none for now; CC0-only if ever).

---

## Phase plan (unchanged from the brief, restated against this design)

- **Phase 2 — pilot**: theme.py + components.py + render.py + lint.py, the
  `/soul-video` skill, and soul-capture end to end. Three checkpoints: script,
  storyboard, video.
- **Phase 3 — scale out**: remaining skill videos, `tools/video-staleness.py`
  wired into the release habit, `videos/README.md` (how to add a video), then
  intro, then philosophy last.
