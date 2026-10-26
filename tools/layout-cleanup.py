#!/usr/bin/env python3
"""Offer to move AI working files into `.ai/` — conservatively, dry run first.

Every file in a Soul project is one of three classes: (1) project content — code,
tests, user docs, ADRs, README, CHANGELOG — in its normal folders; (2) the durable
AI record in `.soul/` or the root (witness, ideas, upstream, mind, handoff, event
log); (3) AI working artifacts — plans, drafts, reviews, eval results, handoff
packs, scratch — in ONE folder, `.ai/`, safe to delete. Projects that predate the
rule have class-3 files scattered through class-1 folders. This script finds the
likely ones and moves only what the owner says to move.

Detection is deliberately narrow: a text file, in the root or `docs/` (or a stray
in `.soul/`), whose NAME or FOLDER marks it as working material. A miss costs a
file left where it was; a false hit costs the owner's trust in the offer, so when
in doubt it does not flag. Moving a working file into project content is the
owner's call, and project content must not link into `.ai/` — so every link this
script repoints from a class-1 file is REPORTED, never silently kept or dropped.

  scan <project> [--json]               list candidates by group (changes nothing)
  apply <project> --plan P [--dry-run]  P maps path -> move | leave | content
  decline <project>                     remember every candidate as `leave`

`leave` / `content` decisions live in `.soul/layout.json` and are never offered
again. Tracked files move with `git mv` so their history survives.
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote

# Class 2 — never offered, wherever they sit. layout.json is this script's own memory.
STORE_FILES = {"witness.md", "ideas.md", "upstream.md", "mind.md", "handoff.md",
               "events.jsonl", "layout.json", "init.md", "private-names.txt"}
TEXT_EXT = {".md", ".txt", ".patch", ".diff", ".log", ".html"}
PROTECTED_NAME_RE = re.compile(
    r"^(readme|changelog|license|licence|contributing|governance)\b|^(agents|claude)\.md$",
    re.I)
SKIP_DIRS = {".git", ".ai", ".claude", "node_modules", "venv", ".venv", "env",
             "__pycache__", "site-packages", "tests", "test"}
LINK_SKIP_DIRS = {".git", ".claude", "node_modules", "venv", ".venv", "env",
                  "__pycache__", "site-packages"}

# (path prefix, group). A file under one of these folders is working material.
DIR_RULES = (
    ("docs/plans/", "plans"),
    ("docs/superpowers/", "plans"),   # plans + specs written by planning skills
    ("plans/", "plans"),
    ("scratch/", "scratch"),
    ("handoff/", "handoffs"),
)
# (pattern over the dash-joined lowercase name tokens, label, group). Whole tokens
# only: `planning-guide.md` and `explanation.md` are user docs, not plans.
NAME_RULES = (
    (r"plans?", "plan", "plans"),
    (r"handoffs?", "handoff", "handoffs"),
    (r"reviews?", "review", "reviews"),
    (r"eval-results?", "eval-results", "reviews"),
    (r"scratch(?:pad)?", "scratch", "scratch"),
    (r"prompts?", "prompt", "scratch"),
    (r"session-(?:notes|summary)", "session-notes/summary", "scratch"),
    (r"todo-ai", "todo-ai", "scratch"),
)
NAME_RULES = tuple((re.compile(r"(?:^|-)%s(?:-|$)" % p), l, g) for p, l, g in NAME_RULES)
GROUP_ORDER = ("plans", "handoffs", "reviews", "scratch", "old-soul-files")

AI_README = """# .ai/ — AI working files

