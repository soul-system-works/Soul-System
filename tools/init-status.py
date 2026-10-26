#!/usr/bin/env python3
"""/soul-init's checklist: what is set, what needs repair here, and what to ask.

/soul-init is run by a model, and each run used to re-ask every question, worded
its own way, because nothing kept the answers. This tool gives every run the same
list, with fixed question wording (QUESTIONS below; the skill shows it word for
word), and keeps the owner's answers in `.soul/init.md`, one dated line per key:

    record:        git          2026-10-23

A recorded answer wins over what the files suggest, EXCEPT that a repair is always
worked out from the real state of this machine: `hand-hooks: yes` recorded on one
machine still reads `repair` on a new one where the hooks are missing, and
`record: local` reads `repair` while the record is tracked.

  status <project> [--json] [--ask KEY ...]
                                     gather and report; never writes. --ask puts that
                                     key's question back this run, even when the answer
                                     is inferred or recorded (/soul-init revisit)
  record <project> <key> <value...>  write or replace that key's line, dated today;
                                     refused (exit 2) while the vault holds this
                                     project's record and nothing links to it
  revisit <project> [key ...]        forget those answers (all when none named)

Exit 0 ok, 2 usage or error. Set SOUL_INIT_NO_GH=1 to skip the `gh` visibility
lookup (the tests do, so they never reach the network).

Values the skill records, per key (the option `value` fields in QUESTIONS):
  import add|leave · vault-link link (recorded after linking; "Not now" is not
  recorded) · record git|local|vault ·
  public yes|no · names none|listed · hand-hooks yes|no ·
  history-scan `clean <sha12>`|`findings <sha12>`|declined ·
  stage prototype|pre-release|released|not-now · line-endings yes|no ·
  existing-store use|no.  `layout` keeps its own list (.soul/layout.json); `mind` has
  no answer, only a repair. An extras question with one member is yes|no; the skill
  records the member's own value (history-scan: `declined` for no).
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import eol  # noqa: E402  (tools/eol.py — line-endings facts)
import vault as vaultlib  # noqa: E402  (tools/vault.py — where / check)

LAYOUT = os.path.join(_HERE, "layout-cleanup.py")
GUARD = os.path.join(ROOT, "hooks", "secret-guard.py")

ANSWERS = os.path.join(".soul", "init.md")
HEADER = ("# /soul-init's remembered answers (tools/init-status.py).\n"
          "# Delete a line, or run `init-status.py revisit`, to be asked again.\n")
KEYS = ("import", "vault-link", "record", "public", "names", "hand-hooks", "history-scan",
        "stage", "layout", "line-endings", "mind", "existing-store")
RECORDABLE = tuple(k for k in KEYS if k not in ("layout", "mind"))
IMPORTERS = ("CLAUDE.md", os.path.join(".claude", "CLAUDE.md"), "AGENTS.md")
STORES = ("witness.md", "ideas.md")
HOOKS = ("pre-commit", "commit-msg", "pre-push")
HOOK_MARK = "Soul System secret check"
# Soul's own files, never working material. layout-cleanup.py's STORE_FILES lists them
# too (v3.6.0); kept here so an older plugin copy's scan cannot flag them.
LAYOUT_SKIP = (".soul/init.md", ".soul/private-names.txt")
EXTRAS = ("hand-hooks", "history-scan", "line-endings")
MAIN = ("record", "stage", "names")
SINGLE = ("vault-link", "import", "existing-store", "layout")

LINE_RE = re.compile(r"^([A-Za-z][\w-]*):[ \t]+(.*?)(?:[ \t]+(\d{4}-\d{2}-\d{2}))?[ \t]*$")
IMPORT_RE = re.compile(r"^\s*(?:-\s+)?@(\S+)\s*$")
STAGE_RE = re.compile(r"^\*\*Stage:\s*([A-Za-z][\w-]*)")
PHASE_RE = re.compile(r"^\*\*Phase:")
GUARD_RE = re.compile(r'^\s*guard="([^"]*)"', re.M)
# Folders the existing-store walk never enters (any folder starting "." is skipped too).
WALK_SKIP = ("node_modules", "venv")
WALK_DEPTH = 4

# The fixed wording. The first option is the recommended one unless a question's
# `recommended` comes out null (the record question in a public repo). Placeholders:
# {path} (existing-store), {n} (layout).
QUESTIONS = {
    "record": {
        "group": "main", "multi": False,
        "text": "Where should this project's record (its decision log and ideas) live?",
        "options": [
            {"value": "git", "label": "In this repo's git",
             "description": "backed up, travels with the repo"},
            {"value": "vault", "label": "In your Soul vault",
             "description": "private, kept with your other projects"},
            {"value": "local", "label": "Only on this machine",
             "description": "no backup, no history"},
        ],
        "public_description": "public: anyone can read it",
    },
    "stage": {
        "group": "main", "multi": False,
        "text": "How settled is this project?",
        "options": [
            # The same descriptions as skills/soul-stage — one wording, not two.
            {"value": "prototype", "label": "Prototype",
             "description": "throwaway code to answer a question; nothing is promised to anyone"},
            {"value": "pre-release", "label": "Pre-release",
             "description": "building the real thing; still free to rename, reorganise and delete"},
            {"value": "released", "label": "Released",
             "description": "people rely on it; changes are careful and announced"},
            {"value": "not-now", "label": "Not now",
             "description": "treated as released until you choose"},
        ],
    },
    "names": {
        "group": "main", "multi": False,
        "text": "Any names that must never appear in this repo: clients, employers, people, "
                "a work email?",
        "options": [
            {"value": "none", "label": "None beyond my global list",
             "description": "~/.claude/soul-private-names.txt still applies"},
            {"value": "listed", "label": "Type them",
             "description": "one per line; Name => TOKEN suggests a replacement"},
        ],
        "public_note": " This repo is public — a name committed here is public.",
    },
    "extras": {
        "group": "extras", "multi": True,
        "text": "Which safety checks should I set up? (tick any)",
        "members": {
            "hand-hooks": {"key": "hand-hooks", "label": "Check commits I make by hand",
                           "description": "installs git hooks that run outside Claude"},
            "history-scan": {"key": "history-scan",
                             "label": "Scan git history for leaked secrets now",
                             "description": "reports only, changes nothing"},
            "line-endings": {"key": "line-endings",
                             "label": "Make line endings the same on Windows and WSL",
                             "description": "one commit adding .gitattributes"},
        },
        # AskUserQuestion needs 2–4 options, so one member is asked as yes / no.
        "one_text": "Set this up? {label} ({description})",
        "one_options": [
            {"value": "yes", "label": "Yes", "description": None},  # the member's own
            {"value": "no", "label": "No",
             "description": "not asked again; /soul-init revisit to change"},
        ],
    },
    "public": {
        "group": "single", "multi": False,
        "text": "Is this repo public, or will it be?",
        "options": [
            {"value": "yes", "label": "Yes", "description": "anyone can read what is committed"},
            {"value": "no", "label": "No", "description": "private to you or your team"},
        ],
    },
    "import": {
        "group": "single", "multi": False,
        "text": "Add the Soul line to your existing CLAUDE.md?",
        "options": [
            {"value": "add", "label": "Add it",
             "description": "one import line at the top; nothing else changes"},
            {"value": "leave", "label": "Leave it",
             "description": "Soul stays off in this project"},
        ],
    },
    "vault-link": {
        "group": "single", "multi": False,
        "text": "Your vault already holds this project's record. Link it here?",
        "options": [
            {"value": "link", "label": "Link it",
             "description": "this checkout uses the vault copy"},
            {"value": "not-now", "label": "Not now", "description": "nothing changes"},
        ],
    },
    "existing-store": {
        "group": "single", "multi": False,
        "text": "{path} looks like this project's record. Use it?",
        "options": [
            {"value": "use", "label": "Use it",
             "description": "Soul writes there; no second copy"},
            {"value": "no", "label": "No", "description": "start a new record in .soul/"},
        ],
    },
    "layout": {
        "group": "single", "multi": False,
        "text": "{n} working files could move into .ai/ (safe to delete). Review them?",
        "options": [
            {"value": "review", "label": "Review", "description": "go group by group"},
            {"value": "leave", "label": "Leave them",
             "description": "remembered; only newly flagged files are asked about"},
        ],
    },
}


class InitError(Exception):
    pass


# ---------------------------------------------------------------- helpers

def _run(cmd, cwd=None, timeout=60):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return None


def _git(project, *args):
    """stdout of a git command, stripped, or None when it failed."""
    r = _run(["git", "-C", project, *args])
    return r.stdout.strip() if r is not None and r.returncode == 0 else None


def _git_ok(project, *args):
    r = _run(["git", "-C", project, *args])
    return r is not None and r.returncode == 0


def _read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return None


def _item(key, action="none", value=None, date=None, source="none", detail=""):
    return {"key": key, "value": value, "date": date, "source": source, "action": action,
            "detail": detail, "question": None, "group": None}


def _recorded(key, rec, action="none", detail=""):
    return _item(key, action, rec[0], rec[1], "recorded", detail)


# ---------------------------------------------------------------- answers file

def answers_path(project):
    return os.path.join(project, ANSWERS)


def read_answers(project):
    """(lines without newlines, {key: (value, date)}); the first line of a key wins."""
    text = _read(answers_path(project))
    lines = text.splitlines() if text else []
    out = {}
    for ln in lines:
        m = LINE_RE.match(ln)
        if m and m.group(1) not in out and m.group(2):
            out[m.group(1)] = (m.group(2), m.group(3))
    return lines, out


def _write_answers(project, lines):
    soul = os.path.join(project, ".soul")
    if os.path.islink(soul) and not os.path.exists(soul):
        raise InitError(".soul is a broken link ({}) — fix it first (`vault.py check`); "
                        "nothing written".format(os.readlink(soul)))
    os.makedirs(soul, exist_ok=True)  # a link to a folder passes: written through it
    path = answers_path(project)
    old = _read(path) or ""
    nl = "\r\n" if "\r\n" in old else "\n"
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(nl.join(lines) + nl)


def _line(key, value, date):
    return "{} {} {}".format((key + ":").ljust(14), value.ljust(12), date)


# The values each key accepts (the option `value`s the skill records). A value outside
# these would be stored, then read back as "not understood" and asked again forever.
VALUES = {
    "import": ("add", "leave"), "vault-link": ("link",), "record": ("git", "local", "vault"),
    "public": ("yes", "no"), "names": ("none", "listed"), "hand-hooks": ("yes", "no"),
    "stage": ("prototype", "pre-release", "released", "not-now"),
    "line-endings": ("yes", "no"), "existing-store": ("use", "no"),
}
SCAN_RE = re.compile(r"^(clean|findings) [0-9a-f]{7,40}$|^declined$")


def record(project, key, value):
    if key not in RECORDABLE:
        raise InitError("unknown key {!r} — one of: {}".format(key, ", ".join(RECORDABLE)))
    value = value.strip()
    if not value or "\n" in value or "\r" in value:
        raise InitError("the value must be one non-empty line")
    if key == "history-scan" and value == "no":  # the one-member Yes/No question's "No"
        value = "declined"
    if key == "history-scan" and not SCAN_RE.match(value):
        raise InitError("history-scan takes `clean <sha>`, `findings <sha>` or `declined`")
    if key in VALUES and value not in VALUES[key]:
        raise InitError("{} takes one of: {} (a vault-link \"Not now\" is not recorded — "
                        "it stays a pending question)".format(key, ", ".join(VALUES[key]))
                        if key == "vault-link" else
                        "{} takes one of: {}".format(key, ", ".join(VALUES[key])))
    lines, _ = read_answers(project)
    if not lines:
        lines = HEADER.splitlines()
    new = _line(key, value, datetime.date.today().isoformat())
    out, done = [], False
    for ln in lines:
        m = LINE_RE.match(ln)
        if m and m.group(1) == key:
            if not done:
                out.append(new)
                done = True
            continue
        out.append(ln)
    if not done:
        out.append(new)
    # A real .soul/ made here beside the vault's copy would be TWO COPIES; the skill
    # links first (vault-link), and "Not now" stays a pending question, not an answer.
    st = vaultlib.check(project)
    if st["state"] == "not-linked" and st["vault_has"]:
        raise InitError("the vault holds this project's record ({}) and nothing links to it "
                        "— link the vault record first; nothing recorded"
                        .format(st["vault_has"]))
    _write_answers(project, out)
    print("recorded in {}: {}".format(ANSWERS, new))
    return 0


def revisit(project, keys):
    lines, have = read_answers(project)
    if not have:
        print("nothing recorded in {}".format(ANSWERS))
        return 0
    out, removed = [], []
    for ln in lines:
        m = LINE_RE.match(ln)
        if m and m.group(2) and (not keys or m.group(1) in keys):
            removed.append(ln)
            continue
        out.append(ln)
    for k in keys:
        if k not in have:
            print("not recorded: {}".format(k))
    if removed:
        _write_answers(project, out)
    for ln in removed:
        print("removed: {}".format(ln))
    if not removed:
        print("nothing removed")
    print("inferred answers stay; run status --ask <key> to be asked anyway")
    return 0


# ---------------------------------------------------------------- context

def _imports(project):
    """[(importer rel path, @target, resolved realpath)] for every `@` line."""
    out = []
    for rel in IMPORTERS:
        p = os.path.join(project, rel)
        text = _read(p) if os.path.isfile(p) else None
        for ln in (text or "").splitlines():
            m = IMPORT_RE.match(ln)
            if not m:
                continue
            t = m.group(1)
            full = os.path.expanduser(t) if t.startswith("~") else (
                t if os.path.isabs(t) else os.path.join(os.path.dirname(p), t))
            out.append((rel, t, os.path.realpath(full)))
    return out


def gather(project):
    c = {"project": project}
    c["answers"] = read_answers(project)[1]
    c["git"] = _git(project, "rev-parse", "--is-inside-work-tree") == "true"
    c["top"] = _git(project, "rev-parse", "--show-toplevel") if c["git"] else None
    c["imports"] = _imports(project)
    contract = [i for i in c["imports"] if ("/" + i[1]).endswith("/operations/CLAUDE.md")]
    c["importer"], c["import_target"], c["import_real"] = contract[0] if contract else (None,) * 3
    c["stores"] = [p for p in STORES + tuple(os.path.join(".soul", s) for s in STORES)
                   if os.path.isfile(os.path.join(project, p))]
    c["fresh"] = not c["importer"] and not c["stores"]
    v = vaultlib.registered_vault()
    c["where"] = 1 if not v else (0 if vaultlib.is_vault(v) else 3)
    c["vault"] = v if c["where"] == 0 else None
    c["vault_named"] = v
    return c


# ---------------------------------------------------------------- the decisions

def check_import(c):
    rec = c["answers"].get("import")
    if c["importer"]:
        if not os.path.isfile(c["import_real"]):  # a dead import fails silently (F038)
            return _item("import", "repair", c["importer"], None, "inferred", "{}: the import "
                         "points at {}, which does not exist — rewrite it to the current Soul "
                         "root (skill: import).".format(c["importer"], c["import_target"]))
        return _item("import", "none", c["importer"], None, "inferred", "{} imports the "
                     "contract ({}).".format(c["importer"], c["import_target"]))
    claude = [p for p in IMPORTERS[:2] if os.path.isfile(os.path.join(c["project"], p))]
    if not claude:
        return _item("import", "repair", detail="No CLAUDE.md here — the skill creates one "
                                                "holding the import line (skill: import).")
    if rec and rec[0] == "leave":
        return _recorded("import", rec, detail="You chose to leave {} without the Soul line."
                         .format(claude[0]))
    return _item("import", "ask", detail="{} exists without the Soul import line."
                 .format(claude[0]))


def _vault_holds(c, target):
    """True when this machine's vault is present and holds this project's record — by
    the broken link's own key (<vault>/projects/<key>/soul) or by vault_match."""
    v = c["vault"]
    if not v:
        return False
    t = os.path.normpath(target or "")
    keys = {os.path.basename(os.path.dirname(t))} if os.path.basename(t) == "soul" else set()
    keys.add(vaultlib.vault_match(c["project"], v))
    return any(os.path.isdir(os.path.join(v, "projects", k, "soul")) for k in keys if k)


