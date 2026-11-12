#!/usr/bin/env python3
"""Soul upkeep hook: tells a session when its handoff cursor has gone stale (SOUL-A032).

Two modes, both Claude Code only:

  upkeep.py              Stop hook. When the cursor (.soul/handoff.md) is stale, block
                         the stop once with {"decision": "block", "reason": ...}: the
                         reason asks the session to refresh it with /soul-handoff, then
                         stop. Silent otherwise.
  upkeep.py --compact    SessionStart hook, matcher `compact`. One line of context: a
                         summary just happened, re-read the cursor and refresh it first.

Stale means one of these happened since the cursor was last written:
  - the working context grew by GROWTH_TOKENS or more. The size is read from the
    transcript's main-thread assistant records, message.usage: input_tokens +
    cache_creation_input_tokens + cache_read_input_tokens. Subagent (isSidechain)
    records are skipped (mind item 7). The owner chose a size step over a commit count:
    "some agents/processes commit a lot and others not so much" (SOUL-I089, open
    question 2 of A032). Records with no usage, or a zero total, are skipped.
  - a summary (compaction): a {"type": "system", "subtype": "compact_boundary"} record.

"Last written" is the newest Write / Edit / MultiEdit tool call in THIS transcript whose
file_path resolves to the cursor. No clocks are read: the WSL clock can pause, so a file's
mtime cannot be lined up with transcript times. A cursor written by an earlier session
(the usual case) leaves no such call, and growth is counted from the session's first
assistant record, so the fixed start-up load (contract, CLAUDE.md, tools) is not counted
as conversation. A cursor written by a shell command is not seen; the cost is one extra
block, after which /soul-handoff writes it with the Write tool.

Silent, always, when:
  - stop_hook_active is set (this stop follows a block — never loop);
  - the project is not Soul-governed (the completion gate's own scope test);
  - no cursor exists yet. A project that has never written one has not taken up the
    handoff; the first /soul-handoff (or /soul-init) starts it, and nagging before that
    would block every long session in a project that never asked for a cursor;
  - `.soul/init.md` holds `upkeep: off` (the owner's opt-out, asked once by /soul-init;
    no line means on — the default the owner chose, A032 open question 3). The value
    is read as init-status.py reads it (its LINE_RE, first line of the key wins,
    stripped and lower-cased); only `off` turns it off — anything else, `no` included,
    is "not understood": init-status asks again and this hook stays on;
  - it already blocked at this point: the block is remembered (a small file in the temp
    folder, keyed by transcript) and counts as a new start, so an ignored block does not
    come back every turn — only after another GROWTH_TOKENS or another summary. F063
    and mind item 5 are the reason: a Stop hook that fires every turn gets switched off.
    If that file cannot be written, the hook does not block at all: an unremembered
    block would come back every turn, the same F063 shape;
  - anything fails: fail open, exit 0, nothing printed.

This hook is separate from the completion gate (hooks/pre-completion-verify.py), which
it imports only for its scope test; when the gate fires is unchanged. Its block is still
seen by the gate: Claude Code records it as a meta "Stop hook feedback" message, and the
gate's verdict reader skips such records (_is_hook_feedback) — before that fix, an
upkeep block landing after the gate's checklist lost the gate's verdict event.

Headless runs: the check fires under `claude -p` too (seen in a live trial, 2026-11-12,
entrypoint sdk-cli). A long headless run in a Soul project with a cursor is blocked once
per GROWTH_TOKENS, and its final result text becomes the refresh line. Measurement arms
turn it off with `upkeep: off`, or run without the plugin.
Codex is not wired: hooks/codex.py reads no transcripts by design, and where Codex
records the context size has not been checked (operations/codex.md says what a Codex
session does instead). Fence: hooks/test_upkeep.py.
"""

import hashlib
import importlib.util
import json
import os
import re
import sys
import tempfile

GROWTH_TOKENS = 50000  # the owner's "about 50,000 tokens" (A032, open question 2)
CURSOR = os.path.join(".soul", "handoff.md")
ANSWERS = os.path.join(".soul", "init.md")  # tools/init-status.py's answers file
_WRITE_TOOLS = {"Write", "Edit", "MultiEdit"}
# tools/init-status.py's LINE_RE, unchanged: the two must read a line the same way.
_LINE_RE = re.compile(r"^([A-Za-z][\w-]*):[ \t]+(.*?)(?:[ \t]+(\d{4}-\d{2}-\d{2}))?[ \t]*$")
_MARK = "[Soul upkeep · SOUL-A032]"
_HERE = os.path.dirname(os.path.abspath(__file__))


