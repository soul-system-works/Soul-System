#!/usr/bin/env python3
"""Move each project's OWED UPSTREAM cursor field into a durable `upstream.md`.

v2.3.0 deletes the `OWED UPSTREAM` field from the handoff cursor. The cursor is
gitignored and rewritten wholesale every session, so the field holds the ONLY copy
of everything parked in it: once a session runs the new `/soul-handoff`, that text
is gone with no copy anywhere. This script moves it out first.

Dry run is the default and prints what would change. `--apply` writes, keeping the
original cursor as `handoff.md.pre-2.3.0` until the owner confirms.

Spec: docs/specs/2026-08-28-upstream-store.md (Task 1).
"""

import argparse
import difflib
import os
import re
import sys

DEFAULT_REGISTRY = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "registry", "PROJECTS.txt")

FIELD_RE = re.compile(r"^OWED UPSTREAM\b", re.M)
# Known cursor field labels. A generic "two or more capitals then ':'" pattern was
# tried first and silently TRUNCATED the field at any column-0 `API:` / `NOTE:` /
# `TODO:` line inside it — the remainder stayed in the cursor with its own label gone,
# so a re-run reported "no field" and the next handoff destroyed it. verify() could
# not see this: it only checks lines INSIDE the block it extracted (fresh-context
# review, 2026-08-28, reproduced). Anything else at column 0 is a REFUSAL, not a
# boundary — a human decides.
KNOWN_FIELDS = (
    "NEXT-SESSION FOCUS", "WHERE WE ARE", "LIVE AL", "OPEN GATES", "NEXT STEP",
    "OWED UPSTREAM", "POINTERS", "OPEN BODY CALLS", "SUGGESTED ROLES",
    "SUGGESTED ROLES / SKILLS", "CAPTURES", "FENCES RELIED ON", "STANDING NOTE",
    "OPEN QUESTIONS", "RISKS", "TASKS", "STATE", "BLOCKED ON",
)
NEXT_FIELD_RE = re.compile(r"^(?:%s)\b" % "|".join(re.escape(f) for f in KNOWN_FIELDS))
UNKNOWN_LABEL_RE = re.compile(r"^[A-Z][A-Z0-9][A-Z0-9 /\-]*\s*[:(]")
ITEM_RE = re.compile(r"^(\s*)(\d+)\.\s")
BULLET_RE = re.compile(r"^(\s*)[-*]\s")
LETTER_RE = re.compile(r"^(\s*)\(?[a-z]\)\s")
EMPTY_VALUES = {"", "none", "none.", "none —", "-", "n/a"}

HEADER = """# Upstream notes — {name}

Lessons about the Soul System itself, learned here. Append as they happen, in this
project's own words; the Soul System collects them on a periodic pass. Do not write
into that repo from here.

This is NOT this project's record — domain lessons go to `witness.md` / `ideas.md`.
An entry with no `**Mined:**` line has not been collected yet.
"""