def check_vault_link(c):
    soul = os.path.join(c["project"], ".soul")
    if not os.path.islink(soul) and c["where"] == 1:
        return None
    if c["where"] == 3 and not os.path.islink(soul):
        return _item("vault-link", "stop", detail="This machine names a vault at {} but it is "
                     "not there — clone the vault to that path first; do not scaffold a "
                     "record (skill: vault-link).".format(c["vault_named"]))
    st = vaultlib.check(c["project"])
    rec = c["answers"].get("vault-link")
    line = vaultlib.check_line(st)
    if st["state"] == "linked":
        return _item("vault-link", "none", "linked", None, "inferred", line)
    if st["state"] == "broken":
        # Re-linking needs the vault here AND holding this record; anything else has
        # nothing to link to, so the run stops rather than offer a repair that fails.
        if not _vault_holds(c, st["target"]):
            d = ("the .soul link points at {}, which is missing — clone the vault there (or "
                 "to the path in ~/.config/soul/vault) and re-run.".format(st["target"]))
            if c["vault"]:
                d += " The vault at {} holds no record for this project.".format(c["vault"])
            return _item("vault-link", "stop", "broken", None, "inferred", d)
        return _item("vault-link", "repair", "broken", None, "inferred", line + " Never "
                     "scaffold over it or remove the link (skill: vault-link).")
    if st["state"] == "two-copies":
        return _item("vault-link", "stop", "two-copies", None, "inferred", line)
    if st["vault_has"]:
        if rec and rec[0] == "not-now":
            return _recorded("vault-link", rec, detail="You chose not to link the vault's "
                             "record ({}) here.".format(st["vault_has"]))
        return _item("vault-link", "ask", detail=line)
    return _item("vault-link", "none", "not linked", None, "inferred",
                 "A vault is named ({}); this project's record is not in it.".format(c["vault"]))


