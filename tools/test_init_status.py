"""Behaviour test for tools/init-status.py (/soul-init's checklist and remembered answers).

FENCE: a recorded answer is not asked again unless the files show it no longer holds —
names listed but .soul/private-names.txt gone, a stage recorded but no **Stage:** line,
or `status --ask KEY` forces it. A repair is never
hidden by one — `hand-hooks: yes` recorded on one machine reads `repair` where the
hooks are missing, and `record: local` reads `repair` while the record is tracked.
`status` never writes; `record` keeps every line it does not own. Each run controls
PATH (git only, plus a fake `gitleaks` when the scan should be offered), sets
SOUL_INIT_NO_GH=1 so `gh` is never called (no network), and points XDG_CONFIG_HOME
at the temp dir so this machine's real vault file is never read.

Run: python3 tools/test_init_status.py  (exit 0 = PASS)
"""

import datetime
import importlib.util
import json
import os
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
          "# header\nhistory-scan:  clean {}   2026-10-23\n".format(head))
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
    base = dict(_GIT_ENV, XDG_CONFIG_HOME=os.path.join(tmp, "config"), SOUL_INIT_NO_GH="1")
    env = dict(base, PATH=bins["plain"])      # no gitleaks, no gh
    envl = dict(base, PATH=bins["leaks"])     # a gitleaks on PATH (never run by status)

    # 1 — fresh repo: one commit, no CLAUDE.md
    p1 = repo(tmp, "fresh", {"README.md": "x\n"})
    st, by = status(env, p1)
    check("fresh: fresh is true", st["fresh"] is True, st)
    check("fresh: import is a repair, not a question", by["import"]["action"] == "repair",
          by.get("import"))
    check("fresh: record, stage, names asked in one main round",
          ["record", "stage", "names"] in st["rounds"]
          and all(by[k]["question"]["group"] == "main" for k in ("record", "stage", "names")),
          st["rounds"])
    check("fresh: no layout item", "layout" not in by)
    check("fresh, no gitleaks: extras = hand-hooks + line-endings",
          by["extras"]["members"] == ["hand-hooks", "line-endings"]
          and by["history-scan"]["action"] == "none"
          and "gitleaks" in by["history-scan"]["detail"], by.get("extras"))
    check("fresh: extras members carry no question of their own",
          all(by[k]["question"] is None and by[k]["group"] == "extras"
              for k in ("hand-hooks", "line-endings")))
    check("fresh: rounds end with extras", st["rounds"][-1] == ["extras"], st["rounds"])
    q = by["extras"]["question"]
    check("extras: only the line-endings fix is recommended (hooks, scan are offers)",
          q["recommended"] is not None
          and q["options"][q["recommended"]]["key"] == "line-endings", q)
    q = by["record"]["question"]
    check("record question: fixed wording, no vault option without a vault",
          q["text"] == "Where should this project's record (its decision log and ideas) live?"
          and [o["label"] for o in q["options"]] == ["In this repo's git", "Only on this machine"]
          and q["recommended"] == 0, q)
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
          "In your Soul vault" in [o["label"] for o in by["record"]["question"]["options"]],
          by["record"]["question"])

    # 14 — the public wording (rendered directly: status itself never calls gh here)
    spec = importlib.util.spec_from_file_location("init_status", _TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    q = mod.render_question("record", public="yes", vault=None)
    check("public repo: record warns, nothing recommended",
          q["options"][0]["description"] == mod.QUESTIONS["record"]["public_description"]
          and "public, anyone can read it" in q["options"][0]["description"]
          and q["recommended"] is None, q)
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

    # 19 — unknown visibility is asked, alone, before the main round; recorded wins
    st, by = status(env, p1)
    pub = by["public"]
    check("unknown visibility: public asked in its own round before the main round",
          pub["action"] == "ask" and ["public"] in st["rounds"]
          and st["rounds"].index(["public"]) < st["rounds"].index(["record", "stage", "names"])
          and pub["question"]["text"] == "Is this repo public, or will it be?"
          and pub["question"]["options"] == mod.QUESTIONS["public"]["options"]
          and [(o["value"], o["label"]) for o in pub["question"]["options"]]
          == [("yes", "Yes"), ("no", "No")]
          and all(o["description"].startswith("nothing is written")
                  for o in pub["question"]["options"])
          and pub["question"]["recommended"] is None, (pub, st["rounds"]))
    p19 = repo(tmp, "pubrec", {"README.md": "x\n"})
    run(env, "record", p19, "public", "no")
    st, by = status(env, p19)
    check("recorded public: none, from the record, not asked", by["public"]["action"] == "none"
          and by["public"]["source"] == "recorded" and ["public"] not in st["rounds"],
          by["public"])

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
    check("--ask record with unknown visibility: public asked first",
          by.get("public", {}).get("action") == "ask" and ["public"] in st["rounds"],
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
    r = run(envv, "record", p31, "sidecar", "keep")
    asked, st, by = sidecar_asked(envv, p31)
    check("sidecar: a recorded keep is final — none, from the record", r.returncode == 0
          and not asked and by.get("sidecar", {}).get("action") == "none"
          and by["sidecar"]["source"] == "recorded" and ["sidecar"] not in st["rounds"],
          (r.stderr, by.get("sidecar")))
    r = run(envv, "record", p31, "sidecar", "maybe")
    check("sidecar: an unknown value is refused", r.returncode == 2, r.stderr)
    run(envv, "revisit", p31, "sidecar")
    asked, _, by = sidecar_asked(envv, p31)
    check("sidecar: revisit asks again", asked, by.get("sidecar"))

    shutil.rmtree(tmp, ignore_errors=True)
    print("\n{} failure(s)".format(len(FAILS)) if FAILS else "\nALL PASS")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
