#!/usr/bin/env python3
"""Line endings: make the repo decide, not each machine's core.autocrlf.

On one machine with Windows git (Sourcetree) set to `core.autocrlf=true` and WSL git
set to nothing, the two disagree about every file: Windows checks files out CRLF,
WSL git then sees each one as modified, and `git add -A` from WSL commits CRLF.
Tools that write LF (this plugin's, an AI's edits) then leave files of mixed
endings. The fix is per repo: a `.gitattributes` catch-all `* text=auto eol=lf`
overrides every machine's autocrlf; then the committed files are renormalized and
the CRLF working copies rewritten to LF.

FENCE: `fix` never sweeps the owner's work into the line-ending commit. It refuses,
changing nothing, while anything is staged, any tracked file has a change that is not
only line endings (`git add --renormalize .` stages every tracked file's working
content; for a `-text` file a CR is content, so any change counts), any file is
marked assume-unchanged or skip-worktree (`git diff` cannot see their edits), or
`.gitattributes` is untracked or has uncommitted edits (it is the owner's work). It
never commits, and never touches an untracked, binary or `-text` (Git LFS) file. A
`text eol=crlf` file committed with CRLF is renormalized like any text file: stored
LF, as that rule means; its CRLF working copy is correct and is not rewritten.

The rule counts as in effect only when the INDEX carries it (the commit must hold it):
`check-attr --cached`, with no global or system attributes file. Known limit:
`.git/info/attributes` still applies to that check, and it is never committed.

  check <repo>   rule in effect? committed CRLF/mixed files? CRLF working copies?
                 exit 0 ok, 1 needs fix, 2 not a git repo / error
  fix <repo>     write the rule (existing rules kept after it, so they still win),
                 renormalize, rewrite CRLF working copies; stage only, never commit.
                 exit 0 done or nothing to do; 1 done, but the re-check still finds
                 something (printed); 2 refused (nothing changed), or stopped partway
                 by an error (what had changed and how to undo it are printed)
"""

import argparse
import os
import subprocess
import sys
import tempfile

# vault.py imports this for the vault's own .gitattributes. A later rule wins in
# .gitattributes, so this block goes FIRST and an existing line such as Git LFS's
# `*.pdf filter=lfs diff=lfs merge=lfs -text` keeps its effect.
RULES = """# Line endings: the repo decides, not each machine's core.autocrlf (Soul tools/eol.py).
* text=auto eol=lf
*.bat text eol=crlf
*.cmd text eol=crlf
*.sln text eol=crlf
"""

# Need not exist: check-attr answers for any path. No extension, so a `*.txt`-only
# rule is not mistaken for the catch-all.
PROBE = "soul-eol-probe"
EXAMPLES = 10
BOM = b"\xef\xbb\xbf"
COMMIT = 'git commit -m "Line endings: the repo decides (.gitattributes, renormalize)"'


class EolError(Exception):
    pass


def _git(top, *args, env=None):
    return subprocess.run(["git", "-C", top, *args], capture_output=True,
                          encoding="utf-8", errors="surrogateescape", env=env)


def _top(repo):
    r = _git(repo, "rev-parse", "--show-toplevel")
    if r.returncode != 0 or not r.stdout.strip():
        raise EolError("{} is not a git repository (or has no working tree)".format(repo))
    return r.stdout.strip()


# ---------------------------------------------------------------- facts

def rule_in_effect(top):
    """True when a catch-all attribute decides line endings for an arbitrary path:
    `eol` set to lf or crlf. A bare `* text=auto` does not count: it normalizes
    commits but leaves working copies to each machine's core.autocrlf — the
    problem this tool exists to end — and `fix` rewrites only `eol=lf` files.
    Read from the index (`--cached`): an untracked or uncommitted .gitattributes would
    not reach the commit. `core.attributesFile=` (empty) drops the global file and
    GIT_ATTR_NOSYSTEM the system one; `.git/info/attributes` still applies (a known
    limit — git has no switch for it)."""
    r = _git(top, "-c", "core.attributesFile=", "check-attr", "--cached", "text", "eol",
             "--", PROBE, env=dict(os.environ, GIT_ATTR_NOSYSTEM="1"))
    if r.returncode != 0:
        raise EolError("git check-attr failed: " + r.stderr.strip())
    vals = {}
    for line in r.stdout.splitlines():  # "soul-eol-probe: eol: lf"
        parts = line.rsplit(": ", 2)
        if len(parts) == 3:
            vals[parts[1]] = parts[2]
    return vals.get("eol") in ("lf", "crlf")


