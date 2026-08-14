#!/usr/bin/env python3
"""Smoke test for the stage-3 renderer.

Four load-bearing assertions:
  - the same storyboard produces byte-identical mp4s (the manifest means nothing
    without it), and the fixture includes a `custom` scene so that covers a
    hand-written motion builder and not only the declarative types;
  - the planned runtime matches the rendered runtime to within one frame (a plan
    that drifts can pass a 60s budget and render over it);
  - a custom builder that does not spend its slot exactly aborts the render,
    because timings.json is published and a drifting builder makes it wrong;
  - every malformed storyboard exits 1 with a message, because the linter IS the
    gate the human reads.

Run: ~/.cache/soul-video/venv/bin/python videos/render/tests/smoke_test.py
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

RENDER_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RENDER_DIR))

import lint      # noqa: E402
import render    # noqa: E402
import theme     # noqa: E402
import timing    # noqa: E402

SMOKE = RENDER_DIR / "tests" / "smoke" / "storyboard.yaml"
OVERVIEW = RENDER_DIR / "tests" / "smoke" / "overview.yaml"
WARN_LONG = RENDER_DIR / "tests" / "smoke" / "warn-long.yaml"
BAD = RENDER_DIR / "tests" / "bad"
# Planted fixtures have to live INSIDE the repo: every reference is containment
# checked, so a storyboard under $HOME cannot be linted at all.
TMP = RENDER_DIR / "tests" / ".tmp"
LINT_PY = RENDER_DIR / "lint.py"
RENDER_PY = RENDER_DIR / "render.py"
WORK = theme.CACHE_ROOT / "smoke-test"

# (fixture, substring the failure message must carry)
NEGATIVES = [
    ("unknown-field.yaml", "unknown field(s) subtitle"),
    ("malformed-type.yaml", "highlight must be list"),
    ("short-hold.yaml", "below computed minimum"),
    ("over-budget.yaml", "over the skill budget"),
    ("missing-asset.yaml", "does not exist"),
    ("svg-text-asset.yaml", "SVGMobject silently drops"),
    ("ns-text-asset.yaml", "SVGMobject silently drops"),
    ("outside-repo.yaml", "resolves outside the repo"),
    ("bad-input-path.yaml", "declared input"),
    ("custom-short.yaml", "below the read-rate minimum"),
    ("custom-missing-module.yaml", "does not exist"),
    ("custom-hold.yaml", "custom scenes size themselves with duration:"),
    ("custom-sibling-import.yaml", "custom builders are a single file"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"  PASS  {message}")


def run(script: Path, *args, env_extra: dict | None = None) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env.update(env_extra or {})
    return subprocess.run([sys.executable, str(script), *args],
                          capture_output=True, text=True, env=env)


def ffprobe_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json",
         "-show_entries", "format=duration:stream=nb_frames", str(path)],
        check=True, capture_output=True, text=True)
    probe = json.loads(out.stdout)
    return float(probe["format"]["duration"]), int(probe["streams"][0]["nb_frames"])


def negatives() -> None:
    print("== negative fixtures (the gate must say no) ==")
    for name, expected in NEGATIVES:
        result = run(LINT_PY, str(BAD / name))
        blob = result.stdout + result.stderr
        check(result.returncode == 1,
              f"{name}: lint exits 1 (got {result.returncode})")
        check(expected in blob, f"{name}: message carries {expected!r}")

    result = run(RENDER_PY, str(BAD / "unknown-field.yaml"),
                 "--out", str(WORK / "never"), "--no-manifest")
    check(result.returncode == 1, "render.py refuses to render a failing storyboard")
    check(not (WORK / "never").exists(), "render.py wrote nothing on refusal")

    # The storyboard itself must be inside the repo, or repo_key has no
    # repo-relative form and the manifest would carry an absolute $HOME path.
    outside = WORK / "outside-storyboard.yaml"
    outside.parent.mkdir(parents=True, exist_ok=True)
    outside.write_text(SMOKE.read_text(encoding="utf-8"), encoding="utf-8")
    result = run(LINT_PY, str(outside))
    check(result.returncode == 1, "out-of-repo storyboard: lint exits 1")
    check("storyboard resolves outside the repo" in result.stdout + result.stderr,
          "out-of-repo storyboard: message names the cause")


def custom_scenes() -> None:
    """The `custom` path: the builder's slot is a contract, checked at render.

    Lint cannot see inside a builder, so the drift abort is the only thing
    standing between an overrunning builder and a timings.json that is wrong for
    every scene after it.
    """
    print("\n== custom scenes ==")
    result = run(RENDER_PY, str(BAD / "drift.yaml"),
                 "--out", str(WORK / "drift"), "--no-manifest")
    blob = result.stdout + result.stderr
    check(result.returncode == 1, "an overrunning builder fails the render")
    check("overran its slot by 15 frame(s)" in blob,
          "the abort names the drift in frames")
    check(not (WORK / "drift").exists(), "nothing was written for the drifting render")

    ok, plan, _report = lint.lint(WARN_LONG)
    check(ok, "warn-long.yaml passes lint (over WARN_SKILL is not a failure)")
    check(plan["duration"] > timing.WARN_SKILL,
          f"warn-long.yaml really is over WARN_SKILL "
          f"({plan['duration']:.2f}s > {timing.WARN_SKILL}s)")
    check(plan["duration"] <= timing.BUDGET_SKILL,
          "warn-long.yaml is still inside the hard budget")
    result = run(LINT_PY, str(WARN_LONG))
    blob = result.stdout + result.stderr
    check(result.returncode == 0, "lint.py exits 0 on a WARN_SKILL storyboard")
    check("WARNING" in blob and "WARN_SKILL" in blob,
          "the WARN_SKILL warning is printed anyway")


def denylist_gate() -> None:
    """The list is gitignored and the names must never reach stdout.

    The temp list is pointed at via SOUL_VIDEO_DENYLIST rather than written over
    the real one: a test that backs up the Body's anonymisation list in memory
    loses it to any hard kill, and that list is the backstop it cannot re-derive.
    """
    print("\n== denylist gate ==")
    production = theme.REPO_ROOT / ".soul" / "denylist.txt"
    before = production.read_bytes() if production.exists() else None

    deny = WORK / "denylist.txt"
    deny.parent.mkdir(parents=True, exist_ok=True)
    # A word the smoke storyboard really contains, and that the linter's own
    # report vocabulary does not — otherwise the not-echoed check self-collides.
    secret = "backstop"
    deny.write_text(secret + "\n", encoding="utf-8")

    result = run(LINT_PY, str(SMOKE), env_extra={lint.DENYLIST_ENV: str(deny)})
    blob = result.stdout + result.stderr
    check(result.returncode == 1, "denylist hit fails lint")
    check("denylist hit" in blob, "the hit is reported")
    check(secret not in blob, "the matched name is NOT echoed to output")

    # A custom scene's module is code, and code carries string literals. The
    # storyboard below is clean; only the .py it names is dirty, so this fails
    # only if the module FILE is a scanned surface.
    planted = "zarquon"
    deny.write_text(planted + "\n", encoding="utf-8")
    TMP.mkdir(parents=True, exist_ok=True)
    try:
        (TMP / "planted_motion.py").write_text(
            '"""Temp fixture. The name lives ONLY in this module\'s source."""\n'
            f'INTERNAL_NOTE = "{planted}"\n\n\n'
            'def build(scene, theme, components, duration):\n'
            '    components.kinetic_line(scene, ["one two three"], duration=duration)\n',
            encoding="utf-8")
        (TMP / "storyboard.yaml").write_text(
            "video: smoke-planted\nschema: 1\nformat: skill\n"
            "inputs: [docs/video-pipeline.md]\nscenes:\n"
            "  - id: planted\n    type: custom\n    module: planted_motion.py\n"
            "    name: build\n    duration: 4.0\n    text: [\"one two three\"]\n",
            encoding="utf-8")
        result = run(LINT_PY, str(TMP / "storyboard.yaml"),
                     env_extra={lint.DENYLIST_ENV: str(deny)})
        blob = result.stdout + result.stderr
        check(result.returncode == 1, "a name inside a custom module's source fails lint")
        check("planted_motion.py" in blob, "the hit names the module file")
        check(planted not in blob, "the planted name is NOT echoed to output")
    finally:
        shutil.rmtree(TMP, ignore_errors=True)

    after = production.read_bytes() if production.exists() else None
    check(after == before, "the production denylist was not touched")


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)

    negatives()
    custom_scenes()
    denylist_gate()

    print("\n== lint ==")
    plans = {}
    for path in (SMOKE, OVERVIEW):
        ok, plan, report = lint.lint(path)
        print(report)
        check(ok, f"lint passes: {path.name}")
        plans[path] = plan

    custom_ids = [s["id"] for s in plans[SMOKE]["scenes"] if s["type"] == "custom"]
    check(custom_ids,
          f"the smoke fixture carries a custom scene ({', '.join(custom_ids)}) — "
          f"so everything below covers a builder, not just the slide types")

    print("\n== double render (determinism) ==")
    started = time.monotonic()
    first = render.render(plans[SMOKE], SMOKE, WORK / "a")
    elapsed = time.monotonic() - started
    second = render.render(plans[SMOKE], SMOKE, WORK / "b")
    digest_a, digest_b = sha256(first["mp4"]), sha256(second["mp4"])
    print(f"  a {digest_a}\n  b {digest_b}")
    check(digest_a == digest_b, "two renders are byte-identical")
    print(f"  one render: {elapsed:.1f}s wall, "
          f"{first['mp4'].stat().st_size / 1024:.0f} KiB")

    print("\n== timings ==")
    stem = f"{plans[SMOKE]['video']}-t{theme.THEME_VERSION}"
    timings = json.loads((WORK / "a" / f"{stem}.timings.json").read_text())
    scenes = plans[SMOKE]["scenes"]
    check(len(timings["scenes"]) == len(scenes),
          f"timings has one entry per scene ({len(scenes)})")
    check(all(s["id"] in timings["scenes"] for s in scenes),
          "every scene id is present")
    check(timings["duration"] <= timing.BUDGET_SKILL,
          f"duration {timings['duration']}s <= BUDGET_SKILL "
          f"({timing.BUDGET_SKILL}s)")

    planned = plans[SMOKE]["duration"]
    measured, frames = ffprobe_duration(first["mp4"])
    frame = 1.0 / theme.FPS
    print(f"  planned {planned:.4f}s ({plans[SMOKE]['frames']} frames) vs "
          f"rendered {measured:.4f}s ({frames} frames)")
    check(abs(measured - planned) <= frame + 1e-9,
          f"planned runtime matches the mp4 within one frame "
          f"(drift {abs(measured - planned) * 1000:.1f}ms)")

    print("\n== chapters ==")
    chaptered = render.render(plans[OVERVIEW], OVERVIEW, WORK / "a")
    check(chaptered["chapters"], "overview fixture declares chapters")
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json",
         "-show_chapters", str(chaptered["mp4"])],
        check=True, capture_output=True, text=True)
    found = json.loads(probe.stdout)["chapters"]
    titles = [c["tags"]["title"] for c in found]
    print(f"  ffprobe chapters: {titles}")
    check(titles == ["Opening", "Closing"], "chapter metadata is muxed into the mp4")

    print("\nOK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
