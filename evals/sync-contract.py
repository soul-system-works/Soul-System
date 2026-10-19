#!/usr/bin/env python3
"""Embed the current project contract into every eval case's system prompt.

Why this exists: `claude plugin eval` runs do not load a workspace CLAUDE.md, so
the contract (operations/CLAUDE.md) would reach neither arm. Each case instead
carries it in its prompt.md frontmatter as `append_system_prompt`, which the
harness passes to BOTH arms (with-plugin and the no-plugin baseline) — so the
arms differ only by what the plugin adds (hooks, skills), not by doctrine.

Hand-copying the contract into three cases would drift the first time the
contract changes; this script is the only writer of that key. Verbatim text, no
sentinel line added.

    python3 evals/sync-contract.py           # rewrite stale cases in place
    python3 evals/sync-contract.py --check   # exit 1 if any case is stale

Stdlib only. A case is any directory under evals/ holding a prompt.md, except
`results/`, `mocks/` and names starting with `_` or `.`.
"""
import argparse
import sys
from pathlib import Path

EVALS = Path(__file__).resolve().parent
CONTRACT = EVALS.parent / "operations" / "CLAUDE.md"
KEY = "append_system_prompt"
SKIP = {"results", "mocks", "node_modules"}


def block_scalar(text):
    """`KEY: |` block for `text`, chomping chosen so YAML yields `text` exactly."""
    if text.endswith("\n\n"):
        chomp = "+"
    elif text.endswith("\n"):
        chomp = ""
    else:
        chomp = "-"
    lines = text.split("\n")
    if text.endswith("\n"):
        lines = lines[:-1]
    # An explicit indentation indicator is needed only if the first line starts
    # with a space; give it always when that happens, never otherwise.
    indent = "2" if lines and lines[0].startswith(" ") else ""
    body = "\n".join(("  " + ln) if ln else "" for ln in lines)
    return f"{KEY}: |{indent}{chomp}\n{body}\n"


def split_frontmatter(src, path):
    if not src.startswith("---\n"):
        raise SystemExit(f"{path}: no YAML frontmatter (expected a leading '---' line)")
    end = src.find("\n---\n", 3)
    if end == -1:
        raise SystemExit(f"{path}: unterminated frontmatter")
    return src[4:end + 1], src[end + 1:]  # (frontmatter incl. final \n, '---\n' + body)


def strip_key(fm):
    """Drop an existing top-level KEY and every indented/blank line under it."""
    out, skipping = [], False
    for ln in fm.splitlines(keepends=True):
        if skipping:
            if ln.strip() == "" or ln[0] in " \t":
                continue
            skipping = False
        if ln.startswith(KEY + ":"):
            skipping = True
            continue
        out.append(ln)
    return "".join(out)


def render(src, path, contract):
    fm, rest = split_frontmatter(src, path)
    return "---\n" + strip_key(fm) + block_scalar(contract) + rest


def cases():
    found = []
    for d in sorted(EVALS.iterdir()):
        if not d.is_dir() or d.name in SKIP or d.name[0] in "_.":
            continue
        if (d / "prompt.md").is_file():
            found.append(d / "prompt.md")
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="exit 1 if any case is stale; write nothing")
    args = ap.parse_args()

    contract = CONTRACT.read_text(encoding="utf-8")
    prompts = cases()
    if not prompts:
        print(f"no cases found under {EVALS}", file=sys.stderr)
        return 1

    stale = []
    for p in prompts:
        src = p.read_text(encoding="utf-8")
        want = render(src, p, contract)
        if want == src:
            continue
        stale.append(p)
        if not args.check:
            p.write_text(want, encoding="utf-8")

    rel = lambda p: p.relative_to(EVALS.parent)
    if args.check:
        for p in stale:
            print(f"stale: {rel(p)} (run python3 evals/sync-contract.py)", file=sys.stderr)
        if not stale:
            print(f"ok: {len(prompts)} case(s) carry the current {rel(CONTRACT)}")
        return 1 if stale else 0
    for p in stale:
        print(f"updated: {rel(p)}")
    print(f"{len(prompts) - len(stale)} already current, {len(stale)} updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