Plans, design drafts, review outputs, eval results, handoff packs and scratch that
AI sessions produced while working on this project. None of it is project content
or the durable record (that lives in `.soul/`), so the whole folder is safe to
delete or archive; anything worth keeping should be promoted out of it by its owner.
"""

# Inline `[x](dest "title")` / `![x](<dest with spaces>)`, and reference definitions
# `[x]: dest`. Backtick code spans are cut out before either is applied.
INLINE_LINK_RE = re.compile(
    r"(!?\[[^\]\n]*\]\()(<[^>\n]*>|[^)\s<>]+)"
    r"((?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^)\n]*\)))?\s*\))")
REF_DEF_RE = re.compile(r"^([ ]{0,3}\[[^\]\n]+\]:[ \t]*)(<[^>\n]*>|[^\s<>]+)")
CODE_SPAN_RE = re.compile(r"(`+)(?:.*?[^`])?\1(?!`)")


def rel(project, path):
    return os.path.relpath(path, project).replace(os.sep, "/")


def is_text(name):
    return os.path.splitext(name)[1].lower() in TEXT_EXT


def name_tokens(name):
    stem = os.path.splitext(name)[0]
    stem = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", stem).lower()
    return "-".join(t for t in re.split(r"[^a-z0-9]+", stem) if t)


def classify(relpath):
    """Return (group, reason) for a file outside `.soul/`, or None."""
    name = os.path.basename(relpath)
    if name in STORE_FILES or PROTECTED_NAME_RE.search(name) or not is_text(name):
        return None
    if relpath.startswith("docs/adr/"):
        return None
    for prefix, group in DIR_RULES:
        if relpath.startswith(prefix):
            return group, "folder rule: under {}".format(prefix)
    # Name rules reach only the root and the TOP level of docs/: deeper folders
    # (docs/specs/, docs/archive/) are curated project content whose names often
    # mention a handoff or a review — this repo's own scan flagged three such.
    if relpath.count("/") > (1 if relpath.startswith("docs/") else 0):
        return None
    tokens = name_tokens(name)
    for pat, label, group in NAME_RULES:
        if pat.search(tokens):
            return group, 'name rule: "{}" in the file name'.format(label)
    return None


def safe(project, relpath):
    """True when `relpath` stays inside the project with no symlink on the way. A
    symlink named like a plan would otherwise be moved, or written THROUGH by a link
    fix, landing on whatever it points at outside the project."""
    if relpath.startswith("../") or relpath == ".." or os.path.isabs(relpath):
        return False
    cur = project
    for part in relpath.split("/"):
        cur = os.path.join(cur, part)
        if os.path.islink(cur):
            return False
    real = os.path.realpath(os.path.join(project, relpath))
    return real == project or real.startswith(project + os.sep)


def walk_files(project, top):
    base = os.path.join(project, top)
    if os.path.islink(base):
        return
    for dirpath, dirs, files in os.walk(base):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")
                         and not os.path.islink(os.path.join(dirpath, d))
                         and rel(project, os.path.join(dirpath, d)) != "docs/adr")
        for f in sorted(files):
            if not os.path.islink(os.path.join(dirpath, f)):
                yield rel(project, os.path.join(dirpath, f))


def load_layout(project):
    path = os.path.join(project, ".soul", "layout.json")
    if not os.path.exists(path):
        return {"decisions": {}}
    data = json.load(open(path, encoding="utf-8"))
    data.setdefault("decisions", {})
    return data


def save_layout(project, data):
    path = os.path.join(project, ".soul", "layout.json")
    text = json.dumps(data, indent=2, sort_keys=True) + "\n"
    if os.path.exists(path) and open(path, encoding="utf-8").read() == text:
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)
    return True


def scan(project):
    """Every current candidate, minus what `.soul/layout.json` already settled."""
    found = []
    for name in sorted(os.listdir(project)):
        full = os.path.join(project, name)
        if os.path.isfile(full) and not os.path.islink(full):
            hit = classify(name)
            if hit:
                found.append((name, "file") + hit)
    for top in ("docs", "plans", "scratch", "handoff"):
        for p in walk_files(project, top):
            hit = classify(p)
            if hit:
                found.append((p, "file") + hit)
    soul = os.path.join(project, ".soul")
    if os.path.isdir(soul) and not os.path.islink(soul):
        for name in sorted(os.listdir(soul)):
            full = os.path.join(soul, name)
            if name in STORE_FILES or os.path.islink(full):
                continue
            if os.path.isdir(full):
                found.append((".soul/" + name, "dir", "old-soul-files",
                              ".soul/ folder that is not part of the record"))
            elif is_text(name):
                found.append((".soul/" + name, "file", "old-soul-files",
                              ".soul/ file that is not a record store"))

    settled = load_layout(project)["decisions"]
    out, taken = [], set()
    for path, kind, group, reason in found:
        if path in settled:
            continue
        target = pick_target(project, path, group, taken)
        taken.add(target)
        out.append({"path": path, "kind": kind, "group": group, "reason": reason,
                    "target": target})
    out.sort(key=lambda c: (GROUP_ORDER.index(c["group"]), c["path"]))
    return out


def pick_target(project, path, group, taken):
    """`.ai/<group>/<name>`; a clash takes the flattened parent path, then a counter."""
    name = os.path.basename(path)
    options = [name, "-".join(path.split("/"))]
    stem, ext = os.path.splitext(options[-1])
    options += ["{}-{}{}".format(stem, n, ext) for n in range(2, 100)]
    for opt in options:
        t = ".ai/{}/{}".format(group, opt)
        if t not in taken and not os.path.lexists(os.path.join(project, t)):
            return t
    raise SystemExit("no free target for {}".format(path))


def print_scan(project, cands):
    if not cands:
        print("no layout candidates in {}".format(project))
        return
    groups = [g for g in GROUP_ORDER if any(c["group"] == g for c in cands)]
    print("LAYOUT SCAN (dry run — nothing changed): {}".format(project))
    print("{} candidate(s) in {} group(s)".format(len(cands), len(groups)))
    for g in groups:
        members = [c for c in cands if c["group"] == g]
        print("\n{} ({})".format(g, len(members)))
        for c in members:
            print("  {}{}".format(c["path"], "/" if c["kind"] == "dir" else ""))
            print("      why: {}".format(c["reason"]))
            print("      ->   {}".format(c["target"]))


# --- git ---------------------------------------------------------------------

def git(project, *args):
    return subprocess.run(["git", "-C", project] + list(args),
                          capture_output=True, text=True)


def in_git(project):
    try:
        return git(project, "rev-parse", "--is-inside-work-tree").stdout.strip() == "true"
    except FileNotFoundError:
        return False


def tracked(project, path):
    r = git(project, "ls-files", "--", path)
    return r.returncode == 0 and bool(r.stdout.strip())


# --- links -------------------------------------------------------------------

def remap(path, moves):
    """Where a project-relative path lives after `moves` (files or whole folders)."""
    if path in moves:
        return moves[path]
    for src, dst in moves.items():
        if path.startswith(src + "/"):
            return dst + path[len(src):]
    return path


def link_fixes(project, moves):
    """([(old_file, new_file, new_text, [(old, new, now)])], [warning]) for every .md
    file whose relative links break under `moves`. Computed BEFORE moving, from the
    old tree; only the changed destinations differ, newlines included."""
    out, warnings = [], []
    for dirpath, dirs, files in os.walk(project):
        dirs[:] = sorted(d for d in dirs if d not in LINK_SKIP_DIRS
                         and not os.path.islink(os.path.join(dirpath, d)))
        for f in sorted(files):
            if not f.lower().endswith(".md"):
                continue
            old_file = rel(project, os.path.join(dirpath, f))
            new_file = remap(old_file, moves)
            if not safe(project, old_file):
                continue
            with open(os.path.join(dirpath, f), encoding="utf-8", errors="surrogateescape",
                      newline="") as fh:
                text = fh.read()
            changes = []

            def repoint(dest):
                bracketed = dest.startswith("<") and dest.endswith(">")
                raw = dest[1:-1] if bracketed else dest
                path, hash_, anchor = raw.partition("#")
                if (not path or re.match(r"^[a-z][a-z0-9+.-]*:", path, re.I)
                        or path.startswith("/")):
                    return dest
                old_dir = os.path.dirname(old_file)
                resolved = os.path.normpath(os.path.join(old_dir, unquote(path))).replace(os.sep, "/")
                if not os.path.exists(os.path.join(project, resolved)):
                    if new_file != old_file:
                        warnings.append("moved file has a link that does not resolve, left as "
                                        "written: {} -> {}".format(new_file, path))
                    return dest
                now = remap(resolved, moves)
                if now == resolved and new_file == old_file:
                    return dest
                new_path = os.path.relpath(now, os.path.dirname(new_file) or ".").replace(os.sep, "/")
                if not bracketed:
                    new_path = new_path.replace(" ", "%20")
                if new_path == path:
                    return dest
                changes.append((path, new_path, now))
                new_raw = new_path + hash_ + anchor
                return "<" + new_raw + ">" if bracketed else new_raw

            def outside_code(line):
                parts, last = [], 0
                for m in CODE_SPAN_RE.finditer(line):
                    parts.append(fix_segment(line[last:m.start()], last == 0))
                    parts.append(m.group(0))
                    last = m.end()
                parts.append(fix_segment(line[last:], last == 0))
                return "".join(parts)

            def fix_segment(seg, at_line_start):
                seg = INLINE_LINK_RE.sub(lambda m: m.group(1) + repoint(m.group(2)) + m.group(3), seg)
                if at_line_start:
                    seg = REF_DEF_RE.sub(lambda m: m.group(1) + repoint(m.group(2)), seg)
                return seg

            lines, fenced = [], False
            for line in text.splitlines(keepends=True):
                if line.lstrip().startswith(("```", "~~~")):
                    fenced = not fenced
                lines.append(line if fenced else outside_code(line))
            if changes:
                out.append((old_file, new_file, "".join(lines), changes))
    return out, warnings


# --- apply -------------------------------------------------------------------

def apply(project, plan, dry_run):
    today = datetime.date.today().isoformat()
    cands = {c["path"]: c for c in scan(project)}
    layout = load_layout(project)
    decisions = layout["decisions"]
    use_git = in_git(project)
    moves, actions, notes, remembered = {}, [], [], False

    for path in sorted(plan):
        choice = plan[path]
        if isinstance(choice, dict):
            choice = choice.get("decision")
        if choice not in ("move", "leave", "content"):
            raise SystemExit("plan: {!r} -> {!r} is not move | leave | content".format(path, choice))
        if choice in ("leave", "content"):
            if decisions.get(path, {}).get("decision") == choice:
                notes.append("already remembered: {} ({})".format(path, choice))
            else:
                decisions[path] = {"decision": choice, "date": today}
                remembered = True
                actions.append("remember {} as {}".format(path, choice))
            continue
        if not os.path.lexists(os.path.join(project, path)):
            notes.append("nothing to move (already moved or gone): {}".format(path))
            continue
        if path not in cands:
            notes.append("NOT MOVED — not a current candidate (the scan did not flag it, "
                         "or it is already settled): {}".format(path))
            continue
        if not (safe(project, path) and safe(project, cands[path]["target"])):
            notes.append("NOT MOVED — source or target passes through a symlink or leaves "
                         "the project: {}".format(path))
            continue
        moves[path] = cands[path]["target"]

    fixes, warnings = link_fixes(project, moves) if moves else ([], [])
    reports = list(warnings)
    for _, new_file, _, changes in fixes:
        if not new_file.startswith(".ai/"):
            for _, new_link, now in changes:
                if now.startswith(".ai/"):
                    reports.append("project content now links into .ai/: {} -> {} — "
                               "promote the target or drop the link".format(new_file, now))

    readme = os.path.join(project, ".ai", "README.md")
    print("MODE: {}".format("DRY RUN (no writes)" if dry_run else "APPLY (writing)"))
    for src, dst in sorted(moves.items()):
        how = "git mv" if use_git and tracked(project, src) else "move"
        actions.append("{} {} -> {}".format(how, src, dst))
    if moves and not os.path.exists(readme):
        actions.append("create .ai/README.md")
    for _, new_file, _, changes in fixes:
        for old_link, new_link, _ in changes:
            actions.append("relink {}: ({}) -> ({})".format(new_file, old_link, new_link))
    for a in actions:
        print("  " + a)
    for n in notes:
        print("  " + n)
    for r in reports:
        print("  " + r)
    if not actions:
        print("  nothing to do")
    if dry_run:
        return 0

    for src, dst in sorted(moves.items()):
        full_src, full_dst = os.path.join(project, src), os.path.join(project, dst)
        os.makedirs(os.path.dirname(full_dst), exist_ok=True)
        if use_git and tracked(project, src):
            r = git(project, "mv", "--", src, dst)
            if r.returncode != 0:
                raise SystemExit("git mv {} -> {} FAILED: {}".format(src, dst, r.stderr.strip()))
        else:
            shutil.move(full_src, full_dst)
    if moves and not os.path.exists(readme):
        open(readme, "w", encoding="utf-8").write(AI_README)
    for _, new_file, text, _ in fixes:
        if not safe(project, new_file):
            print("  NOT RELINKED — {} passes through a symlink or leaves the project"
                  .format(new_file))
            continue
        with open(os.path.join(project, new_file), "w", encoding="utf-8",
                  errors="surrogateescape", newline="") as fh:
            fh.write(text)
    if remembered:
        save_layout(project, layout)
    return 0


def decline(project):
    today = datetime.date.today().isoformat()
    layout = load_layout(project)
    cands = scan(project)
    for c in cands:
        layout["decisions"][c["path"]] = {"decision": "leave", "date": today}
    if cands:
        save_layout(project, layout)
    print("remembered {} candidate(s) as leave in .soul/layout.json; nothing else changed"
          .format(len(cands)))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan", help="list candidates (changes nothing)")
    s.add_argument("project")
    s.add_argument("--json", action="store_true")
    a = sub.add_parser("apply", help="carry out a plan of move | leave | content")
    a.add_argument("project")
    a.add_argument("--plan", required=True, help='JSON file: {"<path>": "move|leave|content"}')
    a.add_argument("--dry-run", action="store_true")
    d = sub.add_parser("decline", help="remember every candidate as leave")
    d.add_argument("project")
    args = ap.parse_args()

    project = os.path.realpath(args.project)
    if not os.path.isdir(project):
        ap.error("no project directory at {}".format(args.project))
    if args.cmd == "scan":
        cands = scan(project)
        if args.json:
            print(json.dumps({"project": project, "candidates": cands}, indent=2))
        else:
            print_scan(project, cands)
        return 0
    if args.cmd == "apply":
        plan = json.load(open(args.plan, encoding="utf-8"))
        return apply(project, plan, args.dry_run)
    return decline(project)


if __name__ == "__main__":
    sys.exit(main())
