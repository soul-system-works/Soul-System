"""One builder per scene type, plus the shared motion primitives (Q14).

Each declarative builder returns a SceneBuild: `group` is everything on screen
when the scene's transition finishes, `reveals` are mobjects added one at a time
during the hold. Reveals are consumed out of the hold, so a builder can never
change a scene's duration — timing.py owns that.

================================================================================
CUSTOM SCENE BUILDER CONTRACT  (scene type `custom`; docs/video-pipeline.md Q14)
================================================================================

A `custom` scene names a Python file and a function in it::

    - id: lifeline
      type: custom
      module: motion.py        # resolved against the storyboard's directory
      name: build              # the function below
      duration: 7.5            # seconds — explicit, and the WHOLE slot
      text:                    # EVERY on-screen string this scene shows
        - "The record"
        - "capture"

render.py calls it as::

    build(scene, theme, components, duration)

  scene       the running Manim Scene. Call scene.play / scene.wait / scene.add
              on it directly; this is not a SceneBuild-returning builder.
  theme       the loaded theme module — every colour, size and speed comes from
              here, never from a literal.
  components  this module. The primitives below are the point of it.
  duration    seconds, already frame-quantised. This is the builder's ENTIRE
              slot: the renderer adds no hold before or after. The incoming
              transition (a fade-out of the previous scene) is spent before the
              builder is called and is NOT part of `duration`.

Five rules, each of which the renderer or the linter enforces:

1. SPEND THE SLOT EXACTLY. render.py measures the scene clock across the call
   and aborts the render if it moved by even one frame more or less than
   `duration`. timings.json is a published sidecar (a future narration stage
   muxes against it) — a builder that overruns makes it a lie. Use
   frames_for() / run_time() / hold_time() below rather than passing raw
   seconds to play(), and spend any leftover with a trailing frozen wait. Every
   primitive here consumes exactly frames_for(its own duration) frames, so the
   arithmetic is yours to close: sum what you asked for, subtract from
   frames_for(duration), wait out the rest.

2. DECLARE EVERY STRING in the storyboard's `text:`. The linter cannot read
   inside the builder, so `text:` is what it denylist-scans and what it charges
   the read rate for: `duration` must be at least BASE_HOLD + WORD_RATE x words.
   The module's own source is denylist-scanned too, so a name in a literal is
   caught either way — but an undeclared string buys no reading time.

3. BE PURE CODE. No wall clock (time, datetime.now, perf_counter), no unseeded
   randomness, no network, no filesystem reads outside the storyboard's own
   directory. Determinism is what makes the manifest's hashes mean anything;
   the seeds and media wipe render.py already sets do not rescue a builder that
   asks the machine what time it is. Two specifics: do not touch
   scene.renderer — render.py reads its clock either side of your call and a
   builder that moves it makes the drift check measure the wrong thing — and do
   not mutate module state on `theme` or `components`, because a later scene,
   or the same video's second render in one process, would inherit it and the
   two renders would not match.

4. STAY CENTRE-SAFE (Q6). Lay out inside fit_safe()/safe_size() so a later 9:16
   cut is a re-layout, not a re-author.

5. BE ONE FILE. The linter rejects any import in a builder module that resolves
   to a file beside it (relative imports included). A local helper is invisible
   twice over: it is not a denylist-scanned surface, so a real name in it
   reaches a public video unchecked, and it is not a hashed input, so editing it
   leaves the video reported FRESH when its content has changed. The graduation
   path is the point of this module — motion that recurs across videos moves
   INTO components.py, which every video already tracks through THEME_VERSION.
   A pattern used once stays inline in its own video's module.

Stdlib and installed packages are fine; it is only local files that are barred.
"""

import numpy as np

import theme  # must precede manim: sets FONTCONFIG_FILE before Pango starts

from manim import (
    BOLD, DOWN, LEFT, ORIGIN, RIGHT, UP,
    Code, Create, FadeIn, FadeOut, Line, Polygon, Rectangle,
    RoundedRectangle, SVGMobject, Text, VGroup, config,
)

import lint
import timing


class SceneBuild:
    def __init__(self, group, reveals=None):
        self.group = group
        self.reveals = reveals or []


def frames_for(seconds: float) -> int:
    """Whole frames, rounded UP — the same quantiser lint.build_plan lays out on."""
    return lint.frames_up(seconds)