NEITHER = ("The record stores are neither tracked nor ignored — one `git add -A` would "
           "commit them.")


def _record_state(c):
    """Where the record actually is: linked · empty · nogit · tracked · ignored · neither."""
    p = c["project"]
    if os.path.islink(os.path.join(p, ".soul")):
        return "linked"
    if not c["stores"]:
        return "empty"
    if not c["git"]:
        return "nogit"
    if _git(p, "ls-files", "--", *c["stores"]):
        return "tracked"
    if all(_git_ok(p, "check-ignore", "-q", "--", s) for s in c["stores"]):
        return "ignored"
    return "neither"


def _infer_record(c, state):
    if state == "linked":
        return "vault", "`.soul` links into the vault."
    if state == "empty":
        return None, "No record stores (witness.md, ideas.md) yet."
    if state == "nogit":
        return "local", "Not a git repo: the record exists only on this machine."
    if state == "tracked":
        if _git_ok(c["project"], "check-ignore", "-q", "--", ".soul/handoff.md"):
            return "git", "The record stores are tracked and .soul/handoff.md is ignored."
        return None, "The record stores are tracked, but .soul/handoff.md is not ignored."
    if state == "ignored":
        return "local", "git ignores the record stores: they stay on this machine."
    return None, NEITHER


def check_record(c, vault_item, public):
    state = _record_state(c)
    val, why = _infer_record(c, state)
    rec = c["answers"].get("record")
    if rec:
        # A recorded answer never hides the real state: the files are read every run and
        # a disagreement is a repair (the skill asks before changing tracked files).
        v = rec[0]
        linked = state == "linked"
        if v == "vault" and not linked:
            extra = (" " + NEITHER) if state == "neither" else ""
            if vault_item and vault_item["action"] != "none":
                return _recorded("record", rec, detail="Recorded vault; settle vault-link "
                                 "first." + extra)
            if not c["vault"]:
                return _item("record", "ask", v, rec[1], "recorded", "Recorded vault, but "
                             "this machine names no vault." + extra)
            return _recorded("record", rec, "repair", (
                "Recorded vault, but the record is not in it yet — " +
                ("scaffold it (skill: the scaffold), then " if not c["stores"] else "") +
                "move it into the vault (skill: the vault move)." + extra))
        if state == "empty":
            return _recorded("record", rec, "repair", "Recorded {}, but no record stores "
                             "exist yet — scaffold them (skill: the scaffold).".format(v))
        if v == "local" and state == "tracked":
            return _recorded("record", rec, "repair", "recorded local, but the record is "
                             "tracked — untrack it (`git rm --cached`) and ignore `.soul/`.")
        if v == "git" and state == "neither":
            return _recorded("record", rec, "repair", "recorded git, but the record is not "
                             "committed — commit it.")
        if v == "git" and state == "ignored":
            return _recorded("record", rec, "repair", "recorded git, but git ignores the "
                             "record — narrow the ignore rule and commit it (skill: record).")
        if state == "neither":
            return _recorded("record", rec, "repair", "recorded {}, but {}".format(
                v, NEITHER[0].lower() + NEITHER[1:]))
        note = "" if val in (None, v) else " (the files now look like {})".format(val)
        return _recorded("record", rec, detail="Recorded {}.{}".format(v, note))
    if val:
        return _item("record", "none", val, None, "inferred", why)
    if public is None:
        why += " Whether the repo is public is unknown."
    return _item("record", "ask", detail=why)


