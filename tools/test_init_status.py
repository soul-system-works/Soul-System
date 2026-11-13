"""Behaviour test for tools/init-status.py (/soul-init's checklist and remembered answers).

FENCE: a recorded answer is not asked again unless the files show it no longer holds —
names listed but .soul/private-names.txt gone, a stage recorded but no **Stage:** line,
or `status --ask KEY` forces it. A repair is never
hidden by one — `hand-hooks: yes` recorded on one machine reads `repair` where the
hooks are missing, and `record: local` reads `repair` while the record is tracked.
`status` never writes; `record` keeps every line it does not own. Each run controls
PATH (git only, plus a fake `gitleaks` when the scan should be offered), sets
SOUL_INIT_NO_GH=1 so `gh` is never called (no network), and points HOME and
XDG_CONFIG_HOME at temp folders so this machine's real vault file is never read and
no `~/soul-vault` is ever seen or made. The WSL drive rule is checked in-process with a
made-up drive letter, never against a real /mnt/<drive>/.

Run: python3 tools/test_init_status.py  (exit 0 = PASS)
"""

import datetime
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOL = os.path.join(_HERE, "init-status.py")
_ROOT = os.path.dirname(_HERE)
_GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
                GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
                GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
TODAY = datetime.date.today().isoformat()
IMPORT = "@{}/operations/CLAUDE.md\n".format(_ROOT)
RULES = "* text=auto eol=lf\n"
HOOK = ("#!/bin/sh\n# Soul System secret check ({0}), installed by /soul-init "
        "(operations/secret-guard.md).\nexit 0\n")
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else "  — " + str(detail)))
    if not ok:
        FAILS.append(name)


def git(cwd, *args):
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True,
                          env=_GIT_ENV)


