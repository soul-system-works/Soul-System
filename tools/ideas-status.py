#!/usr/bin/env python3
"""The open ideas in a project's ideas.md, one line each (SOUL-I096).

A long ideas store hides open work: a session reads the top, not entry ninety. Each
idea now carries one state line, and this script prints the ideas still open, so a
session sees them without reading the whole store. It also flags ideas whose state
line is missing, repeated or not one of the five words. It is a report, not a gate:
it never changes the store and never fails a session.

    python3 tools/ideas-status.py <ideas.md | project dir> [--json]

For a directory it reads <dir>/.soul/ideas.md if that exists, else <dir>/ideas.md.
Exit 0 whenever the report ran, flags included. Exit 2: the file is missing or
cannot be read (one line on stderr).

The state line, one per idea, on a line of its own (leading spaces allowed, so a
list-item store can indent it under the item; `**STATUS:**` also accepted):

    STATUS:    <word>[ — <date or note>]

The word is the text before the first " — " (or the whole value). There are five,
matched exactly, case and all: open Raw, Maturing; waiting Parked; closed Built,
Declined. Anything else — "Maturing (discussed …)", "Built in part", "Graduated
[to …]", "Open" — is an unknown word, reported with its first 30 characters and
never mapped to one of the five.

What counts:
  - An idea id is CODE-I123, the code one or more dash-joined capitals/digits
    (SOUL-I096, MODEL-LIB-I005, PLANT-I001).
  - An idea starts at one of three shapes, all in real stores: a field block line
    `ID:  <id>` (found inside ``` fences too, where this repo keeps them); an
    unindented list item `- **<id>**` and its text (or `- **<id> — title**`); a `##`, `###` or `####` heading
    `<id>` and its title. List items and headings inside a fence are not ideas.
  - An idea runs to the next idea start or the next markdown heading outside a
    fence, whichever comes first. Text before the first idea (the store's header,
    a `STATUS: Raw | Maturing | …` template) belongs to no idea and is ignored.
  - No state line: NO STATE. Two or more: reported, and the first one counts.
  - The title shown: for a heading or list item, the text after the id and its
    separator; for a field block, the first RAW: line, else the first IDEA: line,
    else the first other non-empty field after the id and date. Whitespace
    collapsed, `**` dropped, cut at 80 characters.
"""

import json
import os
import re
import sys

ID = r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-I\d+"
SEP = r"\s*(?:[—–·:|]|-(?=\s))?\s*"
FIELD_START_RE = re.compile(r"^ID:\s+(" + ID + r")\b")
# `- **<id>** — title` or `- **<id> — title**`: both occur in real stores.
LIST_START_RE = re.compile(r"^-\s+\*\*(" + ID + r")\b(?:\*\*)?" + SEP + r"(.*)$")
HEAD_START_RE = re.compile(r"^#{2,4}\s+(" + ID + r")\b" + SEP + r"(.*)$")
HEADING_RE = re.compile(r"^#{1,6}(\s|$)")
FENCE_RE = re.compile(r"^\s*```")
STATUS_RE = re.compile(r"^\s*(?:\*\*STATUS:\*\*|STATUS:)\s+(.*)$")
FIELD_RE = re.compile(r"^([A-Z][A-Z_ ]*):\s*(.*)$")

OPEN = ("Raw", "Maturing")
PARKED = "Parked"
CLOSED = ("Built", "Declined")
WORDS = OPEN + (PARKED,) + CLOSED
TITLE_MAX = 80
UNKNOWN_MAX = 30


def _clean(text):
    text = " ".join(text.replace("**", "").split())
    return text if len(text) <= TITLE_MAX else text[:TITLE_MAX - 1].rstrip() + "…"


def _field_title(lines):
    fields = [m.groups() for m in map(FIELD_RE.match, lines) if m]
    for want in ("RAW", "IDEA"):
        for name, value in fields:
            if name == want and value.strip():
                return value
    for name, value in fields:
        if name not in ("ID", "WHEN", "DATE", "STATUS") and value.strip():
            return value
    return ""


