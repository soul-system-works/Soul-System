"""Verdict-event test for the completion gate (structured gate result).

FENCE: on the stop after the gate blocks, the hook reads the reply's Verify line
and emits soul.gate.completion.verdict — verified | gap | unreported, always marked
self_reported (the hook never observes verification itself). It must emit nothing
when the block came from another hook, must never block, and a reply listing both
a Verified and a Not-verified line is a gap. The verdict also carries this
session's delegation counts, from observed soul.delegation.checked records only.

Run: python3 hooks/test_verdict.py  (exit 0 = fence holds)
"""

import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import threading
from contextlib import redirect_stderr
from unittest import mock

_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "pre_completion_verify", os.path.join(_HERE, "pre-completion-verify.py")
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
_RECORDER = os.path.join(os.path.dirname(_HERE), "tools", "delegation-check.py")


def _user(text, **meta):
    return {"type": "user", **meta, "message": {"role": "user", "content": text}}


def _say(text):
    return {"type": "assistant", "message": {"role": "assistant",
                                             "content": [{"type": "text", "text": text}]}}


FEEDBACK = _user("Stop hook feedback: [python3 hook]: " + _mod._GATE_MARK
                 + " Shipped + claimed complete this turn — fires at most once per 45 min in this project.",
                 isMeta=True)
OTHER_HOOK = _user("Stop hook feedback: [codex review gate]: please review", isMeta=True)
START = [_user("fix calc.py"), _say("The fix is done.")]

CASES = [
    ("clean Verify line -> verified",
     START + [FEEDBACK, _say("Next: merge.\n— Verify: clean (pytest 12/12)")], "verified"),
    ("GAP Verify line -> gap",
     START + [FEEDBACK, _say("— Verify: GAP → never ran the CLI")], "gap"),
    ("plain register, both lines -> gap",
     START + [FEEDBACK, _say("— Verified: unit tests\n— Not verified: the deploy")], "gap"),
    ("plain register, Verified only -> verified",
     START + [FEEDBACK, _say("— Verified: ran the build and the 3 tests")], "verified"),
    ("no Verify line -> unreported",
     START + [FEEDBACK, _say("Okay, all good.")], "unreported"),
    ("another hook's block -> no event",
     START + [OTHER_HOOK, _say("— Verify: clean (x)")], None),
    ("mid-reply mention without the dash -> unreported",
     START + [FEEDBACK, _say("Inputs:\nverified: mock input only")], "unreported"),
    ("fenced example -> unreported",
     START + [FEEDBACK, _say("Format:\n```\n— Verified: pytest\n```\nok")], "unreported"),
    ("quoted gap line does not override a real verified line",
     START + [FEEDBACK, _say("> — Not verified: <missing>\n— Verified: pytest 4/4")], "verified"),
    ("the gate mark in ordinary user text -> no event",
     START + [_user("Explain " + _mod._GATE_MARK), _say("— Verified: x")], None),
    ("checklist from an earlier turn -> no event",
     START + [FEEDBACK, _say("— Verify: clean (x)"), _user("now the docs"),
              _say("Docs updated.")], None),
]


def _checked(session, passed, observed=True):
    """One soul.delegation.checked line, as tools/delegation-check.py writes it
    (`observed` other than True plants a record the recorder never writes)."""
    check = {"passed": passed}
    if observed is not None:
        check["observed"] = observed
    return json.dumps({"type": "soul.delegation.checked", "genaisessionid": session,
                       "data": {"check": check}})


# SOUL-I066: the verdict event summarises this session's observed delegation checks
# — and omits the summary, never the verdict, when there is nothing to count.
CLEAN = START + [FEEDBACK, _say("— Verify: clean (x)")]
DELEGATION_CASES = [
    ("this session's checks counted",
     "S", [_checked("S", True), _checked("S", False), _checked("S", True)],
     {"checked": 3, "failed": 1}),
    ("no delegation records -> key absent", "S", [], None),
    ("other sessions' records ignored",
     "S", [_checked("T", False), _checked("S", True), _checked("T", True)],
     {"checked": 1, "failed": 0}),
    ("only other sessions' records -> key absent", "S", [_checked("T", True)], None),
    ("no session id -> key absent", None, [_checked("S", True)], None),
    ("malformed lines tolerated",
     "S", ["not json{", _checked("S", False), "[1, 2]",
           json.dumps({"type": "soul.delegation.checked", "genaisessionid": "S", "data": 7})],
     {"checked": 1, "failed": 1}),
    ("only observed checks counted",
     "S", [_checked("S", False, observed=False), _checked("S", False, observed=None),
           _checked("S", True, observed="true"), _checked("S", True)],
     {"checked": 1, "failed": 0}),
]


