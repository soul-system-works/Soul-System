#!/usr/bin/env python3
"""Codex event adapter for the Soul completion gate; never parse transcripts.

State is keyed by project, session, turn, and tool call. Bash changes are observed
through Git-visible file fingerprints around a tool call, including already dirty
and untracked files. Ignored files, outside-project writes, and non-Git shell
writes are outside that detector's coverage. Direct edit events still count.
"""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "soul_completion", ROOT / "hooks" / "pre-completion-verify.py"
)
gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gate)
_guard_spec = importlib.util.spec_from_file_location(
    "soul_secret_guard", ROOT / "hooks" / "secret-guard.py"
)
guard = importlib.util.module_from_spec(_guard_spec)
_guard_spec.loader.exec_module(guard)


def _key(*parts):
    return hashlib.sha256(json.dumps(parts).encode()).hexdigest()


def _state(data):
    # Missing IDs must not mix an older edit into an unrelated session or turn.
    if not all(isinstance(data.get(k), str) and data[k] for k in ("cwd", "session_id", "turn_id")):
        raise ValueError("cwd, session_id and turn_id are required")
    base = Path(os.environ.get("PLUGIN_DATA", tempfile.gettempdir())) / "soul-codex"
    return base / _key(str(Path(data["cwd"]).resolve()), data["session_id"], data["turn_id"])


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(text)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _git(cwd, *args):
    return subprocess.run(
        ["git", "-C", str(cwd), *args], check=True, stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL, timeout=3,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    ).stdout


def _fingerprint(cwd):
    """Hash Git-visible dirty content, not just status labels or modification times.

    A file can remain ' M' while its contents change again. Status-only tracking
    would miss that edit. Keep content in the fingerprint and never store it.
    """
    try:
        cwd = Path(cwd).resolve()
        repo = Path(os.fsdecode(_git(cwd, "rev-parse", "--show-toplevel")).strip()).resolve()
        if repo != cwd:
            return None  # Never fingerprint a parent project's files.
        paths = set()
        for args in (
            ("diff", "--no-ext-diff", "--name-only", "-z", "--", "."),
            ("diff", "--no-ext-diff", "--cached", "--name-only", "-z", "--", "."),
            ("ls-files", "--others", "--exclude-standard", "-z", "--", "."),
        ):
            paths.update(p for p in _git(cwd, *args).split(b"\0") if p)
        digest = hashlib.sha256()
        total = 0
        for raw in sorted(paths):
            name = os.fsdecode(raw)
            if name in (".soul/events.jsonl", ".soul/handoff.md"):
                continue
            path = cwd / name
            digest.update(raw + b"\0")
            try:
                info = path.lstat()
            except FileNotFoundError:
                digest.update(b"deleted\0")
                continue
            digest.update(str(stat.S_IMODE(info.st_mode)).encode() + b"\0")
            if path.is_symlink():
                digest.update(os.fsencode(os.readlink(path)))
            elif stat.S_ISREG(info.st_mode):
                total += info.st_size
                if total > 64 * 1024 * 1024:
                    return None  # Bound hook cost; manual verification remains owed.
                with path.open("rb") as stream:
                    for chunk in iter(lambda: stream.read(65536), b""):
                        digest.update(chunk)
            else:
                return None  # Submodules and special files need their own checks.
        return digest.hexdigest()
    except (OSError, subprocess.SubprocessError):
        return None


def _context(event, text):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}))


def _emit_verdict(cwd, data, turn):
    """Emit soul.gate.completion.verdict from the reply to this turn's checklist.

    Parity with the Claude hook's stop_hook_active path, read from Codex's
    last_assistant_message instead of a transcript. Emits only when THIS adapter
    blocked the turn (another hook's block is not ours to read), at most once per
    turn, and nothing when the payload carries no reply string: unknown is not
    "unreported". Codex supplies the last message only, so a Verify line in an
    earlier message of the same reply is missed. Fail-open: never blocks, never raises.
    """
    try:
        message = data.get("last_assistant_message")
        if not (turn / "blocked").exists() or (turn / "verdict").exists() or not isinstance(message, str):
            return
        _write(turn / "verdict", "1")
        gate._emit_event(cwd, data, "soul.gate.completion.verdict",
                         {"verdict": gate._classify_reply(message), "self_reported": True})
    except Exception:
        pass  # the verdict is a record, never a reason to block


def _guard_data_dir():
    # Codex sets PLUGIN_DATA (and CLAUDE_PLUGIN_DATA for compatibility) for plugin hooks.
    return os.environ.get("PLUGIN_DATA") or os.environ.get("CLAUDE_PLUGIN_DATA")


