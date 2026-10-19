"""Exercise Codex event behavior without a model, host trust, or real projects.

Run: python3 -B -m unittest discover -s hooks -p 'test_codex.py' -v
"""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("soul_codex", HERE / "codex.py")
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class CodexEvents(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.project = self.root / "project"
        self.project.mkdir()
        (self.project / "AGENTS.md").write_text("Use soul-resume for the Soul System.\n")
        self.data = {"cwd": str(self.project), "session_id": "session-a", "turn_id": "turn-a"}
        self.env = patch.dict(os.environ, {"PLUGIN_DATA": str(self.root / "state")})
        self.env.start()
        self.addCleanup(self.env.stop)
        cooldown = patch.object(adapter.gate, "_cooldown_path", return_value=str(self.root / "cooldown"))
        cooldown.start()
        self.addCleanup(cooldown.stop)

    def event(self, event, **kwargs):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = adapter.handle({**self.data, "hook_event_name": event, **kwargs})
        return code, out.getvalue(), err.getvalue()

    def edit(self, **kwargs):
        return self.event("PostToolUse", tool_name="apply_patch", **kwargs)

    def stop(self, **kwargs):
        return self.event("Stop", last_assistant_message="The implementation is complete.", **kwargs)

    def git(self, *args):
        subprocess.run(["git", "-C", str(self.project), *args], check=True, capture_output=True)

    def repository(self):
        self.git("init", "-q")
        (self.project / "file.txt").write_text("baseline\n")
        self.git("add", "AGENTS.md", "file.txt")

    def shell(self, action):
        self.event("PreToolUse", tool_name="Bash", tool_use_id="call-1")
        action()
        self.event("PostToolUse", tool_name="Bash", tool_use_id="call-1")

    def test_startup_delivers_actual_contract(self):
        code, out, err = self.event("SessionStart")
        context = json.loads(out)["hookSpecificOutput"]["additionalContext"]
        self.assertEqual(code, 0)
        self.assertIn((adapter.ROOT / "operations/CLAUDE.md").read_text(), context)
        self.assertIn("session-a", context)
        self.assertEqual(err, "")

    def test_ordinary_soul_word_does_not_scope(self):
        (self.project / "AGENTS.md").write_text("Soul music project.\n")
        self.assertEqual(self.event("SessionStart"), (0, "", ""))
        self.edit()
        self.assertEqual(self.stop()[0], 0)

    def test_override_only_project_scopes(self):
        (self.project / "AGENTS.md").unlink()
        (self.project / "AGENTS.override.md").write_text("Use soul-resume.\n")
        self.edit()
        self.assertEqual(self.stop()[0], 2)

    def test_edit_and_claim_blocks_and_emits_event(self):
        self.edit()
        code, out, err = self.stop()
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("Verify the verifier", err)
        event = json.loads((self.project / ".soul/events.jsonl").read_text())
        self.assertEqual(event["genaisessionid"], "session-a")
        self.assertEqual(event["type"], "soul.gate.completion.flagged")

    def test_claim_without_edit_allows(self):
        self.assertEqual(self.stop(), (0, "", ""))

    def test_edit_without_claim_allows(self):
        self.edit()
        self.assertEqual(self.event("Stop", last_assistant_message="Here is the current analysis.")[0], 0)

    def test_previous_turn_does_not_leak(self):
        self.edit()
        self.data["turn_id"] = "turn-b"
        self.assertEqual(self.stop()[0], 0)

    def test_other_session_does_not_leak(self):
        self.edit()
        self.data["session_id"] = "session-b"
        self.assertEqual(self.stop()[0], 0)

    def test_other_project_does_not_leak(self):
        self.edit()
        other = self.root / "other"
        other.mkdir()
        (other / "witness.md").touch()
        self.data["cwd"] = str(other)
        self.assertEqual(self.stop()[0], 0)

    def test_loop_guard_and_repeat_stop(self):
        self.edit()
        self.assertEqual(self.stop(stop_hook_active=True)[0], 0)
        self.assertEqual(self.stop()[0], 2)
        self.assertEqual(self.stop()[0], 0)

    def events(self):
        sink = self.project / ".soul/events.jsonl"
        return [json.loads(line) for line in sink.read_text().splitlines()] if sink.exists() else []

    def test_reply_to_checklist_emits_verdict_once(self):
        self.edit()
        self.assertEqual(self.stop()[0], 2)
        reply = "Next: merge.\n— Verify: clean (pytest 12/12)"
        self.assertEqual(self.event("Stop", stop_hook_active=True, last_assistant_message=reply), (0, "", ""))
        self.assertEqual(self.event("Stop", stop_hook_active=True, last_assistant_message=reply)[0], 0)
        verdicts = [e for e in self.events() if e["type"] == "soul.gate.completion.verdict"]
        self.assertEqual(len(verdicts), 1)
        self.assertEqual(verdicts[0]["data"]["verdict"], "verified")
        self.assertIs(verdicts[0]["data"]["self_reported"], True)
        self.assertEqual(verdicts[0]["genaisessionid"], "session-a")

    def test_verdict_classification_matches_claude_hook(self):
        for reply, want in (
            ("— Verify: GAP → never ran the CLI", "gap"),
            ("— Verified: unit tests\n— Not verified: the deploy", "gap"),
            ("Okay, all good.", "unreported"),
            ("Format:\n```\n— Verified: pytest\n```\nok", "unreported"),
            ("> — Not verified: <missing>\n— Verified: pytest 4/4", "verified"),
        ):
            with self.subTest(reply=reply):
                self.data["turn_id"] = "turn-" + str(abs(hash(reply)))
                (self.root / "cooldown").unlink(missing_ok=True)
                self.edit()
                self.assertEqual(self.stop()[0], 2)
                self.event("Stop", stop_hook_active=True, last_assistant_message=reply)
                self.assertEqual(self.events()[-1]["data"]["verdict"], want)

    def test_no_verdict_without_our_block_or_reply(self):
        self.edit()
        # Another hook's block: this adapter never blocked the turn.
        self.event("Stop", stop_hook_active=True, last_assistant_message="— Verified: x")
        self.assertEqual(self.events(), [])
        self.assertEqual(self.stop()[0], 2)
        # No reply string in the payload: unknown, not "unreported".
        self.assertEqual(self.event("Stop", stop_hook_active=True)[0], 0)
        self.assertEqual([e["type"] for e in self.events()], ["soul.gate.completion.flagged"])

    def test_verdict_failure_fails_open(self):
        self.edit()
        self.assertEqual(self.stop()[0], 2)
        with patch.object(adapter.gate, "_emit_event", side_effect=RuntimeError("sink")):
            self.assertEqual(
                self.event("Stop", stop_hook_active=True, last_assistant_message="— Verified: x"),
                (0, "", ""),
            )

    def test_project_cooldown_is_shared_across_turns(self):
        self.edit()
        self.assertEqual(self.stop()[0], 2)
        self.data["turn_id"] = "turn-b"
        self.edit()
        self.assertEqual(self.stop()[0], 0)

    def test_read_only_shell_does_not_count_as_edit(self):
        self.repository()
        self.shell(lambda: (self.project / "file.txt").read_text())
        self.assertEqual(self.stop()[0], 0)

    def test_shell_modifies_already_dirty_file(self):
        self.repository()
        (self.project / "file.txt").write_text("already dirty\n")
        self.shell(lambda: (self.project / "file.txt").write_text("changed again\n"))
        self.assertEqual(self.stop()[0], 2)

    def test_shell_creates_untracked_file(self):
        self.repository()
        self.shell(lambda: (self.project / "new.txt").write_text("new\n"))
        self.assertEqual(self.stop()[0], 2)

    def test_shell_deletes_file(self):
        self.repository()
        self.shell(lambda: (self.project / "file.txt").unlink())
        self.assertEqual(self.stop()[0], 2)

    def test_shell_ignored_file_is_explicitly_outside_coverage(self):
        self.repository()
        (self.project / ".gitignore").write_text("ignored.txt\n")
        self.shell(lambda: (self.project / "ignored.txt").write_text("ignored\n"))
        self.assertEqual(self.stop()[0], 0)

    def test_shell_non_git_project_is_outside_coverage(self):
        self.shell(lambda: (self.project / "new.txt").write_text("new\n"))
        self.assertEqual(self.stop()[0], 0)

    def test_shell_post_without_pre_does_not_invent_edit(self):
        self.repository()
        self.event("PostToolUse", tool_name="Bash", tool_use_id="unknown")
        self.assertEqual(self.stop()[0], 0)

    def test_missing_ids_and_malformed_json_fail_open_visibly(self):
        for payload in ("not json", "[]", json.dumps({
            "cwd": str(self.project), "hook_event_name": "PostToolUse", "tool_name": "apply_patch"
        })):
            result = subprocess.run(
                [sys.executable, "-B", str(HERE / "codex.py")], input=payload,
                capture_output=True, text=True, check=True,
            )
            self.assertIn("not guaranteed", json.loads(result.stdout)["systemMessage"])


if __name__ == "__main__":
    unittest.main()
