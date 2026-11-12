"""Behaviour test for tools/vault.py (the Soul vault, SOUL-I079).

FENCE: a record is never lost or silently unwired. The move must leave every file
readable through the link with the same bytes; a `restricted` project and a second
record for a key the vault already holds are refused with nothing changed; a broken
link is reported, never silent (it turns the completion gate off and git stays quiet).
Junctions are not exercised here (the fixtures live on the Linux filesystem); the
live junction check is a throwaway run under /mnt/d (recorded with the 3.4.0 release).

Run: python3 tools/test_vault.py  (exit 0 = PASS)
"""

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

_TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vault.py")
# A session's env config (GIT_CONFIG_COUNT/KEY/VALUE) points git's hooks at the guard's
# folder; the sync cases need the vault's own .git/hooks to run, so it is dropped here.
_GIT_ENV = dict({k: v for k, v in os.environ.items()
                 if not re.match(r"GIT_CONFIG_(COUNT|KEY_|VALUE_|PARAMETERS)", k)},
                GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
                GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
                GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else "  — " + detail))
    if not ok:
        FAILS.append(name)


def run(env, *args, stdin=None):
    return subprocess.run([sys.executable, _TOOL, *args], capture_output=True, text=True,
                          env=env, input=stdin)


def git(cwd, *args):
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True,
                          env=_GIT_ENV)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def read(path):
    return open(path, encoding="utf-8").read()


def project(root, name, files, remote=None, commit=False):
    p = os.path.join(root, name)
    for rel, text in files.items():
        write(os.path.join(p, rel), text)
    git(p, "init", "-q")
    if remote:
        git(p, "remote", "add", "origin", remote)
    if commit:
        git(p, "add", "-A")
        git(p, "commit", "-qm", "init")
    return p


def sync_fixture(tmp, env, name):
    """A vault with a bare remote, another project's committed record, project P linked
    as key `syncer`, and a second clone of the remote (another machine)."""
    b = os.path.join(tmp, "sync-" + name)
    bare, v, clone = (os.path.join(b, n) for n in ("remote.git", "vault", "clone"))
    os.makedirs(b)
    git(b, "init", "-q", "--bare", "-b", "main", bare)
    run(env, "init", v)
    write(os.path.join(v, "projects", "other", "soul", "witness.md"), "# other\nline1\n")
    git(v, "init", "-q", "-b", "main")
    git(v, "add", "-A")
    git(v, "commit", "-qm", "vault")
    git(v, "remote", "add", "origin", bare)
    git(v, "push", "-q", "-u", "origin", "main")
    p = project(b, "proj", {".soul/witness.md": "# W\n"})
    r = run(env, "link", p, "--key", "syncer", "--label", "private", "--vault", v)
    if r.returncode != 0:
        check("sync fixture {} links".format(name), False, r.stderr + r.stdout)
    git(b, "clone", "-q", bare, clone)
    return p, v, bare, clone


def remote_commit(clone, rel, text, msg="m2"):
    git(clone, "pull", "-q")
    write(os.path.join(clone, rel), text)
    git(clone, "add", "-A")
    git(clone, "commit", "-qm", msg)
    git(clone, "push", "-q")


def hook(v, name, body):
    path = os.path.join(v, ".git", "hooks", name)
    write(path, "#!/bin/sh\n" + body)
    os.chmod(path, 0o755)


def worktrees(v):
    return git(v, "worktree", "list", "--porcelain").stdout.count("worktree ")


def tree_bytes(d):
    """{path: bytes} for every file under d except .git — ignored files included."""
    out = {}
    for dirpath, dirnames, filenames in os.walk(d):
        dirnames[:] = [n for n in dirnames if n != ".git"]
        for n in filenames:
            p = os.path.join(dirpath, n)
            out[os.path.relpath(p, d)] = open(p, "rb").read()
    return out


