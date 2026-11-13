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

Since v3.13.0 (SOUL-I092) the decisions never answered are not asked as rounds of
questions: `status` lays them out as one PLAN, each line saying what the thing is and
what the default setup does, plus the wording of one dialog to confirm it — so the
owner sees the whole setup, and where it ends, before anything is written.

  status <project> [--json] [--ask KEY ...] [--choose KEY=VALUE ...]
                                     gather and report; never writes. --ask puts that
                                     key's question back this run, even when the answer
                                     is inferred or recorded (/soul-init revisit), as a
                                     picker in `rounds`, not a plan line. --choose shows
                                     the plan with that value in place of the default
                                     (how "Modify setup" is shown before anything is
                                     recorded)
  explain <project>                  one short paragraph per line of the plan
  doc [--check]                      print docs/setup-choices.md (the same texts);
                                     --check exits 1 when the committed page differs
  record <project> <key> <value...>  write or replace that key's line, dated today;
                                     refused (exit 2) while the vault holds this
                                     project's record and nothing links to it
  revisit <project> [key ...]        forget those answers (all when none named)

Exit 0 ok, 1 doc --check found a difference, 2 usage or error. Set SOUL_INIT_NO_GH=1
to skip the `gh` visibility lookup (the tests do, so they never reach the network).

Values the skill records, per key (the option `value` fields in QUESTIONS):
  import add|leave · vault-link link (recorded after linking; "Not now" is not
  recorded) · sidecar move|keep (move recorded after linking) · record git|local|vault ·
  public yes|no (still read, never asked) · names none|listed · hand-hooks yes|no ·
  history-scan `clean <sha12>`|`findings <sha12>`|`triaged <sha12>`|declined ·
  stage prototype|pre-release|released|not-now · line-endings yes|no ·
  existing-store use|no · upkeep on|off.  `layout` keeps its own list (.soul/layout.json); `mind` has
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
import textwrap

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
KEYS = ("import", "vault-link", "sidecar", "record", "public", "names", "hand-hooks",
        "history-scan", "stage", "layout", "line-endings", "mind", "existing-store", "upkeep")
RECORDABLE = tuple(k for k in KEYS if k not in ("layout", "mind"))
# CLAUDE.local.md: the gitignored local file; a project going public keeps its wiring
# there, and /soul-init then writes there, never into a tracked CLAUDE.md (mining pass 3,
# SOUL-234; tools/dispatch.py already read it).
IMPORTERS = ("CLAUDE.md", os.path.join(".claude", "CLAUDE.md"), "AGENTS.md", "CLAUDE.local.md")
STORES = ("witness.md", "ideas.md")
HOOKS = ("pre-commit", "commit-msg", "pre-push")
HOOK_MARK = "Soul System secret check"
# Soul's own files, never working material. layout-cleanup.py's STORE_FILES lists them
# too (v3.6.0); kept here so an older plugin copy's scan cannot flag them.
LAYOUT_SKIP = (".soul/init.md", ".soul/private-names.txt")
EXTRAS = ("hand-hooks", "history-scan", "line-endings")
MAIN = ("record", "stage", "names", "upkeep")
SINGLE = ("vault-link", "import", "existing-store", "layout", "sidecar")
SIDECAR_FILES = ("handoff.md", "private-names.txt")  # what makes .soul/ worth a sidecar

LINE_RE = re.compile(r"^([A-Za-z][\w-]*):[ \t]+(.*?)(?:[ \t]+(\d{4}-\d{2}-\d{2}))?[ \t]*$")
IMPORT_RE = re.compile(r"^\s*(?:-\s+)?@(\S+)\s*$")
STAGE_RE = re.compile(r"^\*\*Stage:\s*([A-Za-z][\w-]*)")
PHASE_RE = re.compile(r"^\*\*Phase:")
GUARD_RE = re.compile(r'^\s*guard="([^"]*)"', re.M)
# Every line /soul-init's hand-hook template has held (v2.10.0, then v3.11.0's, which
# reads git's input once and runs `git lfs pre-push`, then the Windows-git line, mining
# 2026-11-12), stripped; <root> and <hook> match
# anything. A Soul hook holding any other line was merged by hand: its repair rewrites
# only the `guard=` line and keeps the rest (mining pass 3, SOUL-234). test_init_status.py
# checks the skill's current template against this list.
HAND_TEMPLATE_LINES = (
    '#!/bin/sh',
    '# Soul System secret check (<hook>), installed by /soul-init (operations/secret-guard.md).',
    'guard="<root>/hooks/secret-guard.py"',
    'in=',
    '[ "<hook>" = pre-push ] && in=$(cat; echo .) && in=${in%.}',
    'if [ ! -f "$guard" ] || ! command -v python3 >/dev/null 2>&1; then',
    'echo "Soul secret check NOT running — plugin path missing; re-run /soul-init to repair '
    'the hook" >&2',
    'case $(uname -s 2>/dev/null) in',
    'MINGW*|MSYS*|CYGWIN*) echo "Windows git cannot run the WSL guard — this git <hook> is NOT '
    'checked" >&2 ;;',
    '*) echo "Soul secret check NOT running — plugin path missing; re-run /soul-init to repair '
    'the hook" >&2 ;;',
    'exit 0', 'fi', 'else',
    'python3 "$guard" --hand-hook <hook> "$@"',
    'printf \'%s\' "$in" | python3 "$guard" --hand-hook <hook> "$@"',
    'rc=$?',
    '[ "$rc" -eq 3 ] && exit 1',
    '[ "$rc" -ne 0 ] && echo "Soul secret guard failed (exit $rc) — this git <hook> was NOT '
    'checked" >&2',
    'if [ "<hook>" = pre-push ] && command -v git-lfs >/dev/null 2>&1; then',
    'case $(cat .gitattributes 2>/dev/null) in',
    '*filter=lfs*) printf \'%s\' "$in" | git lfs pre-push "$@" || exit $? ;;',
    'esac',
)
_HAND_RES = tuple(re.compile("^" + re.escape(t).replace(re.escape("<root>"), ".+")
                             .replace(re.escape("<hook>"), "[a-z-]+") + "$")
                  for t in HAND_TEMPLATE_LINES)


def hand_hook_extras(text):
    """The lines of a Soul hand hook that no template version holds (a hand merge)."""
    return [ln.strip() for ln in text.splitlines()
            if ln.strip() and not any(r.match(ln.strip()) for r in _HAND_RES)]
# Folders the existing-store walk never enters (any folder starting "." is skipped too).
WALK_SKIP = ("node_modules", "venv")
WALK_DEPTH = 4

