"""Consistency test: model-initiated captures are accepted with an opt-out, and nothing tells a session to write the old mark or wait for a ratify.

FENCE: the owner retired the ratify step (SOUL-I085, SOUL-A031, 2026-11-05): "i have
to "ratify" something all the time. i hate it. ... should be autoratified with opt
out. this way it isn't an extra commit or extra step". A capture the model starts is
now appended unmarked, named in one line ("say no to strike it"), and a no marks it
declined. This test replaces tools/test_unconfirmed_mark.py, the SOUL-204 guard that
checked every example of the mark matched the string /soul-handoff scanned for; there
is no mark and no scan any more.

The text is read in units: a paragraph, or one list item (a line starting "- " or
"3. " opens a new unit). A unit that starts with "**Source:**" or "**Amended:**" is
the history footer and is skipped — the footers record the old rule truthfully and
are not rewritten to pass. The test fails if:

  (a) any skill unit carries the mark — "unconfirmed", any dash, comma or hyphen,
      "owner to ratify". The one allowed mention is /soul-resume's backward-compat
      unit (it contains "treated as accepted"), and that unit must not tell the
      session to write, add, remove or strip anything;
  (b) /soul-handoff's cursor template has an `UNCONFIRMED:` field, or lacks the
      `NEW ENTRIES:` field that replaced it;
  (c) /soul-capture, /soul-handoff or /soul-resume lacks the opt-out wording
      "say no to strike";
  (d) any skill unit says "hold for confirmation", "nothing is appended until", or
      "says go" about appending, or asks the Body to ratify. A witness entry the Body
      types still shows its draft for go / edit / cancel (/soul-capture witness step
      5); that unit passes because it opens "Owner-typed only" — the opt-out covers
      only captures the model starts, so the scope is in the step's own words;
  (e) /soul-help or docs/using-the-soul.md still describes the opt-in model
      ("proposes captures", "nothing is written without your yes", "answers yes/no").

Run: python3 tools/test_capture_opt_out.py  (exit 0 = PASS)
"""

import glob
import os
import re
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MARK = re.compile(r"unconfirmed\s*[—–\-,;:]*\s*owner\s+to\s+ratify", re.I)
_COMPAT_SKILL = "soul-resume"
_COMPAT_WORDS = "treated as accepted"
_INSTRUCTS = re.compile(r"\b(write|writes|add|adds|remove|removes|strip|strips|delete|append)\b", re.I)
_OPT_OUT = "say no to strike"
_OPT_OUT_SKILLS = ("soul-capture", "soul-handoff", "soul-resume")
_OWNER_SCOPE = "owner-typed only"
_HOLD = re.compile(r"hold for confirmation|nothing is appended until", re.I)
_GO = re.compile(r"says go", re.I)
_ASK_RATIFY = re.compile(r"\b(ask|asks|asking)\b[^.]*\bratif", re.I)
_OPT_IN = re.compile(r"propos\w*\s+captures|nothing is written without your yes|answers yes/no", re.I)
_OPT_IN_FILES = ("skills/soul-help/SKILL.md", "docs/using-the-soul.md")


def _read(rel):
    with open(os.path.join(_ROOT, rel), encoding="utf-8") as f:
        return f.read()


def _collapse(s):
    # Text may wrap across lines, and *emphasis* may split a phrase; compare as rendered.
    return re.sub(r"\s+", " ", s.replace("*", "")).strip()


def _units(text):
    """Paragraphs, with each list item its own unit; history footers dropped."""
    units = []
    for para in re.split(r"\n\s*\n", text):
        for item in re.split(r"\n(?=\s*(?:-|\d+[a-z]?\.)\s)", para):
            flat = _collapse(item)
            if flat and not flat.startswith(("Source:", "Amended:")):
                units.append(flat)
    return units


def _skills():
    for path in sorted(glob.glob(os.path.join(_ROOT, "skills", "*", "SKILL.md"))):
        with open(path, encoding="utf-8") as f:
            yield os.path.basename(os.path.dirname(path)), f.read()


def main():
    fails = []

    for skill, text in _skills():
        for u in _units(text):
            # (a) the mark survives only in /soul-resume's compat unit, which instructs nothing.
            if _MARK.search(u):
                compat = skill == _COMPAT_SKILL and _COMPAT_WORDS in u
                if not compat:
                    fails.append(f"(a) {skill} carries the mark: {u[:110]}...")
                elif _INSTRUCTS.search(u):
                    fails.append(f"(a) {skill}'s compat line tells the session to "
                                 f"'{_INSTRUCTS.search(u).group(0)}': {u[:110]}...")
            # (d) no hold-for-go, outside the owner-typed draft step; no ask to ratify.
            owner_step = u.lower().lstrip("0123456789. ").startswith(_OWNER_SCOPE)
            if not owner_step and (_HOLD.search(u) or (_GO.search(u) and "append" in u.lower())):
                fails.append(f"(d) {skill} holds a capture for a go: {u[:110]}...")
            if _ASK_RATIFY.search(u):
                fails.append(f"(d) {skill} asks for a ratify: {u[:110]}...")

    # (b) the cursor template: the fenced block that starts "# Handoff cursor".
    handoff = _read("skills/soul-handoff/SKILL.md")
    m = re.search(r"```\n\s*# Handoff cursor.*?```", handoff, re.S)
    if not m:
        fails.append("(b) cursor template not found in skills/soul-handoff/SKILL.md")
    else:
        template = m.group(0)
        if re.search(r"^\s*UNCONFIRMED:", template, re.M):
            fails.append("(b) cursor template still has an `UNCONFIRMED:` field")
        if not re.search(r"^\s*NEW ENTRIES:", template, re.M):
            fails.append("(b) cursor template has no `NEW ENTRIES:` field")

    # (c) the opt-out wording, in each skill that names a new entry to the Body.
    for skill in _OPT_OUT_SKILLS:
        if _OPT_OUT not in _collapse(_read(f"skills/{skill}/SKILL.md")):
            fails.append(f"(c) {skill} lacks the opt-out wording \"{_OPT_OUT}\"")

    # (e) the reader-facing summaries.
    for rel in _OPT_IN_FILES:
        hit = _OPT_IN.search(_collapse(_read(rel)))
        if hit:
            fails.append(f"(e) {rel} still describes opt-in capture: \"{hit.group(0)}\"")

    if fails:
        for f in fails:
            print("FAIL: " + f)
        return 1
    print("PASS: no skill writes the unconfirmed mark or holds a model capture for a go "
          "(soul-resume's compat line and the owner-typed draft step excepted); cursor has "
          "NEW ENTRIES, not UNCONFIRMED; opt-out wording in " + ", ".join(_OPT_OUT_SKILLS)
          + "; soul-help and the user guide describe the opt-out")
    return 0


if __name__ == "__main__":
    sys.exit(main())
