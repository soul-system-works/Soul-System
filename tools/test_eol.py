"""Behaviour test for tools/eol.py (line endings: the repo decides).

FENCE: `fix` never sweeps the owner's work into the line-ending commit. With
anything staged, a tracked file changed by more than line endings (any change, for a
`-text` file), a file marked assume-unchanged or skip-worktree, or a .gitattributes
that is untracked or edited, it refuses and changes nothing (no .gitattributes, index
untouched). It never touches an untracked, binary or `-text` (Git LFS) file, stores a
`text eol=crlf` file LF but leaves its CRLF working copy, keeps an existing rule AFTER
its block so that rule still wins, and a second run is a no-op. The rule counts only
from the index. A failure partway exits 2 with what changed and how to undo it; a
re-check that still finds something exits 1. CRLF working copies are built by writing
bytes, never through core.autocrlf.

Run: python3 tools/test_eol.py  (exit 0 = PASS)
"""

import os
import shutil
import subprocess
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOL = os.path.join(_HERE, "eol.py")
_GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
                GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
                GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
FAILS = []

sys.path.insert(0, _HERE)
import eol  # noqa: E402


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else "  — " + detail))
    if not ok:
        FAILS.append(name)


def run(*args):
    return subprocess.run([sys.executable, _TOOL, *args], capture_output=True, text=True,
                          env=_GIT_ENV)


def git(cwd, *args):
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True,
                          env=_GIT_ENV)