def run_time(frames: int) -> float:
    """Seconds to ask an ANIMATION for so it emits exactly `frames` frames.

    Manim steps animations with np.arange(0, run_time, 1/fps) — effectively
    ceil(run_time * fps). Asking half a frame short of the target keeps float
    error from ever tipping that ceil to frames + 1.
    """
    return (frames - 0.5) / theme.FPS


def hold_time(frames: int) -> float:
    """Seconds to ask a frozen WAIT for so it emits exactly `frames` frames.

    Different quantiser from run_time, and the difference is silent: a frozen
    wait goes through freeze_current_frame, which TRUNCATES (int(duration/dt))
    instead of rounding up. Half a frame long, not short.
    """
    return (frames + 0.5) / theme.FPS


def safe_size() -> tuple[float, float]:
    """(width, height) of the centred safe column, in Manim units (Q6)."""
    return (config.frame_width * theme.SAFE_W_FRAC,
            config.frame_height * theme.SAFE_H_FRAC)


def fit_safe(mobject):
    """Scale into the centred safe column and park it at frame centre (Q6)."""
    max_w = config.frame_width * theme.SAFE_W_FRAC
    max_h = config.frame_height * theme.SAFE_H_FRAC
    if mobject.width > max_w:
        mobject.scale(max_w / mobject.width)
    if mobject.height > max_h:
        mobject.scale(max_h / mobject.height)
    mobject.move_to(ORIGIN)
    return mobject


def serif(text, size=None, color=None, weight=None, t2c=None, t2w=None):
    """Prose in the theme's serif. The only way any builder should make prose.

    Public because custom scenes were re-declaring it privately and drifting:
    the point of a theme is that nobody names a font at a call site.

    t2c/t2w pass through to Pango (substring -> color / weight): the per-beat
    key-term emphasis (Q20) rides these rather than glyph slicing, because
    Pango spans survive ligatures and kerning where index arithmetic does not
    (see split_rows for the failure that rule comes from).
    """
    return Text(str(text), font=theme.SERIF, font_size=size or theme.SIZE_SUB,
                color=color or theme.INK, weight=weight or "NORMAL",
                t2c=t2c, t2w=t2w)


def mono(text, size=None, color=None, weight=None, t2c=None, t2w=None):
    """Code / identifiers / URLs in the theme's monospace. See serif()."""
    return Text(str(text), font=theme.MONO, font_size=size or theme.SIZE_TERMINAL,
                color=color or theme.INK, weight=weight or "NORMAL",
                t2c=t2c, t2w=t2w)


# Kept as private aliases so the declarative builders below read unchanged.
_serif, _mono = serif, mono


def glow(mobject, color=None, layers=None, spread=None, opacity=None) -> VGroup:
    """The theme's light treatment: `mobject` re-emitting into the dark (Q17).

    Returns a VGroup of the halo copies ONLY — add it behind the mobject, or
    wrap both with `lit()`. Copies are stroked progressively wider and fainter,
    which is pure geometry: no shader, no image filter, no sampling, so it
    survives the byte-identity check like everything else here.

    Fill is deliberately dropped from the halo copies. A filled halo grows a
    solid slab around a card instead of a rim of light.
    """
    color = color or theme.GLOW
    layers = theme.GLOW_LAYERS if layers is None else layers
    spread = theme.GLOW_SPREAD if spread is None else spread
    opacity = theme.GLOW_OPACITY if opacity is None else opacity

    halo = []
    for i in range(layers):
        copy = mobject.copy()
        copy.set_fill(opacity=0.0)
        # Width grows linearly, opacity halves: the near layer carries the rim,
        # the far ones only tint the ground around it.
        copy.set_stroke(color=color, width=(i + 1) * spread,
                        opacity=opacity * (0.5 ** i))
        halo.append(copy)
    # Widest first, so the tightest, brightest layer sits closest to the core.
    return VGroup(*reversed(halo))


def lit(mobject, color=None, **kwargs) -> VGroup:
    """`mobject` with its glow behind it, as one group."""
    return VGroup(glow(mobject, color=color, **kwargs), mobject)


def _has_glyphs(line) -> bool:
    # A Paragraph line is a VGroup of glyphs; has_points() is False even when
    # drawn, so height is the only honest emptiness test.
    return line.height > 1e-6


def _drawn(paragraph):
    return [(i, line) for i, line in enumerate(paragraph.submobjects) if _has_glyphs(line)]


