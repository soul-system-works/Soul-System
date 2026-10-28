#!/usr/bin/env python3
"""Hand a /soul-workflow step to a worker harness, in its own process and worktree.

The host session (whatever harness and model the Body started in) keeps judgment and
the record; workers are other harness+model pairs that get only a brief (SOUL-I080).
This tool is the thin layer between them: it reads the roles table, starts the
worker through that harness's headless CLI with the host's context kept out, and
hands back the evidence — the patch, the exit, the wall time, the tokens — never a
verdict. It never writes the check record itself: `build-verify` and `accept` launch
tools/delegation-check.py, the recorder, as its own process to run the check
confined and record what it saw, because a worker's report is a claim (SOUL-I066).

  roles  [--project DIR] [--json] [--workflow W]     the effective roles table
  workflows [--project DIR] [--json]                 built-in and custom workflows
  run    --role R --brief FILE [--project DIR] [--base REF] [--check CMD]
         [--rung K] [--run-id ID] [--workflow W]     implement, n tries, pick one
  review --role R --brief FILE --diff FILE [--project DIR] [--workdir DIR]
         [--run-id ID] [--workflow W]                every reviewer of R, read-only
  clean  --run-id ID [--family] [--project DIR]      remove a run's worktrees+branches
                                                     (--family: every <ID>-* run too)
  build-verify --brief FILE --check CMD --run-id ID [--project DIR] [--base REF]
         [--workflow W] [--step TEXT] [--no-review]  one round: ladder, recorded
                                                     check, reviewers, bundle.md
  build-verify --repair-of PREV --accepted FILE [--project DIR] [--workflow W]
         [--no-review]                               a repair round from PREV's winner
  accept --run-id ID [--accepted FILE] [--project DIR]
                                                     apply from the original base,
                                                     re-run the check here, clean

Roles table: `~/.claude/soul-roles.md` (global) and `<project>/.claude/soul-roles.md`,
a Markdown table `| role | harness | model | settings |` — settings `key=value`
separated by spaces, only `rung`, `n` (best-of-n), `timeout` (seconds) and `effort`
(a word: the harness's reasoning effort, unset = the harness's own default). A
project that defines any row for a role replaces ALL global rows for that role.
A role's rows are its ladder, ordered by rung (row order when none is given).
Built-in default for a role neither file names: implementer claude:sonnet then
claude:opus; reviewer claude:opus, plus codex:default when `codex` is on PATH.
With `--workflow W`, a custom workflow file's `## Roles` section (the same table)
sits above both files the same way, per role: workflow, project, global, built-in.
A built-in W has no file, so the shared table; an unknown or ignored W is refused.

`run` makes each try a worktree `<project>/.ai/worktrees/<run-id>-<i>` on branch
`soul-wf/<run-id>-<i>` from --base (default HEAD), stages everything the worker left
(untracked too, never committed), writes the diff against base to
`<project>/.ai/workflow-runs/<run-id>/try-<i>.patch`, and runs --check there, under
bubblewrap (tools/confine.py), only to pick the winner: exited 0 and changed
something, then check passed, then fewest changed lines. Tries run one at a time
(a GPU holds one model). result.json (review.json for `review`) holds what was seen.

POSIX only (Linux, macOS, WSL): a timed-out worker's whole process group is killed.
"""

import argparse
import json
import os
import re
import shlex
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
SETTINGS = ("rung", "n", "timeout", "effort")
# `effort=` is a word, not a number (v3.8.0). Claude Code 2.x `--effort` takes the
# first list; Codex's `model_reasoning_effort` the second. A codex worker runs with
# --ignore-user-config, so without `effort=` it gets Codex's built-in default, not
# the user's ~/.codex/config.toml (seen 2026-10-28: reasoning_effort null).
CLAUDE_EFFORTS = ("low", "medium", "high", "xhigh", "max")
CODEX_EFFORTS = ("minimal", "low", "medium", "high", "xhigh")
EFFORTS = {"claude": CLAUDE_EFFORTS, "claude-ollama": CLAUDE_EFFORTS,
           "codex": CODEX_EFFORTS, "codex-ollama": CODEX_EFFORTS}
DEFAULT_TIMEOUT = 1800
GLOBAL_ROLES = os.path.join("~", ".claude", "soul-roles.md")
PROJECT_ROLES = os.path.join(".claude", "soul-roles.md")
# Custom workflows: one Markdown file of steps each, named by its file (the Body's
# choice, 2026-10-28). The host follows the file; the built-ins live in the skill.
GLOBAL_WORKFLOWS = os.path.join("~", ".claude", "soul-workflows")
PROJECT_WORKFLOWS = os.path.join(".claude", "soul-workflows")
BUILT_IN_WORKFLOWS = {
    "build-verify": "another model implements in its own worktree; the recorder runs "
                    "the check confined; reviewers report; at most two repair rounds",
    "review": "the reviewers alone, read-only, on a diff",
}
WORKFLOW_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
RECORD_FILES = ("witness.md", "ideas.md", "mind.md", "upstream.md")
RECORD_DIRS = (".soul/", "findings/", "amendments/")  # the last two: Soul System's own
CLAUDE_MD_NAMES = ("CLAUDE.md", "CLAUDE.local.md", os.path.join(".claude", "CLAUDE.md"))
WALK_SKIP = (".git", "node_modules", ".venv", "venv", "__pycache__")
OLLAMA_URL = "http://localhost:11434"
RUN_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
SIGNALS = tuple(getattr(signal, n) for n in ("SIGTERM", "SIGINT", "SIGHUP")
                if hasattr(signal, n))

