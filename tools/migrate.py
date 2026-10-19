#!/usr/bin/env python3
"""Pack a project into one verified zip on the old computer; place it on the new one.

A git clone carries only what was pushed. Moving computers loses the rest: local
branches and the newest stash, uncommitted edits, untracked inputs, gitignored
records (witness.md, .soul/, .ai/) and the project's Claude memory folder, which
lives outside the repo. /soul-migrate (docs/specs/2026-10-19-soul-migrate.md) drives
this helper; the helper does the mechanical parts and keeps the two ideas the pilot
proved load-bearing: every member is hashed and checked on arrival, and placement
never overwrites anything.

  inventory <project> [--json]                     read-only: what a move would carry
  pack <project> --out DIR --selection FILE        write <name>-<UTC stamp>.zip into DIR
  verify <zip> [--sha256 HEX]                      every member against manifest.json
  place <zip> <dest> [--apply]                     preview, or clone + restore into dest
  place-memory <zip> --key=KEY [--apply]           memory/ into <projects>/KEY/memory
  memory-key <path>                                the guessed memory-folder key

The selection FILE is what the owner approved (fields: `pack --help`). Pack never
takes credential-like paths (unless named in include_credential_like), the rebuildable
folders inventory reported (unless include_rebuildable), or anything under the output
folder or .ai/migrate-out/, whatever the selection says. Pack refuses a shallow clone,
and checks its own zip before reporting it: the same verify, the bundle cloned, both
patches applied to that clone (index.patch the staged changes, worktree.patch the rest),
and the same placement planning place runs. Tracked files marked skip-worktree or
assume-unchanged travel with their working-tree content and get the flag back on
arrival. Only the executable bit of a file mode travels (drvfs reports 0777 for
everything).

The memory folder is found by the "cwd" recorded in the transcripts under
~/.claude/projects/*/, never by decoding a folder name — hyphenated paths decode
wrongly. Claude Code cleans transcripts up while memory/ stays, so with no cwd match
the folder named by the path's key is taken instead, marked unconfirmed. The key is a
guess: every character that is not a letter or digit becomes "-", inferred from the
folders observed on one machine (17 with a recorded cwd fit it; a path with "_" was
encoded "-"); "." and spaces were not observed, and the older "/"-only guess is tried
too. The skill confirms by opening a session in the new path. When more than one
candidate holds memory/, pack stops and lists them; the selection's "memory_key" picks
one. Keys start with "-"; --key KEY and --key=KEY both work. $CLAUDE_CONFIG_DIR
relocates ~/.claude and $CLAUDE_PROJECTS_DIR its projects folder (the tests set both
so the real ~/.claude is never touched).

Exit codes: 0 ok, 1 a check failed (mismatch, conflict, refusal), 2 usage error.
POSIX only (Linux, macOS, WSL): paths are handled as "/"-separated and symlinks
are recreated as such. On Windows the tool refuses to run (exit 2).
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.parse
import zipfile
from datetime import datetime, timezone

OUT_DEFAULT = ".ai/migrate-out"
CRED = re.compile(r"(?i)^(\.env(\..*)?|.*\.env|\.envrc|\.netrc|\.npmrc|\.pypirc|\.pgpass|\.htpasswd"
                  r"|\.mcp\.json|\.ssh|auth\.json|service-account.*\.json"
                  r"|id_(rsa|dsa|ecdsa|ed25519)(\.pub)?|id_\w+_sk(\.pub)?"
                  r"|.*\.(pem|key|p12|pfx|keystore|jks|kdbx|tfvars|ppk|p8)|.*\.tfstate.*"
                  r"|.*(credential|secret|password|api[_-]?key).*"
                  r"|(.*[._-])?tokens?([._-].*)?)$")
# Names that are only credential-like with their folder; settings.local.json may hold
# tokens inside permission allow rules.
CRED_PATH = re.compile(r"(?i)(^|/)(\.kube/config|\.docker/config\.json|\.claude/settings\.local\.json)$")
# Folder name -> how it comes back: "npm"/"venv" from the lock or requirements file,
# "build" by the project's own build, None regenerates on use, else the command itself.
REBUILD = {"node_modules": "npm", ".venv": "venv", "venv": "venv", "__pycache__": None,
           ".pytest_cache": None, ".mypy_cache": None, ".tox": None, "dist": "build",
           "build": "build", ".next": "build", ".nuxt": "build", ".gradle": "build",
           "target": "build", ".terraform": "terraform init", ".cache": None, "coverage": None}
SHELL_WORDS = {"cd", "echo", "export", "set", "true", "false", "exit", "test", "[", "if",
               "then", "else", "fi", "for", "do", "done", "while", "env", "exec"}
# Optional locks off: inventory is read-only and must not rewrite the index. Smudge
# skipped: a clone or checkout must never need the LFS server.
GIT_ENV = {"GIT_OPTIONAL_LOCKS": "0", "GIT_LFS_SKIP_SMUDGE": "1"}
FLAGS = ("skip-worktree", "assume-unchanged")
PATCHES = ("index.patch", "worktree.patch")  # HEAD -> index, then index -> working tree
# Every flag pinned: a patch must not depend on the owner's diff config.
DIFF = ("diff", "--binary", "--no-ext-diff", "--no-textconv", "--no-color", "--submodule=short",
        "--src-prefix=a/", "--dst-prefix=b/")
OPS = ("MERGE_HEAD", "CHERRY_PICK_HEAD", "rebase-merge", "rebase-apply")
EXCLUDE = "git-info-exclude"  # the member carrying .git/info/exclude


class Stop(Exception):
    """A check failed: report it and exit 1."""


class Usage(Exception):
    """Bad arguments: report and exit 2."""


def git(cwd, *args, check=True, raw=False):
    r = subprocess.run(["git", "-C", cwd, *args], capture_output=True,
                       env=dict(os.environ, **GIT_ENV))
    if check and r.returncode:
        raise Stop("git {} failed: {}".format(" ".join(args),
                                              r.stderr.decode(errors="replace").strip()))
    return r.stdout if raw else r.stdout.decode(errors="surrogateescape")


def is_exec(f):
    """Executable bit of an open file. A Windows-mounted disk (drvfs) reports 0777 for
    every file, so there the bit means nothing: trust it only with a `#!` line."""
    mode = os.fstat(f.fileno()).st_mode & 0o777
    if mode != 0o777:
        return bool(mode & 0o111)
    head = f.read(2)
    f.seek(0)
    return head == b"#!"


def digest(f, out=None):
    """(sha256, bytes) of an open binary stream, copied to out when given."""
    h, n = hashlib.sha256(), 0
    for block in iter(lambda: f.read(1 << 20), b""):
        h.update(block)
        n += len(block)
        if out:
            out.write(block)
    return h.hexdigest(), n


def file_sha(path):
    with open(path, "rb") as f:
        return digest(f)[0]


def claude_path(*parts):
    base = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")
    return os.path.join(base, *parts)


def projects_dir():
    return os.environ.get("CLAUDE_PROJECTS_DIR") or claude_path("projects")


def rel_ok(rel):
    # No absolute paths, no traversal, never into a .git directory.
    return bool(rel) and "\x00" not in rel and all(
        p not in ("", ".", "..", ".git") for p in rel.split("/"))


def under(rel, root):
    rel, root = rel.rstrip("/"), root.rstrip("/")
    return rel == root or rel.startswith(root + "/")


def is_credential(rel):
    rel = rel.strip("/")
    return bool(CRED_PATH.search(rel)) or any(CRED.match(p) for p in rel.split("/"))


def strip_userinfo(url):
    """(url without an embedded user:password@, whether one was removed; None when
    urlsplit cannot parse it). An ssh login name with no password (ssh://git@host/x) is
    not a secret and stays; scp-style git@host:path has no netloc and stays as is."""
    try:
        p = urllib.parse.urlsplit(url)
        if "@" not in p.netloc or (p.password is None and "ssh" in p.scheme):
            return url, False
    except ValueError:
        return url, None
    return urllib.parse.urlunsplit(p._replace(netloc=p.netloc.rsplit("@", 1)[1])), True


def rebuild_group(rel, is_dir=False):
    """The rebuildable folder containing rel (outermost wins), or None."""
    parts = rel.strip("/").split("/")
    for i, p in enumerate(parts if is_dir or rel.endswith("/") else parts[:-1]):
        if p in REBUILD:
            return "/".join(parts[:i + 1])
    return None


def rebuild_cmd(project, group):
    name, parent = group.split("/")[-1], os.path.dirname(group)
    kind, has = REBUILD[name], lambda n: os.path.exists(os.path.join(project, parent, n))
    if kind is None:
        return "none needed (recreated on use)"
    if kind == "build":
        return "rebuilt by the project's build"
    cmd = ("npm ci" if has("package-lock.json") else "yarn install --frozen-lockfile"
           if has("yarn.lock") else "pnpm install --frozen-lockfile" if has("pnpm-lock.yaml")
           else "npm install") if kind == "npm" else \
        "python3 -m venv {0} && {0}/bin/pip install ".format(name) + (
            "-r requirements.txt" if has("requirements.txt") else "-e ." if has("pyproject.toml")
            else "<packages: no requirements.txt or pyproject.toml found>") if kind == "venv" \
        else kind
    return "cd {} && {}".format(parent, cmd) if parent else cmd


def walk_files(path, skipped=None):
    """Every file and symlink under path, relative; symlinked folders not followed. A .git
    folder or .git file (a linked worktree's or submodule's pointer) and an unreadable
    folder are skipped, and named in skipped ({rel: why}) when a dict is given."""
    def unreadable(e):
        if skipped is not None:
            skipped[os.path.normpath(os.path.relpath(e.filename, path))] = "folder not readable"
    for d, dirs, files in os.walk(path, onerror=unreadable):
        links = [x for x in dirs if os.path.islink(os.path.join(d, x))]
        dirs[:] = [x for x in dirs if x != ".git" and x not in links]
        for f in files + links:
            rel = os.path.relpath(os.path.join(d, f), path)
            if f != ".git":
                yield rel
            elif skipped is not None:
                skipped[rel] = "git link file (nested repo or worktree)"


def unpackable(path, rel):
    """Why the file at path cannot travel, or None: a zip member name must be UTF-8, and
    reading a FIFO, socket or device would hang or mean nothing."""
    try:
        rel.encode("utf-8")
        mode = os.lstat(path).st_mode
    except UnicodeEncodeError:
        return "name is not valid UTF-8"
    except OSError:
        return "not on disk"
    if stat.S_ISREG(mode):
        return None if os.access(path, os.R_OK) else "not readable"
    return None if stat.S_ISLNK(mode) else "not a regular file"


def leaves(root, path):
    """Why a symlink at path pointing outside root cannot travel, or None."""
    return "symlink leaves the project" if os.path.islink(path) and \
        escapes(root, path, os.readlink(path)) else None


def memory_keys(path):
    """Guessed folder names, likeliest first (see the docstring for how sure)."""
    p = os.path.abspath(path)
    return list(dict.fromkeys([re.sub(r"[^A-Za-z0-9]", "-", p), p.replace("/", "-")]))


def memory_key(path):
    return memory_keys(path)[0]


def recorded_cwds(log):
    out = set()
    with open(log, errors="replace") as f:
        for _, line in zip(range(200), f):
            try:
                out.add(json.loads(line).get("cwd"))
            except (ValueError, AttributeError, TypeError):
                continue
    return out - {None}


def find_memory(project):
    """Memory-folder candidates, cwd matches first: a folder whose 3 newest transcripts
    record cwd == project, then the folders named by memory_keys(project) whose
    transcripts (if any are left) record no other cwd."""
    want, base, found = {os.path.abspath(project), os.path.realpath(project)}, projects_dir(), []
    keys = sorted(os.listdir(base)) if os.path.isdir(base) else []
    seen = {}
    for key in keys:
        folder = os.path.join(base, key)
        logs = sorted((os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".jsonl")),
                      key=os.path.getmtime, reverse=True)[:3] if os.path.isdir(folder) else []
        seen[key] = set().union(*(recorded_cwds(x) for x in logs))
        found += [{"key": key, "matched_by": "cwd"}] if seen[key] & want else []
    for name in memory_keys(project):
        if name in keys and os.path.isdir(os.path.join(base, name)) and not seen[name]:
            found.append({"key": name, "matched_by": "name"})
    for m in found:
        m["path"] = os.path.join(base, m["key"])
        m["has_memory"] = os.path.isdir(os.path.join(m["path"], "memory"))
    return sorted(found, key=lambda m: (m["matched_by"] != "cwd", not m["has_memory"]))


def pick_memory(candidates, sel):
    """The one memory folder to pack: the selection's memory_key, else the only candidate
    holding memory/. Two or more and no memory_key: stop rather than guess."""
    want, held = sel.get("memory_key"), [m for m in candidates if m["has_memory"]]
    if want is False:
        return None
    if want:
        if not rel_ok(want) or "/" in want:
            raise Usage("memory_key must be a single folder name")
        m = next((m for m in candidates if m["key"] == want), None) or {
            "key": want, "matched_by": "selection", "path": os.path.join(projects_dir(), want)}
        if not os.path.isdir(os.path.join(m["path"], "memory")):
            raise Stop("memory_key {} has no memory/ folder".format(want))
        return dict(m, has_memory=True)
    if len(held) > 1:
        raise Stop("more than one memory folder could be this project's; name one as "
                   "\"memory_key\" in the selection:\n  " + "\n  ".join(
                       "{} ({})".format(m["key"], m["matched_by"]) for m in held))
    return held[0] if held else None


def nested_repos(project, rel):
    """Folders at or below rel holding a .git dir or file: pack skips their history."""
    out = []
    for d, dirs, files in os.walk(os.path.join(project, rel)):
        if ".git" in dirs or ".git" in files:
            out.append(os.path.relpath(d, project))
        dirs[:] = [x for x in dirs if x != ".git"]
    return out


def read_json(path, field):
    try:
        with open(path, encoding="utf-8") as f:
            return dict(json.load(f).get(field) or {})
    except (OSError, ValueError, AttributeError, TypeError):
        return {}


def dependencies(project):
    """Names only, best effort: enabled plugins, project agent config, tools scripts call."""
    plugins = read_json(claude_path("settings.json"), "enabledPlugins")
    local = sorted(os.path.join(top, f) for top in (".claude", ".codex")
                   for f in walk_files(os.path.join(project, top)))
    lines = [v for v in read_json(os.path.join(project, "package.json"), "scripts").values()
             if isinstance(v, str)]
    try:
        with open(os.path.join(project, "Makefile"), errors="replace") as f:
            lines += [ln for ln in f if ln.startswith("\t")]
    except OSError:
        pass
    tools = set()
    for seg in (s for line in lines for s in re.split(r"&&|\|\||;|\|", line)):
        words = seg.strip().lstrip("@-").split()
        while words and re.match(r"^\w+=", words[0]):
            words = words[1:]  # VAR=value prefixes
        if words and not words[0].startswith(("$", "(")) and words[0] not in SHELL_WORDS:
            tools.add(words[0])
    return {"plugins": sorted(k for k, v in plugins.items() if v is True),
            "project_local": local[:50], "tools": sorted(tools)}


def git_state(project):
    head = git(project, "rev-parse", "--verify", "-q", "HEAD", check=False).strip()
    if not head:
        raise Stop("the repository has no commits; commit first")
    fmt = "--format=%(refname:short)%00%(upstream:remotename)%00%(upstream:remoteref)" \
          "%00%(upstream:track)"
    branches = [dict(zip(("name", "remote", "merge", "track"), (x or None for x in row.split("\0"))))
                for row in git(project, "for-each-ref", "refs/heads", fmt).splitlines()]
    for b in branches:
        ahead = re.search(r"ahead (\d+)", b["track"] or "")
        b["ahead"] = int(ahead.group(1)) if ahead else 0
    found = {"url": {}, "pushurl": {}, "promisor": {}}  # config, not `remote -v`: no suffixes
    for row in git(project, "config", "-z", "--get-regexp", r"^remote\..*\.(url|pushurl|promisor)$",
                   check=False).split("\0"):
        if row:
            key, value = row.split("\n", 1)
            name, kind = key[len("remote."):].rsplit(".", 1)
            found[kind].setdefault(name, value)
    leaked, odd = [], []
    for kind in ("url", "pushurl"):
        for name, url in found[kind].items():
            found[kind][name], had = strip_userinfo(url)
            leaked += [name] if had else []
            odd += [name] if had is None else []
    attrs = os.path.join(project, ".gitattributes")
    lfs = os.path.isfile(attrs) and "filter=lfs" in open(attrs, errors="replace").read()
    lfs = lfs or bool(shutil.which("git-lfs") and git(project, "lfs", "ls-files", "-n",
                                                       check=False).strip())
    wts = [ln[9:] for ln in git(project, "worktree", "list", "--porcelain").splitlines()
           if ln.startswith("worktree ")]
    return {"head": head, "branches": branches, "remotes": found["url"],
            "pushurls": found["pushurl"], "partial": sorted(n for n, v in found["promisor"].items()
                                         if v.lower() in ("true", "yes", "on", "1")),
            "remote_credentials": sorted(set(leaked)), "remote_unparsed": sorted(set(odd)),
            "in_progress": [op for op, p in zip(OPS, git(project, "rev-parse", *(
                x for op in OPS for x in ("--git-path", op))).splitlines())
                if os.path.lexists(os.path.join(project, p))], "lfs": lfs, "commits": int(git(project, "rev-list", "--all", "--count").strip()),
            "shallow": git(project, "rev-parse", "--is-shallow-repository").strip() == "true",
            "branch": git(project, "symbolic-ref", "-q", "--short", "HEAD", check=False).strip()
            or None, "no_upstream": [b["name"] for b in branches if not b["remote"]],
            "stashes": len(git(project, "stash", "list").splitlines()),
            "worktrees": [w for w in wts if os.path.realpath(w) != os.path.realpath(project)],
            "submodules": [ln.strip() for ln in
                           git(project, "submodule", "status", check=False).splitlines()]}


def inside(rel, dirs):
    """True when a folder above rel is itself listed in dirs (in "a/" form)."""
    parts = rel.rstrip("/").split("/")
    return any("/".join(parts[:i]) + "/" in dirs for i in range(1, len(parts)))


def inventory(project):
    project = os.path.abspath(project)
    top = git(project, "rev-parse", "--show-toplevel", check=False).strip()
    if not top or os.path.realpath(top) != os.path.realpath(project):
        raise Usage("not a git repository root: " + project)
    g = git_state(project)
    creds = ["remote {} had an embedded credential (removed)".format(n)
             for n in g["remote_credentials"]] + \
        ["remote {} could not be parsed — check it for credentials by hand".format(n)
         for n in g["remote_unparsed"]]
    rebuild, groups, nested, unreadable = {}, {}, [], {}
    others = ["ls-files", "-z", "--others", "--exclude-standard", "--directory",
              "--no-empty-directory"]
    listed = [(p, "untracked") for p in git(project, *others).split("\0") if p] + \
        [(p, "ignored") for p in git(project, *others, "--ignored").split("\0") if p]
    dirs = {p for p, _ in listed if p.endswith("/")}
    for rel, kind in listed:
        if under(rel, OUT_DEFAULT) or inside(rel, dirs):
            continue  # the packer's own output folder, or counted with the folder above it
        path = os.path.join(project, rel)
        is_dir = os.path.isdir(path) and not os.path.islink(path)
        skipped = {}
        files = [f for f in (os.path.join(rel, x) for x in walk_files(path, skipped))
                 if not under(f, OUT_DEFAULT)] if is_dir else [rel]
        unreadable.update((os.path.normpath(os.path.join(rel, x)), why)
                          for x, why in skipped.items() if why == "folder not readable")
        unreadable.update((f, "not readable") for f in files
                          if unpackable(os.path.join(project, f), f) == "not readable")
        sizes = {f: os.lstat(os.path.join(project, f)).st_size for f in files}
        cls = "credential" if is_credential(rel) else \
            "rebuildable" if rebuild_group(rel, is_dir) else "normal"
        if cls == "credential":
            creds.append(rel)
        else:  # rebuildable folders anywhere inside get their own group; pack drops only those
            for f, n in sizes.items():
                group = rebuild_group(f)
                if group:
                    rebuild[group] = rebuild.get(group, 0) + n
                elif is_credential(f):
                    creds.append(f)  # reported here; pack drops them per file
            nested += nested_repos(project, rel) if is_dir and cls == "normal" else []
        top_group = rel.split("/")[0] + ("/" if "/" in rel else "")
        s = groups.setdefault(top_group, {"path": top_group, "bytes": 0, "count": 0, "sample": []})
        s["bytes"], s["count"] = s["bytes"] + sum(sizes.values()), s["count"] + len(files)
        if len(s["sample"]) < 20:
            s["sample"].append({"path": rel, "git": kind, "bytes": sum(sizes.values()),
                                "class": cls})
    worktrees = {os.path.realpath(w) for w in g["worktrees"]}
    flagged = [{"path": row[2:], "flag": FLAGS[0] if row[0] in "Ss" else FLAGS[1]}
               for row in git(project, "ls-files", "-v", "-z").split("\0")
               if row[:1] and (row[0] == "S" or row[0].islower())
               and os.path.lexists(os.path.join(project, row[2:]))]
    dirty = [ln[3:] for ln in git(project, "status", "--porcelain=v1",
                                  "--untracked-files=no").splitlines()]
    creds += [f["path"] for f in flagged if is_credential(f["path"])] + [
        d + "  (tracked file with uncommitted changes — the change travels in the patch)"
        for d in dirty if is_credential(d)]
    return {"project": project, "name": os.path.basename(project), "git": g,
            "soul_project": any(os.path.isfile(os.path.join(project, s))
                                for s in ("witness.md", ".soul/witness.md")),
            "dirty": dirty, "flagged": flagged, "unreadable": unreadable,
            "groups": [groups[k] for k in sorted(groups)],
            "credentials": sorted(creds), "memory": find_memory(project),
            "nested_repos": sorted(n for n in nested
                                   if os.path.realpath(os.path.join(project, n)) not in worktrees),
            "rebuildable": [{"path": k, "bytes": b, "rebuild": rebuild_cmd(project, k)}
                            for k, b in sorted(rebuild.items())],
            "dependencies": dependencies(project)}


def upstream(b):
    if not b["remote"]:
        return "  no upstream set (may not be pushed)"
    return " (upstream {}/{}){}".format(b["remote"], (b["merge"] or "")[len("refs/heads/"):],
                                       "  has upstream but {} commits not pushed".format(
                                           b["ahead"]) if b.get("ahead") else "")


NESTED = "nested repo {} — its history is not carried; migrate it separately"
LINKED = "linked worktree {} (its history is in the bundle; its uncommitted files are not carried)"
LFS = "LFS objects are not packed; after arrival run `git lfs pull` — objects never pushed " \
      "to the LFS server are unrecoverable"
UNCONFIRMED = "  (found by folder name — unconfirmed; confirm on arrival)"
NOT_CARRIED = [".git/hooks (copy any local hooks by hand)",
               "local .git/config settings (only remotes, push URLs and upstreams are restored)",
               "refs outside heads/tags/stash, refs/notes among them (objects arrive but nothing "
               "points to them)", "remote-tracking refs (run `git fetch`)", "reflogs",
               ".git/info/attributes", "sparse-checkout settings",
               ".git/git-crypt keys (export them separately)",
               "intent-to-add marks (`git add -N`): the file arrives untracked",
               "folders git cannot open (it skips them with a warning; fix their permissions "
               "and pack again)", "empty folders", "file timestamps"]
INPROGRESS = "{} present: operation in progress — finish or abort it first; its state is not carried"


def print_inventory(inv):
    g = inv["git"]
    rows = [("project", inv["project"] + ("  (Soul project)" if inv["soul_project"] else
                                          "  (not a Soul project)")),
            ("HEAD", "{} on {}".format(g["head"][:12], g["branch"] or "(detached)")),
            ("commits", "{} across all refs".format(g["commits"]))]
    rows += [("warning", "shallow clone - pack refuses it; run `git fetch --unshallow`")] \
        if g["shallow"] else []
    rows += [("warning", "partial clone (remote.{}.promisor is set)".format(n)) for n in g["partial"]]
    rows += [("warning", INPROGRESS.format(op)) for op in g["in_progress"]]
    rows += [("branch", b["name"] + upstream(b)) for b in g["branches"]]
    rows += [("remote", "{}  {}".format(n, u)) for n, u in g["remotes"].items()]
    rows += [("remote", "{}  {}  (push)".format(n, u)) for n, u in g["pushurls"].items()]
    rows += [("stashes", str(g["stashes"]) + ("  (a bundle carries only the newest)"
                                              if g["stashes"] > 1 else ""))]
    rows += [("worktree", LINKED.format(w)) for w in g["worktrees"]]
    rows += [("submodule", s + "  (not carried)") for s in g["submodules"]]
    rows += [("LFS", LFS)] if g["lfs"] else []
    rows += [("dirty", d) for d in inv["dirty"]]
    rows += [("flagged", "{}  ({}; its working-tree content is carried)".format(f["path"], f["flag"]))
             for f in inv["flagged"]]
    rows += [("files", "{:<32} {:>14,} B  {} files".format(s["path"], s["bytes"], s["count"]))
             for s in inv["groups"]]
    rows += [("rebuild", "{:<32} {:>14,} B  {}".format(r["path"], r["bytes"], r["rebuild"]))
             for r in inv["rebuildable"]]
    rows += [("secrets", "names only; never packed unless approved by name")] \
        if inv["credentials"] else []
    rows += [("secret", c) for c in inv["credentials"]]
    rows += [("skipped", "{}  ({}; never packed)".format(r, why))
             for r, why in sorted(inv["unreadable"].items())]
    rows += [("warning", NESTED.format(n)) for n in inv["nested_repos"]]
    rows += [("memory", m["key"] + ("  memory/ present" if m["has_memory"] else "  no memory/")
              + (UNCONFIRMED if m["matched_by"] == "name" else ""))
             for m in inv["memory"]] or [("memory", "(no folder found)")]
    rows += [("needs", "{}: {}".format(k, ", ".join(v)))
             for k, v in inv["dependencies"].items() if v]
    for label, text in rows:
        print("{:<10} {}".format(label, text))


def out_ok(project, out):
    """Out may not be inside the project, except the packer's own .ai/migrate-out."""
    p, o = os.path.realpath(project), os.path.realpath(out)
    return not (o == p or o.startswith(p + os.sep)) or o == os.path.join(p, OUT_DEFAULT)


def escapes(root, link, text):
    """True when a symlink at link with this text points outside root."""
    resolved = os.path.normpath(os.path.join(os.path.dirname(link), text))
    return os.path.isabs(text) or not resolved.startswith(root.rstrip("/") + "/")


def why_out(project, rel, sel, out, rebuildable):
    """Why the file at rel stays home whatever the selection says, or None to pack it.
    rebuildable: the folders inventory reported, the only ones dropped as rebuildable."""
    p = os.path.join(project, rel)
    forced = [os.path.normpath(x) for x in sel.get("include_credential_like") or []]
    skip = {os.path.relpath(os.path.realpath(out), os.path.realpath(project)), OUT_DEFAULT}
    return ("credential-like" if is_credential(rel) and not any(under(rel, x) for x in forced)
            else "rebuildable" if any(under(rel, r) for r in rebuildable)
            and not sel.get("include_rebuildable")
            else "output folder" if any(under(rel, s) for s in skip)
            else unpackable(p, rel) or leaves(project, p))


def select_files(project, selection, out, rebuildable):
    """The approved selection (untracked plus every include_credential_like entry)
    expanded to {rel: None (pack it) or why it is left out}."""
    tracked = set(git(project, "ls-files", "-z").split("\0"))
    chosen = {}
    for item in (selection.get("untracked") or []) + (selection.get("include_credential_like") or []):
        rel = os.path.normpath(item)  # not stripped: " x" and "x" are different files
        if not rel_ok(rel):
            raise Usage("unsafe selection path: " + item)
        path, skipped = os.path.join(project, rel), {}
        if not os.path.lexists(path):
            raise Stop("selected path not found: " + item)
        found = [os.path.join(rel, f) for f in walk_files(path, skipped)] \
            if os.path.isdir(path) and not os.path.islink(path) else [rel]
        chosen.update((os.path.normpath(os.path.join(rel, x)), why) for x, why in skipped.items())
        for f in found:
            chosen[f] = "tracked" if f in tracked else why_out(project, f, selection, out, rebuildable)
    return chosen


def left_out(chosen):
    """What the selection named but pack dropped, as "rel (why)": tracked paths are not
    dropped (the bundle has them), rebuildable files collapse to their folder."""
    out = {(rebuild_group(r) or r) if why == "rebuildable" else r: why
           for r, why in chosen.items() if why not in (None, "tracked")}
    return sorted("{} ({})".format(r, why) for r, why in out.items())


_strs = lambda v: isinstance(v, list) and all(isinstance(x, str) for x in v)  # noqa: E731
SELECTION = {"untracked": _strs, "include_rebuildable": lambda v: isinstance(v, bool),
             "include_credential_like": _strs,
             "memory_key": lambda v: isinstance(v, str) or v is False,
             "smoke": lambda v: isinstance(v, str), "notes": lambda v: isinstance(v, str)}
SELECTION_HELP = """selection file: a JSON object, every field optional
  untracked                list of paths or top-level groups to carry
  include_rebuildable      true: also carry the rebuildable folders inventory reported
  include_credential_like  list of credential-like paths the owner approved; each is carried
  memory_key               string: the memory folder to pack; false: pack no memory
  smoke                    string: the smoke-check command written into RECEIVE.md
  notes                    string: notes written into RECEIVE.md"""

RECEIVE = """# Receiving {name}

Packed {created} from `{old_path}` (HEAD `{head}`). On the new computer, with the
Soul System plugin installed, open a fresh session and run:

    /soul-migrate receive <path to {zipname}>

By hand, the same steps (stop at the first failure):

    python3 <plugin>/tools/migrate.py verify {zipname} --sha256 <hash printed at pack time>
    python3 <plugin>/tools/migrate.py place {zipname} <new project path> [--apply]
    python3 <plugin>/tools/migrate.py memory-key <new project path>
    python3 <plugin>/tools/migrate.py place-memory {zipname} --key=<key> [--apply]

Then open a session in the new path and confirm the memory loaded; if it did not,
move it to the folder that session created under ~/.claude/projects/.

## Branches
{branches}

## Remotes (run `git fetch` once the network is reachable)
{remotes}

## Left out - rebuild after placing
{rebuild}

## Credentials left behind (names only - bring them by your own means)
{creds}

## Not carried
{missing}

## Memory folder
{memory}

## Dependencies to check on this computer
{deps}

## Smoke check (run it; a skipped or failed check is not a pass)

    {smoke}

## Notes
{notes}
"""


def bullets(items):
    return "\n".join("- " + i for i in items) or "- none"


def receive_md(inv, sel, chosen, meta, zipname, mem):
    g = inv["git"]
    missing = (["{} stashes; only the newest is in the bundle".format(g["stashes"])]
               if g["stashes"] > 1 else []) \
        + [LINKED.format(w) for w in g["worktrees"]] \
        + ["submodule {} (clone it separately)".format(s) for s in g["submodules"]] \
        + ([LFS] if g["lfs"] else []) + [NESTED.format(n) for n in inv["nested_repos"]] \
        + NOT_CARRIED + left_out(chosen)
    rebuild = [] if sel.get("include_rebuildable") else \
        ["{} - `{}`".format(r["path"], r["rebuild"]) for r in inv["rebuildable"]]
    return RECEIVE.format(
        zipname=zipname, name=inv["name"], created=meta["created"], old_path=inv["project"],
        head=g["head"], remotes=bullets("{}  {}".format(n, u) for n, u in g["remotes"].items()),
        branches=bullets(b["name"] + upstream(b) for b in g["branches"]),
        rebuild=bullets(rebuild), creds=bullets(meta["credentials"]), missing=bullets(missing),
        memory="from `{}`{}; place it with place-memory".format(
            mem["key"], UNCONFIRMED if mem["matched_by"] == "name" else "")
        if mem else "none found",
        deps="\n".join("- {}: {}".format(k, ", ".join(v) or "none")
                       for k, v in inv["dependencies"].items()),
        smoke=meta["smoke"] or "(none recorded)", notes=meta["notes"] or "none")


def clone_bundle(zpath, tmp, dest, *opts):
    """Clone the package's bundle into dest: {member: extracted path} for the bundle and
    whichever patches the package holds. -o origin: the receiver's clone.defaultRemoteName
    must not rename the remote place removes."""
    with zipfile.ZipFile(zpath) as zf:
        have = [n for n in ("repo.bundle",) + PATCHES if n in zf.namelist()]
        zf.extractall(tmp, have)
    git(tmp, "clone", "-q", "-o", "origin", *opts, os.path.join(tmp, "repo.bundle"), dest)
    return {n: os.path.join(tmp, n) for n in have}


def self_check(zpath):
    """What place will rely on, checked on the finished zip: every member hashes to the
    manifest, the bundle verifies and clones, both patches apply, and place's planning
    accepts files/ and memory/ against the tracked tree the patches leave. The patches go
    to the clone's index, so no second working tree is written. Case collisions are left
    to place: they matter only on a case-insensitive destination."""
    man = verified(zpath)
    with tempfile.TemporaryDirectory(prefix="soul-migrate-") as tmp:
        clone, root = os.path.join(tmp, "clone"), os.path.join(tmp, "dest")
        got = clone_bundle(zpath, tmp, clone, "--no-checkout")
        git(clone, "bundle", "verify", "-q", got["repo.bundle"])
        git(clone, "read-tree", man["project"]["head"])
        for name in (n for n in PATCHES if n in got):
            git(clone, "apply", "--cached", "--whitespace=nowarn", got[name])
        tracked = set(git(clone, "ls-files", "-z").split("\0"))
        dirs = {"/".join(t.split("/")[:i]) for t in tracked for i in range(1, t.count("/") + 1)}
        plan_targets(zpath, root, man, "memory/", fold=False)
        problems = []
        for target, m in plan_targets(zpath, root, man, "files/", fold=False):
            rel = os.path.relpath(target, root)
            parts = rel.split("/")
            if m.get("flag") in FLAGS:
                problems += [] if rel in tracked else ["flagged file is not tracked: " + rel]
            elif rel in tracked or rel in dirs or any(
                    "/".join(parts[:i]) in tracked for i in range(1, len(parts))):
                problems.append("a tracked path is already there: " + rel)
        refuse(problems)


def pack(a):
    project = os.path.abspath(a.project)
    if not out_ok(project, a.out):
        raise Usage("--out is inside the project; use {} or a folder outside it".format(
            os.path.join(project, OUT_DEFAULT)))
    try:
        with open(a.selection, encoding="utf-8") as f:
            sel = json.load(f)
    except (OSError, ValueError) as e:
        raise Usage("cannot read --selection: {}".format(e))
    bad = [k for k, ok in SELECTION.items() if sel.get(k) is not None and not ok(sel[k])] \
        if isinstance(sel, dict) else ["the file (not a JSON object)"]
    if bad:
        raise Usage("--selection: wrong type for {} (see pack --help)".format(", ".join(bad)))
    inv = inventory(project)
    if inv["git"]["shallow"]:
        raise Stop("a shallow clone: its history is incomplete, so the bundle would be too; "
                   "run `git fetch --unshallow` first")
    mem = pick_memory(inv["memory"], sel)
    rebuildable = [r["path"] for r in inv["rebuildable"]]
    chosen = select_files(project, sel, a.out, rebuildable)
    flags = {f["path"]: f["flag"] for f in inv["flagged"]}
    chosen.update((rel, why_out(project, rel, sel, a.out, rebuildable)) for rel in flags)
    created = datetime.now(timezone.utc)
    os.makedirs(a.out, exist_ok=True)
    zpath = os.path.join(os.path.abspath(a.out), "{}-{}.zip".format(
        inv["name"], created.strftime("%Y%m%dT%H%MZ")))
    if os.path.lexists(zpath):
        raise Stop("already exists, not overwriting: " + zpath)
    forced = [os.path.normpath(x) for x in sel.get("include_credential_like") or []]
    g, members = inv["git"], []
    meta = {"name": inv["name"], "old_path": project, "head": g["head"], "branch": g["branch"],
            "branches": g["branches"], "remotes": g["remotes"], "pushurls": g["pushurls"],
            "memory_key": mem and mem["key"],
            "memory_matched_by": mem and mem["matched_by"],
            "created": created.isoformat(timespec="seconds"), "rebuild": inv["rebuildable"],
            "credentials": [c for c in inv["credentials"] if not any(under(c, x) for x in forced)],
            "dependencies": inv["dependencies"],
            "smoke": sel.get("smoke") or "", "notes": sel.get("notes") or ""}
    try:
        with tempfile.TemporaryDirectory(prefix="soul-migrate-") as tmp, \
                zipfile.ZipFile(zpath + ".part", "w", zipfile.ZIP_DEFLATED) as zf:
            def add(arc, path=None, data=None, **extra):
                entry = dict(path=arc, **extra)
                if path and os.path.islink(path):
                    data, entry["symlink"] = os.fsencode(os.readlink(path)), True
                elif path:  # hash the bytes as they are written, not a second read
                    with open(path, "rb") as f, zf.open(arc, "w", force_zip64=True) as out:
                        entry["exec"] = is_exec(f)
                        entry["sha256"], entry["bytes"] = digest(f, out)
                if data is not None:
                    zf.writestr(arc, data)
                    entry["sha256"], entry["bytes"] = hashlib.sha256(data).hexdigest(), len(data)
                members.append(entry)
            bundle = os.path.join(tmp, "repo.bundle")
            git(project, "bundle", "create", "-q", bundle, "--all")
            git(project, "bundle", "verify", "-q", bundle)
            add("repo.bundle", bundle)
            for name, opts in zip(PATCHES, (["--cached"], [])):
                patch = git(project, *DIFF, *opts, raw=True)
                if patch:
                    add(name, data=patch)
            exclude = os.path.join(project, git(project, "rev-parse", "--git-path",
                                                "info/exclude").strip())
            if os.path.isfile(exclude) and any(ln.strip() and not ln.startswith("#")
                                               for ln in open(exclude, errors="replace")):
                add(EXCLUDE, exclude)
            for rel in sorted(r for r, why in chosen.items() if why is None):
                add("files/" + rel, os.path.join(project, rel),
                    **({"flag": flags[rel]} if rel in flags else {}))
            if mem:
                root, skipped = os.path.join(mem["path"], "memory"), {}
                for rel in walk_files(root, skipped):
                    path = os.path.join(root, rel)
                    why = unpackable(path, rel) or leaves(root, path)
                    if why:
                        chosen["memory/" + rel] = why
                    else:
                        add("memory/" + rel, path)
                chosen.update(("memory/" + r, why) for r, why in skipped.items())
            add("RECEIVE.md", data=receive_md(inv, sel, chosen, meta, os.path.basename(zpath),
                                              mem).encode(errors="replace"))  # odd names
            zf.writestr("manifest.json", json.dumps(
                {"schema": 1, "project": meta, "members": members}, indent=2))
        os.replace(zpath + ".part", zpath)
        self_check(zpath)
    except Exception:
        if os.path.lexists(zpath):
            os.remove(zpath)  # a zip that failed its own check must not look carryable
        raise
    finally:
        if os.path.lexists(zpath + ".part"):
            os.remove(zpath + ".part")  # never leave a half-written zip that looks carryable
    skipped = left_out(chosen)
    print("packed {} members{}".format(len(members), "; left out: " + ", ".join(skipped)
                                       if skipped else ""))
    print("checked members hash, bundle clones, patches apply, place's planning accepts it")
    print("zip     " + zpath)
    print("sha256  " + file_sha(zpath))
    return 0


def verified(zpath, want=None):
    """The manifest, once every member hashes to it; else Stop with every problem."""
    problems = []
    if want and file_sha(zpath) != want.strip().lower():
        problems.append("zip sha256 does not match the carried hash")
    try:
        with zipfile.ZipFile(zpath) as zf:
            names = zf.namelist()
            man = json.loads(zf.read("manifest.json"))
            listed = {m["path"]: m for m in man["members"]}
            if len(names) != len(set(names)):
                problems.append("duplicate member names in the zip")
            problems += ["not in manifest: " + n for n in names
                         if n != "manifest.json" and n not in listed]
            for path, m in listed.items():
                if not rel_ok(path) or path not in names:
                    problems.append(("missing: " if rel_ok(path) else "unsafe path: ") + path)
                    continue
                try:
                    with zf.open(path) as f:
                        if digest(f) != (m.get("sha256"), m.get("bytes")):
                            problems.append("hash mismatch: " + path)
                except zipfile.BadZipFile as e:
                    problems.append("corrupt: {} ({})".format(path, e))
    except (OSError, zipfile.BadZipFile, KeyError, ValueError, TypeError) as e:
        problems.append("not a readable package: {}".format(e))
    refuse(problems, "verify failed")
    return man


def refuse(problems, what="placement refused"):
    if problems:
        raise Stop(what + ":\n  " + "\n  ".join(problems))


def case_insensitive(path):
    """True when the disk path will be on folds case: a temp file made in its nearest
    existing parent is found again by its upper-cased name."""
    d = os.path.dirname(os.path.abspath(path))
    while not os.path.isdir(d):
        d = os.path.dirname(d)
    with tempfile.NamedTemporaryFile(prefix="soul-case-", dir=d) as f:
        return os.path.exists(os.path.join(d, os.path.basename(f.name).upper()))


def plan_targets(zpath, dest, man, prefix, fold=True):
    """(target, member) pairs for one prefix, refused on what is wrong before touching dest:
    case collisions among the planned paths when fold (a case-insensitive disk would merge
    them), a file that is also a planned folder, and symlinks that leave dest."""
    plan, problems, folded, files, parents = [], [], {}, set(), set()
    with zipfile.ZipFile(zpath) as zf:
        for m in (m for m in man["members"] if m["path"].startswith(prefix)):
            rel = m["path"][len(prefix):]
            parts = rel.split("/")
            prefixes = ["/".join(parts[:i]) for i in range(1, len(parts) + 1)]
            files.add(rel)
            parents.update(prefixes[:-1])
            for p in prefixes if fold else []:
                prior = folded.setdefault(p.casefold(), p)
                if prior != p:
                    problems.append("case collision: {} / {}".format(prior, p))
            target = os.path.join(dest, rel)
            if m.get("symlink"):
                text = os.fsdecode(zf.read(m["path"]))
                if escapes(dest, target, text):
                    problems.append("symlink escapes the project: {} -> {}".format(rel, text))
            plan.append((target, m))
    problems += ["a planned file is also a planned folder: " + p for p in sorted(files & parents)]
    refuse(sorted(set(problems)))
    return plan


def on_disk_conflicts(dest, plan, fold):
    """What is already under dest: anything at a target, a parent that is a symlink or a
    file (a write would go through it), a name that differs only in case when fold."""
    problems = []
    for target, _ in plan:
        rel = os.path.relpath(target, dest).split("/")
        for i in range(1, len(rel) + 1):
            c = os.path.join(dest, *rel[:i])
            parent, name = os.path.dirname(c), rel[i - 1]
            if fold and os.path.isdir(parent) and any(x != name and x.casefold() == name.casefold()
                                             for x in os.listdir(parent)):
                problems.append("case conflict at " + c)
            if i < len(rel) and (os.path.islink(c) or os.path.lexists(c) and not os.path.isdir(c)):
                problems.append("parent is a symlink or a file: " + c)
        if os.path.lexists(target):
            problems.append("exists, not overwriting: " + target)
    return sorted(set(problems))


def write_members(zpath, plan):
    umask = os.umask(0)
    os.umask(umask)
    with zipfile.ZipFile(zpath) as zf:
        for target, m in plan:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            if m.get("flag") in FLAGS and os.path.lexists(target):
                os.remove(target)  # the clone's own copy of a flagged tracked file; place checked
            if m.get("symlink"):
                os.symlink(os.fsdecode(zf.read(m["path"])), target)
                continue
            # O_EXCL: no overwrite even if something appeared after the check. Streamed: a
            # member may not fit in memory.
            with zf.open(m["path"]) as src, os.fdopen(
                    os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), "wb") as f:
                shutil.copyfileobj(src, f, 1 << 20)
            os.chmod(target, (0o755 if m.get("exec") else 0o644) & ~umask)


