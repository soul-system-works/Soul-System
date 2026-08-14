#!/usr/bin/env python3
"""Storyboard linter — schema, timing budget, and the anonymisation backstop.

Also the single place that computes holds: render.py imports build_plan from
here so the arithmetic the human reviews is the arithmetic that renders. The
plan is laid out in whole FRAMES, not seconds — Manim quantises every play and
wait to `np.arange(0, run_time, 1/fps)`, so a plan in raw seconds drifts and a
59.9s lint pass can render over budget.

Every malformed input must exit 1 with a message. A traceback out of here is a
bug in the linter, not a verdict on the storyboard.

Usage: lint.py <storyboard.yaml>   (exit 0 pass, 1 fail)
"""

import ast
import math
import os
import re
import sys
from pathlib import Path

import yaml

import theme
import timing

SCHEMA_VERSION = 1
FORMATS = {"skill": timing.BUDGET_SKILL, "overview": timing.BUDGET_OVERVIEW}
FRAME = 1.0 / theme.FPS

# The denylist location is overridable so tests never write through the Body's
# real list — losing it would silently disarm the anonymisation backstop.
DENYLIST_ENV = "SOUL_VIDEO_DENYLIST"

TOP_REQUIRED = {"video", "schema", "format", "inputs", "scenes"}
TOP_TYPES = {"video": str, "schema": int, "format": str,
             "inputs": list, "scenes": list}

# Per scene type: (required fields, optional fields). `narration` is reserved by
# the schema and ignored by the v1 renderer — accepted here so storyboards can
# carry it before any audio stage exists.
COMMON_OPTIONAL = {"transition", "hold", "chapter", "narration"}
SCENE_FIELDS = {
    "title":    ({"heading"}, {"sub"}),
    "bullets":  ({"heading", "items"}, set()),
    "code":     (set(), {"lang", "file", "source", "highlight"}),
    "terminal": ({"capture"}, {"reveal"}),
    "diagram":  ({"asset"}, {"heading"}),
    "outro":    ({"text"}, {"url"}),
    "custom":   ({"module", "name", "duration", "text"}, set()),
}
FIELD_TYPES = {
    "id": str, "type": str, "heading": str, "sub": str, "text": str,
    "url": str, "lang": str, "file": str, "source": str, "capture": str,
    "asset": str, "transition": str, "reveal": str, "chapter": str,
    "narration": str, "items": list, "highlight": list, "hold": (int, float),
    "module": str, "name": str, "duration": (int, float),
}
# Per-type overrides of FIELD_TYPES: `text` is one string on an outro and the
# list of every on-screen string on a custom scene.
SCENE_FIELD_TYPES = {"custom": {"text": list}}
PATH_FIELDS = ("capture", "file", "asset", "module")
TRANSITIONS = {"fade", "cut"}
REVEALS = {"line", "block"}


class LintError(Exception):
    pass


def frames_up(seconds: float) -> int:
    """Whole frames, rounded UP — a computed minimum is never undercut."""
    return int(math.ceil(seconds * theme.FPS - 1e-9))


def _words(*parts) -> int:
    return sum(len(str(p).split()) for p in parts if p)


def _typed(scene: dict, field: str, expected) -> None:
    value = scene[field]
    if isinstance(value, bool) or not isinstance(value, expected):
        names = getattr(expected, "__name__", None) or \
            " or ".join(t.__name__ for t in expected)
        raise LintError(f"scene '{scene.get('id', '?')}': {field} must be {names}, "
                        f"got {type(value).__name__}")


def resolve(sb_dir: Path, raw: str, what: str) -> Path:
    """Resolve a reference and refuse to leave the repo.

    An out-of-repo path leaks the machine's layout into the committed manifest
    (repo_key falls back to an absolute path, username included) and puts an
    unreviewed file in a public video.
    """
    path = (sb_dir / str(raw)).resolve()
    if not path.is_relative_to(theme.REPO_ROOT):
        raise LintError(f"{what}: {raw} resolves outside the repo ({path})")
    if not path.exists():
        raise LintError(f"{what}: {raw} does not exist ({path})")
    return path