WORKER_RULES = """

## Worker rules (added by dispatch)

- You are a worker with only this brief: no earlier conversation, no project record.
- Do not write witness.md, ideas.md, mind.md, upstream.md, or anything under .soul/,
  findings/ or amendments/.
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
# A list marker may lead: `- `, `> `, `**`, or a number (`1. `, `2) `).
FINDING = re.compile(r"^[\s>*_`-]*(?:\d+[.)]\s*)?[*_`]*FINDING[*_`]*\s*:[*_`]*\s*(.+?)\s*$")
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
    return parse_roles_lines(path, enumerate(lines, 1), source)


def roles_section(path):
    """(lineno, line) of a workflow file's `## Roles` section: from that heading to
    the next heading of level 1 or 2. Lines inside a ``` fence or an HTML comment
    are not part of it, so a file can show an example without it taking effect."""
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
    except FileNotFoundError:
        return []
    out, inside, fence, comment = [], False, False, False
    for lineno, line in enumerate(lines, 1):
        text = line.strip()
        if comment:
            comment = "-->" not in text
            continue
        if text.startswith("<!--"):
            comment = "-->" not in text[4:]
            continue
        if text.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        if re.match(r"#{1,2}\s", text):
            inside = re.fullmatch(r"##\s+roles", text, re.I) is not None
            continue
        if inside:
            out.append((lineno, line))
    return out


def parse_roles_lines(path, numbered, source):
    """Rows of the table lines among `numbered` ((lineno, line) pairs), checked as
    a roles file's are; errors name `path` and the line."""
    rows = []
    position = {}
    rungs = {}  # (role, rung) -> (lineno, line) of the row that holds it
    for lineno, line in numbered:
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
            if key == "effort":
                if value not in EFFORTS[harness]:
                    raise _row_error(path, lineno, line,
                                     "effort for a {} row must be one of {}, got {!r}"
                                     .format(harness, ", ".join(EFFORTS[harness]), value))
                settings[key] = value
                continue
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
        rung = settings.get("rung", position[role])
        if (role, rung) in rungs:
            # Two rows on one rung: `run --rung K` would silently take the first.
            other, other_line = rungs[(role, rung)]
            raise _row_error(path, lineno, line, "rung {} of role {} is also at {}:{} "
                             "(row: {})".format(rung, role, path, other, other_line.strip()))
        rungs[(role, rung)] = (lineno, line)
        rows.append({"role": role, "harness": harness, "model": model,
                     "rung": rung,
                     "n": settings.get("n", 1),
                     "timeout": settings.get("timeout", DEFAULT_TIMEOUT),
                     "effort": settings.get("effort"),
                     "source": source, "where": "{}:{}".format(path, lineno)})
    return rows


def builtin_rows(which=shutil.which):
    def row(role, harness, model, rung):
        return {"role": role, "harness": harness, "model": model, "rung": rung, "n": 1,
                "timeout": DEFAULT_TIMEOUT, "effort": None, "source": "built-in",
                "where": None}
    rows = [row("implementer", "claude", "sonnet", 1),
            row("implementer", "claude", "opus", 2),
            row("reviewer", "claude", "opus", 1)]
    if which("codex"):
        rows.append(row("reviewer", "codex", "default", 2))
    return rows


def load_roles(project, workflow_file=None):
    """{role: [rows ordered by rung]} — the workflow file's `## Roles` section (when
    one is given) over project over global over built-in, per role. Option C, the
    Body's choice of 2026-10-28: one workflow may use other models without changing
    the shared table for every other workflow."""
    layers = [builtin_rows(),
              parse_roles_file(os.path.expanduser(GLOBAL_ROLES), "global"),
              parse_roles_file(os.path.join(project, PROJECT_ROLES), "project")]
    if workflow_file:
        layers.append(parse_roles_lines(workflow_file, roles_section(workflow_file),
                                        "workflow"))
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
    project = project_dir(args.project, need_git=False)
    table = load_roles(project, workflow_file(project, args.workflow))
    if args.json:
        print(json.dumps(flat(table), indent=2))
        return 0
    print("{:<12} {:<5} {:<14} {:<22} {:<3} {:<8} {:<7} {}".format(
        "role", "rung", "harness", "model", "n", "timeout", "effort", "source"))
    for r in flat(table):
        print("{:<12} {:<5} {:<14} {:<22} {:<3} {:<8} {:<7} {}".format(
            r["role"], r["rung"], r["harness"], r["model"], r["n"], r["timeout"],
            r["effort"] or "-", r["source"] + (" ({})".format(r["where"]) if r["where"] else "")))
    return 0


def _description(path):
    """The `description:` line of a workflow file's frontmatter, or ""."""
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return ""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    for line in (m.group(1).splitlines() if m else []):
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip()
    return ""


def load_workflows(project):
    """[{name, source, path, description, note}] — built-ins first, then files. A
    project file replaces a global one of the same name; a file may not take a
    built-in's name (it is listed, marked ignored) or an unusable one."""
    found = {}
    for source, folder in (("global", os.path.expanduser(GLOBAL_WORKFLOWS)),
                           ("project", os.path.join(project, PROJECT_WORKFLOWS))):
        try:
            names = sorted(os.listdir(folder))
        except OSError:
            continue
        for f in names:
            if f.endswith(".md"):
                found[f[:-3]] = (source, os.path.join(folder, f))
    out = [{"name": n, "source": "built-in", "path": None, "description": d, "note": ""}
           for n, d in BUILT_IN_WORKFLOWS.items()]
    for name in sorted(found):
        source, path = found[name]
        note = ("ignored: a built-in has this name" if name in BUILT_IN_WORKFLOWS else
                "ignored: name must be lower-case letters, digits and -"
                if not WORKFLOW_NAME.match(name) else
                "no description: line" if not _description(path) else "")
        out.append({"name": name, "source": source, "path": path,
                    "description": _description(path), "note": note})
    return out


def workflow_file(project, name):
    """The file whose `## Roles` section `--workflow NAME` adds; None for no name or
    a built-in (the shared table). An unknown name, or a file the listing marks
    ignored, is a usage error."""
    if name is None or name in BUILT_IN_WORKFLOWS:
        return None
    found = [w for w in load_workflows(project) if w["name"] == name]
    if not found:
        raise UsageError("no workflow named {!r} (see: dispatch.py workflows)".format(name))
    if found[0]["note"].startswith("ignored"):
        raise UsageError("workflow {!r} is {} ({})".format(name, found[0]["note"],
                                                           found[0]["path"]))
    return found[0]["path"]


def cmd_workflows(args):
    rows = load_workflows(project_dir(args.project, need_git=False))
    if args.json:
        print(json.dumps(rows, indent=2))
        return 0
    for r in rows:
        print("{:<16} {:<9} {}{}".format(r["name"], r["source"], r["description"],
                                         "  [{}]".format(r["note"]) if r["note"] else ""))
        if r["path"]:
            print("{:<16} {:<9} {}".format("", "", r["path"]))
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


def worker_command(row, workdir, mode, last_file=None):
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
        if row.get("effort"):
            cmd += ["--effort", row["effort"]]
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
    if row.get("effort"):
        # Probe, 2026-10-28 (codex-cli 0.163.0, --ignore-user-config): with this the
        # session file recorded "reasoning_effort":"high"; without it, null.
        cmd += ["-c", "model_reasoning_effort=" + row["effort"]]
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
        # modelUsage covers the whole run, per model; `usage` can be the last turn
        # only (the 2026-10-27 replay: usage said 82 output tokens where modelUsage
        # said 26,958). Summed across models, as a run can use more than one.
        per_model = result.get("modelUsage")
        per_model = [u for u in per_model.values() if isinstance(u, dict)] \
            if isinstance(per_model, dict) else []
        if per_model:
            return (sum(u.get(k) or 0 for u in per_model for k in (
                        "inputTokens", "cacheReadInputTokens", "cacheCreationInputTokens")),
                    sum(u.get("outputTokens") or 0 for u in per_model), text)
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
                          errors="replace", stdin=subprocess.DEVNULL)


# Options for dispatch's own git calls in the project checkout (clean, accept): no
# hook and no fsmonitor of the checkout's runs. git 2.53 runs reference-transaction
# hooks even on `branch -D` (the 2026-10-28 review of v3.8.0).
NO_HOOKS = ("-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false")
# Every diff that writes a patch: a user's diff.noprefix, diff.external or textconv
# config would otherwise change the format `git apply` reads back (the same review).
PATCH_FORMAT = ("--no-ext-diff", "--no-textconv", "--src-prefix=a/", "--dst-prefix=b/")


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


def role_rows(project, role, workflow=None):
    rows = load_roles(project, workflow_file(project, workflow)).get(role)
    if not rows:
        raise UsageError("no role {!r} in the roles table (see: dispatch.py roles{})"
                         .format(role, " --workflow " + workflow if workflow else ""))
    return rows


def with_workflow(payload, workflow):
    """`payload` plus a `workflow` field when --workflow was given (only then)."""
    return dict(payload, workflow=workflow) if workflow else payload