def _gate():
    spec = importlib.util.spec_from_file_location(
        "soul_completion_scope", os.path.join(_HERE, "pre-completion-verify.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def upkeep_answer(cwd):
    """The recorded `upkeep:` value, stripped and lower-cased, or None when unanswered.

    Same rule as init-status.py's read_answers: the first line of a key wins.
    """
    try:
        with open(os.path.join(cwd, ANSWERS), encoding="utf-8", errors="replace") as fh:
            for ln in fh.read().splitlines():
                m = _LINE_RE.match(ln)
                if m and m.group(1) == "upkeep" and m.group(2):
                    return m.group(2).strip().lower()
    except OSError:
        pass
    return None


def _context_size(rec):
    usage = (rec.get("message") or {}).get("usage") or {}
    total = 0
    for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"):
        v = usage.get(k)
        if isinstance(v, int):
            total += v
    return total


def _writes_cursor(rec, cwd, cursor_real):
    for b in (rec.get("message") or {}).get("content") or []:
        if not (isinstance(b, dict) and b.get("type") == "tool_use"
                and b.get("name") in _WRITE_TOOLS):
            continue
        path = (b.get("input") or {}).get("file_path")
        if isinstance(path, str) and path:
            if os.path.realpath(os.path.join(cwd, path)) == cursor_real:
                return True
    return False


def read_transcript(path, cwd, cursor_real):
    """Main-thread events, in file order: ("size", line, tokens) | ("compact", line) |
    ("write", line, tokens). Only lines that can matter are parsed."""
    events = []
    with open(path, encoding="utf-8", errors="ignore") as fh:
        for n, ln in enumerate(fh):
            if '"compact_boundary"' in ln:
                kind = "compact"
            elif '"usage"' in ln and '"assistant"' in ln:
                kind = "size"
            else:
                continue
            try:
                rec = json.loads(ln)
            except ValueError:
                continue
            if not isinstance(rec, dict) or rec.get("isSidechain"):
                continue
            if kind == "compact":
                if rec.get("type") == "system" and rec.get("subtype") == "compact_boundary":
                    events.append(("compact", n, 0))
                continue
            if rec.get("type") != "assistant":
                continue
            size = _context_size(rec)
            if not size:
                continue  # a synthetic or failed reply: no reading
            wrote = "handoff" in ln and _writes_cursor(rec, cwd, cursor_real)
            events.append(("write" if wrote else "size", n, size))
    return events


def staleness(events, since_line=-1):
    """(reason, tokens, last_line) or (None, ...) for events after the last cursor write.

    since_line: a line this hook already blocked at; counts as a new start, like a write.
    reason is "compact", "growth" or None; tokens is the growth since the start.
    """
    start = since_line
    for kind, n, _ in events:
        if kind == "write" and n > start:
            start = n
    after = [e for e in events if e[1] > start]
    last_line = events[-1][1] if events else -1
    if any(kind == "compact" for kind, _, _ in after):
        return "compact", 0, last_line
    sizes = [e for e in events if e[0] != "compact"]
    if not sizes:
        return None, 0, last_line
    before = [e for e in sizes if e[1] <= start]
    base = before[-1][2] if before else sizes[0][2]
    grown = sizes[-1][2] - base
    return ("growth" if grown >= GROWTH_TOKENS else None), max(grown, 0), last_line


def _state_path(transcript_path):
    h = hashlib.sha1(os.path.abspath(transcript_path).encode("utf-8")).hexdigest()[:12]
    return os.path.join(tempfile.gettempdir(), "soul-upkeep-{}".format(h))


def _read_state(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return int(fh.read().strip())
    except (OSError, ValueError):
        return -1


def _write_state(path, line):
    """True when the block was remembered."""
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(str(line))
        return True
    except OSError:
        return False


def _reason(why, tokens, answer):
    what = ("a summary (compaction) happened since it was last written"
            if why == "compact" else
            "about {}k tokens of new conversation since it was last written"
            .format(tokens // 1000))
    text = ("{} The handoff cursor (.soul/handoff.md) is stale: {}. Refresh it now with "
            "/soul-handoff (it runs on its own here; no need to ask), tell the owner in one "
            "line, then stop.".format(_MARK, what))
    if answer is None:
        text += (" The owner has not chosen yet whether upkeep runs on its own: add to "
                 "that line \"to turn this off: /soul-init revisit upkeep\".")
    return text


def _applies(cwd):
    """True when this project is Soul-governed, has a cursor, and upkeep is not off."""
    if not _gate()._is_soul_project(cwd):
        return False
    if not os.path.isfile(os.path.join(cwd, CURSOR)):
        return False
    return upkeep_answer(cwd) != "off"


def stop(data):
    if data.get("stop_hook_active"):
        return None
    cwd = data.get("cwd")
    if not isinstance(cwd, str) or not os.path.isdir(cwd) or not _applies(cwd):
        return None
    transcript = data.get("transcript_path")
    if not isinstance(transcript, str) or not os.path.isfile(transcript):
        return None
    state = _state_path(transcript)
    events = read_transcript(transcript, cwd, os.path.realpath(os.path.join(cwd, CURSOR)))
    why, tokens, last_line = staleness(events, _read_state(state))
    if not why or not _write_state(state, last_line):
        return None  # unremembered, it would block again every turn (F063)
    return {"decision": "block", "reason": _reason(why, tokens, upkeep_answer(cwd))}


def compact(data):
    cwd = data.get("cwd")
    if not isinstance(cwd, str) or not os.path.isdir(cwd) or not _applies(cwd):
        return None
    return {"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": (
            "{} A summary just happened. Before other work, re-read .soul/handoff.md "
            "(contract rule 6), then refresh it with /soul-handoff (it runs on its own "
            "here) and tell the owner in one line.".format(_MARK)),
    }}


def main(argv):
    try:
        data = json.load(sys.stdin)
        if not isinstance(data, dict):
            return 0
        out = compact(data) if "--compact" in argv else stop(data)
        if out:
            print(json.dumps(out))
    except Exception:
        pass  # fail open: upkeep is a reminder, never a reason to hold a stop
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