def _infer_public(c):
    p = c["project"]
    if not c["git"]:
        return None, "Not a git repo."
    if not _git(p, "remote"):
        return None, "No git remote, so visibility is unknown."
    if os.environ.get("SOUL_INIT_NO_GH") or not shutil.which("gh"):
        return None, "gh is not available, so visibility is unknown."
    r = _run(["gh", "repo", "view", "--json", "visibility", "-q", ".visibility"], cwd=p,
             timeout=10)
    out = r.stdout.strip().upper() if r is not None and r.returncode == 0 else ""
    if out == "PUBLIC":
        return "yes", "GitHub says the repo is public."
    if out in ("PRIVATE", "INTERNAL"):
        return "no", "GitHub says the repo is {}.".format(out.lower())
    return None, "gh could not tell whether the repo is public."


def check_public(c):
    rec = c["answers"].get("public")
    if rec:
        return _recorded("public", rec, detail="Recorded.")
    v, why = _infer_public(c)
    return _item("public", "none", v, None, "inferred" if v else "none", why)


def check_names(c):
    rec = c["answers"].get("names")
    if os.path.isfile(os.path.join(c["project"], ".soul", "private-names.txt")):
        return _item("names", "none", "listed", None, "inferred",
                     "This project's private names are in .soul/private-names.txt.")
    if rec and rec[0] == "listed":
        return _item("names", "ask", rec[0], rec[1], "recorded", "Recorded listed, but "
                     ".soul/private-names.txt is missing on this machine.")
    if rec:
        return _recorded("names", rec, detail="No names beyond the global list "
                         "(~/.claude/soul-private-names.txt).")
    return _item("names", "ask", detail="No private-name list for this project.")


