#!/usr/bin/env python3
"""Keep a project's Soul record in the machine's vault, reached by a `.soul` link.

A vault is one private git repo of Obsidian folders, one folder per project:
`projects/<key>/project.md` (label, contributes, remote) and `projects/<key>/soul/`
(the record). The project's `.soul` becomes a link to that `soul/` folder, so the
completion gate, the Mind import and every skill keep finding `.soul/` where they
always did (SOUL-I079; decision: docs/adr/0001-soul-vault.md). /soul-init drives
this helper; the helper does the mechanical parts.

  init <dir> [--name N] [--register]     scaffold a vault (never overwrites); --register
                                         names it in this machine's vault file
  where                                  the vault this machine's file names (exit 1:
                                         none named; 3: named but not there yet)
  link <project> --key K --label L       move the record into the vault and link it,
       [--contributes a,b] [--vault DIR]  or re-link a record the vault already holds
       [--dry-run] [--sidecar]            (a new machine after cloning the vault);
       [--also PATH ...]                  --also moves named private paths with it, into
                                         soul/<same path>, copy-compare-delete (exit 5:
                                         linked, but a named path was not moved)
  index [<vault>]                        rewrite the vault's index.md from projects/*/project.md
  check <project> [--json]               linked / broken / two copies / not linked;
                                         exit 1 if broken or two copies
  sync <project> [-m MSG]                commit only projects/<key>/ (the key from the
                                         .soul link) and index.md, and push, under a lock
                                         in the vault's .git/ (exit 2: NOT PUSHED; 4: the
                                         lock is held)
  session-start                          SessionStart hook: one short line, or nothing

--sidecar moves only the private .soul/ folder (handoff, private-names list, runs); the
record (witness.md, ideas.md, mind.md, upstream.md) stays at the project root, tracked —
for a project whose record is itself public, as Soul-System's is (SOUL-223). The move
records `sidecar: true` in the vault's projects/<key>/project.md, so a fresh clone of a
sidecar project re-links without the flag, and `check` reads the layout from there.

A real .soul/ holding only the completion gate's events.jsonl (or nothing) is not a
second record: the gate writes that log by itself in a fresh clone before anyone
re-links it. `check` reads it as not linked, and `link` merges the log into the
vault's (copy, or append the missing lines), checks every line arrived, and only then
removes the local folder and links. Anything else in .soul/ is still TWO COPIES.

`sync` is how a skill commits the vault: only the project's own folder and index.md,
under a lock file in the vault's .git/, so sessions sharing the one vault working tree
neither commit each other's edits nor run git over each other. It never resets, stashes
or rebases that tree; a remote that moved is merged in a temporary worktree (see
`sync`). KNOWN LIMIT: git run by hand in the vault does not take the lock.

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
import signal
import socket
import subprocess
import sys
import tempfile
import time

_HERE = os.path.dirname(os.path.abspath(__file__))

LABELS = ("public", "private", "confidential", "restricted")
ROOT_STORES = ("witness.md", "ideas.md", "mind.md", "upstream.md")
# Files that may import the Mind; a root-layout move rewrites `@mind.md` in them.
IMPORTERS = ("CLAUDE.md", os.path.join(".claude", "CLAUDE.md"), "AGENTS.md",
             "AGENTS.override.md", "CLAUDE.local.md")
CASELESS_HOSTS = ("github.com", "gitlab.com", "bitbucket.org")
KEY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class VaultError(Exception):
    pass


class VaultLocked(VaultError):
    """Another sync holds the vault's lock (exit 4)."""


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
# Never pushed with the vault: the runtime event log. Each project's
# private-names.txt IS kept (the owner's call, 2026-10-22): it is what arms the
# secret guard on the next machine. A list can hold names no record mentions
# (a work email) — those enter the vault's history.
projects/*/soul/events.jsonl
"""

INDEX_MD = """# Projects

(Generated — not written by hand.) No projects yet.
"""


def init(path, name=None, register=False):
    # Imported here, not at the top: the SessionStart hook runs `vault.py session-start`, which
    # must never depend on eol.py loading. eol.py sits beside this file; a caller that
    # loads this module from elsewhere does not have tools/ on the path.
    if _HERE not in sys.path:
        sys.path.insert(0, _HERE)
    from eol import RULES as EOL_RULES  # the vault's .gitattributes
    path = os.path.abspath(os.path.expanduser(path))
    os.makedirs(os.path.join(path, "projects"), exist_ok=True)
    made = []
    for rel, text in (("vault.md", VAULT_MD.format(name=name or os.path.basename(path))),
                      (".gitignore", GITIGNORE), ("index.md", INDEX_MD),
                      (".gitattributes", EOL_RULES),
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
    if not m:
        return url
    host, path = m.group(1).lower(), m.group(2)
    if host in CASELESS_HOSTS:  # Me/Alpha and me/alpha are one repo there
        path = path.lower()
    return host + "/" + path


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
    when NEITHER side has a remote — the same folder name. A remote on one side only
    never matches, so a same-named project never reads as another's record."""
    projects = os.path.join(vault, "projects")
    if not os.path.isdir(projects):
        return None
    remote = _norm_remote(_remote(project))
    by_name = None
    for key in sorted(os.listdir(projects)):
        theirs = _norm_remote(_frontmatter(os.path.join(projects, key, "project.md")).get("remote"))
        if remote or theirs:
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
    return _real_soul(project) or _holds_record(project)


def _real_soul(project):
    soul = os.path.join(project, ".soul")
    return os.path.isdir(soul) and not os.path.islink(soul)


EVENT_LOG = "events.jsonl"


def _only_event_log(project):
    """True when the project's real .soul/ holds nothing but the completion gate's
    events.jsonl, or nothing at all. The gate writes that log on its own, so a fresh
    clone not yet re-linked grows one before /soul-init runs; it is no second record,
    and reading it as one made check say TWO COPIES and link refuse (v3.6.3)."""
    soul = os.path.join(project, ".soul")
    if not _real_soul(project):
        return False
    try:
        names = os.listdir(soul)
    except OSError:
        return False
    log = os.path.join(soul, EVENT_LOG)
    return all(n == EVENT_LOG for n in names) and (
        not names or (os.path.isfile(log) and not os.path.islink(log)))


def _second_record(project):
    """A real .soul/ that is a record of its own, not just the gate's event log."""
    return _real_soul(project) and not _only_event_log(project)


def _lines(path):
    """The non-blank lines of a file as bytes, in order, without their newline."""
    with open(path, "rb") as f:
        return [ln for ln in f.read().split(b"\n") if ln.strip()]


def _merge_event_log(local, theirs):
    """Fold the local gate log into the vault's: copy it whole when the vault has none,
    else append the local lines it lacks, in order. Raises unless every local line is
    in the vault's file afterwards — the local log is removed only after this passes."""
    if not os.path.exists(theirs):
        shutil.copyfile(local, theirs)
        if _file_hash(local) != _file_hash(theirs):
            raise VaultError("the event log copied into the vault did not match — "
                             ".soul/ untouched")
        return
    have = set(_lines(theirs))
    new = [ln for ln in _lines(local) if ln not in have]
    if new:
        with open(theirs, "rb") as f:
            text = f.read()
        with open(theirs, "ab") as f:
            f.write((b"" if not text or text.endswith(b"\n") else b"\n")
                    + b"".join(ln + b"\n" for ln in new))
    missing = set(_lines(local)) - set(_lines(theirs))
    if missing:
        raise VaultError("{} event-log line(s) did not reach {} — .soul/ untouched"
                         .format(len(missing), theirs))


def _held_records(path):
    """The record stores (witness.md, ideas.md, ...) that sit directly in `path`."""
    return [n for n in ROOT_STORES if os.path.isfile(os.path.join(path, n))]


def _holds_record(path):
    return bool(_held_records(path))


def _is_sidecar(home):
    """True when the vault project at `home` was linked with --sidecar (its project.md
    says `sidecar: true`): the record stays at the project root, only .soul/ is here.
    Recorded, never inferred from what soul/ holds — a vault copy that lost its stores
    must still read as a second record beside a root one."""
    return _frontmatter(os.path.join(home, "project.md")).get("sidecar", "").lower() == "true"


def _mark_sidecar(pm):
    """Add `sidecar: true` inside an existing project.md's frontmatter; True if it is
    there afterwards."""
    if _frontmatter(pm).get("sidecar", "").lower() == "true":
        return True
    try:
        text = open(pm, encoding="utf-8").read()
    except (OSError, UnicodeError):
        return False
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return False
    with open(pm, "w", encoding="utf-8") as f:
        f.write(text[:m.end(1)] + "\nsidecar: true" + text[m.end(1):])
    return True


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
                out[rel] = _file_hash(p)
    return out


def _file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


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
    perms = data.get("permissions", {}) if isinstance(data, dict) else None
    if not isinstance(perms, dict) or not isinstance(
            perms.get("additionalDirectories", []), list):
        raise VaultError("{} is not shaped as Claude Code settings (an object, with "
                         "permissions an object and additionalDirectories a list) — fix it "
                         "by hand first; nothing changed".format(path))
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


PARK = ".vault-moving"
# Instruction files stay with the project: moving one out would unwire it.
ALSO_REFUSED = ("CLAUDE.md", "CLAUDE.local.md", "AGENTS.md", "AGENTS.override.md", ".claude")


def _also_paths(project, paths, keeps_root=False):
    """Validate `--also` paths before anything changes: inside the project, not in or
    holding a .git, not an instruction file, not part of the record, present, no link on
    the way or inside, every file readable (hashed here), none inside another. Returns
    them relative. An unreadable file once failed the move after the record had moved,
    leaving a link with no project.md and no exclude (review case G)."""
    out = []
    for raw in paths:
        full = os.path.normpath(raw if os.path.isabs(raw) else os.path.join(project, raw))
        rel = os.path.relpath(full, project)
        parts = rel.split(os.sep)
        no = lambda why: VaultError("--also {}: {} — nothing changed".format(raw, why))
        if rel == "." or parts[0] == "..":
            raise no("outside the project")
        if ".git" in parts:
            raise no("inside .git")
        if parts[0] in ALSO_REFUSED:
            raise no("an instruction file, which stays with the project")
        if parts[0] == ".soul":
            raise no("part of the record, which moves anyway")
        if rel in ROOT_STORES:
            raise no("a record store, which a sidecar keeps at the project root" if keeps_root
                     else "part of the record, which moves anyway")
        parent = os.path.dirname(full)
        if os.path.realpath(parent) != parent:
            raise no("reached through a link")
        if not os.path.lexists(full):
            raise no("no such file or folder")
        if os.path.islink(full):
            raise no("a link")
        if os.path.lexists(full + PARK):
            raise no("{} is left from an interrupted move — compare and remove it by hand"
                     .format(rel + PARK))
        for dirpath, dirnames, filenames in os.walk(full):
            for n in dirnames + filenames:
                if n == ".git":
                    raise no("holds a nested .git ({})".format(
                        os.path.relpath(os.path.join(dirpath, n), project)))
                if os.path.islink(os.path.join(dirpath, n)):
                    raise no("holds a link ({})".format(
                        os.path.relpath(os.path.join(dirpath, n), project)))
        try:
            _path_hashes(full)
        except OSError as exc:
            raise no("cannot be read ({})".format(exc))
        out.append(rel)
    for a in out:
        for b in out:
            if a != b and (b + os.sep).startswith(a + os.sep):
                raise VaultError("--also {} is inside --also {} — name one — nothing changed"
                                 .format(b, a))
    return sorted(set(out))


def _path_hashes(path):
    """{relative path: hash} for a file, a link or a folder (a file's key is '')."""
    if os.path.islink(path):
        return {"": "link:" + os.readlink(path)}
    if os.path.isfile(path):
        return {"": _file_hash(path)}
    return _tree_hashes(path)


def _remove(path):
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    elif os.path.lexists(path):
        os.remove(path)


def _move_also(project, target, extras):
    """Each extra path, as the record moves: set the original aside (renamed to
    <path>.vault-moving, so a write meanwhile fails loudly instead of being lost), copy
    it to the vault's soul/<same path>, compare every hash there and again through the
    .soul link, and only then remove the set-aside copy. A failure puts the original back
    and removes the copy. Returns the paths NOT moved, each with its reason."""
    _add_exclude(project, "*" + PARK)  # a set-aside copy must never be committable
    failed = []
    for rel in extras:
        src, dst = os.path.join(project, rel), os.path.join(target, rel)
        parked = src + PARK
        try:
            os.rename(src, parked)
        except OSError as exc:
            failed.append((rel, "could not set it aside ({})".format(exc)))
            continue
        try:
            before = _path_hashes(parked)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.isdir(parked):
                shutil.copytree(parked, dst, symlinks=True)
            else:
                shutil.copy2(parked, dst)
            if (_path_hashes(dst) != before
                    or _path_hashes(os.path.join(project, ".soul", rel)) != before):
                raise VaultError("the copy in the vault did not match")
        except (OSError, VaultError) as exc:
            try:
                _remove(dst)
            except OSError:
                pass
            os.rename(parked, src)
            failed.append((rel, "{} — the copy removed, the original back in place"
                           .format(exc)))
            continue
        try:
            _remove(parked)
        except OSError as exc:
            print("{} moved and compared, but the set-aside copy {} could not be removed "
                  "({}) — delete it by hand; git ignores it".format(rel, rel + PARK, exc))
            continue
        print("moved {} → {} ({} file(s); both compares passed)".format(rel, dst, len(before)))
    return failed


ALSO_PARTIAL_EXIT = 5


# ---------------------------------------------------------------- link

def link(project, key, label, contributes=(), vault=None, dry_run=False, sidecar=False,
         also=()):
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
        # A clash is a second record, not a root record beside a sidecar's vault folder
        # (a fresh clone of a sidecar project re-links with no flag), and not a .soul/
        # holding only the gate's event log (merged into the vault's below).
        if _second_record(project) or (_holds_record(project) and (
                not _is_sidecar(home) or _holds_record(target))):
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
        if sidecar and not _real_soul(project):
            raise VaultError("--sidecar moves only .soul/ and there is none — nothing changed")
        if sidecar and _holds_record(soul):
            raise VaultError("--sidecar keeps the record at the project root, but .soul/ holds "
                             "{} — which is the record is the owner's call; nothing changed"
                             .format(", ".join(_held_records(soul))))
        mode = "move"
    # --also (SOUL-I081, narrow case; mining pass 3, SOUL-234): private paths a project
    # going public moves out with its record — plans, reviews, research folders.
    extras = _also_paths(project, also, sidecar or _is_sidecar(home))
    for rel in extras:
        held = os.path.join(soul if mode == "move" else target, rel)
        if os.path.lexists(held):
            raise VaultError("--also {}: {} already exists — nothing changed".format(rel, held))

    if mode == "move":
        # Sidecar: the root record stays where it is (tracked, public); only .soul/ moves.
        moved, rewrites, unsure = ([], [], []) if sidecar else \
            _move_root_stores(project, soul, dry_run)
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
        if mode == "relink" and _real_soul(project):  # only the gate's log (or empty)
            log = os.path.join(soul, EVENT_LOG)
            if os.path.isfile(log):
                say("merge .soul/{} ({} line(s)) into {} — {}", EVENT_LOG, len(_lines(log)),
                    os.path.join(target, EVENT_LOG), "appending the lines it lacks"
                    if os.path.exists(os.path.join(target, EVENT_LOG)) else "a copy")
            say("remove the local .soul/ ({})", "it held only the gate's event log"
                if os.path.isfile(log) else "it was empty")
            if not dry_run:
                # Merge, check every line arrived, and only then remove the local copy.
                if os.path.isfile(log):
                    _merge_event_log(log, os.path.join(target, EVENT_LOG))
                    os.remove(log)
                try:
                    os.rmdir(soul)
                except OSError:  # something new appeared in .soul/ meanwhile
                    raise VaultError("the event log is merged into the vault, but .soul/ "
                                     "now holds {} — not linked; run check and compare"
                                     .format(", ".join(sorted(os.listdir(soul)))))
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
                        "{}---\n\n# {}\n".format(key, label, ", ".join(contributes), remote,
                                               "sidecar: true\n" if sidecar else "", key))
    else:
        if _frontmatter(pm).get("label") not in (None, label):
            print("note: {} says label {} — kept; edit it there to change it"
                  .format(pm, _frontmatter(pm).get("label")))
        if sidecar and not _is_sidecar(home):
            say("add `sidecar: true` to {}", pm)
            if not dry_run and not _mark_sidecar(pm):
                print("CHECK BY HAND: {} has no frontmatter to record `sidecar: true` in — "
                      "until it does, check reads a root record beside this link as TWO "
                      "COPIES".format(pm))

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

    # A sidecar keeps its record tracked at the root on purpose (a fresh clone re-linking
    # one reads that from project.md, with no flag); a tracked .soul still warns.
    keeps_root = sidecar or _is_sidecar(home)
    tracked = _git(project, "ls-files", "--", ".soul", *(() if keeps_root else ROOT_STORES),
                   *extras)
    if tracked:
        print("STILL TRACKED in git — until a `git rm --cached` of these is committed, a git "
              "reset, stash, restore or checkout can put the old committed copy back in place "
              "of the link, and writes then go to that stale copy (check reports TWO COPIES). "
              "History keeps the old copies either way:")
        for t in tracked.splitlines():
            print("  " + t)
    if not dry_run:
        index(vault)
    # Last, once the link is whole (exclude, settings, project.md, index): a failure here
    # leaves a working link and the path where it was, never a half-made link.
    for rel in extras:
        say("move {} → {} (set aside, copy, compare, then remove)", rel,
            os.path.join(target, rel))
    failed = _move_also(project, target, extras) if extras and not dry_run else []
    print("{}: .soul → {}".format("dry run" if dry_run else "done", target))
    if failed:
        print("the record is linked, but {} --also path(s) were NOT moved:".format(len(failed)))
        for rel, why in failed:
            print("  {}: {}".format(rel, why))
        return ALSO_PARTIAL_EXIT
    return 0


# ---------------------------------------------------------------- index

def _latest_witness(path):
    """(ID, date) of the last entry in a witness log, or (None, None). Two entry forms:
    an `ID:` line (its date from the `WHEN:` line after it), or a heading
    `## YYYY-MM-DD — title`, which has no ID: (None, date). The last in the file wins."""
    last_id = last_when = None
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                m = re.match(r"^##\s+(\d{4}-\d{2}-\d{2})\s*[\u2014\u2013-]", line)
                if m:
                    last_id, last_when = None, m.group(1)
                m = re.match(r"^ID:\s+(\S+)", line)
                if m:
                    last_id, last_when = m.group(1), None
                m = re.match(r"^WHEN:\s+(\d{4}-\d{2}-\d{2})", line)
                if m and last_id and not last_when:
                    last_when = m.group(1)
    except OSError:
        pass
    return last_id, last_when


def index(vault, quiet=False):
    """Rewrite <vault>/index.md: one row per projects/<key>/project.md. A hand-added
    project with no soul/ folder is listed too; a restricted one never is."""
    vault = os.path.realpath(os.path.expanduser(vault))
    if not is_vault(vault):
        raise VaultError("{} is not a vault (no vault.md)".format(vault))
    cell = lambda v: (v or "").replace("|", "\\|")
    rows, skipped = [], 0
    projects = os.path.join(vault, "projects")
    for key in sorted(os.listdir(projects)) if os.path.isdir(projects) else []:
        fm = _frontmatter(os.path.join(projects, key, "project.md"))
        if not fm:
            continue
        label = fm.get("label", "").strip("\"'[] ").lower()
        if label not in ("public", "private", "confidential"):  # restricted, or unreadable
            skipped += 1
            continue
        soul = os.path.join(projects, key, "soul")
        wid, when = _latest_witness(os.path.join(soul, "witness.md"))
        rows.append("| [{0}](projects/{0}/project.md) | {1} | {2} | {3} | {4} |".format(
            key, label, cell(fm.get("contributes", "").strip("[]")),
            "yes" if os.path.isdir(soul) else "no",
            # A sidecar's witness is tracked at the project root, out of the vault's sight.
            "in the project" if _is_sidecar(os.path.join(projects, key)) else
            "{} ({})".format(wid, when) if wid and when else (wid or when or "—")))
    text = ("# Projects\n\nGenerated by `tools/vault.py index` — not written by hand.\n\n"
            + ("| Project | Label | Contributes to | Soul | Latest witness |\n"
               "|---|---|---|---|---|\n" + "\n".join(rows) + "\n" if rows
               else "No projects yet.\n"))
    path = os.path.join(vault, "index.md")
    # Match the STORED copy's line ending, not the working copy's: on a CRLF checkout
    # (Windows git, autocrlf) of an LF commit in a vault without the rule, writing CRLF
    # would leave index.md showing modified. Not a git repo, or untracked: LF.
    try:
        stored = subprocess.run(["git", "-C", vault, "ls-files", "--eol", "--", "index.md"],
                                capture_output=True, text=True)
        crlf = stored.returncode == 0 and stored.stdout.startswith("i/crlf")
    except OSError:  # no git on this machine
        crlf = False
    with open(path, "w", encoding="utf-8", newline="\r\n" if crlf else "\n") as f:
        f.write(text)
    if quiet:
        return 0
    print("index.md: {} project(s){}".format(len(rows), ", {} left out (restricted or no "
                                             "public/private/confidential label)"
                                             .format(skipped) if skipped else ""))
    return 0


# ---------------------------------------------------------------- sync

LOCK_NAME = "soul-sync.lock"
LOCKED_EXIT = 4


def _vault_git(vault, *args):
    return subprocess.run(["git", "-C", vault, *args], capture_output=True, text=True)


def _sync_target(project):
    """(vault, key) from a working `.soul` link: <vault>/projects/<key>/soul."""
    soul = os.path.join(os.path.realpath(project), ".soul")
    if not (os.path.islink(soul) and os.path.isdir(soul)):
        raise VaultError(".soul is not a working link into a vault — nothing to sync "
                         "(`check` says why)")
    home = os.path.dirname(os.path.realpath(soul))
    vault = os.path.dirname(os.path.dirname(home))
    if os.path.basename(os.path.dirname(home)) != "projects" or not is_vault(vault):
        raise VaultError(".soul links to {}, which is not <vault>/projects/<key>/soul"
                         .format(os.path.realpath(soul)))
    return vault, os.path.basename(home)


def _lock_holder(path):
    """(text, stale): who holds the lock and for how long, and whether its process is
    known to be gone (same host, no such pid)."""
    try:
        age = max(0, int(time.time() - os.path.getmtime(path)))
        text = open(path, encoding="utf-8", errors="replace").read().strip()
    except OSError:
        return "could not be read", False
    info = dict(kv.partition("=")[::2] for kv in text.split())
    who = "pid {} on {} (project {}, since {}), {} s ago".format(
        info.get("pid", "?"), info.get("host", "?"), info.get("key", "?"),
        info.get("started", "?"), age)
    stale = False
    if info.get("host") == socket.gethostname() and info.get("pid", "").isdigit():
        try:
            os.kill(int(info["pid"]), 0)
        except ProcessLookupError:
            stale = True
        except OSError:
            pass
    return who, stale


class SyncInterrupted(VaultError):
    pass


def _on_signal(signum, frame):
    raise SyncInterrupted("interrupted by signal {} — stopped; the lock and any temporary "
                          "worktree are removed".format(signum))


def sync(project, message=None):
    """Commit this project's vault folder and push it, under one lock.

    Several sessions share the one vault working tree and leave their own edits in it
    uncommitted. So sync NEVER resets, stashes or rebases that tree: a `pull --rebase
    --autostash` left another session's file holding conflict markers that the next
    sync committed and pushed, stranded edits in a stash, and lost a write made
    mid-rebase (fresh-context review of 3.11.0, reproduced). Instead:
    1. commit only projects/<key>/ and the regenerated index.md (`commit --only`, so
       what others staged stays staged);
    2. fetch; if the remote has not moved, push;
    3. if it has, cherry-pick the local commits the remote lacks onto it in a temporary
       worktree outside the vault and push from there (a conflict only in index.md is
       regenerated; any other conflict stops: committed here, NOT PUSHED, exit 2);
    4. bring the shared tree forward with `read-tree -m -u`, which refuses as a whole if
       a path it must change has unsaved edits; then the copy here stays behind and the
       next sync catches up (the cherry-pick filter skips what was already pushed).
    The lock is a file created exclusively in the vault's .git/; a held lock is never
    broken (exit 4). SIGTERM/SIGINT/SIGHUP remove it and the temporary worktree.
    Two sessions once ran git in the vault in the same second (mining pass 3, SOUL-234).
    KNOWN LIMIT: git run by hand in the vault does not take the lock."""
    vault, key = _sync_target(project)
    gd = _vault_git(vault, "rev-parse", "--absolute-git-dir")
    top = _vault_git(vault, "rev-parse", "--show-toplevel").stdout.strip()
    if gd.returncode != 0 or os.path.realpath(top or "/") != os.path.realpath(vault):
        raise VaultError("the vault at {} is not a git repo of its own — `git init` it and "
                         "add its remote first".format(vault))
    gitdir = gd.stdout.strip()
    lock = os.path.join(gitdir, LOCK_NAME)
    old = {sig: signal.signal(sig, _on_signal)
           for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)}
    mine = None
    try:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            who, stale = _lock_holder(lock)
            raise VaultLocked(
                "vault sync lock {} looks stale: held by {}, and that process is gone. "
                "Nothing done. Check that no git runs in the vault, then remove {} and run "
                "sync again".format(lock, who, lock) if stale else
                "vault sync lock {} is held by a running sync: {}. Nothing done; run sync "
                "again when it finishes".format(lock, who))
        mine = os.fstat(fd).st_ino
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write("pid={} host={} key={} started={}\n".format(
                os.getpid(), socket.gethostname(), key, time.strftime("%Y-%m-%dT%H:%M:%S")))
        return _sync_locked(vault, gitdir, key, message)
    finally:
        try:  # only our own lock: one removed by hand may have been replaced by another
            if mine is not None and os.stat(lock).st_ino == mine:
                os.remove(lock)
        except OSError:
            pass
        for sig, h in old.items():
            signal.signal(sig, h)


def _paths(text):
    return [ln for ln in text.splitlines() if ln.strip()]


def _sync_locked(vault, gitdir, key, message):
    for busy in ("rebase-merge", "rebase-apply", "MERGE_HEAD", "CHERRY_PICK_HEAD"):
        if os.path.exists(os.path.join(gitdir, busy)):
            raise VaultError("the vault is in the middle of a rebase or merge ({}) — "
                             "finish it by hand first; nothing done".format(busy))
    spec = "projects/{}/".format(key)
    index(vault, quiet=True)
    paths = [spec, "index.md"]
    r = _vault_git(vault, "add", "-A", "--", *paths)
    if r.returncode != 0:
        raise VaultError("git add {} failed: {}".format(spec, r.stderr.strip()))
    if _vault_git(vault, "diff", "--cached", "--quiet", "--", *paths).returncode == 0:
        print("nothing to commit in {}".format(spec))
    else:
        # A pathspec commit (--only): what someone else staged stays staged, uncommitted.
        r = _vault_git(vault, "commit", "-q", "-m", message or "soul: sync {} ({})".format(
            key, time.strftime("%Y-%m-%d")), "--only", "--", *paths)
        if r.returncode != 0:
            raise VaultError("git commit of {} failed: {}".format(
                spec, (r.stdout + r.stderr).strip()))
        print("committed {} ({})".format(spec, _vault_git(
            vault, "rev-parse", "--short", "HEAD").stdout.strip()))
    branch = _vault_git(vault, "symbolic-ref", "-q", "--short", "HEAD").stdout.strip()
    remote = _vault_git(vault, "config", "branch.{}.remote".format(branch)).stdout.strip()
    merge = _vault_git(vault, "config", "branch.{}.merge".format(branch)).stdout.strip()
    if not (branch and remote and merge):
        raise VaultError("committed here, NOT PUSHED: the vault's branch has no upstream — "
                         "the vault counts as kept only once it is pushed (set one with "
                         "`git -C {} push -u <remote> {}`)".format(vault, branch or "<branch>"))
    refused = ""
    for _ in (1, 2):  # a refused push (the remote moved meanwhile): fetch and retry once
        r = _vault_git(vault, "fetch", "-q", remote)
        if r.returncode != 0:
            raise VaultError("committed here, NOT PUSHED: git fetch failed: {}"
                             .format(r.stderr.strip()))
        up = _vault_git(vault, "rev-parse", "@{u}").stdout.strip()
        head = _vault_git(vault, "rev-parse", "HEAD").stdout.strip()
        if up == head:
            print("up to date with the remote")
            return 0
        if _vault_git(vault, "merge-base", "--is-ancestor", up, head).returncode == 0:
            r = _vault_git(vault, "push", "-q", remote, "HEAD:" + merge)
            if r.returncode == 0:
                print("pushed")
                return 0
            refused = r.stderr.strip()
            continue
        pushed, refused = _integrate(vault, up, head, remote, merge)
        if pushed:
            return _catch_up(vault, branch, head, pushed)
    raise VaultError("committed here, NOT PUSHED: the push was refused twice: {}"
                     .format(refused or "the remote moved again"))


def _integrate(vault, up, head, remote, merge):
    """Cherry-pick the local commits the remote lacks onto it in a temporary worktree
    outside the vault, and push from there. Returns (the remote's new sha, None), or
    (None, git's refusal) when the push was refused."""
    picks = _paths(_vault_git(vault, "rev-list", "--reverse", "--cherry-pick",
                              "--right-only", "--no-merges", up + "..." + head).stdout)
    if not picks:
        return up, None
    tmp = tempfile.mkdtemp(prefix="soul-sync-")
    wt = os.path.join(tmp, "wt")
    try:
        r = _vault_git(vault, "worktree", "add", "-q", "--detach", wt, up)
        if r.returncode != 0:
            raise VaultError("committed here, NOT PUSHED: could not make a temporary "
                             "worktree: {}".format(r.stderr.strip()))
        for c in picks:
            r = _vault_git(wt, "cherry-pick", c)
            if r.returncode == 0:
                continue
            conflicts = _paths(_vault_git(wt, "diff", "--name-only", "--diff-filter=U").stdout)
            if conflicts == ["index.md"]:  # generated: rebuild it from the merged folders
                index(wt, quiet=True)
                _vault_git(wt, "add", "index.md")
                conflicts = []
            if conflicts:
                _vault_git(wt, "cherry-pick", "--abort")
                raise VaultError("committed here, NOT PUSHED: conflicts with the remote in "
                                 "{} — the copy here is unchanged; merge it by hand"
                                 .format(", ".join(conflicts)))
            if _vault_git(wt, "diff", "--cached", "--quiet").returncode == 0:
                _vault_git(wt, "cherry-pick", "--skip")  # already on the remote
                continue
            r = _vault_git(wt, "-c", "core.editor=true", "cherry-pick", "--continue")
            if r.returncode != 0:
                _vault_git(wt, "cherry-pick", "--abort")
                raise VaultError("committed here, NOT PUSHED: cherry-pick failed: {}"
                                 .format((r.stdout + r.stderr).strip()))
        pushed = _vault_git(wt, "rev-parse", "HEAD").stdout.strip()
        if pushed == up:
            return up, None
        r = _vault_git(wt, "push", "-q", remote, pushed + ":" + merge)
        if r.returncode != 0:
            return None, r.stderr.strip() or "push refused"
        print("pushed on top of the remote's newer commits")
        return pushed, None
    finally:
        _vault_git(vault, "worktree", "remove", "--force", wt)
        _vault_git(vault, "worktree", "prune")
        shutil.rmtree(tmp, ignore_errors=True)


def _catch_up(vault, branch, head, pushed):
    """Move the shared tree and branch from `head` to `pushed` without touching a path
    someone has unsaved edits in: read-tree -m -u refuses as a whole if it must."""
    _vault_git(vault, "update-index", "-q", "--refresh")  # stat info only; read-tree trusts it
    r = _vault_git(vault, "read-tree", "-m", "-u", head, pushed)
    if r.returncode != 0:
        changed = set(_paths(_vault_git(vault, "diff", "--name-only", head, pushed).stdout))
        dirty = [ln[3:] for ln in _vault_git(vault, "status", "--porcelain",
                                             "--untracked-files=all").stdout.splitlines()]
        held = sorted(p for p in dirty if p in changed) or [r.stderr.strip() or "some paths"]
        print("pushed; this vault's copy is behind because {} have unsaved edits from other "
              "sessions — run sync again after they commit".format(", ".join(held)))
        return 0
    r = _vault_git(vault, "update-ref", "-m", "soul sync: catch up",
                   "refs/heads/" + branch, pushed, head)
    if r.returncode != 0:
        raise VaultError("pushed, but the branch here moved meanwhile ({}) — run `git -C {} "
                         "status` and sync again".format(r.stderr.strip(), vault))
    print("brought this vault's copy up to date")
    return 0


# ---------------------------------------------------------------- check / hook

def check(project):
    """{'state': 'linked'|'broken'|'two-copies'|'not-linked', 'target', 'vault_has',
    'sidecar'} — sidecar: the vault's project.md records `sidecar: true` (only .soul/ is
    in the vault; the record stays at the project root)."""
    project = os.path.realpath(project)
    soul = os.path.join(project, ".soul")
    if os.path.islink(soul):
        target = os.readlink(soul)
        if not os.path.isabs(target):
            target = os.path.normpath(os.path.join(project, target))
        state = "linked" if os.path.isdir(soul) else "broken"
        # Broken and the vault gone: project.md is unreadable, so sidecar reads False.
        sidecar = _is_sidecar(os.path.dirname(target.rstrip("/")))
        if state == "linked" and _holds_record(project) and (
                not sidecar or _holds_record(target)):
            state = "two-copies"  # a reset brought a tracked root-layout record back
        return {"state": state, "target": target, "vault_has": None, "sidecar": sidecar}
    out = {"state": "not-linked", "target": None, "vault_has": None, "sidecar": False}
    vault = registered_vault()
    if vault and is_vault(vault):
        key = vault_match(project, vault)
        if key and os.path.isdir(os.path.join(vault, "projects", key, "soul")):
            out["vault_has"] = key
            out["target"] = os.path.join(vault, "projects", key, "soul")
            # A .soul/ holding only the gate's event log is not a second record.
            if _second_record(project) or (_holds_record(project) and (
                    not _is_sidecar(os.path.join(vault, "projects", key))
                    or _holds_record(out["target"]))):
                out["state"] = "two-copies"
    return out


def check_line(state):
    if state["state"] == "broken" and state.get("sidecar"):
        return ("Soul vault link BROKEN: .soul → {} is missing, so this project's .soul/ "
                "files (handoff, private-names list) cannot be read or written; the record "
                "at the project root is unaffected. Fix: clone the vault there, or re-run "
                "/soul-init.".format(state["target"]))
    if state["state"] == "broken":
        return ("Soul vault link BROKEN: .soul → {} is missing, so this project's record "
                "(witness, ideas, Mind, handoff) cannot be read or written. Fix: clone the "
                "vault there, or re-run /soul-init.".format(state["target"]))
    if state["state"] == "two-copies":
        return ("Soul record has TWO COPIES: this project holds its own (a .soul/ folder or "
                "root witness.md/ideas.md) and the vault holds one for it ({}). A git reset, stash or checkout of a still-tracked record "
                "can replace the link this way. Compare them before writing; which is current "
                "is the owner's call.".format(state["target"]))
    if state["state"] == "linked" and state.get("sidecar"):
        return ("This project's .soul/ lives in the vault: .soul → {} (the record itself "
                "stays in the project).".format(state["target"]))
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
    ln.add_argument("--also", nargs="+", default=[], metavar="PATH",
                    help="also move these files or folders (relative to the project) into "
                         "the vault's soul/ folder, keeping their paths")
    ln.add_argument("--sidecar", action="store_true",
                    help="move only .soul/; the root record stays in the project, tracked")
    c = sub.add_parser("check", help="linked / broken / not linked")
    c.add_argument("project")
    c.add_argument("--json", action="store_true")
    x = sub.add_parser("index", help="rewrite the vault's index.md")
    x.add_argument("vault", nargs="?", help="default: the machine file's vault")
    sy = sub.add_parser("sync", help="commit this project's vault folder and push it")
    sy.add_argument("project")
    sy.add_argument("-m", "--message")
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
        if args.cmd == "index":
            v = args.vault or registered_vault()
            if not v:
                raise VaultError("no vault named on this machine ({})".format(machine_file()))
            return index(v)
        if args.cmd == "sync":
            return sync(args.project, args.message)
        if args.cmd == "link":
            tags = [t.strip() for t in args.contributes.split(",") if t.strip()]
            return link(args.project, args.key, args.label, tags, args.vault, args.dry_run,
                        args.sidecar, args.also)
        st = check(args.project)
        print(json.dumps(st) if args.json else (check_line(st) or "not linked"))
        return 1 if st["state"] in ("broken", "two-copies") else 0
    except VaultError as exc:
        print("vault: " + str(exc), file=sys.stderr)
        return LOCKED_EXIT if isinstance(exc, VaultLocked) else 2


if __name__ == "__main__":
    sys.exit(main())