def handle(data):
    """Secret guard notices first, then the gate's own handling (SOUL-I070).

    Codex is an OPT-IN for the secret guard: Codex has no env file, and the command
    rewrite that once stood in for one was dropped (owner decision D1, 2026-10-20 —
    Codex's exec policy judged the rewritten script as one command, so the user's
    own prefix rules stopped matching; see the FENCE in hooks/secret-guard.py).
    SessionStart installs the hook folder and says whether the owner's
    shell_environment_policy opt-in is present; PreToolUse on Bash re-verifies the
    folder and gives the bypass / hook-installer notices. Nothing here rewrites,
    allows or blocks a command.

    One JSON object per hook run: the guard's notice, with the adapter's skip message
    folded in if the fingerprint step fails after it.
    """
    event = data.get("hook_event_name")
    if event == "PreToolUse" and data.get("tool_name") == "Bash":
        try:
            out = guard.pre_tool_use(data, _guard_data_dir())
            out = {"systemMessage": out["systemMessage"]} if out else None
        except Exception as exc:
            out = {"systemMessage": f"Soul secret guard skipped ({type(exc).__name__}) — NOT checked."}
        try:
            code = _handle(data)
        except Exception as exc:
            if not out:
                raise
            out = {"systemMessage": f"{out['systemMessage']}\n{_skipped(exc)}"}
            code = 0
        if out:
            print(json.dumps(out))
        return code
    return _handle(data)


def _guard_session_note(cwd):
    """Install the hook folder (so the opt-in has something to point at) and say
    whether Codex is armed. Never raises: the contract context must still go out."""
    try:
        if not guard.soul_scoped(cwd, gate):
            return ""
        return guard.codex_armed_note(cwd, guard.install(_guard_data_dir()))
    except Exception as exc:
        return f"Soul secret guard NOT armed under Codex ({type(exc).__name__})."


def _handle(data):
    cwd = data.get("cwd")
    if not isinstance(cwd, str) or not Path(cwd).is_dir() or not gate._is_soul_project(cwd):
        return 0
    event = data.get("hook_event_name")
    if event == "SessionStart":
        contract = (ROOT / "operations" / "CLAUDE.md").read_text(encoding="utf-8")
        _context(event, (
            f"Soul Codex SessionStart hook ran for session {data.get('session_id', 'unknown')}. "
            "This proves startup delivery, not that Stop has been exercised. "
            "The contract below comes from the currently installed plugin. Read existing "
            "project CLAUDE.md for local Register/Stage, the existing mind.md, and witness.md "
            "tail (root or .soul/). Codex does not expand @imports. "
            "Use $soul-system:soul-resume to check stale project wiring.\n\n" + contract
            + (f"\n\n{note}" if (note := _guard_session_note(cwd)) else "")
        ))
        return 0
    if event not in ("PreToolUse", "PostToolUse", "Stop"):
        return 0
    turn = _state(data)
    if event == "Stop":
        if data.get("stop_hook_active"):
            _emit_verdict(cwd, data, turn)
            return 0
        if not (turn / "edited").exists():
            return 0
        message = data.get("last_assistant_message")
        if not isinstance(message, str) or not gate._CLAIM_RE.search(message):
            return 0
        cooldown = gate._cooldown_path(cwd)
        if gate._within_cooldown(cooldown) or (turn / "blocked").exists():
            return 0
        _write(turn / "blocked", "1")
        gate._mark_fire(cooldown)
        gate._emit_event(cwd, data)
        print(gate._checklist(), file=sys.stderr)
        return 2
    tool = data.get("tool_name")
    if tool == "Bash":
        tool_id = data.get("tool_use_id")
        if not isinstance(tool_id, str) or not tool_id:
            raise ValueError("Bash tracking requires tool_use_id")
        before = turn / (_key(tool_id) + ".before")
        if event == "PreToolUse":
            value = _fingerprint(cwd)
            if value is not None:
                _write(before, value)
        elif before.is_file():
            value = _fingerprint(cwd)
            if value is not None and before.read_text() != value:
                _write(turn / "edited", "1")
            before.unlink(missing_ok=True)
    elif event == "PostToolUse" and tool in {"apply_patch", "Edit", "Write", "MultiEdit", "NotebookEdit"}:
        # Like Claude's detector, this observes an edit-tool invocation. A failed
        # edit can produce a conservative reminder; no claim of successful edit.
        _write(turn / "edited", "1")
    return 0


def main():
    try:
        data = json.load(sys.stdin)
        if not isinstance(data, dict):
            raise ValueError("hook input must be an object")
        return handle(data)
    except Exception as exc:
        # Fail open with a visible diagnostic; silence must not imply armed.
        print(json.dumps({"systemMessage": _skipped(exc)}))
        return 0


def _skipped(exc):
    return (f"Soul Codex hook skipped ({type(exc).__name__}); automatic verification "
            "is not guaranteed. Apply the completion checklist manually.")


if __name__ == "__main__":
    sys.exit(main())