def write(path, text, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f:
        f.write(text)


def read(path):
    return open(path, encoding="utf-8").read()


def run(env, *args):
    return subprocess.run([sys.executable, _TOOL, *args], capture_output=True, text=True,
                          env=env)


def status(env, project):
    r = run(env, "status", project, "--json")
    try:
        st = json.loads(r.stdout)
    except ValueError:
        return {"items": [], "rounds": [], "fresh": None, "_err": r.stderr}, {}
    return st, {i["key"]: i for i in st["items"]}


def actions(by):
    return {k: i["action"] for k, i in by.items()}


def repo(root, name, files, commit=True):
    p = os.path.join(root, name)
    for rel, text in files.items():
        write(os.path.join(p, rel), text)
    git(p, "init", "-q")
    if commit:
        git(p, "add", "-A")
        git(p, "commit", "-qm", "init")
    return p


def install_hooks(p, hooks=("pre-commit", "commit-msg", "pre-push")):
    for h in hooks:
        path = os.path.join(p, ".git", "hooks", h)
        write(path, HOOK.format(h))
        os.chmod(path, 0o755)


def set_up(root, name):
    """A finished project: import, tracked .soul/ stores, ignored runtime state, a stage,
    a private-name list, Soul hooks, the line-ending rule, history scanned at HEAD."""
    p = repo(root, name, {
        "CLAUDE.md": IMPORT + "\n**Stage: prototype** (owner)\n",
        ".soul/witness.md": "# Witness\n", ".soul/ideas.md": "# Ideas\n",
        ".gitignore": ".soul/handoff.md\n.soul/events.jsonl\n.soul/private-names.txt\n",
        ".gitattributes": RULES, "README.md": "x\n"})
    write(os.path.join(p, ".soul", "private-names.txt"), "Acme\n")
    install_hooks(p)
    head = git(p, "rev-parse", "--short=12", "HEAD").stdout.strip()
    write(os.path.join(p, ".soul", "init.md"),
          "# header\nhistory-scan:  clean {}   2026-10-23\n"
          "upkeep:        on           2026-11-12\n".format(head))
    return p


def main():
    tmp = tempfile.mkdtemp(prefix="soul-init-status-test-")
    bins = {}
    for kind in ("plain", "leaks"):
        b = os.path.join(tmp, "bin-" + kind)
        os.makedirs(b)
        os.symlink(shutil.which("git"), os.path.join(b, "git"))
        if kind == "leaks":
            write(os.path.join(b, "gitleaks"), "#!/bin/sh\nexit 0\n")
            os.chmod(os.path.join(b, "gitleaks"), 0o755)
        bins[kind] = b
    # HOME too: the plan's default vault is ~/soul-vault, and git runs see the same HOME.
    os.makedirs(os.path.join(tmp, "home-base"))
    _GIT_ENV.update(HOME=os.path.join(tmp, "home-base"),
                    XDG_CONFIG_HOME=os.path.join(tmp, "config"))
    base = dict(_GIT_ENV, XDG_CONFIG_HOME=os.path.join(tmp, "config"), SOUL_INIT_NO_GH="1")
    env = dict(base, PATH=bins["plain"])      # no gitleaks, no gh
    envl = dict(base, PATH=bins["leaks"])     # a gitleaks on PATH (never run by status)

    # 1 — fresh repo: one commit, no CLAUDE.md
    p1 = repo(tmp, "fresh", {"README.md": "x\n"})
    st, by = status(env, p1)
    check("fresh: fresh is true", st["fresh"] is True, st)
    check("fresh: import is a repair, not a question", by["import"]["action"] == "repair",
          by.get("import"))
    # v3.13.0: the main set is plan lines, not a round; their pickers stay for Modify setup
    check("fresh: record, stage, names, upkeep are plan lines, not a round",
          st["rounds"] == []
          and [ln["key"] for ln in (st.get("plan") or {}).get("lines", [])][:4]
          == ["record", "stage", "names", "upkeep"]
          and all(by[k]["question"]["group"] == "main"
                  for k in ("record", "stage", "names", "upkeep")),
          (st["rounds"], st.get("plan")))
    check("fresh: no layout item", "layout" not in by)
    check("fresh, no gitleaks: extras = hand-hooks + line-endings",
          by["extras"]["members"] == ["hand-hooks", "line-endings"]
          and by["history-scan"]["action"] == "none"
          and "gitleaks" in by["history-scan"]["detail"], by.get("extras"))
    check("fresh: extras members carry no question of their own",
          all(by[k]["question"] is None and by[k]["group"] == "extras"
              for k in ("hand-hooks", "line-endings")))
    check("fresh: the extras picker is a change round of the plan, not a round",
          (st.get("plan") or {}).get("change_rounds", [[]])[-1] == ["extras"]
          and ["extras"] not in st["rounds"], (st["rounds"], st.get("plan")))
    q = by["extras"]["question"]
    check("extras: only the line-endings fix is recommended (hooks, scan are offers)",
          q["recommended"] is not None
          and q["options"][q["recommended"]]["key"] == "line-endings", q)
    q = by["record"]["question"]
    check("record question: fixed wording, three options with no vault, nothing recommended "
          "while visibility is unknown",
          q["text"] == "Where should Soul's log of this project's decisions and ideas live?"
          and [(o["value"], o["label"], o["description"]) for o in q["options"]] == [
              ("git", "In this repo's git",
               "Travels with the code and is backed up with it. Whoever can read the repo "
               "can read the log: if the repo is public, or becomes public, so is the log."),
              ("vault", "In a private vault",
               "A separate private repo of yours that can hold the logs of all your "
               "projects. This project keeps only a link; nothing of the log is committed "
               "here. Adds 2 steps: which vault, then a yes to the move."),
              ("local", "Only on this machine",
               "In this folder, ignored by git. Never published, but one copy and no "
               "backup.")]
          and q["recommended"] is None, q)
    check("record detail: visibility unknown", "public is unknown" in by["record"]["detail"],
          by["record"]["detail"])
    st, by = status(envl, p1)
    check("fresh, gitleaks present: history-scan joins extras",
          by["extras"]["members"] == ["hand-hooks", "history-scan", "line-endings"],
          by.get("extras"))
    check("status never writes", not os.path.exists(os.path.join(p1, ".soul")))

    # 2 — set-up project: everything none
    p2 = set_up(tmp, "setup")
    st, by = status(envl, p2)
    check("set-up: every item none", all(a == "none" for a in actions(by).values())
          and st["rounds"] == [], actions(by))
    check("set-up: values found", by["record"]["value"] == "git"
          and by["stage"]["value"] == "prototype" and by["names"]["value"] == "listed"
          and by["hand-hooks"]["value"] == "yes" and by["line-endings"]["value"] == "ok", by)
    r = run(envl, "status", p2)
    check("set-up: text ends 'All set — nothing to do.'",
          r.stdout.rstrip().endswith("All set — nothing to do."), r.stdout)

    # 3 — a new commit: only history-scan asks; a commit of init.md alone does not
    git(p2, "add", ".soul/init.md")
    git(p2, "commit", "-qm", "answers")
    st, by = status(envl, p2)
    check("committing only .soul/init.md: no new scan asked",
          by["history-scan"]["action"] == "none", by["history-scan"])
    with open(os.path.join(p2, "CLAUDE.md"), "a") as f:  # init's own edits, committed later
        f.write("\n**Stage: prototype**\n")
    with open(os.path.join(p2, ".gitignore"), "a") as f:
        f.write(".soul/private-names.txt\n")
    git(p2, "add", "CLAUDE.md", ".gitignore")
    git(p2, "commit", "-qm", "init's edits")
    st, by = status(envl, p2)
    check("committing only init's own files (CLAUDE.md, .gitignore): no new scan asked",
          by["history-scan"]["action"] == "none", by["history-scan"])
    write(os.path.join(p2, "src.py"), "x = 1\n")
    git(p2, "add", "src.py")
    git(p2, "commit", "-qm", "work")
    st, by = status(envl, p2)
    asks = sorted(k for k, a in actions(by).items() if a != "none")
    check("after a new commit: nothing asks — the scan is offered once (v3.6.1)",
          asks == [] and st["rounds"] == [], (asks, st["rounds"]))
    check("history-scan detail names the new commit and how to rescan",
          "1 commit(s) since" in by["history-scan"]["detail"]
          and "revisit history-scan" in by["history-scan"]["detail"],
          by["history-scan"]["detail"])

    # 4 — recorded hand-hooks yes, hooks gone (a new machine): repair
    p4 = set_up(tmp, "newmachine")
    write(os.path.join(p4, ".soul", "init.md"), "hand-hooks:    yes          2026-10-23\n",
          mode="a")
    for h in ("pre-commit", "commit-msg", "pre-push"):
        os.remove(os.path.join(p4, ".git", "hooks", h))
    st, by = status(env, p4)
    check("recorded yes, hooks missing: repair", by["hand-hooks"]["action"] == "repair"
          and by["hand-hooks"]["source"] == "recorded", by["hand-hooks"])
    write(os.path.join(p4, ".git", "hooks", "pre-push"), "#!/bin/sh\ngit lfs pre-push \"$@\"\n")
    st, by = status(env, p4)
    hh = by["hand-hooks"]
    check("a pre-push held by git-lfs is named, the free slots repaired",
          hh["action"] == "repair" and "git-lfs" in hh["detail"]
          and "pre-commit, commit-msg" in hh["detail"], hh)

    # 5 — recorded declines are not asked again
    p5 = repo(tmp, "declined", {"CLAUDE.md": IMPORT, ".soul/witness.md": "# W\n",
                                ".gitignore": ".soul/handoff.md\n", "a.txt": "x\n"})
    write(os.path.join(p5, ".soul", "init.md"),
          "names:         none         2026-10-23\nstage:         not-now      2026-10-23\n"
          "line-endings:  no           2026-10-23\nhistory-scan:  declined     2026-10-23\n")
    st, by = status(envl, p5)
    check("recorded names/stage/line-endings/history-scan: none, from the record",
          all(by[k]["action"] == "none" and by[k]["source"] == "recorded"
              for k in ("names", "stage", "line-endings", "history-scan")),
          {k: by[k] for k in ("names", "stage", "line-endings", "history-scan")})
    check("recorded: extras holds only hand-hooks", by["extras"]["members"] == ["hand-hooks"],
          by.get("extras"))

    # 6 — record / revisit
    p6 = os.path.join(tmp, "answers")
    os.makedirs(p6)
    write(os.path.join(p6, ".soul", "init.md"),
          "# kept comment\ncustom-key:    some value   2026-01-01\n")
    r1 = run(env, "record", p6, "record", "git")
    r2 = run(env, "record", p6, "record", "local")
    r3 = run(env, "record", p6, "history-scan", "clean", "abc123def456")
    run(env, "record", p6, "names", "none")
    text = read(os.path.join(p6, ".soul", "init.md"))
    lines = text.splitlines()
    check("record writes a padded, dated line", r1.returncode == 0
          and "record:        local        " + TODAY in lines, text)
    check("record replaces, never duplicates", r2.returncode == 0
          and sum(ln.startswith("record:") for ln in lines) == 1, text)
    check("record keeps unknown keys and comments", "# kept comment" in lines
          and "custom-key:    some value   2026-01-01" in lines, text)
    check("a value with a space round-trips", r3.returncode == 0
          and "history-scan:  clean abc123def456 " + TODAY in lines, text)
    r = run(env, "record", p6, "bogus", "x")
    check("unknown key: exit 2, nothing written", r.returncode == 2
          and read(os.path.join(p6, ".soul", "init.md")) == text, r.stderr)
    r = run(env, "revisit", p6, "names")
    after = read(os.path.join(p6, ".soul", "init.md")).splitlines()
    check("revisit names removes that line only", r.returncode == 0 and "removed: names:" in r.stdout
          and not any(ln.startswith("names:") for ln in after)
          and any(ln.startswith("record:") for ln in after), after)
    r = run(env, "revisit", p6)
    after = read(os.path.join(p6, ".soul", "init.md")).splitlines()
    check("revisit with no key removes every answer, keeps comments", r.returncode == 0
          and after == ["# kept comment"], after)
    p6b = os.path.join(tmp, "answers-new")
    os.makedirs(p6b)
    run(env, "record", p6b, "stage", "not-now")
    check("first record creates the file with its header",
          read(os.path.join(p6b, ".soul", "init.md")).startswith("# /soul-init's remembered"))

    # 7 — an old project, no init.md: values inferred
    p7 = repo(tmp, "old", {"CLAUDE.md": IMPORT + "**Stage: released**\n",
                           "witness.md": "# W\n", "ideas.md": "# I\n", ".gitignore": ".soul/\n",
                           ".gitattributes": RULES})
    write(os.path.join(p7, ".soul", "private-names.txt"), "Acme\n")
    install_hooks(p7)
    st, by = status(env, p7)
    check("old project: inferred, not recorded",
          all(by[k]["source"] == "inferred" and by[k]["action"] == "none"
              for k in ("import", "record", "names", "hand-hooks", "stage", "line-endings"))
          and by["record"]["value"] == "git" and by["stage"]["value"] == "released",
          {k: (by[k]["source"], by[k]["value"]) for k in by})
    check("old project: not fresh, layout scanned", st["fresh"] is False
          and by["layout"]["action"] == "none", by.get("layout"))
    check("old project: status wrote no init.md", not os.path.exists(
          os.path.join(p7, ".soul", "init.md")))

    # 8 — .soul links into a vault-like folder: record is vault; record writes through
    vt = os.path.join(tmp, "vault", "projects", "linked", "soul")
    write(os.path.join(tmp, "vault", "vault.md"), "# vault\n")
    write(os.path.join(vt, "witness.md"), "# W\n")
    p8 = repo(tmp, "linked", {"CLAUDE.md": IMPORT})
    os.symlink(vt, os.path.join(p8, ".soul"))
    st, by = status(env, p8)
    check(".soul link: record inferred vault", by["record"]["value"] == "vault"
          and by["record"]["source"] == "inferred", by["record"])
    check(".soul link: vault-link in play and fine", by.get("vault-link", {}).get("action") == "none"
          and by["vault-link"]["value"] == "linked", by.get("vault-link"))
    r = run(env, "record", p8, "names", "none")
    check("record writes through the link", r.returncode == 0
          and os.path.islink(os.path.join(p8, ".soul"))
          and "names:" in read(os.path.join(vt, "init.md")), r.stderr)
    # 8a — a sidecar link (vault.py link --sidecar): only .soul/ is in the vault, the record
    #      stays tracked at the root, so record is read from the root stores: git, not vault
    psc = repo(tmp, "sidecar", {"CLAUDE.md": IMPORT, "witness.md": "# W\n", "ideas.md": "# I\n"})
    write(os.path.join(psc, ".soul", "handoff.md"), "# H\n")
    r = subprocess.run([sys.executable, os.path.join(_HERE, "vault.py"), "link", psc, "--key",
                        "sidecar", "--label", "private", "--sidecar", "--vault",
                        os.path.join(tmp, "vault")], capture_output=True, text=True, env=env)
    st, by = status(env, psc)
    check("sidecar link: record inferred git from the tracked root stores",
          r.returncode == 0 and os.path.islink(os.path.join(psc, ".soul"))
          and by["record"]["value"] == "git" and by["record"]["source"] == "inferred",
          (r.stderr, by.get("record")))
    check("sidecar link: vault-link still linked", by.get("vault-link", {}).get("value")
          == "linked", by.get("vault-link"))

    p8b = repo(tmp, "brokenlink", {"README.md": "x\n"})
    os.symlink(os.path.join(tmp, "nowhere"), os.path.join(p8b, ".soul"))
    r = run(env, "record", p8b, "names", "none")
    check("a broken .soul link: record refuses, exit 2", r.returncode == 2
          and not os.path.exists(os.path.join(tmp, "nowhere")), r.stderr)
    st, by = status(env, p8b)
    check("a broken .soul link, no vault registered: vault-link stop",
          by.get("vault-link", {}).get("action") == "stop", by.get("vault-link"))

    # 9 — CLAUDE.md without the import: ask, alone and first; recorded leave → none
    p9 = repo(tmp, "noimport", {"CLAUDE.md": "# My project\n"})
    st, by = status(env, p9)
    check("CLAUDE.md without import: ask, first round alone",
          by["import"]["action"] == "ask" and st["rounds"][0] == ["import"]
          and by["import"]["question"]["group"] == "single", st["rounds"])
    run(env, "record", p9, "import", "leave")
    st, by = status(env, p9)
    check("recorded leave: import none", by["import"]["action"] == "none"
          and by["import"]["source"] == "recorded", by["import"])

    # 10 — a Mind nothing imports: repair; imported relative to the file: omitted
    p10 = repo(tmp, "mind", {"CLAUDE.md": IMPORT, ".soul/witness.md": "# W\n",
                             ".soul/mind.md": "# Mind\n"})
    st, by = status(env, p10)
    check("unimported mind: repair naming @.soul/mind.md", by.get("mind", {}).get("action")
          == "repair" and "@.soul/mind.md" in by["mind"]["detail"], by.get("mind"))
    write(os.path.join(p10, "CLAUDE.md"), IMPORT + "@.soul/mind.md\n")
    st, by = status(env, p10)
    check("imported mind: item omitted", "mind" not in by, by.get("mind"))
    p10b = repo(tmp, "mind2", {".claude/CLAUDE.md": IMPORT, "mind.md": "# Mind\n"})
    st, by = status(env, p10b)
    check("import in .claude/: the Mind line is relative to it",
          "@../mind.md" in by.get("mind", {}).get("detail", ""), by.get("mind"))

    # 11 — line endings: rule committed, CRLF working copy only → repair
    p11 = repo(tmp, "eol", {".gitattributes": RULES, "a.txt": "one\ntwo\n"})
    write(os.path.join(p11, "a.txt"), b"one\r\ntwo\r\n", mode="wb")
    st, by = status(env, p11)
    check("rule present, CRLF working copy: repair with eol.py fix",
          by["line-endings"]["action"] == "repair" and "eol.py fix" in by["line-endings"]["detail"],
          by["line-endings"])

    # 12 — an existing store outside root/.soul: ask with the path in the question
    p12 = repo(tmp, "docsstore", {"CLAUDE.md": IMPORT, "docs/ideas.md": "# I\n"})
    st, by = status(env, p12)
    es = by.get("existing-store", {})
    check("docs/ideas.md: existing-store asks, path in the wording",
          es.get("action") == "ask"
          and es["question"]["text"] == "docs/ideas.md looks like this project's record. Use it?",
          es)

    # 13 — a vault holds this project's record and nothing links: re-link offered first
    envv = dict(env, XDG_CONFIG_HOME=os.path.join(tmp, "config-v"))
    vroot = os.path.join(tmp, "vault2")
    write(os.path.join(vroot, "vault.md"), "# vault\n")
    write(os.path.join(vroot, "projects", "clone", "soul", "witness.md"), "# W\n")
    write(os.path.join(tmp, "config-v", "soul", "vault"), vroot + "\n")
    p13 = repo(tmp, "clone", {"README.md": "x\n"})
    st, by = status(envv, p13)
    check("vault holds it, nothing links: vault-link asks in the first round",
          by.get("vault-link", {}).get("action") == "ask" and st["rounds"][0] == ["vault-link"],
          (by.get("vault-link"), st["rounds"]))
    check("a vault named: the record question offers it",
          "In a private vault" in [o["label"] for o in by["record"]["question"]["options"]],
          by["record"]["question"])

    # 14 — the public wording (rendered directly: status itself never calls gh here)
    spec = importlib.util.spec_from_file_location("init_status", _TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    q = mod.render_question("record", public="yes", vault=None)
    qn = mod.render_question("record", public="no", vault=None)
    check("public repo: the git option's one text warns, nothing recommended; a private "
          "repo recommends git",
          q["options"][0]["description"] == qn["options"][0]["description"]
          and "if the repo is public, or becomes public, so is the log"
          in q["options"][0]["description"]
          and q["recommended"] is None and qn["recommended"] == 0, (q, qn))
    q = mod.render_question("names", public="yes")
    check("public repo: names question says so",
          q["text"].endswith(" This repo is public — a name committed here is public."), q)
    check("public repo: names recommends nothing", q["recommended"] is None, q)

    # 15 — record never makes two copies: the vault holds it, nothing links → refuse
    r = run(envv, "record", p13, "names", "none")
    check("vault holds the record, nothing links: record refuses, exit 2, no .soul",
          r.returncode == 2 and "link the vault record first" in r.stderr
          and not os.path.lexists(os.path.join(p13, ".soul")), (r.returncode, r.stderr))

    # 16 — a dead contract import is a repair; ~ and relative imports resolve
    p16 = repo(tmp, "deadimport", {
        "CLAUDE.md": "@/nonexistent/plugins/cache/m/soul/3.4.0/operations/CLAUDE.md\n"})
    st, by = status(env, p16)
    check("dead import: repair naming the path", by["import"]["action"] == "repair"
          and "the import points at /nonexistent/plugins/cache/m/soul/3.4.0/operations/"
              "CLAUDE.md, which does not exist" in by["import"]["detail"], by["import"])
    home = os.path.join(tmp, "home")
    write(os.path.join(home, "soulroot", "operations", "CLAUDE.md"), "# contract\n")
    p16b = repo(tmp, "tildeimport", {"CLAUDE.md": "@~/soulroot/operations/CLAUDE.md\n"})
    st, by = status(dict(env, HOME=home), p16b)
    check("~ import that resolves: none", by["import"]["action"] == "none", by["import"])

    # 17 — the stage is read from every instruction file; a **Phase:** block is named
    p17 = repo(tmp, "stagedot", {".claude/CLAUDE.md": IMPORT,
                                 "CLAUDE.md": "**Stage: prototype** (owner)\n"})
    st, by = status(env, p17)
    check("import in .claude/, stage in root CLAUDE.md: found",
          by["stage"]["action"] == "none" and by["stage"]["value"] == "prototype", by["stage"])
    p17b = repo(tmp, "stagecodex", {"AGENTS.md": "<!-- soul -->\n\n**Stage: pre-release**\n"})
    st, by = status(env, p17b)
    check("stage in AGENTS.md: found", by["stage"]["action"] == "none"
          and by["stage"]["value"] == "pre-release", by["stage"])
    p17c = repo(tmp, "phase", {"CLAUDE.md": IMPORT + "\n**Phase: beta — no compat**\n"})
    st, by = status(env, p17c)
    check("a hand-written **Phase:** line: stage asks and says so",
          by["stage"]["action"] == "ask" and "a hand-written **Phase:** block exists — show "
          "it before asking" in by["stage"]["detail"], by["stage"])

    # 18 — extras with one member is a yes/no question (the scan, asked back by --ask)
    r = run(envl, "status", p2, "--json", "--ask", "history-scan")
    st = json.loads(r.stdout)
    by = {i["key"]: i for i in st["items"]}
    q = by["extras"]["question"]
    check("one extras member: single-choice yes/no, members kept",
          q["text"].startswith("Set this up? Scan git history for leaked secrets now (")
          and [o["value"] for o in q["options"]] == ["yes", "no"]
          and q["options"][0]["description"]
          == mod.QUESTIONS["extras"]["members"]["history-scan"]["description"]
          and q["options"][1]["description"] == "not asked again; /soul-init revisit to change"
          and q["multi"] is False and q["recommended"] is None
          and by["extras"]["members"] == ["history-scan"], q)

    # 19 — visibility is a fact, never a question (v3.13.0, SOUL-I092): unknown stays
    #      unknown and is not asked; a recorded answer is still read; --ask public is
    #      ignored with the usual warning
    st, by = status(env, p1)
    pub = by["public"]
    check("unknown visibility: public is not asked, has no question, and is in no round",
          pub["action"] == "none" and pub["value"] is None and pub["question"] is None
          and "public" not in sum(st["rounds"], [])
          and "public" not in mod.QUESTIONS and "public" not in mod.FORCEABLE,
          (pub, st["rounds"]))
    p19 = repo(tmp, "pubrec", {"README.md": "x\n"})
    r19 = run(env, "record", p19, "public", "no")
    st, by = status(env, p19)
    check("recorded public: still accepted, none, from the record, not asked",
          r19.returncode == 0 and by["public"]["action"] == "none"
          and by["public"]["source"] == "recorded" and by["public"]["value"] == "no"
          and ["public"] not in st["rounds"], by["public"])
    r = run(env, "status", p19, "--ask", "public")
    check("--ask public: ignored with the warning", r.returncode == 0
          and "--ask ignores public" in r.stderr, r.stderr)
    r = run(env, "revisit", p19, "public")
    check("revisit public forgets it", r.returncode == 0 and "removed: public:" in r.stdout,
          r.stdout)

    # 20 — a recorded record answer never hides the real state
    p20 = repo(tmp, "reclocal", {"CLAUDE.md": IMPORT, ".soul/witness.md": "# W\n"})
    write(os.path.join(p20, ".soul", "init.md"), "record:        local        2026-10-26\n")
    st, by = status(env, p20)
    check("recorded local, record tracked: repair (untrack)",
          by["record"]["action"] == "repair" and "git rm --cached" in by["record"]["detail"],
          by["record"])
    p20b = repo(tmp, "recgit", {"CLAUDE.md": IMPORT, "README.md": "x\n"})
    write(os.path.join(p20b, ".soul", "witness.md"), "# W\n")
    write(os.path.join(p20b, ".soul", "init.md"), "record:        git          2026-10-26\n")
    st, by = status(env, p20b)
    check("recorded git, record untracked and not ignored: repair (commit it)",
          by["record"]["action"] == "repair"
          and "recorded git, but the record is not committed" in by["record"]["detail"],
          by["record"])
    write(os.path.join(p20b, ".soul", "init.md"), "record:        local        2026-10-26\n")
    st, by = status(env, p20b)
    check("recorded local, record neither tracked nor ignored: repair naming it",
          by["record"]["action"] == "repair" and "one `git add -A`" in by["record"]["detail"],
          by["record"])
    write(os.path.join(p20b, ".gitignore"), ".soul/\n")
    st, by = status(env, p20b)
    check("recorded local, record ignored: agree, none", by["record"]["action"] == "none"
          and by["record"]["source"] == "recorded", by["record"])
    write(os.path.join(p20b, ".soul", "init.md"), "record:        git          2026-10-26\n")
    st, by = status(env, p20b)
    check("recorded git, record ignored: repair", by["record"]["action"] == "repair",
          by["record"])

    # 21 — an existing store outside git's index, or outside git
    p21 = repo(tmp, "untracked-store", {"CLAUDE.md": IMPORT})
    write(os.path.join(p21, "docs", "ideas.md"), "# I\n")
    write(os.path.join(p21, "node_modules", "x", "witness.md"), "# no\n")
    st, by = status(env, p21)
    check("untracked docs/ideas.md: existing-store asks",
          by.get("existing-store", {}).get("action") == "ask"
          and by["existing-store"]["detail"].endswith(": docs/ideas.md."),
          by.get("existing-store"))
    p21b = os.path.join(tmp, "nogit-store")
    write(os.path.join(p21b, "CLAUDE.md"), IMPORT)
    write(os.path.join(p21b, "docs", "ideas.md"), "# I\n")
    st, by = status(env, p21b)
    check("not a git repo, docs/ideas.md: existing-store asks",
          by.get("existing-store", {}).get("action") == "ask", by.get("existing-store"))

    # 22 — a broken .soul link with no usable vault stops; with the vault holding it, repair
    envm = dict(env, XDG_CONFIG_HOME=os.path.join(tmp, "config-m"))
    write(os.path.join(tmp, "config-m", "soul", "vault"), os.path.join(tmp, "no-vault") + "\n")
    st, by = status(envm, p8b)
    check("broken link, registered vault missing: stop",
          by.get("vault-link", {}).get("action") == "stop"
          and "which is missing — clone the vault there" in by["vault-link"]["detail"],
          by.get("vault-link"))
    write(os.path.join(vroot, "projects", "blink", "soul", "witness.md"), "# W\n")
    p22 = repo(tmp, "blink", {"README.md": "x\n"})
    os.symlink(os.path.join(tmp, "old-vault", "projects", "blink", "soul"),
               os.path.join(p22, ".soul"))
    st, by = status(envv, p22)
    check("broken link, vault present and holding the key: repair",
          by.get("vault-link", {}).get("action") == "repair", by.get("vault-link"))

    # 23 — status --ask forces a question back; revisit says how
    r = run(envl, "status", p2, "--json", "--ask", "record", "--ask", "names")
    try:
        st = json.loads(r.stdout)
        by = {i["key"]: i for i in st["items"]}
    except ValueError:
        st, by = {"rounds": []}, {}
    check("status --ask record --ask names: both asked though inferred",
          by.get("record", {}).get("action") == "ask" and by["record"]["question"]
          and by.get("names", {}).get("action") == "ask"
          and any("record" in rnd and "names" in rnd for rnd in st["rounds"]),
          (r.stderr, st.get("rounds")))
    r = run(envl, "status", p2, "--ask", "mind")
    check("status --ask with a key that cannot be forced: warned, not fatal",
          r.returncode == 0 and "--ask ignores mind" in r.stderr, r.stderr)
    r = run(env, "revisit", p2)
    check("revisit names the --ask route",
          "inferred answers stay; run status --ask <key> to be asked anyway" in r.stdout,
          r.stdout)

    # 24 — a Soul hook whose guard path is gone: repair
    p24 = repo(tmp, "deadhook", {"CLAUDE.md": IMPORT, ".soul/witness.md": "# W\n"})
    for h in ("pre-commit", "commit-msg", "pre-push"):
        path = os.path.join(p24, ".git", "hooks", h)
        write(path, HOOK.format(h).replace("exit 0\n",
                                           'guard="/gone/hooks/secret-guard.py"\nexit 0\n'))
        os.chmod(path, 0o755)
    st, by = status(env, p24)
    check("Soul hooks with a dead guard path: repair",
          by["hand-hooks"]["action"] == "repair"
          and "point at a missing plugin path" in by["hand-hooks"]["detail"]
          and "pre-commit, commit-msg, pre-push" in by["hand-hooks"]["detail"], by["hand-hooks"])

    # 25 — the record in a vault: line endings check the vault repo too
    v3 = repo(tmp, "vault3", {"vault.md": "# v\n", "projects/lv/soul/witness.md": "# W\n"})
    p25 = repo(tmp, "lv", {"CLAUDE.md": IMPORT, ".gitattributes": RULES})
    os.symlink(os.path.join(v3, "projects", "lv", "soul"), os.path.join(p25, ".soul"))
    st, by = status(env, p25)
    le = by.get("line-endings", {})
    check("vault without the rule: line-endings asks, naming the vault",
          le.get("action") == "ask" and le.get("detail", "").endswith("Needs it: vault."), le)
    p25b = repo(tmp, "lv2", {"CLAUDE.md": IMPORT})
    os.symlink(os.path.join(v3, "projects", "lv", "soul"), os.path.join(p25b, ".soul"))
    st, by = status(env, p25b)
    check("neither has the rule: line-endings names both",
          by["line-endings"]["detail"].endswith("Needs it: both."), by["line-endings"])

    # 26 — details cite the skill's section names, never step numbers
    stale = [(k, i["detail"]) for p in (p1, p13, p8b) for k, i in status(envv, p)[1].items()
             if "skill step" in i["detail"]]
    check("no detail cites 'skill step N'", not stale, stale)

    # 27 — one wording, two files: the stage descriptions match skills/soul-stage
    stage_md = read(os.path.join(_ROOT, "skills", "soul-stage", "SKILL.md"))
    missing = [o["description"] for o in mod.QUESTIONS["stage"]["options"]
               if o["value"] != "not-now" and o["description"] not in stage_md]
    check("stage descriptions appear verbatim in skills/soul-stage/SKILL.md", not missing,
          missing)

    # 28 — scoped-check fixes: the vault link comes alone; record takes only known
    #      values; --ask forces only choices, and a forced record still asks visibility
    st, by = status(envv, p13)
    check("vault holds it, nothing links: the re-link is the only round",
          st["rounds"] == [["vault-link"]], st["rounds"])
    p28 = repo(tmp, "values", {"README.md": "x\n"})
    r = run(env, "record", p28, "history-scan", "no")
    check("record history-scan no: stored as declined",
          r.returncode == 0 and "declined" in read(os.path.join(p28, ".soul", "init.md")),
          r.stdout + r.stderr)
    r = run(env, "record", p28, "stage", "beta")
    check("record an unknown value: exit 2, nothing stored", r.returncode == 2
          and "beta" not in read(os.path.join(p28, ".soul", "init.md")), r.stderr)
    r = run(env, "record", p28, "vault-link", "not-now")
    check("record vault-link not-now: refused (it stays a pending question)",
          r.returncode == 2, r.stderr)
    r = run(envl, "status", p2, "--json", "--ask", "import", "--ask", "layout")
    st = json.loads(r.stdout) if r.returncode == 0 else {"items": []}
    by = {i["key"]: i for i in st["items"]}
    check("--ask import/layout: warned and ignored, never a second import question",
          r.returncode == 0 and "--ask ignores import, layout" in r.stderr
          and by.get("import", {}).get("action") == "none", (r.stderr, by.get("import")))
    r = run(envl, "status", p2, "--json", "--ask", "record")
    st = json.loads(r.stdout) if r.returncode == 0 else {"items": [], "rounds": []}
    by = {i["key"]: i for i in st["items"]}
    check("--ask record with unknown visibility: record asked as a picker, public not asked",
          by.get("public", {}).get("action") == "none" and ["record"] in st["rounds"]
          and "public" not in sum(st["rounds"], []),
          (by.get("public"), st.get("rounds")))

    # 29 — found in the live trial: an answer recorded this run, not yet carried out,
    #      is a repair (step 4 does it), never the same question again
    p29 = repo(tmp, "addlater", {"CLAUDE.md": "# notes\n", "README.md": "x\n"})
    run(env, "record", p29, "import", "add")
    st, by = status(env, p29)
    check("recorded import add, line not written: repair, not asked again",
          by["import"]["action"] == "repair" and ["import"] not in st["rounds"],
          (by["import"], st["rounds"]))

    # 30 — a fresh clone the completion gate wrote .soul/events.jsonl into: the re-link is
    #      asked, not a TWO COPIES stop (v3.6.3); anything more in .soul/ still stops
    write(os.path.join(vroot, "projects", "clone2", "soul", "witness.md"), "# W\n")
    p30 = repo(tmp, "clone2", {"README.md": "x\n"})
    write(os.path.join(p30, ".soul", "events.jsonl"), '{"event": "x"}\n')
    st, by = status(envv, p30)
    check("gate log only in .soul/, vault holds the record: vault-link asks, alone",
          by.get("vault-link", {}).get("action") == "ask" and st["rounds"] == [["vault-link"]],
          (by.get("vault-link"), st["rounds"]))
    write(os.path.join(p30, ".soul", "handoff.md"), "# H\n")
    st, by = status(envv, p30)
    check("gate log plus handoff.md: vault-link stops on TWO COPIES",
          by.get("vault-link", {}).get("action") == "stop"
          and by["vault-link"]["value"] == "two-copies", by.get("vault-link"))

    # 31 — the sidecar offer (v3.6.3): the record is tracked at the root, the private .soul/
    #      is only on this disk, and this machine's vault holds no record for the project →
    #      asked alone; any one condition off → not asked; a recorded keep is final
    def sidecar_repo(name, commit=True):
        p = repo(tmp, name, {"CLAUDE.md": IMPORT, "witness.md": "# W\n", "ideas.md": "# I\n",
                             ".gitignore": ".soul/\n"}, commit=commit)
        write(os.path.join(p, ".soul", "handoff.md"), "# H\n")
        return p

    def sidecar_asked(env_, p):
        st_, by_ = status(env_, p)
        return by_.get("sidecar", {}).get("action") == "ask", st_, by_

    p31 = sidecar_repo("sc")
    asked, st, by = sidecar_asked(envv, p31)
    q = (by.get("sidecar") or {}).get("question") or {}
    check("sidecar fits: asked in a round of its own", asked and ["sidecar"] in st["rounds"]
          and q.get("group") == "single" and q.get("multi") is False, (by.get("sidecar"),
                                                                      st["rounds"]))
    check("sidecar question: no option recommended", "recommended" in q
          and q["recommended"] is None, q)
    check("sidecar question: fixed wording",
          q.get("text") == "This project's record is committed here, but its .soul/ folder "
          "(handoff, private-names list) is only on this disk. Move .soul/ into your vault?"
          and [(o["value"], o["label"], o["description"]) for o in q.get("options", [])] == [
              ("move", "Move it to the vault", "copies .soul/ into your private vault, checks "
               "every file, and leaves a link here; the record files at the root stay "
               "committed"),
              ("keep", "Keep it here", "nothing changes and this is not asked again "
               "(`/soul-init revisit sidecar` asks again)")], q)
    asked, _, _ = sidecar_asked(env, p31)
    check("sidecar: not asked when this machine names no vault", not asked)
    p31o = repo(tmp, "sc-open", {"CLAUDE.md": IMPORT, "witness.md": "# W\n", "ideas.md": "# I\n"})
    write(os.path.join(p31o, ".soul", "handoff.md"), "# H\n")  # tracked root, .soul/ not ignored
    asked, _, byo = sidecar_asked(envv, p31o)
    check("sidecar: not offered while the record question is open (no opposite answers)",
          not asked and byo.get("record", {}).get("action") in ("ask", "repair"),
          (byo.get("record"), byo.get("sidecar")))
    # the two further cases the replay's round-2 reviewers raised (2026-10-27)
    p31f = sidecar_repo("sc-force")
    r = run(envv, "status", p31f, "--json", "--ask", "record")
    byf = {i["key"]: i for i in json.loads(r.stdout)["items"]} if r.stdout.strip() else {}
    check("sidecar: not offered beside a forced record question (--ask record)",
          byf.get("record", {}).get("action") == "ask" and not byf.get("sidecar"),
          (byf.get("record"), byf.get("sidecar"), r.stderr[-300:]))
    p31l = sidecar_repo("sc-local")
    run(envv, "record", p31l, "record", "local")
    asked, _, byl = sidecar_asked(envv, p31l)
    check("sidecar: not offered while a recorded `record: local` needs its repair",
          not asked and byl.get("record", {}).get("action") == "repair",
          (byl.get("record"), byl.get("sidecar")))
    p31b = sidecar_repo("sc-link")
    shutil.rmtree(os.path.join(p31b, ".soul"))
    write(os.path.join(tmp, "sc-elsewhere", "handoff.md"), "# H\n")
    os.symlink(os.path.join(tmp, "sc-elsewhere"), os.path.join(p31b, ".soul"))
    asked, _, by = sidecar_asked(envv, p31b)
    check("sidecar: not asked when .soul is a link", not asked, by.get("sidecar"))
    p31c = sidecar_repo("sc-untracked", commit=False)
    asked, _, by = sidecar_asked(envv, p31c)
    check("sidecar: not asked when the root stores are untracked", not asked, by.get("sidecar"))
    p31d = sidecar_repo("sc-store")
    write(os.path.join(p31d, ".soul", "mind.md"), "# M\n")
    asked, _, by = sidecar_asked(envv, p31d)
    check("sidecar: not asked when .soul/ holds a record store", not asked, by.get("sidecar"))
    p31e = sidecar_repo("sc-tracked")
    write(os.path.join(p31e, ".soul", "notes.md"), "n\n")
    git(p31e, "add", "-f", ".soul/notes.md")
    git(p31e, "commit", "-qm", "notes")
    asked, _, by = sidecar_asked(envv, p31e)
    check("sidecar: not asked when .soul/ has a tracked file", not asked, by.get("sidecar"))
    p31f = sidecar_repo("sc-held")
    write(os.path.join(vroot, "projects", "sc-held", "soul", "handoff.md"), "# H\n")
    asked, _, by = sidecar_asked(envv, p31f)
    check("sidecar: not asked when the vault already holds a record for it", not asked,
          by.get("sidecar"))
    p31g = sidecar_repo("sc-nothing-private")
    os.remove(os.path.join(p31g, ".soul", "handoff.md"))
    write(os.path.join(p31g, ".soul", "events.jsonl"), '{"event": "x"}\n')
    write(os.path.join(p31g, ".soul", "init.md"), "names:         none         2026-10-27\n")
    asked, _, by = sidecar_asked(envv, p31g)
    check("sidecar: not asked when .soul/ holds only events.jsonl and init.md", not asked,
          by.get("sidecar"))
    write(os.path.join(p31g, ".soul", "private-names.txt"), "Acme\n")
    asked, _, by = sidecar_asked(envv, p31g)
    check("sidecar: asked when .soul/ holds private-names.txt (no handoff.md)", asked,
          by.get("sidecar"))
    r = run(envv, "record", p31, "sidecar", "move")
    asked, _, by = sidecar_asked(envv, p31)
    check("sidecar: a recorded move while .soul/ is still a real folder asks again",
          r.returncode == 0 and asked, (r.stderr, by.get("sidecar")))
    r = run(envv, "record", p31, "sidecar", "keep")
    asked, st, by = sidecar_asked(envv, p31)
    check("sidecar: a recorded keep is final — none, from the record", r.returncode == 0
          and not asked and by.get("sidecar", {}).get("action") == "none"
          and by["sidecar"]["source"] == "recorded" and ["sidecar"] not in st["rounds"],
          (r.stderr, by.get("sidecar")))
    r = run(envv, "record", p31, "sidecar", "maybe")
    check("sidecar: an unknown value is refused, naming move, keep", r.returncode == 2
          and "move, keep" in r.stderr, r.stderr)
    run(envv, "revisit", p31, "sidecar")
    asked, _, by = sidecar_asked(envv, p31)
    check("sidecar: revisit asks again", asked, by.get("sidecar"))

    # 32 — wiring kept in the gitignored CLAUDE.local.md is found: the import, the stage,
    #      and the Mind repair names that file (mining pass 3, SOUL-234)
    p32 = repo(tmp, "localmd", {"CLAUDE.local.md": IMPORT + "\n**Stage: pre-release** (owner)\n",
                                ".soul/witness.md": "# W\n", ".soul/mind.md": "# M\n",
                                ".gitignore": "CLAUDE.local.md\n"})
    st, by = status(env, p32)
    check("CLAUDE.local.md holds the import: found, not asked",
          by["import"]["action"] == "none" and by["import"]["value"] == "CLAUDE.local.md",
          by["import"])
    check("CLAUDE.local.md holds the stage: found",
          by["stage"]["action"] == "none" and by["stage"]["value"] == "pre-release", by["stage"])
    check("the Mind repair writes into CLAUDE.local.md",
          by.get("mind", {}).get("action") == "repair"
          and "after the contract import in CLAUDE.local.md" in by["mind"]["detail"],
          by.get("mind"))

    # 33 — `triaged <sha>`: every hit read, none real
    p33 = repo(tmp, "triaged", {"README.md": "x\n"})
    head33 = git(p33, "rev-parse", "--short=12", "HEAD").stdout.strip()
    r = run(env, "record", p33, "history-scan", "triaged", head33)
    st, by = status(envl, p33)
    check("record history-scan triaged <sha>: stored", r.returncode == 0
          and "history-scan:  triaged " + head33 in read(os.path.join(p33, ".soul", "init.md")),
          r.stdout + r.stderr)
    check("triaged: not asked again, says hits checked, none real",
          by["history-scan"]["action"] == "none"
          and by["history-scan"]["detail"] == "Scanned at {}: hits checked, none real."
          .format(head33), by["history-scan"])
    r = run(env, "record", p33, "history-scan", "triaged")
    check("triaged with no sha: refused", r.returncode == 2 and "triaged <sha>" in r.stderr,
          r.stderr)

    # 34 — hand hooks: the skill's template is all Soul lines; a hook merged by hand keeps
    #      its other lines (only guard= is rewritten); an old pre-push in an LFS repo is
    #      rewritten so hand pushes upload LFS objects (mining pass 3, SOUL-234)
    skill = read(os.path.join(_ROOT, "skills", "soul-init", "SKILL.md"))
    tpl = skill.split("**`hand-hooks`**", 1)[1].split("```sh\n", 1)[1].split("\n```", 1)[0]
    old = ('#!/bin/sh\n# Soul System secret check (<hook>), installed by /soul-init '
           '(operations/secret-guard.md).\nguard="<root>/hooks/secret-guard.py"\n'
           'if [ ! -f "$guard" ] || ! command -v python3 >/dev/null 2>&1; then\n'
           '  echo "Soul secret check NOT running — plugin path missing; re-run /soul-init '
           'to repair the hook" >&2\n  exit 0\nfi\npython3 "$guard" --hand-hook <hook> "$@"\n'
           'rc=$?\n[ "$rc" -eq 3 ] && exit 1\n[ "$rc" -ne 0 ] && echo "Soul secret guard '
           'failed (exit $rc) — this git <hook> was NOT checked" >&2\nexit 0\n')
    left = {n: mod.hand_hook_extras(t.replace("<root>", _ROOT).replace("<hook>", "pre-push"))
            for n, t in (("current", tpl), ("v2.10.0", old))}
    check("every template version (the skill's current one too) is all Soul lines",
          left == {"current": [], "v2.10.0": []}, left)

    def hooks34(name, text_for, files=None):
        p = repo(tmp, name, dict({"CLAUDE.md": IMPORT, ".soul/witness.md": "# W\n"},
                                 **(files or {})))
        for h in ("pre-commit", "commit-msg", "pre-push"):
            path = os.path.join(p, ".git", "hooks", h)
            write(path, text_for(h))
            os.chmod(path, 0o755)
        return p
    p34 = hooks34("tplhooks", lambda h: tpl.replace("<root>", _ROOT).replace("<hook>", h))
    st, by = status(env, p34)
    check("the skill's template, live root: none", by["hand-hooks"]["action"] == "none",
          by["hand-hooks"])
    merged = lambda h: old.replace("<root>", "/gone").replace("<hook>", h).replace(
        "\nexit 0\n", '\ngit lfs pre-push "$@" < "$in"\nexit 0\n') if h == "pre-push" else \
        old.replace("<root>", "/gone").replace("<hook>", h)
    p34b = hooks34("mergedhooks", merged)
    st, by = status(env, p34b)
    d = by["hand-hooks"]["detail"]
    check("a hand-merged pre-push with a dead path: rewrite only its guard= line",
          by["hand-hooks"]["action"] == "repair"
          and "Soul hook(s) pre-push point at a missing plugin path and also hold lines merged "
              "by hand — rewrite only the guard= line" in d
          and "Soul hook(s) pre-commit, commit-msg point at a missing plugin path — rewrite "
              "them with the current root" in d, d)
    lfs_bin = os.path.join(tmp, "bin-lfs")
    os.makedirs(lfs_bin)
    os.symlink(shutil.which("git"), os.path.join(lfs_bin, "git"))
    write(os.path.join(lfs_bin, "git-lfs"), "#!/bin/sh\nexit 0\n")
    os.chmod(os.path.join(lfs_bin, "git-lfs"), 0o755)
    envlfs = dict(base, PATH=lfs_bin)
    attrs = {".gitattributes": "*.bin filter=lfs diff=lfs merge=lfs -text\n"}
    p34c = hooks34("oldlfs", lambda h: old.replace("<root>", _ROOT).replace("<hook>", h), attrs)
    st, by = status(envlfs, p34c)
    check("an old Soul pre-push in an LFS repo: repair, rewrite with the current template",
          by["hand-hooks"]["action"] == "repair"
          and "does not run `git lfs pre-push`" in by["hand-hooks"]["detail"], by["hand-hooks"])
    st, by = status(env, p34c)
    check("...but not where git-lfs is not installed", by["hand-hooks"]["action"] == "none",
          by["hand-hooks"])
    p34d = hooks34("newlfs", lambda h: tpl.replace("<root>", _ROOT).replace("<hook>", h), attrs)
    st, by = status(envlfs, p34d)
    check("the current template in an LFS repo: none", by["hand-hooks"]["action"] == "none",
          by["hand-hooks"])

    # 34b — the template under Windows git (Git for Windows' shell) cannot reach the WSL
    #       guard: it says the push is NOT checked and does not send the owner to
    #       /soul-init, which cannot repair it (MODEL-LIB, 2026-11-10). uname is a stub.
    def hand_run(uname):
        stub = os.path.join(tmp, "bin-uname-" + uname[:5])
        write(os.path.join(stub, "uname"), "#!/bin/sh\necho {}\n".format(uname))
        os.chmod(os.path.join(stub, "uname"), 0o755)
        hk = os.path.join(stub, "pre-push")
        write(hk, tpl.replace("<root>", "/gone").replace("<hook>", "pre-push"))
        return subprocess.run(["sh", hk, "origin", "x"], input="", capture_output=True,
                              text=True, env=dict(base, PATH=stub + os.pathsep + "/usr/bin:/bin"))
    rw, rl = hand_run("MINGW64_NT-10.0-19045"), hand_run("Linux")
    check("34b: under Windows git the hand pre-push says NOT checked, no /soul-init advice; "
          "under Linux the repair advice stays", rw.returncode == 0
          and "Windows git cannot run the WSL guard — this git pre-push is NOT checked"
          in rw.stderr and "/soul-init" not in rw.stderr and rl.returncode == 0
          and "re-run /soul-init" in rl.stderr and "Windows" not in rl.stderr,
          rw.stderr + rl.stderr)

    # 35 — upkeep (SOUL-A032): asked once, default on; the hook reads the same line.
    #      Unanswered, it is on — the question is how to turn it off, so no answer must
    #      never read as off (the owner's choice of default, A032 open question 3).
    p35 = repo(tmp, "upkeep", {"README.md": "x\n"})
    st, by = status(env, p35)
    q = by["upkeep"]["question"]
    check("upkeep: unanswered is asked, on recommended, fixed wording",
          by["upkeep"]["action"] == "ask" and q["recommended"] == 0
          and [o["value"] for o in q["options"]] == ["on", "off"]
          and q["text"] == "Should the Soul keep its notes up to date on its own?"
          and "until then it is on" in by["upkeep"]["detail"], by["upkeep"])
    r = run(env, "record", p35, "upkeep", "sometimes")
    check("upkeep: a value other than on/off is refused, nothing written",
          r.returncode == 2 and "upkeep takes one of: on, off" in r.stderr
          and not os.path.exists(os.path.join(p35, ".soul", "init.md")), r.stderr)
    r = run(env, "record", p35, "upkeep", "off")
    st, by = status(env, p35)
    check("upkeep: recorded off is set, not asked again",
          r.returncode == 0 and by["upkeep"]["action"] == "none"
          and by["upkeep"]["value"] == "off" and "upkeep" not in sum(st["rounds"], []),
          (r.stderr, by["upkeep"]))
    spec = importlib.util.spec_from_file_location(
        "soul_upkeep_hook", os.path.join(_ROOT, "hooks", "upkeep.py"))
    hook = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hook)
    check("upkeep: the hook reads the line `record` wrote", hook.upkeep_answer(p35) == "off",
          read(os.path.join(p35, ".soul", "init.md")))
    st = json.loads(run(env, "status", p35, "--json", "--ask", "upkeep").stdout)
    asked = {i["key"]: i["action"] for i in st["items"]}
    check("upkeep: --ask upkeep puts the question back (/soul-init revisit upkeep)",
          asked.get("upkeep") == "ask", asked)
    # The tool and the hook read a hand-written value the same way: `OFF` is off in both;
    # `no` is not understood — asked again here, and the hook stays on (it blocks).
    write(os.path.join(p35, ".soul", "init.md"), "upkeep:        OFF          2026-11-12\n")
    st, by = status(env, p35)
    check("upkeep: a hand-written OFF reads as off in the tool and the hook",
          by["upkeep"]["action"] == "none" and by["upkeep"]["value"] == "off"
          and hook.upkeep_answer(p35) == "off", (by["upkeep"], hook.upkeep_answer(p35)))
    write(os.path.join(p35, ".soul", "init.md"), "upkeep:        no           2026-11-12\n")
    st, by = status(env, p35)
    check("upkeep: a hand-written `no` is not understood — asked again, and not off",
          by["upkeep"]["action"] == "ask" and "not understood" in by["upkeep"]["detail"]
          and hook.upkeep_answer(p35) != "off", (by["upkeep"], hook.upkeep_answer(p35)))

    plan_checks(tmp, env, envl, envv, vroot, mod)
    shutil.rmtree(tmp, ignore_errors=True)
    print("\n{} failure(s)".format(len(FAILS)) if FAILS else "\nALL PASS")
    return 1 if FAILS else 0


def plan_of(env, project, *extra):
    """(status JSON, its plan or {}, the run) for `status --json` with extra args."""
    r = run(env, "status", project, "--json", *extra)
    try:
        st = json.loads(r.stdout)
    except ValueError:
        st = {"items": [], "rounds": [], "_err": r.stderr}
    return st, st.get("plan") or {}, r


def lines_of(plan):
    return {ln["key"]: ln for ln in plan.get("lines", [])}


def go_keys(plan):
    return [k for k, _ in plan.get("go", [])]


def also_fixes(plan):
    """The plan text's "Also fixes" line ("Also sets up" on a fresh project) with its
    wrapped continuation, flattened."""
    out, on = [], False
    for ln in plan.get("text", "").splitlines():
        if ln.startswith(("Also fixes:", "Also sets up:")):
            on = True
        elif on and not ln.startswith("  "):
            break
        if on:
            out.append(ln)
    return " ".join(" ".join(out).split())


def tree_hash(root):
    """Every file under root (the .git folder included), path and bytes."""
    h = hashlib.sha256()
    for dirpath, dirs, files in os.walk(root):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(dirpath, f)
            h.update(os.path.relpath(p, root).encode() + b"\0")
            with open(p, "rb") as fh:
                h.update(fh.read() + b"\0")
    return h.hexdigest()


def plan_checks(tmp, env, envl, envv, vroot, mod):
    """v3.13.0 (SOUL-I092): one plan with defaults and one dialog, instead of the rounds."""
    home = env["HOME"]
    meanings = {
        "record": "Soul's log of this project's decisions and ideas.",
        "stage": "How careful to be about breaking things.",
        "names": "Names that must never be committed (clients, employers, people).",
        "upkeep": "Soul's handoff note and project notes, kept current.",
        "line-endings": "Windows and Linux tools end lines differently, so files can show as "
                        "changed when they are not.",
        "hand-hooks": "Checks commits you make outside Claude for secrets.",
        "history-scan": "Looks through past commits for leaked secrets, once."}

    # 36 — a fresh project, no remote: a plan, no public question, the record waits
    pf = repo(tmp, "plan-fresh", {"README.md": "x\n"})
    st, plan, _ = plan_of(envl, pf)
    lines = lines_of(plan)
    screen = plan.get("screen", [])
    rq = next((q for q in screen if q.get("key") == "record"), {})
    nq = screen[-1] if screen else {}
    check("36 fresh: a plan; the dialog is the record question then the next step, and no "
          "public question anywhere",
          bool(plan) and [q.get("key") for q in screen] == ["record", "next"]
          and "public" not in sum(st["rounds"], []), (st["rounds"], screen))
    check("36 fresh: the record waits, recommends nothing, offers three options, is not in go",
          lines.get("record", {}).get("waits") is True and "recommended" in rq
          and rq["recommended"] is None
          and [o["value"] for o in rq.get("options", [])] == ["git", "vault", "local"]
          and "record" not in go_keys(plan), (lines.get("record"), rq, plan.get("go")))
    check("36 fresh: every line in order, each with its fixed meaning",
          [k for k in lines if k != "repairs"] == list(meanings)
          and all(lines[k]["meaning"] == m for k, m in meanings.items()),
          plan.get("lines"))
    check("36 fresh: the text says what each line is (every meaning is in it)",
          all(m in " ".join(plan.get("text", "").split()) for m in meanings.values()),
          plan.get("text"))
    check("36 fresh: the next-step question, word for word, the plan in the first preview",
          nq.get("text") == "Here is the rest of the setup I'd make. Nothing is written until "
                            "you say go. What next?"
          and [(o["value"], o["label"], o["description"]) for o in nq.get("options", [])] == [
              ("use", "Use default setup", "Writes the setup shown in the plan."),
              ("modify", "Modify setup", "Opens stage, private names, upkeep and the safety "
                                         "checks, then shows the plan again."),
              ("explain", "Explain a line", "A short paragraph on every line, then this "
                                            "plan again."),
              ("not-now", "Not now", "Nothing is written. Run /soul-init again when you are "
                                     "ready.")]
          and nq["options"][0].get("preview") == plan.get("text")
          and nq.get("multi") is False and plan.get("modified") is False, nq)
    check("36 fresh: change rounds are today's pickers for stage, names, upkeep, extras",
          plan.get("change_rounds") == [["stage", "names", "upkeep"], ["extras"]],
          plan.get("change_rounds"))
    cur = re.search(r"Current: \*\*([^*]+)\*\*",
                    read(os.path.join(_ROOT, "SYSTEM-VERSION.md"))).group(1)
    check("36 fresh: more points at the page, at this release's tag, and at the local copy",
          plan.get("more") == {
              "url": "https://github.com/soul-system-works/Soul-System/blob/v{}/docs/"
                     "setup-choices.md".format(cur),
              "path": os.path.join(_ROOT, "docs", "setup-choices.md")}, plan.get("more"))

    # 37 — the vault: offered whether or not one is registered; the default differs
    pv = repo(tmp, "plan-vaulted", {"README.md": "x\n"})
    _, plan_n, _ = plan_of(env, pv)
    _, plan_v, _ = plan_of(envv, pv)
    opts = lambda pl: [o["value"] for q in pl.get("screen", []) if q.get("key") == "record"
                       for o in q["options"]]
    check("37 the vault option is offered with and without a registered vault",
          "vault" in opts(plan_n) and "vault" in opts(plan_v), (opts(plan_n), opts(plan_v)))
    check("37 vault_default: ~/soul-vault (new) with none registered; the registered one "
          "otherwise; nothing made",
          plan_n.get("vault_default") == {"path": os.path.join(home, "soul-vault"),
                                           "exists": False, "registered": False}
          and plan_v.get("vault_default") == {"path": vroot, "exists": True,
                                              "registered": True}
          and not os.path.exists(os.path.join(home, "soul-vault")),
          (plan_n.get("vault_default"), plan_v.get("vault_default")))
    which = lambda pl: [(o["value"], o["description"]) for o in
                        pl.get("followups", {}).get("vault-which", {}).get("options", [])]
    check("37 vault-which: a new vault is made and becomes the default; an existing one is "
          "named as yours",
          which(plan_n) == [("default", "Made now: a new private git repo in that folder. It "
                                        "becomes this machine's default vault."),
                            ("other", "Type the folder; a vault is made there if there is "
                                      "none.")]
          and which(plan_v)[:1] == [("default", "Your default vault.")]
          and plan_v["followups"]["vault-which"]["text"]
          == "Which vault should hold this project's log?"
          and plan_v["followups"]["vault-which"]["recommended"] == 0,
          (which(plan_n), which(plan_v)))
    conf = plan_v.get("followups", {}).get("vault-confirm", {})
    check("37 vault-confirm: fixed wording, four options",
          conf.get("text") == "Move this project's log into the vault at {}?".format(vroot)
          and [(o["value"], o["label"]) for o in conf.get("options", [])] == [
              ("move", "Move it"), ("tags", "Add tags, then move"),
              ("also", "Also move other private folders"), ("cancel", "Cancel")], conf)
    # The WSL drive rule, in-process with a made-up drive letter: the CLI refuses a
    # project folder that does not exist, and a real drive may hold a real vault.
    letter = next(x for x in "qzyxwvutsrponmlkjihgfeb" if not os.path.exists("/mnt/" + x))
    proj = "/mnt/{}/proj".format(letter)
    keep = {k: os.environ.get(k) for k in ("SOUL_VAULT_FORCE_WSL", "HOME", "XDG_CONFIG_HOME")}
    vp = getattr(mod, "vault_plan", lambda p: {})
    try:
        os.environ.update(SOUL_VAULT_FORCE_WSL="1", HOME=home,
                          XDG_CONFIG_HOME=os.path.join(tmp, "config"))
        none_reg = vp(proj)
        os.environ["XDG_CONFIG_HOME"] = os.path.join(tmp, "config-v")  # names vroot
        passed = vp(proj)
        os.environ["SOUL_VAULT_FORCE_WSL"] = "0"
        not_wsl = vp(proj)
    finally:
        for k, v in keep.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    drive_vault = "/mnt/{}/soul-vault".format(letter)
    pdesc = [o["description"] for o in passed.get("followups", {}).get("vault-which", {})
             .get("options", []) if o["value"] == "default"]
    check("37 WSL, project on a Windows drive: the default vault is on that drive; a "
          "registered vault off the drive is passed over, and the option says so",
          none_reg.get("vault_default") == {"path": drive_vault, "exists": False,
                                            "registered": False}
          and passed.get("vault_default") == {"path": drive_vault, "exists": False,
                                              "registered": False}
          and len(pdesc) == 1 and vroot in pdesc[0]
          and not_wsl.get("vault_default") == {"path": vroot, "exists": True,
                                               "registered": True},
          (none_reg, passed.get("vault_default"), pdesc, not_wsl.get("vault_default")))

    # 38 — a recorded visibility: private recommends git (and puts it in go); public does not
    pp = repo(tmp, "plan-private", {"README.md": "x\n"})
    run(env, "record", pp, "public", "no")
    _, plan, _ = plan_of(env, pp)
    rq = next((q for q in plan.get("screen", []) if q.get("key") == "record"), {})
    check("38 recorded public: no → git recommended and in go",
          rq.get("recommended") == 0 and ["record", "git"] in plan.get("go", []),
          (rq, plan.get("go")))
    pq = repo(tmp, "plan-public", {"README.md": "x\n"})
    run(env, "record", pq, "public", "yes")
    _, plan, _ = plan_of(env, pq)
    rq = next((q for q in plan.get("screen", []) if q.get("key") == "record"), {})
    check("38 recorded public: yes → nothing recommended, record not in go",
          bool(rq) and rq.get("recommended") is None and "record" not in go_keys(plan),
          (rq, plan.get("go")))

    # 39 — go holds exactly the defaults; recorded and carried out, nothing is left to ask
    pg = repo(tmp, "plan-go", {"README.md": "x\n"})
    _, plan, _ = plan_of(env, pg)
    _, plan_l, _ = plan_of(envl, pg)
    want = [["stage", "not-now"], ["names", "none"], ["upkeep", "on"],
            ["line-endings", "yes"], ["hand-hooks", "no"]]
    check("39 go holds exactly the default pairs (history-scan declined only where the scan "
          "can run)", plan.get("go") == want and plan.get("todo") == []
          and plan_l.get("go") == want + [["history-scan", "declined"]],
          (plan.get("go"), plan_l.get("go")))
    for k, v in want + [["record", "git"]]:
        run(env, "record", pg, k, v)
    st, plan, _ = plan_of(env, pg)
    check("39 recorded, line-endings fix not yet done: only that line remains, its default "
          "the recorded yes", [k for k in lines_of(plan) if k != "repairs"] == ["line-endings"]
          and plan["lines"][0]["default"]["value"] == "yes", plan.get("lines"))
    rf = subprocess.run([sys.executable, os.path.join(_HERE, "eol.py"), "fix", pg],
                        capture_output=True, text=True, env=env)
    rc = git(pg, "commit", "-qm", "line endings")
    st, plan, _ = plan_of(env, pg)
    check("39 after the line-endings fix and its commit: plan null, nothing to ask",
          rf.returncode == 0 and rc.returncode == 0 and "plan" in st and st["plan"] is None
          and st["rounds"] == [], (rf.stdout + rf.stderr, rc.stderr, st.get("rounds"),
                                   st.get("plan")))

    # 40 — --choose renders a change before anything is recorded
    _, plan, _ = plan_of(env, pf, "--choose", "stage=prototype")
    nq = (plan.get("screen") or [{}])[-1]
    check("40 --choose stage=prototype: the line, go and modified change; Use this setup",
          lines_of(plan).get("stage", {}).get("default", {}).get("value") == "prototype"
          and ["stage", "prototype"] in plan.get("go", [])
          and ["stage", "not-now"] not in plan.get("go", [])
          and plan.get("modified") is True
          and nq.get("options", [{}])[0].get("label") == "Use this setup",
          (plan.get("lines"), plan.get("go"), nq))
    _, plan, _ = plan_of(env, pf, "--choose", "record=local")
    check("40 --choose record=local: in go, the record no longer waits or asks",
          ["record", "local"] in plan.get("go", [])
          and lines_of(plan).get("record", {}).get("waits") is False
          and [q.get("key") for q in plan.get("screen", [])] == ["next"], plan.get("screen"))
    _, plan, _ = plan_of(envl, pf, "--choose", "history-scan=yes")
    check("40 --choose history-scan=yes: in todo, not in go",
          plan.get("todo") == ["history-scan"] and "history-scan" not in go_keys(plan),
          (plan.get("todo"), plan.get("go")))
    bad = [run(env, "status", pf, "--json", "--choose", a).returncode
           for a in ("import=add", "stage=beta", "stage", "names=")]
    check("40 --choose with a bad key or value: exit 2", bad == [2, 2, 2, 2], bad)

    # 41 — a forced key is a picker, never a plan line; a recorded answer is never replaced
    pu = repo(tmp, "plan-upkeep-off", {"README.md": "x\n"})
    run(env, "record", pu, "upkeep", "off")
    st, plan, _ = plan_of(env, pu, "--ask", "upkeep")
    check("41 --ask upkeep, upkeep off recorded: a picker in rounds, not a plan line, no "
          "default over it", bool(plan) and ["upkeep"] in st["rounds"]
          and "upkeep" not in lines_of(plan) and "upkeep" not in go_keys(plan),
          (st["rounds"], plan.get("go")))
    pn = repo(tmp, "plan-names", {"README.md": "x\n"})
    run(env, "record", pn, "names", "listed")
    run(env, "record", pn, "stage", "prototype")
    _, plan, _ = plan_of(env, pn)
    ln = lines_of(plan)
    check("41 names listed and a stage recorded, files missing: the defaults are the recorded "
          "answers, said so", ln.get("names", {}).get("default", {}).get("value") == "listed"
          and ln.get("stage", {}).get("default", {}).get("value") == "prototype"
          and ["names", "listed"] in plan.get("go", [])
          and ["stage", "prototype"] in plan.get("go", [])
          and "earlier answer" in ln["names"]["default"]["text"],
          (plan.get("lines"), plan.get("go")))

    # 42 — no plan while the vault's record waits for its link; none when all is set
    write(os.path.join(vroot, "projects", "clone3", "soul", "witness.md"), "# W\n")
    p42 = repo(tmp, "clone3", {"README.md": "x\n"})
    st, _, _ = plan_of(envv, p42)
    check("42 vault-link asked, not broken: plan null, the re-link alone",
          "plan" in st and st["plan"] is None and st["rounds"] == [["vault-link"]],
          (st.get("plan"), st["rounds"]))
    ps = set_up(tmp, "plan-setup")
    st, _, _ = plan_of(envl, ps)
    check("42 a project already set up: plan null", "plan" in st and st["plan"] is None,
          st.get("plan"))
    ph = repo(tmp, "plan-half", {"README.md": "x\n"})
    write(os.path.join(ph, ".soul", "init.md"), "stage:         not-now      2026-11-13\n"
          "names:         none         2026-11-13\n")
    _, plan, _ = plan_of(env, ph)
    check("42 half answered: only the unanswered lines",
          [k for k in lines_of(plan) if k != "repairs"]
          == ["record", "upkeep", "line-endings", "hand-hooks"]
          and not {"stage", "names"} & set(go_keys(plan)), plan.get("lines"))

    # 42b — each of the seven repairs is named on the "Also fixes" line
    def fixture(name, files, answers=""):
        p = repo(tmp, name, files)
        if answers:
            write(os.path.join(p, ".soul", "init.md"), answers)
        return p
    fx = [("the Soul line in CLAUDE.md", env, fixture("fix-import", {"README.md": "x\n"})),
          ("hand-commit hooks", env,
           fixture("fix-hooks", {"CLAUDE.md": IMPORT, ".soul/witness.md": "# W\n"},
                   "hand-hooks:    yes          2026-10-23\n")),
          ("the project-notes import", env,
           fixture("fix-mind", {"CLAUDE.md": IMPORT, ".soul/witness.md": "# W\n",
                                ".soul/mind.md": "# M\n"})),
          ("the record's git state", env,
           fixture("fix-record", {"CLAUDE.md": IMPORT, ".soul/witness.md": "# W\n"},
                   "record:        local        2026-10-26\n"))]
    pe = fixture("fix-eol", {"CLAUDE.md": IMPORT, ".gitattributes": RULES, "a.txt": "one\n"})
    write(os.path.join(pe, "a.txt"), b"one\r\n", mode="wb")
    fx.append(("line endings", env, pe))
    write(os.path.join(vroot, "projects", "fix-link", "soul", "witness.md"), "# W\n")
    pl = fixture("fix-link", {"README.md": "x\n"})
    os.symlink(os.path.join(tmp, "old-vault2", "projects", "fix-link", "soul"),
               os.path.join(pl, ".soul"))
    fx.append(("the link to the vault", envv, pl))
    pst = fixture("fix-store", {"CLAUDE.md": IMPORT, "docs/ideas.md": "# I\n"})
    run(env, "record", pst, "existing-store", "use")
    fx.append(("the pointer to your existing record", env, pst))
    missing = []
    for words, env_, p in fx:
        line = also_fixes(plan_of(env_, p)[1])
        if words not in line:
            missing.append((words, line))
    check("42b each repair is named in everyday words on the 'Also fixes' line", not missing,
          missing)

    # 43 — the text fits the dialog's preview box; line endings carry a file count
    pc = repo(tmp, "plan-crlf", {"a.txt": "one\r\ntwo\r\n", "b.txt": "x\r\n", "c.txt": "lf\n"})
    texts = {}
    for name, env_, p, extra in (("fresh", envl, pf, ()), ("crlf", env, pc, ()),
                                 ("half", env, ph, ()), ("vault", envv, pv, ()),
                                 ("chosen", envl, pf, ("--choose", "hand-hooks=yes",
                                                       "--choose", "history-scan=yes",
                                                       "--choose", "names=listed"))):
        texts[name] = plan_of(env_, p, *extra)[1].get("text", "")
    wide = [(n, ln) for n, t in texts.items() for ln in t.splitlines() if len(ln) > 66]
    check("43 every line of plan.text is at most 66 columns", all(texts.values()) and not wide,
          wide or texts)
    flat = {n: " ".join(t.split()) for n, t in texts.items()}
    check("43 the line-endings line carries the count of files that change",
          "(0 files change; adds the rule file)" in flat["fresh"]
          and "(2 files change; adds the rule file)" in flat["crlf"], flat)
    n_fresh = len(texts["fresh"].splitlines())
    check("43 a fresh project's plan is about 30 lines", 20 <= n_fresh <= 34, n_fresh)

    # 44 — the explanation page: generated, committed, never the version number
    r = run(env, "doc", "--check")
    check("44 doc --check passes on the committed page", r.returncode == 0,
          r.stdout + r.stderr)
    r = run(env, "doc")
    page = os.path.join(_ROOT, "docs", "setup-choices.md")
    check("44 doc prints the committed page, without the version number",
          r.returncode == 0 and os.path.isfile(page) and r.stdout == read(page)
          and cur not in r.stdout, r.stderr)
    cp = os.path.join(tmp, "doc-copy")
    for rel in ("tools/init-status.py", "tools/eol.py", "tools/vault.py",
                "docs/setup-choices.md"):
        if os.path.isfile(os.path.join(_ROOT, rel)):
            write(os.path.join(cp, rel), read(os.path.join(_ROOT, rel)))
    tool_cp = os.path.join(cp, "tools", "init-status.py")
    ctl = subprocess.run([sys.executable, tool_cp, "doc", "--check"], capture_output=True,
                         text=True, env=env)
    write(tool_cp, read(tool_cp).replace("How careful to be about breaking things.",
                                         "How careful to be when breaking things."))
    chg = subprocess.run([sys.executable, tool_cp, "doc", "--check"], capture_output=True,
                         text=True, env=env)
    check("44 doc --check fails after a wording change (passes on the unchanged copy)",
          ctl.returncode == 0 and chg.returncode == 1, (ctl.returncode, chg.returncode,
                                                         chg.stdout + chg.stderr))

    # 45 — explain, the text output, and status writing nothing (--choose included)
    r = run(env, "explain", pf)
    check("45 explain: a paragraph per plan line, each naming its revisit",
          r.returncode == 0
          and all("/soul-init revisit {}".format(k) in r.stdout
                  for k in ("record", "stage", "names", "upkeep", "line-endings", "hand-hooks"))
          and "revisit history-scan" not in r.stdout, r.stdout + r.stderr)
    r = run(env, "status", pf)
    check("45 status text: the plan and the four choices, no 'To ask'",
          r.returncode == 0 and "Use default setup" in r.stdout and "Not now" in r.stdout
          and meanings["stage"] in r.stdout and "To ask" not in r.stdout, r.stdout)
    before = tree_hash(pf)
    rs = [plan_of(env, pf)[2], plan_of(env, pf, "--choose", "stage=prototype")[2],
          plan_of(envl, pf, "--choose", "history-scan=yes", "--choose", "record=vault")[2],
          run(env, "status", pf), run(env, "explain", pf)]
    check("45 status (with --choose too) and explain leave the project byte-identical",
          all(x.returncode == 0 for x in rs) and tree_hash(pf) == before
          and not os.path.exists(os.path.join(pf, ".soul")),
          [(x.returncode, x.stderr[-200:]) for x in rs])

    # 46 — the review of v3.13.0: the fixes asked for (R3, R7, R8, R9, R11)
    # R3: a typed folder gets the confirm question too: the sentence with {path} left in.
    conf = plan_of(envv, pv)[1].get("followups", {}).get("vault-confirm", {})
    check("46 R3 vault-confirm carries the template for a typed folder; text stays rendered",
          conf.get("template") == "Move this project's log into the vault at {path}?"
          and conf.get("text") == "Move this project's log into the vault at {}?".format(vroot),
          conf)
    # R7: only the record waits, so Modify setup has nothing to open: it is left out.
    po = repo(tmp, "plan-only-record", {"CLAUDE.md": IMPORT, ".gitattributes": RULES})
    write(os.path.join(po, ".soul", "init.md"),
          "stage:         not-now      2026-11-01\nnames:         none         2026-11-01\n"
          "upkeep:        on           2026-11-01\nhand-hooks:    no           2026-11-01\n"
          "history-scan:  declined     2026-11-01\n")
    _, plan, _ = plan_of(envl, po)
    nq = (plan.get("screen") or [{}])[-1]
    check("46 R7 only the record waits: no change rounds, and no Modify setup option",
          [k for k in lines_of(plan) if k != "repairs"] == ["record"]
          and plan.get("change_rounds") == []
          and [o["value"] for o in nq.get("options", [])] == ["use", "explain", "not-now"],
          (plan.get("lines"), plan.get("change_rounds"), nq))
    # ... and "Not set up" says Modify setup can add them only when it can: with line
    # endings forced (--ask), the extras are asked as a picker, not under Modify setup.
    _, plan_f, _ = plan_of(envl, pf, "--ask", "line-endings")
    t_free, t_forced = texts["fresh"], plan_f.get("text", "")
    check("46 R7 'Not set up' names Modify setup only when an extras round exists",
          "Not set up (Modify setup can add them):" in t_free
          and plan_f.get("change_rounds") == [["stage", "names", "upkeep"]]
          and "Not set up:" in t_forced and "Modify setup can add" not in t_forced,
          (plan_f.get("change_rounds"), t_forced))
    # R8: a recorded value the tool does not understand: the line says so and shows the
    # default that replaces it.
    pw = repo(tmp, "plan-not-understood", {"README.md": "x\n"})
    write(os.path.join(pw, ".soul", "init.md"), "stage:         Prototype    2026-11-01\n"
          "upkeep:        maybe        2026-11-01\n")
    _, plan, _ = plan_of(env, pw)
    ln = lines_of(plan)
    st_t = ln.get("stage", {}).get("default") or {}
    up_t = ln.get("upkeep", {}).get("default") or {}
    check("46 R8 an answer not understood: the line says so, with the default replacing it",
          st_t.get("value") == "not-now" and up_t.get("value") == "on"
          and st_t.get("text", "").startswith("Not now: nothing is written")
          and 'Your earlier answer "Prototype" was not understood' in st_t.get("text", "")
          and 'Your earlier answer "maybe" was not understood' in up_t.get("text", "")
          and ["stage", "not-now"] in plan.get("go", []), (st_t, up_t, plan.get("go")))
    # R9: in a repo known to be public, the Private names line carries today's note.
    _, plan, _ = plan_of(env, pq)
    nm = lines_of(plan).get("names", {}).get("default") or {}
    _, plan_p, _ = plan_of(env, pp)
    check("46 R9 public repo: the names line carries the public note, default still none",
          nm.get("value") == "none" and nm.get("text", "").endswith(
              "This repo is public \u2014 a name committed here is public.")
          and "public" not in (lines_of(plan_p).get("names", {}).get("default") or {})
          .get("text", "x public"), (nm, lines_of(plan_p).get("names")))
    # R11: the wording.
    st, plan, _ = plan_of(envl, pf)
    by = {i["key"]: i for i in st.get("items", [])}
    ex_opts = by.get("extras", {}).get("question", {}).get("options", [])
    up_opts = by.get("upkeep", {}).get("question", {}).get("options", [])
    check("46 R11 the line-endings option and the upkeep option, reworded",
          "Make line endings the same on Windows and Linux" in [o["label"] for o in ex_opts]
          and up_opts and "makes small updates to the project notes"
          in up_opts[0]["description"] and "Mind" not in up_opts[0]["description"],
          (ex_opts, up_opts))
    fresh_lines = plan.get("text", "").splitlines()
    fix_lines = plan_of(env, fx[0][2])[1].get("text", "").splitlines()
    fix_lines2 = plan_of(env, fx[1][2])[1].get("text", "").splitlines()
    check("46 R11 a fresh project's plan says 'Also sets up:', any other 'Also fixes:'",
          any(x.startswith("Also sets up:") for x in fresh_lines)
          and not any(x.startswith("Also fixes:") for x in fresh_lines)
          and any(x.startswith("Also fixes:") for x in fix_lines2)
          and not any(x.startswith("Also sets up:") for x in fix_lines2),
          (fresh_lines, fix_lines, fix_lines2))
    page = " ".join(run(env, "doc").stdout.split())
    check("46 R11 the page names every step the setup can add, and what revisit forgets",
          "a private vault adds two steps" in page
          and "typing private names or choosing Released adds one" in page
          and "the one exception" not in page
          and "every remembered answer is forgotten; answers Soul reads from the project's "
              "files stay" in page and "every answer is asked again" not in page, page[-900:])


if __name__ == "__main__":
    sys.exit(main())
