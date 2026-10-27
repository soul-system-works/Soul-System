#!/usr/bin/env python3
"""Hand a /soul-workflow step to a worker harness, in its own process and worktree.

The host session (whatever harness and model the Body started in) keeps judgment and
the record; workers are other harness+model pairs that get only a brief (SOUL-I080).
This tool is the thin layer between them: it reads the roles table, starts the
worker through that harness's headless CLI with the host's context kept out, and
hands back the evidence — the patch, the exit, the wall time, the tokens — never a
verdict. It never records: the host re-runs the check through
tools/delegation-check.py, because a worker's report is a claim (SOUL-I066).

  roles  [--project DIR] [--json]                    the effective roles table
  run    --role R --brief FILE [--project DIR] [--base REF] [--check CMD]
         [--rung K] [--run-id ID]                    implement, n tries, pick one
  review --role R --brief FILE --diff FILE [--project DIR] [--run-id ID]
                                                     every reviewer of R, read-only
  clean  --run-id ID [--project DIR]                 remove a run's worktrees+branches

Roles table: `~/.claude/soul-roles.md` (global) and `<project>/.claude/soul-roles.md`,
a Markdown table `| role | harness | model | settings |` — settings `key=value`
separated by spaces, only `rung`, `n` (best-of-n) and `timeout` (seconds). A
project that defines any row for a role replaces ALL global rows for that role.
A role's rows are its ladder, ordered by rung (row order when none is given).
Built-in default for a role neither file names: implementer claude:sonnet then
claude:opus; reviewer claude:opus, plus codex:default when `codex` is on PATH.

`run` makes each try a worktree `<project>/.ai/worktrees/<run-id>-<i>` on branch
`soul-wf/<run-id>-<i>` from --base (default HEAD), stages everything the worker left
(untracked too, never committed), writes the diff against base to
`<project>/.ai/workflow-runs/<run-id>/try-<i>.patch`, and runs --check there only to
pick the winner: check passed, then fewest changed lines. Tries run one at a time
(a GPU holds one model). result.json (review.json for `review`) holds what was seen.

POSIX only (Linux, macOS, WSL): a timed-out worker's whole process group is killed.
"""

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import confine  # noqa: E402  (tools/confine.py — allowlisted env, bubblewrap)

HARNESSES = ("claude", "claude-ollama", "codex", "codex-ollama")
SETTINGS = ("rung", "n", "timeout")
DEFAULT_TIMEOUT = 1800
GLOBAL_ROLES = os.path.join("~", ".claude", "soul-roles.md")
PROJECT_ROLES = os.path.join(".claude", "soul-roles.md")
RECORD_FILES = ("witness.md", "ideas.md", "mind.md", "upstream.md")
CLAUDE_MD_NAMES = ("CLAUDE.md", "CLAUDE.local.md", os.path.join(".claude", "CLAUDE.md"))
WALK_SKIP = (".git", "node_modules", ".venv", "venv", "__pycache__")
OLLAMA_URL = "http://localhost:11434"
RUN_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
SIGNALS = tuple(getattr(signal, n) for n in ("SIGTERM", "SIGINT", "SIGHUP")
                if hasattr(signal, n))

WORKER_RULES = """

## Worker rules (added by dispatch)

- You are a worker with only this brief: no earlier conversation, no project record.
- Do not write witness.md, ideas.md, mind.md, upstream.md or anything under .soul/.
- Run the check yourself before finishing{check}.
- End with what you changed, the check's result, and anything you did not run or
  could not do.
"""

REVIEW_ASK = """

## The change to review

{fence}diff
{diff}
{fence}

## Your task

Report findings only, never edit. One finding per line, as
`FINDING: <file:line> — <what is wrong> — <a concrete failure scenario>`,
or the single line `NO FINDINGS`.
"""
FINDING = re.compile(r"^[\s>*_`-]*FINDING[*_`]*\s*:[*_`]*\s*(.+?)\s*$")
NO_FINDINGS = re.compile(r"^[\s>*_`-]*NO FINDINGS\b")


class RolesError(Exception):
    """A roles file that cannot be used; the message names the file, line and row."""


class UsageError(Exception):
    """A request dispatch refuses before any worker starts (exit 2)."""


class Killed(Exception):
    """dispatch got a termination signal while a worker or check ran."""

    def __init__(self, signum):
        super().__init__(signum)
        self.signum = signum


# ---------------------------------------------------------------- roles table