def put(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def get(path):
    with open(path, "rb") as f:
        return f.read()


def repo(root, name, files, commit=True):
    p = os.path.join(root, name)
    for rel, data in files.items():
        put(os.path.join(p, rel), data)
    git(p, "init", "-q")
    if commit:
        git(p, "add", "-A")
        git(p, "commit", "-qm", "init")
    return p


def eol_of(p, rel):
    """(index eol, worktree eol, attr) from git ls-files --eol for one path."""
    out = git(p, "ls-files", "--eol", "--", rel).stdout
    info = out.partition("\t")[0].split()
    return (info[0], info[1], " ".join(info[2:])) if info else (None, None, None)


def main():
    os.environ.update(_GIT_ENV)  # eol._real_changes runs git in this process
    tmp = tempfile.mkdtemp(prefix="soul-eol-test-")
    keep = os.environ.get("SOUL_EOL_KEEP")  # set to keep the fixtures for a look

    # 1 — a clean LF repo with the rule: ok
    a = repo(tmp, "clean", {".gitattributes": eol.RULES.encode(), "a.txt": b"a\nb\n"})
    r = run("check", a)
    check("clean LF repo with the rule: exit 0", r.returncode == 0
          and r.stdout.startswith("line endings: ok (rule present, all LF)"), r.stdout + r.stderr)

    # 1b — the diff flags: --numstat honours --ignore-cr-at-eol, --name-only does not
    d = repo(tmp, "diffprobe", {"eolonly.txt": b"a\nb\n", "content.txt": b"a\nb\n",
                                "crlfidx.txt": b"a\r\nb\r\n"})
    put(os.path.join(d, "eolonly.txt"), b"a\r\nb\r\n")
    put(os.path.join(d, "content.txt"), b"a\nc\n")
    put(os.path.join(d, "crlfidx.txt"), b"a\nb\n")
    check("an EOL-only change is not a real change; a content change is",
          eol._real_changes(d) == ["content.txt"], repr(eol._real_changes(d)))
    names = git(d, "-c", "core.autocrlf=false", "diff", "--ignore-cr-at-eol",
                "--name-only").stdout.split()
    check("(why numstat) --name-only lists EOL-only changes even with the flag",
          "eolonly.txt" in names, repr(names))

    # 2 — no rule: committed CRLF and mixed counted, a CRLF working copy over LF counted
    lfs = b"*.pdf filter=lfs diff=lfs merge=lfs -text\n"
    binary = b"\x00\x01bin\r\nary\r\n\x00"
    files = {".gitattributes": lfs, "crlf.txt": b"one\r\ntwo\r\n", "mixed.txt": b"a\r\nb\n",
             "lf.txt": b"keep\n", "w.txt": b"w1\nw2\n", "run.bat": b"@echo off\r\nexit\r\n",
             "bin.dat": binary, "doc.pdf": b"%PDF\r\nnot really\r\n",
             "sub/deep.md": b"# deep\r\n"}
    b = repo(tmp, "mixed-up", files)
    put(os.path.join(b, "w.txt"), b"w1\r\nw2\r\n")  # what a Windows autocrlf checkout leaves
    put(os.path.join(b, "u.txt"), b"untracked\r\n")
    r = run("check", b)
    first = r.stdout.splitlines()[0] if r.stdout else ""
    check("no rule + CRLF: exit 1 with the summary line first", r.returncode == 1
          and first == "line endings: rule missing; 4 committed CRLF/mixed, 1 working copies CRLF",
          r.stdout + r.stderr)
    check("committed CRLF/mixed listed, binary and -text left out",
          all(n in r.stdout for n in ("crlf.txt", "mixed.txt", "run.bat", "sub/deep.md"))
          and "bin.dat" not in r.stdout and "doc.pdf" not in r.stdout, r.stdout)
    check("the CRLF working copy over an LF commit listed", "  w.txt" in r.stdout, r.stdout)
    check("untracked file not listed", "u.txt" not in r.stdout, r.stdout)
    check("autocrlf reported, Windows config named as not visible",
          "core.autocrlf in this git: not set" in r.stdout and "not visible" in r.stdout, r.stdout)

    head = git(b, "rev-parse", "HEAD").stdout
    index0 = git(b, "ls-files", "-s").stdout
    snap = {rel: get(os.path.join(b, rel)) for rel in list(files) + ["w.txt", "u.txt"]}

    # 3 — refusals change nothing
    put(os.path.join(b, "lf.txt"), b"keep\nstaged edit\n")
    git(b, "add", "lf.txt")
    index_staged = git(b, "ls-files", "-s").stdout
    r = run("fix", b)
    check("staged change: refused, exit 2", r.returncode == 2 and "staged" in r.stderr,
          r.stdout + r.stderr)
    check("staged refusal: .gitattributes unchanged, index unchanged",
          get(os.path.join(b, ".gitattributes")) == lfs
          and git(b, "ls-files", "-s").stdout == index_staged)
    git(b, "reset", "-q")
    put(os.path.join(b, "lf.txt"), b"keep\nan owner's edit\n")
    r = run("fix", b)
    check("real content edit: refused, exit 2, the file named", r.returncode == 2
          and "lf.txt" in r.stderr and "w.txt" not in r.stderr, r.stdout + r.stderr)
    check("content refusal: .gitattributes unchanged, index unchanged",
          get(os.path.join(b, ".gitattributes")) == lfs
          and git(b, "ls-files", "-s").stdout == index0)
    put(os.path.join(b, "lf.txt"), b"keep\n")
    check("refusals left every working file as it was",
          all(get(os.path.join(b, rel)) == data for rel, data in snap.items()))

    nogit = os.path.join(tmp, "not-a-repo")
    os.makedirs(nogit)
    check("not a git repo: check and fix exit 2",
          run("check", nogit).returncode == 2 and run("fix", nogit).returncode == 2)
    no_ga = repo(tmp, "no-ga", {"x.txt": b"x\r\n"})
    put(os.path.join(no_ga, "x.txt"), b"y\r\n")
    r = run("fix", no_ga)
    check("refusal with no .gitattributes leaves none behind", r.returncode == 2
          and not os.path.exists(os.path.join(no_ga, ".gitattributes")), r.stdout + r.stderr)

    # 4 — fix: rule first, existing LFS rule kept after; renormalize; rewrite working copies
    r = run("fix", b)
    check("fix succeeds", r.returncode == 0, r.stdout + r.stderr)
    ga = get(os.path.join(b, ".gitattributes"))
    check("the block is written first, the LFS line kept after it",
          ga.startswith(eol.RULES.encode()) and ga.endswith(lfs) and b"* text=auto eol=lf" in ga,
          repr(ga))
    check("the LFS rule still wins for *.pdf", "-text" in eol_of(b, "doc.pdf")[2],
          repr(eol_of(b, "doc.pdf")))
    check("committed CRLF file renormalized in the index",
          eol_of(b, "crlf.txt")[0] == "i/lf" and eol_of(b, "mixed.txt")[0] == "i/lf"
          and eol_of(b, "sub/deep.md")[0] == "i/lf", repr(eol_of(b, "crlf.txt")))
    check("CRLF working copies rewritten to LF",
          get(os.path.join(b, "crlf.txt")) == b"one\ntwo\n"
          and get(os.path.join(b, "mixed.txt")) == b"a\nb\n"
          and get(os.path.join(b, "w.txt")) == b"w1\nw2\n"
          and get(os.path.join(b, "sub/deep.md")) == b"# deep\n")
    check(".bat working copy stays CRLF", get(os.path.join(b, "run.bat")) == snap["run.bat"])
    check("binary file untouched byte for byte", get(os.path.join(b, "bin.dat")) == binary)
    check("-text (LFS) file untouched byte for byte, index too",
          get(os.path.join(b, "doc.pdf")) == snap["doc.pdf"] and eol_of(b, "doc.pdf")[0] == "i/crlf")
    check("untracked file untouched and still untracked",
          get(os.path.join(b, "u.txt")) == snap["u.txt"]
          and "?? u.txt" in git(b, "status", "--porcelain").stdout)
    check("nothing committed; the next step is suggested",
          git(b, "rev-parse", "HEAD").stdout == head and eol.COMMIT in r.stdout, r.stdout)
    staged = git(b, "diff", "--cached", "--name-only").stdout.split()
    check("renormalized files are reported", "crlf.txt" in r.stdout and "w.txt" in r.stdout
          and "crlf.txt" in staged and "w.txt" not in staged, r.stdout + repr(staged))
    status = git(b, "status", "--porcelain").stdout
    check("no unstaged change left behind", all(line[1] == " " or line.startswith("??")
                                                for line in status.splitlines()), status)
    r = run("check", b)
    check("check after fix: ok", r.returncode == 0, r.stdout)

    # 5 — a second run is a no-op, before and after the commit
    index1 = git(b, "ls-files", "-s").stdout
    snap1 = {rel: get(os.path.join(b, rel)) for rel in snap}
    r = run("fix", b)
    check("second fix before commit: no-op", r.returncode == 0 and "nothing to do" in r.stdout
          and git(b, "ls-files", "-s").stdout == index1
          and all(get(os.path.join(b, rel)) == data for rel, data in snap1.items()),
          r.stdout + r.stderr)
    git(b, "commit", "-qm", "eol")
    r = run("fix", b)
    check("fix after commit: no-op", r.returncode == 0 and "nothing to do" in r.stdout
          and git(b, "status", "--porcelain").stdout.strip() == "?? u.txt", r.stdout + r.stderr)

    # 6 — rule already present, only a CRLF working copy: no .gitattributes change
    c = repo(tmp, "has-rule", {".gitattributes": eol.RULES.encode(), "t.txt": b"t\n"})
    put(os.path.join(c, "t.txt"), b"t\r\n")
    r = run("check", c)
    check("rule present + CRLF working copy: exit 1", r.returncode == 1 and r.stdout.startswith(
          "line endings: rule present; 0 committed CRLF/mixed, 1 working copies CRLF"), r.stdout)
    r = run("fix", c)
    check("fix with the rule present: .gitattributes untouched, copy rewritten",
          r.returncode == 0 and "already in effect" in r.stdout
          and get(os.path.join(c, ".gitattributes")) == eol.RULES.encode()
          and get(os.path.join(c, "t.txt")) == b"t\n", r.stdout + r.stderr)

    # 7 — a bare `* text=auto` is not the rule: working copies stay each machine's call
    d = repo(tmp, "bare-auto", {".gitattributes": b"* text=auto\n", "t.txt": b"t\n"})
    put(os.path.join(d, "t.txt"), b"t\r\n")
    r = run("check", d)
    check("bare text=auto: rule missing, exit 1", r.returncode == 1
          and r.stdout.startswith("line endings: rule missing"), r.stdout)
    r = run("fix", d)
    r2 = run("check", d)
    check("fix over bare text=auto: block first, old line kept, copy LF, check ok",
          r.returncode == 0 and r2.returncode == 0
          and get(os.path.join(d, ".gitattributes")).startswith(eol.RULES.encode())
          and get(os.path.join(d, ".gitattributes")).endswith(b"* text=auto\n")
          and get(os.path.join(d, "t.txt")) == b"t\n", r.stdout + r.stderr + r2.stdout)

    # 8 — assume-unchanged / skip-worktree: `git diff` skips them, so an edit hides from
    #     the fence and renormalize would stage it. Refused, the files named, nothing changed.
    e = repo(tmp, "assume", {"a.txt": b"a\n", "c.txt": b"c\r\n"})
    git(e, "update-index", "--assume-unchanged", "a.txt")
    put(os.path.join(e, "a.txt"), b"a\npassword=hunter2\n")
    idx = git(e, "ls-files", "-s").stdout
    r = run("fix", e)
    check("assume-unchanged file: refused, exit 2, the file named", r.returncode == 2
          and "a.txt" in r.stderr and "assume-unchanged" in r.stderr, r.stdout + r.stderr)
    check("assume-unchanged refusal: no .gitattributes, index unchanged",
          not os.path.exists(os.path.join(e, ".gitattributes"))
          and git(e, "ls-files", "-s").stdout == idx)
    e = repo(tmp, "skip", {"s.txt": b"s\n", "c.txt": b"c\r\n"})
    git(e, "update-index", "--skip-worktree", "s.txt")
    put(os.path.join(e, "s.txt"), b"s\r\n")
    r = run("fix", e)
    check("skip-worktree file: refused, exit 2, named, its bytes untouched", r.returncode == 2
          and "s.txt" in r.stderr and get(os.path.join(e, "s.txt")) == b"s\r\n"
          and not os.path.exists(os.path.join(e, ".gitattributes")), r.stdout + r.stderr)

    # 9 — a leading BOM in .gitattributes is stripped, or it lands mid-file and git
    #     ignores the old first rule (an LFS rule: the full binary would be staged)
    bom = b"\xef\xbb\xbf*.dat -text\n"
    e = repo(tmp, "bom", {".gitattributes": bom, "d.dat": b"x\r\ny\r\n", "c.txt": b"c\r\n"})
    r = run("fix", e)
    ga = get(os.path.join(e, ".gitattributes"))
    check("BOM stripped: no BOM in .gitattributes, the old first rule kept after the block",
          r.returncode == 0 and b"\xef\xbb\xbf" not in ga and ga.endswith(b"\n*.dat -text\n"),
          repr(ga) + r.stderr)
    check("BOM: the old first rule still in effect (-text file not renormalized)",
          "-text" in eol_of(e, "d.dat")[2] and eol_of(e, "d.dat")[0] == "i/crlf",
          repr(eol_of(e, "d.dat")))

    # 10 — .gitattributes is the owner's work when untracked or changed: refused
    e = repo(tmp, "ga-untracked", {"c.txt": b"c\r\n"})
    put(os.path.join(e, ".gitattributes"), b"*.dat -text\n")
    r = run("fix", e)
    check("untracked .gitattributes: refused, exit 2, said so, file and index untouched",
          r.returncode == 2 and ".gitattributes" in r.stderr and "untracked" in r.stderr
          and get(os.path.join(e, ".gitattributes")) == b"*.dat -text\n"
          and git(e, "ls-files", "--", ".gitattributes").stdout == "", r.stdout + r.stderr)
    e = repo(tmp, "ga-modified", {".gitattributes": b"*.dat -text\n", "c.txt": b"c\r\n"})
    put(os.path.join(e, ".gitattributes"), b"*.dat -text\n*.bin -text\n")
    r = run("fix", e)
    check("tracked .gitattributes with an uncommitted edit: refused, file untouched",
          r.returncode == 2 and ".gitattributes" in r.stderr
          and get(os.path.join(e, ".gitattributes")) == b"*.dat -text\n*.bin -text\n",
          r.stdout + r.stderr)

    # 11 — the rule counts only when the commit will carry it: read from the index, with
    #      no global or system attributes file
    e = repo(tmp, "rule-untracked", {"c.txt": b"c\n"})
    put(os.path.join(e, ".gitattributes"), eol.RULES.encode())
    r = run("check", e)
    check("a rule only in an untracked .gitattributes: rule missing, exit 1",
          r.returncode == 1 and r.stdout.startswith("line endings: rule missing"), r.stdout)
    e = repo(tmp, "rule-global", {"c.txt": b"c\n"})
    xdg = os.path.join(tmp, "xdg")
    put(os.path.join(xdg, "git", "attributes"), b"* text eol=lf\n")
    r = subprocess.run([sys.executable, _TOOL, "check", e], capture_output=True, text=True,
                       env=dict(_GIT_ENV, XDG_CONFIG_HOME=xdg))
    check("a rule only in this machine's global attributes file: rule missing, exit 1",
          r.returncode == 1 and r.stdout.startswith("line endings: rule missing"), r.stdout)

    # 12 — a failure partway (index.lock held; a file that cannot be rewritten) ends in
    #      a report of what changed and how to undo it, exit 2, no traceback
    e = repo(tmp, "locked", {"c.txt": b"c\r\n"})
    put(os.path.join(e, ".git", "index.lock"), b"")
    r = run("fix", e)
    out = r.stdout + r.stderr
    check("index.lock held: exit 2, .gitattributes reported written, undo named",
          r.returncode == 2 and "Traceback" not in out and "already changed" in out
          and ".gitattributes written" in out and "delete .gitattributes" in out, out)
    os.remove(os.path.join(e, ".git", "index.lock"))
    e = repo(tmp, "readonly", {"c.txt": b"c\r\n", "w.txt": b"w\n"})
    put(os.path.join(e, "w.txt"), b"w\r\n")
    os.chmod(os.path.join(e, "w.txt"), 0o444)
    r = run("fix", e)
    out = r.stdout + r.stderr
    os.chmod(os.path.join(e, "w.txt"), 0o644)
    check("a copy that cannot be rewritten: exit 2, no traceback, what changed and the undo",
          r.returncode == 2 and "Traceback" not in out and "already changed" in out
          and "c.txt" in out and "git restore --staged ." in out, out)
    check("the new .gitattributes is readable by others (atomic write keeps a normal mode)",
          os.stat(os.path.join(e, ".gitattributes")).st_mode & 0o044 == 0o044,
          oct(os.stat(os.path.join(e, ".gitattributes")).st_mode))

    # 13 — a CR-only change to a `-text` file is content, not line endings: refused
    e = repo(tmp, "minus-text", {".gitattributes": eol.RULES.encode() + b"*.dat -text\n",
                                 "d.dat": b"a\nb\n", "w.txt": b"w\n"})
    put(os.path.join(e, "d.dat"), b"a\r\nb\r\n")
    put(os.path.join(e, "w.txt"), b"w\r\n")
    r = run("fix", e)
    check("CR-only change to a -text file: refused, exit 2, the file named",
          r.returncode == 2 and "d.dat" in r.stderr
          and git(e, "diff", "--cached", "--name-only").stdout == "", r.stdout + r.stderr)

    # 14 — `text eol=crlf` stored with CRLF is reported and renormalized to LF in the
    #      index; its CRLF working copy is correct and left alone
    e = repo(tmp, "crlf-stored", {"run.bat": b"@echo off\r\n"})
    put(os.path.join(e, ".gitattributes"), eol.RULES.encode())
    git(e, "add", ".gitattributes")
    git(e, "commit", "-qm", "rule")
    r = run("check", e)
    check("eol=crlf file stored CRLF: reported, exit 1", r.returncode == 1
          and "  run.bat" in r.stdout and eol_of(e, "run.bat")[0] == "i/crlf",
          r.stdout + repr(eol_of(e, "run.bat")))
    r = run("fix", e)
    r2 = run("check", e)
    check("fix stores it LF, the working copy stays CRLF, check ok",
          r.returncode == 0 and eol_of(e, "run.bat")[0] == "i/lf"
          and get(os.path.join(e, "run.bat")) == b"@echo off\r\n" and r2.returncode == 0,
          r.stdout + r.stderr + r2.stdout)

    # 15 — the probe has no extension (a `*.txt` rule is not a catch-all); fix re-checks
    #      at the end and exits 1 when something still remains
    e = repo(tmp, "txt-only", {".gitattributes": b"*.txt text eol=lf\n", "n.md": b"n\r\n"})
    r = run("check", e)
    check("a *.txt-only rule is not the catch-all: rule missing",
          r.stdout.startswith("line endings: rule missing"), r.stdout)
    e = repo(tmp, "unset-eol", {".gitattributes": b"* !eol\n", "t.txt": b"t\r\n"})
    r = run("fix", e)
    check("a later `* !eol` defeats the block: fix exits 1 and says the rule is still missing",
          r.returncode == 1 and "still" in r.stdout and "rule missing" in r.stdout,
          r.stdout + r.stderr)
    check("exit 1 does not tell the owner to commit, and gives the undo",
          "Next: git commit" not in r.stdout and "git restore --staged ." in r.stdout,
          r.stdout)

    # 16 — renormalize fails partway (an unreadable tracked file): the report names
    #      what git already staged and gives the undo, never "Nothing had changed yet."
    g = repo(tmp, "partial-renorm", {".gitattributes": eol.RULES.encode(),
                                     "a.txt": b"a\n", "z.txt": b"z\n"}, commit=False)
    os.utime(os.path.join(g, "z.txt"), (1577836800, 1577836800))  # not racily clean
    git(g, "add", "-A")
    git(g, "commit", "-qm", "init")
    git(g, "config", "core.trustctime", "false")  # chmod must not make git re-read it
    put(os.path.join(g, "a.txt"), b"a\r\n")      # stored CRLF, bypassing the rule
    git(g, "-c", "core.autocrlf=false", "update-index", "--add", "--cacheinfo",
        "100644,{},a.txt".format(
            subprocess.run(["git", "-C", g, "hash-object", "-w", "--no-filters", "a.txt"],
                           capture_output=True, text=True, env=_GIT_ENV).stdout.strip()))
    git(g, "commit", "-qm", "crlf stored")
    os.chmod(os.path.join(g, "z.txt"), 0)
    r = run("fix", g)
    os.chmod(os.path.join(g, "z.txt"), 0o644)
    staged = git(g, "diff", "--cached", "--name-only").stdout.split()
    check("renormalize fails partway: exit 2, staged files named, undo given",
          r.returncode == 2 and "Nothing had changed yet" not in r.stderr
          and staged == ["a.txt"] and "a.txt" in r.stderr
          and "git restore --staged ." in r.stderr,
          "staged={} {}".format(staged, r.stdout + r.stderr))

    if keep:
        print("fixtures kept at " + tmp)
    else:
        shutil.rmtree(tmp, ignore_errors=True)
    print("\n{} failure(s)".format(len(FAILS)) if FAILS else "\nALL PASS")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