def place(a):
    man = verified(a.zip)
    dest, meta = os.path.abspath(a.dest), man["project"]
    if os.path.lexists(dest) and (os.path.islink(dest) or not os.path.isdir(dest)
                                  or os.listdir(dest)):
        raise Stop("destination exists and is not empty: " + dest)
    names, fold = {m["path"] for m in man["members"]}, case_insensitive(dest)
    print("{} {} -> {}".format("APPLY" if a.apply else "PREVIEW", a.zip, dest))
    print("  clone the bundle; branches: " + ", ".join(b["name"] for b in meta["branches"]))
    for n, u in meta["remotes"].items():
        print("  remote {} -> {}".format(n, u))
    for n in PATCHES:
        print("  {}: {}".format(n, "apply" if n in names else "none"))
    print("  .git/info/exclude: " + ("append the carried lines" if EXCLUDE in names else "none"))
    plan = plan_targets(a.zip, dest, man, "files/", fold)
    for target, m in plan:
        print("  file   " + target + ("  (replaces the clone's copy; {})".format(m["flag"])
                                      if m.get("flag") in FLAGS else ""))
    if not a.apply:
        print("preview only; conflicts with the cloned tree are checked before any file is written")
        return 0
    with tempfile.TemporaryDirectory(prefix="soul-migrate-") as tmp:
        got = clone_bundle(a.zip, tmp, dest)
        bundle = got["repo.bundle"]
        have = set(git(dest, "for-each-ref", "--format=%(refname:short)", "refs/heads").split())
        for b in meta["branches"]:
            if b["name"] not in have:
                git(dest, "branch", "-q", "--no-track", b["name"], "origin/" + b["name"])
        git(dest, "checkout", "-q", *([meta["branch"]] if meta["branch"]
                                      else ["--detach", meta["head"]]))
        if "refs/stash" in git(dest, "bundle", "list-heads", bundle):  # clone skips the stash
            git(dest, "fetch", "-q", bundle, "refs/stash")
            git(dest, "stash", "store", "-m", "migrated stash",
                git(dest, "rev-parse", "FETCH_HEAD").strip())
        git(dest, "remote", "remove", "origin")  # the bundle path; the recorded URLs replace it
        for n, u in meta["remotes"].items():
            git(dest, "remote", "add", n, u)
        for n, u in meta.get("pushurls", {}).items():
            git(dest, "config", "remote.{}.pushurl".format(n), u)
        for b in meta["branches"]:
            if b["remote"] in meta["remotes"]:  # config, not --set-upstream-to: nothing fetched yet
                git(dest, "config", "branch.{}.remote".format(b["name"]), b["remote"])
                git(dest, "config", "branch.{}.merge".format(b["name"]), b["merge"])
        for name, opts in zip(PATCHES, (["--index"], [])):  # staged, then the rest
            if name in got:
                git(dest, "apply", *opts, "--whitespace=nowarn", got[name])
    if EXCLUDE in names:
        exclude = os.path.join(dest, git(dest, "rev-parse", "--git-path", "info/exclude").strip())
        os.makedirs(os.path.dirname(exclude), exist_ok=True)
        with zipfile.ZipFile(a.zip) as zf, open(exclude, "ab") as f:
            f.write(b"\n# carried by /soul-migrate\n" + zf.read(EXCLUDE))
    tracked = set(git(dest, "ls-files", "-z").split("\0"))
    flagged = [(t, m) for t, m in plan if m.get("flag") in FLAGS]
    refuse(on_disk_conflicts(dest, [p for p in plan if p[1].get("flag") not in FLAGS], fold)
           + ["flagged file is not tracked in the clone: " + t for t, _ in flagged
              if os.path.relpath(t, dest) not in tracked],
           "files/ not restored (the clone stays for review)")
    write_members(a.zip, plan)
    for target, m in flagged:
        git(dest, "update-index", "--" + m["flag"], "--", os.path.relpath(target, dest))
    print("placed: {} branches, {} files{}".format(len(meta["branches"]), len(plan), "".join(
        ", {} applied".format(n) for n in PATCHES if n in names)))
    print("next: memory-key {}, place-memory, rebuild, smoke check (RECEIVE.md)".format(dest))
    return 0


