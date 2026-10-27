#!/usr/bin/env python3
"""Hand a /soul-workflow step to a worker harness, in its own process and worktree.

The host session (whatever harness and model the Body started in) keeps judgment and
the record; workers are other harness+model pairs that get only a brief (SOUL-I080).
This tool is the thin layer between them: it reads the roles table, starts the
worker through that harness's headless CLI with the host's context kept out, and
hands back the evidence — the patch, the exit, the wall time, the tokens — never a
verdict. It never records: the host re-runs the check through
tools/delegation-check.py, because a worker's report is a claim (SOUL-I066).

  roles  [--project DIR] [--json]                    the effective roles table
  run    --role R --brief FILE [--project DIR] [--base REF] [--check CMD]
         [--rung K] [--run-id ID]                    implement, n tries, pick one
  review --role R --brief FILE --diff FILE [--project DIR] [--run-id ID]
                                                     every reviewer of R, read-only
  clean  --run-id ID [--project DIR]                 remove a run's worktrees+branches

Roles table: `~/.claude/soul-roles.md` (global) and `<project>/.claude/soul-roles.md`,
a Markdown table `| role | harness | model | settings |` — settings `key=value`
separated by spaces, only `rung`, `n` (best-of-n) and `timeout` (seconds). A
project that defines any row for a role replaces ALL global rows for that role.
A role's rows are its ladder, ordered by rung (row order when none is given).
Built-in default for a role neither file names: implementer claude:sonnet then
claude:opus; reviewer claude:opus, plus codex:default when `codex` is on PATH.

`run` makes each try a worktree `<project>/.ai/worktrees/<run-id>-<i>` on branch
`soul-wf/<run-id>-<i>` from --base (default HEAD), stages everything the worker left
(untracked too, never committed), writes the diff against base to
`<project>/.ai/workflow-runs/<run-id>/try-<i>.patch`, and runs --check there only to
pick the winner: check passed, then fewest changed lines. Tries run one at a time
(a GPU holds one model). result.json (review.json for `review`) holds what was seen.

POSIX only (Linux, macOS, WSL): a timed-out worker's whole process group is killed.
"""

import argparse
import json
import os
import re
import shutil
import sys

HARNESSES = ("claude", "claude-ollama", "codex", "codex-ollama")
SETTINGS = ("rung", "n", "timeout")
DEFAULT_TIMEOUT = 1800
GLOBAL_ROLES = os.path.join("~", ".claude", "soul-roles.md")
PROJECT_ROLES = os.path.join(".claude", "soul-roles.md")


class RolesError(Exception):
    """A roles file that cannot be used; the message names the file, line and row."""


# ---------------------------------------------------------------- roles table

def _cells(line):
    text = line.strip()
    if text.endswith("|"):
        text = text[:-1]
    return [c.strip() for c in text[1:].split("|")]


def _row_error(path, lineno, line, why):
    return RolesError("{}:{}: {} — row: {}".format(path, lineno, why, line.strip()))


def parse_roles_file(path, source):
    """Rows of one roles file, in file order; [] when the file does not exist.

    Only table lines (starting with `|`) are read, so prose around the table is
    free; the header row (first cell `role`) and the `|---|` separator are skipped.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
    except FileNotFoundError:
        return []
    rows = []
    position = {}
    for lineno, line in enumerate(lines, 1):
        if not line.lstrip().startswith("|"):
            continue
        cells = _cells(line)
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c) and any(cells):
            continue  # the separator row
        if cells and cells[0].lower() == "role":
            continue  # the header row
        if len(cells) not in (3, 4):
            raise _row_error(path, lineno, line,
                             "a row needs role | harness | model | settings")
        role, harness, model = cells[:3]
        for name, value in (("role", role), ("harness", harness), ("model", model)):
            if not value:
                raise _row_error(path, lineno, line, "blank {}".format(name))
        if harness not in HARNESSES:
            raise _row_error(path, lineno, line, "unknown harness {!r} (known: {})"
                             .format(harness, ", ".join(HARNESSES)))
        if harness == "claude-ollama" and model == "default":
            # Step 1 probe, 2026-10-27: Ollama answers "model not found" unless the
            # model is an exact installed tag, so there is no default to fall back on.
            raise _row_error(path, lineno, line,
                             "claude-ollama needs an exact installed Ollama tag, not default")
        settings = {}
        for item in (cells[3].split() if len(cells) == 4 else []):
            key, eq, value = item.partition("=")
            if not eq or not key or not value:
                raise _row_error(path, lineno, line,
                                 "setting {!r} is not key=value".format(item))
            if key not in SETTINGS:
                raise _row_error(path, lineno, line, "unknown setting {!r} (known: {})"
                                 .format(key, ", ".join(SETTINGS)))
            try:
                number = int(value)
            except ValueError:
                raise _row_error(path, lineno, line,
                                 "setting {} must be a whole number, got {!r}"
                                 .format(key, value)) from None
            if number < 1:
                raise _row_error(path, lineno, line,
                                 "setting {} must be 1 or more, got {}".format(key, number))
            settings[key] = number
        position[role] = position.get(role, 0) + 1
        rows.append({"role": role, "harness": harness, "model": model,
                     "rung": settings.get("rung", position[role]),
                     "n": settings.get("n", 1),
                     "timeout": settings.get("timeout", DEFAULT_TIMEOUT),
                     "source": source, "where": "{}:{}".format(path, lineno)})
    return rows


def builtin_rows(which=shutil.which):
    def row(role, harness, model, rung):
        return {"role": role, "harness": harness, "model": model, "rung": rung, "n": 1,
                "timeout": DEFAULT_TIMEOUT, "source": "built-in", "where": None}
    rows = [row("implementer", "claude", "sonnet", 1),
            row("implementer", "claude", "opus", 2),
            row("reviewer", "claude", "opus", 1)]
    if which("codex"):
        rows.append(row("reviewer", "codex", "default", 2))
    return rows


def load_roles(project):
    """{role: [rows ordered by rung]} — project over global over built-in, per role."""
    layers = [builtin_rows(),
              parse_roles_file(os.path.expanduser(GLOBAL_ROLES), "global"),
              parse_roles_file(os.path.join(project, PROJECT_ROLES), "project")]
    table = {}
    for rows in layers:
        named = {}
        for r in rows:
            named.setdefault(r["role"], []).append(r)
        table.update(named)  # a layer that names a role replaces all its earlier rows
    return {role: sorted(rows, key=lambda r: r["rung"])  # stable: row order on ties
            for role, rows in sorted(table.items())}


def flat(table):
    return [r for rows in table.values() for r in rows]


def cmd_roles(args):
    table = load_roles(project_dir(args.project, need_git=False))
    if args.json:
        print(json.dumps(flat(table), indent=2))
        return 0
    print("{:<12} {:<5} {:<14} {:<22} {:<3} {:<8} {}".format(
        "role", "rung", "harness", "model", "n", "timeout", "source"))
    for r in flat(table):
        print("{:<12} {:<5} {:<14} {:<22} {:<3} {:<8} {}".format(
            r["role"], r["rung"], r["harness"], r["model"], r["n"], r["timeout"],
            r["source"] + (" ({})".format(r["where"]) if r["where"] else "")))
    return 0


# ---------------------------------------------------------------- shared

def project_dir(path, need_git=True):
    return os.path.abspath(path or os.getcwd())


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("roles", help="show the effective roles table")
    p.add_argument("--project", help="project directory (default: here)")
    p.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        return {"roles": cmd_roles}[args.cmd](args)
    except RolesError as e:
        print("error: {}".format(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