def _line_pitch(paragraph) -> float:
    """Vertical spacing between lines — blank lines carry no geometry of their own."""
    drawn = _drawn(paragraph)
    if len(drawn) < 2:
        return max(paragraph.height, 0.2) + 0.12
    (i, first), (j, second) = drawn[0], drawn[1]
    return abs(first.get_center()[1] - second.get_center()[1]) / (j - i)


def _line_y(paragraph, index: int) -> float:
    """Centre y of line `index`, extrapolated so blank lines still have a position."""
    anchor, line = _drawn(paragraph)[0]
    return line.get_center()[1] - (index - anchor) * _line_pitch(paragraph)


def build_title(scene, ctx):
    parts = [_serif(scene["heading"], theme.SIZE_HEADING, theme.INK, BOLD)]
    if scene.get("sub"):
        parts.append(_serif(scene["sub"], theme.SIZE_SUB, theme.MUTED))
    group = VGroup(*parts).arrange(DOWN, buff=theme.LINE_GAP * 1.8)
    return SceneBuild(fit_safe(group))


def build_bullets(scene, ctx):
    heading = _serif(scene["heading"], theme.SIZE_HEADING * 0.82, theme.INK, BOLD)
    items = []
    for text in scene["items"]:
        dash = _serif("—", theme.SIZE_BULLET, theme.GLOW)
        body = _serif(str(text), theme.SIZE_BULLET, theme.INK)
        items.append(VGroup(dash, body).arrange(RIGHT, buff=0.28))
    stack = VGroup(*items).arrange(DOWN, buff=theme.BULLET_GAP, aligned_edge=LEFT)
    group = VGroup(heading, stack).arrange(DOWN, buff=theme.LINE_GAP * 2.2,
                                           aligned_edge=LEFT)
    fit_safe(group)
    # Items are revealed sequentially, so only the heading fades in with the scene.
    return SceneBuild(VGroup(heading), reveals=list(items))


def build_code(scene, ctx):
    source = lint.code_source(scene, ctx["sb_dir"])
    lines = lint.visible_lines(source)
    code = Code(
        code_string="\n".join(lines),
        language=scene.get("lang"),
        formatter_style=theme.PYGMENTS_STYLE,
        add_line_numbers=True,
        background="rectangle",
        # Code's own background is made invisible and replaced below: an opaque
        # one would sit on top of the highlight bands and hide them.
        background_config={"fill_opacity": 0.0, "stroke_width": 0.0},
        paragraph_config={"font": theme.MONO, "font_size": theme.SIZE_CODE},
    )
    panel = RoundedRectangle(
        width=code.width, height=code.height, corner_radius=0.08,
        fill_color=theme.CODE_PANEL, fill_opacity=1.0,
        stroke_color=theme.PANEL_RIM, stroke_width=1.2,
    ).move_to(code.get_center())
    members = [panel]
    for n in scene.get("highlight") or []:
        pitch = _line_pitch(code.code_lines)
        # On dark, v1's 0.55 amber slab would swallow the glyphs sitting on it.
        # A translucent wash under a lit edge marks the line without painting
        # over a single character of it.
        band = Rectangle(
            width=code.width * 0.97, height=pitch,
            fill_color=theme.GLOW, fill_opacity=theme.HIGHLIGHT_FILL_OPACITY,
            stroke_color=theme.GLOW, stroke_width=1.0,
            stroke_opacity=theme.HIGHLIGHT_STROKE_OPACITY,
        )
        # One band per line rather than one around the set: highlights need not
        # be contiguous, and adjacent bands meet at the line pitch anyway.
        band.move_to([code.get_center()[0], _line_y(code.code_lines, n - 1), 0])
        members.append(band)  # behind the glyphs
    members.append(code)
    return SceneBuild(fit_safe(VGroup(*members)))