def _read_text(path: Path, what: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise LintError(f"{what}: {path} is not UTF-8 text")
    except OSError as exc:
        raise LintError(f"{what}: cannot read {path} ({exc})")


def code_source(scene: dict, sb_dir: Path) -> str:
    if ("file" in scene) == ("source" in scene):
        raise LintError(f"scene '{scene['id']}': code needs exactly one of file / source")
    if "file" in scene:
        path = resolve(sb_dir, scene["file"], f"scene '{scene['id']}' file")
        return _read_text(path, f"scene '{scene['id']}' file")
    return str(scene["source"])


def visible_lines(text: str) -> list[str]:
    """Trailing blank lines are not content and do not buy hold time."""
    lines = text.replace("\r\n", "\n").split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def referenced_files(scene: dict, sb_dir: Path) -> list[Path]:
    return [(sb_dir / scene[k]).resolve() for k in PATH_FIELDS if k in scene]


def _check_scene_schema(scene, index: int) -> None:
    if not isinstance(scene, dict):
        raise LintError(f"scene #{index}: not a mapping")
    if "id" not in scene:
        raise LintError(f"scene #{index}: missing 'id'")
    sid = scene["id"]
    stype = scene.get("type")
    if stype not in SCENE_FIELDS:
        raise LintError(f"scene '{sid}': unknown type {stype!r}; "
                        f"expected one of {', '.join(sorted(SCENE_FIELDS))}")
    required, optional = SCENE_FIELDS[stype]
    allowed = {"id", "type"} | required | optional | COMMON_OPTIONAL
    if stype == "custom":
        # A custom scene's builder owns its whole slot; `hold` would be a second
        # source of truth for the same number and the drift check would fail on
        # whichever one the builder did not honour.
        allowed.discard("hold")
    unknown = set(scene) - allowed
    if unknown:
        raise LintError(f"scene '{sid}': unknown field(s) {', '.join(sorted(unknown))}"
                        + (" (custom scenes size themselves with duration:)"
                           if stype == "custom" and "hold" in unknown else ""))
    missing = required - set(scene)
    if missing:
        raise LintError(f"scene '{sid}': missing field(s) {', '.join(sorted(missing))}")

    types = {**FIELD_TYPES, **SCENE_FIELD_TYPES.get(stype, {})}
    for field in scene:
        if field in types:
            _typed(scene, field, types[field])
    if "items" in scene and not all(isinstance(i, str) for i in scene["items"]):
        raise LintError(f"scene '{sid}': items must all be strings")
    if stype == "custom" and not all(isinstance(t, str) for t in scene["text"]):
        raise LintError(f"scene '{sid}': text must be a list of strings "
                        f"(every on-screen string the scene shows; [] if none)")
    if "highlight" in scene and not all(
            isinstance(n, int) and not isinstance(n, bool) for n in scene["highlight"]):
        raise LintError(f"scene '{sid}': highlight must be a list of line numbers")
    if scene.get("transition", "fade") not in TRANSITIONS:
        raise LintError(f"scene '{sid}': transition must be fade | cut")
    if scene.get("reveal", "block") not in REVEALS:
        raise LintError(f"scene '{sid}': reveal must be line | block")


def _check_doc_schema(doc) -> None:
    if not isinstance(doc, dict):
        raise LintError("storyboard is not a mapping")
    unknown = set(doc) - TOP_REQUIRED
    if unknown:
        raise LintError(f"unknown top-level field(s): {', '.join(sorted(unknown))}")
    missing = TOP_REQUIRED - set(doc)
    if missing:
        raise LintError(f"missing top-level field(s): {', '.join(sorted(missing))}")
    for field, expected in TOP_TYPES.items():
        if isinstance(doc[field], bool) or not isinstance(doc[field], expected):
            raise LintError(f"{field} must be {expected.__name__}, "
                            f"got {type(doc[field]).__name__}")
    if doc["schema"] != SCHEMA_VERSION:
        raise LintError(f"schema {doc['schema']} unsupported; renderer speaks {SCHEMA_VERSION}")
    if doc["format"] not in FORMATS:
        raise LintError(f"format must be one of {', '.join(sorted(FORMATS))}")
    if not doc["inputs"]:
        raise LintError("inputs must be a non-empty list of repo-relative paths")
    if not doc["scenes"]:
        raise LintError("scenes must be a non-empty list")


def _check_asset(path: Path, sid: str) -> None:
    """Manim's SVGMobject drops <text>; without this the labels vanish silently."""
    text = _read_text(path, f"scene '{sid}' asset")
    # Comments are stripped first: an SVG whose comment merely mentions the
    # element is not an SVG that draws one.
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    # Namespace prefixes are legal and common from Inkscape/Illustrator exports,
    # so <svg:text> must not slip past a bare "<text" substring match.
    if re.search(r"<(?:[A-Za-z0-9_.-]+:)?text(?:Path)?\b", text):
        raise LintError(
            f"scene '{sid}': {path.name} contains <text> elements, which Manim's "
            f"SVGMobject silently drops — every label would be missing from the "
            f"frame. Convert text to paths, rasterise, or use a text-free asset.")


def _check_module_imports(path: Path, sb_dir: Path, sid: str) -> None:
    """Custom builders are ONE file. Enforce it, because the gaps are silent.

    A local `from helpers import x` pulls in a file that is not a scanned
    surface (a real name in it reaches a public video unchecked) and not a
    hashed input (editing it leaves the video reported FRESH). Rather than
    chase the import graph, the graph is kept to one node: shared motion code
    graduates into components.py, which every video already hashes via the
    theme version.
    """
    tree_src = _read_text(path, f"scene '{sid}' module")
    try:
        tree = ast.parse(tree_src, filename=str(path))
    except SyntaxError as exc:
        raise LintError(f"scene '{sid}': {path.name} does not parse "
                        f"(line {exc.lineno}): {exc.msg}")

    def refuse(what: str) -> None:
        raise LintError(
            f"scene '{sid}': {path.name} imports {what} — custom builders are a "
            f"single file. A local helper is neither denylist-scanned nor hashed "
            f"into the staleness manifest, so editing it leaves the video falsely "
            f"FRESH and its strings unchecked. Inline it, or graduate the shared "
            f"part into videos/render/components.py.")

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.level:
            refuse(f"relatively ('{'.' * node.level}{node.module or ''}')")
        roots = []
        if isinstance(node, ast.Import):
            roots = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots = [node.module.split(".")[0]]
        for root in roots:
            if (sb_dir / f"{root}.py").exists() or \
                    (sb_dir / root / "__init__.py").exists():
                refuse(f"sibling module '{root}'")


def _check_limits(scene: dict, sb_dir: Path) -> tuple[float, int, int]:
    """Returns (computed_hold_seconds, line_count, reveal_count)."""
    sid, stype = scene["id"], scene["type"]

    if stype == "custom":
        module = resolve(sb_dir, scene["module"], f"scene '{sid}' module")
        if module.suffix != ".py":
            raise LintError(f"scene '{sid}': module {scene['module']} is not a .py file")
        _check_module_imports(module, module.parent, sid)
        # The declared `text` is the whole readability contract for a custom
        # scene: the linter cannot see inside the builder, so the storyboard has
        # to declare what the frame will say, and the same read rate a title
        # scene gets is applied to it.
        words = _words(*scene["text"])
        minimum = timing.BASE_HOLD + timing.WORD_RATE * words
        duration = float(scene["duration"])
        if duration + 1e-9 < minimum:
            raise LintError(
                f"scene '{sid}': duration {duration:.2f}s is below the read-rate "
                f"minimum {minimum:.2f}s for its {words} declared word(s) of "
                f"on-screen text (BASE_HOLD + WORD_RATE x words) — lengthen the "
                f"beat or cut text")
        return duration, 0, 0

    if stype in ("code", "terminal"):
        if stype == "code":
            text = code_source(scene, sb_dir)
        else:
            path = resolve(sb_dir, scene["capture"], f"scene '{sid}' capture")
            text = _read_text(path, f"scene '{sid}' capture")
        lines = visible_lines(text)
        if len(lines) > timing.MAX_CODE_LINES:
            raise LintError(f"scene '{sid}': {len(lines)} lines > MAX_CODE_LINES "
                            f"({timing.MAX_CODE_LINES})")
        if not lines:
            raise LintError(f"scene '{sid}': no visible lines")
        for n in scene.get("highlight", []) or []:
            if not 1 <= n <= len(lines):
                raise LintError(f"scene '{sid}': highlight line {n} outside 1..{len(lines)}")
        hold = timing.BASE_HOLD + timing.CODE_BASE + timing.CODE_LINE_RATE * len(lines)
        reveals = len([ln for ln in lines if ln.strip()]) \
            if stype == "terminal" and scene.get("reveal") == "line" else 0
        return hold, len(lines), reveals

    reveals = 0
    if stype == "bullets":
        items = scene["items"]
        if not items:
            raise LintError(f"scene '{sid}': items must be a non-empty list")
        if len(items) > timing.MAX_BULLETS:
            raise LintError(f"scene '{sid}': {len(items)} bullets > MAX_BULLETS "
                            f"({timing.MAX_BULLETS})")
        words = _words(scene["heading"], *items)
        reveals = len(items)
    elif stype == "title":
        words = _words(scene["heading"], scene.get("sub"))
    elif stype == "outro":
        words = _words(scene["text"], scene.get("url"))
    else:  # diagram — an optional heading is its only prose
        _check_asset(resolve(sb_dir, scene["asset"], f"scene '{sid}' asset"), sid)
        words = _words(scene.get("heading"))

    if words > timing.MAX_WORDS_SCENE:
        raise LintError(f"scene '{sid}': {words} words > MAX_WORDS_SCENE "
                        f"({timing.MAX_WORDS_SCENE})")
    return timing.BASE_HOLD + timing.WORD_RATE * words, 0, reveals


def build_plan(doc: dict, sb_dir: Path) -> dict:
    """Validate and lay the storyboard out on the frame grid. Raises LintError."""
    _check_doc_schema(doc)
    for entry in doc["inputs"]:
        resolve(theme.REPO_ROOT, entry, "declared input")

    reveal_frames = frames_up(theme.REVEAL_STEP)
    seen: set[str] = set()
    entries = []
    clock = 0  # frames
    for i, scene in enumerate(doc["scenes"]):
        _check_scene_schema(scene, i)
        sid = scene["id"]
        if sid in seen:
            raise LintError(f"duplicate scene id '{sid}'")
        seen.add(sid)
        if "chapter" in scene and doc["format"] != "overview":
            raise LintError(f"scene '{sid}': chapter: is allowed only on format: overview")

        computed_s, n_lines, n_reveals = _check_limits(scene, sb_dir)
        # theme.REVEAL_STEP is a theme knob; keep it provably inside the hold the
        # timing constants buy, rather than relying on the constants happening to
        # be generous (a raised REVEAL_STEP would otherwise kill a linted render).
        if n_reveals * theme.REVEAL_STEP > computed_s - 1.0 + 1e-9:
            raise LintError(
                f"scene '{sid}': {n_reveals} reveals x REVEAL_STEP "
                f"({theme.REVEAL_STEP}s) leave under 1.0s of the computed hold "
                f"({computed_s:.2f}s) — lower theme.REVEAL_STEP or cut content")

        computed_f = frames_up(computed_s)
        hold_f = computed_f
        if "hold" in scene:
            explicit_f = frames_up(float(scene["hold"]))
            if explicit_f < computed_f:
                raise LintError(
                    f"scene '{sid}': explicit hold {float(scene['hold'])}s below "
                    f"computed minimum {computed_f * FRAME:.3f}s — cut content, "
                    f"do not shrink holds")
            hold_f = explicit_f
        if hold_f < n_reveals * reveal_frames:
            raise LintError(f"scene '{sid}': reveals do not fit inside the hold")

        trans = scene.get("transition", "fade")
        trans_f = frames_up(timing.TRANSITION_DUR) if trans == "fade" else 0

        entries.append({
            "id": sid, "type": scene["type"], "transition": trans,
            "transition_frames": trans_f, "computed_frames": computed_f,
            "hold_frames": hold_f, "reveal_frames": reveal_frames,
            "n_reveals": n_reveals, "lines": n_lines, "chapter": scene.get("chapter"),
            "transition_dur": trans_f * FRAME,
            "computed_hold": computed_f * FRAME, "hold": hold_f * FRAME,
            "start_frame": clock, "end_frame": clock + trans_f + hold_f,
            "start": clock * FRAME, "end": (clock + trans_f + hold_f) * FRAME,
            "scene": scene,
        })
        clock += trans_f + hold_f

    budget = FORMATS[doc["format"]]
    duration = clock * FRAME
    if duration > budget + 1e-9:
        raise LintError(f"runtime {duration:.2f}s over the {doc['format']} budget "
                        f"({budget}s) — cut scenes")

    return {"video": doc["video"], "format": doc["format"], "inputs": doc["inputs"],
            "scenes": entries, "frames": clock, "duration": duration, "budget": budget}


def budget_warning(plan: dict) -> str | None:
    """Q16: skill videos target 35-40s. Over WARN_SKILL is a smell, not a defect.

    A warning rather than a failure because the number is taste calibrated on one
    video (pilot v1's 51.5s read long), while BUDGET_SKILL is the contract. The
    two must not be confused, so this never changes the exit code.
    """
    if plan["format"] != "skill":
        return None
    if plan["duration"] <= timing.WARN_SKILL + 1e-9:
        return None
    return (f"WARNING: runtime {plan['duration']:.2f}s over WARN_SKILL "
            f"({timing.WARN_SKILL}s) — the Q16 target is 35-40s of motion, not "
            f"stacked holds. Not a failure; the hard budget is "
            f"{timing.BUDGET_SKILL}s.")


def denylist_path() -> Path:
    override = os.environ.get(DENYLIST_ENV)
    return Path(override) if override else theme.REPO_ROOT / ".soul" / "denylist.txt"


def _denylist_scan(surfaces: list[tuple[Path, str]]) -> list[str]:
    """Q8 backstop. The list is gitignored; the names never enter the repo."""
    deny = denylist_path()
    if not deny.exists():
        print(f"WARNING: no denylist at {deny} — anonymisation unchecked "
              f"(the human gate is primary)", file=sys.stderr)
        return []
    names = [ln.strip() for ln in deny.read_text(encoding="utf-8").splitlines()
             if ln.strip() and not ln.startswith("#")]
    if not names:
        return []
    hits = []
    for path, text in surfaces:
        low = text.lower()
        for name in names:
            if name.lower() in low:
                hits.append(f"denylist hit in {path}: <redacted, {len(name)} chars>")
    return hits


def _scan_surfaces(plan: dict, sb_path: Path, raw: str) -> list[tuple[Path, str]]:
    """Storyboard + script.md + every referenced text file (spec: gates section)."""
    sb_dir = sb_path.parent
    surfaces = [(sb_path, raw)]
    paths = [sb_dir / "script.md"] + [
        f for e in plan["scenes"] for f in referenced_files(e["scene"], sb_dir)]
    for path in paths:
        if not path.exists():
            continue
        try:
            surfaces.append((path, path.read_text(encoding="utf-8")))
        except (OSError, UnicodeDecodeError) as exc:
            # Never skip silently: an unscanned surface is an unchecked surface.
            print(f"WARNING: {path} skipped (unreadable: {exc.__class__.__name__}) "
                  f"— not scanned against the denylist", file=sys.stderr)
    return surfaces


def format_table(plan: dict) -> str:
    rows = [f"{'scene':<16} {'type':<9} {'trans':<5} {'computed':>9} "
            f"{'hold':>7} {'start':>7} {'end':>7}"]
    rows.append("-" * 66)
    for e in plan["scenes"]:
        flag = "" if e["hold_frames"] == e["computed_frames"] else "  (explicit)"
        rows.append(f"{e['id']:<16} {e['type']:<9} {e['transition']:<5} "
                    f"{e['computed_hold']:>9.2f} {e['hold']:>7.2f} "
                    f"{e['start']:>7.2f} {e['end']:>7.2f}{flag}")
    rows.append("-" * 66)
    rows.append(f"{'TOTAL':<16} {plan['format']:<9} {'':<5} {'':>9} "
                f"{'':>7} {'':>7} {plan['duration']:>7.2f}  "
                f"/ {plan['budget']:.0f}s budget ({plan['frames']} frames "
                f"@ {theme.FPS}fps)")
    return "\n".join(rows)


def lint(path: Path) -> tuple[bool, dict | None, str]:
    """Returns (ok, plan, report). Never raises on storyboard content."""
    path = Path(path).resolve()
    if not path.is_relative_to(theme.REPO_ROOT):
        # Same rule as every other reference: outside the repo there is no
        # repo-relative key, and repo_key would fall back to an absolute path.
        return False, None, (f"FAIL {path}\n  storyboard resolves outside the "
                             f"repo ({theme.REPO_ROOT})")
    try:
        raw = path.read_text(encoding="utf-8")
        doc = yaml.safe_load(raw)
        plan = build_plan(doc, path.parent)
        surfaces = _scan_surfaces(plan, path, raw)
    except LintError as exc:
        return False, None, f"FAIL {path}\n  {exc}"
    except yaml.YAMLError as exc:
        return False, None, f"FAIL {path}\n  YAML parse error: {exc}"
    except (OSError, UnicodeDecodeError) as exc:
        return False, None, f"FAIL {path}\n  cannot read storyboard: {exc}"
    except Exception as exc:  # a linter that tracebacks gives no verdict at all
        return False, None, f"FAIL {path}\n  malformed storyboard: " \
                            f"{exc.__class__.__name__}: {exc}"

    hits = _denylist_scan(surfaces)
    report = format_table(plan)
    warning = budget_warning(plan)
    if warning:
        report += "\n\n" + warning
    if hits:
        return False, plan, report + "\n\nFAIL — anonymisation:\n  " + "\n  ".join(hits)
    return True, plan, report + f"\n\nOK {path}"


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    ok, _plan, report = lint(Path(argv[1]))
    print(report)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
