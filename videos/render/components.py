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

Four rules, each of which the renderer or the linter enforces:

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
    Code, Create, FadeIn, FadeOut, Line, Paragraph, Polygon, Rectangle,
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


def _serif(text, size, color, weight=None):
    return Text(text, font=theme.SERIF, font_size=size, color=color,
                weight=weight or "NORMAL")


def _mono(text, size, color):
    return Text(text, font=theme.MONO, font_size=size, color=color)


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
        dash = _serif("—", theme.SIZE_BULLET, theme.AMBER)
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
        fill_color=theme.WHITE, fill_opacity=1.0,
        stroke_color=theme.MUTED, stroke_width=1.2,
    ).move_to(code.get_center())
    members = [panel]
    for n in scene.get("highlight") or []:
        pitch = _line_pitch(code.code_lines)
        band = Rectangle(
            width=code.width * 0.97, height=pitch,
            fill_color=theme.AMBER_FILL, fill_opacity=0.55,
            stroke_color=theme.AMBER, stroke_width=1.0,
        )
        # One band per line rather than one around the set: highlights need not
        # be contiguous, and adjacent bands meet at the line pitch anyway.
        band.move_to([code.get_center()[0], _line_y(code.code_lines, n - 1), 0])
        members.append(band)  # behind the glyphs
    members.append(code)
    return SceneBuild(fit_safe(VGroup(*members)))


def build_terminal(scene, ctx):
    text = (ctx["sb_dir"] / scene["capture"]).read_text(encoding="utf-8")
    lines = lint.visible_lines(text)
    body = Paragraph(*[ln if ln.strip() else " " for ln in lines],
                     font=theme.MONO, font_size=theme.SIZE_TERMINAL,
                     color=theme.TERMINAL_FG, alignment="left", line_spacing=0.6)
    panel = RoundedRectangle(
        width=body.width + theme.PANEL_PAD * 2,
        height=body.height + theme.PANEL_PAD * 2,
        corner_radius=0.12,
        fill_color=theme.TERMINAL_BG, fill_opacity=1.0,
        stroke_color=theme.NAVY_DARK, stroke_width=1.5,
    )
    panel.move_to(body.get_center())
    group = VGroup(panel, body)
    fit_safe(group)

    if scene.get("reveal", "block") == "line":
        drawn = [ln for ln in body.submobjects if _has_glyphs(ln)]
        blanks = [ln for ln in body.submobjects if not _has_glyphs(ln)]
        return SceneBuild(VGroup(panel, *blanks), reveals=drawn)
    return SceneBuild(group)


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

    def __init__(self, line, marks, persistent):
        self.line = line              # VGroup of the drawn segments
        self.marks = VGroup(*marks)   # every mark, persistent or not
        self.persistent = VGroup(*persistent)
        self.group = VGroup(self.line, self.marks)
        # Identity, not equality: two marks with the same label are two marks.
        self._doomed = [m for m in marks if not any(m is p for p in persistent)]

    def end(self, scene, duration) -> int:
        """Stop the thread: the line and its non-persistent marks fade out.

        Marks flagged `persistent` stay on screen — that is how a beat carries
        one artefact across into the next thread. Returns frames consumed.
        """
        frames = frames_for(duration)
        scene.play(*[FadeOut(m) for m in [self.line, *self._doomed]],
                   run_time=run_time(frames))
        return frames


def _mark(x: float, y: float, label, color) -> VGroup:
    tick = Line([x, y - theme.THREAD_TICK, 0], [x, y + theme.THREAD_TICK, 0],
                stroke_width=theme.THREAD_STROKE, color=color)
    parts = [tick]
    if label:
        caption = _serif(str(label), theme.SIZE_MARK, theme.MUTED)
        caption.next_to(tick, UP, buff=theme.MARK_GAP)
        parts.append(caption)
    return VGroup(*parts)


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
    color = color or theme.INK
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

    segments, built, persistent = [], [], []
    for i in range(len(fractions) - 1):
        x0 = left + fractions[i] * width
        x1 = left + fractions[i + 1] * width
        seg_f = stops[i + 1] - stops[i]
        if abs(x1 - x0) > 1e-9:
            segment = Line([x0, y, 0], [x1, y, 0],
                           stroke_width=theme.THREAD_STROKE, color=color)
            segments.append(segment)
            if seg_f > 1:
                scene.play(Create(segment), run_time=run_time(seg_f))
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
    return Lifeline(VGroup(*segments, *extras), built, persistent)


def file_card(label, width=None, height=None) -> VGroup:
    """A labelled, document-shaped card — the usual fly_card target.

    Returned unplaced and unadded: position it with .move_to() and scene.add()
    it, then fly chips into it. The label sits BELOW the card so an arriving
    chip never lands on top of it.
    """
    w = float(width or theme.CARD_W)
    h = float(height or theme.CARD_H)
    fold = min(theme.CARD_FOLD, w * 0.5, h * 0.5)
    body = Polygon(
        [-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2 - fold, 0],
        [w / 2 - fold, h / 2, 0], [-w / 2, h / 2, 0],
        stroke_color=theme.INK, stroke_width=1.6,
        fill_color=theme.WHITE, fill_opacity=1.0)
    corner = Polygon(
        [w / 2 - fold, h / 2, 0], [w / 2, h / 2 - fold, 0],
        [w / 2 - fold, h / 2 - fold, 0],
        stroke_color=theme.INK, stroke_width=1.2,
        fill_color=theme.PAPER, fill_opacity=1.0)
    card = VGroup(body, corner)
    if label:
        caption = _mono(str(label), theme.SIZE_CARD, theme.MUTED)
        caption.next_to(card, DOWN, buff=theme.MARK_GAP * 1.5)
        card = VGroup(card, caption)
    return card


def chip(label, color=None) -> VGroup:
    """The small labelled card fly_card throws. Exposed so a builder can park
    one on screen before deciding where it goes."""
    text = _serif(str(label), theme.SIZE_CHIP, theme.INK)
    plate = RoundedRectangle(
        width=text.width + theme.CHIP_PAD * 2,
        height=text.height + theme.CHIP_PAD * 2,
        corner_radius=0.08,
        fill_color=color or theme.AMBER_FILL, fill_opacity=1.0,
        stroke_color=theme.AMBER, stroke_width=1.2)
    plate.move_to(text.get_center())
    return VGroup(plate, text)


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


def kinetic_line(scene, groups, duration=None, y=0.0, size=None, color=None,
                 weight=BOLD) -> VGroup:
    """Land one line of prose, word-group by word-group, with weight.

    The motion-forward alternative to a static `title` scene: instead of the
    whole sentence appearing at once, each group drops in and settles, so the
    eye is led along the line rather than dropped into the middle of it.

        groups    the line, pre-split into the units that land together, e.g.
                  ["Your session", "is about to", "forget something."]
        duration  optional total. Each group is held for WORD_RATE x its own
                  word count regardless — the line can never outrun reading —
                  so `duration` may only ADD a trailing hold, never compress.

    Returns the assembled line. Consumes exactly frames_for(duration), or
    kinetic_frames(groups) when `duration` is None.
    """
    groups = [str(g) for g in groups]
    if not groups:
        raise ValueError("kinetic_line: needs at least one word group")
    parts = [_serif(g, size or theme.SIZE_KINETIC, color or theme.INK, weight)
             for g in groups]
    line = VGroup(*parts).arrange(RIGHT, buff=theme.WORD_GAP)
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
