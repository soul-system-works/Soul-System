"""Behaviour test for tools/layout-cleanup.py (the `.ai/` working-file offer).

FENCE: the scan must never flag code, tests, user docs, ADRs, README or the record
stores, and apply must never change a class-1 file except to repoint a link — and
must REPORT every such link, since project content linking into `.ai/` is the
owner's call to resolve. A fixture repo with misplaced files exercises the lot.

Run: python3 tools/test_layout_cleanup.py  (exit 0 = PASS)
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile

_TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "layout-cleanup.py")
_GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
                GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
                GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")

FILES = {
    "PLAN.md": "# Plan\nSee [feature](docs/plans/feature-x.md).\n",
    "docs/plans/feature-x.md": "# Feature X\nBuilt on the [guide](../guide.md).\n",
    "docs/review-2026-10-01.md": "# Review\n",
    ".soul/witness.md": "# Witness\n",
    ".soul/old-notes-review.md": "# old notes\n",
    ".soul/experiments/run1.md": "# run 1\n",
    "docs/guide.md": "# Guide\n",
    "docs/adr/0001-plan-format.md": "# ADR 1: plan format\n",
    "docs/specs/handoff-design.md": "# Spec: the handoff skill\n",
    "src/plan.py": "PLAN = 1\n",
    "tests/test_review.py": "def test_review():\n    pass\n",
    "README.md": "# Project\nThe [feature plan](docs/plans/feature-x.md) is current.\n",
}
UNTRACKED = {"scratch/notes.txt": "scratch\n"}
NON_CANDIDATES = ("docs/guide.md", "docs/specs/handoff-design.md", "docs/adr/0001-plan-format.md", "src/plan.py",
                  "tests/test_review.py", ".soul/witness.md")
EXPECTED = {
    "PLAN.md": ("plans", "name rule"),
    "docs/plans/feature-x.md": ("plans", "folder rule"),
    "docs/review-2026-10-01.md": ("reviews", "name rule"),
    "scratch/notes.txt": ("scratch", "folder rule"),
    ".soul/old-notes-review.md": ("old-soul-files", ".soul/"),
    ".soul/experiments": ("old-soul-files", ".soul/"),
}
PLAN = {
    "PLAN.md": "move",
    "docs/plans/feature-x.md": "move",
    "scratch/notes.txt": "move",
    ".soul/experiments": "move",
    "docs/review-2026-10-01.md": "content",
    ".soul/old-notes-review.md": "leave",
}


def run(*args):
    return subprocess.run([sys.executable, _TOOL] + list(args),
                          capture_output=True, text=True)


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args), capture_output=True,
                          text=True, env=_GIT_ENV)


def fixture(tmp, name):
    repo = os.path.join(tmp, name)
    for path, text in list(FILES.items()) + list(UNTRACKED.items()):
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(text)
    git(repo, "init", "-q")
    git(repo, "add", *FILES)
    git(repo, "commit", "-q", "-m", "fixture")
    return repo


EDGE_README = (b"# Project\r\n[p](<docs/plans/feature x.md#x>) and `[c](docs/plans/feature-y.md)`\r\n"
               b"\r\n[q]: docs/plans/feature-y.md#sec\r\n")
EDGE_README_AFTER = (b"# Project\r\n[p](<.ai/plans/feature x.md#x>) and `[c](docs/plans/feature-y.md)`\r\n"
                     b"\r\n[q]: .ai/plans/feature-y.md#sec\r\n")
OUTSIDE_LINKED = b"[f](plans/feature-y.md)\n"
EDGE_PLAN = {"PLAN.md": "move", "docs/plans/feature x.md": "move",
             "docs/plans/feature-y.md": "move"}


def edge_fixture(tmp):
    """Symlinks pointing out of the project, odd link syntax, a CRLF file."""
    repo = os.path.join(tmp, "edge")
    files = {
        "README.md": EDGE_README,
        "PLAN.md": b"[outside](../outside.md) [gone](../missing.md)\n",
        "docs/plans/feature x.md": b"# x\n",
        "docs/plans/feature-y.md": b"# y\n",
    }
    outside = {"outside.md": b"# outside\n", "outside-review.md": b"# not ours\n",
               "outside-linked.md": OUTSIDE_LINKED}
    for path, data in list(files.items()):
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "wb").write(data)
    for path, data in outside.items():
        open(os.path.join(tmp, path), "wb").write(data)
    os.makedirs(os.path.join(tmp, "outdir"))
    os.makedirs(os.path.join(repo, ".soul"))
    os.symlink(os.path.join(tmp, "outside-review.md"), os.path.join(repo, "review-ext.md"))
    os.symlink(os.path.join(tmp, "outside-linked.md"), os.path.join(repo, "docs", "linked.md"))
    os.symlink(os.path.join(tmp, "outdir"), os.path.join(repo, ".soul", "extdir"))
    git(repo, "init", "-q")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "edge fixture")
    return repo


def tree_hash(repo, skip=()):
    h = hashlib.sha256()
    for dirpath, dirs, files in os.walk(repo):
        dirs[:] = sorted(d for d in dirs if d != ".git")
        for f in sorted(files):
            p = os.path.relpath(os.path.join(dirpath, f), repo)
            if p in skip:
                continue
            h.update(p.encode() + b"\0" + open(os.path.join(dirpath, f), "rb").read())
    status = git(repo, "status", "--porcelain", "-uall").stdout.splitlines()
    h.update("\n".join(l for l in status if not any(s in l for s in skip)).encode())
    return h.hexdigest()


def read(repo, path):
    return open(os.path.join(repo, path), encoding="utf-8").read()


def main():
    results = []

    def check(name, ok, detail=""):
        results.append(ok)
        print("{}  {}{}".format("ok  " if ok else "FAIL", name, "" if ok else " — " + detail))

    with tempfile.TemporaryDirectory() as tmp:
        repo = fixture(tmp, "main")
        before = {p: read(repo, p) for p in NON_CANDIDATES}

        # 1. scan finds exactly the expected candidates, each with its reason.
        cands = json.loads(run("scan", repo, "--json").stdout)["candidates"]
        got = {c["path"]: c for c in cands}
        check("scan finds exactly the expected candidates", set(got) == set(EXPECTED),
              "got {}".format(sorted(got)))
        check("each candidate carries its group and reason", all(
            p in got and got[p]["group"] == g and r in got[p]["reason"]
            for p, (g, r) in EXPECTED.items()), json.dumps(cands))
        check("targets are .ai/<group>/<name>", all(
            c["target"] == ".ai/{}/{}".format(c["group"], os.path.basename(c["path"]))
            for c in cands))
        check("no non-candidate flagged (code, tests, ADR, guide, README, store)",
              not set(got) & set(NON_CANDIDATES + ("README.md",)))
        check("text scan groups and prints reasons",
              "plans (2)" in run("scan", repo).stdout and "why:" in run("scan", repo).stdout)

        plan_file = os.path.join(tmp, "plan.json")
        with open(plan_file, "w") as fh:
            json.dump(PLAN, fh)

        # 2. apply.
        out = run("apply", repo, "--plan", plan_file)
        check("apply exits 0", out.returncode == 0, out.stderr)
        status = git(repo, "status", "--porcelain").stdout.splitlines()
        renames = [l for l in status if l.startswith("R")]
        check("tracked moves are git renames",
              any("PLAN.md -> .ai/plans/PLAN.md" in l for l in renames)
              and any("docs/plans/feature-x.md -> .ai/plans/feature-x.md" in l for l in renames)
              and any(".soul/experiments/run1.md -> .ai/old-soul-files/experiments/run1.md" in l
                      for l in renames), "\n".join(status))
        check("untracked file moved plainly",
              os.path.exists(os.path.join(repo, ".ai/scratch/notes.txt"))
              and not os.path.exists(os.path.join(repo, "scratch/notes.txt")))
        check(".ai/README.md created", os.path.exists(os.path.join(repo, ".ai/README.md")))
        check("README link repointed into .ai/",
              "(.ai/plans/feature-x.md)" in read(repo, "README.md"), read(repo, "README.md"))
        check("README link fix reported",
              "project content now links into .ai/: README.md -> .ai/plans/feature-x.md"
              in out.stdout, out.stdout)
        check("moved file's own outbound link repointed",
              "(../../docs/guide.md)" in read(repo, ".ai/plans/feature-x.md"))
        check("moved-to-moved link repointed",
              "(feature-x.md)" in read(repo, ".ai/plans/PLAN.md"))
        check("non-candidates byte-identical",
              all(read(repo, p) == t for p, t in before.items()))
        check("content/leave files stay put",
              os.path.exists(os.path.join(repo, "docs/review-2026-10-01.md"))
              and os.path.exists(os.path.join(repo, ".soul/old-notes-review.md")))
        layout = json.loads(read(repo, ".soul/layout.json"))["decisions"]
        check("leave and content remembered with dates",
              layout.get("docs/review-2026-10-01.md", {}).get("decision") == "content"
              and layout.get(".soul/old-notes-review.md", {}).get("decision") == "leave"
              and all("date" in v for v in layout.values()), json.dumps(layout))

        # 3. second scan: nothing new. Second apply: idempotent.
        check("second scan reports nothing",
              run("scan", repo).stdout.startswith("no layout candidates"))
        h = tree_hash(repo)
        out2 = run("apply", repo, "--plan", plan_file)
        check("second apply changes nothing", out2.returncode == 0 and tree_hash(repo) == h,
              out2.stdout + out2.stderr)

        # 4. decline, then scan: nothing; only layout.json changed.
        repo2 = fixture(tmp, "declined")
        h = tree_hash(repo2)
        run("decline", repo2)
        check("decline then scan reports nothing",
              run("scan", repo2).stdout.startswith("no layout candidates"))
        check("decline changes nothing but .soul/layout.json",
              tree_hash(repo2, skip={os.path.join(".soul", "layout.json")}) == h)
        check("decline recorded every candidate as leave",
              set(json.loads(read(repo2, ".soul/layout.json"))["decisions"]) == set(EXPECTED))

        # 5. apply --dry-run changes nothing.
        repo3 = fixture(tmp, "dry")
        h = tree_hash(repo3)
        out3 = run("apply", repo3, "--plan", plan_file, "--dry-run")
        check("dry run changes nothing", tree_hash(repo3) == h and out3.returncode == 0)
        check("dry run reports the link it would repoint",
              "project content now links into .ai/: README.md" in out3.stdout, out3.stdout)

        # 6. Edge cases from fresh-context review (each failed before its fix).
        edge = edge_fixture(tmp)
        cands = {c["path"] for c in json.loads(run("scan", edge, "--json").stdout)["candidates"]}
        check("symlinks are never flagged (file or folder)",
              cands == set(EDGE_PLAN), "got {}".format(sorted(cands)))
        with open(os.path.join(tmp, "edge-plan.json"), "w") as fh:
            json.dump(EDGE_PLAN, fh)
        out = run("apply", edge, "--plan", os.path.join(tmp, "edge-plan.json"))
        check("edge apply exits 0", out.returncode == 0, out.stderr)
        check("link fixing never writes through a symlink to outside the project",
              open(os.path.join(tmp, "outside-linked.md"), "rb").read() == OUTSIDE_LINKED
              and os.path.islink(os.path.join(edge, "docs", "linked.md")))
        readme = open(os.path.join(edge, "README.md"), "rb").read()
        check("<...> destination with a space repointed, anchor kept",
              b"[p](<.ai/plans/feature x.md#x>)" in readme, readme.decode())
        check("reference-style definition repointed, anchor kept",
              b"[q]: .ai/plans/feature-y.md#sec" in readme, readme.decode())
        check("inline code span left alone",
              b"`[c](docs/plans/feature-y.md)`" in readme, readme.decode())
        check("CRLF file changed only at the repointed links", readme == EDGE_README_AFTER,
              repr(readme))
        plan_md = open(os.path.join(edge, ".ai", "plans", "PLAN.md"), "rb").read()
        check("moved file's link outside the project repointed from its new home",
              b"[outside](../../../outside.md)" in plan_md, plan_md.decode())
        check("moved file's unresolvable link reported, left as written",
              b"[gone](../missing.md)" in plan_md
              and "../missing.md" in out.stdout and "PLAN.md" in out.stdout, out.stdout)

    n = len(results)
    if all(results):
        print("PASS  {}/{} — scan is conservative, apply moves and reports, re-runs are no-ops"
              .format(n, n))
        return 0
    print("FAIL  {}/{} passed".format(sum(results), n))
    return 1


if __name__ == "__main__":
    sys.exit(main())
