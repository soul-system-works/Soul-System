#!/usr/bin/env python3
"""Re-run a delegated plan step's "Done when" check and record what was observed.

When a session hands a plan step to another model — a subagent, a local model
(`ollama launch claude -- -p`), `codex exec` — the worker's report is a claim, not
evidence. The main session never takes a worker's word: it re-runs the step's check
itself, here, and the result goes to the project event sink as one
soul.delegation.checked record (SOUL-I066). The CHECK is observed — this tool ran
it and saw the exit code — so it is marked `observed: true`. A REVIEW verdict
(a diff-reviewer pass, say) is handed in by the model, never seen by the tool, so
it is marked `self_reported: true`, the same honesty the completion gate's verdict
event keeps. The gate's verdict event then summarises these records per session.

  record --step S --worker TIER:TOOL[:MODEL] --check CMD   run CMD, record the result
         [--reviewer TOOL[:MODEL]] [--review-verdict pass|fail]
         [--cwd DIR] [--project DIR] [--timeout SECS]
  list [--project DIR] [--session ID] [--json]             show recorded checks

Two directories, kept apart: --cwd is only where the check RUNS (default: here);
--project is where the record GOES. Without --project, the project is found by
walking up from the recorder's own working directory — the session's directory,
never --cwd — to witness.md or .soul/witness.md, and, when that directory is in a
git worktree with neither, the same walk from the main worktree's root. So a check
run in a linked worktree that tracks its own copy of the record still records to
the session's project. This is narrower than the gate's scoping, which also accepts
CLAUDE.md/AGENTS.md markers. No project found means not a Soul project: the check
still runs and reports, but nothing is recorded — the hook likewise never creates
.soul/ outside a Soul project. With $SOUL_EVENT_LOG set the record goes there
regardless; otherwise to <project>/.soul/events.jsonl, the one
hooks/pre-completion-verify.py writes.

record exits 0 when the check passed, 1 when it failed, 2 on a timeout, a usage
error or a check that could not be started (those two record nothing). The default
--timeout is 540 s, under the Claude Code Bash tool's 600 s foreground cap, so the
recorder finishes (and records the timeout) before the tool call is cut off. Killed
by SIGTERM/SIGINT/SIGHUP, it kills the check's whole process group first, records
nothing and exits 128+signal; a signal the caller already ignores (nohup, a
background job) stays ignored.

POSIX only (Linux, macOS, WSL): `shell=True` runs the check under /bin/sh, and the
cleanup that keeps a timed-out or abandoned check from outliving the tool is a
process-group kill: nothing in the check's process group outlives the tool. A
grandchild that left the group (setsid) or a recorder killed by SIGKILL is outside
that promise. On Windows the tool refuses to run (exit 2).
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone

EVENT_TYPE = "soul.delegation.checked"
TIERS = ("deep", "routine", "review")
TAIL_MAX = 300
TAIL_READ = 65536  # bytes read from the end of the output file for the tail
STORES = ("witness.md", os.path.join(".soul", "witness.md"))
SIGNALS = tuple(getattr(signal, n) for n in ("SIGTERM", "SIGINT", "SIGHUP")
                if hasattr(signal, n))


class Killed(Exception):
    """The recorder got a termination signal while the check ran."""

    def __init__(self, signum):
        super().__init__(signum)
        self.signum = signum


def _walk_up(start):
    d = os.path.abspath(start)
    while True:
        if any(os.path.exists(os.path.join(d, s)) for s in STORES):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def _main_worktree_root(start):
    """Parent of `git rev-parse --git-common-dir` — the main worktree's root when
    `start` is in a linked worktree (and the repo's own root otherwise). None
    outside git or on any git error."""
    try:
        out = subprocess.run(["git", "rev-parse", "--git-common-dir"], cwd=start,
                             stdin=subprocess.DEVNULL, capture_output=True, text=True,
                             timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    common = out.stdout.strip()
    if out.returncode != 0 or not common:
        return None
    return os.path.dirname(os.path.abspath(os.path.join(start, common)))


def find_project(start):
    """The Soul project a recorder started in `start` records to, or None (see
    docstring)."""
    found = _walk_up(start)
    if found:
        return found
    root = _main_worktree_root(start)
    return _walk_up(root) if root else None


def sink_path(project):
    """$SOUL_EVENT_LOG, else <project>/.soul/events.jsonl; None when neither exists."""
    env = os.environ.get("SOUL_EVENT_LOG")
    if env:
        return env
    return os.path.join(project, ".soul", "events.jsonl") if project else None


def resolve_project(args, ap):
    if args.project:
        project = os.path.abspath(args.project)
        if not os.path.isdir(project):
            ap.error("no directory at --project {}".format(args.project))
        return project
    return find_project(os.getcwd())  # the session's directory, never --cwd


def parse_worker(text):
    """TIER:TOOL[:MODEL] -> dict. MODEL keeps any further colons (`qwen3:32b`)."""
    parts = text.split(":", 2)
    if len(parts) < 2 or parts[0] not in TIERS or not parts[1].strip():
        raise ValueError("--worker must be TIER:TOOL[:MODEL] with TIER one of {}, got {!r}"
                         .format("|".join(TIERS), text))
    model = parts[2].strip() if len(parts) == 3 else ""
    return {"tier": parts[0], "tool": parts[1].strip(), "model": model or None}


def parse_reviewer(text):
    tool, _, model = text.partition(":")
    if not tool.strip():
        raise ValueError("--reviewer must be TOOL[:MODEL], got {!r}".format(text))
    return {"tool": tool.strip(), "model": model.strip() or None}


def last_line(output):
    for line in reversed((output or "").splitlines()):
        if line.strip():
            return line.strip()[:TAIL_MAX]
    return ""


def _kill_group(pgid):
    try:
        os.killpg(pgid, signal.SIGKILL)
    except OSError:
        pass  # group already empty


def _on_signal(signum, frame):
    # Ignore further signals first: a second SIGTERM must not interrupt the cleanup
    # this exception starts. record()'s finally restores the previous handlers.
    for s in SIGNALS:
        signal.signal(s, signal.SIG_IGN)
    raise Killed(signum)


def _unblock_in_child():
    # The parent blocks SIGNALS around Popen; a signal mask survives fork and exec,
    # so the check must start with them unblocked or it could not be stopped by them.
    signal.pthread_sigmask(signal.SIG_UNBLOCK, SIGNALS)


def run_check(command, cwd, timeout):
    """Run `command` through the shell; return (exit_code | None, timed_out, tail).

    Output goes to a temp file, not a pipe: with a pipe, a background child still
    holding it made a passing shell look like a timeout, and a grandchild that left
    the process group hung the read after the kill. The shell's own exit status is
    the result (wait, not EOF). It runs in its own process group, killed in the
    finally whatever happened — timeout, signal, or a clean exit leaving children —
    so nothing in the check's process group outlives the tool. The termination
    signals are blocked while Popen forks and execs and unblocked once `proc` is
    set, so a signal landing mid-spawn is delivered after the finally can see the
    child. stdin is /dev/null so a check that reads stdin cannot wait on the
    caller's terminal. Popen's OSError propagates.
    """
    with tempfile.TemporaryFile() as out:
        proc = None
        try:
            mask = signal.pthread_sigmask(signal.SIG_BLOCK, SIGNALS)
            try:
                proc = subprocess.Popen(command, shell=True, cwd=cwd,
                                        stdin=subprocess.DEVNULL, stdout=out,
                                        stderr=subprocess.STDOUT, start_new_session=True,
                                        preexec_fn=_unblock_in_child)
            finally:
                signal.pthread_sigmask(signal.SIG_SETMASK, mask)
            try:
                code, timed_out = proc.wait(timeout=timeout), False
            except subprocess.TimeoutExpired:
                code, timed_out = None, True
        finally:
            if proc is not None:
                _kill_group(proc.pid)
            if proc is not None and proc.returncode is None:
                try:
                    proc.wait(timeout=5)  # reap the killed shell
                except Exception:
                    pass
        size = out.seek(0, os.SEEK_END)
        out.seek(max(0, size - TAIL_READ))
        tail = last_line(out.read().decode("utf-8", "replace"))
    return code, timed_out, tail


def emit(project, check_dir, payload):
    """Append one CloudEvents v1.0 line — the shape of _emit_event in
    hooks/pre-completion-verify.py, so one reader serves both."""
    sink = sink_path(project)
    event = {
        "specversion": "1.0",
        "id": str(uuid.uuid4()),
        "source": "urn:soul:project:{}".format(
            os.path.basename(os.path.abspath(project or check_dir)) or "unknown"),
        "type": EVENT_TYPE,
        "time": datetime.now(timezone.utc).isoformat(),
        "datacontenttype": "application/json",
        "data": payload,
    }
    session_id = os.environ.get("CLAUDE_CODE_SESSION_ID")
    if session_id:
        event["genaisessionid"] = session_id
    os.makedirs(os.path.dirname(os.path.abspath(sink)), exist_ok=True)
    with open(sink, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(event) + "\n")


def record(args, ap):
    try:
        worker = parse_worker(args.worker)
        reviewer = parse_reviewer(args.reviewer) if args.reviewer else None
    except ValueError as e:
        ap.error(str(e))
    if args.review_verdict and not reviewer:
        ap.error("--review-verdict needs --reviewer")
    if not args.check.strip():
        ap.error("--check is blank")
    if not args.timeout > 0:  # also refuses nan
        ap.error("--timeout must be > 0, got {:g}".format(args.timeout))
    cwd = os.path.abspath(args.cwd)
    if not os.path.isdir(cwd):
        ap.error("no directory at --cwd {}".format(args.cwd))
    project = resolve_project(args, ap)

    # Killing the recorder must not orphan the check: turn the signals into an
    # exception so run_check's finally kills the check's process group first. A
    # signal already ignored (nohup, a background job) is left ignored.
    previous = {}
    try:
        for s in SIGNALS:
            if signal.getsignal(s) is not signal.SIG_IGN:
                previous[s] = signal.signal(s, _on_signal)
        exit_code, timed_out, tail = run_check(args.check, cwd, args.timeout)
    except Killed as k:
        print("killed by signal {} — check stopped, nothing recorded".format(k.signum),
              file=sys.stderr)
        return 128 + k.signum
    except OSError as e:
        print("error: could not start the check ({}) — nothing recorded".format(e),
              file=sys.stderr)
        return 2
    finally:
        for s, handler in previous.items():
            if handler is not None:  # None: not set from Python; nothing to restore
                signal.signal(s, handler)

    passed = not timed_out and exit_code == 0
    review = None
    if reviewer:
        review = dict(reviewer, verdict=args.review_verdict, self_reported=True)
    payload = {
        "step": args.step,
        "worker": worker,
        "check": {"command": args.check, "exit_code": exit_code, "passed": passed,
                  "timed_out": timed_out, "tail": tail, "observed": True},
        "review": review,
    }
    # The check's result is the point; a sink that cannot be written must not hide
    # it or change the exit status — warn and carry on.
    if sink_path(project) is None:
        print("warning: not a Soul project — result not recorded", file=sys.stderr)
    else:
        try:
            emit(project, cwd, payload)
        except Exception as e:  # noqa: BLE001 — fail-safe emission
            print("warning: delegation record not written to {}: {}"
                  .format(sink_path(project), e), file=sys.stderr)

    if timed_out:
        print("FAIL (timeout {:g}s) — {}".format(args.timeout, tail))
        return 2
    print("{} (exit {}) — {}".format("PASS" if passed else "FAIL", exit_code, tail))
    return 0 if passed else 1


def read_records(sink, session=None):
    """soul.delegation.checked events from the sink; malformed lines are skipped.
    Only a regular file is read — a FIFO as $SOUL_EVENT_LOG would block the open,
    the same guard as the hook's _delegation_counts."""
    if not sink or not os.path.isfile(sink):
        return []
    try:
        with open(sink, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()
    except OSError:
        return []
    out = []
    for line in lines:
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if not isinstance(ev, dict) or ev.get("type") != EVENT_TYPE:
            continue
        if session and ev.get("genaisessionid") != session:
            continue
        out.append(ev)
    return out


def list_records(args, ap):
    sink = sink_path(resolve_project(args, ap))
    if sink is None:
        print("warning: not a Soul project — no record to list", file=sys.stderr)
    records = read_records(sink, args.session)
    if args.json:
        print(json.dumps(records, indent=2))
        return 0
    if not records:
        print("no delegation records")
        return 0
    for ev in records:
        data = ev.get("data") or {}
        w = data.get("worker") or {}
        who = ":".join(p for p in (w.get("tier"), w.get("tool"), w.get("model")) if p)
        ok = "PASS" if (data.get("check") or {}).get("passed") else "FAIL"
        print("{}  {}  {}  {}".format(ev.get("time", "?"), ok, who, data.get("step", "")))
    return 0


def main():
    if os.name == "nt":
        print("error: delegation-check is POSIX-only (Linux, macOS, WSL) — it needs "
              "/bin/sh and process groups", file=sys.stderr)
        return 2
    # A check's tail can hold anything; printing it under a narrow console encoding
    # (cp1252) must not crash the report.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(errors="replace")
            except Exception:
                pass
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record", help="run a step's check and record the result")
    r.add_argument("--step", required=True, help="the plan step's text")
    r.add_argument("--worker", required=True, help="TIER:TOOL[:MODEL], TIER = deep|routine|review")
    r.add_argument("--check", required=True, help="the step's Done-when shell command")
    r.add_argument("--reviewer", help="TOOL[:MODEL] that reviewed the worker's output")
    r.add_argument("--review-verdict", choices=("pass", "fail"))
    r.add_argument("--cwd", default=".", help="where the check runs (only that)")
    r.add_argument("--project", help="where the record goes (default: found by walking "
                   "up from the recorder's own working directory)")
    r.add_argument("--timeout", type=float, default=540,
                   help="seconds before the check is stopped (default 540, under the "
                   "Bash tool's 600 s foreground cap)")
    s = sub.add_parser("list", help="show recorded delegation checks")
    s.add_argument("--project", help="the project whose record to read (default: found "
                   "from the working directory)")
    s.add_argument("--session", help="only records with this genaisessionid")
    s.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.cmd == "record":
        return record(args, r)
    return list_records(args, s)


if __name__ == "__main__":
    sys.exit(main())