def ideas(text):
    """[{id, title, states}] in file order; states are the raw STATUS values."""
    out, cur, fenced = [], None, False
    for ln in text.splitlines():
        if FENCE_RE.match(ln):
            fenced = not fenced
            continue
        start = FIELD_START_RE.match(ln)
        if start:
            cur = {"id": start.group(1), "title": None, "states": [], "lines": []}
            out.append(cur)
            continue
        start = None if fenced else (LIST_START_RE.match(ln) or HEAD_START_RE.match(ln))
        if start:
            cur = {"id": start.group(1), "title": start.group(2), "states": [],
                   "lines": []}
            out.append(cur)
            continue
        if not fenced and HEADING_RE.match(ln):
            cur = None
            continue
        if cur is None:
            continue
        m = STATUS_RE.match(ln)
        if m:
            cur["states"].append(m.group(1).strip())
        else:
            cur["lines"].append(ln)
    for idea in out:
        lines = idea.pop("lines")
        idea["title"] = _clean(idea["title"] if idea["title"] is not None
                               else _field_title(lines))
    return out


def report(path, text):
    """The report as one dict (the --json shape)."""
    rep = {"path": path, "open": [], "parked": [],
           "closed_counts": {w: 0 for w in CLOSED},
           "no_state": [], "unknown": [], "duplicate": [], "found": 0}
    open_counts = {w: 0 for w in OPEN}
    for idea in ideas(text):
        rep["found"] += 1
        if not idea["states"]:
            rep["no_state"].append(idea["id"])
            continue
        if len(idea["states"]) > 1:
            rep["duplicate"].append(idea["id"])
        value = idea["states"][0]
        word = value.split(" — ", 1)[0].strip()
        if word not in WORDS:
            rep["unknown"].append({"id": idea["id"], "value": value[:UNKNOWN_MAX].rstrip()})
        elif word in OPEN:
            open_counts[word] += 1
            rep["open"].append({"id": idea["id"], "state": word, "title": idea["title"]})
        elif word == PARKED:
            rep["parked"].append(idea["id"])
        else:
            rep["closed_counts"][word] += 1
    rep["open_counts"] = open_counts
    return rep


def text_report(rep):
    path = rep["path"]
    if not rep["found"]:
        return ["{}: no idea entries found (ids like PROJ-I001 at a heading, list item "
                "or ID: line)".format(path)]
    oc, cc = rep["open_counts"], rep["closed_counts"]
    lines = ["{}: {} open ({}) · {} parked · {} closed ({})".format(
        path, sum(oc.values()), ", ".join("{} {}".format(w, oc[w]) for w in OPEN),
        len(rep["parked"]), sum(cc.values()),
        ", ".join("{} {}".format(w, cc[w]) for w in CLOSED))]
    if rep["open"]:
        width = max(len(i["id"]) for i in rep["open"])
        for i in rep["open"]:
            lines.append("  {}  {:<8}  {}".format(i["id"].ljust(width), i["state"],
                                                  i["title"]).rstrip())
    if rep["parked"]:
        lines.append("Parked: " + ", ".join(rep["parked"]))
    if rep["no_state"]:
        lines.append("No state ({}): {}".format(len(rep["no_state"]),
                                                ", ".join(rep["no_state"])))
    if rep["unknown"]:
        lines.append("Unknown word ({}): {}".format(len(rep["unknown"]), ", ".join(
            '{} "{}"'.format(u["id"], u["value"]) for u in rep["unknown"])))
    if rep["duplicate"]:
        lines.append("Two STATUS lines ({}): {}".format(len(rep["duplicate"]),
                                                        ", ".join(rep["duplicate"])))
    return lines


def _resolve(arg):
    if os.path.isdir(arg):
        soul = os.path.join(arg, ".soul", "ideas.md")
        return soul if os.path.isfile(soul) else os.path.join(arg, "ideas.md")
    return arg


def main(argv):
    as_json = "--json" in argv
    args = [a for a in argv if a != "--json"]
    if len(args) != 1:
        print("usage: ideas-status.py <ideas.md | project dir> [--json]", file=sys.stderr)
        return 2
    path = _resolve(args[0])
    try:
        with open(path, encoding="utf-8-sig") as f:
            text = f.read()
    except (OSError, UnicodeDecodeError) as exc:
        print("ideas-status: cannot read {}: {}".format(path, exc), file=sys.stderr)
        return 2
    rep = report(path, text)
    if as_json:
        print(json.dumps({k: rep[k] for k in ("path", "open", "parked", "closed_counts",
                                              "no_state", "unknown", "duplicate")},
                         ensure_ascii=False, indent=2))
    else:
        print("\n".join(text_report(rep)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