def check_hand_hooks(c):
    if not c["git"]:
        return None
    r = _run([sys.executable, GUARD, "--own-hooks-dir", c["project"]])
    d = r.stdout.strip() if r is not None and r.returncode == 0 else ""
    if not d:
        return _item("hand-hooks", detail="Could not find this repo's own hooks folder.")
    soul, foreign, free, dead = [], [], [], []
    for h in HOOKS:
        text = _read(os.path.join(d, h))
        if text is None:
            free.append(h)
        elif HOOK_MARK in text:
            soul.append(h)
            g = GUARD_RE.search(text)  # a pinned plugin path dies at the next update
            if g and not os.path.isfile(os.path.expanduser(g.group(1))):
                dead.append(h)
        else:
            who = "git-lfs" if re.search(r"git[ -]lfs", text) else "another tool"
            foreign.append("{} is held by {}, so hand {} are not checked at that step.".format(
                h, who, "pushes" if h == "pre-push" else "commits"))
    held = (" " + " ".join(foreign)) if foreign else ""
    rec = c["answers"].get("hand-hooks")
    if rec and rec[0] == "no":
        return _recorded("hand-hooks", rec, detail="You chose not to check hand commits." + held)
    if soul or (rec and rec[0] == "yes"):
        src = ("recorded", rec[1]) if rec else ("inferred", None)
        fix = []
        if free:
            fix.append("Install the missing Soul hook(s) {} in {} (skill: hand-hooks).".format(
                ", ".join(free), d))
        if dead:
            fix.append("Soul hook(s) {} point at a missing plugin path — rewrite them with the "
                       "current root (skill: hand-hooks).".format(", ".join(dead)))
        if fix:
            return _item("hand-hooks", "repair", "yes", src[1], src[0], " ".join(fix) + held)
        return _item("hand-hooks", "none", "yes", src[1], src[0],
                     "Soul hooks in {}: {}.".format(d, ", ".join(soul) or "none") + held)
    if not free:
        return _item("hand-hooks", detail="Every hook slot is taken by another tool." + held)
    return _item("hand-hooks", "ask", detail="No Soul hooks in {}; commits made by hand are "
                 "not checked.".format(d) + held)


# Files /soul-init itself writes. A later commit touching only these is not new work
# to scan: recording the scan, then committing init's own edits (the import line, a
# stage block, an ignore line), must not make the next run ask again.
INIT_FILES = (".soul/init.md", "CLAUDE.md", ".claude/CLAUDE.md", "AGENTS.md", ".gitignore")


def _commits_since(project, sha):
    """Commits after `sha` that change anything but INIT_FILES; None when `sha` is not
    in this history."""
    full = _git(project, "rev-parse", "--verify", "--quiet", sha + "^{commit}")
    if not full or not _git_ok(project, "merge-base", "--is-ancestor", full, "HEAD"):
        return None
    n = _git(project, "rev-list", "--count", full + "..HEAD", "--", ".",
             *(":(exclude){}".format(f) for f in INIT_FILES))
    return int(n) if n and n.isdigit() else None


