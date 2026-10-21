"""Turn-slicing test for the completion gate (background-subagent blind spot).

FENCE: a <task-notification> record (a background subagent or task finishing,
delivered by Claude Code as a user-role message) must NOT start a new turn.
The incident (2026-09-29, Claude Code 2.1.284): a session edited a file, ran a
review subagent in the background, then replied "All three parts are done."
The notification reset the scanned turn, so _scan returned shipped=False and
the gate never fired. A genuine new user prompt must still reset the turn
(the SOUL-027 precision fix).

FENCE: a turn whose only tool uses are a delegated worker (Agent) and Bash is not
"shipped" — the Body's ruling that worker-only turns stay ungated (SOUL-208).

Run: python3 hooks/test_turn.py  (exit 0 = fence holds)
"""

import importlib.util
import json
import os
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "pre_completion_verify", os.path.join(_HERE, "pre-completion-verify.py")
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def _user(text, **meta):
    return {"type": "user", **meta, "message": {"role": "user", "content": text}}


def _assistant(*blocks):
    return {"type": "assistant", "message": {"role": "assistant", "content": list(blocks)}}


def _tool_result():
    return {"type": "user", "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": "x", "content": "ok"}]}}


EDIT = {"type": "tool_use", "name": "Edit", "input": {"file_path": "calc.py"}}
AGENT = {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "review"}}
DONE = {"type": "text", "text": "All three parts are done."}
NOTE = "<task-notification>\n<task-id>a1</task-id>\n<status>completed</status>\n</task-notification>"


def _scan(records):
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as fh:
        for r in records:
            fh.write(json.dumps(r) + "\n")
        path = fh.name
    try:
        return _mod._scan(path)
    finally:
        os.unlink(path)


CASES = [
    ("notification with harness metadata does not reset the turn",
     [_user("fix calc.py", promptSource="sdk"), _assistant(EDIT), _tool_result(),
      _assistant(AGENT), _tool_result(),
      _user(NOTE, promptSource="system", turnOrigin="task_notification"),
      _assistant(DONE)],
     (True, True)),
    ("notification without metadata (older transcripts) does not reset the turn",
     [_user("fix calc.py"), _assistant(EDIT), _tool_result(), _user(NOTE), _assistant(DONE)],
     (True, True)),
    ("a genuine new user prompt still resets the turn (SOUL-027)",
     [_user("fix calc.py"), _assistant(EDIT), _tool_result(),
      _user("thanks — what do you think of the design?"), _assistant(DONE)],
     (False, True)),
    # promptSource "system" is NOT the key: peer-session messages carry it too,
    # and another session's request is a new turn like a person's.
    ("a peer-session message still resets the turn",
     [_user("fix calc.py"), _assistant(EDIT), _tool_result(),
      _user("Another Claude session sent a message: review the plan",
            promptSource="system", turnOrigin="peer", isMeta=True),
      _assistant(DONE)],
     (False, True)),
    # Worker-only turns stay ungated by design (SOUL-208): a turn whose only
    # tool uses are a delegated worker (Agent) and Bash is not "shipped".
    ("a worker-only turn does not count as shipped (SOUL-208)",
     [_user("run the plan step"), _assistant(AGENT), _tool_result(),
      _assistant({"type": "tool_use", "name": "Bash", "input": {"command": "claude -p step"}}),
      _tool_result(), _assistant(DONE)],
     (False, True)),
]

failed = 0
for name, records, want in CASES:
    got = _scan(records)
    ok = got == want
    failed += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {name}: got {got}, want {want}")
print(f"{'PASS' if not failed else 'FAIL'}  {len(CASES) - failed}/{len(CASES)} — turn slicing")
sys.exit(1 if failed else 0)