def _entries(top):
    """[(index eol, worktree eol, attr tokens, path)] from `git ls-files --eol`."""
    r = _git(top, "ls-files", "--eol", "-z")
    if r.returncode != 0:
        raise EolError("git ls-files --eol failed: " + r.stderr.strip())
    out = []
    for rec in r.stdout.split("\0"):
        info, sep, path = rec.partition("\t")
        parts = info.split()
        if not sep or len(parts) < 3:
            continue
        attr = " ".join(parts[2:])[len("attr/"):]
        out.append((parts[0][len("i/"):], parts[1][len("w/"):], attr.split(), path))
    return out


def _not_text(attr):
    """Binary / Git LFS (`-text`): its bytes are content, never ours to change."""
    return "-text" in attr


def _crlf_copy_ok(attr):
    """`-text`, or a deliberate `eol=crlf`: a CRLF working copy is correct."""
    return _not_text(attr) or "eol=crlf" in attr


def facts(top):
    entries = _entries(top)
    # A `text eol=crlf` file is stored LF too (git converts on checkout), so a stored
    # CRLF copy counts; only its working copy is meant to be CRLF.
    committed = [p for i, w, a, p in entries
                 if i in ("crlf", "mixed") and not _not_text(a)]
    working = [p for i, w, a, p in entries
               if i == "lf" and w in ("crlf", "mixed") and not _crlf_copy_ok(a)]
    autocrlf = _git(top, "config", "--get", "core.autocrlf").stdout.strip()
    return {"rule": rule_in_effect(top), "committed": committed, "working": working,
            "autocrlf": autocrlf}


def _ok(f):
    return f["rule"] and not f["committed"] and not f["working"]


def _examples(title, paths, file=None, indent=""):
    if not paths:
        return
    print("{}{} ({}):".format(indent, title, len(paths)), file=file)
    for p in paths[:EXAMPLES]:
        print(indent + "  " + p, file=file)
    if len(paths) > EXAMPLES:
        print(indent + "  ... and {} more".format(len(paths) - EXAMPLES), file=file)


# ---------------------------------------------------------------- check

def check(repo):
    top = _top(repo)
    f = facts(top)
    if _ok(f):
        print("line endings: ok (rule present, all LF)")
    else:
        print("line endings: rule {}; {} committed CRLF/mixed, {} working copies CRLF".format(
            "present" if f["rule"] else "missing", len(f["committed"]), len(f["working"])))
    _examples("committed with CRLF or mixed endings", f["committed"])
    _examples("working copies CRLF or mixed over an LF commit", f["working"])
    print("core.autocrlf in this git: {} (a Windows-side git such as Sourcetree keeps its "
          "own config, not visible from here)".format(f["autocrlf"] or "not set"))
    if not _ok(f):
        print("fix: python3 {} fix {}".format(os.path.abspath(__file__), top))
    return 0 if _ok(f) else 1


# ---------------------------------------------------------------- fix

def _numstat(top, *flags):
    r = _git(top, "-c", "core.autocrlf=false", "diff", *flags, "--numstat",
             "-z", "--no-renames", "--no-ext-diff", "--no-textconv")
    if r.returncode != 0:
        raise EolError("git diff failed: " + r.stderr.strip())
    out = []
    for rec in r.stdout.split("\0"):
        parts = rec.split("\t", 2)
        if len(parts) == 3:
            out.append(parts[2])
    return out


def _real_changes(top):
    """Tracked files whose working copy differs from the index by more than line
    endings. `--name-only` lists EOL-only changes even with --ignore-cr-at-eol;
    `--numstat` honours the flag and omits them (and still lists a mode change as
    0 0, a deletion, and a binary edit as - -). A `-text` file's bytes are content,
    so a CR-only change to one is real: a second pass without the flag catches it."""
    out = _numstat(top, "--ignore-cr-at-eol")
    not_text = {p for i, w, a, p in _entries(top) if _not_text(a)}
    out += [p for p in _numstat(top) if p in not_text and p not in out]
    return out