def split_rows(block, lines, text_kwargs) -> list[VGroup]:
    """Split a multi-line Text into one VGroup per source line, BY GLYPH COUNT.

    Manim's Paragraph does this by character index and gets it wrong twice over
    (manim 0.21 text_mobject.py): it counts only NON-space characters per line
    while slicing a list that contains every character, so each space shifts
    every later line's slice — and `disable_ligatures=True`, the documented
    escape, cannot switch off JetBrains Mono's `calt` ligatures, so `--fixture`
    still collapses two characters into one glyph and Text raises. Geometry is
    no better at terminal pitch (found at the 2026-08-17 pre-commit review,
    both reproduced): an underscore's centre sits more than half a row below
    its neighbours, so rounding y to a row index deals every `_` one row down,
    and a blank FIRST line un-anchors a topmost-glyph grid. What is reliable:
    a multi-line Text lays glyphs out in source order, and a line rendered
    ALONE in the same style shapes to the same glyph count as inside the block
    (ligatures cannot span a newline). So each line's count is measured on a
    throwaway single-line render and the block's glyphs are dealt out in
    order; the sum is checked so a mismatch aborts instead of mis-grouping.

    `lines` is the source strings; `text_kwargs` the exact style the block was
    rendered with. Rows for blank source lines come back empty, which is what
    makes a line-by-line reveal skip them without stalling.
    """
    lines = [str(ln) for ln in lines]
    rows = [VGroup() for _ in lines]
    glyphs = list(block.submobjects)
    counts = [len(Text(ln, **text_kwargs).submobjects) if ln.strip() else 0
              for ln in lines]
    if sum(counts) != len(glyphs):
        raise ValueError(
            f"terminal_panel: the block rendered {len(glyphs)} glyphs but its "
            f"lines rendered alone total {sum(counts)} — per-line shaping does "
            f"not match the block, so the transcript would be mis-grouped")
    dealt = iter(glyphs)
    for row, n in zip(rows, counts):
        for _ in range(n):
            row.add(next(dealt))
    return rows


class TerminalPanel:
    """What terminal_panel() hands back. Members are scene mobjects, not copies."""

    def __init__(self, panel, body, rows):
        self.panel = panel
        self.body = body            # every glyph, as one mobject
        self.rows = rows            # one VGroup per SOURCE line; blanks empty
        self.group = VGroup(panel, body)
        self.drawn = [r for r in rows if len(r)]


def terminal_panel(lines, fg=None, size=None, pad=None) -> TerminalPanel:
    """A replay panel: monospace transcript on a lifted, rimmed surface.

    Handed back UNPLACED — a custom scene rarely wants frame centre, and
    fit_safe() is the caller's decision. `drawn` is the rows carrying glyphs,
    in order, so a caller revealing line-by-line does not stall on blanks.

    The transcript goes in VERBATIM, leading whitespace included: one multi-line
    Text renders indentation exactly (Pango never ate it — Paragraph did, see
    split_rows), so the capture file is neither rewritten nor re-typed and what
    is on screen is what the human gate reviewed.

    Public because the pilot's custom scenes had reimplemented this panel line
    for line: one look, one policy, one place to change either.
    """
    lines = list(lines)
    if not lines:
        raise ValueError("terminal_panel: no lines to draw")
    style = {"font": theme.MONO, "font_size": size or theme.SIZE_TERMINAL,
             "color": fg or theme.TERMINAL_FG, "line_spacing": 0.6}
    body = Text("\n".join(lines), **style)
    rows = split_rows(body, lines, style)

    pad = theme.PANEL_PAD if pad is None else pad
    panel = RoundedRectangle(
        width=body.width + pad * 2,
        height=body.height + pad * 2,
        corner_radius=0.12,
        # Value + rim, not contrast: on the dark ground the panel separates by
        # being lifted and edged, so it never competes with the amber lights.
        fill_color=theme.TERMINAL_BG, fill_opacity=1.0,
        stroke_color=theme.PANEL_RIM, stroke_width=theme.PANEL_RIM_WIDTH,
    )
    panel.move_to(body.get_center())
    return TerminalPanel(panel, body, rows)


def build_terminal(scene, ctx):
    text = (ctx["sb_dir"] / scene["capture"]).read_text(encoding="utf-8")
    term = terminal_panel(lint.visible_lines(text))
    fit_safe(term.group)
    if scene.get("reveal", "block") == "line":
        return SceneBuild(VGroup(term.panel), reveals=term.drawn)
    return SceneBuild(term.group)


def build_diagram(scene, ctx):
    svg = SVGMobject(str(ctx["sb_dir"] / scene["asset"]))
    members = []
    # Unlike prose, a diagram has no intrinsic size worth honouring — scale it up
    # to the safe column rather than only down.
    max_w = config.frame_width * theme.SAFE_W_FRAC
    max_h = config.frame_height * theme.SAFE_H_FRAC
    if scene.get("heading"):
        max_h *= 0.8
        members.append(_serif(scene["heading"], theme.SIZE_HEADING * 0.7,
                              theme.INK, BOLD))
    svg.scale(min(max_w / svg.width, max_h / svg.height))
    members.append(svg)
    group = VGroup(*members).arrange(DOWN, buff=theme.LINE_GAP * 1.6)
    return SceneBuild(fit_safe(group))