def sync_cases(tmp, env):
    """Sync never touches the shared vault tree outside its own commit, and pushes only
    when the server has not moved (fresh-context reviews of 3.11.0: cases A, B, F, K
    from the first, E1, the ignored-file overwrite and index.md from the second)."""
    rev = lambda d, ref="HEAD": git(d, "rev-parse", ref).stdout.strip()
    ow = os.path.join("projects", "other", "soul", "witness.md")
    mine = os.path.join("soul", "witness.md")
    lockf = lambda v: os.path.join(v, ".git", "soul-sync.lock")

    def untouched(name, v, before, r, server, bare):
        check(name + ": exit 2, NOT PUSHED, the server unchanged", r.returncode == 2
              and "NOT PUSHED" in r.stderr and rev(bare, "main") == server, r.stdout + r.stderr)
        check(name + ": every file in the vault byte-identical, nothing stashed, no lock",
              tree_bytes(v) == before and git(v, "stash", "list").stdout == ""
              and not os.path.exists(lockf(v)) and worktrees(v) == 1,
              str(sorted(k for k in set(tree_bytes(v)) | set(before)
                         if tree_bytes(v).get(k) != before.get(k))))

    # A — the server changed another project's file that a session here has edited
    p, v, bare, clone = sync_fixture(tmp, env, "A")
    remote_commit(clone, ow, "# other\nline1\nfrom machine 2\n")
    write(os.path.join(v, ow), "# other\nline1\nlocal work of session X\n")
    write(os.path.join(p, ".soul", "witness.md"), "# W\nA1\n")
    server, before = rev(bare, "main"), tree_bytes(v)
    r = run(env, "sync", p)
    untouched("A", v, before, r, server, bare)
    check("A: our commit is kept here", "A1" in git(v, "show", "HEAD:projects/syncer/" + mine).stdout)
    px = project(os.path.join(tmp, "sync-A"), "projX", {"README.md": "x\n"})
    os.symlink(os.path.join(v, "projects", "other", "soul"), os.path.join(px, ".soul"))
    r = run(env, "sync", px)
    check("A: that session's sync stops too: no conflict markers anywhere",
          r.returncode == 2 and "<<<<<<<" not in read(os.path.join(v, ow))
          and "<<<<<<<" not in git(bare, "show", "main:" + ow).stdout, r.stdout + r.stderr)

    # B — a session's uncommitted edit while the server moved: never stashed
    p, v, bare, clone = sync_fixture(tmp, env, "B")
    remote_commit(clone, os.path.join("projects", "far", "soul", "witness.md"), "# far\n")
    write(os.path.join(v, ow), "# other\nline1\nsession X: D1\n")
    hook(v, "post-rewrite", 'printf "session X: D2\\n" >> "{}"\n'.format(os.path.join(v, ow)))
    write(os.path.join(p, ".soul", "witness.md"), "# W\nB1\n")
    server, before = rev(bare, "main"), tree_bytes(v)
    r = run(env, "sync", p)
    untouched("B", v, before, r, server, bare)

    # F — a session writes while sync runs (the hook fires when sync's fetch updates the
    #     remote-tracking ref): the write survives; the test fails if the hook never fired
    p, v, bare, clone = sync_fixture(tmp, env, "F")
    remote_commit(clone, os.path.join("projects", "syncer", mine), "# W\nfrom machine 2\n")
    write(os.path.join(v, ow), "# other\nline1\nsession X: D1\n")
    fired = os.path.join(tmp, "sync-F", "fired")
    hook(v, "reference-transaction",
         '[ "$1" = committed ] || exit 0\nrefs=$(cat)\n[ -e "{0}" ] && exit 0\n'
         'case "$refs" in *refs/remotes/*) ;; *) exit 0 ;; esac\n'
         'touch "{0}"\nprintf "session X: D2 mid-sync\\n" >> "{1}"\n'
         .format(fired, os.path.join(v, ow)))
    write(os.path.join(p, ".soul", "witness.md"), "# W\nF1 here\n")
    server = rev(bare, "main")
    r = run(env, "sync", p)
    text = read(os.path.join(v, ow))
    check("F: the mid-run write fired and survives, with D1; NOT PUSHED; commit kept here",
          os.path.exists(fired) and "session X: D1" in text and "D2 mid-sync" in text
          and r.returncode == 2 and "NOT PUSHED" in r.stderr and rev(bare, "main") == server
          and "F1 here" in git(v, "show", "HEAD:projects/syncer/" + mine).stdout,
          r.stdout + r.stderr + text)

    # K — a path someone staged stays staged when the server moved
    p, v, bare, clone = sync_fixture(tmp, env, "K")
    remote_commit(clone, os.path.join("projects", "far", "soul", "witness.md"), "# far\n")
    write(os.path.join(v, ow), "# other\nline1\nstaged edit\n")
    git(v, "add", ow)
    write(os.path.join(p, ".soul", "handoff.md"), "# H\n")
    server, before = rev(bare, "main"), tree_bytes(v)
    r = run(env, "sync", p)
    untouched("K", v, before, r, server, bare)
    check("K: the staged path stays staged and uncommitted",
          ow.replace(os.sep, "/") in git(v, "diff", "--cached", "--name-only").stdout
          and "staged edit" not in git(v, "show", "HEAD:" + ow).stdout,
          git(v, "status", "--porcelain").stdout)

    # The server moved with another machine's tracked copy of a file that is ignored and
    # different here (an events.jsonl): never overwritten (review 2: read-tree did)
    p, v, bare, clone = sync_fixture(tmp, env, "ignored")
    ev = os.path.join("projects", "other", "soul", "events.jsonl")
    git(clone, "pull", "-q")
    write(os.path.join(clone, ev), '{"theirs": 1}\n')
    git(clone, "add", "-f", ev)
    git(clone, "commit", "-qm", "theirs")
    git(clone, "push", "-q")
    write(os.path.join(v, ev), '{"mine": 1}\n')
    write(os.path.join(p, ".soul", "witness.md"), "# W\nI1\n")
    server, before = rev(bare, "main"), tree_bytes(v)
    r = run(env, "sync", p)
    untouched("ignored file", v, before, r, server, bare)

    # E1 — the upstream names a server branch that does not exist: nothing claimed pushed
    p, v, bare, clone = sync_fixture(tmp, env, "E1")
    empty = os.path.join(tmp, "sync-E1", "empty.git")
    git(tmp, "init", "-q", "--bare", "-b", "main", empty)
    git(v, "remote", "add", "empty", empty)
    git(v, "config", "branch.main.remote", "empty")
    write(os.path.join(p, ".soul", "witness.md"), "# W\nE1\n")
    r = run(env, "sync", p)
    check("E1: the server branch is missing: exit 2, NOT PUSHED, never 'pushed'",
          r.returncode == 2 and "NOT PUSHED" in r.stderr and "pushed\n" not in r.stdout
          and git(empty, "branch", "--list").stdout == "", r.stdout + r.stderr)

    # BH — everything here is already on the server, which has moved on: not NOT PUSHED
    p, v, bare, clone = sync_fixture(tmp, env, "BH")
    write(os.path.join(p, ".soul", "witness.md"), "# W\nBH\n")
    run(env, "sync", p)
    remote_commit(clone, "projects/far/soul/witness.md", "# far\n")
    r = run(env, "sync", p)
    check("BH: already on the server, copy behind: exit 0, says so, not NOT PUSHED",
          r.returncode == 0 and "already on the server" in r.stdout
          and "NOT PUSHED" not in r.stderr, r.stdout + r.stderr)

    # PULL — the merge the NOT PUSHED line names actually works (index.md dirty, and the
    #        server changed it too): the pull is named first, the discard only as the step
    #        after git refuses over index.md
    pull = lambda v: git(v, "-c", "pull.rebase=true", "-c", "rebase.autostash=true", "pull",
                         "-q", "--no-rebase", "--no-autostash", "--no-edit")
    p, v, bare, clone = sync_fixture(tmp, env, "PULL")
    remote_commit(clone, "index.md", "# index from the other machine\n")
    write(os.path.join(v, "index.md"), "# regenerated here\n")
    write(os.path.join(p, ".soul", "witness.md"), "# W\nPULL\n")
    r = run(env, "sync", p)
    line = r.stderr
    at = lambda s: line.find(s)
    ok = (r.returncode == 2 and -1 < at("--no-rebase --no-autostash")
          < at("checkout -- index.md"))
    m0 = pull(v)
    m1 = git(v, "checkout", "--", "index.md")
    m2 = pull(v)
    r2 = run(env, "sync", p)
    check("PULL: the named pull is refused over index.md, the named discard then lets it "
          "merge on diverged branches, then sync pushes", ok and m0.returncode != 0
          and "index.md" in m0.stderr and m1.returncode == 0 and m2.returncode == 0
          and r2.returncode == 0 and "pushed" in r2.stdout
          and git(v, "stash", "list").stdout == "", line + m2.stderr + r2.stdout + r2.stderr)

    # PULL-ELSEWHERE — the server changed another file, index.md is dirty here: the line
    #        names the pull alone (no discard: auto mode refuses `checkout --`, GAME-WEB and
    #        SENSOR-BED 2026-11-09/10), and that command alone merges and keeps index.md
    p, v, bare, clone = sync_fixture(tmp, env, "PULL-ELSEWHERE")
    remote_commit(clone, os.path.join("projects", "far", "soul", "witness.md"), "# far\n")
    write(os.path.join(v, "index.md"), "# regenerated here\n")
    write(os.path.join(p, ".soul", "witness.md"), "# W\nPE\n")
    r = run(env, "sync", p)
    line = r.stderr
    named = re.findall(r"`(git -C \S+ [^`]*)`", line)
    m = (subprocess.run(["git", "-c", "pull.rebase=true", "-c", "rebase.autostash=true"]
                        + named[0].split()[1:], capture_output=True, text=True, env=_GIT_ENV,
                        stdin=subprocess.DEVNULL)
         if len(named) == 1 else None)
    r2 = run(env, "sync", p)
    check("PULL-ELSEWHERE: the line names only the pull, no checkout; it merges with "
          "index.md dirty and kept; the next sync pushes", r.returncode == 2
          and "checkout" not in line and len(named) == 1 and "pull --no-rebase "
          "--no-autostash" in named[0] and m is not None and m.returncode == 0
          and read(os.path.join(v, "index.md")) == "# regenerated here\n"
          and r2.returncode == 0 and "pushed" in r2.stdout
          and git(bare, "show", "main:projects/syncer/" + mine).stdout == "# W\nPE\n"
          and git(v, "stash", "list").stdout == "",
          line + (m.stderr if m else "") + r2.stdout + r2.stderr)

    # A refused push (the server's hook says no): exit 2
    p, v, bare, clone = sync_fixture(tmp, env, "refused")
    write(os.path.join(bare, "hooks", "pre-receive"), "#!/bin/sh\nexit 1\n")
    os.chmod(os.path.join(bare, "hooks", "pre-receive"), 0o755)
    write(os.path.join(p, ".soul", "witness.md"), "# W\nR1\n")
    server = rev(bare, "main")
    r = run(env, "sync", p)
    check("a refused push: exit 2, NOT PUSHED, the server unchanged",
          r.returncode == 2 and "NOT PUSHED" in r.stderr and "refused" in r.stderr
          and rev(bare, "main") == server, r.stdout + r.stderr)

    # I — no upstream: committed here, NOT PUSHED, and not a success
    p, v, bare, clone = sync_fixture(tmp, env, "I")
    git(v, "branch", "--unset-upstream")
    write(os.path.join(p, ".soul", "new.md"), "n\n")
    r = run(env, "sync", p)
    check("I: no upstream: NOT PUSHED, exit 2", r.returncode == 2 and "NOT PUSHED" in r.stderr,
          r.stdout + r.stderr)

    # A failed run (the server is unreachable) leaves no lock behind
    p, v, bare, clone = sync_fixture(tmp, env, "fail")
    git(v, "remote", "set-url", "origin", os.path.join(tmp, "no-such-remote.git"))
    write(os.path.join(p, ".soul", "x.md"), "x\n")
    r = run(env, "sync", p)
    check("a failed run: exit 2, the lock removed", r.returncode == 2
          and not os.path.exists(lockf(v)), r.stdout + r.stderr)

    # J — a killed sync leaves only its lock (git finishes on its own and leaves no lock of
    #     its own); the next sync reports it as stale with the removal step
    p, v, bare, clone = sync_fixture(tmp, env, "J")
    mark = os.path.join(tmp, "sync-J", "in-push")
    hook(v, "pre-push", 'touch "{}"\nsleep 2\n'.format(mark))
    write(os.path.join(p, ".soul", "handoff.md"), "# H\n")
    proc = subprocess.Popen([sys.executable, _TOOL, "sync", p], env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for _ in range(200):
        if os.path.exists(mark):
            break
        time.sleep(0.05)
    proc.send_signal(signal.SIGTERM)
    proc.communicate(timeout=30)
    time.sleep(3)  # the orphaned git push finishes its hook and exits
    r = run(env, "sync", p)
    check("J: killed: only soul-sync.lock is left; the next sync says it looks stale, "
          "with the removal step", os.path.exists(mark) and r.returncode == 4
          and "looks stale" in r.stderr and "remove " + lockf(v) in r.stderr
          and not os.path.exists(os.path.join(v, ".git", "index.lock"))
          and not os.path.exists(os.path.join(v, ".git", "HEAD.lock")), r.stderr)
    if os.path.exists(lockf(v)):
        os.remove(lockf(v))
    r = run(env, "sync", p)
    check("J: after the lock is removed by hand, sync runs", r.returncode == 0, r.stdout + r.stderr)

    # The lock: a live holder is "held", a dead one "looks stale" with the removal step
    p, v, bare, clone = sync_fixture(tmp, env, "lock")
    lock = lockf(v)
    host = __import__("socket").gethostname()
    write(lock, "pid={} host={} key=x started=now\n".format(os.getpid(), host))
    r = run(env, "sync", p)
    check("a live holder: exit 4, held by a running sync, no removal step",
          r.returncode == 4 and "held by a running sync" in r.stderr and "remove" not in r.stderr,
          r.stderr)
    write(lock, "pid=999999 host={} key=x started=now\n".format(host))
    r = run(env, "sync", p)
    check("a dead holder: exit 4, looks stale, says remove <path> after checking",
          r.returncode == 4 and "looks stale" in r.stderr and "remove " + lock in r.stderr
          and os.path.exists(lock), r.stderr)

def main():
    tmp = tempfile.mkdtemp(prefix="soul-vault-test-")
    env = dict(_GIT_ENV, XDG_CONFIG_HOME=os.path.join(tmp, "config"), SOUL_VAULT_FORCE_WSL="0")
    vault = os.path.join(tmp, "vault")

    # 1 — init scaffolds, never overwrites, registers one vault per machine
    r = run(env, "init", vault, "--register")
    check("init scaffolds", r.returncode == 0 and all(os.path.exists(os.path.join(vault, f))
          for f in ("vault.md", ".gitignore", "index.md", "projects")), r.stderr)
    ga = os.path.join(vault, ".gitattributes")
    check("init writes the line-ending rule", os.path.isfile(ga)
          and "* text=auto eol=lf" in read(ga))
    write(os.path.join(vault, "vault.md"), "# mine\n")
    r = run(env, "init", vault, "--register")
    check("init never overwrites", r.returncode == 0 and read(os.path.join(vault, "vault.md")) == "# mine\n")
    check("where names the vault", run(env, "where").stdout.strip() == vault)
    other = os.path.join(tmp, "other-vault")
    r = run(env, "init", other, "--register")
    check("a second vault on one machine is refused", r.returncode == 2
          and read(os.path.join(tmp, "config", "soul", "vault")).strip() == vault, r.stderr)

    # 2 — .soul layout, untracked record: moved, same bytes through the link, wired
    files = {".soul/witness.md": "# W\nSOUL-1\n", ".soul/ideas.md": "# I\n",
             ".soul/mind.md": "# Mind\n", ".soul/sub/deep.md": "deep\n",
             ".claude/settings.local.json": json.dumps({"permissions": {"allow": ["Bash(ls)"]}}),
             "CLAUDE.md": "@~/soul/operations/CLAUDE.md\n@.soul/mind.md\n", "README.md": "x\n"}
    a = project(tmp, "alpha", files, remote="git@example.com:me/alpha.git")
    git(a, "add", "README.md", "CLAUDE.md")
    git(a, "commit", "-qm", "init")
    r = run(env, "link", a, "--key", "alpha", "--label", "private", "--contributes", "soul,tools")
    soul = os.path.join(a, ".soul")
    target = os.path.join(vault, "projects", "alpha", "soul")
    check("link succeeds", r.returncode == 0, r.stderr + r.stdout)
    check(".soul is now a link into the vault", os.path.islink(soul)
          and os.path.realpath(soul) == os.path.realpath(target))
    check("every file reads the same through the link",
          all(read(os.path.join(a, rel)) == text for rel, text in files.items()
              if rel.startswith(".soul/")))
    check("no parked copy left behind", not os.path.exists(soul + ".vault-moving"))
    pm = read(os.path.join(vault, "projects", "alpha", "project.md"))
    check("project.md carries label, tags, remote", "label: private" in pm
          and "contributes: [soul, tools]" in pm and "remote: git@example.com:me/alpha.git" in pm, pm)
    st = json.load(open(os.path.join(a, ".claude", "settings.local.json")))
    check("vault allowed, other settings kept",
          os.path.realpath(vault) in st["permissions"]["additionalDirectories"]
          and st["permissions"]["allow"] == ["Bash(ls)"], json.dumps(st))
    status = git(a, "status", "--porcelain").stdout
    check("git status is clean of .soul and the local settings", status.strip() == "", status)
    write(os.path.join(soul, "witness.md"), "# W\nSOUL-1\nSOUL-2\n")
    check("a write through the link lands in the vault",
          "SOUL-2" in read(os.path.join(target, "witness.md")))
    r = run(env, "link", a, "--key", "alpha", "--label", "private")
    exclude = read(os.path.join(a, ".git", "info", "exclude"))
    check("re-running link is a no-op", r.returncode == 0 and "already linked" in r.stdout
          and exclude.splitlines().count(".soul") == 1, r.stdout + r.stderr)

    # 3 — root layout, tracked: stores moved into .soul/, Mind import repointed, tracked named
    b = project(tmp, "beta", {"witness.md": "# W\n", "ideas.md": "# I\n", "mind.md": "# M\n",
                              "CLAUDE.md": "@~/soul/operations/CLAUDE.md\n@mind.md\n"}, commit=True)
    r = run(env, "link", b, "--key", "beta", "--label", "public")
    check("root layout links", r.returncode == 0, r.stderr)
    check("root stores now read through .soul", all(os.path.isfile(os.path.join(b, ".soul", n))
          for n in ("witness.md", "ideas.md", "mind.md"))
          and not os.path.exists(os.path.join(b, "witness.md")))
    check("Mind import repointed", "@.soul/mind.md" in read(os.path.join(b, "CLAUDE.md"))
          and "\n@mind.md" not in read(os.path.join(b, "CLAUDE.md")))
    check("still-tracked record named for the owner", "STILL TRACKED" in r.stdout
          and "witness.md" in r.stdout, r.stdout)

    # 4 — refusals change nothing
    c = project(tmp, "gamma", {".soul/witness.md": "# W\n"})
    r = run(env, "link", c, "--key", "gamma", "--label", "restricted")
    check("restricted refused, nothing changed", r.returncode == 2 and not os.path.islink(
          os.path.join(c, ".soul")) and not os.path.exists(os.path.join(vault, "projects", "gamma")),
          r.stderr)
    r = run(env, "link", c, "--key", "alpha", "--label", "private")
    check("a second record for a held key refused", r.returncode == 2
          and os.path.isdir(os.path.join(c, ".soul")) and not os.path.islink(os.path.join(c, ".soul")),
          r.stderr)
    write(os.path.join(c, ".claude", "settings.local.json"), "{ not json")
    r = run(env, "link", c, "--key", "gamma", "--label", "private")
    check("invalid local settings: refused before anything moves", r.returncode == 2
          and read(os.path.join(c, ".claude", "settings.local.json")) == "{ not json"
          and not os.path.islink(os.path.join(c, ".soul"))
          and not os.path.exists(os.path.join(vault, "projects", "gamma")), r.stderr)
    write(os.path.join(c, ".claude", "settings.local.json"), '{"permissions": []}')
    r = run(env, "link", c, "--key", "gamma", "--label", "private")
    check("misshaped local settings: refused before anything moves", r.returncode == 2
          and not os.path.islink(os.path.join(c, ".soul")), r.stderr)
    os.remove(os.path.join(c, ".claude", "settings.local.json"))
    os.makedirs(os.path.join(c, ".soul.vault-moving"))
    r = run(env, "link", c, "--key", "gamma", "--label", "private")
    check("a leftover parked copy refuses the run", r.returncode == 2
          and not os.path.islink(os.path.join(c, ".soul")), r.stderr)
    os.rmdir(os.path.join(c, ".soul.vault-moving"))
    r = run(env, "link", c, "--key", "../x", "--label", "private")
    check("a key with a path in it refused", r.returncode == 2, r.stderr)

    # 4b — a same-named project from another repo is never matched or linked
    d = project(os.path.join(tmp, "elsewhere"), "alpha", {"README.md": "x\n"},
                remote="git@example.com:someone/else.git")
    r = run(env, "check", d, "--json")
    check("different remote, same name: no match", json.loads(r.stdout)["vault_has"] is None,
          r.stdout)
    r = run(env, "link", d, "--key", "alpha", "--label", "private")
    check("different remote: link refused", r.returncode == 2
          and not os.path.lexists(os.path.join(d, ".soul")), r.stderr)

    h = project(os.path.join(tmp, "nr1"), "site", {".soul/witness.md": "# A\n"})
    run(env, "link", h, "--key", "site", "--label", "private")
    h2 = project(os.path.join(tmp, "nr2"), "site", {".soul/witness.md": "# B\n"},
                 remote="git@github.com:me/site.git")
    r = run(env, "check", h2)
    check("no remote in the vault, a remote here: no TWO COPIES alarm", r.returncode == 0
          and "TWO COPIES" not in r.stdout, r.stdout)
    h3 = project(tmp, "alpha-case", {"README.md": "x\n"}, remote="git@github.com:Me/Alpha.git")
    write(os.path.join(vault, "projects", "casey", "project.md"),
          "---\nkey: casey\nremote: https://github.com/me/alpha\n---\n")
    os.makedirs(os.path.join(vault, "projects", "casey", "soul"))
    r = run(env, "check", h3, "--json")
    check("github remotes match regardless of letter case",
          json.loads(r.stdout)["vault_has"] == "casey", r.stdout)

    # 4c — root-layout edge cases: CRLF kept, list-form import repointed, odd forms flagged,
    #      a credential in the remote never reaches the vault
    e = project(tmp, "delta", {"witness.md": "# W\n", "mind.md": "# M\n",
                               "AGENTS.md": "x\r\n- @mind.md\r\n",
                               "CLAUDE.md": "see mind.md for notes\n"},
                remote="https://me:ghp_SECRET@example.com/me/delta.git")
    r = run(env, "link", e, "--key", "delta", "--label", "private")
    agents = open(os.path.join(e, "AGENTS.md"), "rb").read()
    check("CRLF kept and the list-form import repointed",
          agents == b"x\r\n- @.soul/mind.md\r\n", repr(agents))
    check("a mind.md mention not repointed is flagged", "CHECK BY HAND: CLAUDE.md" in r.stdout,
          r.stdout)
    check("no credential in project.md",
          "ghp_SECRET" not in read(os.path.join(vault, "projects", "delta", "project.md")))
    lm = project(tmp, "local-md", {"witness.md": "# W\n", "mind.md": "# M\n",
                                   "CLAUDE.local.md": "@~/soul/operations/CLAUDE.md\n@mind.md\n"})
    r = run(env, "link", lm, "--key", "local-md", "--label", "private")
    check("the Mind import in CLAUDE.local.md is repointed too (mining pass 3)",
          r.returncode == 0 and "@.soul/mind.md" in read(os.path.join(lm, "CLAUDE.local.md")),
          r.stdout + r.stderr)

    # 5 — a new machine: the clone has no record, the vault holds it → found and re-linked
    a2 = project(tmp, "alpha-clone", {"README.md": "x\n"}, remote="https://example.com/me/alpha")
    r = run(env, "check", a2, "--json")
    check("check finds the vault's record by remote", json.loads(r.stdout)["vault_has"] == "alpha",
          r.stdout)
    r = run(env, "link", a2, "--key", "alpha", "--label", "private")
    check("relink on a new machine", r.returncode == 0 and "SOUL-2" in read(
          os.path.join(a2, ".soul", "witness.md")), r.stderr + r.stdout)

    # 5b — a git reset of a still-tracked record splits it: check says TWO COPIES
    git(b, "reset", "-q", "--hard")
    r = run(env, "check", b)
    check("reset of a tracked record: TWO COPIES reported", r.returncode == 1
          and "TWO COPIES" in r.stdout, r.stdout + r.stderr)
    out = json.loads(run(env, "session-start", stdin=json.dumps({"cwd": b})).stdout or "{}")
    check("two copies is loud at session start", "TWO COPIES" in out.get("systemMessage", ""))

    g = project(tmp, "epsilon", {".soul/witness.md": "# W\n", "README.md": "x\n"}, commit=True)
    run(env, "link", g, "--key", "epsilon", "--label", "private")
    git(g, "reset", "-q", "--hard")
    r = run(env, "check", g)
    check("reset of a tracked .soul/: link replaced, TWO COPIES reported", r.returncode == 1
          and "TWO COPIES" in r.stdout and not os.path.islink(os.path.join(g, ".soul")),
          r.stdout + r.stderr)

    # 5c — a broken link only re-links to the key its target named
    f = project(tmp, "one", {"README.md": "x\n"})
    os.symlink(os.path.join(vault, "projects", "one", "soul"), os.path.join(f, ".soul"))
    r = run(env, "link", f, "--key", "alpha", "--label", "private")
    check("broken link re-linked only to its own key", r.returncode == 2
          and not os.path.exists(os.path.join(f, ".soul")), r.stderr)

    # 5d — a vault named but not cloned is not "no vault"
    env2 = dict(env, XDG_CONFIG_HOME=os.path.join(tmp, "config2"))
    write(os.path.join(tmp, "config2", "soul", "vault"), os.path.join(tmp, "not-cloned") + "\n")
    check("where: named but missing exits 3", run(env2, "where").returncode == 3)
    check("where: none named exits 1",
          run(dict(env, XDG_CONFIG_HOME=os.path.join(tmp, "config3")), "where").returncode == 1)

    # 5e — the index: one row per project, latest witness, hand-added non-Soul projects
    #      listed, restricted never
    write(os.path.join(vault, "projects", "notes", "project.md"),
          "---\nkey: notes\nlabel: private\ncontributes: [research]\n---\n")
    write(os.path.join(vault, "projects", "secret", "project.md"),
          "---\nkey: secret\nlabel: restricted\n---\n")
    write(os.path.join(vault, "projects", "secret2", "project.md"),
          "---\nkey: secret2\nlabel: \"Restricted\"\n---\n")
    write(os.path.join(vault, "projects", "nolabel", "project.md"), "---\nkey: nolabel\n---\n")
    write(os.path.join(target, "witness.md"), "# W\nID:           SOUL-7\nWHEN:         2026-10-22 / x\n")
    r = run(env, "index")
    idx = read(os.path.join(vault, "index.md"))
    check("index lists vaulted projects with their latest witness",
          "| [alpha](projects/alpha/project.md) | private | soul, tools | yes | SOUL-7 (2026-10-22) |" in idx
          and "[beta]" in idx and "[delta]" in idx, idx)
    check("index lists a hand-added project with no record",
          "| [notes](projects/notes/project.md) | private | research | no | — |" in idx, idx)
    check("index never lists a restricted or unlabelled project", "secret" not in idx
          and "nolabel" not in idx and "casey" not in idx and "4 left out" in r.stdout, r.stdout)

    # 5f — witness logs written as dated headings: the cell shows the date, never the
    #      title; whichever entry form comes last wins
    for key, text in (
            ("heady", "# W\n## 2026-10-23 — Vault | second machine\nbody\n"),
            ("heady-hyphen", "# W\n## 2026-10-24 - a hyphen\n"),
            ("id-then-heading", "ID:  SOUL-8\nWHEN:  2026-10-20 / x\n\n## 2026-10-25 — later\n"
                                "WHEN:  2026-10-01 / not an entry of its own\n"),
            ("heading-then-id", "## 2026-10-19 — earlier\n\nID:  SOUL-9\nWHEN:  2026-10-26\n"),
            ("id-only", "ID:  SOUL-10\n")):
        write(os.path.join(vault, "projects", key, "project.md"),
              "---\nkey: {}\nlabel: private\n---\n".format(key))
        write(os.path.join(vault, "projects", key, "soul", "witness.md"), text)
    r = run(env, "index")
    idx = read(os.path.join(vault, "index.md"))
    check("a dated heading shows just the date",
          "| [heady](projects/heady/project.md) | private |  | yes | 2026-10-23 |" in idx
          and "second machine" not in idx, idx)
    check("a hyphen after the date counts too", "| yes | 2026-10-24 |" in idx, idx)
    check("a heading after an ID entry wins", "id-then-heading/project.md) | private |  | yes "
          "| 2026-10-25 |" in idx and "SOUL-8" not in idx, idx)
    check("an ID entry after a heading wins", "| yes | SOUL-9 (2026-10-26) |" in idx, idx)
    check("an ID with no date shows the ID", "| yes | SOUL-10 |" in idx, idx)
    probe = subprocess.run([sys.executable, "-I", "-c",
                            "import importlib.util, sys\n"
                            "s = importlib.util.spec_from_file_location('v', sys.argv[1])\n"
                            "m = importlib.util.module_from_spec(s); s.loader.exec_module(m)\n"
                            "print(m._latest_witness(sys.argv[2]))",
                            _TOOL, os.path.join(vault, "projects", "heady", "soul", "witness.md")],
                           capture_output=True, text=True, cwd=tmp)
    check("a dated heading → (None, date)",
          probe.stdout.strip() == "(None, '2026-10-23')", probe.stdout + probe.stderr)

    # 5g — eol.py is imported only by init: the SessionStart hook (`session-start`, same load path as `check`), which
    #      must work even where eol.py does not load; init finds eol.py from elsewhere
    lone = os.path.join(tmp, "lone")
    os.makedirs(lone)
    shutil.copy(_TOOL, lone)
    r = subprocess.run([sys.executable, "-I", os.path.join(lone, "vault.py"), "check", tmp],
                       capture_output=True, text=True, env=env, cwd=tmp)
    check("vault.py check runs with no eol.py beside it", r.returncode == 0
          and "Error" not in r.stderr, r.stdout + r.stderr)
    elsewhere = os.path.join(tmp, "vault-elsewhere")
    probe = subprocess.run([sys.executable, "-I", "-c",
                            "import importlib.util, sys\n"
                            "s = importlib.util.spec_from_file_location('v', sys.argv[1])\n"
                            "m = importlib.util.module_from_spec(s); s.loader.exec_module(m)\n"
                            "m.init(sys.argv[2])",
                            _TOOL, elsewhere], capture_output=True, text=True, cwd=tmp, env=env)
    check("init loaded from elsewhere finds eol.py and writes the rule",
          probe.returncode == 0 and os.path.isfile(os.path.join(elsewhere, ".gitattributes")),
          probe.stdout + probe.stderr)

    # 5h — index.md is written with the STORED copy's line ending, so a CRLF checkout
    #      of an LF commit does not stay modified; not a git repo, or untracked → LF
    path = os.path.join(vault, "index.md")
    crlf = open(path, "rb").read().replace(b"\n", b"\r\n")
    with open(path, "wb") as fh:
        fh.write(crlf)
    run(env, "index")
    after = open(path, "rb").read()
    check("not a git repo: a CRLF index.md is rewritten LF",
          b"\r" not in after and after == crlf.replace(b"\r\n", b"\n"), repr(after[:80]))
    v2 = os.path.join(tmp, "vault-git")
    run(env, "init", v2)
    os.remove(os.path.join(v2, ".gitattributes"))  # a vault made before the rule
    p2 = os.path.join(v2, "index.md")
    run(env, "index", v2)
    git(v2, "init", "-q")
    git(v2, "-c", "core.autocrlf=false", "add", "index.md")
    git(v2, "commit", "-qm", "lf")
    lf = open(p2, "rb").read()
    with open(p2, "wb") as fh:
        fh.write(lf.replace(b"\n", b"\r\n"))  # what a Windows autocrlf checkout leaves
    run(env, "index", v2)
    check("LF committed, CRLF working copy: written LF, git sees no change",
          open(p2, "rb").read() == lf and git(v2, "status", "--porcelain", "--",
                                              "index.md").stdout == "",
          repr(open(p2, "rb").read()[:80]))
    with open(p2, "wb") as fh:
        fh.write(lf.replace(b"\n", b"\r\n"))
    git(v2, "-c", "core.autocrlf=false", "add", "index.md")
    git(v2, "commit", "-qm", "crlf")
    with open(p2, "wb") as fh:
        fh.write(lf)
    run(env, "index", v2)
    check("CRLF committed: written CRLF, git sees no change",
          open(p2, "rb").read() == lf.replace(b"\n", b"\r\n")
          and git(v2, "status", "--porcelain", "--", "index.md").stdout == "",
          repr(open(p2, "rb").read()[:80]))

    # 6 — broken link: loud in check and at session start; silent where nothing is linked
    os.rename(target, target + ".gone")
    r = run(env, "check", a)
    check("check reports a broken link", r.returncode == 1 and "BROKEN" in r.stdout, r.stdout)
    r = run(env, "session-start", stdin=json.dumps({"cwd": a}))
    out = json.loads(r.stdout or "{}")
    check("session start says it out loud", "BROKEN" in out.get("systemMessage", "")
          and "BROKEN" in out["hookSpecificOutput"]["additionalContext"], r.stdout)
    check("session-start line is short", len(r.stdout) < 2000)
    r = run(env, "link", a, "--key", "alpha", "--label", "private")
    check("broken link with no vault record refused", r.returncode == 2, r.stderr)
    os.rename(target + ".gone", target)
    r = run(env, "session-start", stdin=json.dumps({"cwd": a}))
    out = json.loads(r.stdout or "{}")
    check("linked: context line only, no banner", "systemMessage" not in out
          and "lives in the vault" in out["hookSpecificOutput"]["additionalContext"], r.stdout)
    plain = project(tmp, "plain", {"README.md": "x\n"})
    r = run(env, "session-start", stdin=json.dumps({"cwd": plain}))
    check("session start silent for a project with no link", r.stdout.strip() == "", r.stdout)

    # 7 — sidecar: the record stays tracked at the project root (a public product, SOUL-223);
    #     only the private .soul/ moves to the vault
    roots = {"witness.md": "# W\nSOUL-1\n", "ideas.md": "# I\n", "mind.md": "# M\n"}
    z = project(tmp, "zeta", roots, remote="git@example.com:me/zeta.git", commit=True)
    write(os.path.join(z, ".soul", "handoff.md"), "# Handoff\n")
    r = run(env, "link", z, "--key", "zeta", "--label", "private", "--sidecar")
    zt = os.path.join(vault, "projects", "zeta", "soul")
    check("sidecar link succeeds", r.returncode == 0, r.stderr + r.stdout)
    check("sidecar: root stores stay put, unchanged",
          all(read(os.path.join(z, n)) == t for n, t in roots.items()))
    check("sidecar: .soul is a link into the vault", os.path.islink(os.path.join(z, ".soul"))
          and os.path.realpath(os.path.join(z, ".soul")) == os.path.realpath(zt))
    check("sidecar: the vault holds handoff.md, not the record",
          os.path.isfile(os.path.join(zt, "handoff.md"))
          and read(os.path.join(zt, "handoff.md")) == "# Handoff\n"
          and not os.path.exists(os.path.join(zt, "witness.md")),
          str(os.listdir(zt) if os.path.isdir(zt) else "no " + zt))
    check("sidecar: no STILL TRACKED warning for the root record", "STILL TRACKED" not in r.stdout,
          r.stdout)
    zpm = read(os.path.join(vault, "projects", "zeta", "project.md"))
    check("sidecar: project.md records `sidecar: true` in its frontmatter",
          "\nsidecar: true\n" in zpm.split("\n---", 1)[0] + "\n", zpm)
    r = run(env, "check", z, "--json")
    st = json.loads(r.stdout or "{}")
    check("sidecar: check says linked, sidecar", r.returncode == 0 and st.get("state") == "linked"
          and st.get("sidecar") is True, r.stdout)
    r = run(env, "check", z)
    check("sidecar: no TWO COPIES, says the record stays", r.returncode == 0
          and "TWO COPIES" not in r.stdout and "stays in the project" in r.stdout, r.stdout)

    y = project(tmp, "eta", dict(roots))
    r = run(env, "link", y, "--key", "eta", "--label", "private", "--sidecar")
    check("sidecar with no .soul/: refused, nothing changed", r.returncode == 2
          and "there is none" in r.stderr and not os.path.lexists(os.path.join(y, ".soul"))
          and not os.path.exists(os.path.join(vault, "projects", "eta"))
          and all(read(os.path.join(y, n)) == t for n, t in roots.items()), r.stderr + r.stdout)

    th = project(tmp, "theta", {".soul/witness.md": "# W\n"})
    run(env, "link", th, "--key", "theta", "--label", "private")
    write(os.path.join(th, "witness.md"), "# W back\n")
    st = json.loads(run(env, "check", th, "--json").stdout or "{}")
    check("not sidecar: a root witness.md beside the link is still TWO COPIES",
          st.get("state") == "two-copies" and st.get("sidecar") is False, json.dumps(st))

    # F3 — --sidecar keeps the record at the root; a .soul/ that holds a record store is
    #      refused before anything changes (which copy is the record is the owner's call)
    io = project(tmp, "iota", {".soul/witness.md": "# W in soul\n", ".soul/handoff.md": "# H\n",
                               "ideas.md": "# I root\n"})
    r = run(env, "link", io, "--key", "iota", "--label", "private", "--sidecar")
    check("sidecar, .soul/ holds witness.md: refused, nothing changed", r.returncode == 2
          and "owner's call" in r.stderr and "witness.md" in r.stderr
          and os.path.isdir(os.path.join(io, ".soul"))
          and not os.path.islink(os.path.join(io, ".soul"))
          and read(os.path.join(io, ".soul", "witness.md")) == "# W in soul\n"
          and read(os.path.join(io, "ideas.md")) == "# I root\n"
          and not os.path.exists(os.path.join(vault, "projects", "iota")), r.stderr + r.stdout)

    # Not a sidecar: a root-layout record linked normally, then its vault copy's stores
    # go missing and a reset brings a root witness.md back — still TWO COPIES (sidecar is
    # recorded in project.md, never inferred from what the vault folder holds)
    ka = project(tmp, "kappa", {"witness.md": "# W\n", "ideas.md": "# I\n"})
    r = run(env, "link", ka, "--key", "kappa", "--label", "private")
    kt = os.path.join(vault, "projects", "kappa", "soul")
    for n in ("witness.md", "ideas.md"):
        os.remove(os.path.join(kt, n))
    write(os.path.join(ka, "witness.md"), "# W back\n")
    r = run(env, "check", ka, "--json")
    st = json.loads(r.stdout or "{}")
    check("not sidecar, vault stores gone, root witness.md back: still TWO COPIES",
          r.returncode == 1 and st.get("state") == "two-copies" and st.get("sidecar") is False,
          r.stdout + r.stderr)

    # A hand-added vault project (project.md, no soul/ yet): --sidecar adds the line
    # inside its frontmatter and keeps the rest
    lam = project(tmp, "lambda", {"witness.md": "# W\n", ".soul/handoff.md": "# H\n"})
    lpm = os.path.join(vault, "projects", "lambda", "project.md")
    write(lpm, "---\nkey: lambda\nlabel: private\nremote: \n---\n\n# lambda notes\n")
    r = run(env, "link", lam, "--key", "lambda", "--label", "private", "--sidecar")
    lt = read(lpm)
    check("sidecar into an existing project.md: `sidecar: true` added inside the frontmatter",
          r.returncode == 0 and lt.startswith("---\nkey: lambda\n")
          and "\nsidecar: true\n---\n" in lt and lt.endswith("\n# lambda notes\n"),
          r.stderr + r.stdout + lt)

    z2 = project(tmp, "zeta-clone", dict(roots), remote="https://example.com/me/zeta", commit=True)
    st = json.loads(run(env, "check", z2, "--json").stdout or "{}")
    check("sidecar clone: check is not-linked with the vault's record named",
          st.get("state") == "not-linked" and st.get("vault_has") == "zeta", json.dumps(st))
    r = run(env, "link", z2, "--key", "zeta", "--label", "private")
    check("sidecar clone: re-links without --sidecar", r.returncode == 0
          and os.path.islink(os.path.join(z2, ".soul"))
          and os.path.isfile(os.path.join(z2, ".soul", "handoff.md"))
          and os.path.isfile(os.path.join(z2, "witness.md"))
          and read(os.path.join(z2, ".soul", "handoff.md")) == "# Handoff\n"
          and read(os.path.join(z2, "witness.md")) == roots["witness.md"], r.stderr + r.stdout)
    check("sidecar clone: no STILL TRACKED warning for the root record",
          "STILL TRACKED" not in r.stdout, r.stdout)
    st = json.loads(run(env, "check", z2, "--json").stdout or "{}")
    check("sidecar clone: re-linked with no flag, check says linked, sidecar",
          st.get("state") == "linked" and st.get("sidecar") is True, json.dumps(st))

    a3 = project(tmp, "alpha-clone2", {"witness.md": "# W other\n"},
                 remote="https://example.com/me/alpha")
    r = run(env, "check", a3, "--json")
    st = json.loads(r.stdout or "{}")
    check("clone with a root witness.md, vault holds the record: TWO COPIES",
          r.returncode == 1 and st.get("state") == "two-copies", r.stdout)
    r = run(env, "link", a3, "--key", "alpha", "--label", "private")
    check("clone with a root witness.md, vault holds the record: link refused",
          r.returncode == 2 and not os.path.lexists(os.path.join(a3, ".soul")), r.stderr)

    # 8 — a fresh clone the completion gate has already written .soul/events.jsonl into:
    #     that log alone is no second record. check is not-linked; link merges the log into
    #     the vault's, checks every line arrived, and only then swaps in the link (v3.6.3).
    #     The vault itself gitignores events.jsonl, so a fresh vault clone has none.
    peek = lambda p: read(p) if os.path.isfile(p) else None
    ev = os.path.join(target, "events.jsonl")
    check("fixture: the vault's alpha record has no events.jsonl", not os.path.exists(ev))
    e1 = '{"event": "one"}\n{"event": "two"}\n'
    a4 = project(tmp, "alpha-clone4", {".soul/events.jsonl": e1, "README.md": "x\n"},
                 remote="https://example.com/me/alpha", commit=True)
    r = run(env, "check", a4, "--json")
    st = json.loads(r.stdout or "{}")
    check("gate log only in .soul/: check is not-linked with the vault's record named, exit 0",
          r.returncode == 0 and st.get("state") == "not-linked" and st.get("vault_has") == "alpha",
          r.stdout + r.stderr)
    r = run(env, "link", a4, "--key", "alpha", "--label", "private", "--dry-run")
    check("gate log only: dry run says it would merge, and changes nothing",
          r.returncode == 0 and "would merge" in r.stdout and "events.jsonl" in r.stdout
          and os.path.isdir(os.path.join(a4, ".soul"))
          and not os.path.islink(os.path.join(a4, ".soul"))
          and peek(os.path.join(a4, ".soul", "events.jsonl")) == e1 and not os.path.exists(ev),
          r.stdout + r.stderr)
    r = log4 = run(env, "link", a4, "--key", "alpha", "--label", "private")
    check("gate log only: link succeeds, .soul is now the link", r.returncode == 0
          and os.path.islink(os.path.join(a4, ".soul"))
          and os.path.realpath(os.path.join(a4, ".soul")) == os.path.realpath(target),
          r.stdout + r.stderr)
    check("gate log only, vault had none: the log is copied whole into the vault",
          os.path.isfile(ev) and peek(ev) == e1
          and peek(os.path.join(a4, ".soul", "events.jsonl")) == e1
          and "SOUL-7" in (peek(os.path.join(a4, ".soul", "witness.md")) or ""))
    a5 = project(tmp, "alpha-clone5", {".soul/events.jsonl": '{"event": "two"}\n'
                                       '{"event": "three"}\n', "README.md": "x\n"},
                 remote="https://example.com/me/alpha")
    r = run(env, "link", a5, "--key", "alpha", "--label", "private")
    check("gate log only, vault has one: only the new lines are appended, in order",
          r.returncode == 0 and os.path.islink(os.path.join(a5, ".soul"))
          and peek(ev) == e1 + '{"event": "three"}\n', r.stdout + r.stderr + repr(peek(ev)))
    a6 = project(tmp, "alpha-clone6", {"README.md": "x\n"}, remote="https://example.com/me/alpha")
    os.makedirs(os.path.join(a6, ".soul"))
    st = json.loads(run(env, "check", a6, "--json").stdout or "{}")
    r = run(env, "link", a6, "--key", "alpha", "--label", "private")
    check("an empty .soul/: not TWO COPIES, and link replaces it with the link",
          st.get("state") == "not-linked" and r.returncode == 0
          and os.path.islink(os.path.join(a6, ".soul")), json.dumps(st) + r.stdout + r.stderr)
    check("an empty .soul/: link says it was empty, not that it held the event log",
          "it was empty" in r.stdout and "event log" not in r.stdout, r.stdout)
    check("gate log only: link says the removed .soul/ held only the event log",
          "it held only the gate's event log" in log4.stdout, log4.stdout)

    # The fence stays: a .soul/ holding anything beside the log is a second record
    a7 = project(tmp, "alpha-clone7", {".soul/events.jsonl": e1, ".soul/handoff.md": "# H\n",
                                       "README.md": "x\n"}, remote="https://example.com/me/alpha")
    r = run(env, "check", a7, "--json")
    st = json.loads(r.stdout or "{}")
    check("gate log plus handoff.md: still TWO COPIES", r.returncode == 1
          and st.get("state") == "two-copies", r.stdout)
    before = peek(ev)
    r = run(env, "link", a7, "--key", "alpha", "--label", "private")
    check("gate log plus handoff.md: link refused, nothing changed or merged", r.returncode == 2
          and os.path.isdir(os.path.join(a7, ".soul"))
          and not os.path.islink(os.path.join(a7, ".soul"))
          and read(os.path.join(a7, ".soul", "handoff.md")) == "# H\n" and peek(ev) == before,
          r.stdout + r.stderr)

    # Sidecar layout: the same, with the record tracked at the root
    zev = '{"event": "z"}\n'
    z3 = project(tmp, "zeta-clone3", dict(roots, **{".soul/events.jsonl": zev}),
                 remote="https://example.com/me/zeta")
    git(z3, "add", *roots)
    git(z3, "commit", "-qm", "init")
    r = run(env, "check", z3, "--json")
    st = json.loads(r.stdout or "{}")
    check("sidecar clone with the gate log: not-linked, not TWO COPIES", r.returncode == 0
          and st.get("state") == "not-linked" and st.get("vault_has") == "zeta", r.stdout)
    r = run(env, "link", z3, "--key", "zeta", "--label", "private")
    check("sidecar clone with the gate log: re-links without --sidecar, log merged",
          r.returncode == 0 and os.path.islink(os.path.join(z3, ".soul"))
          and peek(os.path.join(zt, "events.jsonl")) == zev
          and peek(os.path.join(z3, ".soul", "handoff.md")) == "# Handoff\n"
          and read(os.path.join(z3, "witness.md")) == roots["witness.md"], r.stdout + r.stderr)
    z4 = project(tmp, "zeta-clone4", dict(roots, **{".soul/events.jsonl": zev,
                                                     ".soul/init.md": "record: git\n"}),
                 remote="https://example.com/me/zeta")
    r = run(env, "check", z4, "--json")
    st = json.loads(r.stdout or "{}")
    r2 = run(env, "link", z4, "--key", "zeta", "--label", "private")
    check("sidecar clone, .soul/ holds init.md too: TWO COPIES, link refused",
          st.get("state") == "two-copies" and r2.returncode == 2
          and not os.path.islink(os.path.join(z4, ".soul")), r.stdout + r2.stderr)

    # 9 — the index: a sidecar's witness is at the project root, not in the vault
    r = run(env, "index")
    idx = read(os.path.join(vault, "index.md"))
    check("index: a sidecar row says its witness is in the project",
          "| [zeta](projects/zeta/project.md) | private |  | yes | in the project |" in idx, idx)
    check("index: a non-sidecar row with no witness still shows —",
          "| [notes](projects/notes/project.md) | private | research | no | — |" in idx, idx)

    # 10 — sync: commits only projects/<key>/, leaves other sessions' dirty files alone,
    #      refuses while the lock is held (never breaks it), pushes when the server has
    #      not moved and otherwise stops
    #      (mining pass 3, SOUL-234: two sessions ran git in the one vault at once)
    head = lambda d, ref="HEAD": git(d, "rev-parse", ref).stdout.strip()
    bare = os.path.join(tmp, "vault-remote.git")
    git(tmp, "init", "-q", "--bare", "-b", "main", bare)
    vs = os.path.join(tmp, "vault-sync")
    run(env, "init", vs)
    write(os.path.join(vs, "projects", "other", "soul", "witness.md"), "# other\n")
    git(vs, "init", "-q", "-b", "main")
    git(vs, "add", "-A")
    git(vs, "commit", "-qm", "vault")
    git(vs, "remote", "add", "origin", bare)
    git(vs, "push", "-q", "-u", "origin", "main")
    sp = project(tmp, "syncer", {".soul/witness.md": "# W\n"})
    r = run(env, "link", sp, "--key", "syncer", "--label", "private", "--vault", vs)
    check("sync fixture: linked into a git vault", r.returncode == 0, r.stderr + r.stdout)
    other_w = os.path.join(vs, "projects", "other", "soul", "witness.md")
    write(other_w, "# other\nuncommitted, another session's\n")
    write(os.path.join(vs, "scratch.md"), "untracked, not ours\n")
    git(vs, "add", "scratch.md")  # staged by someone else: must stay staged, uncommitted
    r = run(env, "sync", sp)
    files = git(vs, "show", "--name-only", "--format=", "HEAD").stdout.split()
    check("sync commits only the project's folder (index.md is not committed)",
          r.returncode == 0 and files and all(f.startswith("projects/syncer/") for f in files)
          and git(vs, "status", "--porcelain", "--", "index.md").stdout.startswith(" M"),
          r.stdout + r.stderr + str(files) + git(vs, "status", "--porcelain").stdout)
    check("sync leaves another session's dirty and staged files alone",
          read(other_w) == "# other\nuncommitted, another session's\n"
          and git(vs, "status", "--porcelain", "--", "scratch.md").stdout.startswith("A ")
          and git(vs, "status", "--porcelain", "--", other_w).stdout.startswith(" M"),
          git(vs, "status", "--porcelain").stdout)
    check("sync pushes", head(vs) == head(bare, "main") and "pushed" in r.stdout, r.stdout)
    lock = os.path.join(vs, ".git", "soul-sync.lock")
    check("sync removes its lock when done", not os.path.exists(lock))
    r = run(env, "sync", sp)
    check("sync with nothing new: nothing to commit, exit 0", r.returncode == 0
          and "nothing to commit" in r.stdout and "up to date" in r.stdout, r.stdout + r.stderr)

    write(lock, "pid=999999 host={} key=someone started=2026-11-06T10:00:00\n".format(
        __import__("socket").gethostname()))
    write(os.path.join(sp, ".soul", "witness.md"), "# W\nSOUL-L\n")
    before = head(vs)
    r = run(env, "sync", sp)
    check("sync refuses while the lock is held: exit 4, holder and age named, stale said",
          r.returncode == 4 and "pid 999999" in r.stderr and "someone" in r.stderr
          and " s ago" in r.stderr and "looks stale" in r.stderr, r.stderr)
    check("a held lock is never broken and nothing is committed", os.path.exists(lock)
          and head(vs) == before, r.stdout + r.stderr)
    os.remove(lock)

    other_clone = os.path.join(tmp, "vault-sync-2")
    git(tmp, "clone", "-q", bare, other_clone)
    write(os.path.join(other_clone, "projects", "far", "soul", "witness.md"), "# far\n")
    git(other_clone, "add", "-A")
    git(other_clone, "commit", "-qm", "another machine")
    git(other_clone, "push", "-q")
    server = head(bare, "main")
    r = run(env, "sync", sp)
    check("the server moved: committed here, NOT PUSHED, exit 2; dirty and staged files kept",
          r.returncode == 2 and "NOT PUSHED" in r.stderr and "newer commits" in r.stderr
          and head(bare, "main") == server and "SOUL-L" in git(vs, "show",
                                                              "HEAD:projects/syncer/soul/witness.md").stdout
          and not os.path.exists(os.path.join(vs, "projects", "far"))
          and read(other_w) == "# other\nuncommitted, another session's\n"
          and git(vs, "status", "--porcelain", "--", "scratch.md").stdout.startswith("A "),
          r.stdout + r.stderr + git(vs, "status", "--porcelain").stdout)
    r = run(env, "sync", a)
    check("sync on a vault that is not a git repo: refused", r.returncode == 2
          and "not a git repo" in r.stderr, r.stderr)
    r = run(env, "sync", plain)
    check("sync with no .soul link: refused", r.returncode == 2 and "nothing to sync" in r.stderr,
          r.stderr)

    # 11 — link --also: named private paths move with the record, same relative paths,
    #      copy → compare → delete; refusals change nothing (SOUL-I081 narrow case)
    extra = {".soul/witness.md": "# W\n", "docs/plans/p1.md": "# plan\n",
             "research/a/notes.md": "notes\n", "research/b.txt": "b\n",
             "docs/private.md": "tracked, private\n", "README.md": "public\n"}
    ap = project(tmp, "public-soon", extra)
    git(ap, "add", "docs/private.md", "README.md")
    git(ap, "commit", "-qm", "init")
    for bad, why in (("../alpha", "outside the project"), (".git/config", "inside .git"),
                     ("missing.md", "no such file"), (".soul/witness.md", "part of the record")):
        r = run(env, "link", ap, "--key", "public-soon", "--label", "private", "--also", bad)
        check("--also {}: refused, nothing changed".format(bad), r.returncode == 2
              and why in r.stderr and not os.path.islink(os.path.join(ap, ".soul"))
              and not os.path.exists(os.path.join(vault, "projects", "public-soon")), r.stderr)
    r = run(env, "link", ap, "--key", "public-soon", "--label", "private", "--dry-run",
            "--also", "docs/plans", "research", "docs/private.md")
    check("--also dry run lists each path and changes nothing", r.returncode == 0
          and all("would move {} →".format(x) in r.stdout
                  for x in ("docs/plans", "research", "docs/private.md"))
          and os.path.isfile(os.path.join(ap, "docs", "plans", "p1.md"))
          and not os.path.exists(os.path.join(vault, "projects", "public-soon")), r.stdout)
    r = run(env, "link", ap, "--key", "public-soon", "--label", "private",
            "--also", "docs/plans", "research", "docs/private.md")
    pt = os.path.join(vault, "projects", "public-soon", "soul")
    check("--also moves each path into soul/ at the same relative path", r.returncode == 0
          and all(read(os.path.join(pt, rel)) == text for rel, text in extra.items()
                  if rel.startswith(("docs/", "research/"))), r.stdout + r.stderr)
    check("--also: readable through the link, originals removed, the rest untouched",
          read(os.path.join(ap, ".soul", "research", "a", "notes.md")) == "notes\n"
          and not os.path.exists(os.path.join(ap, "research"))
          and not os.path.exists(os.path.join(ap, "docs", "plans"))
          and not os.path.exists(os.path.join(ap, "docs", "private.md"))
          and read(os.path.join(ap, "README.md")) == "public\n", r.stdout)
    check("--also: a tracked path moved is named as still tracked", "STILL TRACKED" in r.stdout
          and "docs/private.md" in r.stdout, r.stdout)
    write(os.path.join(ap, "later.md"), "later\n")
    r = run(env, "link", ap, "--key", "public-soon", "--label", "private", "--also", "later.md")
    check("--also on a project already linked: moved", r.returncode == 0
          and read(os.path.join(pt, "later.md")) == "later\n"
          and not os.path.exists(os.path.join(ap, "later.md")), r.stdout + r.stderr)
    write(os.path.join(ap, "later.md"), "a second one\n")
    r = run(env, "link", ap, "--key", "public-soon", "--label", "private", "--also", "later.md")
    check("--also onto a path the vault already holds: refused, original kept",
          r.returncode == 2 and "already exists" in r.stderr
          and read(os.path.join(ap, "later.md")) == "a second one\n"
          and read(os.path.join(pt, "later.md")) == "later\n", r.stderr)

    # --also refusals added by the fresh-context review: a link on the way or inside, a
    # nested .git, an instruction file; a sidecar's root store is named as staying put
    rp = project(tmp, "also-refusals", {".soul/witness.md": "# W\n", "real/x.md": "x\n",
                                        "withlink/a.md": "a\n", "nested/.git/HEAD": "ref\n",
                                        "CLAUDE.md": "@x\n", ".claude/settings.json": "{}\n"})
    os.symlink(os.path.join(rp, "real"), os.path.join(rp, "via"))
    os.symlink(os.path.join(rp, "real", "x.md"), os.path.join(rp, "withlink", "l.md"))
    for bad, why in (("via/x.md", "reached through a link"), ("withlink", "holds a link"),
                     ("nested", "nested .git"), ("CLAUDE.md", "instruction file"),
                     (".claude", "instruction file")):
        r = run(env, "link", rp, "--key", "also-refusals", "--label", "private", "--also", bad)
        check("--also {}: refused ({}), nothing changed".format(bad, why), r.returncode == 2
              and why in r.stderr and not os.path.islink(os.path.join(rp, ".soul")), r.stderr)
    sc = project(tmp, "also-sidecar", {"witness.md": "# W\n", ".soul/handoff.md": "# H\n"})
    r = run(env, "link", sc, "--key", "also-sidecar", "--label", "private", "--sidecar",
            "--also", "witness.md")
    check("--also a root store with --sidecar: refused, says a sidecar keeps it at the root",
          r.returncode == 2 and "sidecar keeps at the project root" in r.stderr
          and "moves anyway" not in r.stderr, r.stderr)

    # An --also failure midway (a copy that fails): the record is linked and whole, the
    # other path moved, the failed one back in place; exit 5, not "nothing changed"
    mp = project(tmp, "also-midway", {".soul/witness.md": "# W\n", "a.md": "a\n", "b.md": "b\n"})
    probe = subprocess.run([sys.executable, "-I", "-c",
                            "import importlib.util, shutil, sys\n"
                            "s = importlib.util.spec_from_file_location('v', sys.argv[1])\n"
                            "m = importlib.util.module_from_spec(s); s.loader.exec_module(m)\n"
                            "real = shutil.copy2\n"
                            "def boom(a, b, **k):\n"
                            "    if a.endswith('b.md' + m.PARK): raise OSError('disk full')\n"
                            "    return real(a, b, **k)\n"
                            "shutil.copy2 = boom\n"
                            "sys.argv = ['vault.py'] + sys.argv[2:]\n"
                            "sys.exit(m.main())",
                            _TOOL, "link", mp, "--key", "also-midway", "--label", "private",
                            "--also", "a.md", "b.md"], capture_output=True, text=True, env=env, cwd=tmp)
    mt = os.path.join(vault, "projects", "also-midway")
    check("--also failing midway: exit 5, named; the record linked with project.md",
          probe.returncode == 5 and "NOT moved" in probe.stdout and "b.md" in probe.stdout
          and "disk full" in probe.stdout and os.path.islink(os.path.join(mp, ".soul"))
          and os.path.isfile(os.path.join(mt, "project.md"))
          and ".soul" in read(os.path.join(mp, ".git", "info", "exclude")).splitlines(),
          probe.stdout + probe.stderr)
    check("--also failing midway: a.md moved, b.md back in place, no copy or set-aside left",
          peek(os.path.join(mt, "soul", "a.md")) == "a\n" and not os.path.exists(os.path.join(mp, "a.md"))
          and peek(os.path.join(mp, "b.md")) == "b\n"
          and not os.path.exists(os.path.join(mt, "soul", "b.md"))
          and not os.path.exists(os.path.join(mp, "b.md.vault-moving")), probe.stdout)

    # Wok / Wfail — a file written at the original path while it moves is never
    # overwritten or removed: the set-aside original is kept beside it, exit 5, and it
    # is never reported as moved (fresh-context review 2)
    for case, fail in (("Wok", False), ("Wfail", True)):
        wp = project(tmp, "also-" + case.lower(), {".soul/witness.md": "# W\n", "plan.md": "old plan\n"})
        probe = subprocess.run([sys.executable, "-I", "-c",
                                "import importlib.util, shutil, sys\n"
                                "s = importlib.util.spec_from_file_location('v', sys.argv[1])\n"
                                "m = importlib.util.module_from_spec(s); s.loader.exec_module(m)\n"
                                "real = shutil.copy2\n"
                                "fail = sys.argv[2] == '1'\n"
                                "def write_meanwhile(a, b, **k):\n"
                                "    out = real(a, b, **k)\n"
                                "    if a.endswith('plan.md.vault-moving'):\n"
                                "        open(a[:-len('.vault-moving')], 'w').write('new plan\\n')\n"
                                "        if fail: raise OSError('disk full')\n"
                                "    return out\n"
                                "shutil.copy2 = write_meanwhile\n"
                                "sys.argv = ['vault.py'] + sys.argv[3:]\n"
                                "sys.exit(m.main())",
                                _TOOL, "1" if fail else "0", "link", wp, "--key", "also-" + case.lower(),
                                "--label", "private", "--also", "plan.md"],
                               capture_output=True, text=True, env=env, cwd=tmp)
        check("{}: exit 5, plan.md reported NOT moved, never 'moved plan.md'".format(case),
              probe.returncode == 5 and "NOT moved" in probe.stdout
              and "moved plan.md" not in probe.stdout, probe.stdout + probe.stderr)
        check("{}: the new plan.md kept; the original set aside, not lost".format(case),
              peek(os.path.join(wp, "plan.md")) == "new plan\n"
              and peek(os.path.join(wp, "plan.md.vault-moving")) == "old plan\n",
              probe.stdout + str(os.listdir(wp)))

    # G — an --also path that cannot be read is refused before anything changes (it
    #     once failed after the record had moved, with no project.md and no exclude)
    if os.geteuid() != 0:
        gp = project(tmp, "unreadable", {".soul/witness.md": "# W\n", "research/ok.md": "k\n",
                                         "research/locked.md": "locked\n"})
        os.chmod(os.path.join(gp, "research", "locked.md"), 0)
        r = run(env, "link", gp, "--key", "unreadable", "--label", "private", "--also", "research")
        os.chmod(os.path.join(gp, "research", "locked.md"), 0o644)
        check("G: an unreadable --also file: refused, nothing changed", r.returncode == 2
              and not os.path.islink(os.path.join(gp, ".soul"))
              and not os.path.exists(os.path.join(vault, "projects", "unreadable"))
              and read(os.path.join(gp, "research", "locked.md")) == "locked\n", r.stdout + r.stderr)

    sync_cases(tmp, env)

    shutil.rmtree(tmp, ignore_errors=True)
    print("\n{} failure(s)".format(len(FAILS)) if FAILS else "\nALL PASS")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
