"""Consistency test: every skill that writes or removes the unconfirmed mark uses the string /soul-handoff scans for.

FENCE: /soul-handoff step 1 finds unratified entries by scanning the stores for an
exact string. Any example of the mark that differs from it writes entries the scan
never finds — they fall out of the cursor's UNCONFIRMED field and are never put to
the Body. v2.8.0 shipped one such example in /soul-capture (a comma for the second
dash), caught on the first live /soul-handoff run (SOUL-204). The writers are
/soul-capture and /soul-handoff; the removers are /soul-handoff and /soul-resume.

Run: python3 tools/test_unconfirmed_mark.py  (exit 0 = PASS)
"""

import os
import re
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SKILLS = ("soul-capture", "soul-handoff", "soul-resume")


def _read(rel):
    with open(os.path.join(_ROOT, rel), encoding="utf-8") as f:
        return f.read()


def _collapse(s):
    # Spans and the scan string may wrap across lines; compare them as rendered.
    return re.sub(r"\s+", " ", s)


def main():
    handoff = _read("skills/soul-handoff/SKILL.md")
    m = re.search(r"Scan `witness\.md` and `ideas\.md` for\s+`([^`]+)`", handoff)
    if not m:
        print("FAIL: scan string not found in skills/soul-handoff/SKILL.md")
        return 1
    mark = _collapse(m.group(1))

    shown, bad = 0, []
    for skill in _SKILLS:
        text = _read(f"skills/{skill}/SKILL.md")
        spans = [_collapse(s) for s in re.findall(r"`([^`]*)`", text)]
        # A mark example: lowercase "unconfirmed" (the cursor's `UNCONFIRMED` field
        # name is not one) alongside the owner wording, whatever its last word.
        for s in spans:
            if "unconfirmed" in s and ("owner" in s or "ratify" in s):
                shown += 1
                if mark not in s:
                    bad.append((skill, s))
    if not shown:
        print("FAIL: no example of the mark found in " + ", ".join(_SKILLS))
        return 1
    if bad:
        for skill, s in bad:
            print(f"FAIL: {skill} example `{s}` does not contain the scanned mark `{mark}`")
        return 1
    print(f"PASS: {shown} mark example(s) across {', '.join(_SKILLS)} match `{mark}`")
    return 0


if __name__ == "__main__":
    sys.exit(main())
