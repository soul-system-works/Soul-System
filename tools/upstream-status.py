#!/usr/bin/env python3
"""Count unmined upstream notes across the registered adopting projects.

Run from the Soul System repo. Reads project paths from `registry/PROJECTS.txt`
(gitignored — the paths are private and never reach public main). An entry is a
`### ` heading in a project's `upstream.md`; it counts as MINED once it carries a
`**Mined:**` line.

Backs the `/soul-next` upstream line (spec: docs/specs/2026-08-28-upstream-store.md).

`--stamp <project> <n> <id>` marks entry n collected. Without it there is no way to
clear an entry, and the backlog line becomes a permanent, unclearable escalation —
the exact failure this release removed from the adopting project's seat (fresh-context
review, 2026-08-28).
"""
import argparse
import os
import re
import sys

REG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "registry", "PROJECTS.txt")


def entries(path):
    """Return (total, unmined) headings in one upstream.md."""
    text = open(path, encoding="utf-8").read()
    blocks = re.split(r"^### ", text, flags=re.M)[1:]
    return len(blocks), sum(1 for b in blocks if "**Mined:**" not in b)


def stamp(project, index, ident):
    """Mark entry #index (1-based) in a project's upstream.md as mined."""
    for cand in (os.path.join(project, "upstream.md"),
                 os.path.join(project, ".soul", "upstream.md")):
        if os.path.exists(cand):
            path = cand
            break
    else:
        print("no upstream.md under {}".format(project))
        return 1
    text = open(path, encoding="utf-8").read()
    parts = re.split(r"(?m)^(### .*)$", text)
    heads = [i for i in range(1, len(parts), 2)]
    if not 1 <= index <= len(heads):
        print("entry {} out of range (1..{})".format(index, len(heads)))
        return 1
    body_i = heads[index - 1] + 1
    if "**Mined:**" in parts[body_i]:
        print("entry {} is already mined".format(index))
        return 0
    parts[body_i] = parts[body_i].rstrip() + "\n\n**Mined:** {} → {}\n\n".format(
        __import__("datetime").date.today().isoformat(), ident)
    open(path, "w", encoding="utf-8").write("".join(parts))
    print("stamped {} entry {} -> {}".format(os.path.basename(path), index, ident))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--detail", action="store_true",
                    help="list per-project counts (prints real project names)")
    ap.add_argument("--stamp", nargs=3, metavar=("PROJECT", "N", "ID"),
                    help="mark entry N of PROJECT as mined, citing ID")
    args = ap.parse_args()
    if args.stamp:
        return stamp(args.stamp[0], int(args.stamp[1]), args.stamp[2])
    if not os.path.exists(REG):
        print("no registry/PROJECTS.txt — nothing registered")
        return 0
    paths = [l.strip() for l in open(REG, encoding="utf-8")
             if l.strip() and not l.startswith("#")]
    rows, tot_un, tot_all = [], 0, 0
    for p in paths:
        for cand in (os.path.join(p, "upstream.md"),
                     os.path.join(p, ".soul", "upstream.md")):
            if os.path.exists(cand):
                n, un = entries(cand)
                tot_all += n
                tot_un += un
                if un:
                    rows.append((os.path.basename(p.rstrip("/")), un, n))
                break
    # Default is totals-only. The per-project lines carry real project names, and
    # this is the one repo whose main is public and anonymises them (mind 5c) —
    # printing them unconditionally put them in context on every /soul-next run
    # (fresh-context review, 2026-08-28).
    if args.detail:
        for name, un, n in sorted(rows, key=lambda r: -r[1]):
            print("  %-28s %3d unmined / %d" % (name, un, n))
    if tot_un:
        print("\n%d unmined upstream note%s across %d project%s → mining pass."
              % (tot_un, "" if tot_un == 1 else "s",
                 len(rows), "" if len(rows) == 1 else "s"))
    else:
        print("\nNo unmined upstream notes (%d collected)." % tot_all)
    return 0


if __name__ == "__main__":
    sys.exit(main())
