"""Verdict-event test for the completion gate (structured gate result).

FENCE: on the stop after the gate blocks, the hook reads the reply's Verify line
and emits soul.gate.completion.verdict — verified | gap | unreported, always marked
self_reported (the hook never observes verification itself). It must emit nothing
when the block came from another hook, must never block, and a reply listing both
a Verified and a Not-verified line is a gap.

Run: python3 hooks/test_verdict.py  (exit 0 = fence holds)
"""

import importlib.util
import io
import json
import os
import sys
import tempfile
from contextlib import redirect_stderr
from unittest import mock

_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "pre_completion_verify", os.path.join(_HERE, "pre-completion-verify.py")
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def _user(text, **meta):
    return {"type": "user", **meta, "message": {"role": "user", "content": text}}


def _say(text):
    return {"type": "assistant", "message": {"role": "assistant",
                                             "content": [{"type": "text", "text": text}]}}


FEEDBACK = _user("Stop hook feedback: [python3 hook]: " + _mod._GATE_MARK
                 + " Shipped + claimed complete this turn — fires once.", isMeta=True)
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


def _run_hook(records):
    """Run main() as a stop_hook_active stop; return (exit code, events written)."""
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, "witness.md"), "w").close()  # a Soul project
        tpath = os.path.join(tmp, "t.jsonl")
        with open(tpath, "w") as fh:
            fh.writelines(json.dumps(r) + "\n" for r in records)
        stdin = io.StringIO(json.dumps({"stop_hook_active": True, "cwd": tmp,
                                        "transcript_path": tpath}))
        code = None
        with mock.patch.object(sys, "stdin", stdin), redirect_stderr(io.StringIO()):
            try:
                _mod.main()
            except SystemExit as e:
                code = e.code
        sink = os.path.join(tmp, ".soul", "events.jsonl")
        events = [json.loads(l) for l in open(sink)] if os.path.exists(sink) else []
        return code, events


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
print(f"{'PASS' if not failed else 'FAIL'}  {len(CASES) + 1 - failed}/{len(CASES) + 1} — gate verdict event")
sys.exit(1 if failed else 0)