def _hidden(top):
    """Files marked assume-unchanged (a lowercase `ls-files -v` tag) or skip-worktree
    (`S`): `git diff` does not look at them, so the fence cannot see their edits."""
    r = _git(top, "ls-files", "-v", "-z")
    if r.returncode != 0:
        raise EolError("git ls-files -v failed: " + r.stderr.strip())
    return [rec[2:] for rec in r.stdout.split("\0")
            if len(rec) > 2 and (rec[0].islower() or rec[0] == "S")]


def _refuse(msg, paths=()):
    print("eol: refused — " + msg + " Nothing changed.", file=sys.stderr)
    for p in paths[:EXAMPLES]:
        print("  " + p, file=sys.stderr)
    if len(paths) > EXAMPLES:
        print("  ... and {} more".format(len(paths) - EXAMPLES), file=sys.stderr)
    return 2


def _refusal(top):
    """The fence. Exit code 2 after saying why, or None when fix may go ahead."""
    staged = _git(top, "diff", "--cached", "--quiet")
    if staged.returncode not in (0, 1):
        raise EolError("git diff --cached failed: " + staged.stderr.strip())
    if staged.returncode == 1:
        return _refuse("something is already staged, and the line-ending change must be a "
                       "commit of its own. Commit or unstage it, then run fix again.")
    hidden = _hidden(top)
    if hidden:
        return _refuse("{} file(s) are marked assume-unchanged or skip-worktree, so git "
                       "cannot see their edits and `git add --renormalize .` could stage "
                       "them (or fail on them). Clear the marks (`git update-index "
                       "--no-assume-unchanged` / `--no-skip-worktree`), then run fix "
                       "again.".format(len(hidden)), hidden)
    real = _real_changes(top)
    ga = os.path.join(top, ".gitattributes")
    tracked = _git(top, "ls-files", "-z", "--", ".gitattributes").stdout.strip("\0")
    if os.path.lexists(ga) and not tracked:
        return _refuse(".gitattributes exists but is untracked. It is your work, and fix "
                       "would write into it and stage all of it. Commit it (or move it "
                       "aside), then run fix again.")
    if ".gitattributes" in real:
        return _refuse(".gitattributes has uncommitted edits. It is your work, and fix "
                       "would write into it and stage them. Commit or stash them, then run "
                       "fix again.")
    if real:
        return _refuse("{} tracked file(s) have changes that are not only line endings, "
                       "and `git add --renormalize .` would stage them into the line-ending "
                       "commit. Commit or stash them, then run fix again.".format(len(real)),
                       real)
    return None


def _write_atomic(path, data):
    """Temp file in the same directory, then os.replace: never a half-written file."""
    try:
        mode = os.stat(path).st_mode & 0o7777
    except FileNotFoundError:
        mask = os.umask(0)
        os.umask(mask)
        mode = 0o666 & ~mask
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".gitattributes.",
                               suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def _apply(top, f, done):
    """The changes, in order. `done` records each one as it lands, so a failure
    partway can say exactly what had changed."""
    if f["rule"]:
        print("rule: already in effect, .gitattributes not changed")
    else:
        ga = os.path.join(top, ".gitattributes")
        existing, existed = b"", os.path.exists(ga)
        if existed:
            with open(ga, "rb") as fh:
                existing = fh.read()
        # A leading BOM would land mid-file after the block, and git would read the
        # old first rule as a different pattern (an LFS rule then stops applying).
        if existing.startswith(BOM):
            existing = existing[len(BOM):]
        # The block first: existing rules after it still win.
        _write_atomic(ga, RULES.encode("utf-8") + (b"\n" + existing if existing else b""))
        done["ga"] = "changed" if existed else "new"
        r = _git(top, "add", "--", ".gitattributes")
        if r.returncode != 0:
            raise EolError("git add .gitattributes failed: " + r.stderr.strip())
        done["ga_staged"] = True
        print("rule: written at the top of .gitattributes{}".format(
            " (existing rules kept after it)" if existing else ""))

    r = _git(top, "add", "--renormalize", "--", ".")
    # Read what is staged even on failure: git stages every file it could read
    # before exiting 1, and the partial report must name those (scoped review).
    done["renormalized"] = [
        n for n in _git(top, "diff", "--cached", "--name-only", "-z").stdout.split("\0")
        if n and n != ".gitattributes"]
    if r.returncode != 0:
        raise EolError("git add --renormalize failed: " + r.stderr.strip())
    _examples("renormalized in the index", done["renormalized"])
    if not done["renormalized"]:
        print("renormalized in the index: none")

    for i, w, a, p in _entries(top):
        if i != "lf" or w not in ("crlf", "mixed") or _crlf_copy_ok(a) \
                or "eol=lf" not in a:
            continue
        path = os.path.join(top, p)
        if os.path.islink(path) or not os.path.isfile(path):
            continue
        with open(path, "rb") as fh:
            data = fh.read()
        new = data.replace(b"\r\n", b"\n")
        if new != data:
            with open(path, "wb") as fh:
                fh.write(new)
            done["rewritten"].append(p)
    if done["rewritten"]:
        # The index still holds each rewritten file's old (CRLF) size, and git reports
        # a size change as modified without reading the content. Re-adding records the
        # new stat; the content already equals the staged blob, so nothing else stages.
        r = subprocess.run(["git", "-C", top, "--literal-pathspecs", "add",
                            "--pathspec-from-file=-", "--pathspec-file-nul"],
                           input="\0".join(done["rewritten"]), capture_output=True,
                           encoding="utf-8", errors="surrogateescape")
        if r.returncode != 0:
            raise EolError("git add of the rewritten copies failed: " + r.stderr.strip())
    _examples("working copies rewritten to LF", done["rewritten"])
    if not done["rewritten"]:
        print("working copies rewritten to LF: none")


