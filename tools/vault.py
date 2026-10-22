#!/usr/bin/env python3
"""Keep a project's Soul record in the machine's vault, reached by a `.soul` link.

A vault is one private git repo of Obsidian folders, one folder per project:
`projects/<key>/project.md` (label, contributes, remote) and `projects/<key>/soul/`
(the record). The project's `.soul` becomes a link to that `soul/` folder, so the
completion gate, the Mind import and every skill keep finding `.soul/` where they
always did (SOUL-I079, whose fields hold the decisions). /soul-init drives
this helper; the helper does the mechanical parts.

  init <dir> [--name N] [--register]     scaffold a vault (never overwrites); --register
                                         names it in this machine's vault file
  where                                  the vault this machine's file names (exit 1:
                                         none named; 3: named but not there yet)
  link <project> --key K --label L       move the record into the vault and link it,
       [--contributes a,b] [--vault DIR]  or re-link a record the vault already holds
       [--dry-run]                        (a new machine after cloning the vault)
  check <project> [--json]               linked / broken / two copies / not linked;
                                         exit 1 if broken or two copies
  session-start                          SessionStart hook: one short line, or nothing

One vault per machine: the machine file ($XDG_CONFIG_HOME or ~/.config, then
soul/vault) holds one line, the vault's folder. The boundary is where the vault
lives, so the one label rule is enforced here: `restricted` is refused.

What the link test (2026-10-22, I079 LINK TEST) made non-negotiable, each kept below:
- On WSL with the project on a Windows drive the link is a junction (`mklink /J`):
  Windows tools cannot follow a WSL-made symlink. WSL sees a junction as a symlink
  whose target reads back as the /mnt path, and unlink removes only the link.
  So the vault must be on a Windows drive too.
- Claude Code refuses writes through the link until the vault is listed in
  `.claude/settings.local.json` `permissions.additionalDirectories`.
- A broken link turns the gate off and git stays quiet, so `check` and the
  session-start line say it out loud.
- Copy, compare every file's hash, link, compare again through the link; only then
  is the old folder removed. Nothing is deleted before a compare passes.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

LABELS = ("public", "private", "confidential", "restricted")
ROOT_STORES = ("witness.md", "ideas.md", "mind.md", "upstream.md")
# Files that may import the Mind; a root-layout move rewrites `@mind.md` in them.
IMPORTERS = ("CLAUDE.md", os.path.join(".claude", "CLAUDE.md"), "AGENTS.md",
             "AGENTS.override.md")
KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class VaultError(Exception):
    pass


# ---------------------------------------------------------------- machine file

def machine_file():
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(base, "soul", "vault")


def registered_vault():
    """The vault folder this machine's file names, or None when there is no file."""
    try:
        with open(machine_file(), encoding="utf-8") as f:
            line = f.readline().strip()
    except OSError:
        return None
    return os.path.expanduser(line) if line else None


def is_vault(path):
    return os.path.isfile(os.path.join(path, "vault.md"))


# ---------------------------------------------------------------- init

VAULT_MD = """# Soul vault — {name}

One private git repo; one folder per project: `projects/<key>/project.md` (label,
contributes, remote) and `projects/<key>/soul/` (that project's Soul record, which
the project reaches through its `.soul` link).

Labels: public, private, confidential. A `restricted` project never goes in.
The vault counts as kept only once it is pushed.
"""

GITIGNORE = """# Obsidian per-machine state
.obsidian/workspace*
.obsidian/cache
# Never pushed with the vault: each project's private-name list (it may hold an
# employer's or client's names) and the runtime event log
projects/*/soul/private-names.txt
projects/*/soul/events.jsonl
"""

INDEX_MD = """# Projects

(Generated — not written by hand.) No projects yet.
"""


