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
    r = run(env, "link", a4, "--key", "alpha", "--label", "private")
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

    shutil.rmtree(tmp, ignore_errors=True)
    print("\n{} failure(s)".format(len(FAILS)) if FAILS else "\nALL PASS")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
