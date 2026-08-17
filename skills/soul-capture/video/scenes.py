"""Motion for the soul-capture pilot, v2 — the three `custom` beats of script.md.

The video's argument (v2.4, the Body's restructure spec, 2026-08-17 / Q22):
a session is ABOUT to die with what it learned (beat 2, imminent tense), the
capture syntax and its three stores are shown as one pinned surface (beat 3's
intro), each tag then runs the SAME short pattern — light the store, show a
real example, send it home — and the close is the contrast: the stores
survive, everything else evaporates. The rail of store cards is pinned for the
whole sequence — never animated out and back — which is why the syntax, the
three tag beats, and the close are ONE scene: a scene boundary would clear it.

One file, per the custom-scene contract in videos/render/components.py: the
shared gestures (thread / chip / file_card / kinetic_line) come from
`components`, every colour and size from `theme`, and nothing is imported from
beside this file. Every on-screen string is declared in storyboard.yaml's
`text:`. The three examples are REAL record entries (SOUL-I056 / SOUL-176 /
SOUL-F038), abbreviated but not invented — the contract's "never fabricate"
applies to demos above all.

Each builder spends its slot in whole FRAMES and closes the arithmetic with a
trailing frozen wait (contract rule 1) — the frame counts below are the shot
list, and _spend() is what refuses to overrun.
"""

import numpy as np

import theme  # must precede manim: sets FONTCONFIG_FILE before Pango starts

from manim import BOLD, DOWN, LEFT, UP, FadeIn, FadeOut, VGroup

CARD_H = 1.60          # a rail store card's body, before RAIL_K
CARD_PAD = 0.50        # card width = the widest example chip's width + this
CARD_MARGIN = 0.06     # between the rail and the safe column's right edge

# The capture sequence's fixed geography. The rail is a right-hand column of
# the three store cards, pinned from its FadeIn to the final self-fade; the
# left column holds the syntax heading and the three tag lines; examples enter
# bottom-left and travel right into their store.
RAIL_K = 0.60          # scale a store card (and a landing chip) docks at
RAIL_PITCH = 1.70      # vertical distance between rail rows
RAIL_DIM = 0.28        # opacity multiplier for inactive rows (multiplicative:
                       # each member keeps its own build-time opacity ratio)
HEAD_Y = 2.45          # syntax heading centre line
LINE_YS = (1.55, 0.85, 0.15)   # the three tag lines
EX_Y = -2.05           # example block's centre — chip above, description below,
                       # so the block grows DOWN, never right toward the rail
ROW_Y = -1.10          # the close's horizontal row, by card body centre
ROW_PITCH = 1.70       # spacing between the row's card centres

# (tag, description, store, real record id, example — abbreviated, not invented)
ENTRIES = [
    ("idea", "a thought worth coming back to", "ideas.md",
     "SOUL-I056", "graduate the theme tokens into the brand"),
    ("witness", "what just happened, on the record", "witness.md",
     "SOUL-176", "every gate green — still rejected at the watch"),
    ("finding", "a lesson that proved itself", "findings/",
     "SOUL-F038", "cross-project imports silently fail"),
]


def _overlay(comp, text, accent=None):
    """A beat's closing line: centred, with its key term in the theme's light.

    SIZE_KINETIC rather than a third heading size: every full-line statement in
    the video sits at one optical size, or the lines read as differently
    aligned even when they are not (Q19).
    """
    return comp.fit_safe(
        comp.serif(text, theme.SIZE_KINETIC, theme.INK, BOLD,
                   t2c={accent: theme.GLOW} if accent else None))


def _spend(scene, comp, frames, where):
    """Hold whatever is left of the slot, and refuse to have overrun it."""
    if frames < 0:
        raise ValueError(
            f"{where}: the shot list overran its slot by {-frames} frame(s) "
            f"({-frames / theme.FPS:.3f}s) — shorten a gesture, do not lengthen "
            f"the storyboard's duration past the runtime budget")
    if frames:
        scene.wait(comp.hold_time(frames), frozen_frame=True)


def _remember(mobj):
    """Stash build-time opacities so dimming is multiplicative, never flat.

    A glow halo's layers carry four DIFFERENT stroke opacities; a uniform
    set_opacity(0.3) would flatten them and the halo would read brighter than
    its core. Remembering each family member's own values keeps every ratio
    intact at any dim level.
    """
    for m in mobj.family_members_with_points():
        m._base_stroke = m.get_stroke_opacity()
        m._base_fill = m.get_fill_opacity()
    return mobj