def check_history_scan(c):
    if not c["git"]:
        return None
    p = c["project"]
    if not _git(p, "rev-parse", "--verify", "--quiet", "HEAD"):
        return _item("history-scan", detail="No commits yet — nothing to scan.")
    rec = c["answers"].get("history-scan")
    stale = "History never scanned for leaked secrets."
    if rec:
        word, _, sha = rec[0].partition(" ")
        sha = sha.strip()
        if word == "declined":
            return _recorded("history-scan", rec, detail="You declined the history scan.")
        if word in ("clean", "findings") and sha:
            n = _commits_since(p, sha)
            if n == 0:
                return _recorded("history-scan", rec, detail="Scanned at {} ({}); no new "
                                 "commits since.".format(sha, word))
            stale = ("{} new commit(s) since the scan at {}.".format(n, sha) if n else
                     "The scanned commit {} is not in this history.".format(sha))
        else:
            stale = "The recorded value {!r} is not understood.".format(rec[0])
    value, date, src = (rec[0], rec[1], "recorded") if rec else (None, None, "none")
    if not shutil.which("gitleaks"):
        return _item("history-scan", "none", value, date, src, stale + " The scan cannot run "
                     "until gitleaks is installed.")
    return _item("history-scan", "ask", value, date, src, stale)


def check_stage(c):
    # Every instruction file: /soul-stage writes root CLAUDE.md (AGENTS.md in a Codex-only
    # project), which need not be the file holding the import.
    p = c["project"]
    phase = None
    for f in IMPORTERS:
        for ln in (_read(os.path.join(p, f)) or "").splitlines():
            m = STAGE_RE.match(ln)
            if m:
                return _item("stage", "none", m.group(1), None, "inferred",
                             "{} declares the stage.".format(f))
            if phase is None and PHASE_RE.match(ln):
                phase = f
    note = (" {}: a hand-written **Phase:** block exists — show it before asking."
            .format(phase) if phase else "")
    rec = c["answers"].get("stage")
    if rec and rec[0] == "not-now":
        return _recorded("stage", rec, detail="No stage chosen — treated as released until "
                         "you choose (/soul-stage)." + note)
    if rec:
        return _item("stage", "ask", rec[0], rec[1], "recorded", "Recorded {}, but no "
                     "**Stage:** line is in CLAUDE.md, .claude/CLAUDE.md or AGENTS.md."
                     .format(rec[0]) + note)
    return _item("stage", "ask", detail="No **Stage:** line; treated as released." + note)


def check_layout(c):
    if c["fresh"]:
        return None
    r = _run([sys.executable, LAYOUT, "scan", c["project"], "--json"], timeout=120)
    try:
        cands = json.loads(r.stdout)["candidates"]
    except (AttributeError, ValueError, KeyError, TypeError):
        return _item("layout", detail="The layout scan did not run{}.".format(
            ": " + r.stderr.strip().splitlines()[-1] if r is not None and r.stderr.strip()
            else ""))
    n = len([x for x in cands if x.get("path") not in LAYOUT_SKIP])
    if not n:
        return _item("layout", "none", "clean", None, "inferred", "No working files flagged.")
    it = _item("layout", "ask", detail="{} files flagged — run the layout-cleanup flow (skill "
               "`layout`).".format(n))
    it["count"] = n
    return it


def _eol_need(top):
    """(none|repair|ask, sentence) for one repo's line endings."""
    f = eol.facts(top)
    if f["rule"] and not f["committed"] and not f["working"]:
        return "none", "The rule is in place and every file is LF."
    n = len(f["working"])
    if f["rule"] and not f["committed"]:
        return "repair", ("The rule is in place; {} working cop{} CRLF — rewrite to LF with "
                          "`eol.py fix` (no commit needed).".format(
                              n, "y is" if n == 1 else "ies are"))
    return "ask", "Rule {}; {} file(s) committed with CRLF; {} working cop{} CRLF.".format(
        "present" if f["rule"] else "missing", len(f["committed"]), n,
        "y" if n == 1 else "ies")


def _vault_top(c):
    """The git top of the vault `.soul` links into, when it is a repo other than this one."""
    soul = os.path.join(c["project"], ".soul")
    if not os.path.islink(soul) or not os.path.isdir(soul):
        return None
    top = _git(os.path.realpath(soul), "rev-parse", "--show-toplevel")
    if not top or (c["top"] and os.path.realpath(top) == os.path.realpath(c["top"])):
        return None
    return top


