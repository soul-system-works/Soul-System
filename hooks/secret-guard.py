#!/usr/bin/env python3
"""Soul System secret guard — credentials block, private names warn (SOUL-I070).
EXPERIMENTAL (owner's call, 2026-10-20).

git itself runs the check. At session start the plugin writes a STABLE, read-only
directory of git hook wrappers and points `core.hooksPath` at it for every git the
session runs, through git's environment config (GIT_CONFIG_COUNT / GIT_CONFIG_KEY_n /
GIT_CONFIG_VALUE_n): Claude Code's SessionStart hook appends that shell to
$CLAUDE_ENV_FILE. Codex is an OPT-IN: the owner sets the same variables in Codex's
`shell_environment_policy.set` (operations/secret-guard.md). pre-commit,
pre-applypatch, commit-msg and pre-push call `secret-guard.py --git-hook <name>`;
every wrapper then chains to the repository's own hook (git-lfs, husky, pre-commit)
with the same arguments and input. Design: docs/specs/2026-10-20-secret-guard.md;
doctrine: operations/secret-guard.md.

FENCE — no Codex command rewrite. A PreToolUse `updatedInput` prefix was built and
dropped (third review, owner decision D1, 2026-10-20): Codex's exec policy then
judges the whole rewritten `bash -lc` script as one command, so the user's own
prefix rules (a forbidden `git push --force`) stop matching, apply_patch heredoc
interception is lost, and a POSIX prefix breaks every command on Windows.

FENCE — no reference-transaction / post-index-change wrappers (decision D2): they
fire on every ref and index update, and on /mnt/d a wrapper per call took a
30-commit rebase from 11.6 s to 30.4 s and a 200-tag fetch from 4.9 s to 16.3 s
(third review's measurement). A repo's own hooks of those two names do not run
inside AI sessions; operations/secret-guard.md says so.

Why it exists: this system's leaks came through text the AI wrote — real project
names in record entries and a commit SUBJECT (SOUL-169, SOUL-175, SOUL-178), and
a work email in author metadata (SOUL-151). The by-hand pre-push name scan missed
twice (SOUL-178; SOUL-185 nearly passed nine names).

FENCE — git runs the check; nothing PREDICTS what git will do. The first build
parsed the AI's Bash command to guess what a commit or push would contain; two
fresh-context reviews broke the guess again and again (cd inside ( ) or $( ),
GIT_DIR, pushd, a trailing # comment, backslash-newline, quoted <<EOF, git aliases,
`gh repo create --push`, a time-out dropping a found credential). The owner
approved replacing prediction with git's own hooks (2026-10-20). Do not add a
command parser back: the only command-text matching left is the warn-only bypass
notice (--no-verify and friends), which can neither block nor clear anything.

FENCE — names WARN, they never block. SOUL-175 recorded the Body declining a
mechanical forbidden-strings guard in favour of review; that ruling stands for
names. Only credentials (gitleaks) block, and only the OWNER clears a credential
false positive, by approving a `.gitleaksignore` entry. Inline `gitleaks:allow`
comments are ignored (--ignore-gitleaks-allow) so the AI cannot clear one by
editing the file it is committing.

FENCE — a credential may get through only VISIBLY. Every path where the guard does
not actually check says "NOT checked" in one line: gitleaks missing (every hook
run, plus a deduplicated soul.secret_guard.unavailable event), gitleaks erroring
(it exits 0 when its own git call fails — so its stderr is read, never printed), a
push range it cannot resolve, the time budget running out (a credential already
found still blocks), an override file that differs from HEAD, the plugin path gone
(the wrapper says so and still chains), any guard error. Never print a secret
value (gitleaks --redact; only rule/file/line/fingerprint are read), never the line
around a name, and never a NAME-MAP name (SOUL-169/175: the map's names are what
leaked) — any printed word containing one is replaced by its REF token.

Scope: Soul-governed repositories only (the gate's _is_soul_project at the
repository top); elsewhere the wrappers only chain. Fence: hooks/test_secret_guard.py.
"""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]

BLOCK_EXIT = 3      # --git-hook: a credential was found. The wrappers turn it into exit 1;
                    # any other non-zero exit means the guard itself failed (fail open, loudly).
_LEAKS_EXIT = 3     # gitleaks --exit-code: distinct from its own error exit (1)
_MAX_LISTED = 20    # cap each list in a message; the count is always given
BUDGET_GIT_HOOK = 60  # seconds per hook run; the brief's ~60 s. SOUL_GUARD_BUDGET overrides.
GH_CAP = 5          # one `gh repo view`; a hang counts as "could not check" → treated public

# The hook names git runs from core.hooksPath (githooks(5), git 2.43). Once
# core.hooksPath is set git looks ONLY there — a missing name silently runs no hook,
# which would drop the git-lfs pre-push/post-* hooks five adopting projects carry —
# so each gets a wrapper that chains to the repository's own hook. Absent on purpose:
# reference-transaction and post-index-change (cost, see the FENCE above), and
# push-to-checkout (its mere existence replaces git's `updateInstead` worktree
# update; and git clears GIT_CONFIG_COUNT for a local push, so the receiving side
# never sees this dir anyway).
HOOK_NAMES = (
    "applypatch-msg", "pre-applypatch", "post-applypatch", "pre-commit",
    "pre-merge-commit", "prepare-commit-msg", "commit-msg", "post-commit", "pre-rebase",
    "post-checkout", "post-merge", "pre-push", "pre-receive", "update", "proc-receive",
    "post-receive", "post-update", "pre-auto-gc", "post-rewrite",
    "sendemail-validate", "fsmonitor-watchman", "p4-changelist", "p4-prepare-changelist",
    "p4-post-changelist", "p4-pre-submit",
)
# pre-merge-commit is NOT guarded: a merge (a `git pull`) brings in commits that may
# already be public, and blocking it for a remote's existing credential damages
# ordinary git; new commits that arrive by merge, cherry-pick, rebase or revert are
# checked when they are pushed. pre-applypatch (`git am`) is guarded like a commit.
GUARD_HOOKS = ("pre-commit", "pre-applypatch", "commit-msg", "pre-push")
STABLE_NAME = "soul-guard-hooks"
POINTER = "plugin-root"
OWNED = "# soul-guard-wrapper: generated by the Soul System plugin; do not edit (operations/secret-guard.md)"
MISSING_LINE = ("Soul secret check NOT running — plugin path missing; "
                "re-run /soul-init or restart the session")
MIN_GIT = (2, 31)   # GIT_CONFIG_COUNT env config (2.31); --show-scope needs 2.26

USER_LIST_HEADER = """\
# Soul System — private names (user level; never commit this file).
# One entry per line. A line starting with '#' is a comment (a '#' later in a
# line is part of the entry, so 'C# Guild' stays whole); blank lines are ignored.
# Match is literal, case-insensitive and WHOLE-WORD: letters and digits make up a
# word, anything else (space, hyphen, dot, slash, underscore) separates words, so
# 'Acme' matches 'acme-notes.md' but not 'acmeist'. Optional replacement after
# '=>', e.g.:
#   Example Client Ltd => CLIENT-A
# A line starting with '!' is an ALLOWED phrase: masked before matching, so an
# intentionally public phrase containing a listed name does not warn, e.g.:
#   !Example Client Ltd v. State (2019)
# The secret guard WARNS (never blocks) when one of these appears in what the
# AI commits or pushes to a public repo. See operations/secret-guard.md.
"""


class GuardTimeout(Exception):
    """The run's overall budget is spent."""


class CapExpired(Exception):
    """One call hit its own cap while budget remained (e.g. a hung `gh`)."""


_DEADLINE = [None]


def _left(cap):
    if _DEADLINE[0] is None:
        return cap
    left = _DEADLINE[0] - time.monotonic()
    if left <= 0.05:
        raise GuardTimeout()
    return min(cap, left)


_CHILD = [None]   # the running child, so a Ctrl-C / SIGTERM handler can kill its group


def _kill_child_and_exit(signum, frame):
    proc = _CHILD[0]
    if proc is not None:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except OSError:
            pass
    os._exit(128 + signum)


def _run(args, cap, capture_output=False, input=None, **kw):
    """subprocess.run under the deadline. The child gets its own process group, and
    a time-out kills the whole group: killing gitleaks alone leaves its git child
    holding the pipes, and the wait would outlast the budget. (Its own group also
    means a terminal Ctrl-C does not reach it — git_hook_main's signal handler
    kills it instead.)"""
    timeout = _left(cap)
    if capture_output:
        kw["stdout"] = kw["stderr"] = subprocess.PIPE
    kw["stdin"] = subprocess.PIPE if input is not None else kw.get("stdin", subprocess.DEVNULL)
    with subprocess.Popen(args, start_new_session=True, **kw) as proc:
        _CHILD[0] = proc
        try:
            out, err = proc.communicate(input=input, timeout=timeout)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except OSError:
                pass
            proc.communicate()
            _CHILD[0] = None
            if _DEADLINE[0] is not None and _DEADLINE[0] - time.monotonic() <= 0.05:
                raise GuardTimeout()
            raise CapExpired()
        _CHILD[0] = None
    return subprocess.CompletedProcess(args, proc.returncode, out, err)


