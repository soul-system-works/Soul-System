"""Behaviour test for the roles table loader in tools/dispatch.py (SOUL-I080).

FENCE: the roles table says which harness and model does each job, so a wrong merge
sends work to the wrong model without a word. A project that names a role replaces
EVERY global row of that role (never a mix of the two); with no row anywhere the
built-in default applies, and its Codex reviewer only when `codex` is on PATH; a
role's rows form its ladder, ordered by rung (row order when no rung is given); a
malformed row, an unknown harness, or two rows of one role on the same rung stops
the load with an error that names the file, the line and the row (both rows, for
a shared rung).

Run: python3 tools/test_roles.py  (exit 0 = PASS)
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

_TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dispatch.py")
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else "  — " + str(detail)))
    if not ok:
        FAILS.append(name)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def table(*rows):
    return ("# Roles\n\nSome prose the loader ignores.\n\n"
            "| role | harness | model | settings |\n|---|---|---|---|\n"
            + "".join(r + "\n" for r in rows))


def roles(home, project, path_dirs, *extra):
    env = dict(os.environ, HOME=home, PATH=os.pathsep.join(path_dirs))
    return subprocess.run([sys.executable, _TOOL, "roles", "--project", project, "--json",
                           *extra], capture_output=True, text=True, env=env)


def rows_of(r):
    try:
        return json.loads(r.stdout)
    except ValueError:
        return None


def brief(rows):
    """(role, harness, model, rung, source) per row, in the order the tool gave."""
    return [(x["role"], x["harness"], x["model"], x["rung"], x["source"]) for x in rows or []]


def main():
    tmp = tempfile.mkdtemp(prefix="soul-roles-test-")
    home = os.path.join(tmp, "home")
    project = os.path.join(tmp, "proj")
    os.makedirs(home)
    os.makedirs(project)
    nopath = os.path.join(tmp, "empty-bin")
    os.makedirs(nopath)
    withcodex = os.path.join(tmp, "codex-bin")
    os.makedirs(withcodex)
    fake = os.path.join(withcodex, "codex")
    write(fake, "#!/bin/sh\nexit 0\n")
    os.chmod(fake, 0o755)
    global_file = os.path.join(home, ".claude", "soul-roles.md")
    project_file = os.path.join(project, ".claude", "soul-roles.md")

    # 1 — built-in default, no file anywhere; codex reviewer only when codex is on PATH
    r = roles(home, project, [nopath])
    got = brief(rows_of(r))
    check("default without codex on PATH", r.returncode == 0 and got == [
        ("implementer", "claude", "sonnet", 1, "built-in"),
        ("implementer", "claude", "opus", 2, "built-in"),
        ("reviewer", "claude", "opus", 1, "built-in")], r.stdout + r.stderr)
    r = roles(home, project, [withcodex])
    got = brief(rows_of(r))
    check("default with codex on PATH adds the codex reviewer", r.returncode == 0 and got == [
        ("implementer", "claude", "sonnet", 1, "built-in"),
        ("implementer", "claude", "opus", 2, "built-in"),
        ("reviewer", "claude", "opus", 1, "built-in"),
        ("reviewer", "codex", "default", 2, "built-in")], r.stdout + r.stderr)
    rows = rows_of(r) or [{}]
    check("default rows carry n=1 and the 1800 s timeout",
          all(x.get("n") == 1 and x.get("timeout") == 1800 for x in rows), r.stdout)

    # 2 — global rows replace the built-in for their role only
    write(global_file, table("| implementer | claude-ollama | qwen3.8:27b-q8_0 | n=3 timeout=600 |",
                             "| implementer | claude | opus |  |",
                             "| tester | codex | default | |"))
    r = roles(home, project, [nopath])
    rows = rows_of(r)
    got = brief(rows)
    check("global rows replace the built-in role; other roles keep the built-in",
          r.returncode == 0 and got == [
              ("implementer", "claude-ollama", "qwen3.8:27b-q8_0", 1, "global"),
              ("implementer", "claude", "opus", 2, "global"),
              ("reviewer", "claude", "opus", 1, "built-in"),
              ("tester", "codex", "default", 1, "global")], r.stdout + r.stderr)
    check("settings parsed (n, timeout), defaults filled",
          rows and rows[0]["n"] == 3 and rows[0]["timeout"] == 600
          and rows[1]["n"] == 1 and rows[1]["timeout"] == 1800, r.stdout)

    # 3 — a project row for a role replaces ALL global rows of that role
    write(project_file, table("| implementer | codex | gpt-5.4 | rung=1 |"))
    r = roles(home, project, [nopath])
    got = brief(rows_of(r))
    check("project replaces every global row of the role, keeps the others",
          r.returncode == 0 and got == [
              ("implementer", "codex", "gpt-5.4", 1, "project"),
              ("reviewer", "claude", "opus", 1, "built-in"),
              ("tester", "codex", "default", 1, "global")], r.stdout + r.stderr)

    # 4 — ladder order: by rung, row order when no rung is given
    write(project_file, table("| implementer | claude | opus | rung=3 |",
                              "| implementer | claude | sonnet | rung=1 |",
                              "| implementer | claude-ollama | qwen3.8:27b-q8_0 | rung=2 |",
                              "| reviewer | claude | opus | |",
                              "| reviewer | codex | default | |"))
    r = roles(home, project, [nopath])
    got = brief(rows_of(r))
    check("ladder ordered by rung", r.returncode == 0 and got[:3] == [
        ("implementer", "claude", "sonnet", 1, "project"),
        ("implementer", "claude-ollama", "qwen3.8:27b-q8_0", 2, "project"),
        ("implementer", "claude", "opus", 3, "project")], r.stdout + r.stderr)
    check("no rung: row order", got[3:5] == [
        ("reviewer", "claude", "opus", 1, "project"),
        ("reviewer", "codex", "default", 2, "project")], str(got))

    # 5 — the human view names each row's source
    env = dict(os.environ, HOME=home, PATH=nopath)
    r = subprocess.run([sys.executable, _TOOL, "roles", "--project", project],
                       capture_output=True, text=True, env=env)
    check("text view lists rows with their source", r.returncode == 0
          and "claude-ollama" in r.stdout and "project" in r.stdout
          and "global" in r.stdout, r.stdout + r.stderr)

    # 6 — errors name the file, line and row
    cases = [
        ("unknown harness", "| implementer | gemini | pro | |", "gemini"),
        ("too few cells", "| implementer | claude |", "implementer | claude"),
        ("blank model", "| implementer | claude |  | |", "model"),
        ("setting not key=value", "| implementer | claude | opus | fresh |", "fresh"),
        ("unknown setting", "| implementer | claude | opus | temp=0.2 |", "temp"),
        ("non-integer rung", "| implementer | claude | opus | rung=two |", "rung"),
        ("n below 1", "| implementer | claude | opus | n=0 |", "n"),
        ("claude-ollama needs an exact model", "| implementer | claude-ollama | default | |",
         "claude-ollama"),
    ]
    for name, row, word in cases:
        write(project_file, table("| reviewer | claude | opus | |", row))
        r = roles(home, project, [nopath])
        msg = r.stderr
        check("error: " + name, r.returncode == 2 and project_file in msg
              and ":8:" in msg and row.strip() in msg and word in msg, msg + r.stdout)
    # 6b — two rows of one role on the same rung: an error naming both rows
    first = "| implementer | claude | sonnet | |"
    second = "| implementer | claude | opus | rung=1 |"
    write(project_file, table("| reviewer | claude | opus | |", first, second))
    r = roles(home, project, [nopath])
    check("error: duplicate rung names both rows", r.returncode == 2
          and project_file in r.stderr and first in r.stderr and second in r.stderr
          and ":8" in r.stderr and ":9" in r.stderr and "rung 1" in r.stderr,
          r.stderr + r.stdout)
    write(project_file, table("| implementer | claude | sonnet | |",
                              "| reviewer | claude | opus | rung=1 |"))
    r = roles(home, project, [nopath])
    check("the same rung in two different roles is fine", r.returncode == 0, r.stderr)

    write(global_file, table("| implementer | claude | opus | bogus |"))
    os.remove(project_file)
    r = roles(home, project, [nopath])
    check("error in the global file names the global file",
          r.returncode == 2 and global_file in r.stderr and "bogus" in r.stderr, r.stderr)

    # workflows: built-ins, then files; a project file replaces a global one; a file
    # may not take a built-in's name or an unusable one
    def flow(name, desc):
        return "---\nname: {}\ndescription: {}\n---\n\n1. Step.\n".format(name, desc)
    gdir = os.path.join(home, ".claude", "soul-workflows")
    pdir = os.path.join(project, ".claude", "soul-workflows")
    write(os.path.join(gdir, "quick-fix.md"), flow("quick-fix", "GLOBAL quick fix"))
    write(os.path.join(gdir, "second-look.md"), flow("second-look", "a second look"))
    write(os.path.join(pdir, "quick-fix.md"), flow("quick-fix", "PROJECT quick fix"))
    write(os.path.join(pdir, "review.md"), flow("review", "shadow"))
    write(os.path.join(pdir, "Bad Name.md"), flow("x", "bad"))
    write(os.path.join(pdir, "bare.md"), "1. Step without frontmatter.\n")
    r = subprocess.run([sys.executable, _TOOL, "workflows", "--project", project, "--json"],
                       capture_output=True, text=True, env=dict(os.environ, HOME=home))
    try:
        wf = {w["name"]: w for w in json.loads(r.stdout)}
    except ValueError:
        wf = {}
    check("workflows: the two built-ins listed first",
          [w for w in wf][:2] == ["build-verify", "review"]
          and wf["build-verify"]["source"] == "built-in", r.stdout + r.stderr)
    check("workflows: a project file replaces a global one of the same name",
          wf.get("quick-fix", {}).get("description") == "PROJECT quick fix"
          and wf["quick-fix"]["source"] == "project", wf.get("quick-fix"))
    check("workflows: a global file with no project twin is listed",
          wf.get("second-look", {}).get("source") == "global", wf.get("second-look"))
    named_review = [w for w in json.loads(r.stdout or "[]") if w["name"] == "review"]
    check("workflows: a file may not take a built-in's name",
          [w["source"] for w in named_review] == ["built-in", "project"]
          and named_review[1]["note"].startswith("ignored: a built-in"), named_review)
    check("workflows: an unusable name and a missing description are marked",
          "ignored" in wf.get("Bad Name", {}).get("note", "")
          and wf.get("bare", {}).get("note") == "no description: line", r.stdout)

    workflow_roles(home, project, nopath, gdir, pdir, global_file, project_file)

    shutil.rmtree(tmp, ignore_errors=True)
    print("\n{} failure(s)".format(len(FAILS)) if FAILS else "\nALL PASS")
    return 1 if FAILS else 0


def line_of(path, text):
    """The 1-based line of `path` that holds `text`."""
    with open(path, encoding="utf-8") as f:
        return next(i for i, l in enumerate(f, 1) if text in l)


def workflow_roles(home, project, nopath, gdir, pdir, global_file, project_file):
    """A workflow file's `## Roles` section over the shared table, per role."""
    def flow(name, *rows, before="", after=""):
        return ("---\nname: {}\ndescription: d\n---\n\n# {}\n\n1. Step.\n\n{}"
                "## Roles\n\n| role | harness | model | settings |\n|---|---|---|---|\n{}\n"
                "{}## Notes\n\n| reviewer | gemini | not-read | |\n"
                .format(name, name, before, "".join(r + "\n" for r in rows), after))
    write(global_file, table("| implementer | claude | sonnet | |",
                             "| reviewer | claude | opus | |"))
    write(project_file, table("| reviewer | claude | opus | |",
                              "| reviewer | codex | default | |"))
    quick = os.path.join(pdir, "quick-fix.md")
    codex_row = "| reviewer | codex | gpt-5.4 | timeout=900 |"
    write(quick, flow("quick-fix", codex_row))
    write(os.path.join(gdir, "quick-fix.md"),
          flow("quick-fix", "| tester | claude | haiku | |"))
    second = os.path.join(gdir, "second-look.md")
    write(second, flow("second-look", "| implementer | claude | opus | |",
                       "| reviewer | claude | opus | |"))
    write(os.path.join(pdir, "review.md"), flow("review", "| reviewer | codex | shadow | |"))
    write(os.path.join(pdir, "Bad Name.md"), flow("x", "| reviewer | codex | bad | |"))
    shared = roles(home, project, [nopath])
    check("workflow roles: the shared table loads", shared.returncode == 0, shared.stderr)

    r = roles(home, project, [nopath], "--workflow", "quick-fix")
    rows = rows_of(r) or []
    got = brief(rows)
    check("workflow roles: the file's role replaces every row of that role below it",
          r.returncode == 0 and [x for x in got if x[0] == "reviewer"] == [
              ("reviewer", "codex", "gpt-5.4", 1, "workflow")], r.stdout + r.stderr)
    check("workflow roles: a role the file does not name falls through unchanged",
          [x for x in got if x[0] == "implementer"] == [
              ("implementer", "claude", "sonnet", 1, "global")], got)
    wrow = [x for x in rows if x["source"] == "workflow"]
    check("workflow roles: --json gives the file and line, and the row's settings",
          len(wrow) == 1 and wrow[0]["where"] == "{}:{}".format(quick, line_of(quick, codex_row))
          and wrow[0]["timeout"] == 900, wrow)
    check("workflow roles: a table outside the ## Roles section is not read",
          bool(got) and not any(x[2] == "not-read" for x in got), got)
    check("workflow roles: the project's quick-fix.md replaces the global one, its "
          "Roles section too", bool(got) and not any(x[0] == "tester" for x in got), got)
    r = roles(home, project, [nopath], "--workflow", "second-look")
    rows = rows_of(r) or []
    check("workflow roles: a global workflow file's section is used when no project twin",
          r.returncode == 0 and brief(rows) == [
              ("implementer", "claude", "opus", 1, "workflow"),
              ("reviewer", "claude", "opus", 1, "workflow")]
          and all(x["where"].startswith(second + ":") for x in rows), r.stdout + r.stderr)
    env = dict(os.environ, HOME=home, PATH=nopath)
    r = subprocess.run([sys.executable, _TOOL, "roles", "--project", project,
                        "--workflow", "quick-fix"], capture_output=True, text=True, env=env)
    check("workflow roles: the text view names the workflow file and line as source",
          r.returncode == 0
          and "workflow ({}:{})".format(quick, line_of(quick, codex_row)) in r.stdout
          and "global ({}:".format(global_file) in r.stdout, r.stdout + r.stderr)

    for name in ("build-verify", "review"):
        r = roles(home, project, [nopath], "--workflow", name)
        check("workflow roles: built-in {} selects the shared table, unchanged".format(name),
              r.returncode == 0 and rows_of(r) == rows_of(shared), r.stdout + r.stderr)
    r = roles(home, project, [nopath], "--workflow", "no-such-flow")
    check("workflow roles: an unknown workflow is a usage error naming it",
          r.returncode == 2 and "no workflow named 'no-such-flow'" in r.stderr
          and not r.stdout, r.stderr)
    r = roles(home, project, [nopath], "--workflow", "Bad Name")
    check("workflow roles: a workflow the listing marks ignored is refused, with why",
          r.returncode == 2 and "ignored" in r.stderr and "lower-case" in r.stderr, r.stderr)

    bad = "| reviewer | gemini | pro | |"
    write(quick, flow("quick-fix", "| reviewer | claude | opus | |", bad))
    r = roles(home, project, [nopath], "--workflow", "quick-fix")
    check("workflow roles: a malformed row names the workflow file, line and row",
          r.returncode == 2 and "{}:{}:".format(quick, line_of(quick, bad)) in r.stderr
          and bad in r.stderr and "gemini" in r.stderr, r.stderr)
    r = roles(home, project, [nopath])
    check("workflow roles: without --workflow a broken workflow section changes nothing",
          r.returncode == 0 and rows_of(r) == rows_of(shared), r.stderr)
    first, second_row = "| reviewer | claude | opus | |", "| reviewer | codex | default | rung=1 |"
    write(quick, flow("quick-fix", first, second_row))
    r = roles(home, project, [nopath], "--workflow", "quick-fix")
    check("workflow roles: two rows on one rung inside the section name both",
          r.returncode == 2 and quick in r.stderr and first in r.stderr
          and second_row in r.stderr and "rung 1" in r.stderr, r.stderr)

    # A commented-out or fenced example is not a table; the template ships one commented
    write(quick, flow("quick-fix", before="```\n## Roles\n| reviewer | codex | fenced | |\n```\n\n"))
    r = roles(home, project, [nopath], "--workflow", "quick-fix")
    check("workflow roles: an empty section and a fenced example change nothing",
          r.returncode == 0 and rows_of(r) == rows_of(shared), r.stdout + r.stderr)
    template = os.path.join(os.path.dirname(_TOOL), "..", "skills", "soul-workflow",
                            "templates", "quick-fix.md")
    with open(template, encoding="utf-8") as f:
        text = f.read()
    write(quick, text)
    r = roles(home, project, [nopath], "--workflow", "quick-fix")
    check("template: its commented-out ## Roles example changes nothing",
          r.returncode == 0 and rows_of(r) == rows_of(shared) and "## Roles" in text,
          r.stdout + r.stderr)
    write(quick, text.replace("<!--", "").replace("-->", ""))
    r = roles(home, project, [nopath], "--workflow", "quick-fix")
    got = brief(rows_of(r))
    check("template: uncommented, its example makes Codex the only reviewer",
          r.returncode == 0 and [x[:3] for x in got if x[0] == "reviewer"] == [
              ("reviewer", "codex", "default")]
          and [x[4] for x in got if x[0] == "implementer"] == ["global"],
          r.stdout + r.stderr)


def test_fence():
    assert main() == 0


if __name__ == "__main__":
    sys.exit(main())