def _cells(line):
    text = line.strip()
    if text.endswith("|"):
        text = text[:-1]
    return [c.strip() for c in text[1:].split("|")]


def _row_error(path, lineno, line, why):
    return RolesError("{}:{}: {} — row: {}".format(path, lineno, why, line.strip()))


def parse_roles_file(path, source):
    """Rows of one roles file, in file order; [] when the file does not exist.

    Only table lines (starting with `|`) are read, so prose around the table is
    free; the header row (first cell `role`) and the `|---|` separator are skipped.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
    except FileNotFoundError:
        return []
    rows = []
    position = {}
    for lineno, line in enumerate(lines, 1):
        if not line.lstrip().startswith("|"):
            continue
        cells = _cells(line)
        if all(re.fullmatch(r":?-+:?", c) for c in cells if c) and any(cells):
            continue  # the separator row
        if cells and cells[0].lower() == "role":
            continue  # the header row
        if len(cells) not in (3, 4):
            raise _row_error(path, lineno, line,
                             "a row needs role | harness | model | settings")
        role, harness, model = cells[:3]
        for name, value in (("role", role), ("harness", harness), ("model", model)):
            if not value:
                raise _row_error(path, lineno, line, "blank {}".format(name))
        if harness not in HARNESSES:
            raise _row_error(path, lineno, line, "unknown harness {!r} (known: {})"
                             .format(harness, ", ".join(HARNESSES)))
        if harness == "claude-ollama" and model == "default":
            # Step 1 probe, 2026-10-27: Ollama answers "model not found" unless the
            # model is an exact installed tag, so there is no default to fall back on.
            raise _row_error(path, lineno, line,
                             "claude-ollama needs an exact installed Ollama tag, not default")
        settings = {}
        for item in (cells[3].split() if len(cells) == 4 else []):
            key, eq, value = item.partition("=")
            if not eq or not key or not value:
                raise _row_error(path, lineno, line,
                                 "setting {!r} is not key=value".format(item))
            if key not in SETTINGS:
                raise _row_error(path, lineno, line, "unknown setting {!r} (known: {})"
                                 .format(key, ", ".join(SETTINGS)))
            try:
                number = int(value)
            except ValueError:
                raise _row_error(path, lineno, line,
                                 "setting {} must be a whole number, got {!r}"
                                 .format(key, value)) from None
            if number < 1:
                raise _row_error(path, lineno, line,
                                 "setting {} must be 1 or more, got {}".format(key, number))
            settings[key] = number
        position[role] = position.get(role, 0) + 1
        rows.append({"role": role, "harness": harness, "model": model,
                     "rung": settings.get("rung", position[role]),
                     "n": settings.get("n", 1),
                     "timeout": settings.get("timeout", DEFAULT_TIMEOUT),
                     "source": source, "where": "{}:{}".format(path, lineno)})
    return rows


def builtin_rows(which=shutil.which):
    def row(role, harness, model, rung):
        return {"role": role, "harness": harness, "model": model, "rung": rung, "n": 1,
                "timeout": DEFAULT_TIMEOUT, "source": "built-in", "where": None}
    rows = [row("implementer", "claude", "sonnet", 1),
            row("implementer", "claude", "opus", 2),
            row("reviewer", "claude", "opus", 1)]
    if which("codex"):
        rows.append(row("reviewer", "codex", "default", 2))
    return rows


def load_roles(project):
    """{role: [rows ordered by rung]} — project over global over built-in, per role."""
    layers = [builtin_rows(),
              parse_roles_file(os.path.expanduser(GLOBAL_ROLES), "global"),
              parse_roles_file(os.path.join(project, PROJECT_ROLES), "project")]
    table = {}
    for rows in layers:
        named = {}
        for r in rows:
            named.setdefault(r["role"], []).append(r)
        table.update(named)  # a layer that names a role replaces all its earlier rows
    return {role: sorted(rows, key=lambda r: r["rung"])  # stable: row order on ties
            for role, rows in sorted(table.items())}


def flat(table):
    return [r for rows in table.values() for r in rows]


def cmd_roles(args):
    table = load_roles(project_dir(args.project, need_git=False))
    if args.json:
        print(json.dumps(flat(table), indent=2))
        return 0
    print("{:<12} {:<5} {:<14} {:<22} {:<3} {:<8} {}".format(
        "role", "rung", "harness", "model", "n", "timeout", "source"))
    for r in flat(table):
        print("{:<12} {:<5} {:<14} {:<22} {:<3} {:<8} {}".format(
            r["role"], r["rung"], r["harness"], r["model"], r["n"], r["timeout"],
            r["source"] + (" ({})".format(r["where"]) if r["where"] else "")))
    return 0


# ---------------------------------------------------------------- adapters

def claude_md_excludes(workdir):
    """Every CLAUDE.md a Claude worker started in `workdir` could load: the user's
    own, those in the folders above, and those anywhere inside (a nested one loads
    when the worker reads files beside it)."""
    paths = [os.path.join(os.path.expanduser("~"), ".claude", "CLAUDE.md")]
    d = os.path.dirname(workdir)
    while True:
        paths += [os.path.join(d, n) for n in CLAUDE_MD_NAMES
                  if os.path.isfile(os.path.join(d, n))]
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    for root, dirs, files in os.walk(workdir):
        dirs[:] = [x for x in dirs if x not in WALK_SKIP]
        paths += [os.path.join(root, n) for n in ("CLAUDE.md", "CLAUDE.local.md")
                  if n in files]
    return list(dict.fromkeys(paths))


def secret_dirs():
    """Folders a Claude worker may not read: credentials and the owner's private
    record (confine.SECRET_DIRS, the list the confined checks hide too). The sandbox
    limits writes and network, but reads are wide by default. `~/x` and
    `//abs/path` are Claude Code's permission-rule spellings."""
    out = ["~/" + d for d in confine.SECRET_DIRS]
    v = confine.registered_vault()  # the vault holds every vaulted project's record
    if v:
        out.append("/" + v)
    return out


