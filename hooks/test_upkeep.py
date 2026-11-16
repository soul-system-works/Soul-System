"""Behaviour test for hooks/upkeep.py, the handoff-cursor staleness hook (SOUL-A032).

FENCE: the hook is silent unless the cursor is stale, and blocks once per staleness.
F063 and mind item 5: a Stop hook that fired on every turn was the reason the
completion gate's regex was narrowed, and a hook that nags gets switched off. So a
fresh cursor, `stop_hook_active`, `upkeep: off`, a non-Soul project and a project with
no cursor yet must all print nothing; a stale cursor (about 100,000 tokens of new
conversation, or a summary) blocks once and not again until it is stale again. That
holds when the per-user temp folder cannot be trusted too: the block is remembered in
the home cache instead. With no trusted folder at all the hook cannot remember, so it
does not block (F063).

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
import unittest

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
        # 99k after the write: just under the step, so a lower step would block here.
        self.add(user(), size(START), size(START + 5000, write=self.cursor), user(),
                 size(START + 104000))
        self.assertIsNone(self.run_hook())

    def test_growth_blocks_once(self):
        self.add(user(), size(START, write=self.cursor), user(), size(START + 101000))
        out = self.run_hook()
        self.assertEqual(out["decision"], "block")
        self.assertIn("/soul-handoff", out["reason"])
        self.assertIn("about 101k tokens", out["reason"])
        # The owner's sun mark starts a line about what Soul did on its own (SOUL-239).
        self.assertIn('in one line that starts with "\u2600  "', out["reason"])
        # The next turn ignores the block and stops again: no second block ...
        self.add(user(), size(START + 110000))
        self.assertIsNone(self.run_hook())
        # ... until another 100,000 tokens have passed.
        self.add(user(), size(START + 202000))
        self.assertEqual(self.run_hook()["decision"], "block")

    def test_growth_counts_from_the_cursor_write(self):
        # 99k after the write is fresh, even though the session is 249k past its start.
        self.add(user(), size(START), size(START + 150000, write=self.cursor), user(),
                 size(START + 249000))
        self.assertIsNone(self.run_hook())

    def test_stop_hook_active_is_silent(self):
        self.add(user(), size(START, write=self.cursor), user(), size(START + 110000))
        self.assertIsNone(self.run_hook(active=True))

    def test_upkeep_off_is_silent(self):
        self.answer("upkeep:       off          2026-11-12")
        self.add(user(), size(START, write=self.cursor), user(), size(START + 110000))
        self.assertIsNone(self.run_hook())

    def test_upkeep_value_is_read_like_init_status(self):
        # `OFF` is off; `no` is not an answer init-status understands, so it stays on.
        self.add(user(), size(START, write=self.cursor), user(), size(START + 110000))
        self.answer("upkeep:       OFF          2026-11-12")
        self.assertIsNone(self.run_hook())
        self.answer("upkeep:       no           2026-11-12")
        self.assertEqual(self.run_hook()["decision"], "block")

    def test_no_block_when_the_block_cannot_be_remembered(self):
        # Unremembered, a block would come back every turn (F063): make the state file
        # unwritable — a folder in its place — and the hook must stay silent.
        self.add(user(), size(START, write=self.cursor), user(), size(START + 110000))
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
        self.add(user(), size(START, write=self.cursor), user(), size(START + 110000))
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
        self.add(user(), size(START, write=self.cursor), user(), size(START + 110000))
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
        self.add(user(), size(START, write=self.cursor), user(), size(START + 110000))
        self.assertIsNone(self.run_hook())
        self.assertEqual(os.listdir(fallback), [])

    def test_replies_without_a_reading_are_skipped(self):
        # A zero reading first would make the whole start-up load count as growth ...
        # (99k of growth: the start-up load on top would pass the step.)
        self.add(user(), zero(), size(START), user(), size(START + 99000))
        self.assertIsNone(self.run_hook())
        # ... and a zero reading last would hide real growth.
        self.records = []
        self.add(user(), size(START, write=self.cursor), user(), size(START + 110000), zero())
        self.assertEqual(self.run_hook()["decision"], "block")

    def test_malformed_input_fails_open(self):
        for raw in ("not json", "[1, 2]", json.dumps({"cwd": 7, "transcript_path": []})):
            self.assertIsNone(self.run_hook(raw=raw), raw)
        with open(self.transcript, "w") as f:  # garbage lines around a stale reading
            f.write("{broken\n" + json.dumps(size(START, write=self.cursor)) + "\n\x00\n"
                    + json.dumps(size(START + 110000)) + "\n")
        self.assertEqual(self.run_hook()["decision"], "block")

    def test_turn_off_hint_only_until_answered(self):
        self.add(user(), size(START, write=self.cursor), user(), size(START + 110000))
        self.assertIn("/soul-init revisit upkeep", self.run_hook()["reason"])
        self.add(user(), size(START + 220000))
        self.answer("upkeep:       on           2026-11-12")
        out = self.run_hook()
        self.assertEqual(out["decision"], "block")
        self.assertNotIn("revisit upkeep", out["reason"])

    def test_non_soul_project_is_silent(self):
        other = self.make_project("plain", soul=False)
        self.add(user(), size(START), user(), size(START + 110000))
        self.assertIsNone(self.run_hook(cwd=other))

    def test_no_cursor_yet_is_silent(self):
        bare = self.make_project("new", cursor=False)
        self.add(user(), size(START), user(), size(START + 110000), compact())
        self.assertIsNone(self.run_hook(cwd=bare))

    def test_summary_since_the_write_is_stale(self):
        self.add(user(), size(START, write=self.cursor), user(), size(START + 60000),
                 compact(), user("summary"), size(32000))
        out = self.run_hook()
        self.assertEqual(out["decision"], "block")
        self.assertIn("summary", out["reason"])

    def test_summary_soon_after_a_write_is_not_stale(self):
        # Under SUMMARY_GAP (max(half the step, 50,000)) of work between the write and the
        # summary: no second refresh (an adopting project's upstream note, 2026-11-16).
        self.add(user(), size(START, write=self.cursor), user(), size(START + 20000),
                 compact(), user("summary"), size(32000))
        self.assertIsNone(self.run_hook())

    def test_growth_still_counts_across_an_ignored_summary(self):
        # 40k before the summary (ignored) + 70k after it = 110k: the step is reached.
        self.add(user(), size(START, write=self.cursor), user(), size(START + 40000),
                 compact(), user("summary"), size(30000), user(), size(100000))
        out = self.run_hook()
        self.assertEqual(out["decision"], "block")
        self.assertNotIn("summary", out["reason"])

    def test_reason_keeps_the_reply_as_the_answer(self):
        self.add(user(), size(START, write=self.cursor), user(), size(START + 120000))
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
        self.add(user(), size(START), user(), size(START + 99000))
        self.assertIsNone(self.run_hook())
        self.add(user(), size(START + 101000))
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
            # 120k past the session's start: a write that did not count would block.
            self.add(user(), size(START), size(START + 110000, write=path), user(),
                     size(START + 120000))
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


if __name__ == "__main__":
    unittest.main()
