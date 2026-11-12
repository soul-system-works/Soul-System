#!/usr/bin/env python3
"""The mechanical brake on a Mind change (SOUL-A032): old mind.md against new.

/soul-distill grades each change it makes to the Mind as minor (applied on its own)
or major (held for the owner). The model's grade can be wrong in the flattering
direction (mind item 2), so before anything is applied this script checks, item by
item, what a grade cannot talk round:

  1. every numbered item in the old Mind still exists under the same number (a cut,
     a merge or a renumbering fails — the Mind's items are cited by number from
     outside it, so a renumbering is a change of meaning too);
  2. every record id an old item cites is still cited in the item with that number
     (an item without its incident gets reinterpreted — F053/A020). An id moved to
     another item counts as dropped.

Either check failing makes the whole change major, whatever the model graded it.
A whole-file count was not enough: cutting item 7 and adding item 13 kept the count,
and an item whose ids were also cited elsewhere could be cut without losing an id
(fresh-context review of the A032 build, 2026-11-12).

    python3 tools/mind-guard.py <old mind.md> <new mind.md>

Exit 0: both checks pass. Exit 1: a check failed; each reason is printed. Exit 2: a
file could not be read. /soul-distill treats any exit but 0 as major.

What counts:
  - The stamp is not checked: the `**Last distilled:**` line and everything after the
    last `---` line above it (step 7's template). Every distill rewrites it, and its
    "against SOUL-234 / A031 …" ids would otherwise make every distill major.
  - The header (everything before the first item) is not checked.
  - An item starts at a line that begins, unindented, with a number and a dot
    ("12. ...") outside fenced code, and runs to the next item, a `#` heading or the
    stamp. Indented or fenced numbered lines are not items.
  - An old Mind with no numbered items (the retired four-bucket form) is checked as
    one block: every id it cites must still be cited somewhere in the new one.
  - A record id is CODE-123 or CODE-X123 (SOUL-118, SOUL-F063, SOUL-I089, THERMAL-231,
    THERMAL-I086; a code may hold more dashes, PLANT-BOP-12), or a bare F, A or I
    with two or more digits (F063, A022, I089). A bare id in the old item is still
    cited when the new one cites it with a code (F063 -> SOUL-F063); the other way
    round is not accepted. Any WORD-123 token counts, so dropping "UTF-8" also fails:
    a false alarm holds a change for the owner, which is the safe side.
Commit hashes and item numbers are not ids.
"""

import re
import sys

ITEM_RE = re.compile(r"^(\d+)\.\s+\S")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^#")
STAMP_RE = re.compile(r"^\*\*Last distilled:\*\*")
CODED_RE = re.compile(r"\b((?:[A-Z][A-Z0-9]*-)+)([A-Z]?\d+)\b")
BARE_RE = re.compile(r"(?<![-\w])([FAI]\d{2,})\b")


def _body(text):
    """The lines outside fences, with the stamp removed."""
    lines, fenced = [], False
    for ln in text.splitlines():
        if FENCE_RE.match(ln):
            fenced = not fenced
            continue
        if not fenced:
            lines.append(ln)
    stamp = next((i for i, ln in enumerate(lines) if STAMP_RE.match(ln)), None)
    if stamp is None:
        return lines
    rule = max((i for i in range(stamp) if lines[i].strip() == "---"), default=stamp)
    return lines[:rule]


def items(text):
    """{number: item text}; the text of a repeated number is joined."""
    out, cur = {}, None
    for ln in _body(text):
        m = ITEM_RE.match(ln)
        if m:
            cur = int(m.group(1))
            out[cur] = out.get(cur, "") + "\n" + ln
        elif HEADING_RE.match(ln):
            cur = None
        elif cur is not None:
            out[cur] += "\n" + ln
    return out


def ids(text):
    """(coded ids, bare ids, the id part of every coded id)."""
    coded, bare, tails = set(), set(), set()
    for m in CODED_RE.finditer(text):
        coded.add(m.group(1) + m.group(2))
        tails.add(m.group(2))
    for m in BARE_RE.finditer(text):
        bare.add(m.group(1))
    return coded, bare, tails


def _lost(old, new):
    o_coded, o_bare, _ = ids(old)
    n_coded, n_bare, n_tails = ids(new)
    return sorted(o_coded - n_coded) + sorted(x for x in o_bare - n_bare if x not in n_tails)


def check(old, new):
    """The list of reasons the change is major; empty when both checks pass."""
    o_items, n_items = items(old), items(new)
    if not o_items:
        lost = _lost("\n".join(_body(old)), "\n".join(_body(new)))
        return (["record ids the old Mind cites are gone: {}".format(", ".join(lost))]
                if lost else [])
    reasons = []
    gone = sorted(n for n in o_items if n not in n_items)
    if gone:
        reasons.append("item(s) {} are gone (a cut, a merge or a renumbering)"
                       .format(", ".join(map(str, gone))))
    for n in sorted(o_items):
        if n in n_items:
            lost = _lost(o_items[n], n_items[n])
            if lost:
                reasons.append("item {} no longer cites: {}".format(n, ", ".join(lost)))
    return reasons


def _read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def main(argv):
    if len(argv) != 2:
        print("usage: mind-guard.py <old mind.md> <new mind.md>", file=sys.stderr)
        return 2
    try:
        old, new = _read(argv[0]), _read(argv[1])
    except OSError as exc:
        print("mind-guard: cannot read {}".format(exc), file=sys.stderr)
        return 2
    reasons = check(old, new)
    if reasons:
        print("mind-guard: MAJOR — hold the whole change for the owner:")
        for r in reasons:
            print("  - " + r)
        return 1
    print("mind-guard: ok (items {} -> {}; every old item kept with its ids)".format(
        len(items(old)), len(items(new))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