def build_outro(scene, ctx):
    parts = [_serif(scene["text"], theme.SIZE_OUTRO, theme.INK, BOLD)]
    if scene.get("url"):
        parts.append(_mono(scene["url"], theme.SIZE_URL, theme.MUTED))
    group = VGroup(*parts).arrange(DOWN, buff=theme.LINE_GAP * 2.0)
    return SceneBuild(fit_safe(group))


# ---------------------------------------------------------------------------
# Shared motion primitives — for `custom` scene builders (see the contract at
# the top of this file). Every one of them consumes a whole number of frames and
# RETURNS that number, so a builder can close its own arithmetic against the
# slot render.py measures.
# ---------------------------------------------------------------------------


def _point(where):
    """A position, from either a mobject or a raw [x, y, z]."""
    if hasattr(where, "get_center"):
        return where.get_center()
    return np.array(where, dtype=float)


class Lifeline:
    """Handle for a drawn thread — see thread(). Not constructed directly."""

    def __init__(self, line, marks, persistent, halos=()):
        self.line = line              # VGroup of the drawn segments (cores+halos)
        self.marks = VGroup(*marks)   # every mark, persistent or not
        self.persistent = VGroup(*persistent)
        self.group = VGroup(self.line, self.marks)
        self.halos = list(halos)      # the filament's light, separable from it
        # Identity, not equality: two marks with the same label are two marks.
        self._doomed = [m for m in marks if not any(m is p for p in persistent)]

    def end(self, scene, duration) -> int:
        """Stop the thread: the light goes out, THEN the filament dims away.

        Two stages on purpose (Q17). One FadeOut of everything reads as a
        drawing being erased; the glow dying first, and the line only then
        going, reads as something that was alive stopping — which is the whole
        argument of the mortality beat. Marks flagged `persistent` keep their
        light: that is the one lamp still on after the session is gone.

        Returns frames consumed.
        """
        frames = frames_for(duration)
        dying = [*self.halos]
        for mark in self._doomed:
            halo = getattr(mark, "halo", None)
            if halo is not None:
                dying.append(halo)
        remains = [self.line, *self._doomed]

        if frames < 4 or not dying:
            # Too short to stage; one gesture beats a two-frame flicker.
            scene.play(*[FadeOut(m) for m in remains], run_time=run_time(frames))
            return frames

        die_f = min(max(int(round(frames * theme.GLOW_DIE_FRAC)), 2), frames - 2)
        scene.play(*[FadeOut(m) for m in dying], run_time=run_time(die_f))
        scene.play(*[FadeOut(m) for m in remains],
                   run_time=run_time(frames - die_f))
        return frames


def _mark(x: float, y: float, label, color) -> VGroup:
    """A lit tick on the filament, with a quiet caption above it.

    The tick glows; the caption does not. A haloed label smears into itself at
    this size, and the words have to stay readable while the light does the
    emotional work — the mark's `.halo` is exposed so Lifeline.end() can kill
    the light without touching the text.
    """
    tick = Line([x, y - theme.THREAD_TICK, 0], [x, y + theme.THREAD_TICK, 0],
                stroke_width=theme.THREAD_STROKE, color=color)
    halo = glow(tick, color=color)
    parts = [halo, tick]
    if label:
        caption = _serif(str(label), theme.SIZE_MARK, theme.MUTED)
        caption.next_to(tick, UP, buff=theme.MARK_GAP)
        parts.append(caption)
    mark = VGroup(*parts)
    mark.halo = halo
    return mark