def _gate():
    spec = importlib.util.spec_from_file_location(
        "soul_completion", ROOT / "hooks" / "pre-completion-verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------- git helpers

def _git(cwd, *args, cap=15):
    return _run(["git", "-c", "core.quotePath=false", "-C", str(cwd), *args], cap,
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})


def _git_out(cwd, *args):
    r = _git(cwd, *args)
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else None


def repo_root(d):
    if d is None or not os.path.isdir(d):
        return None
    out = _git_out(d, "rev-parse", "--show-toplevel")
    return out.strip() if out and out.strip() else None


def is_source_repo(root):
    """The Soul System source repo, by content (same three-file guard as
    tools/codex-project.py and /soul-next step 2b)."""
    p = Path(root)
    return ((p / "findings" / "open").is_dir() and (p / "operations" / "CLAUDE.md").is_file()
            and (p / "SYSTEM-VERSION.md").is_file())


def _inside(path, top):
    try:
        top = os.path.realpath(top)
        return os.path.commonpath([os.path.realpath(path), top]) == top
    except ValueError:
        return False


def soul_scoped(start, gate, top=None):
    """True when `start`, or a folder above it up to its repository's top (just
    `start` outside a repository), is a Soul project — so a session started in a
    subfolder of a Soul repo is armed too."""
    top = top or repo_root(start)
    d = os.path.realpath(start)
    stop = os.path.realpath(top) if top and _inside(d, top) else d
    while True:
        if gate._is_soul_project(d):
            return True
        parent = os.path.dirname(d)
        if d == stop or parent == d:
            return False
        d = parent


def is_soul_vault(root):
    """A Soul vault (tools/vault.py init): every vaulted project's record lives in it,
    so a session commits there from a project folder outside it (SOUL-I079). Scoped on
    structure, not wording, so a retitled vault.md does not drop it out of scope;
    over-scoping a look-alike repo only adds checks."""
    return (os.path.isfile(os.path.join(root, "vault.md"))
            and os.path.isdir(os.path.join(root, "projects")))


def repo_in_scope(root, gate):
    """A repository is checked when its top is a Soul project or a Soul vault, or when
    the session's own folder (SOUL_GUARD_CWD, from the env file) lies inside it and is
    one."""
    if gate._is_soul_project(root) or is_soul_vault(root):
        return True
    c = os.environ.get("SOUL_GUARD_CWD")
    return bool(c) and os.path.isdir(c) and _inside(c, root) and soul_scoped(c, gate, root)


def _added_lines(diff_text):
    """Yield (path, text) for every added line of a -U0 diff. A '\x1e<sha>' line
    (push logs) starts a new commit: yield (None, sha)."""
    path, in_header = None, False
    for ln in diff_text.splitlines():
        if ln.startswith("\x1e"):
            yield None, ln[1:].strip()
            continue
        if ln.startswith("diff --git "):
            in_header = True
            continue
        if in_header:
            if ln.startswith("+++ "):
                p = ln[4:]
                path = None if p == "/dev/null" else (p[2:] if p.startswith("b/") else p)
                in_header = False
            continue
        if ln.startswith("+") and path:
            yield path, ln[1:]


# -------------------------------------------------------------------- name lists

def user_list_path():
    return os.path.join(os.path.expanduser("~"), ".claude", "soul-private-names.txt")


def parse_names(text, label):
    """([(needle, replacement, display)], [allowed phrase]) from the list format.
    '#' starts a comment only at the start of a line, so `C# Guild` stays whole."""
    entries, allows = [], []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("!"):
            if line[1:].strip():
                allows.append(line[1:].strip())
            continue
        needle, _, repl = line.partition("=>")
        needle, repl = needle.strip(), repl.strip() or None
        if needle:
            entries.append((needle, repl, f'"{needle}" ({label})'))
    return entries, allows


# A codename or token is UPPER-CASE with a hyphen (PLANT-BOP, CLIENT-A, REF-07). Only
# such a token right of an arrow is the public replacement side; anything else there
# is treated as a private name (fail toward checking).
_CODENAME = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)+$")


def parse_name_map(text):
    """(entries, rejected rows) from column 2 of registry/NAME-MAP.md: backticked
    identifiers. Right of '→' in a comma item, a codename-shaped token is the
    replacement side and is skipped; any other identifier is a name. Displayed by
    REF id only, never by name — the repo practice for this map (mind item 6c). A
    table row holding identifiers that does not parse is COUNTED, so a reshaped row
    cannot drop names silently (SOUL-185: nine names nearly passed)."""
    entries, rejected = [], 0
    for line in text.splitlines():
        m = re.match(r"^\|\s*(REF-\d+)\s*\|(.*?)\|", line)
        if not m:
            if line.lstrip().startswith("|") and "`" in line:
                rejected += 1
            continue
        ref, col = m.group(1), m.group(2)
        for item in col.split(","):
            left, arrow, right = item.partition("→")
            idents = re.findall(r"`([^`]+)`", left)
            if arrow:
                idents += [t for t in re.findall(r"`([^`]+)`", right)
                           if not _CODENAME.match(t.strip())]
            for ident in idents:
                if ident.strip():
                    entries.append((ident.strip(), f"its token {ref} or codename",
                                    f"NAME-MAP {ref} entry", ref))
    return entries, rejected


def _word(needle):
    """Whole-word pattern: letters and digits form words; anything else separates.
    An edge of the entry that is itself punctuation (`@corp.example`) needs no
    boundary on that side."""
    pat = re.escape(needle)
    if needle[:1].isalnum():
        pat = r"(?<![^\W_])" + pat
    if needle[-1:].isalnum():
        pat += r"(?![^\W_])"
    return re.compile(pat, re.IGNORECASE)


class Names:
    """Compiled name patterns plus the allowed-phrase mask applied before them.

    Matching is WHOLE-WORD for every entry: an identifier that occurs inside an
    ordinary English word would otherwise warn on prose forever (found in this
    repo's own tracked files against a NAME-MAP identifier, 2026-10-20)."""

    def __init__(self, entries, allows):
        self.patterns = [(_word(needle), repl, display) for needle, repl, display in entries]
        allows = sorted(set(allows), key=len, reverse=True)
        self.allow = re.compile("|".join(map(re.escape, allows)), re.IGNORECASE) if allows else None

    def __bool__(self):
        return bool(self.patterns)

    def hits(self, text):
        text = text or ""
        if self.allow:
            text = self.allow.sub(lambda m: " " * len(m.group()), text)
        for pat, repl, display in self.patterns:
            if pat.search(text):
                yield display, repl


class Redactor:
    """Replaces any printed word that contains a NAME-MAP name with its REF token.
    Substring, not whole-word: over-redacting a path segment costs nothing, and a
    name must never reach the transcript (SOUL-169/175)."""

    _SEP = r"[^\s/\\:'\"`,;()\[\]{}<>|=]*"

    def __init__(self, nmap_entries):
        self.rules = [(re.compile(self._SEP + re.escape(e[0]) + self._SEP, re.IGNORECASE), e[3])
                      for e in sorted(nmap_entries, key=lambda e: len(e[0]), reverse=True)]

    def __call__(self, text):
        for pat, ref in self.rules:
            text = pat.sub(f"[{ref}]", text)
        return text


def _name_map_path(root):
    """registry/NAME-MAP.md here, else in the main worktree (a linked worktree of the
    source repo has no copy: the map is gitignored), else None."""
    here = os.path.join(root, "registry", "NAME-MAP.md")
    if os.path.isfile(here):
        return here
    common = (_git_out(root, "rev-parse", "--path-format=absolute", "--git-common-dir") or "").strip()
    if common and os.path.basename(common) == ".git":
        main = os.path.join(os.path.dirname(common), "registry", "NAME-MAP.md")
        if os.path.isfile(main):
            return main
    return None


def load_names(root, notes):
    """(Names, Redactor). The redactor holds NAME-MAP names whatever the repo's
    visibility, so nothing printed in the source repo can carry one."""
    entries, allows, nmap_entries = [], [], []
    upath = user_list_path()
    if not os.path.exists(upath):
        try:
            os.makedirs(os.path.dirname(upath), exist_ok=True)
            with open(upath, "w", encoding="utf-8") as fh:
                fh.write(USER_LIST_HEADER)
            notes.append(f"Created {upath} (empty) — add private names there, one per line.")
        except OSError as exc:
            notes.append(f"Could not create {upath} ({type(exc).__name__}); user-level names NOT checked.")
    else:
        try:
            e, a = parse_names(Path(upath).read_text(encoding="utf-8", errors="replace"), "user list")
            entries += e
            allows += a
        except OSError:
            notes.append(f"Could not read {upath}; user-level names NOT checked.")
    proj = os.path.join(root, ".soul", "private-names.txt")
    if os.path.isfile(proj):
        e, a = parse_names(Path(proj).read_text(encoding="utf-8", errors="replace"), "project list")
        entries += e
        allows += a
    nmap = _name_map_path(root) if is_source_repo(root) else None
    if is_source_repo(root) and nmap is None:
        notes.append("registry/NAME-MAP.md is absent here and in the main worktree — NAME-MAP "
                     "names are NOT checked.")
    if nmap:
        nmap_entries, rejected = parse_name_map(Path(nmap).read_text(encoding="utf-8", errors="replace"))
        entries += [e[:3] for e in nmap_entries]
        if rejected:
            notes.append(f"NAME-MAP: {rejected} table row(s) holding identifiers did not parse "
                         "as `| REF-nn | … |` — their names were NOT checked.")
    return Names(entries, allows), Redactor(nmap_entries)


