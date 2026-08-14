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

THEME_VERSION = 1

RESOLUTION = (1920, 1080)
FPS = 30

# Palette — hex tokens lifted verbatim from architecture.svg.
PAPER           = "#fbf7ec"   # background
INK             = "#2c3e50"   # primary text / strokes
MUTED           = "#5d6d7e"   # secondary text, hairlines
NAVY            = "#2c4670"   # accent
NAVY_DARK       = "#1a2d4a"   # accent, dark variant
AMBER           = "#8a5a09"   # emphasis
AMBER_FILL      = "#f5d78e"   # emphasis fill
AMBER_HIGHLIGHT = "#fff8cc"   # emphasis fill, lightest
GREEN           = "#1e4528"
RED             = "#b7472a"
WHITE           = "#ffffff"

# Terminal scenes invert: a dark panel sitting on the paper frame.
TERMINAL_BG = "#161d26"
TERMINAL_FG = "#e6ecf2"
TERMINAL_DIM = "#8fa2b4"

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

PYGMENTS_STYLE = "friendly"   # light-background style; no LaTeX involved


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
