#!/usr/bin/env python3
"""Stage 3 — storyboard.yaml -> mp4 + timings.json (+ chapters). No LLM here.

Same storyboard + captures + theme + pinned environment => byte-identical mp4.
That property is what makes the staleness manifest's hashes mean anything, so
nothing in this path may read the clock or a random source.

Usage: render.py <storyboard.yaml> [--out DIR] [--no-manifest]
"""

import argparse
import hashlib
import json
import random
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

import theme  # must precede manim: sets FONTCONFIG_FILE before Pango starts
import lint

from manim import FadeIn, FadeOut, Scene, tempconfig

import components


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def repo_key(path: Path) -> str:
    """Manifest keys are repo-relative; anything outside stays absolute."""
    try:
        return str(path.resolve().relative_to(theme.REPO_ROOT))
    except ValueError:
        return str(path.resolve())


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


class StoryboardScene(Scene):
    # Manim's Scene takes no arbitrary kwargs; the plan arrives as class state.
    plan = None
    ctx = None

    def construct(self):
        live = []
        for entry in self.plan["scenes"]:
            build = components.build(entry["scene"], self.ctx)
            if len(build.reveals) != entry["n_reveals"]:
                raise SystemExit(
                    f"error: scene '{entry['id']}' built {len(build.reveals)} "
                    f"reveals but the plan budgeted {entry['n_reveals']} — the "
                    f"component and the linter disagree")
            if entry["transition_frames"]:
                anims = [FadeIn(build.group)] + [FadeOut(m) for m in live]
                self.play(*anims, run_time=run_time(entry["transition_frames"]))
            else:
                for m in live:
                    self.remove(m)
                self.add(build.group)

            used = 0
            for mobject in build.reveals:
                self.play(FadeIn(mobject), run_time=run_time(entry["reveal_frames"]))
                used += entry["reveal_frames"]
            rest = entry["hold_frames"] - used
            if rest < 0:
                raise SystemExit(f"error: scene '{entry['id']}' reveals ({used} "
                                 f"frames) exceed its hold ({entry['hold_frames']})")
            if rest > 0:
                # frozen_frame pinned rather than inferred: it selects which of
                # the two quantisers above applies, so it must not be guessed.
                self.wait(hold_time(rest), frozen_frame=True)
            live = [build.group] + list(build.reveals)


def _escape_ffmeta(value: str) -> str:
    # Backslash FIRST: escaping it last would re-escape the ones just inserted.
    value = value.replace("\\", "\\\\")
    for ch in "=;#\n":
        value = value.replace(ch, "\\" + ch)
    return value


def write_chapters(plan: dict, dest: Path) -> bool:
    """ffmetadata chapters at each `chapter:` boundary (overview format only)."""
    marks = [(e["start_frame"], e["chapter"]) for e in plan["scenes"] if e.get("chapter")]
    if not marks:
        return False
    lines = [";FFMETADATA1"]
    for i, (start, title) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else plan["frames"]
        lines += ["[CHAPTER]", "TIMEBASE=1/1000",
                  f"START={int(round(start * 1000 / theme.FPS))}",
                  f"END={int(round(end * 1000 / theme.FPS))}",
                  f"title={_escape_ffmeta(str(title))}"]
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


# x264's default threading splits the frame by core count and bakes that count
# into the bitstream, so the same storyboard hashes differently on a machine with
# a different CPU. Single-threaded encoding is the price of a portable hash.
X264_PARAMS = "threads=1:sliced-threads=0:lookahead-threads=1"
X264_PRESET = "medium"
X264_CRF = "18"


def encoder_info() -> dict:
    """Recorded per manifest entry so an environment mismatch is detectable."""
    version = subprocess.run(["ffmpeg", "-version"], check=True,
                             capture_output=True, text=True).stdout
    return {"ffmpeg": version.splitlines()[0].strip(),
            "x264_params": X264_PARAMS,
            "preset": X264_PRESET, "crf": X264_CRF}


