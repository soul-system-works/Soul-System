"""Consistency test: the unconfirmed mark /soul-capture writes is the one /soul-handoff scans for.

FENCE: /soul-handoff step 1 finds unratified entries by scanning the stores for an
exact string. Any example of the mark in /soul-capture that differs from it writes
entries the scan never finds — they fall out of the cursor's UNCONFIRMED field and
are never put to the Body. v2.8.0 shipped one such example (a comma for the second
dash), caught on the first live /soul-handoff run (SOUL-204).

Run: python3 tools/test_unconfirmed_mark.py  (exit 0 = PASS)
"""

import os
import re
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read(rel):
    with open(os.path.join(_ROOT, rel), encoding="utf-8") as f:
        return f.read()


def main():
    handoff = _read("skills/soul-handoff/SKILL.md")
    m = re.search(r"Scan `witness\.md` and `ideas\.md` for\s+`([^`]+)`", handoff)
    if not m:
        print("FAIL: scan string not found in skills/soul-handoff/SKILL.md")
        return 1
    mark = m.group(1)

    capture = _read("skills/soul-capture/SKILL.md")
    # Every backticked span that shows the mark must carry the scanned string whole;
    # spans may wrap across lines, so collapse whitespace before comparing.
    spans = [re.sub(r"\s+", " ", s) for s in re.findall(r"`([^`]*)`", capture)]
    shown = [s for s in spans if "unconfirmed" in s and "ratify" in s]
    bad = [s for s in shown if mark not in s]
    if not shown:
        print("FAIL: no example of the mark found in skills/soul-capture/SKILL.md")
        return 1
    if bad:
        for s in bad:
            print(f"FAIL: capture example `{s}` does not contain the scanned mark `{mark}`")
        return 1
    print(f"PASS: {len(shown)} mark example(s) in soul-capture match `{mark}`")
    return 0


if __name__ == "__main__":
    sys.exit(main())