def thread(scene, duration, marks=(), y=0.0, width=None, color=None,
           label=None) -> Lifeline:
    """Draw a session lifeline left-to-right, dropping labelled marks as it goes.

    The spine of every "a session runs, things happen in it, then it ends" beat.
    Start a second thread by calling this again with a lower `y` — two lifelines
    one above the other is the handoff/resume shape.

        marks     iterable of {"at": 0..1, "label": str, "persistent": bool};
                  `at` is the fraction along the thread where the mark lands.
        y         vertical offset from frame centre, in Manim units.
        width     defaults to the safe column, and is clamped to it.
        label     optional caption at the left end (drawn instantly, 0 frames).

    Returns a Lifeline; call .end(scene, seconds) to fade it. Consumes exactly
    frames_for(duration) frames.
    """
    color = color or theme.GLOW
    max_w, _ = safe_size()

    # The caption is part of the assembly, not decoration hung off its end: its
    # width is reserved out of the safe column BEFORE the line is sized, or a
    # default-width thread pushes its own label off frame (contract rule 4).
    caption = None
    reserved = 0.0
    if label:
        caption = _serif(str(label), theme.SIZE_MARK, theme.MUTED)
        reserved = caption.width + theme.MARK_GAP * 2
    avail = max_w - reserved
    if avail <= 0:
        raise ValueError(f"thread: label {label!r} alone fills the safe column "
                         f"({max_w:.2f} units) — shorten it")
    width = min(float(width) if width else avail, avail)
    if reserved + width > max_w + 1e-6:
        raise ValueError(f"thread: line ({width:.2f}) plus label ({reserved:.2f}) "
                         f"exceeds the safe column ({max_w:.2f} units)")

    marks = [dict(m) for m in marks]
    for spec in marks:
        spec["at"] = float(spec.get("at", 0.5))
        if not 0.0 <= spec["at"] <= 1.0:
            raise ValueError(f"thread: mark 'at' must be within 0..1, got {spec['at']}")
    marks.sort(key=lambda m: m["at"])

    total_f = frames_for(duration)
    pop_f = frames_for(theme.MARK_POP)
    draw_f = total_f - pop_f * len(marks)
    if draw_f < 1:
        raise ValueError(
            f"thread: {duration}s ({total_f} frames) cannot hold {len(marks)} "
            f"marks at MARK_POP ({theme.MARK_POP}s = {pop_f} frames) plus a draw")

    left = -(reserved + width) / 2.0 + reserved
    fractions = [0.0] + [m["at"] for m in marks] + [1.0]
    # Segment boundaries are laid out on the frame grid FIRST, then made
    # monotone, so the frames always sum back to draw_f no matter how the marks
    # round — the slot has to close exactly.
    stops = [int(round(f * draw_f)) for f in fractions]
    stops[0], stops[-1] = 0, draw_f
    for i in range(1, len(stops)):
        stops[i] = min(max(stops[i], stops[i - 1]), draw_f)

    extras = []
    if caption is not None:
        # Placed from the geometry, not next_to() on the drawn line: the caption
        # names the thread from the first frame, so it cannot wait for segments
        # that do not exist yet.
        caption.move_to([left - theme.MARK_GAP - caption.width / 2, y, 0])
        scene.add(caption)
        extras.append(caption)

    segments, halos, built, persistent = [], [], [], []
    for i in range(len(fractions) - 1):
        x0 = left + fractions[i] * width
        x1 = left + fractions[i + 1] * width
        seg_f = stops[i + 1] - stops[i]
        if abs(x1 - x0) > 1e-9:
            core = Line([x0, y, 0], [x1, y, 0],
                        stroke_width=theme.THREAD_STROKE, color=color)
            # A filament, not a rule: the halo is Created alongside the core so
            # the light arrives with the line rather than switching on after it.
            halo = glow(core, color=color)
            segment = VGroup(halo, core)
            halos.append(halo)
            segments.append(segment)
            if seg_f > 1:
                # lag_ratio=0, load-bearing: Create's default (1.0) hands each
                # of the five stacked copies of this same path (4 halo layers +
                # core) its own disjoint slice of the run time, so the line
                # visibly redraws itself five times — the Body rejected exactly
                # that at the dark-draft watch (2026-08-17, Q19). Zero grows
                # them together: one pass, the light arriving with the line.
                scene.play(Create(segment, lag_ratio=0.0),
                           run_time=run_time(seg_f))
            else:
                # A one-frame Create asks for half a frame of run_time, which
                # trips Manim's validate_run_time warning and gets clamped. The
                # segment is added outright and the frame held instead: same
                # frame written, same bytes, no warning. seg_f == 0 just adds.
                scene.add(segment)
                if seg_f == 1:
                    scene.wait(hold_time(1), frozen_frame=True)
        elif seg_f > 0:
            # Zero-length segment with frames budgeted to it (two marks at the
            # same `at`): hold rather than silently give the frames away.
            scene.wait(hold_time(seg_f), frozen_frame=True)
        if i < len(marks):
            spec = marks[i]
            mark = _mark(x1, y, spec.get("label"), color)
            scene.play(FadeIn(mark, shift=DOWN * theme.MARK_GAP),
                       run_time=run_time(pop_f))
            built.append(mark)
            if spec.get("persistent"):
                persistent.append(mark)

    assembly = VGroup(*segments, *extras, *built)
    if assembly.width > max_w + 1e-6:
        # Caught after drawing rather than never: a long mark label at at=1.0 is
        # only measurable once built, and contract rule 4 is not advisory.
        raise ValueError(
            f"thread: the drawn assembly is {assembly.width:.2f} units wide "
            f"against a {max_w:.2f}-unit safe column — a mark label is hanging "
            f"outside the frame's safe area. Shorten a label or move the mark in.")
    return Lifeline(VGroup(*segments, *extras), built, persistent, halos)


