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
       [--dry-run] [--sidecar]            (a new machine after cloning the vault)
  index [<vault>]                        rewrite the vault's index.md from projects/*/project.md
  check <project> [--json]               linked / broken / two copies / not linked;
                                         exit 1 if broken or two copies
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

_HERE = os.path.dirname(os.path.abspath(__file__))

LABELS = ("public", "private", "confidential", "restricted")
ROOT_STORES = ("witness.md", "ideas.md", "mind.md", "upstream.md")
# Files that may import the Mind; a root-layout move rewrites `@mind.md` in them.
IMPORTERS = ("CLAUDE.md", os.path.join(".claude", "CLAUDE.md"), "AGENTS.md",
             "AGENTS.override.md")
CASELESS_HOSTS = ("github.com", "gitlab.com", "bitbucket.org")
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


# ---------------------------------------------------------------- link

def link(project, key, label, contributes=(), vault=None, dry_run=False, sidecar=False):
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
            say("remove the local .soul/ (it held only the gate's event log)")
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
    tracked = _git(project, "ls-files", "--", ".soul", *(() if keeps_root else ROOT_STORES))
    if tracked:
        print("STILL TRACKED in git — until a `git rm --cached` of these is committed, a git "
              "reset, stash, restore or checkout can put the old committed copy back in place "
              "of the link, and writes then go to that stale copy (check reports TWO COPIES). "
              "History keeps the old copies either way:")
        for t in tracked.splitlines():
            print("  " + t)
    if not dry_run:
        index(vault)
    print("{}: .soul → {}".format("dry run" if dry_run else "done", target))
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


def index(vault):
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
    print("index.md: {} project(s){}".format(len(rows), ", {} left out (restricted or no "
                                             "public/private/confidential label)"
                                             .format(skipped) if skipped else ""))
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
    ln.add_argument("--sidecar", action="store_true",
                    help="move only .soul/; the root record stays in the project, tracked")
    c = sub.add_parser("check", help="linked / broken / not linked")
    c.add_argument("project")
    c.add_argument("--json", action="store_true")
    x = sub.add_parser("index", help="rewrite the vault's index.md")
    x.add_argument("vault", nargs="?", help="default: the machine file's vault")
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
        if args.cmd == "link":
            tags = [t.strip() for t in args.contributes.split(",") if t.strip()]
            return link(args.project, args.key, args.label, tags, args.vault, args.dry_run,
                        args.sidecar)
        st = check(args.project)
        print(json.dumps(st) if args.json else (check_line(st) or "not linked"))
        return 1 if st["state"] in ("broken", "two-copies") else 0
    except VaultError as exc:
        print("vault: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
