"""Behaviour test for hooks/upkeep.py, the handoff-cursor staleness hook (SOUL-A032).

FENCE: the hook is silent unless the cursor is stale, and blocks once per staleness.
F063 and mind item 5: a Stop hook that fired on every turn was the reason the
completion gate's regex was narrowed, and a hook that nags gets switched off. So a
fresh cursor, `stop_hook_active`, `upkeep: off`, a non-Soul project and a project with
no cursor yet must all print nothing; a stale cursor (about 200,000 tokens of new
conversation, or a summary) blocks once and not again until it is stale again. That
holds when the per-user temp folder cannot be trusted too: the block is remembered in
the home cache instead. With no trusted folder at all the hook cannot remember, so it
does not block (F063).

SOUL-243 put state triggers in front of the 200,000-token backstop: background work
started since the cursor was written and still running, a cursor over 150 lines, a Mind
due by the witness count — all in ONE block per stop, highest first, each remembered
before it is returned (per cursor write, or per day per project). A cursor changed by any
means counts as written; after three reminders with no answer, `upkeep: on` is recorded.
`--start` names Mind changes soul-distill holds for the owner's yes.

Each case writes a fake transcript with the field names a real Claude Code transcript
carries (message.usage input / cache tokens, isSidechain, a system compact_boundary
record, a Write tool_use with input.file_path), runs the hook as Claude Code does (JSON
on stdin), and points TMPDIR, HOME and XDG_CACHE_HOME at the case's own folders so the
remembered block never touches the machine's temp folder or home cache.

Run: python3 -B -m unittest discover -s hooks -p 'test_upkeep.py' -v
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))
_HOOK = os.path.join(_HERE, "upkeep.py")
START = 54000  # a typical first-turn context: contract, CLAUDE.md, tool list


def zero():
    """A reply with no usage reading (an API error or a synthetic message)."""
    return {"type": "assistant", "isSidechain": False, "message": {
        "role": "assistant", "content": [{"type": "text", "text": "No response requested."}],
        "usage": {"input_tokens": 0, "cache_creation_input_tokens": 0,
                  "cache_read_input_tokens": 0, "output_tokens": 0}}}


def size(tokens, sidechain=False, write=None):
    content = [{"type": "text", "text": "working"}]
    if write:
        content.append({"type": "tool_use", "name": "Write",
                        "input": {"file_path": write, "content": "# Handoff cursor"}})
    return {"type": "assistant", "isSidechain": sidechain, "message": {
        "role": "assistant", "content": content,
        "usage": {"input_tokens": 2, "cache_creation_input_tokens": 1000,
                  "cache_read_input_tokens": tokens - 1002, "output_tokens": 300}}}


def user(text="go on"):
    return {"type": "user", "isSidechain": False,
            "message": {"role": "user", "content": text}}


def compact():
    return {"type": "system", "subtype": "compact_boundary", "isSidechain": False,
            "compactMetadata": {"trigger": "auto", "preTokens": 400000, "postTokens": 30000}}


# Background work, in the record shapes a real transcript carries (read from a Claude Code
# transcript, 2026-11-18): the launch call, its tool_result carrying the task id, and the
# later <task-notification> — a user message, or a queued_command attachment when it
# arrived while the session was busy.

def launch(tid, desc="Audit hooks", tokens=START + 1000, bash=False):
    """The assistant's call and its result: an Agent launch, or a background Bash."""
    call = "toolu_" + tid
    if bash:
        use = {"type": "tool_use", "id": call, "name": "Bash", "input": {
            "command": "sleep 600", "description": desc, "run_in_background": True}}
        result = ("Command running in background with ID: {}. Output is being written to: "
                  "/tmp/tasks/{}.output. You will be notified when it completes.".format(tid, tid))
    else:
        use = {"type": "tool_use", "id": call, "name": "Agent", "input": {
            "description": desc, "subagent_type": "implementer", "prompt": "do it",
            "run_in_background": "true"}}
        result = [{"type": "text", "text": (
            "Async agent launched successfully.\nagentId: {} (internal ID - do not mention "
            "to user.)\nThe agent is working in the background.".format(tid))}]
    rec = size(tokens)
    rec["message"]["content"].append(use)
    return [rec, {"type": "user", "isSidechain": False, "message": {"role": "user", "content": [
        {"tool_use_id": call, "type": "tool_result", "content": result}]}}]