def _run_hook(records, session_id=None, seed=(), prepare=None):
    """Run main() as a stop_hook_active stop; return (exit code, events written).

    `seed` lines are written to the sink first (raw, so a malformed one can be
    planted), and `prepare(project_dir)` runs before the hook; neither's lines are
    returned — only events the hook itself wrote are."""
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, "witness.md"), "w").close()  # a Soul project
        tpath = os.path.join(tmp, "t.jsonl")
        with open(tpath, "w") as fh:
            fh.writelines(json.dumps(r) + "\n" for r in records)
        sink = os.path.join(tmp, ".soul", "events.jsonl")
        if seed:
            os.makedirs(os.path.dirname(sink))
            with open(sink, "w") as fh:
                fh.writelines(line + "\n" for line in seed)
        if prepare:
            prepare(tmp)
        before = len(open(sink).readlines()) if os.path.exists(sink) else 0
        hook_in = {"stop_hook_active": True, "cwd": tmp, "transcript_path": tpath}
        if session_id:
            hook_in["session_id"] = session_id
        stdin = io.StringIO(json.dumps(hook_in))
        env = {k: v for k, v in os.environ.items() if k != "SOUL_EVENT_LOG"}
        code = None
        with mock.patch.object(sys, "stdin", stdin), redirect_stderr(io.StringIO()), \
                mock.patch.dict(os.environ, env, clear=True):
            try:
                _mod.main()
            except SystemExit as e:
                code = e.code
        lines = open(sink).readlines()[before:] if os.path.exists(sink) else []
        return code, [json.loads(l) for l in lines]


# Fail-open on malformed input: a non-string cwd must not raise.
with mock.patch.object(sys, "stdin", io.StringIO('{"stop_hook_active": true, "cwd": 1}')):
    try:
        _mod.main()
        bad_code = None
    except SystemExit as e:
        bad_code = e.code
    except Exception as e:  # noqa: BLE001 — the failure being fenced
        bad_code = repr(e)

failed = 0
print(f"{'ok  ' if bad_code == 0 else 'FAIL'} malformed cwd -> exit 0: got {bad_code}")
failed += bad_code != 0
for name, records, want in CASES:
    code, events = _run_hook(records)
    got = events[0]["data"]["verdict"] if events else None
    ok = (code == 0 and got == want and len(events) <= 1
          and all(e["type"] == "soul.gate.completion.verdict"
                  and e["data"]["self_reported"] is True for e in events))
    failed += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {name}: exit {code}, verdict {got}, want {want}")
for name, session, seed, want in DELEGATION_CASES:
    code, events = _run_hook(CLEAN, session_id=session, seed=seed)
    got = events[0]["data"].get("delegation", None) if len(events) == 1 else "no-verdict"
    ok = (code == 0 and len(events) == 1 and events[0]["data"]["verdict"] == "verified"
          and got == want and ("delegation" in events[0]["data"]) == (want is not None))
    failed += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {name}: exit {code}, delegation {got}, want {want}")


# End to end: the REAL recorder, run from the Soul project under session S, writes
# the record this hook's verdict path then counts — one format, one sink, both sides.
def _record_real_check(project):
    env = {k: v for k, v in os.environ.items() if k != "SOUL_EVENT_LOG"}
    env["CLAUDE_CODE_SESSION_ID"] = "S"
    subprocess.run([sys.executable, _RECORDER, "record", "--step", "s1", "--worker",
                    "routine:subagent", "--check", "true"], cwd=project,
                   env=env, capture_output=True, timeout=60, check=True)


try:
    code, events = _run_hook(CLEAN, session_id="S", prepare=_record_real_check)
    got = events[0]["data"].get("delegation") if len(events) == 1 else "no-verdict"
except Exception as e:  # noqa: BLE001 — a recorder failure is this case failing
    code, got = None, repr(e)
ok = code == 0 and got == {"checked": 1, "failed": 0}
failed += not ok
print(f"{'ok  ' if ok else 'FAIL'} real recorder -> verdict counts it: exit {code}, "
      f"delegation {got}")

# A non-regular sink ($SOUL_EVENT_LOG at a FIFO, /dev/stderr) must not hang the stop:
# opening a FIFO for reading blocks until a writer appears.
with tempfile.TemporaryDirectory() as tmp:
    fifo = os.path.join(tmp, "events.fifo")
    os.mkfifo(fifo)
    result = []
    with mock.patch.dict(os.environ, {"SOUL_EVENT_LOG": fifo}):
        worker = threading.Thread(target=lambda: result.append(
            _mod._delegation_counts(tmp, "S")), daemon=True)
        worker.start()
        worker.join(3)
    hung = worker.is_alive()
    if hung:  # release the blocked open so the thread can finish
        os.close(os.open(fifo, os.O_WRONLY | os.O_NONBLOCK))
        worker.join(3)
ok = not hung and result == [None]
failed += not ok
print(f"{'ok  ' if ok else 'FAIL'} FIFO sink -> None without blocking: hung {hung}, "
      f"got {result}")
total = len(CASES) + len(DELEGATION_CASES) + 3
print(f"{'PASS' if not failed else 'FAIL'}  {total - failed}/{total} — gate verdict event")
sys.exit(1 if failed else 0)