def need_sandbox(rows):
    """A Claude worker without its sandbox would run its shell unconfined — refuse.
    On Linux the sandbox needs bubblewrap and socat; without socat Claude Code turns
    the sandbox off (seen 2026-10-27). macOS has it built in."""
    if not sys.platform.startswith("linux"):
        return
    if any(r["harness"] in ("claude", "claude-ollama") for r in rows):
        missing = [t for t in ("bwrap", "socat") if not shutil.which(t)]
        if missing:
            raise UsageError("a Claude worker runs inside Claude Code's sandbox, which needs "
                             "{} here — install it (e.g. `sudo apt install bubblewrap socat`)"
                             .format(" and ".join(missing)))


def worker_env(harness):
    """The allowlisted environment plus the route's own values, nothing inherited.
    The 2026-10-27 review of v3.7.0: workers got the host's whole environment — its
    messaging socket and token, session id, GH_TOKEN, GIT_CONFIG_*, the secret
    guard's variables. Step 1 isolation probe, 2026-10-27 (v3.7.0 plan, "Step 1
    result"): a host that itself runs over Ollama exports ANTHROPIC_BASE_URL and
    AUTH_TOKEN, and a worker inheriting them would silently go to the local model;
    the Anthropic route gets none of ANTHROPIC_* but an EMPTY API key, so the
    subscription login answers. The Ollama route sets all three on purpose."""
    if harness == "claude":
        return confine.clean_env({"ANTHROPIC_API_KEY": ""})
    if harness == "claude-ollama":
        return confine.clean_env({"ANTHROPIC_BASE_URL": OLLAMA_URL,
                                  "ANTHROPIC_AUTH_TOKEN": "ollama", "ANTHROPIC_API_KEY": ""})
    return confine.clean_env()