def init(path, name=None, register=False):
    path = os.path.abspath(os.path.expanduser(path))
    os.makedirs(os.path.join(path, "projects"), exist_ok=True)
    made = []
    for rel, text in (("vault.md", VAULT_MD.format(name=name or os.path.basename(path))),
                      (".gitignore", GITIGNORE), ("index.md", INDEX_MD),
                      (os.path.join("projects", ".gitkeep"), "")):
        p = os.path.join(path, rel)
        if not os.path.exists(p):
            with open(p, "w", encoding="utf-8") as f:
                f.write(text)
            made.append(rel)
    print("vault at {}: {}".format(path, "created " + ", ".join(made) if made
                                   else "already scaffolded, nothing written"))
    if register:
        current = registered_vault()
        if current and os.path.realpath(current) != os.path.realpath(path):
            raise VaultError("this machine already names a vault ({}) — one vault per "
                             "machine; edit {} by hand to change it".format(current, machine_file()))
        if not current:
            os.makedirs(os.path.dirname(machine_file()), exist_ok=True)
            with open(machine_file(), "w", encoding="utf-8") as f:
                f.write(path + "\n")
        print("registered in {}".format(machine_file()))
    return 0


# ---------------------------------------------------------------- helpers

def _git(project, *args):
    r = subprocess.run(["git", "-C", project, *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def _remote(project):
    return _git(project, "remote", "get-url", "origin")


def _norm_remote(url):
    """host/path, so an SSH clone and an HTTPS clone of one repo match."""
    url = (url or "").strip().rstrip("/")
    url = url[:-4] if url.endswith(".git") else url
    m = re.match(r"^(?:[a-z+]+://)?(?:[^@/]+@)?([^/:]+)[:/](.+)$", url)
    return (m.group(1).lower() + "/" + m.group(2)) if m else url


def _frontmatter(path):
    try:
        text = open(path, encoding="utf-8").read()
    except (OSError, UnicodeError):
        return {}
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        k, sep, v = line.partition(":")
        if sep:
            out[k.strip()] = v.strip()
    return out


def vault_match(project, vault):
    """The key of the vault project that is this project: the same remote, or — only
    when one side has no remote — the same folder name. Two different remotes never
    match, so a same-named project is never linked to another's record."""
    projects = os.path.join(vault, "projects")
    if not os.path.isdir(projects):
        return None
    remote = _norm_remote(_remote(project))
    by_name = None
    for key in sorted(os.listdir(projects)):
        theirs = _norm_remote(_frontmatter(os.path.join(projects, key, "project.md")).get("remote"))
        if remote and theirs:
            if theirs == remote:
                return key
        elif key == os.path.basename(project):
            by_name = key
    return by_name


def _remote_clash(project, home):
    """The vault project's remote when it is a different repo from this one, else None."""
    mine = _norm_remote(_remote(project))
    theirs = _norm_remote(_frontmatter(os.path.join(home, "project.md")).get("remote"))
    return theirs if mine and theirs and mine != theirs else None


def _has_local(project):
    """A record held in the project itself: a real .soul/ folder or a root store."""
    soul = os.path.join(project, ".soul")
    return (os.path.isdir(soul) and not os.path.islink(soul)) or any(
        os.path.isfile(os.path.join(project, n)) for n in ROOT_STORES)


def _tree_hashes(root):
    """{relative path: sha256 or 'link:<target>'} for everything under root."""
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        for name in dirnames + filenames:
            p = os.path.join(dirpath, name)
            rel = os.path.relpath(p, root)
            if os.path.islink(p):
                out[rel] = "link:" + os.readlink(p)
            elif os.path.isfile(p):
                h = hashlib.sha256()
                with open(p, "rb") as f:
                    for chunk in iter(lambda: f.read(1 << 20), b""):
                        h.update(chunk)
                out[rel] = h.hexdigest()
    return out


def _is_wsl():
    if os.environ.get("SOUL_VAULT_FORCE_WSL") is not None:  # tests only
        return os.environ["SOUL_VAULT_FORCE_WSL"] == "1"
    try:
        return "microsoft" in open("/proc/version").read().lower()
    except OSError:
        return False


def _on_windows_drive(path):
    return re.match(r"^/mnt/[a-z]/", os.path.realpath(path) + "/") is not None


def link_kind(project, vault):
    """'junction' or 'symlink'; raises when Windows tools could not reach the vault."""
    if _is_wsl() and _on_windows_drive(project):
        if not _on_windows_drive(vault):
            raise VaultError("the project is on a Windows drive but the vault ({}) is not — "
                             "Windows tools could not follow the link; put the vault on a "
                             "Windows drive (e.g. under /mnt/d)".format(vault))
        return "junction"
    return "symlink"


def _make_link(kind, link, target):
    if kind == "symlink":
        os.symlink(target, link)
        return
    win = lambda p: subprocess.run(["wslpath", "-w", p], capture_output=True,
                                   text=True, check=True).stdout.strip()
    r = subprocess.run(["cmd.exe", "/c", "mklink", "/J", win(link), win(target)],
                       capture_output=True, text=True, cwd=os.path.dirname(link))
    if r.returncode != 0 or not os.path.islink(link):
        raise VaultError("mklink /J failed: " + (r.stdout + r.stderr).strip())


def _add_exclude(project, line):
    """Append `line` to .git/info/exclude unless present. False when not a git repo."""
    path = _git(project, "rev-parse", "--git-path", "info/exclude")
    if not path:
        return False
    path = os.path.join(project, path) if not os.path.isabs(path) else path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
    if line not in text.splitlines():
        with open(path, "a", encoding="utf-8") as f:
            f.write(("" if not text or text.endswith("\n") else "\n") + line + "\n")
    return True


def _read_settings(project):
    """The project's .claude/settings.local.json, or {}; raises on invalid JSON."""
    path = os.path.join(project, ".claude", "settings.local.json")
    if not os.path.exists(path):
        return {}
    try:
        data = json.load(open(path, encoding="utf-8"))
    except ValueError as exc:
        raise VaultError("{} is not valid JSON ({}) — fix it by hand first; nothing "
                         "changed".format(path, exc))
    if not isinstance(data, dict):
        raise VaultError("{} is not a JSON object — fix it by hand first; nothing "
                         "changed".format(path))
    return data


def _allow_dir(project, vault, data):
    """Merge the vault into .claude/settings.local.json additionalDirectories."""
    dirs = data.setdefault("permissions", {}).setdefault("additionalDirectories", [])
    if vault in dirs:
        return False
    dirs.append(vault)
    path = os.path.join(project, ".claude", "settings.local.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    return True


# `@mind.md`, `@./mind.md`, `@../mind.md`, `- @mind.md`, with or without a trailing note.
MIND_IMPORT = re.compile(r"(?m)^([ \t]*(?:-[ \t]+)?)@((?:\.{1,2}/)*)mind\.md(?=\s|$)")


def _move_root_stores(project, soul, dry_run):
    """Root layout → .soul/: move the stores and repoint `@mind.md` imports.
    Returns (moved, rewritten files, files that still name mind.md — check by hand)."""
    moved = [n for n in ROOT_STORES if os.path.isfile(os.path.join(project, n))]
    clash = [n for n in moved if os.path.lexists(os.path.join(soul, n))]
    if clash:
        raise VaultError("both {0} and .soul/{0} exist — which is the record is the "
                         "owner's call; nothing moved".format(clash[0]))
    rewrites, unsure = [], []
    for rel in (IMPORTERS if "mind.md" in moved else ()):
        p = os.path.join(project, rel)
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8", newline="") as f:  # keep CRLF files CRLF
            text = f.read()
        new = MIND_IMPORT.sub(r"\1@\2.soul/mind.md", text)
        if new != text:
            rewrites.append((p, new))
        if re.search(r"(?<!\.soul/)\bmind\.md", new):
            unsure.append(p)
    if not dry_run:
        os.makedirs(soul, exist_ok=True)
        for n in moved:
            os.rename(os.path.join(project, n), os.path.join(soul, n))
        for p, new in rewrites:
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.write(new)
    return moved, [p for p, _ in rewrites], unsure


# ---------------------------------------------------------------- link

def link(project, key, label, contributes=(), vault=None, dry_run=False):
    project = os.path.realpath(project)
    if label not in LABELS:
        raise VaultError("unknown label {!r} — one of {}".format(label, ", ".join(LABELS)))
    if label == "restricted":
        raise VaultError("a restricted project never goes in a vault — its record stays "
                         "in the project (local or in git)")
    if not KEY_RE.match(key or ""):
        raise VaultError("key {!r}: letters, digits, '.', '_', '-' only".format(key))
    vault = vault or registered_vault()
    if not vault:
        raise VaultError("no vault named on this machine ({}) — run `init <dir> --register`"
                         .format(machine_file()))
    vault = os.path.realpath(os.path.expanduser(vault))
    if not is_vault(vault):
        raise VaultError("{} is not a vault (no vault.md) — clone it or run init".format(vault))

    soul = os.path.join(project, ".soul")
    parked = soul + ".vault-moving"
    home = os.path.join(vault, "projects", key)
    target = os.path.join(home, "soul")
    kind = link_kind(project, vault)
    say = (lambda *a: print("would " + a[0].format(*a[1:]))) if dry_run else \
          (lambda *a: print(a[0].format(*a[1:])))

    # Every check runs before anything changes, dry run included.
    settings = _read_settings(project)
    if os.path.lexists(parked):
        raise VaultError("{} is left from an interrupted run and holds a copy of the record "
                         "— compare it with {} and remove one by hand; nothing "
                         "changed".format(parked, target))
    clash = _remote_clash(project, home) if os.path.isdir(home) else None
    if clash:
        raise VaultError("vault project {!r} belongs to another repo ({}) — choose another "
                         "key; nothing changed".format(key, clash))
    if os.path.islink(soul):
        current = os.readlink(soul)
        if os.path.realpath(soul) == os.path.realpath(target) and os.path.isdir(target):
            print("already linked: .soul → {}".format(target))
            mode = "linked"
        elif os.path.exists(soul):
            raise VaultError(".soul already links elsewhere ({}) — not changed".format(current))
        elif os.path.basename(os.path.dirname(current.rstrip("/"))) != key:
            raise VaultError(".soul is a broken link to {} — that names a different key than "
                             "{!r}; nothing changed".format(current, key))
        elif os.path.isdir(target):
            mode = "relink-broken"
        else:
            raise VaultError(".soul is a broken link to {} and the vault has no record for "
                             "{!r} — clone the vault there, or name the right key".format(current, key))
    elif os.path.isdir(target):
        if _has_local(project):
            raise VaultError("the vault already holds a record for {!r} and this project has "
                             "its own — merging two records is the owner's call; nothing "
                             "changed".format(key))
        mode = "relink"
    else:
        if os.path.lexists(home) and os.listdir(home) and not os.path.isfile(
                os.path.join(home, "project.md")):
            raise VaultError("{} exists and is not a vault project folder".format(home))
        if not _has_local(project):
            raise VaultError("no record to move (no .soul/ and no root witness.md or "
                             "ideas.md) — scaffold it first")
        mode = "move"

    if mode == "move":
        moved, rewrites, unsure = _move_root_stores(project, soul, dry_run)
        for n in moved:
            say("move {} → .soul/{}", n, n)
        for p in rewrites:
            say("repoint the Mind import in {} to .soul/mind.md", os.path.relpath(p, project))
        for p in unsure:
            print("CHECK BY HAND: {} still names mind.md in a form not repointed — the Mind "
                  "will not load until it reads .soul/mind.md".format(os.path.relpath(p, project)))
        say("copy .soul/ → {} and compare every file", target)
        say("replace .soul/ with a {} to it, and compare again through the link", kind)
        if not dry_run:
            # Before the swap: the parked copy must never be committable.
            _add_exclude(project, os.path.basename(parked))
            before = _tree_hashes(soul)
            made_home = not os.path.exists(home)
            try:
                os.makedirs(home, exist_ok=True)
                shutil.copytree(soul, target, symlinks=True)
                if _tree_hashes(target) != before:
                    raise VaultError("the copy in the vault did not match — removed it; "
                                     ".soul/ untouched")
                os.rename(soul, parked)
            except BaseException:
                shutil.rmtree(target, ignore_errors=True)
                if made_home:
                    shutil.rmtree(home, ignore_errors=True)
                raise
            try:
                _make_link(kind, soul, target)
                if _tree_hashes(soul) != before:
                    raise VaultError("the record read through the link did not match — "
                                     "rolled back; .soul/ untouched")
            except BaseException:
                if os.path.islink(soul):
                    os.unlink(soul)
                os.rename(parked, soul)
                shutil.rmtree(target, ignore_errors=True)
                if made_home:
                    shutil.rmtree(home, ignore_errors=True)
                raise
            try:
                shutil.rmtree(parked)
            except OSError as exc:
                print("record MOVED and linked, but the old copy at {} could not be removed "
                      "({}) — delete it by hand; git ignores it meanwhile".format(parked, exc))
            print("moved {} files; both compares passed".format(len(before)))
    elif mode in ("relink", "relink-broken"):
        if mode == "relink-broken":
            say("remove the broken .soul link")
            if not dry_run:
                os.unlink(soul)
        say("link .soul → {} ({}) — the vault already holds this record", target, kind)
        if not dry_run:
            _make_link(kind, soul, target)

    pm = os.path.join(home, "project.md")
    if not os.path.exists(pm):
        say("write {}", pm)
        if not dry_run:
            remote = re.sub(r"^([a-z+]+://)[^@/]+@", r"\1", _remote(project) or "")
            with open(pm, "w", encoding="utf-8") as f:
                f.write("---\nkey: {}\nlabel: {}\ncontributes: [{}]\nremote: {}\nsoul: true\n"
                        "---\n\n# {}\n".format(key, label, ", ".join(contributes), remote, key))
    elif _frontmatter(pm).get("label") not in (None, label):
        print("note: {} says label {} — kept; edit it there to change it"
              .format(pm, _frontmatter(pm).get("label")))

    if dry_run:
        say("add .soul to .git/info/exclude; add the vault to "
            ".claude/settings.local.json additionalDirectories")
    else:
        if _add_exclude(project, ".soul"):
            if _git(project, "check-ignore", "-q", ".claude/settings.local.json") is None:
                _add_exclude(project, ".claude/settings.local.json")
        if _allow_dir(project, vault, settings):
            print("allowed the vault in .claude/settings.local.json (writes through the "
                  "link are refused without it)")

    tracked = _git(project, "ls-files", "--", ".soul", *ROOT_STORES)
    if tracked:
        print("STILL TRACKED in git — until a `git rm --cached` of these is committed, a git "
              "reset, stash, restore or checkout can put the old committed copy back in place "
              "of the link, and writes then go to that stale copy (check reports TWO COPIES). "
              "History keeps the old copies either way:")
        for t in tracked.splitlines():
            print("  " + t)
    print("{}: .soul → {}".format("dry run" if dry_run else "done", target))
    return 0


# ---------------------------------------------------------------- check / hook

def check(project):
    """{'state': 'linked'|'broken'|'two-copies'|'not-linked', 'target', 'vault_has'}"""
    project = os.path.realpath(project)
    soul = os.path.join(project, ".soul")
    if os.path.islink(soul):
        target = os.readlink(soul)
        if not os.path.isabs(target):
            target = os.path.normpath(os.path.join(project, target))
        state = "linked" if os.path.isdir(soul) else "broken"
        if state == "linked" and any(os.path.isfile(os.path.join(project, n))
                                     for n in ROOT_STORES):
            state = "two-copies"  # a reset brought a tracked root-layout record back
        return {"state": state, "target": target, "vault_has": None}
    out = {"state": "not-linked", "target": None, "vault_has": None}
    vault = registered_vault()
    if vault and is_vault(vault):
        key = vault_match(project, vault)
        if key and os.path.isdir(os.path.join(vault, "projects", key, "soul")):
            out["vault_has"] = key
            out["target"] = os.path.join(vault, "projects", key, "soul")
            if _has_local(project):
                out["state"] = "two-copies"
    return out


def check_line(state):
    if state["state"] == "broken":
        return ("Soul vault link BROKEN: .soul → {} is missing, so this project's record "
                "(witness, ideas, Mind, handoff) cannot be read or written. Fix: clone the "
                "vault there, or re-run /soul-init.".format(state["target"]))
    if state["state"] == "two-copies":
        return ("Soul record has TWO COPIES: this project holds its own (a .soul/ folder or "
                "root witness.md/ideas.md) and the vault holds one for it ({}). A git reset, stash or checkout of a still-tracked record "
                "can replace the link this way. Compare them before writing; which is current "
                "is the owner's call.".format(state["target"]))
    if state["state"] == "linked":
        return "Soul record lives in the vault: .soul → {}.".format(state["target"])
    if state["vault_has"]:
        return ("The vault holds a Soul record for this project ({}) but nothing links "
                "to it — /soul-init re-links it.".format(state["vault_has"]))
    return None


def session_start(data):
    cwd = data.get("cwd") if isinstance(data.get("cwd"), str) else os.getcwd()
    st = check(cwd)
    line = check_line(st)
    if not line:
        return None
    out = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": line}}
    if st["state"] != "linked":
        out["systemMessage"] = line
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init", help="scaffold a vault (never overwrites)")
    i.add_argument("dir")
    i.add_argument("--name")
    i.add_argument("--register", action="store_true", help="name it in this machine's file")
    sub.add_parser("where", help="the vault this machine names")
    ln = sub.add_parser("link", help="move the record into the vault and link it")
    ln.add_argument("project")
    ln.add_argument("--key", required=True)
    ln.add_argument("--label", required=True, choices=LABELS)
    ln.add_argument("--contributes", default="", help="comma-separated tags")
    ln.add_argument("--vault", help="default: the machine file's vault")
    ln.add_argument("--dry-run", action="store_true")
    c = sub.add_parser("check", help="linked / broken / not linked")
    c.add_argument("project")
    c.add_argument("--json", action="store_true")
    sub.add_parser("session-start", help="SessionStart hook (reads the event on stdin)")
    args = ap.parse_args()

    if args.cmd == "session-start":
        try:
            raw = sys.stdin.read()
            out = session_start(json.loads(raw) if raw.strip() else {})
        except Exception as exc:  # a silent crash would hide a broken link
            out = {"systemMessage": "Soul vault check skipped ({}) — a broken .soul link "
                                    "would not be reported.".format(type(exc).__name__)}
        if out:
            print(json.dumps(out))
        return 0
    try:
        if args.cmd == "init":
            return init(args.dir, args.name, args.register)
        if args.cmd == "where":
            v = registered_vault()
            if not v:
                print("no vault named ({})".format(machine_file()), file=sys.stderr)
                return 1
            if not is_vault(v):  # exit 3, not 1: "clone it first", never "no vault"
                print("{} is named in {} but holds no vault.md — clone the vault there "
                      "first".format(v, machine_file()), file=sys.stderr)
                return 3
            print(v)
            return 0
        if args.cmd == "link":
            tags = [t.strip() for t in args.contributes.split(",") if t.strip()]
            return link(args.project, args.key, args.label, tags, args.vault, args.dry_run)
        st = check(args.project)
        print(json.dumps(st) if args.json else (check_line(st) or "not linked"))
        return 1 if st["state"] in ("broken", "two-copies") else 0
    except VaultError as exc:
        print("vault: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