def check_line_endings(c):
    # The vault is a second repo the record is written into, so it is checked too
    # (SOUL-219: about 114 vault files rewritten by hand).
    repos = []
    if c["git"] and c["top"]:
        repos.append(("project", c["top"]))
    vtop = _vault_top(c)
    if vtop:
        repos.append(("vault", vtop))
    if not repos:
        return None
    needs = []
    for name, top in repos:
        try:
            needs.append((name,) + _eol_need(top))
        except eol.EolError as exc:
            return _item("line-endings", detail="The line-ending check failed ({}): {}"
                         .format(name, exc))
    vault = len(repos) > 1

    def say(rows):
        return " ".join(("{}: {}".format(n.capitalize(), d) if vault else d)
                        for n, _, d in rows)

    acting = [r for r in needs if r[1] != "none"]
    if not acting:
        return _item("line-endings", "none", "ok", None, "inferred", say(needs))
    which = (" Needs it: {}.".format("both" if len(acting) == 2 else acting[0][0])
             if vault else "")
    rec = c["answers"].get("line-endings")
    declined = bool(rec and rec[0] == "no")
    if any(r[1] == "ask" for r in acting) and not declined:
        return _item("line-endings", "ask", detail=say(needs) + which)
    if any(r[1] == "repair" for r in acting):  # a recorded no never hides a repair
        return _item("line-endings", "repair", detail=say(needs) + which)
    return _recorded("line-endings", rec, detail="You chose not to add the rule. "
                     + say(needs) + which)


def check_mind(c):
    p = c["project"]
    minds = [m for m in (os.path.join(".soul", "mind.md"), "mind.md")
             if os.path.isfile(os.path.join(p, m))]
    if not minds:
        return None
    loaded = {real for _, _, real in c["imports"]}
    if any(os.path.realpath(os.path.join(p, m)) in loaded for m in minds):
        return None
    f = c["importer"] or "CLAUDE.md"
    rel = os.path.relpath(os.path.join(p, minds[0]), os.path.dirname(os.path.join(p, f)))
    return _item("mind", "repair", minds[0], None, "inferred", "{} exists but nothing imports "
                 "it — add `@{}` after the contract import in {} (skill: mind)."
                 .format(minds[0], rel.replace(os.sep, "/"), f))


def _walk_stores(project):
    """`*ideas*.md` / `*witness*.md` below the root, found on disk (untracked, or no git)."""
    out = []
    for dirpath, dirs, files in os.walk(project):
        rel = os.path.relpath(dirpath, project)
        depth = 0 if rel == "." else rel.count(os.sep) + 1
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d not in WALK_SKIP
                         and depth < WALK_DEPTH)
        if depth == 0:
            continue  # root stores are c["stores"]
        for f in sorted(files):
            if f.lower().endswith(".md") and re.search(r"ideas|witness", f, re.I):
                out.append(os.path.join(rel, f).replace(os.sep, "/"))
    return out


def check_existing_store(c):
    if c["stores"]:
        return None
    out = (_git(c["project"], "ls-files", "--", "*ideas*.md", "*witness*.md") or ""
           if c["git"] else "")
    found = [x for x in out.splitlines() if "/" in x and not x.startswith(".soul/")
             and re.search(r"ideas|witness", os.path.basename(x), re.I)]
    if not found:
        found = _walk_stores(c["project"])
    if os.path.realpath(c["project"]) == os.path.realpath(ROOT):
        # The Soul System's own doctrine (operations/witness-log-format.md) is no record.
        found = [x for x in found if not x.startswith("operations/")]
    if not found:
        return None
    rec = c["answers"].get("existing-store")
    if rec and rec[0] == "no":
        return _recorded("existing-store", rec, detail="You said {} is not the record."
                         .format(found[0]))
    it = _item("existing-store", "ask", detail="Found outside the root and .soul/: {}."
               .format(", ".join(found)))
    it["path"] = found[0]
    return it


# ---------------------------------------------------------------- questions and rounds

def render_question(key, public=None, vault=None, path=None, n=None, members=()):
    q = QUESTIONS[key]
    text, rec = q["text"], 0
    if key == "stage":  # how settled a project is only the owner knows
        rec = None
    multi = q["multi"]
    if key == "public":  # only the owner knows what the repo is, or will be
        rec = None
    if key == "extras":  # each is an offer, none a default (skill: hand-hooks)
        opts, rec = [dict(q["members"][k]) for k in members], None
        if len(opts) == 1:  # AskUserQuestion needs 2–4 options: one member is yes / no
            m = opts[0]
            text = q["one_text"].format(label=m["label"], description=m["description"])
            opts = [dict(o) for o in q["one_options"]]
            opts[0]["description"] = m["description"]
            multi = False
    else:
        opts = [dict(o) for o in q["options"]]
    if key == "record":
        if not vault:
            opts = [o for o in opts if o["value"] != "vault"]
        if public == "yes":
            opts[0]["description"] = q["public_description"]
            rec = None
    if key == "names" and public == "yes":  # like record: in public, no default
        text += q["public_note"]
        rec = None
    text = text.replace("{path}", str(path)).replace("{n}", str(n))
    return {"text": text, "options": opts, "multi": multi, "group": q["group"],
            "recommended": rec}


ASKABLE = tuple(k for k in KEYS if k in QUESTIONS) + EXTRAS
# Keys --ask may force: a choice the owner can sensibly make again. The rest
# (import, vault-link, existing-store, layout) are asked only when the files call for
# it — forcing them asks about something that is not there (a second import line).
FORCEABLE = ("record", "public", "names", "hand-hooks", "history-scan", "stage",
             "line-endings")


