"""Theme tokens — the visual identity, extracted from architecture.svg (Q9).

Bumping THEME_VERSION marks every video RENDER-STALE: the whole set re-renders
under the new look with zero re-authoring. Anything that changes what a frame
looks like belongs here, including animation speeds.

Importing this module sets FONTCONFIG_FILE. That must happen before manim (and
therefore Pango) is first imported, so every module that touches manim imports
theme FIRST — the ordering is load-bearing, not stylistic.
"""

import os
from pathlib import Path

THEME_VERSION = 2

RESOLUTION = (1920, 1080)
FPS = 30

# Palette, v2 — the LUMINOUS DARK theme (Q17). v1's roles are inverted: the
# ground is the navy lineage (#1a2d4a) taken down to night, and v1's paper
# (#fbf7ec) becomes the ink. Warm-dark throughout — there is no neutral gray and
# no pure black anywhere in here, because the ground has to read as depth rather
# than as an absence, and the amber light has to have something warm to sit in.
GROUND          = "#0f141d"   # background — the frame itself
GROUND_LIFT     = "#171f2b"   # a surface sitting ON the ground (panels, cards)
INK             = "#fbf7ec"   # primary text — v1's paper, inverted into the role
MUTED           = "#93a2b8"   # subs, captions, hairlines
NAVY            = "#2c4670"   # accent, unchanged: it reads as itself on dark
NAVY_DARK       = "#1a2d4a"   # the ground's parent; panel borders

# The light. Content is the light source in this theme (Q17), so the amber family
# stops being "emphasis fill" and becomes an emitter: GLOW is the core a filament
# or chip is drawn in, GLOW_HOT is its hottest centre, GLOW_DEEP the same light
# cooled — an ember tone, held in the palette; today only the smoke diagram
# asset samples it (no renderer code does).
GLOW            = "#f5d78e"
GLOW_HOT        = "#fff8cc"
GLOW_DEEP       = "#8a5a09"

# Re-derived for dark: v1's #1e4528 / #b7472a are near-invisible on the ground.
GREEN           = "#6fcf97"
RED             = "#ff8a6a"
WHITE           = "#ffffff"

# Glow treatment — layered copies behind a lit mobject, each wider and fainter.
# Pure geometry, no shaders and no image filters, so it stays byte-deterministic.
GLOW_LAYERS     = 4      # copies behind the core
GLOW_SPREAD     = 3.2    # stroke width added per layer outward
GLOW_OPACITY    = 0.22   # the innermost halo; each layer out gets half again
GLOW_DIE_FRAC   = 0.42   # of an `end()`, spent killing the glow before the line

# Terminal scenes no longer invert — everything is dark now. The panel earns its
# separation from the ground by VALUE (lifted) plus a lit rim, not by contrast.
TERMINAL_BG = "#141c28"
TERMINAL_FG = "#e8eef6"
TERMINAL_DIM = "#7f90a6"
PANEL_RIM = NAVY          # the faint border that detaches a panel from the ground
PANEL_RIM_WIDTH = 1.5

# Code scenes: the panel the syntax sits on, and the highlight band. On dark the
# v1 band (amber at 0.55) would swallow the glyphs, so the band is a translucent
# wash under a lit edge instead — the text is never painted over.
CODE_PANEL = GROUND_LIFT
HIGHLIGHT_FILL_OPACITY = 0.15
HIGHLIGHT_STROKE_OPACITY = 0.55

# file_card: a document that holds light rather than a white sheet.
CARD_FILL = GROUND_LIFT
CARD_FILL_OPACITY = 1.0

# Fonts are fetched, never committed (see setup.py). Georgia itself is a Windows
# font and cannot be redistributed; Gelasio is its OFL metric-compatible twin.
SERIF = "Gelasio"
MONO = "JetBrains Mono"

# Every face the theme can ask Pango for. Italic is here because the Pygments
# style italicises code comments: without the real face Pango synthesises an
# oblique, which is exactly the silent fallback this pipeline refuses.
REQUIRED_FONT_FILES = (
    "Gelasio-Regular.ttf",
    "Gelasio-Bold.ttf",
    "JetBrainsMono-Regular.ttf",
    "JetBrainsMono-Bold.ttf",
    "JetBrainsMono-Italic.ttf",
    "JetBrainsMono-BoldItalic.ttf",
)