def read_text(path, what):
    try:
        # errors="replace": a worker's patch may hold non-UTF-8 bytes (a Latin-1
        # file crashed bundle-building after the pass was recorded — 2026-10-28 review)
        with open(path, encoding="utf-8", errors="replace") as fh:
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


def with_effort(payload, row):
    """`payload` plus the row's `effort` when the row sets one (only then)."""
    return dict(payload, effort=row["effort"]) if row.get("effort") else payload


def write_json(path, result):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
        fh.write("\n")


# ---------------------------------------------------------------- run

def worktree_git(project, worktree):
    """git options that reach `worktree` through the project's own records of it,
    never through the worktree's `.git` file, which the worker can rewrite: a worker
    that swapped it for a repo of its own with a core.fsmonitor hook had that hook
    run by dispatch's `git add`, unconfined, on the host (the 2026-10-27 review of
    v3.7.0). Taken before the worker starts; the admin folder must point back here."""
    common = git(project, "rev-parse", "--git-common-dir").stdout.strip()
    admins = os.path.join(os.path.realpath(os.path.join(project, common)), "worktrees")
    want = os.path.realpath(os.path.join(worktree, ".git"))
    # Usually worktrees/<basename>; git adds a number when that name is taken.
    names = [os.path.basename(worktree)] + sorted(
        os.listdir(admins) if os.path.isdir(admins) else [])
    for name in names:
        try:
            with open(os.path.join(admins, name, "gitdir"), encoding="utf-8") as fh:
                points = fh.read().strip()
        except OSError:
            continue
        if os.path.realpath(points) == want:
            return ["--git-dir=" + os.path.join(admins, name), "--work-tree=" + worktree,
                    "-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null"]
    raise UsageError("cannot find git's record of the worktree {} in {}".format(
        worktree, admins))


def stage_and_diff(worktree, gitargs, base, patch_path):
    """Stage everything the worker left (untracked too; never commit) and write the
    diff against base. Returns (changed_lines, record_touched). `gitargs` come
    from worktree_git."""
    git(worktree, *gitargs, "add", "-A")
    patch = subprocess.run(["git", *gitargs, "diff", "--cached", "--binary", "--no-renames",
                            *PATCH_FORMAT, base], cwd=worktree, capture_output=True,
                           stdin=subprocess.DEVNULL)
    with open(patch_path, "wb") as fh:
        fh.write(patch.stdout)
    changed = 0
    for line in git(worktree, *gitargs, "diff", "--cached", "--numstat", "--no-renames",
                    base).stdout.splitlines():
        added, deleted = line.split("\t")[:2]  # "-" for a binary file: counts 0
        changed += (int(added) if added.isdigit() else 0) + (
            int(deleted) if deleted.isdigit() else 0)
    names = git(worktree, *gitargs, "diff", "--cached", "--name-only", "-z", "--no-renames",
                base).stdout.split("\0")
    touched = any(n in RECORD_FILES or n.startswith(RECORD_DIRS) for n in names if n)
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
    """A try that exited 0 and changed something, then (when the check ran) passed
    it, then fewest changed lines. A check that already passes at base made an
    empty or timed-out try the winner — fewest lines is zero (the 2026-10-27
    review). A try that touched the Soul record, or ran without its sandbox, is
    never the winner."""
    ok = [t for t in tries if not t["record_touched"] and not t.get("sandbox_inactive")
          and t["exit"] == 0 and t["changed_lines"] > 0]
    if have_check:
        ok = [t for t in ok if t["check_rc"] == 0]
    return min(ok, key=lambda t: (t["changed_lines"], t["try"]))["try"] if ok else None


def confinable_here(project):
    return confine.confine_argv(["true"], project) is not None


def need_confine_for_n(row, check, project):
    # The selection check runs the worker's code, so it runs confined (the 2026-10-27
    # review: it ran with the host's whole environment and no sandbox). Where it
    # cannot be confined, one try skips it — the host's confined re-run through the
    # recorder is the gate — and best-of-n, which needs it to choose, is refused.
    if check and row["n"] > 1 and not confinable_here(project):
        raise UsageError("best-of-n runs each try's check, which needs bubblewrap to "
                         "confine it — install it (e.g. `sudo apt install bubblewrap`) "
                         "or use n=1")


def resolve_base(project, ref, flag="--base"):
    base = git(project, "rev-parse", "--verify", "--quiet", ref + "^{commit}")
    if base.returncode != 0:
        raise UsageError("{} {!r} is not a commit".format(flag, ref))
    return base.stdout.strip()


def cmd_run(args):
    project = project_dir(args.project)
    rows = role_rows(project, args.role, args.workflow)
    rung = args.rung if args.rung is not None else rows[0]["rung"]
    row = next((r for r in rows if r["rung"] == rung), None)
    if row is None:
        raise UsageError("role {!r} has no rung {} (its rungs: {})".format(
            args.role, rung, ", ".join(str(r["rung"]) for r in rows)))
    need_harness([row])
    need_sandbox([row])
    if args.check is not None and not args.check.strip():
        raise UsageError("--check is blank")
    need_confine_for_n(row, args.check, project)
    brief = read_text(args.brief, "brief")
    base = resolve_base(project, args.base)
    run_id = args.run_id or time.strftime("%Y%m%d-%H%M%S")
    result = run_tries(project, args.role, row, brief, args.check, base, run_id,
                       args.workflow)
    print(json.dumps(result, indent=2))
    return 0 if result["winner"] is not None else 1