def file_card(label, width=None, height=None) -> VGroup:
    """A labelled, document-shaped card — the usual fly_card target.

    Returned unplaced and unadded: position it with .move_to() and scene.add()
    it, then fly chips into it. The label sits BELOW the card so an arriving
    chip never lands on top of it.

    On the dark theme the card is a lit object: a rim of amber light around a
    lifted surface. For a labelled card, `card[0]` is the lit group (body +
    corner + halo) — its centre coincides with the document body's, since the
    halo is centre-symmetric, so aligning by `card[0]` IS aligning by the body.
    """
    w = float(width or theme.CARD_W)
    h = float(height or theme.CARD_H)
    fold = min(theme.CARD_FOLD, w * 0.5, h * 0.5)
    body = Polygon(
        [-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - fold, 0],
        [w / 2 - fold, h / 2, 0], [-w / 2, h / 2, 0],
        stroke_color=theme.GLOW, stroke_width=1.6,
        fill_color=theme.CARD_FILL, fill_opacity=theme.CARD_FILL_OPACITY)
    # The fold shows the ground through the corner, so the card reads as a sheet
    # with a turned corner rather than as a pentagon.
    corner = Polygon(
        [w / 2 - fold, h / 2, 0], [w / 2, h / 2 - fold, 0],
        [w / 2 - fold, h / 2 - fold, 0],
        stroke_color=theme.GLOW, stroke_width=1.2,
        fill_color=theme.GROUND, fill_opacity=1.0)
    card = VGroup(body, corner, glow(body))
    if label:
        caption = _mono(str(label), theme.SIZE_CARD, theme.MUTED)
        caption.next_to(card, DOWN, buff=theme.MARK_GAP * 1.5)
        card = VGroup(card, caption)
    return card


def chip(label, color=None) -> VGroup:
    """The small labelled card fly_card throws. Exposed so a builder can park
    one on screen before deciding where it goes."""
    # The chip is the brightest thing in the theme — a solid amber plate, so its
    # label is set in the GROUND colour. Cream on amber would be two lights
    # cancelling; dark on amber reads as something stamped and carried.
    text = _serif(str(label), theme.SIZE_CHIP, theme.GROUND)
    plate = RoundedRectangle(
        width=text.width + theme.CHIP_PAD * 2,
        height=text.height + theme.CHIP_PAD * 2,
        corner_radius=0.08,
        fill_color=color or theme.GLOW, fill_opacity=1.0,
        stroke_color=theme.GLOW_HOT, stroke_width=1.2)
    plate.move_to(text.get_center())
    return VGroup(glow(plate, color=color or theme.GLOW), plate, text)