def worker_command(row, workdir, mode, check=None, last_file=None):
    """argv for one worker. mode "run" may edit `workdir`; "review" only reads it."""
    harness, model = row["harness"], row["model"]
    if harness in ("claude", "claude-ollama"):
        if mode == "run":
            # Full Bash, inside the OS sandbox below. "The check is the only Bash" was
            # the first design; the v3.6.3 replay (2026-10-27) showed it too tight — the
            # worker could not run one test file to see it fail, nor `git status`, and
            # stopped with five denials. The Body chose the sandbox over an unsandboxed
            # shell or an allow list (SOUL-I080). The sandbox confines Bash only: a
            # probe on 2026-10-27 (haiku, these flags) with bare `Write,Edit` wrote
            # ../x, an absolute path outside and Edited a file one level up — all
            # landed. Scoped to `Write(./**),Edit(./**)` (relative to the worktree,
            # the worker's cwd), the same probe was denied all three and still wrote
            # inside the worktree.
            tools, permission = "Read,Write(./**),Edit(./**),Glob,Grep,Bash", "acceptEdits"
        else:
            tools, permission = "Read,Glob,Grep", "plan"
        cmd = ["claude", "-p", "--output-format", "json", "--permission-mode", permission,
               "--allowedTools", tools]
        if model != "default":
            cmd += ["--model", model]
        # Isolation verified by the Step 1 probe, 2026-10-27: without these flags the
        # worker answered sentinel questions from ~/.claude/CLAUDE.md, the contract
        # and the Mind, and loaded plugins, hooks, auto-memory and MCP servers; with
        # them it answered NONE to all, on both the Anthropic and the Ollama route.
        # Only the worktree's top two CLAUDE.md levels were probed; the rest of the
        # exclude list is the same mechanism applied further.
        settings = {"claudeMdExcludes": claude_md_excludes(workdir), "autoMemoryEnabled": False,
                    # Sandbox probe, 2026-10-27 (v3.7.0 plan, "Sandbox probe"): with these,
                    # git status/log, the test suites (temp writes) and writes in the
                    # worktree worked; a write outside, the network, and a shell or Read
                    # of a denied folder were all blocked. No command may leave it, and a
                    # sandbox that cannot start fails the run instead of being switched
                    # off (the 2026-10-27 review: without socat it was turned off).
                    "sandbox": {"enabled": True, "failIfUnavailable": True,
                                "autoAllowBashIfSandboxed": True,
                                "allowUnsandboxedCommands": False},
                    "permissions": {"deny": ["Read({}/**)".format(p) for p in secret_dirs()]}}
        return cmd + ["--setting-sources", "", "--strict-mcp-config",
                      "--settings", json.dumps(settings)]
    # codex / codex-ollama. Step 1 probe, 2026-10-27: without these flags `codex exec`
    # answered from AGENTS.md and the contract; with them it answered NONE and stayed
    # logged in. The Ollama variant (--oss --local-provider ollama) was NOT probed.
    cmd = ["codex", "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
           "-c", "project_doc_max_bytes=0", "-C", workdir,
           "-s", "workspace-write" if mode == "run" else "read-only",
           "--json", "-o", last_file]
    if harness == "codex-ollama":
        cmd += ["--oss", "--local-provider", "ollama"]
    if model != "default":
        cmd += ["-m", model]
    return cmd + ["-"]  # the prompt comes on stdin: a diff can outgrow one argv entry