def notice(tid, status="completed", queued=False):
    text = ("<task-notification>\n<task-id>{}</task-id>\n<tool-use-id>toolu_{}</tool-use-id>\n"
            "<status>{}</status>\n<summary>Agent finished</summary>\n</task-notification>"
            .format(tid, tid, status))
    if queued:
        return {"type": "attachment", "isSidechain": False,
                "attachment": {"type": "queued_command", "prompt": text}}
    return {"type": "user", "isSidechain": False, "origin": {"kind": "task-notification"},
            "message": {"role": "user", "content": text}}


def task_stop(tid, tokens=START + 2000):
    call = "toolu_stop_" + tid
    rec = size(tokens)
    rec["message"]["content"].append(
        {"type": "tool_use", "id": call, "name": "TaskStop", "input": {"task_id": tid}})
    body = json.dumps({"message": "Successfully stopped task: {} (Audit hooks)".format(tid),
                       "task_id": tid, "task_type": "local_agent"})
    return [rec, {"type": "user", "isSidechain": False, "message": {"role": "user", "content": [
        {"tool_use_id": call, "type": "tool_result", "content": body}]}}]


def witness(*dates):
    """A witness log in the record's entry format: ID line, then a WHEN line."""
    out = ["# Witness\n"]
    for i, d in enumerate(dates, 1):
        out.append("```\nID:           SOUL-{:03d}\nWHEN:         {} / a session\n"
                   "WHAT:         something happened\n```\n".format(i, d))
    return "\n".join(out)


