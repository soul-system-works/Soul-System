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
import shutil
import subprocess
import sys
import tempfile

_TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vault.py")
_GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
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


def main():
    tmp = tempfile.mkdtemp(prefix="soul-vault-test-")
    env = dict(_GIT_ENV, XDG_CONFIG_HOME=os.path.join(tmp, "config"), SOUL_VAULT_FORCE_WSL="0")
    vault = os.path.join(tmp, "vault")

    # 1 — init scaffolds, never overwrites, registers one vault per machine
    r = run(env, "init", vault, "--register")
    check("init scaffolds", r.returncode == 0 and all(os.path.exists(os.path.join(vault, f))
          for f in ("vault.md", ".gitignore", "index.md", "projects")), r.stderr)
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
    write(os.path.join(target, "witness.md"), "# W\nID:           SOUL-7\nWHEN:         2026-10-22 / x\n")
    r = run(env, "index")
    idx = read(os.path.join(vault, "index.md"))
    check("index lists vaulted projects with their latest witness",
          "| [alpha](projects/alpha/project.md) | private | soul, tools | yes | SOUL-7 (2026-10-22) |" in idx
          and "[beta]" in idx and "[delta]" in idx, idx)
    check("index lists a hand-added project with no record",
          "| [notes](projects/notes/project.md) | private | research | no | — |" in idx, idx)
    check("index never lists a restricted project", "secret" not in idx and "1 restricted left out"
          in r.stdout, r.stdout)

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

    shutil.rmtree(tmp, ignore_errors=True)
    print("\n{} failure(s)".format(len(FAILS)) if FAILS else "\nALL PASS")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
