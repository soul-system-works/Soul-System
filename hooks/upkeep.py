#!/usr/bin/env python3
"""Soul upkeep hook: tells a session when its handoff cursor needs upkeep (SOUL-A032).

Three modes, all Claude Code only:

  upkeep.py              Stop hook. When one or more upkeep reasons are due, block the
                         stop once with {"decision": "block", "reason": ...}: one line
                         per due reason, highest first, then one tail — tell the owner in
                         one line that starts with the sun mark; the reply before this
                         stays the answer. Silent otherwise.
  upkeep.py --compact    SessionStart hook, matcher `compact`. One line of context: a
                         summary just happened, re-read the cursor (the Stop check decides
                         whether it also needs a refresh).
  upkeep.py --start      SessionStart hook, matcher `startup|resume`. When soul-distill
                         left major Mind changes waiting (.ai/distill/mind-held-*.md),
                         one context line naming them, every session until answered:
                         "a held draft is not a question" — it reached the owner only
                         when a session chose to raise it, and sat for a day and a half
                         (the 2026-11-18 field report; SOUL-243).

The reasons, highest first (SOUL-243: the owner raised the token step to 200,000 as a
backstop "with state triggers" in front of it; the field report and SOUL-I095 named them):
  1. background — an Agent/Task launch, or a Bash command sent to the background, after
     the last cursor write, whose task has not ended by this stop. It dies with the
     session and the cursor does not know it: "the case that actually loses work". A
     launch is the tool_result of that call ("Async agent launched … agentId: ID" /
     "Command running in background with ID: ID"); it ends at a <task-notification> for
     that <task-id> with a final status (completed, failed, killed or stopped — the
     statuses seen in real transcripts; one agent can notify more than once, and any of
     them ends it), in a user record or a queued_command attachment (a notification that
     arrives while the session is busy is recorded only as the attachment), or at a
     TaskStop result for it. Once per cursor write.
  2. stale — the working context grew by GROWTH_TOKENS or more, or a summary came after
     at least SUMMARY_GAP tokens of work, since the cursor was last written (below).
  3. length — the cursor is over CURSOR_MAX_LINES lines. In-place edits keep a cursor
     fresh but never prune it (147 lines became 208 in the field report). At most once
     per calendar day per project.
  4. mind — mind.md (root or .soul/) has a `**Last distilled:** YYYY-MM-DD` stamp and
     MIND_DUE_ENTRIES or more witness entries (an `ID:` line, then a `WHEN:` line that
     starts with the date) are dated after it. The check lived only inside a full
     /soul-handoff, which a session that edits its cursor in place never runs; the Mind
     fell 28 entries behind (field report). No mind.md or no stamp: never. At most once
     per calendar day per project.

Stale, in detail:
  - the working context grew by GROWTH_TOKENS or more. The size is read from the
    transcript's main-thread assistant records, message.usage: input_tokens +
    cache_creation_input_tokens + cache_read_input_tokens. Subagent (isSidechain)
    records are skipped (mind item 7). The owner chose a size step over a commit count:
    "some agents/processes commit a lot and others not so much" (SOUL-I089, open
    question 2 of A032). Records with no usage, or a zero total, are skipped.
  - a summary (compaction): a {"type": "system", "subtype": "compact_boundary"} record,
    when at least SUMMARY_GAP tokens of work came between the cursor write and the
    summary. A summary minutes after a fresh refresh asked for a second one with almost
    nothing new (an adopting project's upstream note, 2026-11-16); the owner set the
    gap: half the refresh step or 50,000 tokens, whichever is higher.

"Last written" is the later of two: the newest Write / Edit / MultiEdit tool call in THIS
transcript whose file_path resolves to the cursor, and the last stop at which the
cursor's CONTENT differed from the sha256 this hook stored at the stop before. The
content check is the field report's first fix: a session that updated the cursor four
times by a script was stopped for a "stale" cursor minutes old. A content change is
placed at the stop that sees it. No clocks are read: the WSL clock can pause, so a
file's mtime cannot be lined up with transcript times. A cursor written by an earlier
session (the usual case) leaves no such call and no stored hash, and growth is counted
from the session's first assistant record, so the fixed start-up load (contract,
CLAUDE.md, tools) is not counted as conversation.

When the owner has not answered whether upkeep runs on its own, a block carries "to turn
this off: /soul-init revisit upkeep". The third such block in one session appends
`upkeep: on <date>` to .soul/init.md (tools/init-status.py's line format) and says so;
the hint then stops. The owner "answered it in words more than once ('continue
autonomously'), but nothing records that" (field report; SOUL-243).

Silent, always, when:
  - stop_hook_active is set (this stop follows a block — never loop; it only stores
    the cursor's hash, so the obeyed block's write is not seen again at the next stop);
  - the project is not Soul-governed (the completion gate's own scope test);
  - no cursor exists yet. A project that has never written one has not taken up the
    handoff; the first /soul-handoff (or /soul-init) starts it, and nagging before that
    would block every long session in a project that never asked for a cursor;
  - `.soul/init.md` holds `upkeep: off` (the owner's opt-out, asked once by /soul-init;
    no line means on — the default the owner chose, A032 open question 3). The value
    is read as init-status.py reads it (its LINE_RE, first line of the key wins,
    stripped and lower-cased); only `off` turns it off — anything else, `no` included,
    is "not understood": init-status asks again and this hook stays on. It silences
    every reason and the --start line;
  - the due reasons already fired: every block is remembered BEFORE it is returned
    (small files in the temp folder: one per transcript — the stale point, the cursor
    hash, the write a background block fired for, the hint count — and one per project,
    keyed by the cursor's real path — the dates the per-day reasons fired). A stale
    block counts as a new start, so an ignored block does not come back every turn —
    only after another GROWTH_TOKENS or another summary. F063 and mind item 5 are the
    reason: a Stop hook that fires every turn gets switched off. If that file cannot be
    written, the hook does not block at all: an unremembered block would come back every
    turn, the same F063 shape (a per-day reason whose project file cannot be written is
    dropped, the rest still block). The files sit in a per-user 0700 folder in the temp
    folder; a folder another user could write is not trusted, and the files move to
    ${XDG_CACHE_HOME:-~/.cache}/soul-upkeep (same check) rather than let another user
    silence the block through them. Only when both folders fail is there nowhere to
    remember, and then the hook does not block (F063);
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
Codex: the Stop check is not wired — hooks/codex.py reads no transcripts by design, and
where Codex records the context size has not been checked (operations/codex.md says what
a Codex session does instead). The --start line needs no transcript, so hooks/codex.py
adds held_note() to its own SessionStart context. Fence: hooks/test_upkeep.py.
"""