def place_memory(a):
    man = verified(a.zip)
    if not rel_ok(a.key) or "/" in a.key:
        raise Usage("--key must be a single folder name")
    dest = os.path.join(projects_dir(), a.key, "memory")
    plan = plan_targets(a.zip, dest, man, "memory/", case_insensitive(dest))
    if not plan:
        print("no memory/ in this package; nothing to place")
        return 0
    if os.path.lexists(dest):
        raise Stop("memory folder already exists, not overwriting: " + dest)
    print("{} {} files -> {}".format("APPLY" if a.apply else "PREVIEW", len(plan), dest))
    if a.apply:
        write_members(a.zip, plan)
        print("placed; open a session in the new path and confirm the memory loaded")
    return 0


def main(argv=None):
    if os.name == "nt":
        print("error: migrate is POSIX-only (Linux, macOS, WSL)", file=sys.stderr)
        return 2
    # File names and remote URLs can hold anything; a narrow console encoding must not
    # crash the report.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(errors="replace")
            except Exception:
                pass
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, args in (("inventory", ["project", "--json"]),
                       ("pack", ["project", "--out", "--selection"]),
                       ("verify", ["zip", "--sha256"]), ("place", ["zip", "dest", "--apply"]),
                       ("place-memory", ["zip", "--key", "--apply"]), ("memory-key", ["path"])):
        s = sub.add_parser(name, epilog=SELECTION_HELP if name == "pack" else None,
                           formatter_class=argparse.RawDescriptionHelpFormatter)
        for arg in args:
            s.add_argument(arg, **({"action": "store_true"} if arg in ("--json", "--apply") else
                                   {"required": True} if arg in ("--out", "--selection", "--key")
                                   else {}))
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--key" in argv[:-1]:  # keys start with "-", which argparse would read as an option
        i = argv.index("--key")
        argv[i:i + 2] = ["--key=" + argv[i + 1]]
    a = ap.parse_args(argv)
    try:
        if a.cmd == "inventory":
            inv = inventory(a.project)
            if a.json:
                print(json.dumps(inv, indent=2))
            else:
                print_inventory(inv)
        elif a.cmd == "memory-key":
            print(memory_key(a.path))
        elif a.cmd == "verify":
            man = verified(a.zip, a.sha256)
            print("verified {} members of {}".format(len(man["members"]), a.zip))
        else:
            return {"pack": pack, "place": place, "place-memory": place_memory}[a.cmd](a)
        return 0
    except Usage as e:
        print("error: {}".format(e), file=sys.stderr)
        return 2
    except (Stop, OSError) as e:
        print("STOP: {}".format(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