def status(project, force=()):
    c = gather(project)
    vault_item = check_vault_link(c)
    public = check_public(c)
    found = {
        "import": check_import(c), "vault-link": vault_item,
        "record": check_record(c, vault_item, public["value"]), "public": public,
        "names": check_names(c), "hand-hooks": check_hand_hooks(c),
        "history-scan": check_history_scan(c), "stage": check_stage(c),
        "layout": check_layout(c), "line-endings": check_line_endings(c),
        "mind": check_mind(c), "existing-store": check_existing_store(c),
    }
    # --ask: the owner's way back to a question an inferred or recorded answer settled.
    # A repair or a stop stays what it is; a scan that cannot run is not offered.
    for k in force:
        i = found.get(k)
        if k not in FORCEABLE or i is None or i["action"] != "none":
            continue
        if k == "history-scan" and not shutil.which("gitleaks"):
            continue
        i["action"] = "ask"
    # Unknown visibility changes the record and names questions, so it is asked first.
    if public["value"] is None and any(found[k] and found[k]["action"] == "ask"
                                       for k in ("record", "names")):
        public["action"] = "ask"
    items = [found[k] for k in KEYS if found[k] is not None]
    asked = {i["key"]: i for i in items if i["action"] == "ask"}
    for k, i in asked.items():
        if k in EXTRAS:
            i["group"] = "extras"
            continue
        i["question"] = render_question(k, public=public["value"], vault=c["vault"],
                                        path=i.pop("path", None), n=i.pop("count", None))
        i["group"] = i["question"]["group"]
    members = [k for k in EXTRAS if k in asked]
    rounds = [[k] for k in SINGLE if k in asked]
    if "public" in asked:
        rounds.append(["public"])
    main = [k for k in MAIN if k in asked]
    rounds += [main[i:i + 4] for i in range(0, len(main), 4)]
    # While the vault holds this record and nothing links to it, nothing else can be
    # recorded here (record() refuses; a local .soul/ would be TWO COPIES): link first.
    if "vault-link" in asked and found["vault-link"]["value"] != "broken":
        rounds, members = [["vault-link"]], []
    if members:
        ex = _item("extras", "ask", detail="One combined question for: {}.".format(
            ", ".join(members)))
        ex["members"] = members
        ex["question"] = render_question("extras", members=members)
        ex["group"] = "extras"
        items.append(ex)
        rounds.append(["extras"])
    return {"project": project, "fresh": c["fresh"], "items": items, "rounds": rounds}


def print_text(st):
    items = st["items"]
    by = {i["key"]: i for i in items}
    stops = [i for i in items if i["action"] == "stop"]
    done = [i for i in items if i["action"] == "none"]
    repairs = [i for i in items if i["action"] == "repair"]
    print("/soul-init status: {}{}".format(st["project"], " (fresh)" if st["fresh"] else ""))
    if stops:
        print("\nStop")
        for i in stops:
            print("  {}: {}".format(i["key"], i["detail"]))
    if done:
        print("\nAll set")
        for i in done:
            if i["value"] is None:
                print("  {}: {}".format(i["key"], i["detail"]))
            else:
                print("  {}: {}  {}".format(i["key"], i["value"], i["date"] or "(found)"))
    if repairs:
        print("\nRepairs")
        for i in repairs:
            print("  {}: {}".format(i["key"], i["detail"]))
    if st["rounds"]:
        print("\nTo ask")
        for n, rnd in enumerate(st["rounds"], 1):
            print("  Round {}:".format(n))
            for k in rnd:
                q = by[k]["question"]
                print("    [{}] {}".format(k, q["text"]))
                for j, o in enumerate(q["options"]):
                    print("      - {} — {}{}".format(o["label"], o["description"],
                                                    "  (recommended)" if j == q["recommended"]
                                                    else ""))
                if by[k]["detail"] and k != "extras":
                    print("      why: {}".format(by[k]["detail"]))
    if not repairs and not st["rounds"] and not stops:
        print("\nAll set — nothing to do.")


# ---------------------------------------------------------------- entry

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("status", help="what is set, what to repair, what to ask (no writes)")
    s.add_argument("project")
    s.add_argument("--json", action="store_true")
    s.add_argument("--ask", action="append", default=[], metavar="KEY",
                   help="ask this key's question this run even when it is answered")
    r = sub.add_parser("record", help="remember one answer, dated today")
    r.add_argument("project")
    r.add_argument("key")
    r.add_argument("value", nargs="+")
    v = sub.add_parser("revisit", help="forget answers (all when no key is named)")
    v.add_argument("project")
    v.add_argument("keys", nargs="*")
    try:
        args = ap.parse_args()
    except SystemExit as exc:
        return 2 if exc.code else 0
    project = os.path.realpath(args.project)
    if not os.path.isdir(project):
        print("init-status: no project directory at {}".format(args.project), file=sys.stderr)
        return 2
    try:
        if args.cmd == "record":
            return record(project, args.key, " ".join(args.value))
        if args.cmd == "revisit":
            return revisit(project, args.keys)
        skip = [k for k in args.ask if k not in FORCEABLE]
        if skip:  # warn, never fail: /soul-init revisit passes the keys the owner named
            print("init-status: --ask ignores {} (asked only when the files call for it; "
                  "forceable: {})".format(", ".join(skip), ", ".join(FORCEABLE)),
                  file=sys.stderr)
        st = status(project, force=args.ask)
        if args.json:
            print(json.dumps(st, indent=2))
        else:
            print_text(st)
        return 0
    except (InitError, OSError) as exc:
        print("init-status: {}".format(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