# The fixed wording. The first option is the recommended one unless a question's
# `recommended` comes out null (the record question unless the repo is known private).
# Placeholders: {path} (existing-store), {n} (layout).
QUESTIONS = {
    # One text per option for every visibility (SOUL-I092): the git option itself says
    # what a public repo means for the log, so no separate public question is needed.
    # The vault option is offered whether or not a vault exists: /soul-init can make one.
    "record": {
        "group": "main", "multi": False,
        "text": "Where should Soul's log of this project's decisions and ideas live?",
        "options": [
            {"value": "git", "label": "In this repo's git",
             "description": "Travels with the code and is backed up with it. Whoever can "
                            "read the repo can read the log: if the repo is public, or "
                            "becomes public, so is the log."},
            {"value": "vault", "label": "In a private vault",
             "description": "A separate private repo of yours that can hold the logs of "
                            "all your projects. This project keeps only a link; nothing of "
                            "the log is committed here. Adds 2 steps: which vault, then a "
                            "yes to the move."},
            {"value": "local", "label": "Only on this machine",
             "description": "In this folder, ignored by git. Never published, but one copy "
                            "and no backup."},
        ],
    },
    "stage": {
        "group": "main", "multi": False,
        "text": "How settled is this project? A choice writes a short rules block into "
                "CLAUDE.md.",
        "options": [
            # The same descriptions as skills/soul-stage — one wording, not two.
            {"value": "prototype", "label": "Prototype",
             "description": "throwaway code to answer a question; nothing is promised to anyone"},
            {"value": "pre-release", "label": "Pre-release",
             "description": "building the real thing; still free to rename, reorganise and delete"},
            {"value": "released", "label": "Released",
             "description": "people rely on it; changes are careful and announced"},
            {"value": "not-now", "label": "Not now",
             "description": "writes nothing; treated as released until you choose"},
        ],
    },
    "names": {
        "group": "main", "multi": False,
        "text": "Any names that must never appear in this repo: clients, employers, people, "
                "a work email?",
        "options": [
            {"value": "none", "label": "None beyond my global list",
             "description": "writes nothing; ~/.claude/soul-private-names.txt still applies"},
            {"value": "listed", "label": "Type them",
             "description": "saved to .soul/private-names.txt, never committed; a commit "
                            "containing one gets a warning"},
        ],
        "public_note": " This repo is public — a name committed here is public.",
    },
    # Asked once; no answer means on, the default the owner chose (SOUL-A032, open
    # question 3). hooks/upkeep.py reads the same line, so `off` silences the hook too.
    "upkeep": {
        "group": "main", "multi": False,
        "text": "Should the Soul keep its notes up to date on its own?",
        "options": [
            {"value": "on", "label": "Yes, on its own",
             "description": "refreshes the handoff note in long sessions and after a "
                            "summary, and makes small updates to the project notes; tells "
                            "you in one line "
                            "each time, and a no undoes it"},
            {"value": "off", "label": "No, I'll ask",
             "description": "nothing runs by itself; /soul-next reminds you, and you run "
                            "/soul-handoff and /soul-distill"},
        ],
    },
    "extras": {
        "group": "extras", "multi": True,
        "text": "Which safety checks should I set up? (tick any)",
        "members": {
            "hand-hooks": {"key": "hand-hooks", "label": "Check commits I make by hand",
                           "description": "adds three scripts to .git/hooks that check for "
                                          "secrets when you commit outside Claude; nothing "
                                          "is committed"},
            "history-scan": {"key": "history-scan",
                             "label": "Scan git history for leaked secrets now",
                             "description": "runs gitleaks over past commits and shows what "
                                            "it finds; changes nothing"},
            "line-endings": {"key": "line-endings",
                             "label": "Make line endings the same on Windows and Linux",
                             "description": "adds .gitattributes and converts files to Unix "
                                            "line endings, as one commit"},
        },
        # AskUserQuestion needs 2–4 options, so one member is asked as yes / no.
        "one_text": "Set this up? {label} ({description})",
        "one_options": [
            {"value": "yes", "label": "Yes", "description": None},  # the member's own
            {"value": "no", "label": "No",
             "description": "not asked again; /soul-init revisit to change"},
        ],
    },
    "import": {
        "group": "single", "multi": False,
        "text": "Add the Soul line to your existing CLAUDE.md?",
        "options": [
            {"value": "add", "label": "Add it",
             "description": "one line at the top loads the Soul's rules; your notes stay as "
                            "they are"},
            {"value": "leave", "label": "Leave it",
             "description": "nothing changes; the Soul stays off in this project"},
        ],
    },
    "vault-link": {
        "group": "single", "multi": False,
        "text": "Your vault already holds this project's record. Link it here?",
        "options": [
            {"value": "link", "label": "Link it",
             "description": "makes .soul here a link to the vault's copy; nothing is "
                            "committed"},
            {"value": "not-now", "label": "Not now",
             "description": "nothing changes, and nothing else can be set up here until "
                            "it is linked"},
        ],
    },
    "sidecar": {
        "group": "single", "multi": False,
        "text": "This project's record is committed here, but its .soul/ folder (handoff, "
                "private-names list) is only on this disk. Move .soul/ into your vault?",
        "options": [
            {"value": "move", "label": "Move it to the vault",
             "description": "copies .soul/ into your private vault, checks every file, and "
                            "leaves a link here; the record files at the root stay committed"},
            {"value": "keep", "label": "Keep it here",
             "description": "nothing changes and this is not asked again (`/soul-init "
                            "revisit sidecar` asks again)"},
        ],
    },
    "existing-store": {
        "group": "single", "multi": False,
        "text": "{path} looks like this project's record. Use it?",
        "options": [
            {"value": "use", "label": "Use it",
             "description": "writes a one-line pointer in .soul/; the Soul adds to that "
                            "file, no second copy"},
            {"value": "no", "label": "No",
             "description": "starts a new, empty record in .soul/"},
        ],
    },
    "layout": {
        "group": "single", "multi": False,
        "text": "{n} working files could move into .ai/ (safe to delete). Review them?",
        "options": [
            {"value": "review", "label": "Review",
             "description": "shows them group by group; nothing moves without your yes"},
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
    "import": ("add", "leave"), "vault-link": ("link",), "sidecar": ("move", "keep"),
    "record": ("git", "local", "vault"),
    "public": ("yes", "no"), "names": ("none", "listed"), "hand-hooks": ("yes", "no"),
    "stage": ("prototype", "pre-release", "released", "not-now"),
    "line-endings": ("yes", "no"), "existing-store": ("use", "no"), "upkeep": ("on", "off"),
}
# `triaged <sha>`: every hit was read and none is a real secret. Without it a scan whose
# only hit was a false match stayed "findings", and a later session told the owner the
# history held possible leaked secrets (mining pass 3, SOUL-234).
SCAN_RE = re.compile(r"^(clean|findings|triaged) [0-9a-f]{7,40}$|^declined$")


def validate(key, value):
    """The value `record` stores for `key`, or InitError. One check for `record` and for
    `status --choose`, so the plan never shows a value that could not be recorded."""
    if key not in RECORDABLE:
        raise InitError("unknown key {!r} — one of: {}".format(key, ", ".join(RECORDABLE)))
    value = value.strip()
    if not value or "\n" in value or "\r" in value:
        raise InitError("the value must be one non-empty line")
    if key == "history-scan" and value == "no":  # the one-member Yes/No question's "No"
        value = "declined"
    if key == "history-scan" and not SCAN_RE.match(value):
        raise InitError("history-scan takes `clean <sha>`, `findings <sha>`, `triaged <sha>` "
                        "or `declined`")
    if key in VALUES and value not in VALUES[key]:
        raise InitError("{} takes one of: {} (a vault-link \"Not now\" is not recorded — "
                        "it stays a pending question)".format(key, ", ".join(VALUES[key]))
                        if key == "vault-link" else
                        "{} takes one of: {}".format(key, ", ".join(VALUES[key])))
    return value


def record(project, key, value):
    value = validate(key, value)
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
    # A sidecar link (vault.py link --sidecar): only .soul/ is in the vault; the record
    # stays at the project root, so its state is read there as if nothing were linked.
    c["sidecar"] = (os.path.islink(os.path.join(project, ".soul"))
                    and vaultlib.check(project)["sidecar"])
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
    if rec and rec[0] == "add":  # answered this run; the line is written in step 4
        return _recorded("import", rec, "repair", "Recorded add; the import line is not "
                         "written in {} yet (skill: import).".format(claude[0]))
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


def check_sidecar(c):
    """Offer `vault.py link --sidecar` only where it fits (the owner's call, v3.6.3): the
    record is committed at the root, a real .soul/ beside it holds only private files
    (handoff, private-names list) kept on this disk alone, and this machine's vault is
    here with no record for the project. Anything else is a different move, or none."""
    p = c["project"]
    soul = os.path.join(p, ".soul")
    if os.path.islink(soul) or not os.path.isdir(soul) or c["where"] != 0 or not c["git"]:
        return None
    if vaultlib.check(p)["vault_has"] or vaultlib._holds_record(soul):
        return None
    # Narrow (the owner's call): only a .soul/ holding a private file worth keeping. One
    # holding just the gate's log and init.md has nothing the vault would add.
    if not any(os.path.isfile(os.path.join(soul, n)) for n in SIDECAR_FILES):
        return None
    root = [s for s in c["stores"] if os.sep not in s]
    tracked = set((_git(p, "ls-files", "--", *root) or "").splitlines()) if root else set()
    if not root or not tracked.issuperset(root) or _git(p, "ls-files", "--", ".soul"):
        return None
    rec = c["answers"].get("sidecar")
    if rec and rec[0] == "keep":
        return _recorded("sidecar", rec, detail="You chose to keep .soul/ on this disk.")
    return _item("sidecar", "ask", detail="The record stores ({}) are tracked; .soul/ is not, "
                 "and the vault at {} holds no record for this project."
                 .format(", ".join(root), c["vault"]))


NEITHER = ("The record stores are neither tracked nor ignored — one `git add -A` would "
           "commit them.")


def _record_state(c):
    """Where the record actually is: linked · empty · nogit · tracked · ignored · neither."""
    p = c["project"]
    stores = c["stores"]
    if c["sidecar"]:  # git refuses paths through the link, so only the root stores count
        stores = [s for s in stores if not s.startswith(".soul" + os.sep)]
    elif os.path.islink(os.path.join(p, ".soul")):
        return "linked"
    if not stores:
        return "empty"
    if not c["git"]:
        return "nogit"
    if _git(p, "ls-files", "--", *stores):
        return "tracked"
    if all(_git_ok(p, "check-ignore", "-q", "--", s) for s in stores):
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
        if c["sidecar"] and _git_ok(c["project"], "check-ignore", "-q", "--", ".soul"):
            return "git", ("The record stores are tracked at the project root; .soul/ is an "
                           "ignored link into the vault (a sidecar).")
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
    # A fact, never a question (v3.13.0, SOUL-I092). "Is this repo public, or will it
    # be?" wrote nothing, and the owner asked twice what it did. SOUL-202's concern (a
    # public repo publishes a committed log) is kept by the git option's own text, which
    # says so for every visibility. Still read: a recorded `public: no` (or GitHub saying
    # private) makes git the suggested record answer.
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
    soul, foreign, free, dead, merged, no_lfs = [], [], [], [], [], []
    attrs = _read(os.path.join(c["top"] or c["project"], ".gitattributes")) or ""
    uses_lfs = "filter=lfs" in attrs and shutil.which("git-lfs")
    for h in HOOKS:
        text = _read(os.path.join(d, h))
        if text is None:
            free.append(h)
        elif HOOK_MARK in text:
            soul.append(h)
            extra = hand_hook_extras(text)
            g = GUARD_RE.search(text)  # a pinned plugin path dies at the next update
            if g and not os.path.isfile(os.path.expanduser(g.group(1))):
                (merged if extra else dead).append(h)
            elif h == "pre-push" and uses_lfs and not extra and "git lfs pre-push" not in text:
                no_lfs.append(h)  # LFS was installed after this hook took its slot
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
        if merged:
            fix.append("Soul hook(s) {} point at a missing plugin path and also hold lines "
                       "merged by hand — rewrite only the guard= line and keep the rest "
                       "(skill: hand-hooks).".format(", ".join(merged)))
        if no_lfs:
            fix.append("The Soul pre-push does not run `git lfs pre-push` and this repo uses "
                       "Git LFS, so hand pushes skip the LFS upload — rewrite it with the "
                       "current template (skill: hand-hooks).")
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
        if word in ("clean", "findings", "triaged") and sha:
            # Offered once (the owner, 2026-10-26, v3.6.1): re-offering after every new
            # commit asked on almost every run of an active repo, and the secret guard
            # already checks each new commit as it is made. `--ask history-scan` (or
            # /soul-init revisit history-scan) scans again.
            n = _commits_since(p, sha)
            since = ("; {} commit(s) since — `/soul-init revisit history-scan` scans "
                     "again".format(n) if n else "")
            how = ": hits checked, none real" if word == "triaged" else " ({})".format(word)
            return _recorded("history-scan", rec, detail="Scanned at {}{}{}.".format(
                sha, how, since))
        else:
            stale = "The recorded value {!r} is not understood.".format(rec[0])
    value, date, src = (rec[0], rec[1], "recorded") if rec else (None, None, "none")
    if not shutil.which("gitleaks"):
        return _item("history-scan", "none", value, date, src, stale + " The scan cannot run "
                     "until gitleaks is installed.")
    return _item("history-scan", "ask", value, date, src, stale)


def check_stage(c):
    # Every instruction file: /soul-stage writes root CLAUDE.md (AGENTS.md in a Codex-only
    # project; CLAUDE.local.md when the wiring is there), which need not be the file
    # holding the import.
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
                     "**Stage:** line is in CLAUDE.md, .claude/CLAUDE.md, AGENTS.md or "
                     "CLAUDE.local.md."
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


def _eol_need(f):
    """(none|repair|ask, sentence) for one repo's line endings, from its eol.facts."""
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
    needs, facts = [], {}
    for name, top in repos:
        try:
            facts[name] = eol.facts(top)
            needs.append((name,) + _eol_need(facts[name]))
        except eol.EolError as exc:
            return _item("line-endings", detail="The line-ending check failed ({}): {}"
                         .format(name, exc))
    # For the plan's line: how many committed files the fix rewrites, summed over the
    # repos that need it, and whether it adds the rule file.
    fixing = [n for n, a, _ in needs if a != "none"]
    c["eol"] = {"files": sum(len(facts[n]["committed"]) for n in fixing),
                "adds_rule": any(not facts[n]["rule"] for n in fixing),
                "repos": len(fixing)}
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
    if rec and rec[0] == "use":  # answered; the pointer is written in step 4
        return _recorded("existing-store", rec, "repair", "Recorded use; write the .soul/ "
                         "pointer to {} (skill: existing-store).".format(found[0]))
    it = _item("existing-store", "ask", detail="Found outside the root and .soul/: {}."
               .format(", ".join(found)))
    it["path"] = found[0]
    return it


def check_upkeep(c):
    # Read as hooks/upkeep.py reads it: stripped, lower-cased, on/off only. Anything
    # else is not understood: asked again here, and the hook stays on.
    rec = c["answers"].get("upkeep")
    value = rec[0].strip().lower() if rec else None
    if value in VALUES["upkeep"]:
        return _item("upkeep", "none", value, rec[1], "recorded",
                     "Upkeep runs on its own." if value == "on"
                     else "Upkeep is off: /soul-next reminds; nothing runs by itself.")
    if rec:
        return _item("upkeep", "ask", detail="The recorded value {!r} is not understood; "
                     "until it is answered, upkeep stays on.".format(rec[0]))
    return _item("upkeep", "ask", detail="Not asked yet; until then it is on.")


# ---------------------------------------------------------------- questions and rounds

def render_question(key, public=None, vault=None, path=None, n=None, members=()):
    q = QUESTIONS[key]
    text, rec = q["text"], 0
    if key == "stage":  # how settled a project is only the owner knows
        rec = None
    multi = q["multi"]
    if key == "sidecar":  # whether .soul/ goes to the vault is the owner's (v3.6.3)
        rec = None
    if key == "extras":
        # Hooks and the scan are offers, not defaults (skill: hand-hooks). Line endings
        # is recommended: it is offered only when the repo has the problem, and the
        # owner saw it on every project (SOUL-219).
        opts = [dict(q["members"][k]) for k in members]
        rec = members.index("line-endings") if "line-endings" in members else None
        if len(opts) == 1:  # AskUserQuestion needs 2–4 options: one member is yes / no
            m = opts[0]
            text = q["one_text"].format(label=m["label"], description=m["description"])
            opts = [dict(o) for o in q["one_options"]]
            opts[0]["description"] = m["description"]
            multi = False
            rec = 0 if rec == 0 else None
    else:
        opts = [dict(o) for o in q["options"]]
    if key == "record" and public != "no":  # git is suggested only in a known-private repo
        rec = None
    if key == "names" and public == "yes":  # in public, no default
        text += q["public_note"]
        rec = None
    text = text.replace("{path}", str(path)).replace("{n}", str(n))
    return {"text": text, "options": opts, "multi": multi, "group": q["group"],
            "recommended": rec}


ASKABLE = tuple(k for k in KEYS if k in QUESTIONS) + EXTRAS
# Keys --ask may force: a choice the owner can sensibly make again. The rest
# (import, vault-link, existing-store, layout) are asked only when the files call for
# it — forcing them asks about something that is not there (a second import line).
FORCEABLE = ("record", "names", "hand-hooks", "history-scan", "stage", "line-endings",
             "upkeep")


# ---------------------------------------------------------------- the plan

# The plan (v3.13.0, SOUL-I092; the owner's decisions of 2026-11-12/13): show the setup
# /soul-init would make, every line saying what the thing is before what will be done,
# then one dialog — so a person sees where each choice leads and where the setup ends
# before anything is written. The owner's test: "a person should be presented with
# reasonable options and they should understand where their choices will lead and not
# have to guess on when the setup will end."
PLAN_KEYS = ("record", "stage", "names", "upkeep", "line-endings", "hand-hooks",
             "history-scan")
# plan.text is shown in the dialog's preview box, which is small: it shows about
# (terminal rows - 26) lines and (columns - 38) characters a line, and cuts the rest with
# "N lines hidden" (Claude Code 2.1.325, read from its code on 2026-11-13; the owner's
# first trial showed 27 lines with "3 lines hidden"). So the plan is two short lines an
# item. It is Markdown, in the box and in chat: a bold name and the chosen setting as
# inline code, which is what gets a colour (the owner, at the trial: "can each section
# have color or something? hard to differentiate descrtipon from section").
WIDTH = 58
EARLIER = " Your earlier answer."
# A recorded value the tool does not read (`stage: Prototype`, `upkeep: maybe`): the line
# shows the default that replaces it, and says why (the review of v3.13.0).
NOT_UNDERSTOOD = " Your earlier answer \"{}\" was not understood; this replaces it."
# Per key: the line's name, what the thing is (the owner's fixed meanings), the default
# setup's value, and per value: (label, what the plan says it does, what it adds).
# In "what the plan says", the words before "|" name the setting: the plan colours them.
# "short" is the plan's phrase for the thing, "icon" starts its explanation.
SHORT_BLOCK = "a short rules block in CLAUDE.md"
PLAN = {
    "record": {
        "name": "Record", "short": "Soul's log of decisions and ideas", "icon": "📒",
        "meaning": "Soul's log of this project's decisions and ideas.",
        "default": None,
        "values": {
            "git": ("In this repo's git", "In this repo's git|, committed with the code.",
                    "a .soul/ folder, committed"),
            "vault": ("In a private vault", "In a private vault|; only a link is kept here.",
                      "2 steps: which vault, then a yes to the move"),
            "local": ("Only on this machine", "Only on this machine|, ignored by git.",
                      "a .soul/ folder that git ignores"),
        },
        "more": "Nothing is suggested unless the repo is known to be private (GitHub says "
                "so, or an earlier answer did); then In this repo's git is suggested.",
    },
    "stage": {
        "name": "Stage", "short": "how careful to be about breaking things", "icon": "🚦",
        "meaning": "How careful to be about breaking things.",
        "default": "not-now",
        "values": {
            "not-now": ("Not now", "Not now|: nothing written; treated as released.",
                        None),
            "prototype": ("Prototype", "Prototype|: " + SHORT_BLOCK + ".", SHORT_BLOCK),
            "pre-release": ("Pre-release", "Pre-release|: " + SHORT_BLOCK + ".", SHORT_BLOCK),
            "released": ("Released", "Released|: " + SHORT_BLOCK + ".", SHORT_BLOCK),
        },
        "more": "Any choice but Not now writes a short rules block into CLAUDE.md.",
    },
    "names": {
        "name": "Private names", "short": "names that must never be committed",
        "icon": "🔒",
        "meaning": "Names that must never be committed (clients, employers, people).",
        "default": "none",
        "values": {
            "none": ("None", "None| beyond your global list.", None),
            "listed": ("Type them", "Typed| by you, kept in .soul/, never committed.",
                       "1 step: you type the names"),
        },
        "more": "",
    },
    "upkeep": {
        "name": "Upkeep", "short": "handoff note and project notes, kept current", "icon": "🔄",
        "meaning": "Soul's handoff note and project notes, kept current.",
        "default": "on",
        "values": {
            "on": ("On", "On|: refreshed on their own; one line says so each time.", None),
            "off": ("Off", "Off|: nothing runs by itself; you run them.", None),
        },
        "more": "",
    },
    # In the defaults (the owner, 2026-11-13: "i think line endings would be added by
    # default"); offered whenever the rule file is missing, so most fresh projects get it.
    "line-endings": {
        "name": "Line endings", "short": "Windows and Linux end lines differently",
        "icon": "📄",
        "meaning": "Windows and Linux tools end lines differently, so files can show as "
                   "changed when they are not.",
        "default": "yes",
        "values": {
            "yes": ("Fix them", "Fixed| in one commit ({count}).", "one commit"),
            "no": ("Leave them", "Left| as they are; not asked again.", None),
        },
        "more": "Offered when the rule file is missing or a file was committed with "
                "Windows line endings.",
    },
    "hand-hooks": {
        "name": "Hand-commit hooks", "short": "checks commits you make outside Claude",
        "icon": "🔐",
        "meaning": "Checks commits you make outside Claude for secrets.",
        "default": "no",
        "values": {
            "no": ("Not set up", "Not set up|.", None),
            "yes": ("Set them up", "Set up|: three scripts in .git/hooks, never committed.",
                    "three scripts in .git/hooks"),
        },
        "more": "",
    },
    # `yes` is a --choose-only value meaning "run the scan": what is recorded is its
    # outcome (`clean <sha>` ...), after it runs, so it is a todo, never a `go` pair.
    "history-scan": {
        "name": "History scan", "short": "checks past commits for leaked secrets",
        "icon": "🔍",
        "meaning": "Looks through past commits for leaked secrets, once.",
        "default": "declined",
        "values": {
            "declined": ("Not run", "Not run|.", None),
            "yes": ("Run it now", "Run now|: reads past commits and changes nothing.",
                    "a scan now"),
        },
        "more": "Offered only when gitleaks is installed.",
    },
}
OFF_BY_DEFAULT = {"hand-hooks": "no", "history-scan": "declined"}  # the "Not set up" line
# What an extras member's "no" means, for the explanations (its "yes" is the member's
# own label and description in QUESTIONS).
EXTRA_NO = {
    "hand-hooks": "nothing is installed; commits you make outside Claude are not checked",
    "history-scan": "the scan does not run; the commits Claude makes are still checked",
    "line-endings": "nothing changes, and this is not asked again",
}
# The "Also fixes" line: each repair in everyday words, then its explanation.
REPAIRS = (
    ("import", "the Soul line in CLAUDE.md",
     "The one line that loads Soul's rules is added to CLAUDE.md (made if missing), or "
     "pointed at where Soul is now."),
    ("hand-hooks", "hand-commit hooks",
     "Hooks you chose before are put back, or pointed at where Soul is now."),
    ("mind", "the project-notes import",
     "A line is added so Claude reads the project notes (mind.md)."),
    ("record", "the record's git state",
     "The log is committed, or kept out of git, as your answer says."),
    ("line-endings", "line endings",
     "Files whose copy here has Windows line endings are rewritten; no commit."),
    ("vault-link", "the link to the vault",
     "A broken link to this project's log in your vault is made again."),
    ("existing-store", "the pointer to your existing record",
     "A one-line note tells Soul to add to the log you already keep."),
)
NEXT_TEXT = ("Here is the rest of the setup I'd make. Nothing is written until you say go. "
             "What next?")
NEXT_OPTIONS = (
    ("use", "Use default setup", "Writes the setup shown in the plan."),
    ("modify", "Modify setup", "Opens stage, private names, upkeep and the safety checks, "
                               "then shows the plan again."),
    ("explain", "Explain a line", "What every line means, with its choices; then this "
                                  "plan again."),
    ("not-now", "Not now", "Nothing is written. Run /soul-init again when you are ready."),
)
USE_MODIFIED = "Use this setup"
VAULT_WHICH = "Which vault should hold this project's log?"
VAULT_HAVE = "Your default vault."
VAULT_NEW = "Made now: a new private git repo in that folder."
VAULT_BECOMES = " It becomes this machine's default vault."
VAULT_THERE = "A vault is already in that folder."
VAULT_PASSED = (" Your default vault, {}, is passed over: a project on a Windows drive "
                "needs a vault on one.")
VAULT_OTHER = ("other", "Somewhere else", "Type the folder; a vault is made there if there "
                                          "is none.")
VAULT_CONFIRM = "Move this project's log into the vault at {path}?"
VAULT_CONFIRM_OPTIONS = (
    ("move", "Move it", "Copies it, checks every file, then leaves a link here."),
    ("tags", "Add tags, then move", "Tags for your vault's index and for Obsidian; spaces "
                                    "become hyphens."),
    ("also", "Also move other private folders", "Plans, reviews or research folders move "
                                                "with it."),
    ("cancel", "Cancel", "Nothing moves; the log stays where it is."),
)
PAGE = os.path.join("docs", "setup-choices.md")
PAGE_URL = "https://github.com/soul-system-works/Soul-System/blob/{}/docs/setup-choices.md"


def parse_choose(pairs):
    """{key: value} from --choose KEY=VALUE, checked as `record` checks it."""
    out = {}
    for pair in pairs:
        key, eq, value = pair.partition("=")
        if not eq:
            raise InitError("--choose takes KEY=VALUE, not {!r}".format(pair))
        if key not in PLAN_KEYS:
            raise InitError("--choose takes one of: {}".format(", ".join(PLAN_KEYS)))
        if key == "history-scan" and value.strip() == "yes":  # run it; recorded after
            out[key] = "yes"
            continue
        value = validate(key, value)
        if value not in PLAN[key]["values"]:
            raise InitError("--choose {} takes one of: {}".format(
                key, ", ".join(PLAN[key]["values"])))
        out[key] = value
    return out


def _display(path):
    home = os.path.expanduser("~").rstrip("/")
    if home and (path == home or path.startswith(home + "/")):
        return "~" + path[len(home):]
    return path


def vault_plan(project):
    """{"vault_default", "followups"}: the vault offered when the record goes to a vault.
    The registered vault when `vault.py link` would accept it for this project (on WSL a
    project on a Windows drive needs a vault on a Windows drive); else `soul-vault` on
    the project's Windows drive under WSL; else ~/soul-vault (the owner, 2026-11-13)."""
    reg = vaultlib.registered_vault()
    drive = None
    if vaultlib._is_wsl() and vaultlib._on_windows_drive(project):
        drive = re.match(r"^/mnt/([a-z])/", os.path.realpath(project) + "/").group(1)
    usable = bool(reg) and (drive is None or vaultlib._on_windows_drive(reg))
    if usable:
        path = reg
    elif drive:
        path = "/mnt/{}/soul-vault".format(drive)
    else:
        path = os.path.join(os.path.expanduser("~"), "soul-vault")
    exists = vaultlib.is_vault(path)
    if usable:
        desc = VAULT_HAVE
    else:
        desc = VAULT_THERE if exists else VAULT_NEW
        if reg:
            desc += VAULT_PASSED.format(_display(reg))
        elif not exists:
            desc += VAULT_BECOMES
    which = {"key": "vault-which", "text": VAULT_WHICH,
             "options": [{"value": "default", "label": "Use " + _display(path),
                          "description": desc},
                         dict(zip(("value", "label", "description"), VAULT_OTHER))],
             "multi": False, "group": "vault", "recommended": 0}
    # `template`: the same sentence with {path} left in, for a folder the owner types
    # ("Somewhere else"); `text` is rendered for the default (the review of v3.13.0).
    confirm = {"key": "vault-confirm", "text": VAULT_CONFIRM.format(path=_display(path)),
               "template": VAULT_CONFIRM,
               "options": [dict(zip(("value", "label", "description"), o))
                           for o in VAULT_CONFIRM_OPTIONS],
               "multi": False, "group": "vault", "recommended": None}
    return {"vault_default": {"path": path, "exists": exists, "registered": usable},
            "followups": {"vault-which": which, "vault-confirm": confirm}}


def _more():
    m = re.search(r"^Current: \*\*([^*\s]+)\*\*",
                  _read(os.path.join(ROOT, "SYSTEM-VERSION.md")) or "", re.M)
    return {"url": PAGE_URL.format("v" + m.group(1) if m else "main"),
            "path": os.path.join(ROOT, PAGE)}


def _says(c, key, value):
    """(label, what the plan says it does, what it adds) for one value of a line."""
    label, says, adds = PLAN[key]["values"][value]
    says = says.replace("|", "", 1)
    if key == "line-endings" and value == "yes":
        e = c.get("eol") or {"files": 0, "adds_rule": True, "repos": 1}
        n = e["files"]
        count = "{} file{} change{}".format(n, "" if n == 1 else "s", "s" if n == 1 else "")
        if e["adds_rule"]:
            count += "; adds rule file"
        says = says.format(count=count)
        if e["repos"] > 1:
            says = says.replace("in one commit", "in one commit per repo")
    return label, says, adds


def _head(key, value):
    """The words that name a setting, at the start of what the plan says about it."""
    return PLAN[key]["values"][value][1].partition("|")[0]


def _recorded_value(c, key):
    """The recorded answer when it is one of the line's values, else None."""
    rec = c["answers"].get(key)
    if not rec:
        return None
    try:
        v = validate(key, rec[0])
    except InitError:
        return None  # not understood: the line takes the default setup's value
    return v if v in PLAN[key]["values"] else None


def _wrap(text, first="", rest="  "):
    return textwrap.wrap(text, WIDTH, initial_indent=first, subsequent_indent=rest,
                         break_long_words=False, break_on_hyphens=False)


def _one_of(labels):
    labels = [lb[0].lower() + lb[1:] for lb in labels]
    return labels[0] if len(labels) == 1 else ", ".join(labels[:-1]) + ", or " + labels[-1]


# A setting the owner changed under Modify setup gets a line saying what it was (the
# owner, 2026-11-13: "a visual queue that their modification was selected ... can that
# changed be some other color besides white or blue?"). Markdown here has one accent
# colour, so the line is a one-line `diff` block: its "+" line is drawn green where code
# colouring is on, and as plain text where it is off. The owner picked it from three
# previews in the box. The two fence lines are not drawn, so they do not count against
# the box's height.
CHANGED = "```diff\n+   changed from {}\n```"


def _plan_item(name, phrase, setting=None, head=None, was=None):
    """One item of the plan: a bold name with what it is, then the setting on an arrow
    line with its first words as inline code (see WIDTH), then CHANGED when it was."""
    out = _wrap("{} \u2014 {}".format(name, phrase), "", "    ")
    out[0] = out[0].replace(name, "**{}**".format(name), 1)
    if setting:
        arrow = _wrap(setting[:-1] if setting.endswith(".") else setting,
                      "  \u2192 ", "    ")
        if head and arrow[0][4:].startswith(head):
            arrow[0] = "  \u2192 `{}`{}".format(head, arrow[0][4 + len(head):])
        out += arrow
    if was:
        out += CHANGED.format(was).split("\n")
    return out


def plan_text(lines):
    out = []
    off = [ln for ln in lines if ln["default"]
           and OFF_BY_DEFAULT.get(ln["key"]) == ln["default"]["value"]]
    for ln in lines:
        if ln in off or ln["key"] == "repairs":
            continue
        d = ln["default"]
        if d is None:
            out += _plan_item(ln["name"], ln["short"],
                              "you choose, in the question with this plan", "you choose")
        else:
            out += _plan_item(ln["name"], ln["short"], d["text"], d.get("head"),
                              d.get("was"))
    if off:
        out += _plan_item("Not set up", ", ".join(ln["name"][0].lower() + ln["name"][1:]
                                                  for ln in off))
    for ln in lines:
        if ln["key"] == "repairs":
            out += _plan_item(ln["name"], ln["default"]["text"])
    return "\n".join(out)


def build_plan(c, found, public, keys, choose, extras):
    """The plan for the unforced, unanswered keys (see the module docstring)."""
    lines, go, todo, modified = [], [], [], False
    for key in keys:
        p = PLAN[key]
        rec = _recorded_value(c, key)
        # A recorded answer is never replaced by the default setup's value: the line
        # asks only because the files disagree (a names list missing, no Stage line).
        if key == "record":  # in go only when suggested (a known-private repo) or chosen
            value = rec or ("git" if public == "no" else None)
            in_go = public == "no" and rec is None
        else:
            value, in_go = rec or p["default"], True
        was = None  # the setting a --choose replaced, for the plan's "changed from" line
        if key in choose:
            modified = modified or choose[key] != value
            if value is not None and choose[key] != value:
                was = _head(key, value)
            value, in_go = choose[key], True
        default = None
        if value is not None:
            raw = c["answers"].get(key)
            note = (EARLIER if rec is not None and value == rec else
                    NOT_UNDERSTOOD.format(raw[0]) if raw and rec is None else "")
            if key == "names" and public == "yes":  # today's note, on the line itself
                note += QUESTIONS["names"]["public_note"]
            default = {"value": value, "text": _says(c, key, value)[1] + note,
                       "head": _head(key, value), "was": was}
            if in_go and key == "history-scan" and value == "yes":
                todo.append(key)
            elif in_go:
                go.append([key, value])
        others = []
        for v in p["values"]:
            if v != value:
                label, _, adds = _says(c, key, v)
                others.append({"value": v, "label": label, "adds": adds})
        lines.append({"key": key, "name": p["name"], "meaning": p["meaning"],
                      "short": p["short"],
                      "waits": key == "record" and key not in choose,
                      "default": default, "others": others})
    fixes = [(k, words) for k, words, _ in REPAIRS
             if found.get(k) and found[k]["action"] == "repair"]
    if fixes:
        # On a fresh project these are first-time steps, not fixes (the review of v3.13.0).
        lines.append({"key": "repairs",
                      "name": "Also sets up" if c["fresh"] else "Also fixes",
                      "meaning": "What follows from earlier answers or from the files "
                                 "here, with no question.",
                      "waits": False,
                      "default": {"value": [k for k, _ in fixes],
                                  "text": ", ".join(w for _, w in fixes)},
                      "others": []})
    by = {ln["key"]: ln for ln in lines}
    main = [k for k in ("stage", "names", "upkeep") if k in by]
    change_rounds = ([main] if main else []) + ([["extras"]] if extras else [])
    text = plan_text(lines)
    changeable = main + ([k for k in EXTRAS if k in by] if extras else [])
    more = _more()
    opts = []
    for value, label, desc in NEXT_OPTIONS:
        if value == "modify" and not change_rounds:  # nothing for it to open
            continue
        o = {"value": value, "label": label, "description": desc}
        if value == "use":
            o["label"] = USE_MODIFIED if modified else label
            o["preview"] = text
        elif value == "modify":
            o["preview"] = "\n".join(
                ["Modify setup opens these, then shows the plan again:"]
                + ["  {}: {}".format(by[k]["name"], PLAN[k]["values"][
                    by[k]["default"]["value"]][0]) for k in changeable])
        elif value == "explain":
            o["preview"] = "\n".join(["What every line means, with its choices; then the plan again.",
                                      "The same, with more: " + more["url"],
                                      "On this machine: " + more["path"]])
        opts.append(o)
    screen = []
    if by.get("record", {}).get("waits"):
        screen.append(dict({"key": "record"}, **found["record"]["question"]))
    screen.append({"key": "next", "text": NEXT_TEXT, "options": opts, "multi": False,
                   "group": "plan", "recommended": 0})
    vp = vault_plan(c["project"])
    return {"lines": lines, "go": go, "todo": todo, "text": text, "modified": modified,
            "screen": screen, "change_rounds": change_rounds,
            "followups": vp["followups"], "vault_default": vp["vault_default"],
            "more": more}


# ---------------------------------------------------------------- explanations

def _choices(key):
    """[(value, label, description)] for the explanations, from the question wording."""
    if key in EXTRAS:
        m = QUESTIONS["extras"]["members"][key]
        return [("yes", m["label"], m["description"]),
                ("declined" if key == "history-scan" else "no", "No", EXTRA_NO[key])]
    return [(o["value"], o["label"], o["description"]) for o in QUESTIONS[key]["options"]]


def _sentence(text):
    text = text.rstrip(".")
    return text[0].upper() + text[1:] + "."


def explain_parts(key):
    p = PLAN[key]
    opts = [(label + (" (the default)" if value == p["default"] else ""), _sentence(desc))
            for value, label, desc in _choices(key)]
    return {"name": p["name"], "meaning": p["meaning"], "options": opts,
            "more": p["more"], "revisit": "/soul-init revisit {}".format(key)}


def explain_block(key):
    """One item's explanation, as Markdown: an icon and a bold name, then a bullet for
    each choice (the owner, at the trial: "needs better formatting or just an icon for
    each item. the white runs together")."""
    e = explain_parts(key)
    out = ["{} **{}** \u2014 {}".format(PLAN[key]["icon"], e["name"], e["meaning"])]
    for label, desc in e["options"]:
        base, dflt, _ = label.partition(" (the default)")
        out.append("- **{}**{}: {}".format(base, " (default)" if dflt else "", desc))
    if e["more"]:
        out.append("- " + e["more"])
    out.append("- Change it later: `{}`".format(e["revisit"]))
    return "\n".join(out)


def repairs_block(name, keys):
    out = ["\U0001F527 **{}** \u2014 with no question:".format(name)]
    out += ["- **{}**: {}".format(_sentence(words)[:-1], why)
            for k, words, why in REPAIRS if k in keys]
    return "\n".join(out)


def explain_text(st):
    plan = st.get("plan")
    if not plan:
        return "Nothing here waits for an answer, so there is no plan to explain.\n"
    out = [repairs_block(ln["name"], ln["default"]["value"]) if ln["key"] == "repairs"
           else explain_block(ln["key"]) for ln in plan["lines"]]
    return "\n\n".join(out) + "\n"


def doc_text():
    """docs/setup-choices.md: the explanations and the question wording, for a reader
    new to Soul. Never the version number, nothing about one machine."""
    out = [
        "# Setup choices", "",
        "<!-- Generated by `python3 tools/init-status.py doc` from the wording in that "
        "tool. Change the wording there, then regenerate this page; `doc --check` fails "
        "while the two differ. -->", "",
        "When you run `/soul-init` in a project, Soul shows the whole setup it would make "
        "before it writes anything. Soul is a set of rules and notes that help Claude keep "
        "track of a project: what was decided, why, and what comes next. This page "
        "explains each line of that setup and each choice you are offered.", "",
        "## How it goes", "",
        "1. Soul looks at the project and works out what is already in place. Your "
        "answers are kept in `.soul/init.md` inside the project, so a setting you "
        "answered before is not asked again.",
        "2. A few projects get a short question first: for example, whether to add "
        "Soul's line to a `CLAUDE.md` you already have.",
        "3. Then one dialog shows the plan: a line for each setting never answered, saying "
        "what it is and what Soul would do. When where Soul's log lives is not settled, "
        "that question is in the same dialog.",
        "4. The dialog asks: \"{}\"".format(NEXT_TEXT),
    ]
    out += ["   - **{}**: {}".format(label, desc) for _, label, desc in NEXT_OPTIONS]
    out += [
        "5. After **Modify setup** the plan is shown again with your changes, and the "
        "first choice reads **{}**.".format(USE_MODIFIED), "",
        "Nothing is written until you choose that first option. The setup then ends, with "
        "three exceptions: a private vault adds two steps (see below); typing private names "
        "or choosing Released adds one.", "",
        "## Where Soul's log lives", "",
        "> " + QUESTIONS["record"]["text"], "",
    ]
    out += ["- **{}**: {}".format(o["label"], o["description"])
            for o in QUESTIONS["record"]["options"]]
    out += ["", PLAN["record"]["more"], "",
            "To change it later, run `{}`.".format(explain_parts("record")["revisit"]), "",
            "## The other lines", ""]
    for key in PLAN_KEYS[1:]:
        e = explain_parts(key)
        out += ["### " + e["name"], "", e["meaning"], ""]
        out += ["- **{}**: {}".format(label, desc) for label, desc in e["options"]]
        out += [""] + ([e["more"], ""] if e["more"] else [])
        out += ["To change it later, run `{}`.".format(e["revisit"]), ""]
    out += [
        "Hand-commit hooks and the history scan are not set up by the default setup; "
        "the plan lists them under \"Not set up\", and **Modify setup** can add them.", "",
        "## Also fixes", "",
        "Some things need no question: they follow from answers already given, or from "
        "what Soul finds in the project. The plan names them on its \"Also fixes\" line "
        "(\"Also sets up\" in a project new to Soul).",
        "",
    ]
    out += ["- **{}**: {}".format(_sentence(words)[:-1], why) for _, words, why in REPAIRS]
    out += [
        "", "## A private vault", "",
        "A vault is a separate private git repo of yours that can hold the logs of all "
        "your projects. A project whose log is in the vault keeps only a link to it. "
        "Choosing **In a private vault** adds two questions.", "",
        "> " + VAULT_WHICH, "",
        "- **Use ~/soul-vault** (or the vault this machine already uses): \"{}\" when it "
        "is there; \"{}\" when it is not.".format(VAULT_HAVE, VAULT_NEW + VAULT_BECOMES),
        "- **{}**: {}".format(VAULT_OTHER[1], VAULT_OTHER[2]), "",
        "The vault suggested is the one this machine already uses. With none, it is "
        "`soul-vault` in your home folder. On Windows with WSL, when the project is on a "
        "Windows drive (a path under `/mnt/<drive>/`), it is `soul-vault` on that drive "
        "instead, because a link from a Windows drive cannot reach a folder inside Linux; "
        "a vault elsewhere is then passed over, and the option says so.", "",
        "Soul then shows what would move, moving nothing yet, and asks (with the folder "
        "you chose):", "",
        "> " + VAULT_CONFIRM.format(path="~/soul-vault"), "",
    ]
    out += ["- **{}**: {}".format(label, desc) for _, label, desc in VAULT_CONFIRM_OPTIONS]
    out += [
        "", "## Changing an answer later", "",
        "Each answer is one dated line in `.soul/init.md`. To be asked again, run "
        "`/soul-init revisit <setting>` (for example `/soul-init revisit stage`); with "
        "no setting named, every remembered answer is forgotten; answers Soul reads from "
        "the project's files stay.",
    ]
    return "\n".join(out) + "\n"


def doc(check):
    text = doc_text()
    if not check:
        sys.stdout.write(text)
        return 0
    if _read(os.path.join(ROOT, PAGE)) != text:
        print("init-status: {} differs from `doc` — regenerate it: python3 "
              "tools/init-status.py doc > {}".format(PAGE, PAGE), file=sys.stderr)
        return 1
    print("{} matches `doc`".format(PAGE))
    return 0


def status(project, force=(), choose=None):
    choose = dict(choose or {})
    c = gather(project)
    vault_item = check_vault_link(c)
    public = check_public(c)
    found = {
        "import": check_import(c), "vault-link": vault_item, "sidecar": check_sidecar(c),
        "record": check_record(c, vault_item, public["value"]), "public": public,
        "names": check_names(c), "hand-hooks": check_hand_hooks(c),
        "history-scan": check_history_scan(c), "stage": check_stage(c),
        "layout": check_layout(c), "line-endings": check_line_endings(c),
        "mind": check_mind(c), "existing-store": check_existing_store(c),
        "upkeep": check_upkeep(c),
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
    # Never offer the sidecar while the record's own place is still open: the owner
    # could answer `record vault` and `sidecar move`, opposite layouts. Found by the
    # v3.7.0 replay's reviewer (2026-10-27) in released v3.6.3.
    rec_item, sc_item = found["record"], found["sidecar"]
    if sc_item and sc_item["action"] == "ask" and rec_item and \
            rec_item["action"] in ("ask", "repair"):
        found["sidecar"] = None
    items = [found[k] for k in KEYS if found[k] is not None]
    asked = {i["key"]: i for i in items if i["action"] == "ask"}
    for k, i in asked.items():
        if k in EXTRAS:
            i["group"] = "extras"
            continue
        i["question"] = render_question(k, public=public["value"], vault=c["vault"],
                                        path=i.pop("path", None), n=i.pop("count", None))
        i["group"] = i["question"]["group"]
    # The single-question rounds come first, as before. A key forced with --ask is asked
    # directly as today's picker (that is how /soul-init revisit asks) and is never a
    # plan line; every other unanswered choice is a line of the plan.
    forced = {k for k in force if k in FORCEABLE}
    rounds = [[k] for k in SINGLE if k in asked]
    main = [k for k in MAIN if k in asked and k in forced]
    rounds += [main[i:i + 4] for i in range(0, len(main), 4)]
    lines = [k for k in PLAN_KEYS if k in asked and k not in forced]
    forced_members = [k for k in EXTRAS if k in asked and k in forced]
    plan_members = [k for k in EXTRAS if k in lines]
    # One extras item: the forced members when any (asked now), else the plan's (asked
    # only under Modify setup).
    members = forced_members or plan_members
    # While the vault holds this record and nothing links to it, nothing else can be
    # recorded here (record() refuses; a local .soul/ would be TWO COPIES): link first.
    if "vault-link" in asked and found["vault-link"]["value"] != "broken":
        rounds, members, lines = [["vault-link"]], [], []
    if members:
        ex = _item("extras", "ask", detail="One combined question for: {}.".format(
            ", ".join(members)))
        ex["members"] = members
        ex["question"] = render_question("extras", members=members)
        ex["group"] = "extras"
        items.append(ex)
        if forced_members:
            rounds.append(["extras"])
    ignored = [k for k in choose if k not in lines]
    if ignored:  # warn, never fail: a stale --choose from an earlier screen
        print("init-status: --choose ignores {} (not a line of this plan)".format(
            ", ".join(ignored)), file=sys.stderr)
    plan = None
    if lines:
        plan = build_plan(c, found, public["value"], lines, choose,
                          extras=bool(plan_members and not forced_members))
    return {"project": project, "fresh": c["fresh"], "items": items, "rounds": rounds,
            "plan": plan}


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
    plan = st.get("plan")
    if plan:  # the plan and its one dialog, where the main and extras rounds used to be
        print("\nThe plan")
        for ln in plan["text"].splitlines():
            if not ln.startswith("```"):  # the fences of a "changed from" line
                print("  " + ln if ln else "")
        for q in plan["screen"]:
            print("\n  [{}] {}".format(q["key"], q["text"]))
            for j, o in enumerate(q["options"]):
                print("    - {} — {}{}".format(o["label"], o["description"],
                                              "  (recommended)" if j == q["recommended"]
                                              else ""))
    if not repairs and not st["rounds"] and not stops and not plan:
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
    s.add_argument("--choose", action="append", default=[], metavar="KEY=VALUE",
                   help="show the plan with this value in place of the default (no write)")
    e = sub.add_parser("explain", help="a short paragraph on each line of the plan")
    e.add_argument("project")
    d = sub.add_parser("doc", help="print docs/setup-choices.md from the same texts")
    d.add_argument("--check", action="store_true",
                   help="exit 1 when the committed page differs")
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
    if args.cmd == "doc":
        return doc(args.check)
    project = os.path.realpath(args.project)
    if not os.path.isdir(project):
        print("init-status: no project directory at {}".format(args.project), file=sys.stderr)
        return 2
    try:
        if args.cmd == "record":
            return record(project, args.key, " ".join(args.value))
        if args.cmd == "revisit":
            return revisit(project, args.keys)
        if args.cmd == "explain":
            sys.stdout.write(explain_text(status(project)))
            return 0
        choose = parse_choose(args.choose)
        skip = [k for k in args.ask if k not in FORCEABLE]
        if skip:  # warn, never fail: /soul-init revisit passes the keys the owner named
            print("init-status: --ask ignores {} (asked only when the files call for it; "
                  "forceable: {})".format(", ".join(skip), ", ".join(FORCEABLE)),
                  file=sys.stderr)
        st = status(project, force=args.ask, choose=choose)
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
