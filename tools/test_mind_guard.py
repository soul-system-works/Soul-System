"""Behaviour test for tools/mind-guard.py, the mechanical brake on a Mind change.

FENCE: /soul-distill applies a Mind change on its own only when it is minor (SOUL-A032).
The model grades the change, and its grade can be wrong in the flattering direction
(mind item 2), so this script must fail — exit 1, saying why — whenever an old item
number is gone (a cut, a merge, a renumbering) or an old item no longer cites a record
id it cited (an item without its incident gets reinterpreted, F053/A020). A pure
addition or a rewording that keeps every id must pass, or every distill is held —
and the `**Last distilled:**` stamp, which every distill rewrites, is never checked.
The first build counted items and ids over the whole file: the stamp made every real
distill major, and a cut plus an addition passed (fresh-context review, 2026-11-12).

Each case writes an old and a new mind.md to a temp folder and runs the script as
/soul-distill does.

Run: python3 tools/test_mind_guard.py  (exit 0 = PASS)
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest

_TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mind-guard.py")
_MIND = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mind.md")

OLD = """# Project notes — MODEL-LIB

## Carry these (project-specific, not re-derivable)

1. **The calibration lean.** Counts come out generous (SOUL-155, F063).
2. **Never run filter-repo on the mount.** It stalls silently (SOUL-169, SOUL-F038).
3. **Measure the turn, not the block.** Per block reads 170 chars (THERMAL-I086, A022).

---
**Last distilled:** 2026-11-01 against SOUL-234
"""


class MindGuard(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="soul-mind-guard-test-")
        self.addCleanup(shutil.rmtree, self.dir, True)

    def guard(self, new, old=OLD):
        paths = []
        for name, text in (("old.md", old), ("new.md", new)):
            p = os.path.join(self.dir, name)
            with open(p, "w", encoding="utf-8") as f:
                f.write(text)
            paths.append(p)
        r = subprocess.run([sys.executable, _TOOL, *paths], capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def test_unchanged_passes(self):
        code, out = self.guard(OLD)
        self.assertEqual(code, 0, out)
        self.assertIn("items 3 -> 3", out)

    def test_new_item_and_rewording_pass(self):
        new = OLD.replace("It stalls silently", "It stalls with no error").replace(
            "---", "4. **A new trap.** Found once (SOUL-240).\n\n---")
        code, out = self.guard(new)
        self.assertEqual(code, 0, out)
        self.assertIn("items 3 -> 4", out)

    def test_cut_item_fails(self):
        new = OLD.replace("2. **Never run filter-repo on the mount.** It stalls silently "
                          "(SOUL-169, SOUL-F038).\n", "")
        code, out = self.guard(new)
        self.assertEqual(code, 1, out)
        self.assertIn("item(s) 2 are gone", out)

    def test_merge_fails_even_when_ids_are_kept(self):
        new = OLD.replace("(SOUL-155, F063).\n2. **Never run filter-repo on the mount.**",
                          "(SOUL-155, F063). Also never run filter-repo on the mount:")
        code, out = self.guard(new)
        self.assertEqual(code, 1, out)
        self.assertIn("item(s) 2 are gone", out)

    def test_dropped_incident_id_fails(self):
        new = OLD.replace("(SOUL-155, F063)", "(F063)")
        code, out = self.guard(new)
        self.assertEqual(code, 1, out)
        self.assertIn("item 1 no longer cites: SOUL-155", out)

    def test_project_codes_and_bare_ids_are_ids(self):
        new = OLD.replace("(THERMAL-I086, A022)", "(measured)")
        code, out = self.guard(new)
        self.assertEqual(code, 1, out)
        self.assertIn("THERMAL-I086", out)
        self.assertIn("A022", out)
        old = OLD.replace("(THERMAL-I086, A022)", "(THERMAL-I086, A022, PLANT-BOP-12)")
        code, out = self.guard(OLD, old=old)
        self.assertEqual(code, 1, out)
        self.assertIn("item 3 no longer cites: PLANT-BOP-12", out)

    def test_bare_id_may_gain_a_code_but_not_lose_one(self):
        code, out = self.guard(OLD.replace("F063", "SOUL-F063"))
        self.assertEqual(code, 0, out)
        code, out = self.guard(OLD.replace("SOUL-F038", "F038"))
        self.assertEqual(code, 1, out)
        self.assertIn("SOUL-F038", out)

    def test_fenced_and_indented_numbers_are_not_items(self):
        old = OLD.replace("---", "```\n1. not an item\n7. nor this (SOUL-777)\n```\n"
                                 "   4. nested\n---")
        code, out = self.guard(OLD, old=old)
        self.assertEqual(code, 0, out)
        self.assertIn("items 3 -> 3", out)

    def test_the_stamp_is_not_checked(self):
        # This repo's own Mind, a new last item and a rewritten stamp: a plain distill.
        with open(_MIND, encoding="utf-8") as f:
            mind = f.read()
        head, _, _ = mind.rpartition("\n---\n")
        new = (head + "\n99. **A new trap.** Found once (SOUL-999).\n\n---\n"
               "**Last distilled:** 2026-11-12 against SOUL-999. Added: 99.\n")
        code, out = self.guard(new, old=mind)
        self.assertEqual(code, 0, out)
        code, out = self.guard(OLD.replace("against SOUL-234", "against SOUL-240"))
        self.assertEqual(code, 0, out)

    def test_cut_plus_addition_fails(self):
        new = OLD.replace("2. **Never run filter-repo on the mount.** It stalls silently "
                          "(SOUL-169, SOUL-F038).\n", "").replace(
            "---", "4. **A new trap.** Found once (SOUL-240).\n\n---")
        code, out = self.guard(new)
        self.assertEqual(code, 1, out)
        self.assertIn("item(s) 2 are gone", out)

    def test_cut_of_an_item_cited_elsewhere_fails(self):
        old = OLD.replace("(SOUL-155, F063)", "(SOUL-155, F063, SOUL-169, SOUL-F038)")
        new = old.replace("2. **Never run filter-repo on the mount.** It stalls silently "
                          "(SOUL-169, SOUL-F038).\n", "2. **Renamed.** No ids now.\n")
        code, out = self.guard(new, old=old)
        self.assertEqual(code, 1, out)
        self.assertIn("item 2 no longer cites: SOUL-169, SOUL-F038", out)

    def test_an_id_moved_to_another_item_counts_as_dropped(self):
        new = OLD.replace("(SOUL-155, F063)", "(F063)").replace("(SOUL-169,", "(SOUL-155, SOUL-169,")
        code, out = self.guard(new)
        self.assertEqual(code, 1, out)
        self.assertIn("item 1 no longer cites: SOUL-155", out)

    def test_a_mind_without_numbered_items_is_checked_whole(self):
        old = "# Notes\n\n## Rules\n- Keep the lean (SOUL-155).\n- Mount (SOUL-169).\n"
        code, out = self.guard("# Notes\n\n1. **Lean.** (SOUL-155)\n", old=old)
        self.assertEqual(code, 1, out)
        self.assertIn("SOUL-169", out)
        code, out = self.guard("# Notes\n\n1. **Lean.** (SOUL-155)\n2. **Mount.** "
                               "(SOUL-169)\n", old=old)
        self.assertEqual(code, 0, out)

    def test_unreadable_file_is_exit_2(self):
        r = subprocess.run([sys.executable, _TOOL, os.path.join(self.dir, "missing.md"),
                            os.path.join(self.dir, "missing.md")],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
