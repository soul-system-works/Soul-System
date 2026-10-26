"""Behaviour test for tools/init-status.py (/soul-init's checklist and remembered answers).

FENCE: a recorded answer is never asked again, and a repair is never hidden by one —
`hand-hooks: yes` recorded on one machine reads `repair` where the hooks are missing.
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
    check("extras: every check is an offer, none recommended",
          by["extras"]["question"]["recommended"] is None, by["extras"]["question"])
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
    write(os.path.join(p2, "src.py"), "x = 1\n")
    git(p2, "add", "src.py")
    git(p2, "commit", "-qm", "work")
    st, by = status(envl, p2)
    asks = sorted(k for k, a in actions(by).items() if a != "none")
    check("after a new commit: only history-scan asks",
          asks == ["extras", "history-scan"] and st["rounds"] == [["extras"]]
          and by["extras"]["members"] == ["history-scan"], (asks, st["rounds"]))
    check("history-scan detail names the new commit", "1 new commit" in by["history-scan"]["detail"],
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
    p8b = repo(tmp, "brokenlink", {"README.md": "x\n"})
    os.symlink(os.path.join(tmp, "nowhere"), os.path.join(p8b, ".soul"))
    r = run(env, "record", p8b, "names", "none")
    check("a broken .soul link: record refuses, exit 2", r.returncode == 2
          and not os.path.exists(os.path.join(tmp, "nowhere")), r.stderr)
    st, by = status(env, p8b)
    check("a broken .soul link: vault-link repair", by.get("vault-link", {}).get("action")
          == "repair", by.get("vault-link"))

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
          q["options"][0]["description"] == "public: anyone can read it"
          and q["recommended"] is None, q)
    q = mod.render_question("names", public="yes")
    check("public repo: names question says so",
          q["text"].endswith(" This repo is public — a name committed here is public."), q)

    shutil.rmtree(tmp, ignore_errors=True)
    print("\n{} failure(s)".format(len(FAILS)) if FAILS else "\nALL PASS")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