# The name lists a Soul vault keeps on purpose (check_pre_commit).
VAULT_LISTS = re.compile(r"^(?:projects/[^/]+/soul/private-names\.txt"
                         r"|machine/soul-private-names\.txt"
                         r"|projects/[^/]+/registry/NAME-MAP\.md)$")


def _name_list_file(path):
    base = os.path.basename(path)
    return base.endswith("private-names.txt") or base == "NAME-MAP.md"


# ------------------------------------------------------------------ session state

def _state_dir():
    """A per-user 0700 directory, or None when one cannot be trusted: a cache another
    user could write could mark a repo PRIVATE and silence the name check."""
    d = os.path.join(tempfile.gettempdir(), f"soul-secret-guard-{os.getuid()}")
    try:
        os.makedirs(d, mode=0o700, exist_ok=True)
        st = os.lstat(d)
        if (not stat.S_ISDIR(st.st_mode) or st.st_uid != os.getuid()
                or st.st_mode & 0o077):
            return None
        return d
    except OSError:
        return None


def _session():
    """The session the env file or Codex prefix named; hand commits share a day."""
    return os.environ.get("SOUL_GUARD_SESSION") or "git-hook-" + time.strftime("%Y%m%d")


def _state_path():
    d = _state_dir()
    if d is None:
        return None
    return os.path.join(d, hashlib.sha256(_session().encode()).hexdigest()[:16] + ".json")


def _load_state():
    path = _state_path()
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError, TypeError):
        return {}


def _save_state(state):
    path = _state_path()
    if path is None:
        return
    try:
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path))
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(state, fh)
        os.replace(tmp, path)
    except OSError:
        pass


def _github_slug(url):
    m = re.search(r"github\.com[:/]+([^/\s]+)/([^/\s]+?)(?:\.git)?/?$", url or "")
    return f"{m.group(1)}/{m.group(2)}" if m else None


def _remote_url(root, remote):
    """A configured remote's fetch URL; a pushed-to URL is its own answer."""
    if not remote:
        return ""
    out = _git_out(root, "remote", "get-url", remote)
    return out.strip() if out else remote


def is_public(root, url, rep=None):
    """True unless `gh` says PRIVATE or INTERNAL for this GitHub URL. Fails toward
    checking: no gh, no remote, a non-GitHub URL, any gh error or a hang (GH_CAP)
    all count as possibly public. Cached per repo and URL for the session."""
    key = f"{root}|{url}"
    state = _load_state()
    cache = state.setdefault("visibility", {})
    if key not in cache:
        vis = None
        gh = shutil.which("gh")
        slug = _github_slug(url)
        if gh and slug:
            try:
                r = _run([gh, "repo", "view", slug, "--json", "visibility"], GH_CAP, cwd=root,
                         capture_output=True, env={**os.environ, "GH_PROMPT_DISABLED": "1"})
                if r.returncode == 0:
                    vis = json.loads(r.stdout.decode("utf-8", "replace")).get("visibility")
            except (OSError, ValueError, CapExpired):
                vis = None
        cache[key] = vis or "UNKNOWN"
        _save_state(state)
    if rep is not None:
        rep.visibility = cache[key]
    return cache[key] not in ("PRIVATE", "INTERNAL")