def _json_lines(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except OSError:
        return []
    out = []
    for line in lines:
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if isinstance(ev, dict):
            out.append(ev)
    return out


def read_output(harness, log_path, last_file):
    """(tokens_in, tokens_out, final text) from what the harness printed. Tokens are
    None when the harness did not report them, and never a price: Ollama runs report
    a made-up one (SOUL-200)."""
    events = _json_lines(log_path)
    if harness.startswith("claude"):
        result = next((ev for ev in reversed(events) if "result" in ev or "usage" in ev), {})
        text = result.get("result") if isinstance(result.get("result"), str) else ""
        usage = result.get("usage")
        if not isinstance(usage, dict):
            return None, None, text
        tokens_in = sum(usage.get(k) or 0 for k in (
            "input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
        return tokens_in, usage.get("output_tokens"), text
    try:
        with open(last_file, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except (OSError, TypeError):
        text = ""
    turns = [ev["usage"] for ev in events
             if ev.get("type") == "turn.completed" and isinstance(ev.get("usage"), dict)]
    if not turns:
        return None, None, text
    return (sum(u.get("input_tokens") or 0 for u in turns),
            sum(u.get("output_tokens") or 0 for u in turns), text)


# ---------------------------------------------------------------- processes

def _kill_group(pgid):
    try:
        os.killpg(pgid, signal.SIGKILL)
    except OSError:
        pass  # group already empty


def run_process(cmd, cwd, env, stdin_text, log_path, err_path, timeout):
    """Run `cmd` in its own process group; return (exit code | "timeout", wall_s).

    stdout goes to `log_path`, stderr to `err_path` (into the log when None). The
    whole group is killed in the finally — after a timeout, a signal to dispatch, or
    a clean exit — so nothing a worker or check started outlives its try."""
    t0 = time.monotonic()
    with tempfile.TemporaryFile() as stdin, open(log_path, "wb") as out:
        stdin.write(stdin_text.encode("utf-8"))
        stdin.seek(0)
        err = open(err_path, "wb") if err_path else None
        proc = None
        try:
            proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=stdin, stdout=out,
                                    stderr=err or subprocess.STDOUT, start_new_session=True)
            try:
                code = proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                code = "timeout"
        finally:
            if proc is not None:
                _kill_group(proc.pid)
                if proc.returncode is None:
                    try:
                        proc.wait(timeout=5)  # reap the killed leader
                    except Exception:
                        pass
            if err:
                err.close()
    return code, round(time.monotonic() - t0, 1)


def _on_signal(signum, frame):
    for s in SIGNALS:
        signal.signal(s, signal.SIG_IGN)  # a second signal must not cut the cleanup
    raise Killed(signum)


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                          stdin=subprocess.DEVNULL)


# ---------------------------------------------------------------- shared

def project_dir(path, need_git=True):
    """--project as given, else the git top level of here (else here)."""
    if path:
        project = os.path.abspath(path)
        if not os.path.isdir(project):
            raise UsageError("no directory at --project {}".format(path))
    else:
        top = git(os.getcwd(), "rev-parse", "--show-toplevel")
        project = top.stdout.strip() if top.returncode == 0 else os.getcwd()
    if need_git and git(project, "rev-parse", "--is-inside-work-tree").stdout.strip() != "true":
        raise UsageError("{} is not in a git work tree".format(project))
    return project


def role_rows(project, role):
    rows = load_roles(project).get(role)
    if not rows:
        raise UsageError("no role {!r} in the roles table (see: dispatch.py roles)"
                         .format(role))
    return rows


def read_text(path, what):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError as e:
        raise UsageError("cannot read the {} {}: {}".format(what, path, e)) from None


def need_harness(rows):
    for r in rows:
        exe = "claude" if r["harness"].startswith("claude") else "codex"
        if not shutil.which(exe):
            raise UsageError("a {} row needs `{}` on PATH".format(r["harness"], exe))


def run_dir_for(project, run_id):
    if not RUN_ID.match(run_id) or run_id.endswith(".lock"):
        raise UsageError("--run-id {!r}: letters, digits and . _ - only".format(run_id))
    return os.path.join(project, ".ai", "workflow-runs", run_id)


def ignore_ai(project):
    """Keep .ai/ out of git here before tries land in it. In a project that does not
    ignore it, the try worktrees show as untracked and one `git add -A` in the main
    checkout adds them as embedded repos (the v3.7.0 build's own report). Local only:
    .git/info/exclude, never the project's tracked .gitignore."""
    if git(project, "check-ignore", "-q", ".ai/workflow-runs").returncode == 0:
        return
    path = git(project, "rev-parse", "--git-path", "info/exclude").stdout.strip()
    if not path:
        return
    path = os.path.join(project, path) if not os.path.isabs(path) else path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n.ai/\n")


def log_dispatch(project, payload):
    """One soul.workflow.dispatch event per run or review, to the project's event sink
    (the recorder's rules: $SOUL_EVENT_LOG, else .soul/events.jsonl of a Soul project,
    else nothing). The host's recorder sees only the winner it re-checks, so a role
    that times out or never passes left no trace — the v3.6.3 replay's local arm
    (2026-10-27) ran an hour, failed, and stats showed nothing. These are the tool's
    own observations (exit codes, its selection check), never a worker's claim."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "delegation_check", os.path.join(_HERE, "delegation-check.py"))
        dc = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dc)
        where = None if os.environ.get("SOUL_EVENT_LOG") else dc.find_project(project)
        if where is None and not os.environ.get("SOUL_EVENT_LOG"):
            return
        dc.emit(where, project, payload, event_type="soul.workflow.dispatch")
    except Exception as exc:  # a record that cannot be written never fails the run
        print("warning: dispatch event not recorded ({})".format(exc), file=sys.stderr)


def emit_result(path, result):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
        fh.write("\n")
    print(json.dumps(result, indent=2))


# ---------------------------------------------------------------- run

def stage_and_diff(worktree, base, patch_path):
    """Stage everything the worker left (untracked too; never commit) and write the
    diff against base. Returns (changed_lines, record_touched)."""
    git(worktree, "add", "-A")
    patch = subprocess.run(["git", "diff", "--cached", "--binary", "--no-renames", base],
                           cwd=worktree, capture_output=True, stdin=subprocess.DEVNULL)
    with open(patch_path, "wb") as fh:
        fh.write(patch.stdout)
    changed = 0
    for line in git(worktree, "diff", "--cached", "--numstat", "--no-renames",
                    base).stdout.splitlines():
        added, deleted = line.split("\t")[:2]  # "-" for a binary file: counts 0
        changed += (int(added) if added.isdigit() else 0) + (
            int(deleted) if deleted.isdigit() else 0)
    names = git(worktree, "diff", "--cached", "--name-only", "-z", "--no-renames",
                base).stdout.split("\0")
    touched = any(n in RECORD_FILES or n.startswith(".soul/") for n in names if n)
    return changed, touched


def read_text_quiet(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def sandbox_inactive(row, err_path):
    """Claude Code says "Sandbox disabled" on stderr when it could not start the
    sandbox (seen 2026-10-27, without socat)."""
    return row["harness"] in ("claude", "claude-ollama") and \
        "Sandbox disabled" in read_text_quiet(err_path)


def pick_winner(tries, have_check):
    """Passing check, then fewest changed lines. With no check given, a try that
    exited 0 and changed something stands in for passing. A try that touched the
    Soul record, or ran without its sandbox, is never the winner."""
    tries = [t for t in tries if not t["record_touched"] and not t.get("sandbox_inactive")]
    if have_check:
        ok = [t for t in tries if t["check_rc"] == 0]
    else:
        ok = [t for t in tries if t["exit"] == 0 and t["changed_lines"] > 0]
    return min(ok, key=lambda t: (t["changed_lines"], t["try"]))["try"] if ok else None


def cmd_run(args):
    project = project_dir(args.project)
    rows = role_rows(project, args.role)
    rung = args.rung if args.rung is not None else rows[0]["rung"]
    row = next((r for r in rows if r["rung"] == rung), None)
    if row is None:
        raise UsageError("role {!r} has no rung {} (its rungs: {})".format(
            args.role, rung, ", ".join(str(r["rung"]) for r in rows)))
    need_harness([row])
    need_sandbox([row])
    if args.check is not None and not args.check.strip():
        raise UsageError("--check is blank")
    # The selection check runs the worker's code, so it runs confined (the 2026-10-27
    # review: it ran with the host's whole environment and no sandbox). Where it
    # cannot be confined, one try skips it — the host's confined re-run through the
    # recorder is the gate — and best-of-n, which needs it to choose, is refused.
    confinable = confine.confine_argv(["true"], project) is not None
    if args.check and not confinable and row["n"] > 1:
        raise UsageError("best-of-n runs each try's check, which needs bubblewrap to "
                         "confine it — install it (e.g. `sudo apt install bubblewrap`) "
                         "or use n=1")
    brief = read_text(args.brief, "brief")
    base = git(project, "rev-parse", "--verify", "--quiet", args.base + "^{commit}")
    if base.returncode != 0:
        raise UsageError("--base {!r} is not a commit".format(args.base))
    base = base.stdout.strip()
    run_id = args.run_id or time.strftime("%Y%m%d-%H%M%S")
    run_dir = run_dir_for(project, run_id)
    if os.path.exists(os.path.join(run_dir, "result.json")):
        raise UsageError("run id {} already has a result.json".format(run_id))
    os.makedirs(run_dir, exist_ok=True)
    prompt = brief.rstrip("\n") + WORKER_RULES.format(
        check=": `{}`".format(args.check) if args.check else " (no check was named: say so)")

    ignore_ai(project)
    tries = []
    for i in range(1, row["n"] + 1):  # one at a time: a GPU holds one model
        name = "{}-{}".format(run_id, i)
        worktree = os.path.join(project, ".ai", "worktrees", name)
        branch = "soul-wf/" + name
        added = git(project, "worktree", "add", "-q", "-b", branch, worktree, base)
        if added.returncode != 0:
            raise UsageError("git worktree add {} failed: {}".format(
                worktree, added.stderr.strip()))
        stem = os.path.join(run_dir, "try-{}".format(i))
        last = stem + ".last.txt"
        code, wall = run_process(worker_command(row, worktree, "run", args.check, last),
                                 worktree, worker_env(row["harness"]), prompt,
                                 stem + ".log", stem + ".stderr", row["timeout"])
        tokens_in, tokens_out, _ = read_output(row["harness"], stem + ".log", last)
        changed, touched = stage_and_diff(worktree, base, stem + ".patch")
        # A try whose shell ran unconfined or not at all can never win.
        inactive = sandbox_inactive(row, stem + ".stderr")
        check_rc = None
        if args.check and confinable:  # for selection only: the host re-runs it
            check_rc, _ = run_process(
                confine.confine_argv(["/bin/sh", "-c", args.check], worktree), worktree,
                confine.clean_env(), "", stem + ".check.log", None, row["timeout"])
        tries.append({"try": i, "worktree": worktree, "branch": branch, "exit": code,
                      "wall_s": wall, "tokens_in": tokens_in, "tokens_out": tokens_out,
                      "patch": stem + ".patch", "log": stem + ".log",
                      "changed_lines": changed, "check_rc": check_rc,
                      "record_touched": touched, "sandbox_inactive": inactive})
    result = {"run_id": run_id, "role": args.role, "harness": row["harness"],
              "model": row["model"], "rung": row["rung"], "base": base,
              "check": args.check, "check_skipped": bool(args.check) and not confinable,
              "tries": tries, "winner": pick_winner(tries, bool(args.check) and confinable)}
    if result["check_skipped"]:
        print("note: no bubblewrap here, so the selection check did not run; the "
              "recorder's confined re-run is the gate", file=sys.stderr)
    emit_result(os.path.join(run_dir, "result.json"), result)
    log_dispatch(project, {
        "mode": "run", "run_id": run_id, "role": args.role, "harness": row["harness"],
        "model": row["model"], "rung": row["rung"], "tries": len(tries),
        "won": result["winner"] is not None,
        "timeouts": sum(1 for t in tries if t["exit"] == "timeout"),
        "wall_s": round(sum(t["wall_s"] for t in tries), 1)})
    return 0 if result["winner"] is not None else 1


# ---------------------------------------------------------------- review

def parse_findings(text):
    """(findings, verdict): the FINDING lines' text; verdict "findings", "none" (a
    NO FINDINGS line and no finding) or "unparsed" (neither)."""
    findings, none = [], False
    for line in (text or "").splitlines():
        m = FINDING.match(line)
        if m:
            findings.append(m.group(1))
        elif NO_FINDINGS.match(line):
            none = True
    return findings, "findings" if findings else "none" if none else "unparsed"


def cmd_review(args):
    project = project_dir(args.project, need_git=False)
    # A candidate's reviewers must read the candidate, not the project's own checkout:
    # the first live review (2026-10-27) would have read the host branch's files
    # beside a diff written against another base.
    workdir = os.path.realpath(args.workdir) if args.workdir else project
    if not os.path.isdir(workdir):
        raise UsageError("--workdir {} is not a folder".format(args.workdir))
    rows = role_rows(project, args.role)
    need_harness(rows)
    need_sandbox(rows)
    brief = read_text(args.brief, "brief")
    diff = read_text(args.diff, "diff")
    run_id = args.run_id or time.strftime("%Y%m%d-%H%M%S")
    run_dir = run_dir_for(project, run_id)
    if os.path.exists(os.path.join(run_dir, "review.json")):
        raise UsageError("run id {} already has a review.json".format(run_id))
    os.makedirs(run_dir, exist_ok=True)
    longest = max([len(m) for m in re.findall(r"`+", diff)] + [0])
    prompt = brief.rstrip("\n") + REVIEW_ASK.format(fence="`" * max(3, longest + 1),
                                                    diff=diff.rstrip("\n"))
    reviewers = []
    for j, row in enumerate(rows, 1):  # each reviewer once, not a ladder
        stem = os.path.join(run_dir, "review-{}-{}".format(j, row["harness"]))
        last = stem + ".last.txt"
        code, wall = run_process(worker_command(row, workdir, "review", last_file=last),
                                 workdir, worker_env(row["harness"]), prompt,
                                 stem + ".log", stem + ".stderr", row["timeout"])
        tokens_in, tokens_out, text = read_output(row["harness"], stem + ".log", last)
        with open(stem + ".txt", "w", encoding="utf-8") as fh:
            fh.write(text)
        findings, verdict = parse_findings(text)
        inactive = sandbox_inactive(row, stem + ".stderr")
        if inactive:  # read-only by its tools, but not by the sandbox it was given
            verdict = "unconfined"
        reviewers.append({"harness": row["harness"], "model": row["model"],
                          "exit": code, "wall_s": wall, "tokens_in": tokens_in,
                          "tokens_out": tokens_out, "raw": stem + ".txt",
                          "log": stem + ".log", "findings": findings, "verdict": verdict,
                          "sandbox_inactive": inactive})
    emit_result(os.path.join(run_dir, "review.json"),
                {"run_id": run_id, "role": args.role, "reviewers": reviewers})
    for r in reviewers:
        log_dispatch(project, {
            "mode": "review", "run_id": run_id, "role": args.role, "harness": r["harness"],
            "model": r["model"], "tries": 1,
            "won": r["exit"] == 0 and r["verdict"] in ("findings", "none"),
            "timeouts": 1 if r["exit"] == "timeout" else 0, "wall_s": r["wall_s"]})
    return 0


# ---------------------------------------------------------------- clean

def cmd_clean(args):
    project = project_dir(args.project)
    run_dir_for(project, args.run_id)  # validates the id
    own = re.compile(re.escape(args.run_id) + r"-\d+\Z")
    root = os.path.realpath(os.path.join(project, ".ai", "worktrees"))
    removed = []
    for line in git(project, "worktree", "list", "--porcelain").stdout.splitlines():
        if not line.startswith("worktree "):
            continue
        path = line[len("worktree "):]
        if (os.path.dirname(os.path.realpath(path)) != root
                or not own.match(os.path.basename(path))):
            continue
        r = git(project, "worktree", "remove", "--force", path)
        if r.returncode != 0:
            print("warning: could not remove {}: {}".format(path, r.stderr.strip()),
                  file=sys.stderr)
        else:
            removed.append(path)
    git(project, "worktree", "prune")
    branches = [b for b in git(project, "for-each-ref", "--format=%(refname:short)",
                               "refs/heads/soul-wf/").stdout.split()
                if own.match(b[len("soul-wf/"):])]
    for b in branches:
        git(project, "branch", "-D", b)
    print("removed {} worktree(s) and {} branch(es) of run {}; its evidence stays in "
          ".ai/workflow-runs/{}/".format(len(removed), len(branches), args.run_id,
                                         args.run_id))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    here = "project directory (default: the git top level here)"
    p = sub.add_parser("roles", help="show the effective roles table")
    p.add_argument("--project", help=here)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("run", help="run a role's worker on a brief, n tries, pick one")
    p.add_argument("--role", required=True)
    p.add_argument("--brief", required=True, help="file holding the brief")
    p.add_argument("--project", help=here)
    p.add_argument("--base", default="HEAD", help="commit the tries start from (default HEAD)")
    p.add_argument("--check", help="the step's Done-when command: the only Bash the "
                   "worker may run, and how the winner is picked")
    p.add_argument("--rung", type=int, help="ladder rung to run (default: the lowest)")
    p.add_argument("--run-id", help="names the worktrees, branches and run folder "
                   "(default: a timestamp)")
    p = sub.add_parser("review", help="every reviewer of a role, read-only, on a diff")
    p.add_argument("--role", required=True)
    p.add_argument("--brief", required=True, help="file holding the brief")
    p.add_argument("--diff", required=True, help="file holding the diff to review")
    p.add_argument("--project", help=here)
    p.add_argument("--workdir", help="folder the reviewers read (default: the project); "
                   "for a build-verify candidate, its winner's worktree")
    p.add_argument("--run-id", help="names the run folder (default: a timestamp)")
    p = sub.add_parser("clean", help="remove a run's worktrees and branches")
    p.add_argument("--run-id", required=True)
    p.add_argument("--project", help=here)
    args = ap.parse_args()
    if os.name == "nt":
        print("error: dispatch is POSIX-only (Linux, macOS, WSL) — it needs process "
              "groups", file=sys.stderr)
        return 2
    # Killing dispatch must not orphan a worker: the signals become an exception, so
    # run_process's finally kills the worker's group. One already ignored stays so.
    for s in SIGNALS:
        if signal.getsignal(s) is not signal.SIG_IGN:
            signal.signal(s, _on_signal)
    commands = {"roles": cmd_roles, "run": cmd_run, "review": cmd_review,
                "clean": cmd_clean}
    try:
        return commands[args.cmd](args)
    except (RolesError, UsageError) as e:
        print("error: {}".format(e), file=sys.stderr)
        return 2
    except Killed as k:
        print("killed by signal {} — worker stopped".format(k.signum), file=sys.stderr)
        return 128 + k.signum


if __name__ == "__main__":
    sys.exit(main())
