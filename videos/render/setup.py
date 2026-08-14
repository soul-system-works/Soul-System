#!/usr/bin/env python3
"""One-time setup: venv + pinned deps + pinned fonts. Run with system python3.

Fonts are fetched, never committed — the repo stays text-only and Georgia (which
Gelasio is metric-compatible with) is not redistributable anyway. Both the commit
and the sha256 are pinned: an upstream force-push cannot silently change a face
and therefore cannot silently change a rendered frame.

Everything heavy lands under ~/.cache/soul-video (ext4). The repo is on drvfs.
"""

import hashlib
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import theme  # noqa: E402

GELASIO_COMMIT = "2c0540285e823e996a5276223807e2175515daae"  # SorkinType/Gelasio
JBMONO_COMMIT = "cd5227bd1f61dff3bbd6c814ceaf7ffd95e947d9"   # JetBrainsMono v2.304

GELASIO = f"https://raw.githubusercontent.com/SorkinType/Gelasio/{GELASIO_COMMIT}/fonts/ttf"
JBMONO = f"https://raw.githubusercontent.com/JetBrains/JetBrainsMono/{JBMONO_COMMIT}/fonts/ttf"

FONTS = [
    (f"{GELASIO}/Gelasio-Regular.ttf", "Gelasio-Regular.ttf",
     "48c797fbe0e07c48a18cb962e7bdfa23f19618327dddf54093265328dc9eb39d"),
    (f"{GELASIO}/Gelasio-Bold.ttf", "Gelasio-Bold.ttf",
     "e0ef3addf1acf35f5c6aef2be00d0a2c01363bf70a5950e16650976051a0c462"),
    (f"{JBMONO}/JetBrainsMono-Regular.ttf", "JetBrainsMono-Regular.ttf",
     "a0bf60ef0f83c5ed4d7a75d45838548b1f6873372dfac88f71804491898d138f"),
    (f"{JBMONO}/JetBrainsMono-Bold.ttf", "JetBrainsMono-Bold.ttf",
     "5590990c82e097397517f275f430af4546e1c45cff408bde4255dad142479dcb"),
    (f"{JBMONO}/JetBrainsMono-Italic.ttf", "JetBrainsMono-Italic.ttf",
     "9d0a1f7a708e6af183f1193b7e81d40da294f5c67682c085d8401c60aac8ded4"),
    (f"{JBMONO}/JetBrainsMono-BoldItalic.ttf", "JetBrainsMono-BoldItalic.ttf",
     "4039d5ce0ed225bf9c8b2c8c6436290ae2f356b7e90d70fa666227238324aa3b"),
]

assert {name for _, name, _ in FONTS} == set(theme.REQUIRED_FONT_FILES), \
    "setup.py pins and theme.REQUIRED_FONT_FILES have drifted apart"

FONTS_CONF = """<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
  <!-- Deliberately NOT including the system config: the render must see exactly
       these two families, so a missing font fails loud instead of substituting. -->
  <dir>{font_dir}</dir>
  <cachedir>{cache_dir}</cachedir>
  <config></config>
</fontconfig>
"""

VENV = theme.CACHE_ROOT / "venv"
REQUIREMENTS = Path(__file__).resolve().parent / "requirements.txt"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch_fonts() -> None:
    theme.FONT_DIR.mkdir(parents=True, exist_ok=True)
    for url, name, digest in FONTS:
        dest = theme.FONT_DIR / name
        if dest.exists() and _sha256(dest) == digest:
            print(f"ok    {name}")
            continue
        print(f"fetch {name}")
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
        got = hashlib.sha256(data).hexdigest()
        if got != digest:
            raise SystemExit(f"error: {name} sha256 {got} != pinned {digest}")
        dest.write_bytes(data)


def write_fontconfig() -> None:
    cache_dir = theme.CACHE_ROOT / "fontcache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    theme.FONTCONFIG_PATH.write_text(
        FONTS_CONF.format(font_dir=theme.FONT_DIR, cache_dir=cache_dir),
        encoding="utf-8")
    print(f"wrote {theme.FONTCONFIG_PATH}")


def build_venv() -> Path:
    python = VENV / "bin" / "python"
    if not python.exists():
        print(f"creating venv at {VENV}")
        subprocess.run([sys.executable, "-m", "venv", str(VENV)], check=True)
        subprocess.run([str(python), "-m", "pip", "install", "-q",
                        "--upgrade", "pip"], check=True)
    subprocess.run([str(python), "-m", "pip", "install", "-q",
                    "-r", str(REQUIREMENTS)], check=True)
    return python


def verify(python: Path) -> None:
    subprocess.run(
        [str(python), "-c",
         "import sys; sys.path.insert(0, %r); "
         "import theme; theme.verify_fonts(); print('fonts ok')"
         % str(Path(__file__).resolve().parent)],
        check=True)


def main() -> int:
    fetch_fonts()
    write_fontconfig()
    python = build_venv()
    verify(python)
    print(f"\nrenderer python: {python}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