def _default_remote(root):
    up = _git_out(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if up and "/" in up.strip():
        return up.strip().split("/", 1)[0]
    remotes = (_git_out(root, "remote") or "").split()
    return "origin" if "origin" in remotes else (remotes[0] if remotes else None)


# ---------------------------------------------------------------------- gitleaks

def gitleaks(root, log_opts=None):
    """(status, findings, errored). status: 'clean'|'leaks'|'missing'. errored is
    True when gitleaks reported any error: it exits 0 when its own git call fails
    (a bad range, a corrupt index — "0 commits scanned"), so stderr is read, never
    printed, and any output there at --log-level error means "not checked".
    `--pre-commit --staged` reads the index git hands the hook (GIT_INDEX_FILE), so
    `commit -a` and `commit <paths>` are scanned as git will commit them."""
    exe = shutil.which("gitleaks")
    if not exe:
        return "missing", [], False
    with tempfile.TemporaryDirectory() as tmp:
        report = os.path.join(tmp, "report.json")
        args = [exe, "git", "--redact", "--no-banner", "--no-color", "--ignore-gitleaks-allow",
                "--exit-code", str(_LEAKS_EXIT), "--log-level", "error",
                "--gitleaks-ignore-path", root, "--report-format", "json", "--report-path", report]
        args += ["--pre-commit", "--staged"] if log_opts is None else [f"--log-opts={log_opts}"]
        try:
            r = _run(args + [root], 600, cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        except (OSError, CapExpired):
            return "clean", [], True
        errored = bool(r.stderr.strip()) or r.returncode not in (0, _LEAKS_EXIT)
        if r.returncode != _LEAKS_EXIT:
            return "clean", [], errored
        try:
            with open(report, encoding="utf-8") as fh:
                raw = json.load(fh)
        except (OSError, ValueError):
            raw = [{"RuleID": "unknown", "File": "?", "StartLine": "?",
                    "Fingerprint": "(report unreadable)"}]
    keep = ("RuleID", "File", "StartLine", "Commit", "Fingerprint")
    return "leaks", [{k: f.get(k) for k in keep} for f in raw], errored


# ------------------------------------------------------------------------ checks

class Report:
    def __init__(self):
        self.leaks, self.names, self.notes, self.files = [], [], [], []
        self.unavailable = False
        self.visibility = None
        self.first_push = False
        self.redact = lambda s: s

    def add_name_hits(self, names, text, where):
        for display, repl in names.hits(text):
            hit = (display, where, repl)
            if hit not in self.names:
                self.names.append(hit)

    def note(self, line):
        if line not in self.notes:
            self.notes.append(line)


def _scan_leaks(rep, root, log_opts=None, what="staged changes"):
    try:
        status, found, errored = gitleaks(root, log_opts)
    except GuardTimeout:
        rep.note(f"credential scan of {what} timed out — NOT checked.")
        raise
    if status == "missing":
        rep.unavailable = True
        return
    if errored:
        rep.note(f"credential scan of {what} FAILED (gitleaks reported an error) — NOT checked; "
                 "run `gitleaks git` by hand before relying on this.")
    rep.leaks.extend(found)


def gitleaks_text(root, text):
    """(status, findings, errored) for message text, via `gitleaks stdin` (8.30.1).
    `git log -p` carries no commit messages and no tag objects, so `gitleaks git`
    never sees them (fourth review: `git commit -m "deploy: use key …"` committed and
    pushed silently). Its .gitleaksignore lookup is pointed at an empty folder: the
    stdin fingerprint is only `:rule:line`, so message findings carry the guard's own
    fingerprint and are cleared by message_ignored() instead."""
    exe = shutil.which("gitleaks")
    if not exe:
        return "missing", [], False
    with tempfile.TemporaryDirectory() as tmp:
        report = os.path.join(tmp, "report.json")
        args = [exe, "stdin", "--redact", "--no-banner", "--no-color", "--ignore-gitleaks-allow",
                "--exit-code", str(_LEAKS_EXIT), "--log-level", "error",
                "--gitleaks-ignore-path", tmp, "--report-format", "json", "--report-path", report]
        try:
            r = _run(args, 600, cwd=root, input=text.encode("utf-8", "replace"),
                     stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        except (OSError, CapExpired):
            return "clean", [], True
        errored = bool(r.stderr.strip()) or r.returncode not in (0, _LEAKS_EXIT)
        if r.returncode != _LEAKS_EXIT:
            return "clean", [], errored
        try:
            with open(report, encoding="utf-8") as fh:
                raw = json.load(fh)
        except (OSError, ValueError):
            raw = [{"RuleID": "unknown", "StartLine": 0}]
    return "leaks", [{"RuleID": f.get("RuleID"), "StartLine": f.get("StartLine"),
                      "EndLine": f.get("EndLine")} for f in raw], errored


def _message_fingerprint(rule, lines):
    """Stable, value-free id for a credential in a message: the owner can approve it as
    a .gitleaksignore line, and the same finding gives the same id at commit-msg and
    at pre-push. A 64-bit prefix of a SHA-256 over EVERY line of the finding, first to
    last, each with trailing whitespace removed (git's cleanup does the same, so the
    commit-msg file and `git log %B` agree). Hashing only the first line gave every
    private key the same id — its BEGIN line (fifth review)."""
    text = "\n".join(ln.rstrip() for ln in lines)
    return f"message:{rule}:{hashlib.sha256(text.encode('utf-8', 'replace')).hexdigest()[:16]}"


def message_ignored(root):
    try:
        text = Path(os.path.join(root, ".gitleaksignore")).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    return {ln.strip() for ln in text.splitlines() if ln.strip().startswith("message:")}


def scan_messages(rep, root, items, what):
    """Credentials in message texts: items = [(label, text)], one gitleaks run for all.
    Findings carry the label (e.g. "commit 1a2b3c4 message") and the line within it."""
    rows = []      # one per blob line: (label, line number in its message, text)
    for label, text in items:
        for i, ln in enumerate((text or "").splitlines(), 1):
            rows.append((label, i, ln))
    if not rows:
        return
    try:
        status, found, errored = gitleaks_text(root, "\n".join(r[2] for r in rows) + "\n")
    except GuardTimeout:
        rep.note(f"credential scan of {what} timed out — NOT checked.")
        raise
    if status == "missing":
        rep.unavailable = True
        return
    if errored:
        rep.note(f"credential scan of {what} FAILED (gitleaks reported an error) — NOT checked.")
    ignored = message_ignored(root)
    for f in found:
        try:
            start = int(f.get("StartLine"))
            end = max(start, int(f.get("EndLine") or start))
            label, n, _ = rows[start - 1]
            span = [r[2] for r in rows[start - 1:end] if r[0] == label]
        except (TypeError, ValueError, IndexError):
            label, n, span = what, "?", []
        fp = _message_fingerprint(f.get("RuleID"), span)
        if fp not in ignored:
            rep.leaks.append({"RuleID": f.get("RuleID"), "File": label, "StartLine": n, "Fingerprint": fp})


def _override_notes(rep, root):
    """An override file whose bytes on disk differ from HEAD clears findings before
    anyone reviews it. Bytes, not `git status`: an ignored or skip-worktree file
    reads as clean there while gitleaks still applies it."""
    for name in (".gitleaksignore", ".gitleaks.toml"):
        path = os.path.join(root, name)
        if not os.path.isfile(path):
            continue
        try:
            disk = Path(path).read_bytes()
        except OSError:
            disk = None
        head = _git(root, "show", f"HEAD:{name}")
        if disk is None or head.returncode != 0 or head.stdout != disk:
            rep.note(f"{name} differs from HEAD (untracked, ignored, skip-worktree, modified or "
                     "staged) — its entries already clear findings in this scan but are not in "
                     "review yet; confirm the owner approved them.")
    for var in ("GITLEAKS_CONFIG", "GITLEAKS_CONFIG_TOML"):
        if os.environ.get(var):
            rep.note(f"${var} is set — gitleaks is using a config from outside the repo.")


def _identity_emails(root):
    """Author and committer email of the commit being made (git exports --author
    and amend identities to the hook; `git var` reads env and config as git does)."""
    out = []
    for var in ("GIT_AUTHOR_IDENT", "GIT_COMMITTER_IDENT"):
        ident = _git_out(root, "var", var) or ""
        m = re.search(r"<([^>]*)>", ident)
        if m:
            out.append(m.group(1))
    return out


def check_pre_commit(rep, root, names):
    _override_notes(rep, root)
    _scan_leaks(rep, root)
    out = _git_out(root, "diff", "--cached", "--name-only", "-z", "--diff-filter=d") or ""
    paths = [p for p in out.split("\0") if p]
    # A vault keeps each project's list on purpose (ADR 0001): it arms the guard on
    # the next machine. So too the machine-wide list (machine/, which
    # ~/.claude/soul-private-names.txt links to) and Soul-System's private registry
    # kept in its vault folder (SOUL-225). Lists anywhere else in it are still flagged.
    vault = is_soul_vault(root)
    rep.files = [p for p in paths if _name_list_file(p) and not (
        vault and VAULT_LISTS.match(p))]
    if not names or not is_public(root, _remote_url(root, _default_remote(root)), rep):
        return
    # Nor are those lists scanned for the names they hold (the owner's call, v3.6.3): a
    # list is made of names, so every commit of one warned. Every other vault file is.
    kept = lambda p: vault and bool(VAULT_LISTS.match(p or ""))
    for p in paths:
        if not kept(p):
            rep.add_name_hits(names, p, f"file {p}")
    diff = _git_out(root, "diff", "--cached", "--no-ext-diff", "--no-color", "-U0",
                    "--diff-filter=d") or ""
    for path, text in _added_lines(diff):
        if not kept(path):
            rep.add_name_hits(names, text, f"file {path}")
    rep.add_name_hits(names, "\n".join(_identity_emails(root)), "author/committer email")


def _message_text(root, path):
    """The message as git will keep it. git drops comment lines only in `strip` mode,
    which is the default only when an editor was used; with -m / -F and no editor
    (git then runs the hook with GIT_EDITOR=:) it keeps `#` lines, so they are
    checked. `scissors` keeps comments but cuts at the scissors line when editing.
    A --cleanup flag on the command line is invisible to the hook: in that case the
    config/editor answer is used, and every unclear case keeps every line."""
    text = Path(path if os.path.isabs(path) else os.path.join(os.getcwd(), path)).read_text(
        encoding="utf-8", errors="replace")
    editor = os.environ.get("GIT_EDITOR") != ":"
    mode = ((_git_out(root, "config", "commit.cleanup") or "default").strip() or "default").lower()
    strip = mode == "strip" or (mode == "default" and editor)
    cut = strip or (mode == "scissors" and editor)
    if not (strip or cut):
        return text
    char = ((_git_out(root, "config", "core.commentChar") or "#").strip() or "#")[:1]
    if char == "a":  # core.commentChar=auto: git picks an unused one — keep every line
        return text
    kept = []
    for ln in text.splitlines():
        if ln.startswith(char):
            if re.match(re.escape(char) + r" -+ >8 -+$", ln):
                break
            if strip:
                continue
        kept.append(ln)
    return "\n".join(kept)


def check_commit_msg(rep, root, argv, names):
    if not argv:
        rep.note("commit-msg hook got no message file — the commit message was NOT checked.")
        return
    try:
        msg = _message_text(root, argv[0])
    except OSError:
        rep.note("could not read the commit message file — the commit message was NOT checked.")
        return
    scan_messages(rep, root, [("commit message", msg)], "the commit message")
    if names and is_public(root, _remote_url(root, _default_remote(root)), rep):
        rep.add_name_hits(names, msg, "commit message")


_ZERO = re.compile(r"^0+$")


def _norm_url(u):
    u = (u or "").strip().rstrip("/")
    if u.startswith("file://"):
        u = u[len("file://"):]
    return os.path.realpath(u) if u and os.path.exists(u) else u


def _remote_urls(root, name, key):
    """remote.<name>.<key> values in config order (git fetches from the first url)."""
    out = _git_out(root, "config", "--get-all", f"remote.{name}.{key}") or ""
    return [_norm_url(u) for u in out.splitlines() if u.strip()]


def _target_remote(root, remote, url):
    """The configured remote whose tracking refs describe where this push goes, or None
    (a first push: all history). Tracking refs come from the FIRST url only (git fetches
    from it), while a push goes to every pushurl — or, with none, to every url — so:
    by name (git's $1), only a remote with exactly one url and no pushurl other than it;
    by URL (git's $2), only when it equals a remote's first url as `git remote get-url`
    reports it (insteadOf applied). Anything else is a first push. Errs toward checking
    (the owner's N5 rule): an old key reached a pushurl mirror (sixth review) and an
    extra-url mirror (seventh review) silently."""
    names = (_git_out(root, "remote") or "").split()
    if remote in names:
        urls = _remote_urls(root, remote, "url")
        push = set(_remote_urls(root, remote, "pushurl")) or set(urls)
        return remote if len(urls) == 1 and push <= set(urls) else None
    want = {_norm_url(u) for u in (remote, url) if u}
    for name in names:
        first = (_git_out(root, "remote", "get-url", name) or "").strip()
        if first and _norm_url(first) in want:
            return name
    return None


def _push_range(root, remote, lines, url=""):
    """(positives, negatives, labels, tags, first_push, skipped) for git's pre-push ref
    lines.

    A deletion (local sha all zeros) sends nothing. An update excludes the remote's old
    tip when this repo has it; a new ref (or an old tip this repo lacks) excludes what
    the target remote's tracking refs hold (`--remotes=<name>`) when _target_remote()
    says they describe the push target, and nothing otherwise — a first push, all
    history. No argument ever carries a path, so the joined --log-opts cannot split on
    a space. One combined range: excluding commits already on the target removes
    nothing being sent. tags: [(ref, sha)] of annotated tag objects being pushed.
    first_push: some new ref's range is all history. skipped: [(ref, "blob"|"tree")]
    for refs that name no commit; they are left out of the range and reported. One
    `cat-file --batch-check` answers every old tip and every local object type."""
    name = _target_remote(root, remote, url)
    # A configured remote: exclude what its tracking refs hold. Any other target is a
    # first push — nothing is excluded, all history is checked (the owner's N5 rule,
    # applied to URLs too: excluding "what any remote holds" let an old key on a
    # private origin go unscanned to a new mirror, fifth review).
    fallback = f"--remotes={name}" if name else None
    pos, labels, olds, lrefs = [], [], [], []
    for ln in lines:
        parts = ln.split()
        if len(parts) != 4:
            continue
        lref, lsha, rref, rsha = parts
        if _ZERO.match(lsha):
            continue
        pos.append(lsha)
        lrefs.append(lref)
        labels.append(f"{lref} -> {rref}")
        olds.append(None if _ZERO.match(rsha) else rsha)
    asked = list(dict.fromkeys(o for o in olds if o))
    queries = [f"{o}^{{commit}}" for o in asked] + pos
    answers = []
    if queries:
        r = _run(["git", "-C", str(root), "cat-file", "--batch-check"], 30, capture_output=True,
                 input="".join(q + "\n" for q in queries).encode(),
                 env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
        answers = r.stdout.decode("utf-8", "replace").splitlines()
    answers += [""] * (len(queries) - len(answers))
    have = {o for o, a in zip(asked, answers) if " commit " in a and not a.endswith(" missing")}
    types = answers[len(asked):]
    tags = [(lref, sha) for lref, sha, t in zip(lrefs, pos, types) if " tag " in t]
    # What each pushed ref finally names (a tag peeled to its end). Only commits enter the
    # range; a blob or tree pushed under a ref is said plainly, never passed silently
    # (sixth review: tag → blob / tree and lightweight tag → blob carried a key out).
    peeled = types
    if tags:
        r = _run(["git", "-C", str(root), "cat-file", "--batch-check"], 30, capture_output=True,
                 input="".join(f"{sha}^{{}}\n" if " tag " in t else f"{sha}\n"
                               for sha, t in zip(pos, types)).encode(),
                 env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
        peeled = r.stdout.decode("utf-8", "replace").splitlines()
        peeled += [""] * (len(pos) - len(peeled))
    skipped = []
    keep = []
    for i, (lref, t) in enumerate(zip(lrefs, peeled)):
        kind = next((k for k in ("blob", "tree") if f" {k} " in t), None)
        if kind:
            skipped.append((lref if lref != pos[i] else f"object {pos[i]} -> {labels[i].split(' -> ', 1)[-1]}",
                            kind))
        else:
            keep.append(i)
    pos, labels, olds = [pos[i] for i in keep], [labels[i] for i in keep], [olds[i] for i in keep]
    neg = [o if o in have else fallback for o in olds]
    whole = any(n is None for n in neg)          # a new ref to an unknown target
    first_push = whole or (fallback in neg and not (_git_out(
        root, "for-each-ref", "--count=1", "--format=x", f"refs/remotes/{name}/") or "").strip())
    return pos, list(dict.fromkeys(n for n in neg if n)), labels, tags, first_push, skipped


_TAG_DEPTH = 10


def _tag_chain(rep, root, ref, sha):
    """[(label, message)] for an annotated tag and every tag object it points at in
    turn (a tag of a tag), up to _TAG_DEPTH. Only the outer tag has a ref line, so an
    inner tag's message reached the remote unscanned (fifth review). A read failure or
    a deeper chain says NOT checked."""
    out, name = [], ref.replace("refs/tags/", "", 1)
    for _ in range(_TAG_DEPTH):
        raw = _git_out(root, "cat-file", "tag", sha)
        if raw is None:
            rep.note(f"could not read a tag object under {name} — its message was NOT checked.")
            return out
        head, _, msg = raw.partition("\n\n")
        inner = re.search(r"^tag (.+)$", head, re.M)
        out.append((f"tag {inner.group(1) if inner else name} message", msg))
        kind = re.search(r"^type (\S+)$", head, re.M)
        obj = re.search(r"^object (\S+)$", head, re.M)
        if not (kind and obj and kind.group(1) == "tag"):
            return out
        sha = obj.group(1)
    rep.note(f"tag {name} nests more than {_TAG_DEPTH} tags deep — the inner tag messages were "
             "NOT checked.")
    return out


def _printable(text):
    """A ref or label for a one-line notice: control characters (a newline would split
    the line) shown as escapes."""
    return re.sub(r"[\x00-\x1f\x7f]", lambda m: f"\\x{ord(m.group()):02x}", text)


def check_pre_push(rep, root, argv, stdin_text, names):
    remote = argv[0] if argv else None
    url = argv[1] if len(argv) > 1 else ""
    lines = [ln for ln in stdin_text.splitlines() if ln.strip()]
    pos, neg, labels, tags, first_push, skipped = _push_range(root, remote, lines, url)
    # A ref naming a blob or tree (directly, or at the end of a tag chain) is NOT scanned —
    # said plainly, never passed. An in-process content scan was built and dropped (ninth
    # review): path-only gitleaks rules never fire on stdin, a finding could span two files
    # and name the wrong one, and many paths to one blob blew the time and memory budget.
    # A printed by-hand command was dropped before that: it kept growing traps (subfolder
    # scope, attributes, a config in the tree, allow comments). Such a ref takes deliberate
    # plumbing (`hash-object -w`, then `git tag`); the module's rule asks that it be VISIBLE.
    # The annotated tags on the way still have their messages scanned (_tag_chain).
    for ref, kind in skipped:
        rep.note(f"NOT checked — {_printable(ref)} points at a {kind}; only commits and tag messages "
                 "are scanned on push. Do not push it until its content has been checked.")
    if not pos and not tags:
        return
    rargs = pos + (["--not"] + neg if neg else [])
    count = _git_out(root, "rev-list", "--count", *rargs, "--") if pos else "0"
    if count is None:
        rep.note(f"could not resolve the outgoing commits for {', '.join(labels)} — NOT checked.")
        return
    if count.strip() == "0" and not tags:
        return
    rep.first_push = first_push
    _override_notes(rep, root)
    what = f"outgoing commits ({', '.join(labels)})"
    if count.strip() != "0":
        _scan_leaks(rep, root, log_opts=" ".join(rargs), what=what)
    log = (_git_out(root, "log", "--format=%x1e%H%x1f%ae%x1f%ce%x1f%B", *rargs, "--") or "") if pos else ""
    commits = [(rec.split("\x1f", 3) + ["", "", ""])[:4] for rec in log.split("\x1e")[1:]]
    tag_items = [item for ref, sha in tags for item in _tag_chain(rep, root, ref, sha)]
    scan_messages(rep, root,
                  [(f"commit {sha[:7]} message", body) for sha, _, _, body in commits] + tag_items,
                  f"the messages of {what}")
    # Visibility of the repository git actually pushes to: its $2, not the fetch url.
    vis_url = url or _remote_url(root, remote)
    if not names or not is_public(root, vis_url, rep):
        return
    for sha, ae, ce, body in commits:
        short = sha[:7]
        rep.add_name_hits(names, body, f"commit {short} message")
        rep.add_name_hits(names, f"{ae}\n{ce}", f"commit {short} author/committer email")
    for label, msg in tag_items:
        rep.add_name_hits(names, msg, label)
    if not pos:
        return  # tags only: `git log` with no positive ref would read HEAD's history
    files = _git_out(root, "log", "--name-only", "-z", "--diff-filter=d", "--format=%x1e%H",
                     *rargs, "--") or ""
    short = "?"
    for chunk in files.split("\0"):
        for ln in chunk.split("\n"):
            if ln.startswith("\x1e"):
                short = ln[1:8]
            elif ln.strip():
                rep.add_name_hits(names, ln, f"commit {short} file {ln}")
    diff = _git_out(root, "log", "-p", "--no-ext-diff", "--no-color", "-U0", "--diff-filter=d",
                    "--format=%x1e%H", *rargs, "--") or ""
    for path, text in _added_lines(diff):
        if path is None:
            short = text[:7]
        else:
            rep.add_name_hits(names, text, f"commit {short} file {path}")


# ----------------------------------------------------------------------- output

_OVERRIDE = (
    "If a finding is a false positive, ONLY THE OWNER can clear it: ask them to approve "
    "adding its fingerprint (shown above) as one line in .gitleaksignore at the repo root, "
    "committed so it is visible in review. A credential in a message is better reworded "
    "(`git commit --amend`, or rebase for an older commit) than ignored. Do NOT add a .gitleaksignore entry, a "
    "gitleaks:allow comment or a config allowlist yourself, and do not bypass the hook "
    "(contract rule 8 — overrides happen out loud). If it is a real credential: "
    "unstage/remove it, rotate it, and keep it out of history.")


_FIRST_PUSH = (
    "First push to this remote — all history was checked (the target is a URL that is no "
    "configured remote's first url, a remote with several urls or a pushurl other than its "
    "url, or a remote with no remote-tracking refs yet: a new backup mirror, "
    "`gh repo create --push`). "
    "A credential already rotated is cleared by the owner approving its fingerprint in "
    ".gitleaksignore; it still blocks until then (owner's decision, 2026-10-20).")


def _bullets(items):
    lines = [f"  - {x}" for x in items[:_MAX_LISTED]]
    if len(items) > _MAX_LISTED:
        lines.append(f"  - … and {len(items) - _MAX_LISTED} more")
    return lines


def render(rep, kind, root):
    """The report as text (redacted), or '' when there is nothing to say."""
    name = os.path.basename(root)
    lines = []
    if rep.leaks:
        lines.append(f"Soul secret guard BLOCKED this git {kind} in {name}: "
                     f"{len(rep.leaks)} credential finding(s) (values redacted).")
        lines += _bullets([
            f"{f.get('RuleID')} in {f.get('File')}:{f.get('StartLine')}"
            + (f" (commit {str(f.get('Commit'))[:7]})" if f.get("Commit") else "")
            + f" — fingerprint {f.get('Fingerprint')}" for f in rep.leaks])
        if rep.first_push:
            lines.append(_FIRST_PUSH)
        lines.append(_OVERRIDE)
    if rep.unavailable:
        lines.append("Soul secret guard: credential scan NOT running — gitleaks not installed. "
                     f"This git {kind} was NOT checked for credentials. Install gitleaks "
                     "(see operations/secret-guard.md).")
    if rep.names:
        vis = ("a PUBLIC repo" if rep.visibility == "PUBLIC" else
               "a repo whose visibility could not be checked (treated as public)")
        lines.append(f"Soul secret guard (warning, not blocking): private names in what this "
                     f"git {kind} sends from {name}, {vis}:")
        lines += _bullets([f"{d} in {w}" + (f" → suggest {r}" if r else "")
                           for d, w, r in rep.names])
        lines.append("The owner decides; names warn and never block (SOUL-175).")
    if rep.files:
        lines.append("Soul secret guard (warning): a private-name list is staged for commit — "
                     "it should stay out of git:")
        lines += _bullets(rep.files)
    lines += [f"Soul secret guard: {n}" for n in rep.notes]
    return rep.redact("\n".join(lines))


# ------------------------------------------------------------------- git hook entry

def _budget():
    try:
        return float(os.environ.get("SOUL_GUARD_BUDGET") or BUDGET_GIT_HOOK)
    except ValueError:
        return BUDGET_GIT_HOOK


def _unavailable_event(root, gate):
    """One soul.secret_guard.unavailable event per repo per session (per day for hand
    commits). The printed line repeats on every hook run; the record does not need to."""
    state = _load_state()
    said = state.setdefault("unavailable_events", [])
    if root in said:
        return
    said.append(root)
    _save_state(state)
    gate._emit_event(root, {"session_id": os.environ.get("SOUL_GUARD_SESSION")},
                     "soul.secret_guard.unavailable", {
                         "gate": "secret_guard", "finding": "SOUL-I070",
                         "outcome": "allowed_unscanned", "reason": "gitleaks not installed"})


def git_hook_main(hook, argv, stdin_text=""):
    """`secret-guard.py --git-hook <name> [git's hook args]`. Returns BLOCK_EXIT when
    a credential is found (the wrapper exits 1), else 0; reports go to stderr."""
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, _kill_child_and_exit)  # Ctrl-C must not leave gitleaks running
    _DEADLINE[0] = time.monotonic() + _budget()
    rep, root = Report(), None
    kind = {"pre-push": "push", "pre-applypatch": "am"}.get(hook, "commit")
    try:
        root = repo_root(os.getcwd())
        if root is None:
            return 0
        gate = _gate()
        if hook not in GUARD_HOOKS or not repo_in_scope(root, gate):
            return 0  # out of scope: the wrapper only chains
        try:
            # Names (and the NAME-MAP redactor) first, so nothing printed after a
            # time-out or error can carry a NAME-MAP name.
            names, rep.redact = load_names(root, rep.notes)
            if hook in ("pre-commit", "pre-applypatch"):
                check_pre_commit(rep, root, names)
            elif hook == "commit-msg":
                check_commit_msg(rep, root, argv, names)
            else:
                check_pre_push(rep, root, argv, stdin_text, names)
        except GuardTimeout:
            rep.note(f"timed out (budget {_budget():g} s) — this git {kind} was NOT fully "
                     "checked; run `gitleaks git` by hand before relying on it."
                     + (" The credential(s) already found still block." if rep.leaks else ""))
        _DEADLINE[0] = None
        if rep.unavailable:
            _unavailable_event(root, gate)
        text = render(rep, kind, root)
        if text:
            print(text, file=sys.stderr)
        return BLOCK_EXIT if rep.leaks else 0
    except Exception as exc:
        # A credential already found still blocks; otherwise fail open, loudly.
        rep.note(f"skipped ({type(exc).__name__}) — this git {kind} was NOT "
                 f"{'fully ' if rep.leaks else ''}checked.")
        if root:
            print(render(rep, kind, root), file=sys.stderr)
        else:
            print(f"Soul secret guard: {rep.notes[-1]}", file=sys.stderr)
        return BLOCK_EXIT if rep.leaks else 0
    finally:
        _DEADLINE[0] = None


def _wrapper_ran(hook):
    """True only when the session's wrapper for this hook, in this repo, PASSED the check
    and exec'd into the hand hook that is our parent process. A marker set anywhere
    else names another process: `exec git …` makes git's ID equal the shell's `$$`,
    and git is the hand hook's parent, not ours — so only the parent may match (the
    grandparent once did, and a forged commit and push got through, fifth review)."""
    mark = os.environ.get("SOUL_GUARD_ACTIVE", "")
    head, _, pid = mark.rpartition(":")
    name, _, path = head.partition(":")
    if name != hook or not pid.isdigit() or os.path.realpath(path or "/nonexistent") != os.path.realpath(os.getcwd()):
        return False
    return int(pid) == os.getppid()


def own_hooks_dir(cwd):
    """The repository's own hooks directory, resolved as the wrappers resolve it: the
    last core.hooksPath that is not command scope (the session's env entry is), else
    <git-common-dir>/hooks. A relative core.hooksPath is relative to the folder hooks
    run in — the worktree top — not to `cwd`. For /soul-init, which must not install
    into the stable dir (inside a session `git rev-parse --git-path hooks` names it)."""
    def git(*args):
        return subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True).stdout
    path = ""
    for ln in git("config", "--show-scope", "--path", "--get-all", "core.hooksPath").splitlines():
        scope, _, val = ln.partition("\t")
        if scope != "command":
            path = val
    if path:
        top = git("rev-parse", "--show-toplevel").strip() or os.path.abspath(cwd)
        return os.path.normpath(os.path.join(top, os.path.expanduser(path)))
    common = git("rev-parse", "--path-format=absolute", "--git-common-dir").strip()
    return os.path.normpath(os.path.join(common, "hooks")) if common else None


# ---------------------------------------------------------------- stable hooks dir

def _sq(s):
    """Single-quote for POSIX sh."""
    return "'" + s.replace("'", "'\"'\"'") + "'"


def stable_dir(data_dir=None):
    """One folder per plugin copy (named by a short hash of this copy's root). Two
    copies — a plugin update while another session stays open — shared one folder
    and rewrote each other's pointer on every command (fourth review); separate
    folders cannot flap. A session's env file names its own copy's folder."""
    data_dir = data_dir or os.environ.get("CLAUDE_PLUGIN_DATA")
    name = f"{STABLE_NAME}-{hashlib.sha256(str(ROOT).encode()).hexdigest()[:8]}"
    if data_dir:
        return os.path.join(data_dir, name)
    return os.path.join(os.path.expanduser("~"), ".claude", name)


# The wrapper uses shell builtins, git, and `cat` for pre-push only (one linear read
# of git's ref lines, which go to the guard and then to the chained hook). Every other
# hook execs the chained one with stdin untouched (proc-receive speaks a protocol on
# it). Line 2 marks the file as owned: install() may replace or remove only such
# files, and the chain never runs one (a copied wrapper would otherwise call itself).
_WRAPPER = r"""#!/bin/sh
@OWNED@
# Git hook wrapper for '@HOOK@' (SOUL-I070, experimental). Runs the secret guard
# (pre-commit, pre-applypatch, commit-msg, pre-push only), then ALWAYS the
# repository's own hook with the same arguments and input, exiting with its status.
hook=@HOOK@
dir=@DIR@
refs=
if [ "$hook" = pre-push ]; then
  refs=$(cat; echo .)
  refs=${refs%.}
fi
case " pre-commit pre-applypatch commit-msg pre-push " in
*" $hook "*)
  # Always checks: a marker set from outside must not skip it (fourth review —
  # `SOUL_GUARD_ACTIVE=… git commit` committed a staged credential), so it is cleared
  # first. It is set again — bound to this process ID — only after the guard PASSED,
  # so a /soul-init hand hook this wrapper chains to may skip a second run; when the
  # plugin copy is gone or the guard failed, the hand hook must check (fifth review:
  # a session armed from a deleted copy committed a key past a live hand hook).
  unset SOUL_GUARD_ACTIVE
  root=
  [ -r "$dir/@POINTER@" ] && IFS= read -r root < "$dir/@POINTER@"
  if [ -n "$root" ] && [ -f "$root/hooks/secret-guard.py" ] && command -v python3 >/dev/null 2>&1; then
    if [ "$hook" = pre-push ]; then
      printf '%s' "$refs" | python3 "$root/hooks/secret-guard.py" --git-hook "$hook" "$@"
    else
      python3 "$root/hooks/secret-guard.py" --git-hook "$hook" "$@"
    fi
    rc=$?
    [ "$rc" -eq @BLOCK@ ] && exit 1
    if [ "$rc" -eq 0 ]; then
      SOUL_GUARD_ACTIVE="$hook:$(pwd -P):$$"
      export SOUL_GUARD_ACTIVE
    else
      echo "Soul secret guard failed (exit $rc) — this git $hook was NOT checked" >&2
    fi
  else
    echo "@MISSING@" >&2
  fi
  ;;
esac
# Chain: the repo's own hooks dir — the last core.hooksPath NOT set on the command
# line or by env (that one is this dir), else <git-common-dir>/hooks.
tab=$(printf '\t')
cfg=$(git config --show-scope --path --get-all core.hooksPath 2>/dev/null)
orig=
while IFS="$tab" read -r scope val; do
  [ -n "$scope" ] && [ "$scope" != command ] && orig=$val
done <<SOUL_EOF
$cfg
SOUL_EOF
if [ -z "$orig" ]; then
  common=$(git rev-parse --git-common-dir 2>/dev/null) && orig="$common/hooks"
fi
if [ -n "$orig" ] && [ -f "$orig/$hook" ] && [ -x "$orig/$hook" ]; then
  o=$(cd "$orig" 2>/dev/null && pwd -P)
  s=$(cd "$dir" 2>/dev/null && pwd -P)
  l2=
  { IFS= read -r l2 && IFS= read -r l2; } < "$orig/$hook" 2>/dev/null
  if [ -n "$o" ] && [ "$o" != "$s" ] && [ "$l2" != "@OWNED@" ]; then
    # exec in every case, so this process ID becomes the chained hook's own: the hand
    # hook's guard then accepts only its PARENT's ID. (A pipe made the hook a child,
    # which needed the grandparent — and `exec git` forged that, fifth review.)
    if [ "$hook" = pre-push ]; then
      [ -z "$refs" ] && exec "$orig/$hook" "$@" </dev/null
      refs=${refs%?}
      exec "$orig/$hook" "$@" <<SOUL_REFS
$refs
SOUL_REFS
    fi
    exec "$orig/$hook" "$@"
  fi
fi
exit 0
"""


def wrapper_text(hook, directory):
    return (_WRAPPER.replace("@OWNED@", OWNED).replace("@HOOK@", hook)
            .replace("@DIR@", _sq(directory)).replace("@POINTER@", POINTER)
            .replace("@BLOCK@", str(BLOCK_EXIT)).replace("@MISSING@", MISSING_LINE))


def _expected(directory, plugin_root=None):
    files = {hook: (wrapper_text(hook, directory), 0o555) for hook in HOOK_NAMES}
    files[POINTER] = (str(plugin_root or ROOT) + "\n", 0o444)
    return files


def _owned(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            fh.readline()
            return fh.readline().rstrip("\n") == OWNED
    except OSError:
        return False


def _write_if_changed(path, text, mode):
    try:
        with open(path, encoding="utf-8") as fh:
            if fh.read() == text and stat.S_IMODE(os.stat(path).st_mode) == mode:
                return
    except OSError:
        pass
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def install(data_dir=None, plugin_root=None):
    """Write (or refresh) the stable hooks dir and its plugin-root pointer; return it.

    Read-only afterwards (files 0555/0444, dir 0555): a hook installer run inside a
    session (`git lfs install` writes into `git rev-parse --git-path hooks`, which is
    this dir) then fails loudly instead of silently replacing a wrapper. Wrappers this
    plugin no longer ships are removed — only files marked as ours (OWNED). Atomic per
    file; a concurrent install that finds the dir locked retries."""
    d = stable_dir(data_dir)
    want = _expected(d, plugin_root)
    os.makedirs(d, mode=0o700, exist_ok=True)
    for attempt in range(3):
        try:
            os.chmod(d, 0o700)
            for name in os.listdir(d):
                path = os.path.join(d, name)
                if name not in want and os.path.isfile(path) and _owned(path):
                    os.unlink(path)
            for name, (text, mode) in want.items():
                _write_if_changed(os.path.join(d, name), text, mode)
            break
        except PermissionError:
            if attempt == 2:
                raise
            time.sleep(0.2)
        finally:
            os.chmod(d, 0o555)
    return d


def installed_ok(directory, plugin_root=None):
    """True when every wrapper and the pointer match what install() writes, read-only,
    in a read-only dir. The expected content is computed from this code (no stored
    hash to go stale). Cheap: a couple of dozen small reads, no subprocess."""
    try:
        if os.stat(directory).st_mode & 0o222:
            return False
        for name, (text, mode) in _expected(directory, plugin_root).items():
            path = os.path.join(directory, name)
            if stat.S_IMODE(os.stat(path).st_mode) != mode:
                return False
            with open(path, encoding="utf-8") as fh:
                if fh.read() != text:
                    return False
        return True
    except OSError:
        return False


def ensure_installed(data_dir=None):
    """(dir, notice or None): reinstall when missing or modified, and say so."""
    d = stable_dir(data_dir)
    if installed_ok(d):
        return d, None
    existed = os.path.isdir(d)
    install(data_dir)
    return d, (f"Soul secret guard: its git hook folder was {'modified' if existed else 'missing'}"
               f" — reinstalled ({d}). Do not edit it; run hook installers outside an AI session.")


def _strip_zeros(var, indent):
    return f'{indent}while :; do case "${var}" in 0?*) {var}=${{{var}#0}};; *) break;; esac; done'


def env_snippet(directory, session=None, cwd=None):
    """POSIX shell that routes git's hooks through `directory` for every git it runs.

    Adds core.hooksPath at the NEXT free GIT_CONFIG_COUNT index (a count set by
    someone else is respected; leading zeros are stripped; a non-number is left alone
    and the command is said to be NOT armed — never a shell error). Idempotent:
    Claude Code runs the env file before EVERY Bash command, so a re-run that finds
    its own entry in place adds nothing (marker SOUL_GUARD_GIT_IDX, re-validated,
    never trusted blindly). Arms only while the folder exists; if it vanished,
    Claude's PreToolUse hook reinstalls it before the command and says so."""
    lines = [f"# Soul secret guard (SOUL-I070, experimental): git runs its hooks from {directory} "
             "(operations/secret-guard.md)"]
    exports = []
    if session:
        exports.append(f"SOUL_GUARD_SESSION={_sq(session)}")
    if cwd:
        exports.append(f"SOUL_GUARD_CWD={_sq(cwd)}")
    if exports:
        lines.append("export " + " ".join(exports))
    lines += [
        f"__sg_d={_sq(directory)}",
        'if [ -d "$__sg_d" ]; then',
        '  __sg_n=${GIT_CONFIG_COUNT:-0}',
        _strip_zeros("__sg_n", "  "),
        '  case "$__sg_n" in',
        '  ""|*[!0-9]*) echo "Soul secret guard NOT armed for this command — GIT_CONFIG_COUNT is not a number" >&2; __sg_n= ;;',
        '  esac',
        '  if [ -n "$__sg_n" ]; then',
        '    __sg_i=${SOUL_GUARD_GIT_IDX:-}',
        _strip_zeros("__sg_i", "    "),
        '    case "$__sg_i" in ""|*[!0-9]*) __sg_i= ;; esac',
        '    __sg_ok=',
        '    if [ -n "$__sg_i" ] && [ "$__sg_i" -lt "$__sg_n" ]; then',
        '      eval "__sg_k=\\${GIT_CONFIG_KEY_$__sg_i:-}; __sg_v=\\${GIT_CONFIG_VALUE_$__sg_i:-}"',
        '      [ "$__sg_k" = core.hooksPath ] && [ "$__sg_v" = "$__sg_d" ] && __sg_ok=1',
        '    fi',
        '    if [ -z "$__sg_ok" ]; then',
        '      eval "export GIT_CONFIG_KEY_$__sg_n=core.hooksPath GIT_CONFIG_VALUE_$__sg_n=\\"\\$__sg_d\\""',
        '      export GIT_CONFIG_COUNT=$((__sg_n + 1)) SOUL_GUARD_GIT_IDX=$__sg_n',
        '    fi',
        '  fi',
        'fi',
        "unset __sg_d __sg_i __sg_n __sg_ok __sg_k __sg_v",
    ]
    return "\n".join(lines) + "\n"


def _git_version():
    try:
        out = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=10).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    m = re.search(r"(\d+)\.(\d+)", out)
    return (int(m.group(1)), int(m.group(2))) if m else None


def _not_armed(reason, event="SessionStart"):
    msg = (f"Soul secret guard NOT armed — {reason}. The AI's git commits and pushes are NOT "
           "checked for credentials or private names this session (operations/secret-guard.md).")
    return {"systemMessage": msg,
            "hookSpecificOutput": {"hookEventName": event, "additionalContext": msg}}


def _verify_armed(env_file, cwd):
    """Source the env file the way the session will and ask git where its hooks are."""
    shell = os.path.basename(os.environ.get("SHELL") or "")
    shell = shutil.which(shell) if shell in ("bash", "zsh", "sh", "dash") else None
    shell = shell or shutil.which("sh") or "/bin/sh"
    r = subprocess.run([shell, "-c", '. "$1" >/dev/null 2>&1; git config core.hooksPath', "sh", env_file],
                       cwd=cwd, capture_output=True, text=True, timeout=20)
    return r.stdout.strip()


def session_start(data, env_file=None, data_dir=None):
    """Claude Code SessionStart: in a Soul project (or a subfolder of a Soul repo),
    install the stable dir, append the activation shell to $CLAUDE_ENV_FILE (once per
    file), then VERIFY: source it in a subshell and check git's hooks path. Returns
    hook JSON or None. Silent when armed; "NOT armed — <reason>" otherwise."""
    cwd = data.get("cwd") if isinstance(data.get("cwd"), str) else os.getcwd()
    if not os.path.isdir(cwd) or not soul_scoped(cwd, _gate()):
        return None
    env_file = env_file if env_file is not None else os.environ.get("CLAUDE_ENV_FILE")
    try:
        version = _git_version()
        if version is None:
            return _not_armed("git was not found")
        if version < MIN_GIT:
            return _not_armed(f"git {version[0]}.{version[1]} is older than 2.31 (env config "
                              "GIT_CONFIG_COUNT needs 2.31; --show-scope needs 2.26)")
        d = install(data_dir)
        if not env_file:
            return _not_armed("Claude Code gave this hook no CLAUDE_ENV_FILE")
        snippet = env_snippet(d, data.get("session_id"), os.path.realpath(cwd))
        try:
            existing = Path(env_file).read_text(encoding="utf-8")
        except OSError:
            existing = ""
        if snippet not in existing:
            with open(env_file, "a", encoding="utf-8") as fh:
                fh.write(("\n" if existing and not existing.endswith("\n") else "") + snippet)
        got = _verify_armed(env_file, cwd)
        if got != d:
            return _not_armed(f"after the env file runs, git's core.hooksPath is "
                              f"{got or 'unset'!r}, not {d!r}")
        return None
    except Exception as exc:
        return _not_armed(f"{type(exc).__name__}: {exc}")


# ---------------------------------------------------------------- notices

# Warn-only, cheap, no parser: forms that stop git running hooks or remove the env
# entry. It can neither block nor clear anything (see the module FENCE). git accepts
# `--no-veri` and longer for --no-verify (shorter is ambiguous with --no-verbose,
# checked on git 2.43); the notice matches down to `--no-v` anyway — over-warning
# costs nothing. `-n` counts only after `git … commit`.
_BYPASS = re.compile(
    r"(?<![\w-])--no-v(?:e|er|eri|erif|erify)?(?![\w-])"
    r"|\bgit(?:\s+(?:-[Cc]\s+\S+|--?[\w-]+(?:=\S+)?))*\s+commit\b[^\n;&|]*\s-[A-Za-z]*n[A-Za-z]*(?![\w-])"
    r"|(?:(?<![\w-])-c\s*|--config-env[= ])['\"]?core\.hookspath"
    r"|\bGIT_CONFIG_(?:COUNT|PARAMETERS|KEY_)"
    r"|\bunset\b[^\n;&|]*\bGIT_CONFIG"
    r"|\benv\b(?:\s+-[A-Za-z]*i[A-Za-z]*|\s+--ignore-environment)\b"
    r"|SOUL_GUARD_",   # any mention: =, +=, printf -v, read, export -n, env -u (fifth review)
    re.IGNORECASE)
BYPASS_LINE = "Soul secret guard: this command bypasses git hooks — NOT checked"
# Hook installers: inside a session git's hooks path is the guard's read-only folder,
# so they fail there (or set a path the session overrides). Say why before they run.
_INSTALLER = re.compile(
    r"\bgit\s+lfs\s+(?:install|update|track)\b|\bpre-commit\s+install\b|\blefthook\s+install\b"
    r"|\bhusky\b|\bgit\b[^\n;&|]*\bconfig\b[^\n;&|]*\bcore\.hookspath\b",
    re.IGNORECASE)
INSTALLER_LINE = ("Soul secret guard: run hook installers outside an AI session — inside it, "
                  "git's hooks path points at the Soul guard")


def command_notices(command):
    if not isinstance(command, str):
        return []
    out = []
    if _BYPASS.search(command):
        out.append(BYPASS_LINE)
    if _INSTALLER.search(command):
        out.append(INSTALLER_LINE)
    return out


def pre_tool_use(data, data_dir=None, event="PreToolUse"):
    """PreToolUse on Bash (Claude Code; the Codex adapter calls it too): in a Soul
    project, re-verify the hook folder (reinstall if missing or modified, and say so)
    and give the bypass / hook-installer notices. Never decides anything."""
    if data.get("tool_name") not in (None, "Bash"):
        return None
    cwd = data.get("cwd")
    if not isinstance(cwd, str) or not os.path.isdir(cwd) or not soul_scoped(cwd, _gate()):
        return None
    lines = []
    try:
        _, note = ensure_installed(data_dir)
        if note:
            lines.append(note)
    except OSError as exc:
        lines.append(f"Soul secret guard: its git hook folder could not be reinstalled "
                     f"({type(exc).__name__}) — commits and pushes are NOT checked.")
    lines += command_notices((data.get("tool_input") or {}).get("command"))
    if not lines:
        return None
    text = "\n".join(lines)
    return {"systemMessage": text,
            "hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}


def codex_opt_in(directory):
    """The Codex config that arms the guard (Codex has no env file). `set` runs after
    Codex's automatic KEY/SECRET/TOKEN exclusions, so GIT_CONFIG_KEY_0 survives; an
    include-pattern allowlist would still drop it (Codex config docs, "Shell
    environment policy", and codex-rs protocol/src/shell_environment.rs, read
    2026-10-20)."""
    return ("[shell_environment_policy]\n"
            f'set = {{ GIT_CONFIG_COUNT = "1", GIT_CONFIG_KEY_0 = "core.hooksPath", '
            f'GIT_CONFIG_VALUE_0 = "{directory}" }}')


def codex_armed_note(cwd, directory):
    """One context line for Codex's SessionStart: armed only by the owner's opt-in.
    Heuristic: the opt-in counts as present when a Codex config file names the
    folder. Read-only; never edits the config."""
    home = os.environ.get("CODEX_HOME") or os.path.join(os.path.expanduser("~"), ".codex")
    for p in (os.path.join(home, "config.toml"), os.path.join(cwd, ".codex", "config.toml")):
        try:
            if directory in Path(p).read_text(encoding="utf-8", errors="replace"):
                return (f"Soul secret guard (experimental): {p} routes git hooks to {directory}; "
                        "git checks commits and pushes.")
        except OSError:
            continue
    return ("Soul secret guard NOT armed under Codex — it is an opt-in. To arm it, the owner "
            "adds this to ~/.codex/config.toml (operations/secret-guard.md):\n" + codex_opt_in(directory))


# ------------------------------------------------------------------------ entry

def main():
    argv = sys.argv[1:]
    if argv[:1] == ["--git-hook"]:
        hook = argv[1] if len(argv) > 1 else "pre-commit"
        stdin_text = ""
        if hook == "pre-push":
            try:
                stdin_text = sys.stdin.read()
            except (OSError, ValueError):
                stdin_text = ""
        return git_hook_main(hook, argv[2:], stdin_text)
    if argv[:1] == ["--hand-hook"]:
        hook = argv[1] if len(argv) > 1 else "pre-commit"
        if _wrapper_ran(hook):
            return 0  # this session's wrapper ran the check and chained here
        stdin_text = sys.stdin.read() if hook == "pre-push" else ""
        return git_hook_main(hook, argv[2:], stdin_text)
    if argv[:1] == ["--own-hooks-dir"]:
        d = own_hooks_dir(argv[1] if len(argv) > 1 else os.getcwd())
        if d:
            print(d)
        return 0 if d else 1
    try:
        data = json.load(sys.stdin)
        if not isinstance(data, dict):
            raise ValueError("hook input must be an object")
    except Exception as exc:
        print(json.dumps({"systemMessage": (
            f"Soul secret guard skipped ({type(exc).__name__}: unreadable hook input) — "
            "NOT checked.")}))
        return 0
    try:
        out = session_start(data) if argv[:1] == ["--session-start"] else pre_tool_use(data)
    except Exception as exc:
        out = {"systemMessage": f"Soul secret guard skipped ({type(exc).__name__}) — NOT checked."}
    if out:
        print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