import hashlib
import importlib.util
import json
import os
import re
import stat
import sys
import tempfile
import time

# The owner's step, for every project. SOUL-239 raised 50,000 (A032 open question 2) to
# 100,000; SOUL-243 raised it to 200,000 "as the backstop with state triggers" — the
# background, length and Mind reasons below — after a field report that a token step
# counts reading as much as doing ("it halves the interruptions of a reading-heavy
# session").
GROWTH_TOKENS = 200000
SUMMARY_GAP = max(GROWTH_TOKENS // 2, 50000)  # see the docstring: a summary soon after a write
# The cursor size the handoff skill's own check names ("about 150"); the field report's
# cursor grew from 147 to 208 by in-place edits (SOUL-243).
CURSOR_MAX_LINES = 150
# soul-distill's growth signal: "~15+ new witness entries since the Last-distilled stamp".
MIND_DUE_ENTRIES = 15
# Blocks carrying the turn-off hint before `upkeep: on` is recorded (field report: "After
# three refresh lines with the reminder and no opt-out, record `upkeep: on`").
HINTS_BEFORE_RECORDING = 3
CURSOR = os.path.join(".soul", "handoff.md")
ANSWERS = os.path.join(".soul", "init.md")  # tools/init-status.py's answers file
HELD_DIR = os.path.join(".ai", "distill")  # soul-distill's mind-held-<date>.md
_WRITE_TOOLS = {"Write", "Edit", "MultiEdit"}
_LAUNCH_TOOLS = {"Agent", "Task"}
_STOP_TOOLS = {"TaskStop", "KillShell", "KillBash"}
_ENDED = {"completed", "failed", "killed", "stopped"}  # seen in real transcripts
# tools/init-status.py's LINE_RE, unchanged: the two must read a line the same way.
_LINE_RE = re.compile(r"^([A-Za-z][\w-]*):[ \t]+(.*?)(?:[ \t]+(\d{4}-\d{2}-\d{2}))?[ \t]*$")
# tools/init-status.py's HEADER, for an answers file this hook creates.
_ANSWERS_HEADER = ("# /soul-init's remembered answers (tools/init-status.py).\n"
                   "# Delete a line, or run `init-status.py revisit`, to be asked again.\n")
_AGENT_ID_RE = re.compile(r"agentId: ([\w-]+)")
_BASH_ID_RE = re.compile(r"^\s*Command running in background with ID: ([\w-]+)")
_NOTICE_RE = re.compile(r"<task-notification>(.*?)</task-notification>", re.S)
_TASK_ID_RE = re.compile(r"<task-id>\s*([^<\s]+)\s*</task-id>")
_STATUS_RE = re.compile(r"<status>\s*(\w+)\s*</status>")
_STAMP_RE = re.compile(r"^\*\*Last distilled:\*\*\s*(\d{4}-\d{2}-\d{2})", re.M)
_WHEN_RE = re.compile(r"^ID:[^\n]*\n[ \t]*WHEN:[ \t]*(\d{4}-\d{2}-\d{2})", re.M)
_HELD_RE = re.compile(r"^mind-held-.*\.md$")
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


def _record_on(cwd, today):
    """Append `upkeep: on <today>` to .soul/init.md in init-status.py's line format
    (its _line: key padded to 14, value to 12). True when it now reads as on."""
    path = os.path.join(cwd, ANSWERS)
    line = "{} {} {}".format("upkeep:".ljust(14), "on".ljust(12), today)
    try:
        try:
            with open(path, encoding="utf-8", newline="") as fh:
                old = fh.read()
        except FileNotFoundError:
            old = None
        with open(path, "a", encoding="utf-8", newline="") as fh:
            if old is None:
                fh.write(_ANSWERS_HEADER + line + "\n")
            else:
                nl = "\r\n" if "\r\n" in old else "\n"
                fh.write(("" if not old or old.endswith("\n") else nl) + line + nl)
    except OSError:
        return False
    return upkeep_answer(cwd) == "on"


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


def _text(content):
    """The text of a message or tool_result content: a string, or its text blocks."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text") for b in content if isinstance(b, dict)
                         and b.get("type") == "text" and isinstance(b.get("text"), str))
    return ""


def _ended_ids(text):
    out = []
    for body in _NOTICE_RE.findall(text):
        # Claude Code's resume summary lists every task that did not finish in ONE
        # notification (several task-ids, status stopped): each of them has ended.
        status = _STATUS_RE.search(body)
        if status and status.group(1).lower() in _ENDED:
            out.extend(_TASK_ID_RE.findall(body))
    return out


def read_transcript(path, cwd, cursor_real):
    """(events, last line number). Main-thread events, in file order:
    ("size", line, tokens) | ("compact", line, 0) | ("write", line, tokens) |
    ("launch", line, (task id, description)) | ("end", line, task id).
    Only lines that can matter are parsed."""
    events, calls, n = [], {}, -1
    with open(path, encoding="utf-8", errors="ignore") as fh:
        for n, ln in enumerate(fh):
            if '"compact_boundary"' in ln:
                kind = "compact"
            elif '"assistant"' in ln and ('"usage"' in ln or '"tool_use"' in ln):
                kind = "size"
            elif "<task-notification>" in ln:
                kind = "notice"
            elif '"tool_result"' in ln and ("agentId" in ln or "running in background" in ln
                                            or "stopped task" in ln or "is not running" in ln):
                kind = "result"
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
            if kind == "notice":
                # Only a delivered notification: a user message, or one queued while the
                # session was busy. Tool output that merely quotes one does not count.
                if rec.get("type") == "user":
                    text = _text((rec.get("message") or {}).get("content"))
                elif rec.get("type") == "attachment":
                    att = rec.get("attachment") or {}
                    text = (_text(att.get("prompt"))
                            if att.get("type") == "queued_command" else "")
                else:
                    text = ""
                events.extend(("end", n, tid) for tid in _ended_ids(text))
                if '"tool_result"' not in ln:
                    continue
                kind = "result"  # a tool result that quotes one is still read as a result
            if kind == "result":
                if rec.get("type") != "user":
                    continue
                for b in (rec.get("message") or {}).get("content") or []:
                    if not (isinstance(b, dict) and b.get("type") == "tool_result"):
                        continue
                    name, inp = calls.get(b.get("tool_use_id"), (None, {}))
                    text = _text(b.get("content"))
                    desc = inp.get("description") if isinstance(
                        inp.get("description"), str) else ""
                    m = None
                    if name in _LAUNCH_TOOLS and "Async agent launched" in text:
                        m = _AGENT_ID_RE.search(text)
                    elif name == "Bash":
                        m = _BASH_ID_RE.match(text)
                    if m:
                        events.append(("launch", n, (m.group(1), desc)))
                    elif name in _STOP_TOOLS and ("stopped task" in text
                                                  or "is not running" in text):
                        tid = inp.get("task_id") or inp.get("shell_id")
                        if isinstance(tid, str) and tid:
                            events.append(("end", n, tid))
                continue
            if rec.get("type") != "assistant":
                continue
            for b in (rec.get("message") or {}).get("content") or []:
                if (isinstance(b, dict) and b.get("type") == "tool_use"
                        and b.get("name") in (_LAUNCH_TOOLS | _STOP_TOOLS | {"Bash"})):
                    inp = b.get("input")
                    calls[b.get("id")] = (b.get("name"), inp if isinstance(inp, dict) else {})
            size = _context_size(rec)
            if not size:
                continue  # a synthetic or failed reply: no reading
            wrote = "handoff" in ln and _writes_cursor(rec, cwd, cursor_real)
            events.append(("write" if wrote else "size", n, size))
    return events, n


def staleness(events, since_line=-1):
    """(reason, tokens, last_line) or (None, ...) for events after the last cursor write.

    since_line: a line this hook already blocked at, or where it saw the cursor's
    content change; counts as a new start, like a write.
    reason is "compact", "growth" or None; tokens is the growth since the start.
    """
    events = [e for e in events if e[0] in ("size", "write", "compact")]
    start = since_line
    for kind, n, _ in events:
        if kind == "write" and n > start:
            start = n
    after = [e for e in events if e[1] > start]
    last_line = events[-1][1] if events else -1
    sizes = [e for e in events if e[0] != "compact"]
    before = [e for e in sizes if e[1] <= start]
    base = before[-1][2] if before else (sizes[0][2] if sizes else None)
    # Growth is summed per stretch between summaries: a summary shrinks the context, so
    # the readings after it start low again.
    done, seg, latest = 0, base, base
    for kind, _, tok in after:
        if kind == "compact":
            grown = done + (max(latest - seg, 0) if seg is not None else 0)
            if grown >= SUMMARY_GAP:
                return "compact", 0, last_line
            done, seg, latest = grown, None, None
            continue
        if seg is None:
            seg = tok
        latest = tok
    if base is None and not done and seg is None:
        return None, 0, last_line
    grown = done + (max(latest - seg, 0) if seg is not None else 0)
    return ("growth" if grown >= GROWTH_TOKENS else None), grown, last_line


def background(events, write_point):
    """[(task id, description)] launched after write_point and not ended, in order."""
    ended = {v for k, _, v in events if k == "end"}
    out, seen = [], set()
    for kind, n, v in events:
        if kind == "launch" and n > write_point and v[0] not in ended and v[0] not in seen:
            seen.add(v[0])
            out.append(v)
    return out


def _store(cwd, name):
    """A record store at the project root or in .soul/, wherever it is."""
    for p in (os.path.join(cwd, name), os.path.join(cwd, ".soul", name)):
        if os.path.isfile(p):
            return p
    return None


def mind_due(cwd):
    """(entries, stamp date) when MIND_DUE_ENTRIES or more witness entries are dated after
    the Mind's `Last distilled` date; else None (no mind.md, no stamp, too few)."""
    mind, witness = _store(cwd, "mind.md"), _store(cwd, "witness.md")
    if not mind or not witness:
        return None
    try:
        with open(mind, encoding="utf-8", errors="replace") as fh:
            stamp = _STAMP_RE.search(fh.read())
        if not stamp:
            return None
        with open(witness, encoding="utf-8", errors="replace") as fh:
            dates = _WHEN_RE.findall(fh.read())
    except OSError:
        return None
    count = sum(1 for d in dates if d > stamp.group(1))
    return (count, stamp.group(1)) if count >= MIND_DUE_ENTRIES else None


def _trusted_dir(d):
    """d, made 0700 if missing, when it is a real folder owned by this user with no
    group or other bits; else None. Same check as hooks/secret-guard.py's _state_dir."""
    try:
        os.makedirs(d, mode=0o700, exist_ok=True)
        st = os.lstat(d)
        if (not stat.S_ISDIR(st.st_mode) or st.st_uid != os.getuid()
                or st.st_mode & 0o077):
            return None
        return d
    except OSError:
        return None


def _state_dir():
    """Where the remembered block lives: a per-user 0700 folder in the temp folder;
    if that one cannot be trusted, ${XDG_CACHE_HOME:-~/.cache}/soul-upkeep under the
    same check; None when neither can, and then the hook does not block (F063).

    The remembered block used to be $TMPDIR/soul-upkeep-<hash>, a name any local user
    could compute and create first: a planted line number, or a file this user cannot
    write, silenced the hook's one block. A per-user temp folder another user made
    first (or one on a filesystem without Unix modes) fails the check; the home cache
    keeps the block remembered there instead of nagging every turn or going silent.
    Found in the 2026-11-16 cleanup audit; no incident. Native Windows has no getuid,
    and its temp folder is already per-user, so it keeps the plain folder."""
    if not hasattr(os, "getuid"):
        return tempfile.gettempdir()
    d = _trusted_dir(os.path.join(tempfile.gettempdir(),
                                  "soul-upkeep-{}".format(os.getuid())))
    if d is not None:
        return d
    cache = os.environ.get("XDG_CACHE_HOME") or os.path.join(
        os.path.expanduser("~"), ".cache")
    return _trusted_dir(os.path.join(cache, "soul-upkeep"))


def _state_path(key, prefix="soul-upkeep-"):
    """None when no state folder can be trusted: then nothing can be remembered.
    key: the transcript path (per session), or the cursor's real path (per project,
    prefix "soul-upkeep-p-")."""
    d = _state_dir()
    if d is None:
        return None
    h = hashlib.sha1(os.path.abspath(key).encode("utf-8")).hexdigest()[:12]
    return os.path.join(d, "{}{}".format(prefix, h))


def _read_state(path):
    """The session's remembered state. line: where a stale block last fired; hash: the
    cursor's sha256 at the last stop; written: where a content change was seen; bg: the
    write point a background block fired for; hints: blocks that carried the turn-off
    hint. A 3.13.2 file holds a bare line number: read as `line`."""
    st = {"line": -1, "hash": None, "written": -1, "bg": None, "hints": 0}
    if path is None:
        return st
    try:
        with open(path, encoding="utf-8") as fh:
            val = json.loads(fh.read().strip())
    except (OSError, ValueError):
        return st
    if isinstance(val, int) and not isinstance(val, bool):
        st["line"] = val
    elif isinstance(val, dict):
        for k in ("line", "written", "hints"):
            if isinstance(val.get(k), int) and not isinstance(val.get(k), bool):
                st[k] = val[k]
        if isinstance(val.get("hash"), str):
            st["hash"] = val["hash"]
        if isinstance(val.get("bg"), int) and not isinstance(val.get("bg"), bool):
            st["bg"] = val["bg"]
    return st


def _read_days(path):
    """The project's per-day reasons: {"length": date, "mind": date} when each last fired."""
    try:
        with open(path, encoding="utf-8") as fh:
            val = json.loads(fh.read())
        return {k: v for k, v in val.items() if isinstance(v, str)} \
            if isinstance(val, dict) else {}
    except (OSError, ValueError, TypeError):
        return {}


def _write_state(path, value):
    """True when it was remembered."""
    if path is None:
        return False
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(value))
        return True
    except OSError:
        return False