def fly_card(scene, label, source, target, duration, color=None) -> VGroup:
    """Fly a small labelled chip from `source` into `target`, landing with weight.

    The "this went into the record" gesture: `target` is usually a file_card().
    `source` and `target` may each be a mobject or a raw [x, y, z] point. The
    chip overshoots by CARD_LAND_SCALE and relaxes out of it, which reads as
    mass rather than as a slide.

    Returns the chip (left on screen). Consumes exactly frames_for(duration).
    """
    # Both halves floored at two frames: a one-frame play asks for half a frame
    # of run_time, which Manim's validate_run_time warns about and clamps.
    total_f = frames_for(duration)
    settle_f = min(frames_for(theme.CARD_SETTLE), max(total_f // 3, 2))
    fly_f = total_f - settle_f
    if fly_f < 2:
        raise ValueError(
            f"fly_card: {duration}s ({total_f} frames) leaves no room to fly "
            f"after CARD_SETTLE ({theme.CARD_SETTLE}s = {settle_f} frames)")

    card = chip(label, color)
    card.move_to(_point(source))
    scene.add(card)
    scene.play(card.animate.move_to(_point(target)).scale(theme.CARD_LAND_SCALE),
               run_time=run_time(fly_f))
    scene.play(card.animate.scale(1.0 / theme.CARD_LAND_SCALE),
               run_time=run_time(settle_f))
    return card


def kinetic_frames(groups) -> int:
    """Frames kinetic_line needs for `groups` at WORD_RATE — its floor duration.

    Floored at TWO frames per group: a group still needs frames to exist in,
    WORD_RATE x 0 would silently vanish, and a single frame would ask play() for
    half a frame of run_time — below Manim's validate_run_time floor.
    """
    return sum(max(frames_for(timing.WORD_RATE * len(str(g).split())), 2)
               for g in groups)


_BASELINE_PROBE = "Ag"


def _baseline_lift(text, size, weight) -> float:
    """How far `text`'s bbox centre sits from the probe's when both share one
    baseline. arrange() aligns bbox CENTRES, and glyph boxes differ per group
    (descenders, caps, periods), so centre-aligned word-groups land on visibly
    different baselines — the within-sentence jitter the Body rejected at the
    dark-draft watch (2026-08-17, Q19). Measured off a throwaway render of
    "<text> Ag" (the probe pair spans full ascender + descender; spaces carry
    no glyphs, so the probe is always the trailing two), never guessed from
    font metrics.
    """
    probe = _serif(f"{text} {_BASELINE_PROBE}", size, theme.INK, weight)
    glyphs = list(probe.submobjects)
    body = glyphs[:-len(_BASELINE_PROBE)]
    anchor = glyphs[-len(_BASELINE_PROBE):]
    if not body:
        return 0.0
    return VGroup(*body).get_center()[1] - VGroup(*anchor).get_center()[1]


def kinetic_line(scene, groups, duration=None, y=0.0, size=None, color=None,
                 weight=BOLD, accents=()) -> VGroup:
    """Land one line of prose, word-group by word-group, with weight.

    The motion-forward alternative to a static `title` scene: instead of the
    whole sentence appearing at once, each group drops in and settles, so the
    eye is led along the line rather than dropped into the middle of it.

        groups    the line, pre-split into the units that land together, e.g.
                  ["Your session", "is about to", "forget something."]
        duration  optional total. Each group is held for WORD_RATE x its own
                  word count regardless — the line can never outrun reading —
                  so `duration` may only ADD a trailing hold, never compress.
        accents   substrings set in the theme's light (GLOW, and bold where the
                  line is not already) wherever they occur inside a group — the
                  per-beat key term (Q20). An accent must live inside ONE
                  group; matching never spans the gaps between them.

    Returns the assembled line. Consumes exactly frames_for(duration), or
    kinetic_frames(groups) when `duration` is None.
    """
    groups = [str(g) for g in groups]
    if not groups:
        raise ValueError("kinetic_line: needs at least one word group")
    size = size or theme.SIZE_KINETIC
    parts = []
    for g in groups:
        marks = [a for a in accents if str(a) in g]
        parts.append(_serif(g, size, color or theme.INK, weight,
                            t2c={a: theme.GLOW for a in marks} or None,
                            t2w={a: BOLD for a in marks} or None))
    line = VGroup(*parts).arrange(RIGHT, buff=theme.WORD_GAP)
    for part, g in zip(parts, groups):
        part.shift(UP * _baseline_lift(g, size, weight))
    fit_safe(line)
    if y:
        line.shift(UP * y)

    per_f = [max(frames_for(timing.WORD_RATE * len(g.split())), 2) for g in groups]
    need_f = sum(per_f)
    total_f = frames_for(duration) if duration is not None else need_f
    if total_f < need_f:
        raise ValueError(
            f"kinetic_line: {duration}s ({total_f} frames) is under the "
            f"WORD_RATE minimum for these groups ({need_f} frames) — this "
            f"primitive will not read faster than timing.WORD_RATE")

    for part, frames in zip(parts, per_f):
        scene.play(FadeIn(part, shift=DOWN * theme.KINETIC_DROP),
                   run_time=run_time(frames))
    rest = total_f - need_f
    if rest:
        scene.wait(hold_time(rest), frozen_frame=True)
    return line


BUILDERS = {
    "title": build_title,
    "bullets": build_bullets,
    "code": build_code,
    "terminal": build_terminal,
    "diagram": build_diagram,
    "outro": build_outro,
}


def build(scene, ctx) -> SceneBuild:
    stype = scene["type"]
    if stype not in BUILDERS:
        # `custom` is the only type that gets here: render.py drives it directly
        # because its builder owns the scene clock, not a static group.
        raise KeyError(f"scene type {stype!r} has no declarative builder — "
                       f"render.py must handle it")
    return BUILDERS[stype](scene, ctx)