def _report_partial(done, exc):
    err = sys.stderr
    print("eol: fix stopped partway — {}: {}".format(type(exc).__name__, exc), file=err)
    staged = done["ga_staged"] or done["renormalized"] is not None
    if not (done["ga"] or staged or done["rewritten"]):
        print("Nothing had changed yet.", file=err)
        return
    print("already changed:", file=err)
    if done["ga"]:
        print("  .gitattributes written ({}), {}".format(
            "a new file" if done["ga"] == "new" else "the block added at the top",
            "staged" if done["ga_staged"] else "not staged"), file=err)
    if done["renormalized"] is not None:
        _examples("renormalized in the index", done["renormalized"], err, "  ")
        if not done["renormalized"]:
            print("  renormalized in the index: none", file=err)
    _examples("working copies rewritten to LF", done["rewritten"], err, "  ")
    print("to undo:", file=err)
    if staged:
        print("  git restore --staged .   (fix checked that nothing else was staged)",
              file=err)
    if done["ga"] == "new":
        print("  delete .gitattributes   (it was new)", file=err)
    elif done["ga"]:
        print("  git checkout -- .gitattributes", file=err)
    if done["rewritten"]:
        print("  the rewritten working copies hold the same content with LF endings; "
              "after the restore, `git checkout -- <file>` brings back the committed "
              "bytes if wanted", file=err)


def fix(repo):
    top = _top(repo)
    f = facts(top)
    if _ok(f):
        print("line endings: already ok (rule present, all LF) — nothing to do")
        return 0
    refused = _refusal(top)
    if refused is not None:
        return refused

    done = {"ga": None, "ga_staged": False, "renormalized": None, "rewritten": []}
    try:
        _apply(top, f, done)
    except Exception as exc:  # a traceback or a silent half-change hides what changed
        _report_partial(done, exc)
        return 2

    staged = _git(top, "diff", "--cached", "--quiet").returncode == 1
    after = facts(top)  # the re-check: the index and working copies as fix left them
    if _ok(after):
        if staged:
            print("staged, not committed. Next: " + COMMIT)
        return 0
    if staged:
        print("staged, not committed — do not commit yet; to undo: git restore --staged .")
    print("line endings: still not ok — rule {}; {} committed CRLF/mixed, {} working "
          "copies CRLF".format("present" if after["rule"] else "missing",
                               len(after["committed"]), len(after["working"])))
    _examples("committed with CRLF or mixed endings", after["committed"])
    _examples("working copies CRLF or mixed over an LF commit", after["working"])
    if not after["rule"]:
        print("a later line in .gitattributes, or .git/info/attributes, overrides the "
              "block's `eol=lf` for an arbitrary path")
    return 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="report the repo's line-ending state")
    c.add_argument("repo")
    x = sub.add_parser("fix", help="write the rule, renormalize, rewrite CRLF working copies")
    x.add_argument("repo")
    args = ap.parse_args()
    try:
        return check(args.repo) if args.cmd == "check" else fix(args.repo)
    except EolError as exc:
        print("eol: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