def _level(mobj, level):
    """Animations taking `mobj` to level x its remembered opacities."""
    return [m.animate.set_stroke(opacity=m._base_stroke * level)
                     .set_fill(opacity=m._base_fill * level)
            for m in mobj.family_members_with_points()]


def hook(scene, th, comp, duration):
    """Beat 1 — the line lands word-group by word-group, then the skill name."""
    total_f = comp.frames_for(duration)
    sub_f = comp.frames_for(0.4)

    groups = ["Your session", "is about to", "forget something."]
    line = comp.kinetic_line(scene, groups, y=0.5, accents=("forget",))
    used = comp.kinetic_frames(groups)

    sub = comp.serif("soul-capture", th.SIZE_SUB, th.MUTED)
    sub.next_to(line, DOWN, buff=th.LINE_GAP * 1.8)
    scene.play(FadeIn(sub), run_time=comp.run_time(sub_f))
    used += sub_f

    _spend(scene, comp, total_f - used, "hook")


def mortality(scene, th, comp, duration):
    """Beat 2 — a session draws, collects three unguessables, and is ABOUT to die.

    v2.4 reframe (Body's spec, point 1): the line lands while the thread is
    still lit — imminent, not retrospective — and THEN the light goes out
    under it. The warning precedes the death it warns about; the line hangs
    over the empty frame afterwards as the hook for the capture sequence.
    """
    total_f = comp.frames_for(duration)
    draw_s, fade_s = 4.0, 1.3
    pause_f, land_f, read_f = 10, 15, 24

    life = comp.thread(scene, draw_s, y=0.0, marks=[
        {"at": 0.22, "label": "a decision"},
        {"at": 0.50, "label": "an incident"},
        {"at": 0.78, "label": "a convention"},
    ])
    used = comp.frames_for(draw_s)

    scene.wait(comp.hold_time(pause_f), frozen_frame=True)
    used += pause_f

    line = _overlay(comp, "This session is about to end — these die with it.",
                    accent="die")
    line.shift(UP * 1.5)   # over the still-living thread, not on it
    scene.play(FadeIn(line), run_time=comp.run_time(land_f))
    used += land_f
    scene.wait(comp.hold_time(read_f), frozen_frame=True)
    used += read_f

    used += life.end(scene, fade_s)

    _spend(scene, comp, total_f - used, "mortality")   # the warning, made good