def run_tries(project, role, row, brief, check, base, run_id, workflow):
    """One `run`: `row`'s n tries of `brief` from `base`, each in its own worktree,
    one picked. Writes result.json and the dispatch event and returns the result;
    the caller prints. Shared by `run` and `build-verify` (v3.8.0), so the ladder
    that build-verify climbs is the same machinery a custom workflow's `run` uses."""
    confinable = confinable_here(project)
    run_dir = run_dir_for(project, run_id)
    if os.path.exists(os.path.join(run_dir, "result.json")):
        raise UsageError("run id {} already has a result.json".format(run_id))
    os.makedirs(run_dir, exist_ok=True)
    prompt = brief.rstrip("\n") + WORKER_RULES.format(
        check=": `{}`".format(check) if check else " (no check was named: say so)")

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
        gitargs = worktree_git(project, worktree)
        stem = os.path.join(run_dir, "try-{}".format(i))
        last = stem + ".last.txt"
        code, wall = run_process(worker_command(row, worktree, "run", last),
                                 worktree, worker_env(row["harness"]), prompt,
                                 stem + ".log", stem + ".stderr", row["timeout"])
        tokens_in, tokens_out, _ = read_output(row["harness"], stem + ".log", last)
        changed, touched = stage_and_diff(worktree, gitargs, base, stem + ".patch")
        # A try whose shell ran unconfined or not at all can never win.
        inactive = sandbox_inactive(row, stem + ".stderr")
        check_rc = None
        if check and confinable:  # for selection only: the recorder re-runs it
            check_rc, _ = run_process(
                confine.confine_argv(["/bin/sh", "-c", check], worktree), worktree,
                confine.clean_env(), "", stem + ".check.log", None, row["timeout"])
        tries.append({"try": i, "worktree": worktree, "branch": branch, "exit": code,
                      "wall_s": wall, "tokens_in": tokens_in, "tokens_out": tokens_out,
                      "effort": row.get("effort"),
                      "patch": stem + ".patch", "log": stem + ".log",
                      "changed_lines": changed, "check_rc": check_rc,
                      "record_touched": touched, "sandbox_inactive": inactive})
    result = with_workflow({
        "run_id": run_id, "role": role, "harness": row["harness"],
        "model": row["model"], "effort": row.get("effort"), "rung": row["rung"],
        "base": base, "check": check, "check_skipped": bool(check) and not confinable,
        "tries": tries, "winner": pick_winner(tries, bool(check) and confinable)},
        workflow)
    if result["check_skipped"]:
        print("note: no bubblewrap here, so the selection check did not run; the "
              "recorder's confined re-run is the gate", file=sys.stderr)
    write_json(os.path.join(run_dir, "result.json"), result)
    log_dispatch(project, with_workflow(with_effort({
        "mode": "run", "run_id": run_id, "role": role, "harness": row["harness"],
        "model": row["model"], "rung": row["rung"], "tries": len(tries),
        "won": result["winner"] is not None,
        "timeouts": sum(1 for t in tries if t["exit"] == "timeout"),
        "wall_s": round(sum(t["wall_s"] for t in tries), 1)}, row), workflow))
    return result


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
    rows = role_rows(project, args.role, args.workflow)
    need_harness(rows)
    need_sandbox(rows)
    brief = read_text(args.brief, "brief")
    diff = read_text(args.diff, "diff")
    run_id = args.run_id or time.strftime("%Y%m%d-%H%M%S")
    result = review_all(project, args.role, rows, workdir, brief, diff, run_id,
                        args.workflow)
    print(json.dumps(result, indent=2))
    return 0


def review_all(project, role, rows, workdir, brief, diff, run_id, workflow):
    """Every reviewer row once, read-only, in `workdir`. Writes review.json and one
    dispatch event per reviewer and returns the result; the caller prints. Shared by
    `review` and `build-verify` (v3.8.0)."""
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
                          "effort": row.get("effort"),
                          "exit": code, "wall_s": wall, "tokens_in": tokens_in,
                          "tokens_out": tokens_out, "raw": stem + ".txt",
                          "log": stem + ".log", "findings": findings, "verdict": verdict,
                          "sandbox_inactive": inactive})
    result = with_workflow({"run_id": run_id, "role": role, "reviewers": reviewers},
                           workflow)
    write_json(os.path.join(run_dir, "review.json"), result)
    for r in reviewers:
        log_dispatch(project, with_workflow(with_effort({
            "mode": "review", "run_id": run_id, "role": role, "harness": r["harness"],
            "model": r["model"], "tries": 1,
            "won": r["exit"] == 0 and r["verdict"] in ("findings", "none"),
            "timeouts": 1 if r["exit"] == "timeout" else 0, "wall_s": r["wall_s"]}, r),
            workflow))
    return result


# ---------------------------------------------------------------- clean

def cmd_clean(args):
    project = project_dir(args.project)
    run_dir_for(project, args.run_id)  # validates the id
    # --family: only the names dispatch and the skill make from this id — tries
    # <id>-<i>, <id>-k<rung>-a<attempt>-<i>, <id>-r<round>[-k..-a..]-<i>, and the
    # review workflow's <id>-head. `<id>-<anything>` was the first pattern; it took
    # family X-2's worktrees when X was accepted (the 2026-10-28 review of v3.8.0).
    own = re.compile(r"\A" + re.escape(args.run_id) + (
        r"(?:(?:-r\d+)?(?:-k\d+-a\d+)?-\d+|-head)\Z" if args.family else r"-\d+\Z"))
    root = os.path.realpath(os.path.join(project, ".ai", "worktrees"))
    removed = []
    for line in git(project, *NO_HOOKS, "worktree", "list", "--porcelain").stdout.splitlines():
        if not line.startswith("worktree "):
            continue
        path = line[len("worktree "):]
        if (os.path.dirname(os.path.realpath(path)) != root
                or not own.match(os.path.basename(path))):
            continue
        r = git(project, *NO_HOOKS, "worktree", "remove", "--force", path)
        if r.returncode != 0:
            print("warning: could not remove {}: {}".format(path, r.stderr.strip()),
                  file=sys.stderr)
        else:
            removed.append(path)
    git(project, *NO_HOOKS, "worktree", "prune")
    deleted = 0
    for b in git(project, *NO_HOOKS, "for-each-ref", "--format=%(refname:short)",
                 "refs/heads/soul-wf/").stdout.split():
        if not own.match(b[len("soul-wf/"):]):
            continue
        r = git(project, *NO_HOOKS, "branch", "-D", b)
        if r.returncode != 0:  # e.g. still checked out in a worktree that stayed
            print("warning: could not delete branch {}: {}".format(b, r.stderr.strip()),
                  file=sys.stderr)
        else:
            deleted += 1
    print("removed {} worktree(s) and {} branch(es) of run {}{}; its evidence stays in "
          ".ai/workflow-runs/".format(len(removed), deleted, args.run_id,
                                      " and its family" if args.family else ""))
    return 0


# ---------------------------------------------------------------- build-verify
#
# Round 1 of the workflow-value test (soul-benchmark experiments/2026-10-28-
# workflow-value/RESULT.md): build-verify cost 3.3x plain Claude Code for the same
# quality. The workers were cheap; the host was not — 32 turns (plain: 8) spent on
# mechanics: launching each attempt, reading result.json, re-running the check,
# launching review, recording tallies, committing the candidate, applying. The
# owner's call (2026-10-28): one call per round does the mechanics; the host reads
# one bundle, weighs the findings, and decides. The check is still never a worker's
# word: the recorder runs it, confined, as its own process.

RECORDER = os.path.join(_HERE, "delegation-check.py")
MAX_ROUND = 3  # round 1 plus at most two repair rounds without the owner
INLINE_PATCH_LINES = 600
ACCEPTED_LINE = re.compile(r"^[-*]?\s*(F\d+)(?!\w)\s*(?:[:—–-]\s*)?(.*)$")

FAILED_ATTEMPT = """

## The previous attempt failed

This is a fresh attempt from the same starting point. What the previous attempt
left, as the dispatch tool saw it:
"""


def tail_lines(text, n):
    lines = (text or "").rstrip("\n").splitlines()
    return "\n".join(lines[-n:])


def fenced(text, lang=""):
    """`text` in a code fence longer than any backtick run inside it."""
    longest = max([len(m) for m in re.findall(r"`+", text)] + [0])
    fence = "`" * max(3, longest + 1)
    return "{}{}\n{}\n{}".format(fence, lang, text.rstrip("\n"), fence)