def _reason(items, answer, recorded):
    """One line per due reason (already highest first), then the tail."""
    lines = ["{} The handoff cursor (.soul/handoff.md) needs upkeep:".format(_MARK)]
    for kind, val in items:
        if kind == "background":
            names = ", ".join(d or tid for tid, d in val[:3])
            more = " and {} more".format(len(val) - 3) if len(val) > 3 else ""
            lines.append("- background work is running that the cursor does not mention: "
                         "add a line for it ({}{}).".format(names, more))
        elif kind in ("compact", "growth"):
            what = ("a summary (compaction) happened since it was last written"
                    if kind == "compact" else
                    "about {}k tokens of new conversation since it was last written"
                    .format(val // 1000))
            lines.append("- it is stale: {}. Refresh it with /soul-handoff.".format(what))
        elif kind == "length":
            lines.append("- the cursor is {} lines: delete finished items and flush "
                         "history to the witness log.".format(val))
        elif kind == "mind":
            lines.append("- the Mind is due: run /soul-distill ({} witness entries dated "
                         "after its last distill, {}).".format(*val))
    text = ("Do this now (it runs on its own here; no need to ask), then tell the owner "
            "in one line that starts with \"☀  \". Your reply before this stays the "
            "answer: do not restate, shorten or replace it.")
    if recorded:
        text += (" The owner has not chosen whether upkeep runs on its own, after {} "
                 "reminders: it is now recorded as on in .soul/init.md. Add to that line "
                 "\"upkeep is now recorded as on; /soul-init revisit upkeep changes it\"."
                 .format(HINTS_BEFORE_RECORDING))
    elif answer is None:
        text += (" The owner has not chosen yet whether upkeep runs on its own: add to "
                 "that line \"to turn this off: /soul-init revisit upkeep\".")
    return "\n".join(lines + [text])


def _applies(cwd):
    """True when this project is Soul-governed, has a cursor, and upkeep is not off."""
    if not _gate()._is_soul_project(cwd):
        return False
    if not os.path.isfile(os.path.join(cwd, CURSOR)):
        return False
    return upkeep_answer(cwd) != "off"


def stop(data):
    active = bool(data.get("stop_hook_active"))
    cwd = data.get("cwd")
    if not isinstance(cwd, str) or not os.path.isdir(cwd) or not _applies(cwd):
        return None
    transcript = data.get("transcript_path")
    if not isinstance(transcript, str) or not os.path.isfile(transcript):
        return None
    cursor = os.path.join(cwd, CURSOR)
    cursor_real = os.path.realpath(cursor)
    state_path = _state_path(transcript)
    st = _read_state(state_path)
    events, end_line = read_transcript(transcript, cwd, cursor_real)

    # A: a cursor written any way counts — by content, not only by tool (field report;
    # SOUL-243). The first stop of a session only stores the hash: a cursor from an
    # earlier session is not "written now".
    try:
        with open(cursor, "rb") as fh:
            body = fh.read()
    except OSError:
        body = None
    if body is not None:
        digest = hashlib.sha256(body).hexdigest()
        if st["hash"] is not None and digest != st["hash"]:
            st["written"] = end_line
        st["hash"] = digest
    write_point = max([n for k, n, _ in events if k == "write"] + [st["written"]])
    if active:
        # This stop follows a block: never block here (never loop). Still store the
        # hash the obeyed block just wrote, or the next stop would see a "changed"
        # cursor, put the write past its own turn, and miss that turn's launches and
        # growth (review of 85bb6c4).
        _write_state(state_path, st)
        return None

    due = []
    running = background(events, write_point)
    if running and st["bg"] != write_point:  # once per cursor write
        due.append(("background", running))
        st["bg"] = write_point
    why, tokens, last_line = staleness(events, max(st["line"], st["written"]))
    if why:
        due.append((why, tokens))
        st["line"] = last_line

    # The per-day reasons are per project: a new session the same day is not asked again.
    today = time.strftime("%Y-%m-%d")
    days_path = _state_path(cursor_real, "soul-upkeep-p-")
    days = _read_days(days_path) if days_path else {}
    daily = []
    if body is not None and days.get("length") != today:
        n = len(body.decode("utf-8", "replace").splitlines())
        if n > CURSOR_MAX_LINES:
            daily.append(("length", n))
    if days.get("mind") != today:
        mind = mind_due(cwd)
        if mind:
            daily.append(("mind", mind))
    if daily:
        days.update((k, today) for k, _ in daily)
        if _write_state(days_path, days):
            due.extend(daily)  # unremembered, they would come back every turn (F063)

    answer = upkeep_answer(cwd)
    if due and answer is None:
        st["hints"] += 1
    # Remembered before it is returned; no trusted folder (None) or a failed write:
    # nowhere to remember the block, so no block (F063).
    if not _write_state(state_path, st) or not due:
        return None
    recorded = (answer is None and st["hints"] >= HINTS_BEFORE_RECORDING
                and _record_on(cwd, today))
    return {"decision": "block", "reason": _reason(due, answer, recorded)}


def compact(data):
    cwd = data.get("cwd")
    if not isinstance(cwd, str) or not os.path.isdir(cwd) or not _applies(cwd):
        return None
    return {"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": (
            "{} A summary just happened. Before other work, re-read .soul/handoff.md "
            "(contract rule 6). Refresh it with /soul-handoff only when the Stop check asks "
            "(it does when enough work came between its last write and the summary)."
            .format(_MARK)),
    }}


def _held_count(path):
    """The changes a held file lists: the top-level list items under its heading
    `## Changes` (any case), where soul-distill writes one `- ` line per waiting
    change; None when there is no such heading or it lists none. A looser match
    ("change" anywhere) counted headings like "Unchanged" or "Exchange" (review of
    85bb6c4)."""
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except OSError:
        return None
    inside, items = False, 0
    for ln in lines:
        if not inside:
            inside = bool(re.match(r"^##\s+changes\s*$", ln, re.I))
            continue
        if re.match(r"^#{1,2}\s", ln):
            break
        if re.match(r"^(?:[-*+]|\d+[.)])\s+\S", ln):
            items += 1
    return items or None


def held_note(cwd):
    """The --start line ("☀  N Mind changes wait for your yes: <path>"), or None:
    no held file, not a Soul project, or upkeep off."""
    if not _gate()._is_soul_project(cwd) or upkeep_answer(cwd) == "off":
        return None
    try:
        names = sorted(n for n in os.listdir(os.path.join(cwd, HELD_DIR))
                       if _HELD_RE.match(n))
    except OSError:
        return None
    paths = [os.path.join(HELD_DIR, n) for n in names]
    paths = [p for p in paths if os.path.isfile(os.path.join(cwd, p))]
    if not paths:
        return None
    counts = [_held_count(os.path.join(cwd, p)) for p in paths]
    if all(counts):
        n = sum(counts)
        what = "{} Mind change{} wait{}".format(n, "" if n == 1 else "s",
                                                "s" if n == 1 else "")
    else:
        what = "Mind changes wait"
    return "☀  {} for your yes: {}".format(what, ", ".join(
        p.replace(os.sep, "/") for p in paths))


def start(data):
    cwd = data.get("cwd")
    if not isinstance(cwd, str) or not os.path.isdir(cwd):
        return None
    note = held_note(cwd)
    if not note:
        return None
    return {"hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "{} Tell the owner this line, as it is, in your first reply "
                             "(they wait until the owner answers; soul-distill): {}"
                             .format(_MARK, note),
    }}


def main(argv):
    try:
        data = json.load(sys.stdin)
        if not isinstance(data, dict):
            return 0
        if "--compact" in argv:
            out = compact(data)
        elif "--start" in argv:
            out = start(data)
        else:
            out = stop(data)
        if out:
            print(json.dumps(out))
    except Exception:
        pass  # fail open: upkeep is a reminder, never a reason to hold a stop
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
