#!/usr/bin/env python3
"""Stage 3 — storyboard.yaml -> mp4 + timings.json (+ chapters). No LLM here.

Same storyboard + captures + theme + pinned environment => byte-identical mp4.
That property is what makes the staleness manifest's hashes mean anything, so
nothing in this path may read the clock or a random source.

Usage: render.py <storyboard.yaml> [--out DIR] [--no-manifest]
"""

import argparse
import hashlib
import importlib.util
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


# The frame quantisers live in components.py: custom-scene builders need the
# same two functions, and two copies of this arithmetic would drift.
run_time = components.run_time
hold_time = components.hold_time

# Keyed by resolved path so a video whose scenes share one module imports it
# once — a module with import-time side effects must not run twice per render.
_BUILDER_MODULES: dict[Path, object] = {}


def load_builder(scene: dict, sb_dir: Path):
    """Import a `custom` scene's module from its file and fetch its builder.

    Direct importlib from the path, deliberately: the storyboard's directory is
    not a package and must not become one — a video's motion module is a source
    file next to the storyboard it belongs to, not an installable. lint has
    already proved the path exists and stays inside the repo.
    """
    path = (sb_dir / scene["module"]).resolve()
    module = _BUILDER_MODULES.get(path)
    if module is None:
        # A path-derived module name: two videos may both ship a `motion.py`,
        # and colliding on sys.modules would silently render the wrong one.
        name = "soul_video_custom_" + hashlib.sha256(
            str(path).encode("utf-8")).hexdigest()[:12]
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise SystemExit(f"error: scene '{scene['id']}': cannot import {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        try:
            spec.loader.exec_module(module)
        except Exception as exc:
            # A failed exec leaves a half-initialised module bound; drop it so a
            # retry in the same process re-executes rather than importing a shell.
            sys.modules.pop(name, None)
            raise SystemExit(f"error: scene '{scene['id']}': {path} failed to "
                             f"import: {exc.__class__.__name__}: {exc}")
        _BUILDER_MODULES[path] = module

    builder = getattr(module, scene["name"], None)
    if not callable(builder):
        offered = sorted(n for n, v in vars(module).items()
                         if callable(v) and not n.startswith("_"))
        raise SystemExit(
            f"error: scene '{scene['id']}': {path.name} has no callable "
            f"'{scene['name']}' (found: {', '.join(offered) or 'nothing'})")
    return builder


class StoryboardScene(Scene):
    # Manim's Scene takes no arbitrary kwargs; the plan arrives as class state.
    plan = None
    ctx = None

    def custom_scene(self, entry, live):
        """Hand the slot to a builder, then prove it gave the slot back.

        A custom scene has no static group to fade IN — the builder draws its
        own opening — so the incoming transition only clears the previous scene.
        Nothing is added after the builder either: `duration` is the whole slot.
        """
        trans_f = entry["transition_frames"]
        if trans_f:
            if live:
                self.play(*[FadeOut(m) for m in live], run_time=run_time(trans_f))
            else:
                self.wait(hold_time(trans_f), frozen_frame=True)
        else:
            for m in live:
                self.remove(m)

        builder = load_builder(entry["scene"], self.ctx["sb_dir"])
        # renderer.time advances by exactly dt per frame WRITTEN (add_frame),
        # not by the run_time asked for, so this measures emitted frames — the
        # thing timings.json claims — and not the builder's intent.
        before = self.renderer.time
        where = f"{entry['scene']['module']}:{entry['scene']['name']}"
        try:
            builder(self, theme, components, entry["hold"])
        except SystemExit:
            raise
        except Exception as exc:
            # Builder bugs and the primitives' ValueErrors are storyboard
            # defects, not renderer crashes: they get the same one-line form as
            # every other refusal rather than a traceback the author must read.
            raise SystemExit(f"error: scene '{entry['id']}': builder {where} "
                             f"raised {exc.__class__.__name__}: {exc}")
        spent = int(round((self.renderer.time - before) * theme.FPS))
        drift = spent - entry["hold_frames"]
        if drift:
            raise SystemExit(
                f"error: scene '{entry['id']}': builder {where} "
                f"{'over' if drift > 0 else 'under'}ran its slot by {abs(drift)} "
                f"frame(s) ({abs(drift) / theme.FPS:.3f}s) — spent {spent} of the "
                f"{entry['hold_frames']} frames ({entry['hold']:.3f}s) it was "
                f"given. timings.json would be wrong for every later scene; "
                f"quantise with components.run_time / hold_time and spend the "
                f"remainder as a trailing wait.")
        return list(self.mobjects)

    def construct(self):
        live = []
        for entry in self.plan["scenes"]:
            if entry["type"] == "custom":
                live = self.custom_scene(entry, live)
                continue
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
        "background_color": theme.GROUND,
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