def bitexact_encode(raw: Path, dest: Path, chapters: Path | None) -> None:
    """Final pass: pinned encoder settings, stable timestamps, no metadata.

    Quality ceiling: this is the SECOND lossy generation. Manim encodes its
    partial movie files at a hard-coded crf 23 (scene_file_writer.py, literal in
    av_options — manim 0.21 exposes no config knob for it) and stream-copies
    them into the intermediate, so crf 18 here preserves a crf-23 source rather
    than improving on it. Lowering this crf buys nothing without patching Manim.
    """
    cmd = ["ffmpeg", "-y", "-nostdin", "-loglevel", "error",
           "-fflags", "+bitexact", "-i", str(raw)]
    if chapters:
        cmd += ["-i", str(chapters)]
    cmd += ["-map", "0:v",
            "-c:v", "libx264", "-preset", X264_PRESET, "-crf", X264_CRF,
            "-x264-params", X264_PARAMS, "-pix_fmt", "yuv420p",
            "-fflags", "+bitexact", "-flags:v", "+bitexact",
            # :g, not bare -1 — bare -map_metadata -1 also blanks the per-chapter
            # titles, leaving nameless chapters in the overview cuts.
            "-map_metadata:g", "-1",
            "-map_chapters", "1" if chapters else "-1",
            "-movflags", "+faststart", "-f", "mp4", str(dest)]
    subprocess.run(cmd, check=True)


def render(plan: dict, sb_path: Path, out_dir: Path) -> dict:
    theme.verify_fonts()
    random.seed(0)
    np.random.seed(0)

    video_id = plan["video"]
    work = theme.CACHE_ROOT / "media" / video_id
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True, exist_ok=True)

    StoryboardScene.plan = plan
    StoryboardScene.ctx = {"sb_dir": sb_path.parent}
    with tempconfig({
        "pixel_width": theme.RESOLUTION[0],
        "pixel_height": theme.RESOLUTION[1],
        "frame_rate": theme.FPS,
        "background_color": theme.PAPER,
        "media_dir": str(work),
        "output_file": f"{video_id}-raw",
        "disable_caching": True,
        "write_to_movie": True,
        "save_last_frame": False,
        "renderer": "cairo",
        "verbosity": "WARNING",
        "progress_bar": "none",
        "log_to_file": False,
    }):
        scene = StoryboardScene(random_seed=0)
        scene.render()
        raw = Path(scene.renderer.file_writer.movie_file_path)

    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{video_id}-t{theme.THEME_VERSION}"
    chapters_file = work / "chapters.ffmeta"
    has_chapters = write_chapters(plan, chapters_file)
    mp4 = out_dir / f"{stem}.mp4"
    bitexact_encode(raw, mp4, chapters_file if has_chapters else None)

    timings = {
        "video": video_id,
        "theme_version": theme.THEME_VERSION,
        "fps": theme.FPS,
        "frames": plan["frames"],
        "duration": round(plan["duration"], 6),
        "scenes": {e["id"]: {"start": round(e["start"], 6),
                             "end": round(e["end"], 6)}
                   for e in plan["scenes"]},
    }
    (out_dir / f"{stem}.timings.json").write_text(
        json.dumps(timings, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return {"mp4": mp4, "timings": timings, "chapters": has_chapters}


def update_manifest(plan: dict, sb_path: Path, mp4: Path) -> Path:
    manifest_path = theme.REPO_ROOT / "videos" / "manifest.json"
    manifest = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    storyboard_key = repo_key(sb_path)
    claimed = manifest.get(plan["video"], {}).get("storyboard")
    if claimed and claimed != storyboard_key:
        raise SystemExit(
            f"error: video id '{plan['video']}' is already claimed by {claimed}; "
            f"{storyboard_key} would overwrite its manifest entry. Ids must be "
            f"unique across the manifest — rename one.")

    tracked = [sb_path] + [theme.REPO_ROOT / p for p in plan["inputs"]]
    for entry in plan["scenes"]:
        tracked += lint.referenced_files(entry["scene"], sb_path.parent)

    hashes = {}
    for path in tracked:
        path = Path(path)
        if not path.exists():
            raise SystemExit(f"error: declared input missing: {path}")
        hashes[repo_key(path)] = sha256_file(path)

    manifest[plan["video"]] = {
        "storyboard": storyboard_key,
        "theme_version": theme.THEME_VERSION,
        "encoder": encoder_info(),
        "hashes": dict(sorted(hashes.items())),
        "output": sha256_file(mp4),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest_path


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("storyboard", type=Path)
    ap.add_argument("--out", type=Path,
                    default=theme.REPO_ROOT / "videos" / "out")
    ap.add_argument("--no-manifest", action="store_true",
                    help="skip the staleness manifest (used by the smoke test)")
    args = ap.parse_args(argv)

    sb_path = args.storyboard.resolve()
    ok, plan, report = lint.lint(sb_path)
    print(report)
    if not ok:
        print("refusing to render: lint failed", file=sys.stderr)
        return 1

    result = render(plan, sb_path, args.out.resolve())
    print(f"wrote {result['mp4']}  ({plan['duration']:.2f}s"
          f"{', chaptered' if result['chapters'] else ''})")
    if not args.no_manifest:
        print(f"wrote {update_manifest(plan, sb_path, result['mp4'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
