"""Behaviour test for tools/ideas-status.py, the open-ideas report (SOUL-I096).

FENCE: a long ideas store hides open work, so each idea carries one STATUS line and
this script prints the open ones. It must find ideas in all three shapes real stores
use — a field block (`ID:` line, inside ``` fences in this repo), a `- **<id>**`
list item, a `##`/`###`/`####` heading — and it must never guess a state: a word
that is not exactly Raw, Maturing, Parked, Built or Declined is reported as unknown
("Maturing (discussed …)" is not Maturing, "Built in part" is not Built), an idea
with no STATUS or with two is reported, and a STATUS that sits after a non-idea
heading belongs to no idea. It is a report, not a gate: exit 0 whenever it ran,
exit 2 only when the store cannot be read.

Each case writes a store to a temp folder and runs the script as a session does.

Run: python3 tools/test_ideas_status.py  (exit 0 = PASS)
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

_TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ideas-status.py")

HEADER = """# Ideas — SOUL

Capture with /soul-capture idea. Format:

```
ID:        [CODE]-I###          e.g. SOUL-I001
STATUS:    Raw | Maturing | Parked | Built | Declined
```

STATUS: Raw
"""

FIELD = HEADER + """
## Ideas

```
ID:        SOUL-I001
WHEN:      2026-11-01
RAW:       A first   **raw** idea
STATUS:    Raw
```

```
ID:        SOUL-I002
WHEN:      2026-11-02
IDEA:      An older entry with IDEA, not RAW
STATUS:    Built — v3.13.0
```

```
ID:        SOUL-I003
WHEN:      2026-11-03
RAW:       Third
STATUS:    Maturing — discussed 2026-11-20
```

```
ID:        SOUL-I004
WHEN:      2026-11-04
RAW:       Fourth
STATUS:    Parked — after the release
```

```
ID:        SOUL-I005
WHEN:      2026-11-05
RAW:       Fifth
STATUS:    Declined
```
"""

LIST = """# Ideas — MODEL-LIB

- **MODEL-LIB-I001** — A style guide for the library
  (owner, 2026-11-13).
  STATUS: Maturing — discussed 2026-11-14
- **MODEL-LIB-I002** · Keep open work findable
  STATUS: Raw
- **MODEL-LIB-I003** - Test against a second tool
  STATUS: Built — 2026-11-20
- **MODEL-LIB-I004** — Parked one
  STATUS: Parked
- **MODEL-LIB-I005** — Declined one
  **STATUS:** Declined — not needed
"""

HEADING = """# Ideas — THERMAL

## THERMAL-I001 — One command that reruns everything
STATUS: Raw

### Round 1
Discussed.

### THERMAL-I002: The workflow doc as a recipe
STATUS: Maturing

#### THERMAL-I003 · Split the data repo
STATUS: Parked — until the move

## THERMAL-I004 — Calibrate the heater
STATUS: Built — v2