def capture(scene, th, comp, duration):
    """Beat 3 — syntax, the pinned rail, three identical tag beats, the close.

    Shot list, in frames (30fps), summing to the slot:
      15 heading · 15 tag lines · 15 rail · 12 beat ·
      3 x (12 activate · 12 example in · 100 read · 30 example travels home ·
           12 dim back + clear centre) ·
      12 rail relights · 18 the teaching surface evaporates · 15 closing line ·
      12 sub · 24 the survivors step into a row · 78 stillness ·
      18 self-fade · rest a breath of dark
    """
    total_f = comp.frames_for(duration)
    used = 0
    max_w, max_h = comp.safe_size()
    left = -max_w / 2.0

    # --- the pinned surface -------------------------------------------------
    heading = comp.mono("/soul-capture <tag>", th.SIZE_SUB, th.INK,
                        t2c={"<tag>": th.GLOW})
    heading.move_to(np.array([left + heading.width / 2.0, HEAD_Y, 0.0]))

    lines = []
    for (token, desc, _s, _i, _e), row_y in zip(ENTRIES, LINE_YS):
        line = comp.serif(f"{token} — {desc}", th.SIZE_BULLET * 0.88, th.INK,
                          t2c={token: th.GLOW}, t2w={token: BOLD})
        line.move_to(np.array([left + line.width / 2.0, row_y, 0.0]))
        lines.append(_remember(line))

    body_w = max(comp.chip(e[3]).width for e in ENTRIES) + CARD_PAD
    rail_x = max_w / 2.0 - body_w * RAIL_K / 2.0 - CARD_MARGIN
    cards = []
    for (_t, _d, store, _i, _e), row_y in zip(ENTRIES,
                                              (RAIL_PITCH, 0.0, -RAIL_PITCH)):
        card = comp.file_card(store, width=body_w, height=CARD_H).scale(RAIL_K)
        card.shift(np.array([rail_x - card[0].get_center()[0],
                             row_y - card[0].get_center()[1], 0.0]))
        cards.append(_remember(card))

    scene.play(FadeIn(heading), run_time=comp.run_time(15))
    scene.play(*[FadeIn(l) for l in lines], run_time=comp.run_time(15))
    scene.play(*[FadeIn(c) for c in cards], run_time=comp.run_time(15))
    scene.wait(comp.hold_time(12), frozen_frame=True)
    used += 57

    # --- three tag beats, identical by construction -------------------------
    stamped = [[], [], []]   # chips that have landed, dimmed with their card
    for i, (token, desc, store, ex_id, ex_text) in enumerate(ENTRIES):
        anims = _level(lines[i], 1.0) + _level(cards[i], 1.0)
        for j in range(3):
            if j != i:
                anims += _level(lines[j], RAIL_DIM) + _level(cards[j], RAIL_DIM)
                for old in stamped[j]:
                    anims += _level(old, RAIL_DIM)
        scene.play(*anims, run_time=comp.run_time(12))
        used += 12

        stamp = comp.chip(ex_id)
        caption = comp.serif(ex_text, th.SIZE_SUB * 0.85, th.MUTED)
        # Stacked, not side-by-side: the description sits BELOW its chip so the
        # example block grows down and never crowds the rail (Body's draft4
        # note; descriptions are capped at two lines by authoring).
        example = VGroup(stamp, caption).arrange(DOWN, buff=0.22,
                                                 aligned_edge=LEFT)
        example.move_to(np.array([left + example.width / 2.0, EX_Y, 0.0]))
        scene.play(FadeIn(example, shift=UP * 0.2), run_time=comp.run_time(12))
        used += 12
        scene.wait(comp.hold_time(100), frozen_frame=True)
        used += 100

        # The travel home: the stamp shrinks into its store at rail scale, so
        # every beat's landing is geometrically the same gesture.
        scene.play(stamp.animate
                   .move_to(cards[i][0].get_center()).scale(RAIL_K),
                   run_time=comp.run_time(30))
        used += 30
        stamped[i].append(_remember(stamp))

        scene.play(FadeOut(caption),
                   *_level(lines[i], RAIL_DIM), *_level(cards[i], RAIL_DIM),
                   *_level(stamp, RAIL_DIM),
                   run_time=comp.run_time(12))
        used += 12

    # --- the close: what survives, and what does not ------------------------
    relight = []
    for i in range(3):
        relight += _level(cards[i], 1.0)
        for old in stamped[i]:
            relight += _level(old, 1.0)
    scene.play(*relight, run_time=comp.run_time(12))
    used += 12

    scene.play(FadeOut(heading), *[FadeOut(l) for l in lines],
               run_time=comp.run_time(18))
    used += 18

    closing = _overlay(comp, "These survive the session.", accent="survive")
    closing.shift(UP * 1.2)
    scene.play(FadeIn(closing), run_time=comp.run_time(15))
    used += 15
    sub = comp.serif("Everything else is gone.", th.SIZE_SUB, th.MUTED)
    sub.next_to(closing, DOWN, buff=th.LINE_GAP * 1.8)
    scene.play(FadeIn(sub), run_time=comp.run_time(12))
    used += 12

    # The survivors step forward: the rail re-forms as a horizontal row under
    # the claim, every stamp riding its card (Body's draft4 note).
    glide = []
    for i, x in enumerate((-ROW_PITCH, 0.0, ROW_PITCH)):
        delta = np.array([x - cards[i][0].get_center()[0],
                          ROW_Y - cards[i][0].get_center()[1], 0.0])
        glide.append(cards[i].animate.shift(delta))
        glide += [old.animate.shift(delta) for old in stamped[i]]
    scene.play(*glide, run_time=comp.run_time(24))
    used += 24

    scene.wait(comp.hold_time(78), frozen_frame=True)
    used += 78

    # The soft exit lives here, as the rule beat learned: the outro's fixed
    # 0.4s incoming fade alone reads abrupt. Tightened at the draft4 watch —
    # the full break to the outro read ~0.8s too long.
    remaining = [closing, sub, *cards]
    for group in stamped:
        remaining += group
    scene.play(*[FadeOut(m) for m in remaining], run_time=comp.run_time(18))
    used += 18

    _spend(scene, comp, total_f - used, "capture")   # a breath of dark