def find_block(text):
    """Return (start_line, end_line, lines) for the OWED UPSTREAM field, or None."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if FIELD_RE.match(ln):
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    stopper = None
    for j in range(start + 1, len(lines)):
        ln = lines[j]
        if not ln or ln[0].isspace():
            continue
        if NEXT_FIELD_RE.match(ln):
            end = j
            break
        if UNKNOWN_LABEL_RE.match(ln):
            stopper = ln.strip()[:60]
            end = j
            break
    # trim trailing blank lines back to the field itself
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    return start, end, lines[start:end], stopper


def strip_label(block):
    """Drop the `OWED UPSTREAM...:` label, keep everything the owner wrote after it."""
    first = block[0]
    m = re.match(r"^OWED UPSTREAM[^:]*:[ \t]*", first)
    rest = first[m.end():] if m else ""
    return ([rest] if rest.strip() else []) + block[1:]


def dedent(lines, skip_first=False):
    """Strip the common indent. The label remainder (line 0 when the cursor wrote
    `OWED UPSTREAM: text`) always sits at indent 0 and would pin the common indent
    at 0, leaving the body at its 15-20 column cursor alignment — which CommonMark
    then renders as an indented CODE BLOCK. Sixteen entries in the largest store
    shipped that way before a fresh-context review caught it (2026-08-28)."""
    body = lines[1:] if skip_first else lines
    indents = [len(l) - len(l.lstrip()) for l in body if l.strip()]
    cut = min(indents) if indents else 0
    out = [l[cut:] if len(l) >= cut else l.lstrip() for l in body]
    return ([lines[0].strip()] + out) if skip_first else out


def split_items(lines):
    """Split on `N. ` markers at the modal indent. No markers -> one block, verbatim.

    Returns (preamble_lines, [item_lines, ...]). The modal indent matters: an item
    may itself contain a numbered sub-list, and splitting on those would shred it.
    """
    hits = [(i, len(ITEM_RE.match(l).group(1))) for i, l in enumerate(lines)
            if ITEM_RE.match(l)]
    if len(hits) < 2:
        # No numbered list. Some projects wrote the field as a bullet list instead.
        hits = [(i, len(BULLET_RE.match(l).group(1))) for i, l in enumerate(lines)
                if BULLET_RE.match(l)]
    if len(hits) < 2:
        hits = [(i, len(LETTER_RE.match(l).group(1))) for i, l in enumerate(lines)
                if LETTER_RE.match(l)]
    if len(hits) < 2:
        return [], [lines]
    indents = [d for _, d in hits]
    modal = max(set(indents), key=indents.count)
    idx = [i for i, d in hits if d == modal]
    if len(idx) < 2:
        return [], [lines]
    preamble = lines[: idx[0]] if any(l.strip() for l in lines[: idx[0]]) else []
    items = [lines[a:b] for a, b in zip(idx, idx[1:] + [len(lines)])]
    return preamble, items


def title_of(item):
    text = " ".join(l.strip() for l in item if l.strip())
    text = re.sub(r"^\s*(?:\d+\.|[-*]|\(?[a-z]\))\s*", "", text)
    text = re.sub(r"^\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"^\[[^\]]*\]\s*", "", text)   # drop a leading cursor-era aside
    text = re.sub(r"\s+", " ", text).strip()
    cut = text[:78]
    if len(text) > 78:
        cut = cut.rsplit(" ", 1)[0] + "…"
    return cut or "(untitled)"


def cursor_date(text, fallback):
    m = re.search(r"^#\s*Handoff cursor\s*[—-]\s*(\d{4}-\d{2}-\d{2})", text, re.M)
    return m.group(1) if m else fallback


def record_layout(project):
    """Where this project keeps its record. Detect, never assume."""
    if os.path.exists(os.path.join(project, "witness.md")):
        return os.path.join(project, "upstream.md")
    return os.path.join(project, ".soul", "upstream.md")


def render(project, date, preamble, items):
    name = os.path.basename(project.rstrip("/"))
    out = [HEADER.format(name=name)]
    if preamble:
        out.append("\n_Carried from the handoff cursor of {}, verbatim:_\n".format(date)
                   + "\n".join("> " + l if l.strip() else ">" for l in preamble).rstrip()
                   + "\n")
    for item in items:
        body = "\n".join(item).rstrip()
        out.append("\n### {} · {}\n\n{}\n".format(date, title_of(item), body))
    return "\n".join(out)


def verify(source_lines, rendered):
    """Every non-trivial source line must survive into the output."""
    missing = []
    for l in source_lines:
        s = l.strip()
        if len(s) > 3 and s not in rendered:
            missing.append(s)
    return missing


def is_soul_system_repo(project):
    """The Soul System repo is upstream; it owes nothing to itself."""
    return (os.path.isdir(os.path.join(project, "findings", "open"))
            and os.path.exists(os.path.join(project, "operations", "CLAUDE.md")))


def process(project, apply_changes, quiet=False):
    if is_soul_system_repo(project):
        return "skipped — this IS the Soul System repo"
    cursor = os.path.join(project, ".soul", "handoff.md")
    if not os.path.exists(cursor):
        return "no cursor"
    text = open(cursor, encoding="utf-8").read()
    found = find_block(text)
    if not found:
        return "no field"
    start, end, block, stopper = found
    if stopper:
        return ("REFUSED — unrecognised column-0 label {!r} inside the field; it would "
                "truncate the block. Add it to KNOWN_FIELDS or fix the cursor by hand."
                .format(stopper))
    payload = strip_label(block)
    joined = " ".join(l.strip() for l in payload).strip()
    if joined.lower().rstrip(".") in EMPTY_VALUES:
        return "empty"
    if not joined:
        # F2: a label with no inline text whose block came back bare is a PARSE
        # failure wearing an empty field's clothes, and the old code hid it from
        # the summary entirely (fresh-context review, 2026-08-28, reproduced).
        return ("REFUSED — field label present but no content captured; the block may "
                "have been truncated at line {}. Check by hand.".format(end + 1))

    # The label line contributed a zero-indent first element iff it carried inline text.
    label_inline = bool(re.match(r"^OWED UPSTREAM[^:]*:[ \t]*\S", block[0]))
    body = dedent(payload, skip_first=label_inline)
    date = cursor_date(text, "2026-08-28")
    preamble, items = split_items(body)
    rendered = render(project, date, preamble, items)

    missing = verify(payload, rendered)
    if missing:
        return "REFUSED — {} source line(s) would be lost, first: {!r}".format(
            len(missing), missing[0][:60])

    target = record_layout(project)
    lines = text.splitlines()
    new_cursor = "\n".join(lines[:start] + lines[end:]).rstrip() + "\n"

    if not quiet:
        print("\n" + "=" * 72)
        print("PROJECT: {}".format(project))
        print("  field lines {}-{} ({} lines) -> {}".format(
            start + 1, end, end - start, target))
        print("  {} entr{} · existing target: {}".format(
            len(items), "y" if len(items) == 1 else "ies",
            "APPEND" if os.path.exists(target) else "create"))
        print("-" * 72)
        print("\n".join(rendered.splitlines()[:14]))
        print("  ... [{} lines total]".format(len(rendered.splitlines())))
        print("-" * 72)
        print("  cursor diff:")
        for d in list(difflib.unified_diff(
                text.splitlines(), new_cursor.splitlines(),
                "handoff.md", "handoff.md (new)", lineterm="", n=1))[:8]:
            print("   " + d)
        print("   ... ({} lines removed)".format(end - start))

    if apply_changes:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        if os.path.exists(target):
            with open(target, "a", encoding="utf-8") as fh:
                fh.write("\n" + "\n".join(rendered.split("\n")[len(HEADER.splitlines()) + 1:]))
        else:
            open(target, "w", encoding="utf-8").write(rendered)
        open(cursor + ".pre-2.3.0", "w", encoding="utf-8").write(text)
        open(cursor, "w", encoding="utf-8").write(new_cursor)
        return "APPLIED -> {}".format(target)
    return "would migrate {} lines -> {}".format(end - start, target)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("projects", nargs="*", help="project paths (default: --sweep roots)")
    ap.add_argument("--apply", action="store_true", help="write (default is dry run)")
    ap.add_argument("--sweep", action="append", default=[],
                    help="scan a directory of projects")
    ap.add_argument("--registry", metavar="FILE", nargs="?", const=DEFAULT_REGISTRY,
                    help="read project paths from a registry file "
                         "(default: registry/PROJECTS.txt)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    targets = list(args.projects)
    if args.registry:
        if not os.path.exists(args.registry):
            ap.error("no registry at {}".format(args.registry))
        targets += [l.strip() for l in open(args.registry, encoding="utf-8")
                    if l.strip() and not l.startswith("#")]
    for root in args.sweep:
        if os.path.isdir(root):
            targets += [os.path.join(root, d) for d in sorted(os.listdir(root))
                        if os.path.isdir(os.path.join(root, d))]
    if not targets:
        ap.error("give project paths, --registry, or --sweep <dir>")

    print("MODE: {}".format("APPLY (writing)" if args.apply else "DRY RUN (no writes)"))
    results = []
    for p in targets:
        r = process(p, args.apply, args.quiet)
        results.append((p, r))

    print("\n" + "=" * 72 + "\nSUMMARY")
    acted = 0
    for p, r in results:
        if r in ("no cursor", "no field"):
            continue
        if r != "empty":
            acted += 1
        print("  {:<48} {}".format(os.path.basename(p.rstrip("/")), r))
    print("  {} project(s) with content; {} scanned.".format(acted, len(results)))
    if any("REFUSED" in r for _, r in results):
        print("  REFUSALS PRESENT — nothing was written for those. Fix before --apply.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
