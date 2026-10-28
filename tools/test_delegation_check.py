"""Behaviour test for tools/delegation-check.py (the delegated-step check recorder).

FENCE: the main session's re-run of a delegated step's check is OBSERVED, so its
record must carry the real exit code, pass/fail and timeout as the tool saw them;
a review verdict is handed in, so it is always marked self_reported. A usage error
records nothing; a sink that cannot be written never hides the check's result.
The record goes to the Soul project found from the recorder's own working
directory (or the main worktree's) — never from --cwd, which is only where the check
runs — and never into a non-Soul directory. Nothing in the check's process group
outlives the tool, whether it timed out, finished leaving children, or the tool
itself was killed; a signal the caller ignores stays ignored.

Run: python3 -m unittest tools/test_delegation_check.py -v
"""

import importlib.util
import io
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

_TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "delegation-check.py")
_spec = importlib.util.spec_from_file_location("delegation_check", _TOOL)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def _soul_project(path, layout="witness.md"):
    os.makedirs(os.path.dirname(os.path.join(path, layout)), exist_ok=True)
    open(os.path.join(path, layout), "w").close()
    return path


class DelegationCheck(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.tmp = self.temporary.name
        self.sink = os.path.join(self.tmp, "events.jsonl")
        self.env = {k: v for k, v in os.environ.items()
                    if k not in ("SOUL_EVENT_LOG", "CLAUDE_CODE_SESSION_ID")}
        self.env["SOUL_EVENT_LOG"] = self.sink

    def run_tool(self, *args, env=None, cwd=None, timeout=None):
        return subprocess.run([sys.executable, _TOOL] + list(args), capture_output=True,
                              text=True, env=env or self.env, cwd=cwd or self.tmp,
                              timeout=timeout)

    def record(self, check, *extra, worker="routine:ollama:qwen3:32b", env=None, cwd=None):
        return self.run_tool("record", "--step", "step 1", "--worker", worker,
                             "--check", check, *extra, env=env, cwd=cwd)

    def events(self, path=None):
        path = path or self.sink
        if not os.path.exists(path):
            return []
        with open(path, encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]

    def test_passing_check_records_passed_and_exits_0(self):
        out = self.record("echo first; echo all good")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout.strip(), "PASS (exit 0) — all good")
        [ev] = self.events()
        self.assertEqual(ev["specversion"], "1.0")
        self.assertEqual(ev["type"], "soul.delegation.checked")
        self.assertEqual(ev["source"], "urn:soul:project:" + os.path.basename(self.tmp))
        check = ev["data"]["check"]
        self.assertEqual(check, {"command": "echo first; echo all good", "exit_code": 0,
                                 "passed": True, "timed_out": False, "tail": "all good",
                                 "observed": True})
        self.assertEqual(ev["data"]["step"], "step 1")
        self.assertIsNone(ev["data"]["review"])

    def test_failing_check_records_failed_and_exits_1(self):
        out = self.record("echo boom >&2; echo; exit 3")
        self.assertEqual(out.returncode, 1, out.stderr)
        self.assertEqual(out.stdout.strip(), "FAIL (exit 3) — boom")
        [ev] = self.events()
        self.assertEqual(ev["data"]["check"]["exit_code"], 3)
        self.assertIs(ev["data"]["check"]["passed"], False)
        self.assertEqual(ev["data"]["check"]["tail"], "boom")

    def test_timeout_records_timed_out_and_exits_2(self):
        out = self.record("echo started; sleep 30", "--timeout", "1")
        self.assertEqual(out.returncode, 2, out.stderr)
        self.assertTrue(out.stdout.startswith("FAIL (timeout 1s)"), out.stdout)
        [ev] = self.events()
        check = ev["data"]["check"]
        self.assertIsNone(check["exit_code"])
        self.assertIs(check["timed_out"], True)
        self.assertIs(check["passed"], False)

    def test_tail_is_truncated_to_300_chars(self):
        out = self.record("printf 'x%.0s' $(seq 1 500); echo")
        self.assertEqual(out.returncode, 0, out.stderr)
        [ev] = self.events()
        self.assertEqual(ev["data"]["check"]["tail"], "x" * 300)

    def test_worker_parsing(self):
        self.record("true", worker="deep:subagent")
        self.record("true", worker="review:codex:gpt-5:high")
        a, b = self.events()
        self.assertEqual(a["data"]["worker"], {"tier": "deep", "tool": "subagent", "model": None})
        self.assertEqual(b["data"]["worker"],
                         {"tier": "review", "tool": "codex", "model": "gpt-5:high"})

    def test_blank_check_and_nonpositive_timeout_are_usage_errors(self):
        for extra in (("--check", ""), ("--check", "  \t"),
                      ("--check", "touch ran", "--timeout", "0"),
                      ("--check", "touch ran", "--timeout", "-5"),
                      ("--check", "touch ran", "--timeout", "nan")):
            out = self.run_tool("record", "--step", "s", "--worker", "routine:t", *extra)
            self.assertEqual(out.returncode, 2, (extra, out.stdout, out.stderr))
        self.assertEqual(self.events(), [])
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "ran")))

    def test_default_timeout_is_under_the_bash_tool_cap(self):
        seen = {}

        def fake_run(command, cwd, timeout, confined=None):
            seen["timeout"] = timeout
            return 0, False, ""
        argv = [_TOOL, "record", "--step", "s", "--worker", "routine:t", "--check", "true"]
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.dict(os.environ, self.env, clear=True), \
                mock.patch.object(_mod, "run_check", fake_run), \
                redirect_stdout(io.StringIO()):
            self.assertEqual(_mod.main(), 0)
        self.assertEqual(seen["timeout"], 540)  # the Bash tool's foreground cap is 600 s

    def test_bad_worker_exits_2_and_records_nothing(self):
        for worker in ("deep", "deep:", "subagent", ":claude", "9x:claude", "a b:claude"):
            out = self.record("touch ran", worker=worker)
            self.assertEqual(out.returncode, 2, worker)
        self.assertEqual(self.events(), [])
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "ran")))

    def test_workflow_role_names_are_accepted_as_the_worker_tier(self):
        out = self.record("true", worker="implementer:claude:sonnet")
        self.assertEqual(out.returncode, 0, out.stderr)
        [ev] = self.events()
        self.assertEqual(ev["data"]["worker"], {"tier": "implementer", "tool": "claude",
                                                "model": "sonnet"})

    def test_review_fields_are_self_reported(self):
        self.record("true", "--reviewer", "diff-reviewer:opus", "--review-verdict", "pass")
        [ev] = self.events()
        self.assertEqual(ev["data"]["review"], {"tool": "diff-reviewer", "model": "opus",
                                                "verdict": "pass", "self_reported": True})
        self.assertIs(ev["data"]["check"]["observed"], True)

    def test_session_id_from_env_and_absent_when_unset(self):
        self.record("true")
        env = dict(self.env, CLAUDE_CODE_SESSION_ID="sess-1")
        self.record("true", env=env)
        unset, set_ = self.events()
        self.assertNotIn("genaisessionid", unset)
        self.assertEqual(set_["genaisessionid"], "sess-1")

    def test_unwritable_sink_still_returns_check_result(self):
        blocker = os.path.join(self.tmp, "a-file")
        open(blocker, "w").close()
        env = dict(self.env, SOUL_EVENT_LOG=os.path.join(blocker, "events.jsonl"))
        out = self.record("echo nope; exit 1", env=env)
        self.assertEqual(out.returncode, 1)
        self.assertEqual(out.stdout.strip(), "FAIL (exit 1) — nope")
        self.assertIn("warning: delegation record not written", out.stderr)
        out = self.record("echo ok", env=env)
        self.assertEqual(out.returncode, 0)
        self.assertIn("warning", out.stderr)

    def test_list_filters_by_session(self):
        self.record("true", env=dict(self.env, CLAUDE_CODE_SESSION_ID="A"))
        self.record("false", env=dict(self.env, CLAUDE_CODE_SESSION_ID="B"))
        with open(self.sink, "a") as fh:
            fh.write("not json{\n")
        out = self.run_tool("list", "--session", "B")
        self.assertEqual(out.returncode, 0, out.stderr)
        lines = out.stdout.strip().splitlines()
        self.assertEqual(len(lines), 1)
        self.assertIn("FAIL", lines[0])
        self.assertIn("routine:ollama:qwen3:32b", lines[0])
        self.assertTrue(lines[0].endswith("step 1"))
        records = json.loads(self.run_tool("list", "--json").stdout)
        self.assertEqual([r["genaisessionid"] for r in records], ["A", "B"])

    def no_log_env(self, **extra):
        env = {k: v for k, v in self.env.items() if k != "SOUL_EVENT_LOG"}
        env.update(extra)
        return env

    def test_cwd_is_honoured(self):
        project = _soul_project(os.path.join(self.tmp, "proj"))
        sub = os.path.join(project, "sub")
        os.makedirs(sub)
        env = self.no_log_env()
        out = self.record("pwd", "--cwd", sub, env=env, cwd=project)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(os.path.realpath(out.stdout.split("— ", 1)[1].strip()),
                         os.path.realpath(sub))
        [ev] = self.events(os.path.join(project, ".soul", "events.jsonl"))
        self.assertEqual(ev["source"], "urn:soul:project:proj")
        listed = self.run_tool("list", env=env, cwd=project)
        self.assertIn("PASS", listed.stdout)

    def test_record_walks_up_from_its_own_dir_to_the_project(self):
        for layout in ("witness.md", os.path.join(".soul", "witness.md")):
            project = _soul_project(os.path.join(self.tmp, "p-" + layout[0]), layout)
            deep = os.path.join(project, "src", "deep")
            os.makedirs(deep)
            env = self.no_log_env()
            out = self.record("pwd", env=env, cwd=deep)
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertEqual(os.path.realpath(out.stdout.split("— ", 1)[1].strip()),
                             os.path.realpath(deep))  # --cwd defaults to here
            [ev] = self.events(os.path.join(project, ".soul", "events.jsonl"))
            self.assertEqual(ev["source"], "urn:soul:project:" + os.path.basename(project))
            self.assertFalse(os.path.exists(os.path.join(deep, ".soul")))
            listed = self.run_tool("list", env=env, cwd=deep)
            self.assertIn("PASS", listed.stdout)

    def test_cwd_does_not_choose_the_project(self):
        project = _soul_project(os.path.join(self.tmp, "other"))
        bare = os.path.join(self.tmp, "bare")
        os.makedirs(bare)
        out = self.record("true", "--cwd", project, env=self.no_log_env(), cwd=bare)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("not a Soul project", out.stderr)
        self.assertFalse(os.path.exists(os.path.join(project, ".soul", "events.jsonl")))

    def test_project_flag_separates_record_from_check_dir(self):
        project = _soul_project(os.path.join(self.tmp, "home"))
        elsewhere = os.path.join(self.tmp, "elsewhere")
        os.makedirs(elsewhere)
        env = self.no_log_env()
        out = self.record("pwd", "--cwd", elsewhere, "--project", project, env=env)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(os.path.realpath(out.stdout.split("— ", 1)[1].strip()),
                         os.path.realpath(elsewhere))
        [ev] = self.events(os.path.join(project, ".soul", "events.jsonl"))
        self.assertEqual(ev["source"], "urn:soul:project:home")
        self.assertFalse(os.path.exists(os.path.join(elsewhere, ".soul")))
        listed = self.run_tool("list", "--project", project, env=env)
        self.assertIn("PASS", listed.stdout)

    GIT = ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c",
           "commit.gpgsign=false"]

    def git(self, cwd, *cmd):
        subprocess.run(self.GIT + list(cmd), cwd=cwd, check=True, capture_output=True)

    @unittest.skipUnless(shutil.which("git"), "needs git")
    def test_linked_worktree_records_to_the_main_worktree(self):
        main = os.path.join(self.tmp, "main")
        os.makedirs(main)
        wt = os.path.join(self.tmp, "wt")
        self.git(main, "init", "-q")
        self.git(main, "commit", "-q", "--allow-empty", "-m", "x")
        self.git(main, "worktree", "add", "-q", wt)
        _soul_project(main)  # untracked, so the worktree has no witness.md of its own
        self.assertFalse(os.path.exists(os.path.join(wt, "witness.md")))
        out = self.record("true", env=self.no_log_env(), cwd=wt)
        self.assertEqual(out.returncode, 0, out.stderr)
        [ev] = self.events(os.path.join(main, ".soul", "events.jsonl"))
        self.assertEqual(ev["source"], "urn:soul:project:main")
        self.assertFalse(os.path.exists(os.path.join(wt, ".soul", "events.jsonl")))

    @unittest.skipUnless(shutil.which("git"), "needs git")
    def test_check_in_worktree_with_tracked_record_records_to_the_session(self):
        # The common case: soul-init tracks the record, so a linked worktree carries
        # its own .soul/witness.md. --cwd <worktree> must not move the record there.
        main = os.path.join(self.tmp, "main")
        wt = os.path.join(self.tmp, "wt")
        _soul_project(main, os.path.join(".soul", "witness.md"))
        self.git(main, "init", "-q")
        self.git(main, "add", os.path.join(".soul", "witness.md"))
        self.git(main, "commit", "-q", "-m", "x")
        self.git(main, "worktree", "add", "-q", wt)
        self.assertTrue(os.path.exists(os.path.join(wt, ".soul", "witness.md")))
        out = self.record("pwd", "--cwd", wt, env=self.no_log_env(), cwd=main)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(os.path.realpath(out.stdout.split("— ", 1)[1].strip()),
                         os.path.realpath(wt))  # the check ran in the worktree
        [ev] = self.events(os.path.join(main, ".soul", "events.jsonl"))
        self.assertEqual(ev["source"], "urn:soul:project:main")
        self.assertFalse(os.path.exists(os.path.join(wt, ".soul", "events.jsonl")))

    def test_not_a_soul_project_runs_the_check_but_records_nothing(self):
        bare = os.path.join(self.tmp, "bare")
        os.makedirs(bare)
        out = self.record("echo fine", env=self.no_log_env(), cwd=bare)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout.strip(), "PASS (exit 0) — fine")
        self.assertEqual(out.stderr.count("not a Soul project — result not recorded"), 1)
        self.assertFalse(os.path.exists(os.path.join(bare, ".soul")))
        out = self.record("exit 4", env=self.no_log_env(), cwd=bare)
        self.assertEqual(out.returncode, 1)
        self.assertFalse(os.path.exists(os.path.join(bare, ".soul")))

    def test_killing_the_recorder_kills_the_check(self):
        started = os.path.join(self.tmp, "started")
        orphan = os.path.join(self.tmp, "orphan")
        proc = subprocess.Popen(
            [sys.executable, _TOOL, "record", "--step", "s", "--worker", "routine:t",
             "--check", "touch started; sleep 1.5; touch orphan"],
            cwd=self.tmp, env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        deadline = time.time() + 10
        while not os.path.exists(started) and time.time() < deadline:
            time.sleep(0.05)
        self.assertTrue(os.path.exists(started), "check never started")
        proc.send_signal(signal.SIGTERM)
        _, err = proc.communicate(timeout=10)
        self.assertEqual(proc.returncode, 128 + signal.SIGTERM, err)
        time.sleep(2.5)
        self.assertFalse(os.path.exists(orphan), "the check outlived the recorder")
        self.assertEqual(self.events(), [])

    def test_ignored_signal_stays_ignored(self):
        # Under nohup or as a background job the caller ignores the signal; the
        # recorder must not turn it back into a kill.
        started = os.path.join(self.tmp, "started")
        proc = subprocess.Popen(
            [sys.executable, _TOOL, "record", "--step", "s", "--worker", "routine:t",
             "--check", "touch started; sleep 1; echo done"],
            cwd=self.tmp, env=self.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, preexec_fn=lambda: signal.signal(signal.SIGHUP, signal.SIG_IGN))
        deadline = time.time() + 10
        while not os.path.exists(started) and time.time() < deadline:
            time.sleep(0.05)
        self.assertTrue(os.path.exists(started), "check never started")
        proc.send_signal(signal.SIGHUP)
        out, err = proc.communicate(timeout=10)
        self.assertEqual(proc.returncode, 0, err)
        self.assertEqual(out.strip(), "PASS (exit 0) — done")
        [ev] = self.events()
        self.assertIs(ev["data"]["check"]["passed"], True)

    def test_signal_handler_ignores_further_signals(self):
        saved = {s: signal.getsignal(s) for s in _mod.SIGNALS}
        self.addCleanup(lambda: [signal.signal(s, h) for s, h in saved.items()])
        with self.assertRaises(_mod.Killed):
            _mod._on_signal(signal.SIGTERM, None)
        for s in _mod.SIGNALS:
            self.assertIs(signal.getsignal(s), signal.SIG_IGN, s)

    def test_previous_handler_of_none_is_not_restored(self):
        # signal.signal() returns None for a handler not installed from Python;
        # passing None back raises TypeError, which must not crash the report.
        real = signal.signal

        def fake_signal(s, handler):
            if handler is None:
                raise TypeError("signal handler must be signal.SIG_IGN, ...")
            return None
        argv = [_TOOL, "record", "--step", "s", "--worker", "routine:t", "--check", "true"]
        out = io.StringIO()
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.dict(os.environ, self.env, clear=True), \
                mock.patch.object(_mod.signal, "signal", fake_signal), \
                redirect_stdout(out):
            code = _mod.main()
        self.assertIs(signal.signal, real)
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().strip(), "PASS (exit 0) —")

    def test_check_starts_with_termination_signals_unblocked(self):
        # The recorder blocks them around Popen; the mask is inherited across exec,
        # so without the child-side unblock this shell would survive its own SIGTERM.
        out = self.record("kill -TERM $$; echo survived")
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        [ev] = self.events()
        self.assertEqual(ev["data"]["check"]["exit_code"], -signal.SIGTERM)
        self.assertNotIn("survived", out.stdout)

    def test_list_does_not_block_on_a_fifo_sink(self):
        fifo = os.path.join(self.tmp, "events.fifo")
        os.mkfifo(fifo)
        try:
            out = self.run_tool("list", env=dict(self.env, SOUL_EVENT_LOG=fifo), timeout=10)
        except subprocess.TimeoutExpired:  # run() has already killed the hung list
            self.fail("list blocked opening a FIFO sink")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout.strip(), "no delegation records")

    def test_background_child_holding_output_does_not_fake_a_timeout(self):
        t0 = time.time()
        out = self.record("sleep 5 & echo ok; exit 0", "--timeout", "3")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertLess(time.time() - t0, 2.5)
        [ev] = self.events()
        self.assertIs(ev["data"]["check"]["passed"], True)
        self.assertEqual(ev["data"]["check"]["tail"], "ok")

    @unittest.skipUnless(shutil.which("setsid"), "needs setsid")
    def test_escaped_grandchild_does_not_hang_after_timeout(self):
        t0 = time.time()
        out = self.record("setsid sleep 5 & echo hi; sleep 30", "--timeout", "1")
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertLess(time.time() - t0, 3.5)
        [ev] = self.events()
        self.assertIs(ev["data"]["check"]["timed_out"], True)

    def test_check_does_not_read_the_callers_stdin(self):
        with tempfile.TemporaryFile() as out:
            proc = subprocess.Popen(
                [sys.executable, _TOOL, "record", "--step", "s", "--worker", "routine:t",
                 "--check", "cat; echo done", "--timeout", "3"],
                cwd=self.tmp, env=self.env, stdin=subprocess.PIPE, stdout=out,
                stderr=subprocess.STDOUT)
            try:
                proc.wait(timeout=10)  # the caller's stdin is held open throughout
            finally:
                proc.stdin.close()
                proc.kill()
                proc.wait()
            out.seek(0)
            text = out.read().decode("utf-8", "replace")
        self.assertEqual(proc.returncode, 0, text)
        self.assertEqual(text.strip(), "PASS (exit 0) — done")

    def test_check_that_cannot_start_exits_2_and_records_nothing(self):
        argv = [_TOOL, "record", "--step", "s", "--worker", "routine:t", "--check", "true",
                "--cwd", self.tmp]
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.dict(os.environ, self.env, clear=True), \
                mock.patch.object(_mod.subprocess, "Popen", side_effect=OSError("no sh")), \
                redirect_stdout(out), redirect_stderr(err):
            code = _mod.main()
        self.assertEqual(code, 2)
        self.assertIn("could not start the check", err.getvalue())
        self.assertIn("nothing recorded", err.getvalue())
        self.assertEqual(self.events(), [])

    def test_unencodable_tail_does_not_crash_a_narrow_console(self):
        env = dict(self.env, PYTHONIOENCODING="cp1252")
        out = subprocess.run(
            [sys.executable, _TOOL, "record", "--step", "s", "--worker", "routine:t",
             "--check", "printf '\\342\\234\\223 \\346\\227\\245 ok\\n'"],
            capture_output=True, env=env, cwd=self.tmp)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertTrue(out.stdout.startswith(b"PASS (exit 0)"), out.stdout)
        self.assertTrue(out.stdout.rstrip().endswith(b"? ? ok"), out.stdout)
        [ev] = self.events()
        self.assertEqual(ev["data"]["check"]["tail"], "\u2713 \u65e5 ok")

    # SOUL-I080: /soul-workflow adds where a check sits in a workflow, the host's
    # verdict on each reviewer's findings, and a per-role table of both.

    def test_workflow_fields_are_optional_on_record(self):
        out = self.record("true", "--workflow", "build-verify", "--role", "implementer",
                          "--rung", "2", "--round", "1", "--run-id", "r1",
                          worker="routine:claude:sonnet")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.record("true")
        full, bare = self.events()
        self.assertEqual(full["type"], "soul.delegation.checked")  # the gate counts it
        self.assertEqual({k: full["data"][k] for k in ("workflow", "role", "rung", "round",
                                                       "run_id")},
                         {"workflow": "build-verify", "role": "implementer", "rung": 2,
                          "round": 1, "run_id": "r1"})
        self.assertIs(full["data"]["check"]["observed"], True)
        for key in ("workflow", "role", "rung", "round", "run_id"):
            self.assertNotIn(key, bare["data"])  # the old record shape is unchanged

    def test_bad_rung_or_round_is_a_usage_error(self):
        for extra in (("--rung", "0"), ("--rung", "x"), ("--round", "-1")):
            out = self.record("touch ran", *extra)
            self.assertEqual(out.returncode, 2, extra)
        self.assertEqual(self.events(), [])
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "ran")))

    def test_round_help_says_the_first_attempt_is_round_1(self):
        # /soul-workflow counts the first attempt as round 1 and repairs as 2 and 3;
        # the help said 0 (the 2026-10-27 review).
        out = self.run_tool("record", "--help")
        text = " ".join(out.stdout.split())
        self.assertIn("1 = the first attempt", text)
        self.assertNotIn("0 = first attempt", text)

    def review(self, *args, env=None):
        return self.run_tool("review", *args, env=env)

    def test_review_records_a_self_reported_review_event(self):
        out = self.review("--run-id", "r1", "--reviewer", "codex:default",
                          "--raised", "3", "--accepted", "1")
        self.assertEqual(out.returncode, 0, out.stderr)
        [ev] = self.events()
        self.assertEqual(ev["type"], "soul.workflow.review")
        self.assertEqual(ev["specversion"], "1.0")
        self.assertEqual(ev["data"], {"run_id": "r1",
                                      "reviewer": {"tool": "codex", "model": "default"},
                                      "raised": 3, "accepted": 1, "self_reported": True})
        listed = self.run_tool("list")
        self.assertEqual(listed.stdout.strip(), "no delegation records")  # not a check

    def test_review_usage_errors_record_nothing(self):
        for args in (("--run-id", "r", "--reviewer", "codex", "--raised", "1",
                      "--accepted", "2"),
                     ("--run-id", "r", "--reviewer", "codex", "--raised", "-1",
                      "--accepted", "0"),
                     ("--run-id", "r", "--reviewer", ":opus", "--raised", "1",
                      "--accepted", "0"),
                     ("--run-id", "", "--reviewer", "codex", "--raised", "1",
                      "--accepted", "0"),
                     ("--reviewer", "codex", "--raised", "1", "--accepted", "0")):
            out = self.review(*args)
            self.assertEqual(out.returncode, 2, (args, out.stdout, out.stderr))
        self.assertEqual(self.events(), [])

    def test_review_event_is_not_counted_by_the_gate(self):
        hook = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "hooks", "pre-completion-verify.py")
        spec = importlib.util.spec_from_file_location("pcv", hook)
        pcv = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pcv)
        env = dict(self.env, CLAUDE_CODE_SESSION_ID="S")
        self.review("--run-id", "r", "--reviewer", "claude:opus", "--raised", "2",
                    "--accepted", "2", env=env)
        self.record("false", "--role", "implementer", "--rung", "1", env=env)
        with mock.patch.dict(os.environ, {"SOUL_EVENT_LOG": self.sink}):
            self.assertEqual(pcv._delegation_counts(self.tmp, "S"),
                             {"checked": 1, "failed": 1})

    def stats_fixture(self):
        self.record("true", "--role", "implementer", "--rung", "1",
                    worker="routine:claude:sonnet")
        self.record("false", "--role", "implementer", "--rung", "1",
                    worker="routine:claude:sonnet")
        self.record("true", "--role", "implementer", "--rung", "2",
                    worker="routine:claude:opus")
        self.record("false", worker="deep:subagent")
        for reviewer, raised, accepted in (("claude:opus", 2, 1), ("claude:opus", 3, 3),
                                           ("codex:default", 1, 0)):
            self.review("--run-id", "r", "--reviewer", reviewer, "--raised", str(raised),
                        "--accepted", str(accepted))
        with open(self.sink, "a") as fh:
            fh.write("not json{\n")

    def test_stats_per_role_and_per_reviewer(self):
        self.stats_fixture()
        out = self.run_tool("stats", "--json")
        self.assertEqual(out.returncode, 0, out.stderr)
        got = json.loads(out.stdout)
        self.assertEqual(got["workers"], [
            {"role": "deep", "worker": "subagent", "checks": 1, "passed": 0, "failed": 1,
             "top_rung": None},
            {"role": "implementer", "worker": "claude:opus", "checks": 1, "passed": 1,
             "failed": 0, "top_rung": 2},
            {"role": "implementer", "worker": "claude:sonnet", "checks": 2, "passed": 1,
             "failed": 1, "top_rung": 1}])
        self.assertEqual(got["reviewers"], [
            {"reviewer": "claude:opus", "runs": 2, "raised": 5, "accepted": 4},
            {"reviewer": "codex:default", "runs": 1, "raised": 1, "accepted": 0}])
        text = self.run_tool("stats")
        self.assertEqual(text.returncode, 0, text.stderr)
        self.assertRegex(text.stdout, r"implementer\s+claude:sonnet\s+2\s+1\s+1\s+1")
        self.assertRegex(text.stdout, r"claude:opus\s+2\s+5\s+4")

    def test_stats_counts_every_dispatch_won_or_not(self):
        with open(self.sink, "a") as fh:
            for data in ({"mode": "run", "role": "local", "harness": "claude-ollama",
                          "model": "q:27b", "won": False, "timeouts": 1, "wall_s": 3600},
                         {"mode": "run", "role": "local", "harness": "claude-ollama",
                          "model": "q:27b", "won": True, "timeouts": 0, "wall_s": 60},
                         {"mode": "review", "role": "reviewer", "harness": "codex",
                          "model": "default", "won": True, "timeouts": 0, "wall_s": 30}):
                fh.write(json.dumps({"type": "soul.workflow.dispatch", "data": data}) + "\n")
        got = json.loads(self.run_tool("stats", "--json").stdout)
        self.assertEqual(got["dispatches"], [
            {"mode": "review", "role": "reviewer", "worker": "codex:default", "runs": 1,
             "won": 1, "timeouts": 0, "minutes": 0.5},
            {"mode": "run", "role": "local", "worker": "claude-ollama:q:27b", "runs": 2,
             "won": 1, "timeouts": 1, "minutes": 61.0}])
        self.assertIn("timeouts", self.run_tool("stats").stdout)

    def test_stats_with_no_records(self):
        out = self.run_tool("stats")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout.strip(), "no workflow records")
        got = json.loads(self.run_tool("stats", "--json").stdout)
        self.assertEqual(got, {"dispatches": [], "workers": [], "reviewers": []})

    def test_windows_is_refused(self):
        err = io.StringIO()
        with mock.patch.object(_mod.os, "name", "nt"), \
                mock.patch.object(sys, "argv", [_TOOL, "list"]), redirect_stderr(err):
            code = _mod.main()
        self.assertEqual(code, 2)
        self.assertIn("POSIX-only", err.getvalue())

    # --confine (the 2026-10-27 review of v3.7.0): the host's re-run executes code a
    # worker wrote, so on request it runs under bubblewrap with the allowlisted
    # environment, or not at all.

    def fake_bwrap(self):
        """A bwrap stand-in on a PATH dir: logs argv and env, then runs the command."""
        d = os.path.join(self.tmp, "wrap-bin")
        self.wraplog = os.path.join(self.tmp, "wrap-log.json")
        os.makedirs(d)
        with open(os.path.join(d, "bwrap"), "w") as f:
            f.write("#!{}\nimport json, os, sys\n"
                    "ARITY = {{'--ro-bind': 2, '--bind': 2, '--dev': 1, '--proc': 1,\n"
                    "         '--tmpfs': 1, '--chdir': 1, '--unshare-net': 0,\n"
                    "         '--die-with-parent': 0, '--new-session': 0}}\n"
                    "a = sys.argv[1:]\n"
                    "json.dump({{'argv': a, 'env': dict(os.environ)}}, open({!r}, 'w'))\n"
                    "i = 0\n"
                    "while a[i] in ARITY:\n"
                    "    if a[i] == '--chdir':\n"
                    "        os.chdir(a[i + 1])\n"
                    "    i += 1 + ARITY[a[i]]\n"
                    "os.execvp(a[i], a[i:])\n".format(sys.executable, self.wraplog))
        os.chmod(os.path.join(d, "bwrap"), 0o755)
        return d

    def test_confine_runs_the_check_under_bwrap_with_the_allowlisted_env(self):
        wrap = self.fake_bwrap()
        work = os.path.join(self.tmp, "work")
        os.makedirs(work)
        env = dict(self.env, PATH=wrap + os.pathsep + self.env.get("PATH", ""),
                   GH_TOKEN="ghp_x", CLAUDE_CODE_MESSAGING_TOKEN="tok",
                   GIT_CONFIG_COUNT="1", OPENAI_API_KEY="sk")
        out = self.record("echo confined ok", "--confine", "--cwd", work, env=env)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        with open(self.wraplog) as fh:
            seen = json.load(fh)
        real = os.path.realpath(work)
        self.assertEqual(seen["argv"][-3:], ["/bin/sh", "-c", "echo confined ok"])
        self.assertEqual(seen["argv"][seen["argv"].index("--bind") + 1], real)
        self.assertIn("--unshare-net", seen["argv"])
        for k in ("GH_TOKEN", "CLAUDE_CODE_MESSAGING_TOKEN", "GIT_CONFIG_COUNT",
                  "OPENAI_API_KEY", "SOUL_EVENT_LOG"):
            self.assertNotIn(k, seen["env"])
        [ev] = self.events()
        self.assertIs(ev["data"]["check"]["passed"], True)
        self.assertEqual(ev["data"]["check"]["tail"], "confined ok")

    def test_confine_without_bwrap_refuses_and_records_nothing(self):
        empty = os.path.join(self.tmp, "no-bwrap")
        os.makedirs(empty)
        out = self.record("touch ran", "--confine", env=dict(self.env, PATH=empty))
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertIn("bubblewrap", out.stderr)
        self.assertEqual(self.events(), [])
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "ran")))

    def test_without_confine_the_check_runs_as_before(self):
        wrap = self.fake_bwrap()
        out = self.record("echo plain", env=dict(self.env, PATH=wrap + os.pathsep
                                                 + self.env.get("PATH", "")))
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertFalse(os.path.exists(self.wraplog))

    @unittest.skipUnless(sys.platform.startswith("linux") and shutil.which("bwrap"),
                         "needs a real bubblewrap")
    def test_confine_with_real_bwrap_cannot_write_outside(self):
        base = tempfile.mkdtemp(prefix="soul-dc-confine-",
                                dir="/var/tmp" if os.access("/var/tmp", os.W_OK) else None)
        self.addCleanup(shutil.rmtree, base, True)
        work = os.path.join(base, "work")
        os.makedirs(work)
        outside = os.path.join(base, "outside.txt")
        check = "touch inside.txt && touch {}".format(outside)
        out = self.record(check, "--confine", "--cwd", work)
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertFalse(os.path.exists(outside))
        self.assertTrue(os.path.exists(os.path.join(work, "inside.txt")))
        free = self.record(check, "--cwd", work)  # control: unconfined it does write
        self.assertEqual(free.returncode, 0, free.stdout + free.stderr)
        self.assertTrue(os.path.exists(outside))


if __name__ == "__main__":
    unittest.main()
