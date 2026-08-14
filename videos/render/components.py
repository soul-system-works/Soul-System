"""One builder per scene type. Boring, legible, centre-safe.

Each builder returns a SceneBuild: `group` is everything on screen when the
scene's transition finishes, `reveals` are mobjects added one at a time during
the hold. Reveals are consumed out of the hold, so a builder can never change a
scene's duration — timing.py owns that.
"""

import theme  # must precede manim: sets FONTCONFIG_FILE before Pango starts

from manim import (
    BOLD, DOWN, LEFT, ORIGIN, RIGHT,
    Code, Paragraph, Rectangle, RoundedRectangle, SVGMobject, Text, VGroup, config,
)

import lint


class SceneBuild:
    def __init__(self, group, reveals=None):
        self.group = group
        self.reveals = reveals or []


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


BUILDERS = {
    "title": build_title,
    "bullets": build_bullets,
    "code": build_code,
    "terminal": build_terminal,
    "diagram": build_diagram,
    "outro": build_outro,
}


def build(scene, ctx) -> SceneBuild:
    return BUILDERS[scene["type"]](scene, ctx)