## THERMAL-I005 — Drop the old run
STATUS: Declined
"""


class IdeasStatus(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="soul-ideas-status-test-")
        self.addCleanup(shutil.rmtree, self.dir, True)

    def write(self, text, rel="ideas.md"):
        p = os.path.join(self.dir, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        return p

    def run_tool(self, *args):
        r = subprocess.run([sys.executable, _TOOL, *args], capture_output=True, text=True)
        return r.returncode, r.stdout, r.stderr

    def report(self, text):
        code, out, err = self.run_tool(self.write(text), "--json")
        self.assertEqual(code, 0, err)
        return json.loads(out)

    def counts(self, rep):
        return ([(i["id"], i["state"]) for i in rep["open"]], rep["parked"],
                rep["closed_counts"])

    def test_field_blocks_inside_fences(self):
        rep = self.report(FIELD)
        self.assertEqual(self.counts(rep), (
            [("SOUL-I001", "Raw"), ("SOUL-I003", "Maturing")], ["SOUL-I004"],
            {"Built": 1, "Declined": 1}))
        self.assertEqual(rep["open"][0]["title"], "A first raw idea")
        self.assertEqual(rep["no_state"] + rep["unknown"] + rep["duplicate"], [])

    def test_field_block_without_raw_shows_idea_line(self):
        rep = self.report(FIELD.replace("STATUS:    Built — v3.13.0", "STATUS:    Raw"))
        self.assertEqual(rep["open"][1], {"id": "SOUL-I002", "state": "Raw",
                                          "title": "An older entry with IDEA, not RAW"})

    def test_list_items_with_indented_status(self):
        rep = self.report(LIST)
        self.assertEqual(self.counts(rep), (
            [("MODEL-LIB-I001", "Maturing"), ("MODEL-LIB-I002", "Raw")],
            ["MODEL-LIB-I004"], {"Built": 1, "Declined": 1}))
        self.assertEqual(rep["open"][0]["title"], "A style guide for the library")
        # The ` · ` separator is dropped from the title too.
        self.assertEqual(rep["open"][1]["title"], "Keep open work findable")

    def test_list_item_with_title_inside_the_bold(self):
        # A real store writes `- **CODE-I010 — Title.**`: the separator sits inside
        # the bold. It must still be an idea, or the whole store reads as empty.
        rep = self.report("- **PLANT-I010 — Two pumps in series.** More text.\n"
                          "  STATUS:    Raw\n"
                          "- **PLANT-I011 · A second one**\n  STATUS:    Built\n")
        self.assertEqual(self.counts(rep), ([("PLANT-I010", "Raw")], [], {"Built": 1, "Declined": 0}))
        self.assertEqual(rep["open"][0]["title"], "Two pumps in series. More text.")

    def test_heading_shapes(self):
        rep = self.report(HEADING)
        self.assertEqual(self.counts(rep), (
            [("THERMAL-I001", "Raw"), ("THERMAL-I002", "Maturing")], ["THERMAL-I003"],
            {"Built": 1, "Declined": 1}))
        self.assertEqual(rep["open"][0]["title"], "One command that reruns everything")
        self.assertEqual(rep["open"][1]["title"], "The workflow doc as a recipe")

    def test_plain_text_report(self):
        code, out, err = self.run_tool(self.write(HEADING))
        self.assertEqual(code, 0, err)
        lines = out.splitlines()
        self.assertTrue(lines[0].endswith(
            ": 2 open (Raw 1, Maturing 1) · 1 parked · 2 closed (Built 1, Declined 1)"),
            out)
        self.assertEqual(lines[1].split(), ["THERMAL-I001", "Raw", "One", "command",
                                            "that", "reruns", "everything"])
        self.assertEqual(lines[3], "Parked: THERMAL-I003")
        self.assertEqual(len(lines), 4, out)

    def test_non_idea_heading_ends_the_idea(self):
        text = ("## THERMAL-I001 — First\nSome notes.\n\n## Closed section\n"
                "STATUS: Built\n\n## THERMAL-I002 — Second\nSTATUS: Raw\n")
        rep = self.report(text)
        self.assertEqual(rep["no_state"], ["THERMAL-I001"])
        self.assertEqual(rep["closed_counts"], {"Built": 0, "Declined": 0})
        self.assertEqual([i["id"] for i in rep["open"]], ["THERMAL-I002"])

    def test_unknown_words_are_not_mapped(self):
        text = ("## TEACH-I001 — One\nSTATUS: Maturing (discussed 2026-11-13; step 1 built)\n"
                "## TEACH-I002 — Two\nSTATUS: Built in part (v3.13.2)\n"
                "## TEACH-I003 — Three\nSTATUS: Open\n")
        rep = self.report(text)
        self.assertEqual(rep["open"], [])
        self.assertEqual(rep["closed_counts"], {"Built": 0, "Declined": 0})
        self.assertEqual(rep["unknown"], [
            {"id": "TEACH-I001", "value": "Maturing (discussed 2026-11-13"},
            {"id": "TEACH-I002", "value": "Built in part (v3.13.2)"},
            {"id": "TEACH-I003", "value": "Open"}])
        code, out, _ = self.run_tool(self.write(text))
        self.assertIn('Unknown word (3): TEACH-I001 "Maturing (discussed 2026-11-13", '
                      'TEACH-I002 "Built in part (v3.13.2)", TEACH-I003 "Open"', out)

    def test_missing_and_repeated_status(self):
        text = ("- **PLANT-I001** — No state here\n"
                "- **PLANT-I002** — Two states\n  STATUS: Raw\n  STATUS: Built — later\n")
        rep = self.report(text)
        self.assertEqual(rep["no_state"], ["PLANT-I001"])
        self.assertEqual(rep["duplicate"], ["PLANT-I002"])
        self.assertEqual([(i["id"], i["state"]) for i in rep["open"]], [("PLANT-I002", "Raw")])
        code, out, _ = self.run_tool(self.write(text))
        self.assertIn("No state (1): PLANT-I001", out)
        self.assertIn("Two STATUS lines (1): PLANT-I002", out)

    def test_header_before_first_idea_is_ignored(self):
        # HEADER alone holds a template ID line, a template STATUS line and a bare
        # "STATUS: Raw"; none of them is an idea.
        code, out, err = self.run_tool(self.write(HEADER))
        self.assertEqual(code, 0, err)
        self.assertEqual(out.strip().split(": ", 1)[1],
                         "no idea entries found (ids like PROJ-I001 at a heading, "
                         "list item or ID: line)")
        rep = self.report(HEADER + HEADING)
        self.assertEqual(rep["unknown"] + rep["no_state"], [])
        self.assertEqual(len(rep["open"]), 2)

    def test_directory_prefers_dot_soul(self):
        self.write(LIST, "proj/ideas.md")
        self.write(HEADING, "proj/.soul/ideas.md")
        code, out, err = self.run_tool(os.path.join(self.dir, "proj"), "--json")
        self.assertEqual(code, 0, err)
        rep = json.loads(out)
        self.assertEqual(rep["path"], os.path.join(self.dir, "proj", ".soul", "ideas.md"))
        self.assertEqual(rep["parked"], ["THERMAL-I003"])
        self.write(LIST, "flat/ideas.md")
        code, out, err = self.run_tool(os.path.join(self.dir, "flat"), "--json")
        self.assertEqual(json.loads(out)["parked"], ["MODEL-LIB-I004"])

    def test_missing_file_exits_2(self):
        code, out, err = self.run_tool(os.path.join(self.dir, "nope.md"))
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertEqual(len(err.strip().splitlines()), 1, err)
        code, _, _ = self.run_tool(self.dir)  # a directory with no ideas.md
        self.assertEqual(code, 2)

    def test_json_keys(self):
        code, out, err = self.run_tool(self.write(LIST), "--json")
        self.assertEqual(code, 0, err)
        self.assertEqual(sorted(json.loads(out)), sorted(
            ["path", "open", "parked", "closed_counts", "no_state", "unknown",
             "duplicate"]))

    def test_long_title_is_cut(self):
        rep = self.report("## SOUL-I009 — " + "word " * 40 + "\nSTATUS: Raw\n")
        title = rep["open"][0]["title"]
        self.assertEqual(len(title), 80)
        self.assertTrue(title.endswith("…"), title)


if __name__ == "__main__":
    unittest.main()