class Upkeep(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp(prefix="soul-upkeep-test-")
        self.addCleanup(shutil.rmtree, self.base, True)
        self.tmp = os.path.join(self.base, "tmp")
        os.makedirs(self.tmp)
        self.home = os.path.join(self.base, "home")
        self.xdg = os.path.join(self.base, "xdg-cache")
        self.project = self.make_project("proj")
        self.cursor = os.path.join(self.project, ".soul", "handoff.md")
        self.transcript = os.path.join(self.base, "session.jsonl")
        self.records = []

    def make_project(self, name, soul=True, cursor=True):
        p = os.path.join(self.base, name)
        os.makedirs(os.path.join(p, ".soul"))
        if soul:
            with open(os.path.join(p, "witness.md"), "w") as f:
                f.write("# Witness\n")
        if cursor:
            with open(os.path.join(p, ".soul", "handoff.md"), "w") as f:
                f.write("# Handoff cursor\n")
        return p

    def add(self, *records):
        self.records.extend(records)
        with open(self.transcript, "w", encoding="utf-8") as f:
            for r in self.records:
                f.write(json.dumps(r) + "\n")

    def run_hook(self, *args, active=False, cwd=None, raw=None, env=None):
        data = {"session_id": "s1", "transcript_path": self.transcript,
                "cwd": cwd or self.project, "hook_event_name": "Stop",
                "stop_hook_active": active}
        if "--compact" in args:
            data.update(hook_event_name="SessionStart", source="compact")
        if "--start" in args:
            data.update(hook_event_name="SessionStart", source="startup")
        r = subprocess.run([sys.executable, _HOOK, *args],
                           input=json.dumps(data) if raw is None else raw,
                           capture_output=True, text=True,
                           env={**os.environ, "TMPDIR": self.tmp, "HOME": self.home,
                                "XDG_CACHE_HOME": self.xdg, **(env or {})},
                           timeout=30)
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout) if r.stdout.strip() else None

    def answer(self, line):
        with open(os.path.join(self.project, ".soul", "init.md"), "w") as f:
            f.write("# /soul-init's remembered answers (tools/init-status.py).\n" + line + "\n")

    # ------------------------------------------------------------- the Stop check

    def test_fresh_cursor_is_silent(self):
        # 199k after the write: just under the step (SOUL-243: 200,000), so the old
        # 100,000 step would block here.
        self.add(user(), size(START), size(START + 5000, write=self.cursor), user(),
                 size(START + 204000))
        self.assertIsNone(self.run_hook())

    def test_growth_blocks_once(self):
        self.add(user(), size(START, write=self.cursor), user(), size(START + 201000))
        out = self.run_hook()
        self.assertEqual(out["decision"], "block")
        self.assertIn("/soul-handoff", out["reason"])
        self.assertIn("about 201k tokens", out["reason"])
        # The owner's sun mark starts a line about what Soul did on its own (SOUL-239).
        self.assertIn('in one line that starts with "\u2600  "', out["reason"])
        # The next turn ignores the block and stops again: no second block ...
        self.add(user(), size(START + 210000))
        self.assertIsNone(self.run_hook())
        # ... until another 200,000 tokens have passed.
        self.add(user(), size(START + 402000))
        self.assertEqual(self.run_hook()["decision"], "block")

    def test_growth_counts_from_the_cursor_write(self):
        # 199k after the write is fresh, even though the session is 349k past its start.
        self.add(user(), size(START), size(START + 150000, write=self.cursor), user(),
                 size(START + 349000))
        self.assertIsNone(self.run_hook())

    def test_stop_hook_active_is_silent(self):
        self.add(user(), size(START, write=self.cursor), user(), size(START + 210000))
        self.assertIsNone(self.run_hook(active=True))

    def test_upkeep_off_is_silent(self):
        self.answer("upkeep:       off          2026-11-12")
        self.add(user(), size(START, write=self.cursor), user(), size(START + 210000))
        self.assertIsNone(self.run_hook())

    def test_upkeep_value_is_read_like_init_status(self):
        # `OFF` is off; `no` is not an answer init-status understands, so it stays on.
        self.add(user(), size(START, write=self.cursor), user(), size(START + 210000))
        self.answer("upkeep:       OFF          2026-11-12")
        self.assertIsNone(self.run_hook())
        self.answer("upkeep:       no           2026-11-12")
        self.assertEqual(self.run_hook()["decision"], "block")

    def test_no_block_when_the_block_cannot_be_remembered(self):
        # Unremembered, a block would come back every turn (F063): make the state file
        # unwritable — a folder in its place — and the hook must stay silent.
        self.add(user(), size(START, write=self.cursor), user(), size(START + 210000))
        self.assertEqual(self.run_hook()["decision"], "block")
        folder = os.path.join(self.tmp, "soul-upkeep-{}".format(os.getuid()))
        state = [os.path.join(folder, n) for n in os.listdir(folder)]
        self.assertEqual(len(state), 1, os.listdir(folder))
        os.remove(state[0])
        os.mkdir(state[0])
        self.assertIsNone(self.run_hook())

    def test_state_planted_in_the_shared_temp_folder_is_ignored(self):
        # Another local user can create a file in the shared temp folder first. The
        # remembered block once lived there by a name anyone could compute; a planted
        # line number past the end of the transcript silenced the block.
        self.add(user(), size(START, write=self.cursor), user(), size(START + 210000))
        h = hashlib.sha1(os.path.abspath(self.transcript).encode("utf-8")).hexdigest()[:12]
        with open(os.path.join(self.tmp, "soul-upkeep-" + h), "w") as f:
            f.write("999999999")
        self.assertEqual(self.run_hook()["decision"], "block")

    def untrusted_temp_folder(self):
        """The per-user temp folder made first by someone else: others may write it, and
        it holds a planted line number past the end of any transcript."""
        folder = os.path.join(self.tmp, "soul-upkeep-{}".format(os.getuid()))
        os.mkdir(folder)
        os.chmod(folder, 0o777)
        h = hashlib.sha1(os.path.abspath(self.transcript).encode("utf-8")).hexdigest()[:12]
        planted = os.path.join(folder, "soul-upkeep-" + h)
        with open(planted, "w") as f:
            f.write("999999999")
        return folder, planted

    def test_untrusted_temp_folder_falls_back_to_the_home_cache(self):
        # The planted value must not silence the block, and the block must still be
        # remembered — in ${XDG_CACHE_HOME:-~/.cache}/soul-upkeep — so the next stop is
        # silent although the cursor is still stale (F063: no block every turn).
        folder, planted = self.untrusted_temp_folder()
        self.add(user(), size(START, write=self.cursor), user(), size(START + 210000))
        for env, cache in ((None, self.xdg),
                           ({"XDG_CACHE_HOME": ""}, os.path.join(self.home, ".cache"))):
            with self.subTest(cache=cache):
                self.assertEqual(self.run_hook(env=env)["decision"], "block")
                self.assertIsNone(self.run_hook(env=env))
                state = os.path.join(cache, "soul-upkeep")
                self.assertEqual(os.stat(state).st_mode & 0o777, 0o700)
                self.assertEqual(len(os.listdir(state)), 1, os.listdir(state))
        # Nothing was read from or written to the untrusted folder.
        self.assertEqual(os.listdir(folder), [os.path.basename(planted)])
        with open(planted) as f:
            self.assertEqual(f.read(), "999999999")

    def test_no_trusted_folder_means_no_block(self):
        # Both the temp folder and the home-cache fallback are open to other users:
        # there is nowhere safe to remember the block, and an unremembered block would
        # come back every turn (F063), so the hook stays silent.
        self.untrusted_temp_folder()
        fallback = os.path.join(self.xdg, "soul-upkeep")
        os.makedirs(fallback)
        os.chmod(fallback, 0o777)
        self.add(user(), size(START, write=self.cursor), user(), size(START + 210000))
        self.assertIsNone(self.run_hook())
        self.assertEqual(os.listdir(fallback), [])

    def test_replies_without_a_reading_are_skipped(self):
        # A zero reading first would make the whole start-up load count as growth ...
        # (199k of growth: the start-up load on top would pass the step.)
        self.add(user(), zero(), size(START), user(), size(START + 199000))
        self.assertIsNone(self.run_hook())
        # ... and a zero reading last would hide real growth.
        self.records = []
        self.add(user(), size(START, write=self.cursor), user(), size(START + 210000), zero())
        self.assertEqual(self.run_hook()["decision"], "block")

    def test_malformed_input_fails_open(self):
        for raw in ("not json", "[1, 2]", json.dumps({"cwd": 7, "transcript_path": []})):
            self.assertIsNone(self.run_hook(raw=raw), raw)
        with open(self.transcript, "w") as f:  # garbage lines around a stale reading
            f.write("{broken\n" + json.dumps(size(START, write=self.cursor)) + "\n\x00\n"
                    + json.dumps(size(START + 210000)) + "\n")
        self.assertEqual(self.run_hook()["decision"], "block")

    def test_turn_off_hint_only_until_answered(self):
        self.add(user(), size(START, write=self.cursor), user(), size(START + 210000))
        self.assertIn("/soul-init revisit upkeep", self.run_hook()["reason"])
        self.add(user(), size(START + 420000))
        self.answer("upkeep:       on           2026-11-12")
        out = self.run_hook()
        self.assertEqual(out["decision"], "block")
        self.assertNotIn("revisit upkeep", out["reason"])

    def test_non_soul_project_is_silent(self):
        other = self.make_project("plain", soul=False)
        self.add(user(), size(START), user(), size(START + 210000))
        self.assertIsNone(self.run_hook(cwd=other))

    def test_no_cursor_yet_is_silent(self):
        bare = self.make_project("new", cursor=False)
        self.add(user(), size(START), user(), size(START + 210000), compact())
        self.assertIsNone(self.run_hook(cwd=bare))

    def test_summary_since_the_write_is_stale(self):
        self.add(user(), size(START, write=self.cursor), user(), size(START + 210000),
                 compact(), user("summary"), size(32000))
        out = self.run_hook()
        self.assertEqual(out["decision"], "block")
        self.assertIn("summary", out["reason"])

    def test_summary_soon_after_a_write_is_not_stale(self):
        # Under SUMMARY_GAP (max(half the step, 50,000)) of work between the write and the
        # summary: no second refresh (an adopting project's upstream note, 2026-11-16).
        # 90k: under the gap of 100,000 (SOUL-243), over the old 50,000.
        self.add(user(), size(START, write=self.cursor), user(), size(START + 90000),
                 compact(), user("summary"), size(32000))
        self.assertIsNone(self.run_hook())

    def test_growth_still_counts_across_an_ignored_summary(self):
        # 90k before the summary (ignored) + 120k after it = 210k: the step is reached.
        self.add(user(), size(START, write=self.cursor), user(), size(START + 90000),
                 compact(), user("summary"), size(30000), user(), size(150000))
        out = self.run_hook()
        self.assertEqual(out["decision"], "block")
        self.assertNotIn("summary", out["reason"])

    def test_summary_exactly_at_the_gap_is_stale(self):
        self.add(user(), size(START, write=self.cursor), user(), size(START + 100000),
                 compact(), user("summary"), size(32000))
        self.assertEqual(self.run_hook()["decision"], "block")

    def test_two_summaries_sum_their_work(self):
        # 60k before the first summary (ignored) + 45k before the second = 105k: stale.
        self.add(user(), size(START, write=self.cursor), user(), size(START + 60000),
                 compact(), user("summary"), size(30000), user(), size(75000),
                 compact(), user("summary"), size(30000))
        out = self.run_hook()
        self.assertEqual(out["decision"], "block")
        self.assertIn("summary", out["reason"])

    def test_reason_keeps_the_reply_as_the_answer(self):
        self.add(user(), size(START, write=self.cursor), user(), size(START + 220000))
        out = self.run_hook()
        self.assertIn("stays the answer", out["reason"])
        self.assertNotIn("then stop", out["reason"])

    def test_refresh_after_summary_is_fresh(self):
        self.add(user(), size(START, write=self.cursor), compact(), user("summary"),
                 size(32000), size(33000, write=self.cursor), user(), size(60000))
        self.assertIsNone(self.run_hook())

    def test_cursor_from_an_earlier_session_counts_from_session_start(self):
        # No write in this transcript: growth is measured from the first reading,
        # so the start-up load is not counted as conversation.
        self.add(user(), size(START), user(), size(START + 199000))
        self.assertIsNone(self.run_hook())
        self.add(user(), size(START + 201000))
        self.assertEqual(self.run_hook()["decision"], "block")

    def test_subagent_records_are_not_counted(self):
        self.add(user(), size(START, write=self.cursor), user(), size(START + 10000),
                 size(400000, sidechain=True))
        self.assertIsNone(self.run_hook())

    def test_write_through_a_vault_link_counts(self):
        vault = os.path.join(self.base, "vault", "soul")
        os.makedirs(vault)
        with open(os.path.join(vault, "handoff.md"), "w") as f:
            f.write("# Handoff cursor\n")
        linked = os.path.join(self.base, "linked")
        os.makedirs(linked)
        with open(os.path.join(linked, "witness.md"), "w") as f:
            f.write("# Witness\n")
        os.symlink(vault, os.path.join(linked, ".soul"))
        # The session wrote through the link; the hook compares real paths, so the
        # write still counts, and so does one to the vault's own path.
        for path in (os.path.join(linked, ".soul", "handoff.md"),
                     os.path.join(vault, "handoff.md")):
            self.records = []
            # 220k past the session's start: a write that did not count would block.
            self.add(user(), size(START), size(START + 210000, write=path), user(),
                     size(START + 220000))
            self.assertIsNone(self.run_hook(cwd=linked), path)

    # ------------------------------------------------------------- after a summary

    def test_compact_start_says_refresh_first(self):
        out = self.run_hook("--compact")
        ctx = out["hookSpecificOutput"]["additionalContext"]
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "SessionStart")
        self.assertIn("re-read .soul/handoff.md", ctx)
        self.assertIn("only when the Stop check asks", ctx)

    def test_compact_start_silent_when_off_or_no_cursor(self):
        self.answer("upkeep:       off          2026-11-12")
        self.assertIsNone(self.run_hook("--compact"))
        bare = self.make_project("new", cursor=False)
        self.assertIsNone(self.run_hook("--compact", cwd=bare))

    # ------------------------------------------------------------- SOUL-243

    def new_session(self):
        """Another session in the same project: its own transcript, so its own state."""
        self.transcript = os.path.join(self.base, "session-{}.jsonl".format(len(os.listdir(
            self.base))))
        self.records = []

    def write(self, rel, text, project=None):
        path = os.path.join(project or self.project, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        return path

    def test_cursor_written_by_a_shell_counts(self):
        # A cursor updated by a script leaves no Write call; its content changed, so it
        # was written (field report, SOUL-243). 110k of work then a summary is stale only
        # if counted from the session's start.
        self.add(user(), size(START))
        self.assertIsNone(self.run_hook())  # the first stop stores the cursor's hash
        with open(self.cursor, "a") as f:
            f.write("NEXT STEP: the script's line\n")
        self.add(user(), size(START + 110000), compact(), user("summary"), size(32000))
        self.assertIsNone(self.run_hook())
        # Growth counts from the stop that saw the change.
        self.add(user(), size(32000 + 199000))
        self.assertIsNone(self.run_hook())
        self.add(user(), size(32000 + 201000))
        self.assertIn("about 201k tokens", self.run_hook()["reason"])

    def test_state_from_3_13_2_still_reads(self):
        # 3.13.2 remembered a bare line number: the line it blocked at (here, the last).
        self.add(user(), size(START, write=self.cursor), user(), size(START + 210000))
        folder = os.path.join(self.tmp, "soul-upkeep-{}".format(os.getuid()))
        os.mkdir(folder, 0o700)
        h = hashlib.sha1(os.path.abspath(self.transcript).encode("utf-8")).hexdigest()[:12]
        with open(os.path.join(folder, "soul-upkeep-" + h), "w") as f:
            f.write("3")
        self.assertIsNone(self.run_hook())
        self.add(user(), size(START + 420000))
        self.assertEqual(self.run_hook()["decision"], "block")

    def test_background_agent_blocks_once_per_cursor_write(self):
        self.add(user(), size(START, write=self.cursor), *launch("a1", "Audit hooks"),
                 user(), size(START + 5000))
        out = self.run_hook()
        self.assertIn("background work is running that the cursor does not mention: "
                      "add a line for it (Audit hooks)", out["reason"])
        self.assertNotIn("stale", out["reason"])
        self.add(user(), size(START + 6000))
        self.assertIsNone(self.run_hook())  # once per cursor write
        # A new cursor write, then another launch: asked again, for the new one only.
        self.add(size(START + 7000, write=self.cursor),
                 *launch("a2", "Map consumers", START + 8000), size(START + 9000))
        reason = self.run_hook()["reason"]
        self.assertIn("(Map consumers)", reason)
        self.assertNotIn("Audit hooks", reason)

    def test_background_bash_blocks(self):
        self.add(user(), size(START, write=self.cursor), *launch("b1", "Full suite", bash=True),
                 size(START + 5000))
        self.assertIn("add a line for it (Full suite)", self.run_hook()["reason"])

    def test_background_work_that_ended_is_silent(self):
        ends = {"notified": [notice("a1")],
                "notified while busy": [notice("a1", queued=True)],
                "killed": [notice("a1", "killed")], "failed": [notice("a1", "failed")],
                "stopped at session end": [notice("a1", "stopped")],
                "TaskStop": task_stop("a1"),
                # one agent can notify more than once; any final status ends it
                "notified twice": [notice("a1"), notice("a1")]}
        for name, end in ends.items():
            with self.subTest(end=name):
                self.new_session()
                self.add(user(), size(START, write=self.cursor), *launch("a1"), *end,
                         size(START + 5000))
                self.assertIsNone(self.run_hook())
        with self.subTest(end="launched before the cursor write"):
            self.new_session()
            self.add(user(), size(START), *launch("a1"), size(START + 3000, write=self.cursor),
                     size(START + 5000))
            self.assertIsNone(self.run_hook())

    def test_quoted_notification_does_not_end_the_task(self):
        # Tool output that quotes a notification (a Read of a transcript or of this file)
        # is not a delivered one.
        quoted = notice("a1")["message"]["content"]
        self.add(user(), size(START, write=self.cursor), *launch("a1"), size(START + 3000),
                 {"type": "user", "isSidechain": False, "message": {"role": "user", "content": [
                     {"tool_use_id": "toolu_read", "type": "tool_result", "content": quoted}]}},
                 size(START + 5000))
        self.assertEqual(self.run_hook()["decision"], "block")

    def test_background_after_an_obeyed_block_is_reported(self):
        # The session obeys a block: rewrites the cursor, then stops with
        # stop_hook_active. That stop must still store the new hash, or the next normal
        # stop sees a "changed" cursor, moves the write point past the next turn, and
        # misses that turn's launch (review of 85bb6c4).
        self.add(user(), size(START, write=self.cursor), user(), size(START + 210000))
        self.assertEqual(self.run_hook()["decision"], "block")
        with open(self.cursor, "w") as f:
            f.write("# Handoff cursor\nrefreshed\n")
        self.add(size(START + 212000, write=self.cursor))
        self.assertIsNone(self.run_hook(active=True))  # never blocks there
        self.add(user(), *launch("a9", "Long audit", START + 214000), size(START + 215000))
        self.assertIn("add a line for it (Long audit)", self.run_hook()["reason"])

    def test_one_notification_can_end_several_tasks(self):
        # Claude Code's resume summary lists every task that did not finish in one
        # notification: several task-ids, status stopped. Each of them has ended.
        text = ("<task-notification>\n<task-id>a1</task-id>\n<task-id>b1</task-id>\n"
                "<status>stopped</status>\n<summary>Background tasks didn't finish before "
                "the previous session ended</summary>\n</task-notification>")
        self.add(user(), size(START, write=self.cursor), *launch("a1"),
                 *launch("b1", "Suite", START + 2000, bash=True),
                 {"type": "user", "isSidechain": False,
                  "message": {"role": "user", "content": text}},
                 size(START + 5000))
        self.assertIsNone(self.run_hook())

    def long_cursor(self, lines):
        with open(self.cursor, "w") as f:
            f.write("".join("- line {}\n".format(i) for i in range(lines)))

    def test_long_cursor_asks_once_a_day_per_project(self):
        self.long_cursor(151)
        self.add(user(), size(START, write=self.cursor), user(), size(START + 5000))
        out = self.run_hook()
        self.assertIn("the cursor is 151 lines: delete finished items and flush history to "
                      "the witness log", out["reason"])
        self.add(user(), size(START + 6000))
        self.assertIsNone(self.run_hook())
        self.new_session()  # a new session the same day: not asked again
        self.add(user(), size(START), user(), size(START + 5000))
        self.assertIsNone(self.run_hook())

    def test_cursor_at_the_limit_is_silent(self):
        self.long_cursor(150)
        self.add(user(), size(START, write=self.cursor), user(), size(START + 5000))
        self.assertIsNone(self.run_hook())

    def test_mind_due_asks_once_a_day_per_project(self):
        self.write("mind.md", "# Mind\n\n**Last distilled:** 2026-11-01 against SOUL-001\n")
        # Entries dated on the stamp's own day do not count; 15 after it do.
        self.write("witness.md", witness(*(["2026-11-01"] * 3 + ["2026-11-02"] * 15)))
        self.add(user(), size(START), user(), size(START + 5000))
        out = self.run_hook()
        self.assertIn("the Mind is due: run /soul-distill (15 witness entries dated after its "
                      "last distill, 2026-11-01)", out["reason"])
        self.new_session()
        self.add(user(), size(START), user(), size(START + 5000))
        self.assertIsNone(self.run_hook())

    def test_mind_not_due(self):
        cases = {"14 entries": ("mind.md", "2026-11-01", 14),
                 "no mind.md": (None, None, 30),
                 "no stamp": ("mind.md", None, 30)}
        for name, (mind, stamp, n) in cases.items():
            with self.subTest(case=name):
                p = self.make_project(name.replace(" ", "-"))
                self.write("witness.md", witness(*["2026-11-02"] * n), p)
                if mind:
                    self.write(mind, "# Mind\n" + ("\n**Last distilled:** {} x\n".format(stamp)
                                                   if stamp else ""), p)
                self.new_session()
                self.add(user(), size(START), user(), size(START + 5000))
                self.assertIsNone(self.run_hook(cwd=p))

    def test_mind_due_with_stores_in_soul_folder(self):
        p = self.make_project("dotsoul", soul=False)
        self.write(os.path.join(".soul", "witness.md"), witness(*["2026-11-02"] * 16), p)
        self.write(os.path.join(".soul", "mind.md"), "**Last distilled:** 2026-11-01\n", p)
        self.add(user(), size(START), user(), size(START + 5000))
        self.assertIn("the Mind is due", self.run_hook(cwd=p)["reason"])

    def answers(self, project):
        spec = importlib.util.spec_from_file_location(
            "soul_init_status", os.path.join(os.path.dirname(_HERE), "tools", "init-status.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.read_answers(project)

    def test_upkeep_recorded_on_after_three_reminders(self):
        today = time.strftime("%Y-%m-%d")
        for existing in (None, "stage:        prototype    2026-11-01"):  # no newline at end
            with self.subTest(existing=existing):
                p = self.make_project("e-{}".format(bool(existing)))
                if existing:
                    self.write(os.path.join(".soul", "init.md"), existing, p)
                self.new_session()
                self.add(user(), size(START, write=os.path.join(p, ".soul", "handoff.md")))
                for i in (1, 2, 3, 4):
                    self.add(user(), size(START + 201000 * i))
                    reason = self.run_hook(cwd=p)["reason"]
                    if i < 3:
                        self.assertIn("to turn this off: /soul-init revisit upkeep", reason)
                    elif i == 3:
                        self.assertIn("it is now recorded as on in .soul/init.md", reason)
                        self.assertIn("/soul-init revisit upkeep changes it", reason)
                    else:
                        self.assertNotIn("revisit upkeep", reason)
                lines, got = self.answers(p)
                self.assertEqual(got["upkeep"], ("on", today))
                if existing:
                    self.assertEqual(got["stage"], ("prototype", "2026-11-01"))
                    self.assertEqual(lines[0], existing)

    def test_all_due_reasons_make_one_block_highest_first(self):
        self.long_cursor(160)
        self.write("mind.md", "**Last distilled:** 2026-11-01\n")
        self.write("witness.md", witness(*["2026-11-02"] * 20))
        self.add(user(), size(START, write=self.cursor), *launch("a1"), user(),
                 size(START + 210000))
        reason = self.run_hook()["reason"]
        order = [reason.index(s) for s in ("background work is running", "it is stale",
                                           "the cursor is 160 lines", "the Mind is due")]
        self.assertEqual(order, sorted(order))
        self.assertEqual(reason.count('starts with "☀  "'), 1)
        self.assertEqual(reason.count("stays the answer"), 1)
        self.assertIsNone(self.run_hook())  # all remembered: the next stop is silent

    # ------------------------------------------------------------- at session start

    def held(self, text, name="mind-held-2026-11-17.md", project=None):
        return self.write(os.path.join(".ai", "distill", name), text, project)

    def start_line(self, **kw):
        out = self.run_hook("--start", **kw)
        if out is None:
            return None
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "SessionStart")
        return out["hookSpecificOutput"]["additionalContext"]

    def test_start_names_held_mind_changes(self):
        self.held("# Held\n\n## Changes\n\n- cut item 4\n- merge 2 and 6\n  - detail\n"
                  "- reword 9\n\n## Draft\n\n- not a change\n")
        self.assertIn("☀  3 Mind changes wait for your yes: "
                      ".ai/distill/mind-held-2026-11-17.md", self.start_line())

    def test_start_held_file_not_countable(self):
        self.held("A full draft of the Mind, no list of changes.\n")
        self.assertIn("☀  Mind changes wait for your yes: "
                      ".ai/distill/mind-held-2026-11-17.md", self.start_line())

    def test_start_counts_only_a_changes_heading(self):
        # Only a heading that is exactly `## Changes` (any case) holds the count; the
        # distill skill writes one `- ` line per waiting change there.
        self.held("# Held\n\n## Unchanged items\n\n- a\n- b\n\n## Exchange notes\n- c\n")
        self.assertIn("☀  Mind changes wait for your yes:", self.start_line())
        self.held("# Held\n\n## CHANGES\n\n- cut item 4\n\n## Draft\n- not one\n")
        self.assertIn("☀  1 Mind change waits for your yes:", self.start_line())

    def test_start_silent_without_held_file_or_when_off(self):
        self.assertIsNone(self.start_line())
        self.held("x", name="mind-declined-2026-11-17.md")
        self.assertIsNone(self.start_line())
        self.held("## Changes\n- one\n")
        self.answer("upkeep:       off          2026-11-12")
        self.assertIsNone(self.start_line())
        plain = self.make_project("plain", soul=False)
        self.held("## Changes\n- one\n", project=plain)
        self.assertIsNone(self.start_line(cwd=plain))

    def test_start_is_wired_for_startup_and_resume(self):
        with open(os.path.join(_HERE, "hooks.json"), encoding="utf-8") as f:
            entries = json.load(f)["hooks"]["SessionStart"]
        wired = [e.get("matcher") for e in entries
                 for h in e["hooks"] if h["command"].endswith('upkeep.py" --start')]
        self.assertEqual(wired, ["startup|resume"])


if __name__ == "__main__":
    unittest.main()