def run_recorder(argv, cwd):
    """(exit code, output) of tools/delegation-check.py run as its own process: the
    recorder is the instrument the worker did not make, so dispatch launches it and
    reads its exit code — never imports it and calls it in-process. Killed while it
    runs, dispatch passes SIGTERM on: the recorder then kills its check's process
    group and records nothing."""
    proc = subprocess.Popen([sys.executable, RECORDER] + argv, cwd=cwd,
                            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    try:
        out, _ = proc.communicate()
    except BaseException:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()
        raise
    return proc.returncode, out.decode("utf-8", "replace")


def record_check(project, ctx, row, cwd, run_id, round_no):
    """Run ctx's check through the recorder, confined, in `cwd`. Returns {rc, tail,
    counted}: `counted` when the recorder ran the check and recorded the result —
    exit 0 or 1, or 2 for a check that timed out (the recorder records a timeout
    and prints "FAIL (timeout"). Any other 2 is a refusal (no bubblewrap, a check
    that could not start): nothing was recorded."""
    # Values go as `--opt=value`: a step that starts with `-` (a brief whose first
    # line is `---`) made the recorder's argparse fail (the 2026-10-28 review). No
    # --project: the recorder finds the Soul project from its working directory, as
    # the host's own call always did; --project made it create .soul/events.jsonl in
    # projects that do not use Soul (the same review).
    rc, out = run_recorder(
        ["record", "--step=" + ctx["step"],
         "--worker=implementer:{}:{}".format(row["harness"], row["model"]),
         "--check=" + ctx["check"], "--cwd=" + cwd, "--confine",
         "--workflow=" + ctx["workflow"], "--role=implementer",
         "--rung={}".format(row["rung"]), "--round={}".format(round_no),
         "--run-id=" + run_id,
         # The row's timeout, as the selection check had: the recorder's own default
         # (540 s) would record a slower check as a timeout the selection passed.
         "--timeout={}".format(row.get("timeout", DEFAULT_TIMEOUT))],
        project)
    counted = rc in (0, 1) or (rc == 2 and "FAIL (timeout" in out)
    return {"rc": rc, "tail": tail_lines(out, 40), "counted": counted}


def failure_section(run_dir, result, rec):
    """What attempt 2 is told about attempt 1: each try's exit, changed lines and
    the end of its check log, and the recorder's word when it disagreed."""
    out = [FAILED_ATTEMPT]
    for t in result["tries"]:
        log = read_text_quiet(os.path.join(run_dir, "try-{}.check.log".format(t["try"])))
        out.append("\n- try {}: exit {}, {} changed line(s), check {}; {}\n".format(
            t["try"], t["exit"], t["changed_lines"],
            "not run" if t["check_rc"] is None else "exit {}".format(t["check_rc"]),
            "the end of its check's output:\n\n" + fenced(tail_lines(log, 60)) + "\n"
            if log.strip() else "no check output"))
    if rec is not None and rec["rc"] != 0:
        out.append("\nThe recorder's re-run of the check on the selected try failed "
                   "(exit {}):\n\n{}\n".format(rec["rc"], fenced(rec["tail"])))
    return "".join(out)


def load_bundle(project, run_id):
    path = os.path.join(run_dir_for(project, run_id), "bundle.json")
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as e:
        raise UsageError("no readable bundle for run {} ({}): pass a build-verify "
                         "round's family run id".format(run_id, e)) from None


def parse_accepted(path, bundle, allow_empty):
    """{finding id: the host's note} from an accepted-findings file: one finding per
    line, each starting with an id from the bundle (`F2`, `F2: note`, `F2 — note`)."""
    text = read_text(path, "accepted findings")
    known = {f["id"] for f in bundle.get("findings") or []}
    accepted, bad, unknown = {}, [], []
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        m = ACCEPTED_LINE.match(line.strip())
        if not m:
            bad.append(str(lineno))
        elif m.group(1) not in known:
            unknown.append(m.group(1))
        else:
            note = m.group(2).strip()
            prev = accepted.get(m.group(1))
            accepted[m.group(1)] = "; ".join(x for x in (prev, note) if x)
    if bad:
        raise UsageError("{}: line(s) {} do not start with a finding id (F1, F2, …)"
                         .format(path, ", ".join(bad)))
    if unknown:
        raise UsageError("{}: no finding {} in run {} (it has: {})".format(
            path, ", ".join(unknown), bundle["run_id"],
            ", ".join(sorted(known, key=lambda x: int(x[1:]))) or "none"))
    if not accepted and not allow_empty:
        raise UsageError("{}: nothing accepted — use `accept`, not a repair".format(path))
    return accepted


def record_tallies(project, bundle, accepted):
    """One `delegation-check.py review` per reviewer of `bundle`'s round: findings
    raised, and how many the host accepted (handed in, so self-reported there)."""
    review = bundle.get("review")
    lines = []
    for r in (review or {}).get("reviewers", []):
        ids = r["finding_ids"]
        rc, out = run_recorder(  # `=` values and no --project: see record_check
            ["review", "--run-id=" + review["run_id"],
             "--reviewer={}:{}".format(r["harness"], r["model"]),
             "--raised={}".format(len(ids)),
             "--accepted={}".format(sum(1 for i in ids if i in accepted))], project)
        if rc != 0:  # a tally that cannot be written never stops the round
            print("warning: review tally not recorded (exit {}): {}".format(
                rc, tail_lines(out, 5)), file=sys.stderr)
        lines.append(out.strip())
    return lines


def read_cost(harness, log_path):
    """total_cost_usd from a `claude` worker's JSON result, else None — never for
    claude-ollama, whose runs report a made-up price (SOUL-200), nor codex, which
    reports none."""
    if harness != "claude":
        return None
    result = next((ev for ev in reversed(_json_lines(log_path))
                   if "result" in ev or "usage" in ev), {})
    cost = result.get("total_cost_usd")
    return cost if isinstance(cost, (int, float)) and not isinstance(cost, bool) else None


def first_line(text):
    return next((l.strip() for l in text.splitlines() if l.strip()), "")[:120]


def prepare_first(project, args):
    """The first round's context, checked; nothing is started or written."""
    for flag, value in (("--brief", args.brief), ("--check", args.check),
                        ("--run-id", args.run_id)):
        if not value:
            raise UsageError("build-verify needs {} (or --repair-of for a repair "
                             "round)".format(flag))
    if args.accepted:
        raise UsageError("--accepted goes with --repair-of (or with `accept`)")
    if not args.check.strip():
        raise UsageError("--check is blank")
    brief = read_text(args.brief, "brief")
    base = resolve_base(project, args.base or "HEAD")
    workflow = args.workflow or "build-verify"
    return {"family": args.run_id, "round": 1, "prefix": args.run_id,
            "original_base": base, "base": base, "brief_text": brief,
            "original_brief": None, "check": args.check,
            "step": args.step or first_line(brief), "workflow": workflow,
            "start_rung": None, "prev": None, "accepted": {}}


def prepare_repair(project, args):
    """A repair round's context from PREV's bundle, checked; nothing written yet."""
    for flag, value in (("--brief", args.brief), ("--check", args.check),
                        ("--run-id", args.run_id), ("--base", args.base),
                        ("--step", args.step)):
        if value:
            raise UsageError("{} is not taken with --repair-of: a repair round keeps "
                             "the previous round's".format(flag))
    if not args.accepted:
        raise UsageError("--repair-of needs --accepted FILE (the findings to fix)")
    prev = load_bundle(project, args.repair_of)
    if prev.get("status") != "winner" or not prev.get("winner"):
        raise UsageError("run {} has no recorded winner to repair (status {})".format(
            args.repair_of, prev.get("status")))
    if prev["round"] >= MAX_ROUND:
        raise UsageError("run {} is round {}: two repair rounds are spent — bring it "
                         "to the owner".format(args.repair_of, prev["round"]))
    accepted = parse_accepted(args.accepted, prev, allow_empty=False)
    found = {f["id"]: f for f in prev["findings"]}
    round_no = prev["round"] + 1
    lines = ["\n\n## Accepted findings to fix\n\n"
             "Reviewers read the previous candidate (the code you start from) and "
             "raised these; the host checked each against the code and accepted it.\n"]
    for fid, note in accepted.items():
        lines.append("\n- {} [{}] {}".format(fid, found[fid]["reviewer"], found[fid]["text"]))
        if note:
            lines.append("\n  Host's note: {}".format(note))
    original = read_text(prev["original_brief"], "original brief")
    return {"family": prev["family"], "round": round_no,
            "prefix": "{}-r{}".format(prev["family"], round_no),
            "original_base": prev["original_base"], "base": None,
            "brief_text": original.rstrip("\n") + "".join(lines) + "\n",
            "original_brief": prev["original_brief"], "check": prev["check"],
            "step": prev["step"], "workflow": args.workflow or prev["workflow"],
            "start_rung": prev["winner"]["rung"], "prev": prev, "accepted": accepted}


def index_from_patch(project, winner, base):
    """Set the winner worktree's index to `base` plus the winner's stored try patch —
    the patch the host read — and return its git options (worktree_git). Never
    `add -A` on the live worktree: the selection check and the recorder ran there
    with write access, and their artefacts (build.out, __pycache__) were swept into
    the candidate commit and the applied patch (the 2026-10-28 review of v3.8.0).
    The worktree's files are left as they are."""
    gitargs = worktree_git(project, winner["worktree"])
    for args in (("read-tree", base), ("apply", "--cached", "--binary", winner["patch"])):
        r = git(winner["worktree"], *gitargs, *args)
        if r.returncode != 0:
            raise UsageError("git {} in {} failed: {}".format(
                args[0], winner["worktree"], (r.stderr or r.stdout).strip()))
    return gitargs


def commit_candidate(project, prev):
    """Commit PREV's winner on its own worktree branch, through the project's own
    record of the worktree (worktree_git): the worker could rewrite the worktree's
    `.git`, and a hook of its making must not run here (the 2026-10-27 review). The
    identity is given and signing is off, so a host's git config cannot stop it."""
    w = prev["winner"]
    gitargs = index_from_patch(project, w, prev["base"])
    done = git(w["worktree"], *gitargs, "-c", "user.name=soul-workflow",
               "-c", "user.email=soul-workflow@localhost", "-c", "commit.gpgsign=false",
               "commit", "--no-verify", "-qm",
               "candidate {} round {}".format(prev["run_id"], prev["round"]))
    staged = git(w["worktree"], *gitargs, "diff", "--cached", "--quiet").returncode
    if done.returncode != 0 and staged != 0:
        raise UsageError("could not commit the candidate in {}: {}".format(
            w["worktree"], (done.stderr or done.stdout).strip()))
    return resolve_base(project, w["branch"], "the candidate branch")


def cmd_build_verify(args):
    project = project_dir(args.project)
    ctx = prepare_repair(project, args) if args.repair_of else prepare_first(project, args)
    run_dir = run_dir_for(project, ctx["prefix"])
    if os.path.exists(os.path.join(run_dir, "bundle.json")):
        raise UsageError("run {} already has a bundle.json".format(ctx["prefix"]))
    review_id = "{}-rev{}".format(ctx["family"], ctx["round"])
    if not args.no_review and os.path.exists(
            os.path.join(run_dir_for(project, review_id), "review.json")):
        raise UsageError("review run {} already has a review.json".format(review_id))
    rows = role_rows(project, "implementer", ctx["workflow"])
    start = ctx["start_rung"] if ctx["start_rung"] is not None else rows[0]["rung"]
    ladder = [r for r in rows if r["rung"] >= start]
    if not ladder:
        raise UsageError("role 'implementer' has no rung {} or above".format(start))
    reviewers = [] if args.no_review else role_rows(project, "reviewer", ctx["workflow"])
    need_harness(ladder + reviewers)
    need_sandbox(ladder + reviewers)
    for row in ladder:
        need_confine_for_n(row, ctx["check"], project)
    # The recorder confines every check; without bubblewrap it refuses, and the round
    # would end check-not-recorded only after a worker had spent its tokens.
    if not confinable_here(project):
        raise UsageError("build-verify records each check confined, which needs "
                         "bubblewrap here — install it (e.g. `sudo apt install "
                         "bubblewrap`), or use the `run`/`review` building blocks")

    os.makedirs(run_dir, exist_ok=True)
    tallies = []
    if ctx["prev"]:
        # Tallies only once the candidate is committed: a repair refused there can be
        # retried without counting the reviewers twice.
        ctx["base"] = commit_candidate(project, ctx["prev"])
        tallies = record_tallies(project, ctx["prev"], ctx["accepted"])
    brief_path = os.path.join(run_dir, "brief.md")
    with open(brief_path, "w", encoding="utf-8") as fh:
        fh.write(ctx["brief_text"])
    if ctx["original_brief"] is None:  # round 1: its own copy is the original
        ctx["original_brief"] = brief_path

    status, attempts, chosen, rec = "no-winner", [], None, None
    for row in ladder:
        prompt, last = ctx["brief_text"], None
        for attempt in (1, 2):
            run_id = "{}-k{}-a{}".format(ctx["prefix"], row["rung"], attempt)
            if attempt == 2:
                prompt = ctx["brief_text"].rstrip("\n") + failure_section(*last)
                with open(os.path.join(run_dir, "brief-k{}-a2.md".format(row["rung"])),
                          "w", encoding="utf-8") as fh:
                    fh.write(prompt)
            result = run_tries(project, "implementer", row, prompt, ctx["check"],
                               ctx["base"], run_id, ctx["workflow"])
            entry = {"run_id": run_id, "rung": row["rung"], "attempt": attempt,
                     "harness": row["harness"], "model": row["model"],
                     "effort": row.get("effort"), "selected": result["winner"],
                     "recorder_rc": None, "tries": result["tries"]}
            attempts.append(entry)
            rec = None
            if result["winner"] is not None:
                t = result["tries"][result["winner"] - 1]
                rec = record_check(project, ctx, row, t["worktree"], run_id, ctx["round"])
                entry["recorder_rc"] = rec["rc"]
                chosen = dict({k: t[k] for k in ("try", "worktree", "branch", "patch")},
                              run_id=run_id, harness=row["harness"], model=row["model"],
                              effort=row.get("effort"), rung=row["rung"],
                              timeout=row["timeout"])
                if rec["rc"] == 0:
                    status = "winner"
                elif not rec["counted"]:
                    status = "check-not-recorded"
            if status != "no-winner":
                break
            last = (run_dir_for(project, run_id), result, rec)
        if status != "no-winner":
            break
    if status == "no-winner":
        chosen = None  # a try the recorder failed is not shown as the candidate

    review, findings = None, []
    if status == "winner" and reviewers:
        result = review_all(project, "reviewer", reviewers,
                            os.path.realpath(chosen["worktree"]), ctx["brief_text"],
                            read_text(chosen["patch"], "winner's patch"), review_id,
                            ctx["workflow"])
        review = {"run_id": review_id, "reviewers": []}
        for r in result["reviewers"]:
            ids = []
            for text in r["findings"]:
                ids.append("F{}".format(len(findings) + 1))
                findings.append({"id": ids[-1], "reviewer": "{}:{}".format(
                    r["harness"], r["model"]), "text": text})
            review["reviewers"].append(dict(r, finding_ids=ids))

    bundle = {"run_id": ctx["prefix"], "family": ctx["family"], "round": ctx["round"],
              "status": status, "workflow": ctx["workflow"], "step": ctx["step"],
              "check": ctx["check"], "project": project,
              "original_base": ctx["original_base"], "base": ctx["base"],
              "original_brief": ctx["original_brief"], "brief": brief_path,
              "repair_of": ctx["prev"]["run_id"] if ctx["prev"] else None,
              "accepted": ctx["accepted"], "tallies": tallies,
              "winner": chosen if status == "winner" else None,
              "candidate": chosen, "attempts": attempts,
              "recorded_check": rec and {"command": ctx["check"], "rc": rec["rc"],
                                         "tail": rec["tail"]},
              "review": review, "findings": findings}
    write_json(os.path.join(run_dir, "bundle.json"), bundle)
    text = bundle_md(project, bundle)
    with open(os.path.join(run_dir, "bundle.md"), "w", encoding="utf-8") as fh:
        fh.write(text)
    print(text, end="")
    return {"winner": 0, "no-winner": 1}.get(status, 2)


def bundle_md(project, b):
    """Everything the host needs from a round, in ONE read: status, the winning row,
    the recorded check, the patch, the findings, the cost, the next commands."""
    say = {"winner": "winner recorded passing", "no-winner": "no winner",
           "check-not-recorded": "check not recorded"}[b["status"]]
    out = ["# build-verify {} — {}\n\n".format(b["run_id"], say),
           "Status: {} · round {} of {} · family run id {}{}\n".format(
               say, b["round"], MAX_ROUND, b["family"],
               " · repair of {}".format(b["repair_of"]) if b["repair_of"] else "")]
    c = b["candidate"]
    if c:
        out.append("Implementer: {}:{} · effort {} · rung {} · run {} try {}\n".format(
            c["harness"], c["model"], c["effort"] or "-", c["rung"], c["run_id"], c["try"]))
    per_rung = {}
    for a in b["attempts"]:
        per_rung[a["rung"]] = a["attempt"]
    out.append("Attempts: {}\n".format(" · ".join(
        "rung {}: {}".format(k, v) for k, v in per_rung.items()) or "none"))

    out.append("\n## Recorded check\n\n")
    r = b["recorded_check"]
    if r:
        out.append("`{}` — recorder exit {}\n\n{}\n".format(r["command"], r["rc"],
                                                           fenced(r["tail"])))
        if b["status"] == "check-not-recorded":
            out.append("\nThe recorder refused or could not run the check (its output is "
                       "above), so nothing was recorded. What to do next is the owner's "
                       "call.\n")
    else:
        out.append("The last attempt selected no try, so the recorder ran nothing.\n")
    if b["status"] == "no-winner":
        out.append("\nEach attempt (selection check per try; recorder exit when a try "
                   "was selected):\n\n")
        for a in b["attempts"]:
            out.append("- {} ({}:{}): {}; recorder {}\n".format(
                a["run_id"], a["harness"], a["model"], "; ".join(
                    "try {} exit {}, {} lines, check {}".format(
                        t["try"], t["exit"], t["changed_lines"], t["check_rc"])
                    for t in a["tries"]),
                "-" if a["recorder_rc"] is None else "exit {}".format(a["recorder_rc"])))

    if c:
        out.append("\n## Patch\n\n")
        numstat = git(project, "apply", "--numstat", c["patch"]).stdout.strip()
        out.append("{}\n\n".format(fenced(numstat or "(empty)")))
        patch = read_text_quiet(c["patch"])
        if len(patch.splitlines()) <= INLINE_PATCH_LINES:
            out.append(fenced(patch, "diff") + "\n")
        else:
            out.append("{} lines — at {}; read it before accepting.\n".format(
                len(patch.splitlines()), c["patch"]))

    out.append("\n## Findings\n\n")
    if b["review"] is None:
        out.append("No review ran{}.\n".format(
            "" if b["status"] == "winner" else " (no recorded winner)"))
    else:
        out.extend("{} [{}] {}\n".format(f["id"], f["reviewer"], f["text"])
                   for f in b["findings"])
        if not b["findings"]:
            out.append("None.\n")
        out.append("\nReviewers:\n")
        for rv in b["review"]["reviewers"]:
            out.append("- {}:{} (effort {}) — {}, exit {}, {} s{}\n".format(
                rv["harness"], rv["model"], rv["effort"] or "-", rv["verdict"], rv["exit"],
                rv["wall_s"], ", findings " + " ".join(rv["finding_ids"])
                if rv["finding_ids"] else ""))
            if rv["verdict"] == "unparsed":
                raw = read_text_quiet(rv["raw"]) or read_text_quiet(
                    rv["log"][:-len(".log")] + ".stderr")
                out.append("\n" + fenced(tail_lines(raw, 30) or "(no output)") + "\n")

    out.append("\n## Cost\n\n")
    total, unknown = 0.0, 0
    workers = [("implementer", a["run_id"], t, a["harness"], a["model"])
               for a in b["attempts"] for t in a["tries"]]
    workers += [("reviewer", b["review"]["run_id"], rv, rv["harness"], rv["model"])
                for rv in (b["review"] or {}).get("reviewers", [])]
    for role, run_id, w, harness, model in workers:
        cost = read_cost(harness, w["log"])
        if cost is None:
            unknown += 1
        else:
            total += cost
        out.append("- {} {}{} {}:{} — tokens in {} / out {}, {} s{}\n".format(
            role, run_id, " try {}".format(w["try"]) if "try" in w else "", harness, model,
            w["tokens_in"], w["tokens_out"], w["wall_s"],
            ", ${:.4f}".format(cost) if cost is not None else ""))
    out.append("Reported cost: ${:.4f}{}\n".format(
        total, " ({} worker(s) report none)".format(unknown) if unknown else ""))

    out.append("\n## Next\n\n")
    tool = "python3 " + shlex.quote(os.path.abspath(__file__))
    where = " --project " + shlex.quote(project)
    accepted = os.path.join(run_dir_for(project, b["run_id"]), "accepted.txt")
    if b["status"] == "winner":
        if b["findings"] and b["round"] < MAX_ROUND:
            out.append("Repair: write the accepted finding ids, one per line (`F1: note`), "
                       "to {} and run\n  {} build-verify --repair-of {} --accepted {}{}\n"
                       .format(accepted, tool, b["run_id"], shlex.quote(accepted), where))
        elif b["findings"]:
            out.append("No repair round left: two repair rounds are spent — bring open "
                       "findings to the owner.\n")
        out.append("Accept: {} accept --run-id {}{}{}\n".format(
            tool, b["run_id"], " [--accepted {}]".format(shlex.quote(accepted))
            if b["findings"] else "", where))
    elif b["status"] == "no-winner":
        out.append("Every rung's two attempts failed: bring it to the owner with this "
                   "evidence. Clean up after: {} clean --run-id {} --family{}\n".format(
                       tool, b["family"], where))
    else:
        out.append("The recorder refused or could not run the check: bring its output "
                   "to the owner. Clean up after: {} clean --run-id {} --family{}\n"
                   .format(tool, b["family"], where))
    return "".join(out)


# ---------------------------------------------------------------- accept

def cmd_accept(args):
    """Apply the final round's change from the ORIGINAL base, spot-check it here
    through the recorder, and clean the family's worktrees and branches."""
    project = project_dir(args.project)
    # From a subfolder, `git apply` silently skips paths outside it and still exits
    # 0 (the 2026-10-28 review): apply only at the top level.
    top = git(project, *NO_HOOKS, "rev-parse", "--show-toplevel").stdout.strip()
    if not top or os.path.realpath(top) != os.path.realpath(project):
        raise UsageError("accept applies at the git top level; --project {} is not it "
                         "({})".format(project, top or "no top level"))
    bundle = load_bundle(project, args.run_id)
    if bundle.get("status") != "winner" or not bundle.get("winner"):
        raise UsageError("run {} has no recorded winner to accept (status {})".format(
            args.run_id, bundle.get("status")))
    accepted = parse_accepted(args.accepted, bundle, allow_empty=True) \
        if args.accepted else {}
    w = bundle["winner"]
    run_dir = run_dir_for(project, args.run_id)
    # The combined change, never only the last round's patch: after a repair, that
    # patch is against the committed candidate, not against the host's branch. Built
    # from the stored patches the host read, never the live worktree (index_from_patch).
    gitargs = index_from_patch(project, w, bundle["base"])
    diff = subprocess.run(["git", *gitargs, "diff", "--binary", "--cached", *PATCH_FORMAT,
                           bundle["original_base"]], cwd=w["worktree"],
                          capture_output=True, stdin=subprocess.DEVNULL)
    if diff.returncode != 0:
        raise UsageError("could not diff {} against the original base: {}".format(
            w["worktree"], diff.stderr.decode("utf-8", "replace").strip()))
    combined = os.path.join(run_dir, "combined.patch")
    with open(combined, "wb") as fh:
        fh.write(diff.stdout)
    checked = git(project, *NO_HOOKS, "apply", "--check", combined)
    if checked.returncode != 0:
        raise UsageError("the combined patch does not apply here; nothing applied:\n{}"
                         .format((checked.stderr or checked.stdout).strip()))
    numstat = git(project, *NO_HOOKS, "apply", "--numstat", combined).stdout.strip()
    applied = git(project, *NO_HOOKS, "apply", combined)
    if applied.returncode != 0:
        raise UsageError("git apply failed after its --check passed: {}".format(
            applied.stderr.strip()))
    # Tallies only once the change is in: a refused apply can be retried without
    # counting the reviewers twice.
    record_tallies(project, bundle, accepted)
    rec = record_check(project, bundle, w, project, bundle["family"] + "-accept",
                       bundle["round"])
    print("applied {} from {} (from the original base {}):\n{}".format(
        combined, args.run_id, bundle["original_base"][:12], numstat))
    print("\nspot check, recorded here (recorder exit {}):\n{}\n".format(
        rec["rc"], rec["tail"]))
    cmd_clean(argparse.Namespace(project=project, run_id=bundle["family"], family=True))
    if rec["rc"] == 0:
        return 0
    print("\nthe patch stays applied. Undo: git apply -R {}".format(shlex.quote(combined)))
    if not rec["counted"]:
        print("the check was not recorded (the recorder refused or could not run it); "
              "what to do next is the owner's call")
        return 2
    return 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    here = "project directory (default: the git top level here)"
    flow = ("the workflow this is for: its file's `## Roles` rows replace those roles' "
            "shared rows (a built-in name: the shared table)")
    p = sub.add_parser("roles", help="show the effective roles table")
    p.add_argument("--project", help=here)
    p.add_argument("--json", action="store_true")
    p.add_argument("--workflow", help=flow)
    p = sub.add_parser("workflows", help="list built-in and custom workflows")
    p.add_argument("--project", help=here)
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("run", help="run a role's worker on a brief, n tries, pick one")
    p.add_argument("--role", required=True)
    p.add_argument("--brief", required=True, help="file holding the brief")
    p.add_argument("--project", help=here)
    p.add_argument("--base", default="HEAD", help="commit the tries start from (default HEAD)")
    p.add_argument("--check", help="the step's Done-when command: named to the worker, "
                   "and run (confined) on each try to pick the winner")
    p.add_argument("--rung", type=int, help="ladder rung to run (default: the lowest)")
    p.add_argument("--run-id", help="names the worktrees, branches and run folder "
                   "(default: a timestamp)")
    p.add_argument("--workflow", help=flow)
    p = sub.add_parser("review", help="every reviewer of a role, read-only, on a diff")
    p.add_argument("--role", required=True)
    p.add_argument("--brief", required=True, help="file holding the brief")
    p.add_argument("--diff", required=True, help="file holding the diff to review")
    p.add_argument("--project", help=here)
    p.add_argument("--workdir", help="folder the reviewers read (default: the project); "
                   "for a build-verify candidate, its winner's worktree")
    p.add_argument("--run-id", help="names the run folder (default: a timestamp)")
    p.add_argument("--workflow", help=flow)
    p = sub.add_parser("clean", help="remove a run's worktrees and branches")
    p.add_argument("--run-id", required=True)
    p.add_argument("--family", action="store_true",
                   help="also every run named <run-id>-<anything> (its attempts, repair "
                   "rounds and reviews)")
    p.add_argument("--project", help=here)
    p = sub.add_parser("build-verify", help="one build-verify round: implementer ladder, "
                       "the check run by the recorder, reviewers, bundle.md")
    p.add_argument("--brief", help="file holding the brief (first round)")
    p.add_argument("--check", help="the Done-when command (first round): named to the "
                   "worker, run confined on each try, then run by the recorder")
    p.add_argument("--run-id", help="the family run id (first round); attempts run as "
                   "<id>-k<rung>-a<attempt>, the review as <id>-rev<round>")
    p.add_argument("--project", help=here)
    p.add_argument("--base", help="commit the first round starts from (default HEAD)")
    p.add_argument("--workflow", help=flow + " (default build-verify; a repair round: "
                   "the previous round's)")
    p.add_argument("--step", help="the step text for the record (default: the brief's "
                   "first non-blank line)")
    p.add_argument("--repair-of", metavar="PREV", help="a repair round of PREV, the "
                   "previous round's family run id (<id>, then <id>-r2)")
    p.add_argument("--accepted", metavar="FILE", help="with --repair-of: the accepted "
                   "findings, one per line, each starting with its id (F1, F2: note)")
    p.add_argument("--no-review", action="store_true", help="no reviewers this round")
    p = sub.add_parser("accept", help="apply a build-verify winner from the original "
                       "base, re-run the check here through the recorder, clean")
    p.add_argument("--run-id", required=True, help="the final round's family run id")
    p.add_argument("--accepted", metavar="FILE", help="findings of the final round the "
                   "host accepted (for the reviewers' tallies; default none)")
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
    commands = {"roles": cmd_roles, "workflows": cmd_workflows, "run": cmd_run, "review": cmd_review,
                "clean": cmd_clean, "build-verify": cmd_build_verify, "accept": cmd_accept}
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