REPO_ROOT = Path(__file__).resolve().parents[2]
FONT_DIR = REPO_ROOT / "videos" / ".fonts"
FONTCONFIG_PATH = FONT_DIR / "fonts.conf"

# Heavy IO stays off /mnt/d (drvfs); see mind.md 5b.
CACHE_ROOT = Path.home() / ".cache" / "soul-video"

# Type scale. Manim font_size is relative to a frame 8 units tall; components
# scale-to-fit inside the safe column afterwards, so these are starting sizes.
SIZE_HEADING  = 52
SIZE_SUB      = 32
SIZE_BULLET   = 34
SIZE_CODE     = 22
SIZE_TERMINAL = 22
SIZE_OUTRO    = 46
SIZE_URL      = 26
SIZE_KINETIC  = 46     # a kinetic_line word-group
SIZE_MARK     = 24     # a thread mark's label
SIZE_CARD     = 26     # a file_card's label
SIZE_CHIP     = 22     # a fly_card chip's label

# Layout — everything lives inside a centred column so a later 9:16 cut is a
# re-layout, not a re-author (Q6).
SAFE_W_FRAC = 0.72
SAFE_H_FRAC = 0.76
LINE_GAP = 0.34        # units between stacked prose lines
BULLET_GAP = 0.52
PANEL_PAD = 0.32       # terminal panel padding around its text

# Animation speeds. Reveals are consumed OUT of a scene's hold, never added to
# it, so total runtime stays exactly sum(transition + hold).
REVEAL_STEP = 0.25     # s per sequentially revealed bullet / terminal line

# Motion primitives, used by `custom` scenes (components.thread / fly_card /
# kinetic_line). Geometry is in Manim units on a frame 8 units tall; every one of
# these is a look, so they live here and not in timing.py — timing.py owns how
# long a VIEWER needs, these own how long a GESTURE takes.
THREAD_STROKE   = 3.0    # thread line and mark-tick stroke width
THREAD_TICK     = 0.16   # half-length of a mark tick across the thread
MARK_GAP        = 0.14   # between a mark tick and its label
MARK_POP        = 0.20   # s — one mark landing on the thread
CARD_W          = 1.50   # file_card body
CARD_H          = 1.90
CARD_FOLD       = 0.38   # the folded document corner
CHIP_PAD        = 0.18   # fly_card chip padding around its label
CARD_LAND_SCALE = 1.06   # overshoot a landing chip relaxes out of
CARD_SETTLE     = 0.18   # s — that relaxation
WORD_GAP        = 0.22   # between kinetic_line word-groups
KINETIC_DROP    = 0.35   # distance a landing word-group falls through

# Dark-background style, chosen for the theme rather than for taste: lightbulb's
# ground (#1d2331) is the same navy family as GROUND, its text (#d4d2c8) is a
# warm cream next to INK, its keywords (#FFAD66) are the amber the whole theme is
# lit by, and its comments (#7e8aa1) land on MUTED. No LaTeX involved.
PYGMENTS_STYLE = "lightbulb"


def configure_fontconfig() -> None:
    """Point Pango at videos/.fonts only. Idempotent."""
    os.environ["FONTCONFIG_FILE"] = str(FONTCONFIG_PATH)
    os.environ.setdefault("FONTCONFIG_PATH", str(FONT_DIR))


configure_fontconfig()


def verify_fonts() -> None:
    """Fail loud rather than silently falling back to a default face."""
    if not FONTCONFIG_PATH.exists():
        raise SystemExit(
            f"error: no fontconfig at {FONTCONFIG_PATH}\n"
            f"       run: python3 videos/render/setup.py"
        )
    absent = [f for f in REQUIRED_FONT_FILES if not (FONT_DIR / f).exists()]
    if absent:
        raise SystemExit(
            f"error: missing font face(s) in {FONT_DIR}: {', '.join(absent)}\n"
            f"       Pango would synthesise these rather than fail.\n"
            f"       run: python3 videos/render/setup.py"
        )
    import manimpango

    available = set(manimpango.list_fonts())
    missing = [f for f in (SERIF, MONO) if f not in available]
    if missing:
        raise SystemExit(
            "error: fonts not resolvable through "
            f"{FONTCONFIG_PATH}: {', '.join(missing)}\n"
            f"       visible families: {', '.join(sorted(available))}\n"
            f"       run: python3 videos/render/setup.py"
        )
