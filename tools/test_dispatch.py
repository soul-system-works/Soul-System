"""Behaviour test for tools/dispatch.py run / review / clean (SOUL-I080).

FENCE: a worker gets the brief and nothing of the host's context. A Claude worker
starts with the isolation the 2026-10-27 probe verified (no setting sources, strict
MCP, every CLAUDE.md in reach excluded, auto-memory off) and with the host's
Anthropic routing removed — a host running on a local model must not send the
worker there by inheritance — while the Ollama route sets it on purpose; a Codex
worker skips user config, rules and AGENTS.md. Every worker gets the allowlisted
environment (none of the host's socket, tokens, keys or git config), and the
selection check that runs a worker's code runs under bubblewrap with that same
environment — skipped for one try and refused for best-of-n where it cannot be
confined (2026-10-27 review). Each try works in its own worktree
on its own branch and is never committed; the patch holds untracked files too;
best-of-n picks a try that exited 0, changed something and passed, with the fewest
changed lines — never an empty or timed-out try, even when the check passes at
base; a hung worker is killed with its whole process group and recorded as
"timeout"; a try that touches the record (findings/ and amendments/ included) is
flagged; dispatch's own git never trusts the worktree's `.git`; tokens come from
modelUsage when Claude reports it; reviewers run read-only and their FINDING lines
(numbered ones too) are parsed; `clean` removes only its own run's worktrees and
branches, `--family` every `<id>-*` run, and reports only what it deleted.
`run`/`review --workflow NAME` use that workflow's `## Roles` rows over the shared
table, and say so in result.json, review.json and the dispatch event; an unknown
name is refused before any worker starts.

Stub `claude` and `codex` executables on a temp PATH record argv, environment, cwd
and stdin, and make the scripted edit. Nothing here touches the real repository.

Run: python3 tools/test_dispatch.py  (exit 0 = PASS)
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

_TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dispatch.py")
_GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
                GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
                GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
CHECK = "grep -qx FIXED app.txt"
FAILS = []

STUB = r'''#!{python}
import json, os, subprocess, sys, time
log = {log!r}  # baked in: a worker gets the allowlisted environment, not the test's
name = os.path.basename(sys.argv[0])
args = sys.argv[1:]
n = len([f for f in os.listdir(log) if f.startswith("call-")])
stdin = sys.stdin.read()
work = args[args.index("-C") + 1] if "-C" in args else os.getcwd()
with open(os.path.join(log, "call-%03d.json" % n), "w") as f:
    json.dump({{"name": name, "argv": args, "env": dict(os.environ), "cwd": os.getcwd(),
               "stdin": stdin}}, f)
plan = json.load(open({plan!r}))
act = plan[min(n, len(plan) - 1)]
for rel, text in act.get("early", {{}}).items():  # written before any sleep
    open(os.path.join(work, rel), "w").write(text)
if act.get("sh"):
    subprocess.run(act["sh"], shell=True, cwd=work)
time.sleep(act.get("sleep", 0))
for rel, text in act.get("write", {{}}).items():
    p = os.path.join(work, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(text)
say = act.get("say", "done")
sys.stderr.write(act.get("stderr", ""))
if name == "claude":
    out = {{"type": "result", "result": say, "usage": {{
        "input_tokens": 100, "cache_read_input_tokens": 20, "output_tokens": 7}}}}
    if act.get("model_usage"):
        out["modelUsage"] = act["model_usage"]
    if act.get("cost") is not None:
        out["total_cost_usd"] = act["cost"]
    print(json.dumps(out))
else:
    open(args[args.index("-o") + 1], "w").write(say)
    print(json.dumps({{"type": "thread.started"}}))
    print(json.dumps({{"type": "turn.completed", "usage": {{
        "input_tokens": 50, "cached_input_tokens": 10, "output_tokens": 3}}}}))
sys.exit(act.get("exit", 0))
'''

# A stand-in for bubblewrap: records its argv and environment, then runs the command
# after its options in the --chdir folder. It confines nothing; the real confinement
# is tools/test_confine.py's real case.
FAKE_BWRAP = r'''#!{python}
import json, os, sys
ARITY = {{"--ro-bind": 2, "--bind": 2, "--dev": 1, "--proc": 1, "--tmpfs": 1,
         "--chdir": 1, "--unshare-net": 0, "--die-with-parent": 0, "--new-session": 0}}
args = sys.argv[1:]
log = {log!r}
n = len(os.listdir(log))
with open(os.path.join(log, "bwrap-%03d.json" % n), "w") as f:
    json.dump({{"argv": args, "env": dict(os.environ)}}, f)
i, chdir = 0, None
while i < len(args) and args[i] in ARITY:
    if args[i] == "--chdir":
        chdir = args[i + 1]
    i += 1 + ARITY[args[i]]
if chdir:
    os.chdir(chdir)
os.execvp(args[i], args[i:])
'''
ALLOWED = {"PATH", "HOME", "USER", "LOGNAME", "LANG", "TERM", "TMPDIR", "SHELL", "OLLAMA_HOST"}
HOST_POWERS = dict(CLAUDE_CODE_MESSAGING_SOCKET="/run/sock", CLAUDE_CODE_MESSAGING_TOKEN="tok",
                   CLAUDE_CODE_SESSION_ID="sid", GH_TOKEN="ghp_x", OPENAI_API_KEY="sk-o",
                   GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="core.pager", GIT_CONFIG_VALUE_0="x",
                   SOUL_GUARD_CWD="/", CODEX_COMPANION_SESSION_ID="c",
                   ANTHROPIC_MODEL="opus", CLAUDE_CODE_USE_BEDROCK="1", LC_ALL="C")


def allowlisted(env, *extra):
    """The variable names in `env` outside the allowlist (LC_* allowed) and `extra`."""
    return sorted(k for k in env if k not in ALLOWED and not k.startswith("LC_")
                  and k not in extra)


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else "  — " + str(detail)[:1500]))
    if not ok:
        FAILS.append(name)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def git(cwd, *args):
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True,
                          env=_GIT_ENV)


class World:
    """A temp HOME, a temp project repo and a stub bin dir, rebuilt per case."""

    def __init__(self, tmp):
        self.tmp = tmp
        self.home = os.path.join(tmp, "home")
        self.proj = os.path.join(tmp, "proj")
        self.bin = os.path.join(tmp, "bin")
        self.log = os.path.join(tmp, "stub-log")
        self.plan = os.path.join(tmp, "stub-plan.json")
        self.brief = os.path.join(tmp, "brief.md")
        self.wrap = os.path.join(tmp, "wrap-bin")
        self.wraplog = os.path.join(tmp, "wrap-log")
        os.makedirs(self.home)
        os.makedirs(self.bin)
        os.makedirs(self.log)
        os.makedirs(self.wraplog)
        stub = STUB.format(python=sys.executable, log=self.log, plan=self.plan)
        for name in ("claude", "codex"):
            write(os.path.join(self.bin, name), stub)
            os.chmod(os.path.join(self.bin, name), 0o755)
        write(os.path.join(self.wrap, "bwrap"),
              FAKE_BWRAP.format(python=sys.executable, log=self.wraplog))
        os.chmod(os.path.join(self.wrap, "bwrap"), 0o755)
        write(os.path.join(tmp, "CLAUDE.md"), "an ancestor's file\n")  # above the project
        for rel, text in {"app.txt": "BUG\n", "CLAUDE.md": "project contract\n",
                          "sub/CLAUDE.md": "nested\n", "witness.md": "# record\n",
                          ".gitignore": ".ai/\n"}.items():
            write(os.path.join(self.proj, rel), text)
        git(self.proj, "init", "-q")
        git(self.proj, "add", "-A")
        git(self.proj, "commit", "-qm", "init")
        self.base = git(self.proj, "rev-parse", "HEAD").stdout.strip()
        write(self.brief, "GOAL-SENTINEL: make app.txt say FIXED.\n")

    def roles(self, *rows):
        write(os.path.join(self.proj, ".claude", "soul-roles.md"),
              "| role | harness | model | settings |\n|---|---|---|---|\n"
              + "".join(r + "\n" for r in rows))

    def script(self, *acts):
        for d in (self.log, self.wraplog):
            shutil.rmtree(d)
            os.makedirs(d)
        write(self.plan, json.dumps(list(acts)))

    def wraps(self):
        return [json.loads(read(os.path.join(self.wraplog, f)))
                for f in sorted(os.listdir(self.wraplog))]

    def calls(self):
        out = []
        for f in sorted(os.listdir(self.log)):
            out.append(json.loads(read(os.path.join(self.log, f))))
        return out

    def env(self, **extra):
        env = {k: v for k, v in _GIT_ENV.items() if not k.startswith("ANTHROPIC_")}
        env.update(HOME=self.home,
                   PATH=os.pathsep.join([self.bin, self.wrap, "/usr/bin", "/bin"]),
                   SOUL_EVENT_LOG=os.path.join(self.tmp, "events.jsonl"))
        env.update(extra)
        return env

    def dispatch(self, *args, env=None, timeout=120):
        return subprocess.run([sys.executable, _TOOL, *args, "--project", self.proj],
                              capture_output=True, text=True, env=env or self.env(),
                              cwd=self.tmp, timeout=timeout)

    def run(self, run_id, *extra, env=None, check=CHECK):
        r = self.dispatch("run", "--role", "implementer", "--brief", self.brief,
                          "--check", check, "--run-id", run_id, *extra, env=env)
        path = os.path.join(self.proj, ".ai", "workflow-runs", run_id, "result.json")
        result = json.loads(read(path)) if os.path.exists(path) else None
        return r, result

    def wt(self, run_id, i):
        return os.path.join(self.proj, ".ai", "worktrees", "{}-{}".format(run_id, i))


def after(argv, flag):
    return argv[argv.index(flag) + 1] if flag in argv else None


def main():
    tmp = tempfile.mkdtemp(prefix="soul-dispatch-test-")
    w = World(tmp)

    # 1 — Anthropic route: isolation flags, clean env, worktree, untracked files, rules
    w.roles("| implementer | claude | sonnet | |")
    w.script({"write": {"app.txt": "FIXED\n", "notes/new.txt": "untracked line\n"},
              "say": "changed app.txt; check passed"})
    host_env = w.env(ANTHROPIC_BASE_URL="http://localhost:11434",
                     ANTHROPIC_AUTH_TOKEN="ollama", ANTHROPIC_API_KEY="sk-host", **HOST_POWERS)
    r, res = w.run("a1", env=host_env)
    calls = w.calls()
    check("run exits 0 with a winner and writes result.json",
          r.returncode == 0 and res and res.get("winner") == 1, r.stdout + r.stderr)
    check("run prints the result it wrote", res is not None and r.stdout.strip()
          and json.loads(r.stdout) == res, r.stdout)
    call = calls[0] if calls else {"argv": [], "env": {}, "cwd": "", "stdin": ""}
    argv = call["argv"]
    wt = w.wt("a1", 1)
    check("claude: -p, json output, acceptEdits, model",
          "-p" in argv and after(argv, "--output-format") == "json"
          and after(argv, "--permission-mode") == "acceptEdits"
          and after(argv, "--model") == "sonnet", argv)
    check("claude: full Bash for the implementer (the sandbox is the boundary); "
          "Write and Edit only inside the worktree",
          after(argv, "--allowedTools") == "Read,Write(./**),Edit(./**),Glob,Grep,Bash", argv)
    sset = json.loads(after(argv, "--settings") or "{}")
    check("claude: sandbox on, fails closed, auto-allow inside it, no unsandboxed escape",
          sset.get("sandbox") == {"enabled": True, "failIfUnavailable": True,
                                  "autoAllowBashIfSandboxed": True,
                                  "allowUnsandboxedCommands": False}, sset)
    deny = sset.get("permissions", {}).get("deny", [])
    check("claude: credential folders unreadable (~/.ssh, ~/.claude, ~/.codex)",
          all("Read(~/{}/**)".format(d) in deny for d in (".ssh", ".claude", ".codex")), deny)
    check("claude: isolation flags as probed (setting sources empty, strict MCP)",
          after(argv, "--setting-sources") == "" and "--strict-mcp-config" in argv, argv)
    try:
        settings = json.loads(after(argv, "--settings"))
    except (TypeError, ValueError):
        settings = {}
    excludes = settings.get("claudeMdExcludes", [])
    want = [os.path.join(w.home, ".claude", "CLAUDE.md"), os.path.join(wt, "CLAUDE.md"),
            os.path.join(wt, "sub", "CLAUDE.md"), os.path.join(w.proj, "CLAUDE.md"),
            os.path.join(tmp, "CLAUDE.md")]
    check("claude: auto-memory off and every CLAUDE.md in reach excluded",
          settings.get("autoMemoryEnabled") is False and all(p in excludes for p in want),
          {"settings": settings, "want": want})
    env = call["env"]
    check("anthropic route drops the host's local routing even when set",
          "ANTHROPIC_BASE_URL" not in env and "ANTHROPIC_AUTH_TOKEN" not in env
          and env.get("ANTHROPIC_API_KEY") == "",
          {k: v for k, v in env.items() if k.startswith("ANTHROPIC")})
    check("anthropic route: the allowlisted environment plus an empty API key only",
          not allowlisted(env, "ANTHROPIC_API_KEY") and env.get("HOME") == w.home
          and env.get("LC_ALL") == "C", allowlisted(env, "ANTHROPIC_API_KEY"))
    wraps = w.wraps()
    bw = wraps[0] if wraps else {"argv": [], "env": {}}
    rwt = os.path.realpath(wt)
    check("selection check runs under bubblewrap: worktree bound, no network, then the check",
          len(wraps) == 1 and bw["argv"][-3:] == ["/bin/sh", "-c", CHECK]
          and after(bw["argv"], "--bind") == rwt and after(bw["argv"], "--chdir") == rwt
          and "--unshare-net" in bw["argv"] and after(bw["argv"], "--ro-bind") == "/",
          bw["argv"])
    check("selection check gets the allowlisted environment, not the host's",
          bw["env"] and not allowlisted(bw["env"]) and "GH_TOKEN" not in bw["env"],
          allowlisted(bw["env"]))
    check("worker runs in its own worktree on its own branch",
          os.path.realpath(call["cwd"]) == os.path.realpath(wt)
          and git(w.proj, "branch", "--list", "soul-wf/a1-1").stdout.strip() != ""
          and git(wt, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip() == "soul-wf/a1-1",
          call["cwd"])
    check("the brief reaches the worker with the worker rules appended",
          call["stdin"].startswith("GOAL-SENTINEL") and "witness.md" in call["stdin"]
          and ".soul/" in call["stdin"] and CHECK in call["stdin"]
          and "did not run" in call["stdin"], call["stdin"])
    t = (res or {}).get("tries", [{}])[0]
    patch = read(t["patch"]) if t.get("patch") and os.path.exists(t["patch"]) else ""
    check("patch holds the tracked change and the untracked file",
          "app.txt" in patch and "notes/new.txt" in patch and "+FIXED" in patch, patch)
    check("try fields: exit, wall, tokens, changed lines, check, record flag",
          t.get("exit") == 0 and isinstance(t.get("wall_s"), (int, float))
          and t.get("tokens_in") == 120 and t.get("tokens_out") == 7
          and t.get("changed_lines") == 3 and t.get("check_rc") == 0
          and t.get("record_touched") is False
          and os.path.realpath(t.get("worktree", "")) == os.path.realpath(wt)
          and t.get("branch") == "soul-wf/a1-1", t)
    check("result header: run id, role, harness, model, rung",
          res and (res["run_id"], res["role"], res["harness"], res["model"], res["rung"])
          == ("a1", "implementer", "claude", "sonnet", 1), res)
    check("nothing committed in the worktree; the project is untouched",
          git(wt, "rev-parse", "HEAD").stdout.strip() == w.base
          and git(w.proj, "rev-parse", "HEAD").stdout.strip() == w.base
          and read(os.path.join(w.proj, "app.txt")) == "BUG\n")

    # 2 — Ollama route sets the routing; --rung picks the ladder row
    w.roles("| implementer | claude | sonnet | |",
            "| implementer | claude-ollama | qwen3.8:27b-q8_0 | |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    r, res = w.run("o1", "--rung", "2", env=w.env(**HOST_POWERS))
    call = (w.calls() or [{"argv": [], "env": {}}])[0]
    env = call["env"]
    check("ollama route: the allowlisted environment plus its three values only",
          env and not allowlisted(env, "ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN",
                                  "ANTHROPIC_API_KEY"),
          allowlisted(env, "ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY"))
    check("ollama route sets base URL, token and an empty API key",
          env.get("ANTHROPIC_BASE_URL") == "http://localhost:11434"
          and env.get("ANTHROPIC_AUTH_TOKEN") == "ollama"
          and env.get("ANTHROPIC_API_KEY") == "",
          {k: v for k, v in env.items() if k.startswith("ANTHROPIC")})
    check("--rung 2 runs the second row with its exact model",
          r.returncode == 0 and res and res["harness"] == "claude-ollama" and res["rung"] == 2
          and after(call["argv"], "--model") == "qwen3.8:27b-q8_0"
          and "--strict-mcp-config" in call["argv"], r.stderr + str(call["argv"]))
    r, _ = w.run("o2", "--rung", "5")
    check("a rung the role does not have is a usage error",
          r.returncode == 2 and "rung" in r.stderr, r.stderr)

    # 3 — codex flags, default model and the Ollama variant
    w.roles("| implementer | codex | default | |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    r, res = w.run("c1", env=w.env(**HOST_POWERS))
    call = (w.calls() or [{"argv": [], "env": {}}])[0]
    argv = call["argv"]
    wt = w.wt("c1", 1)
    check("codex: the allowlisted environment, nothing added",
          call["env"] and not allowlisted(call["env"]), allowlisted(call["env"]))
    check("codex exec: isolation flags as probed",
          argv[:1] == ["exec"] and "--ephemeral" in argv and "--ignore-user-config" in argv
          and "--ignore-rules" in argv and after(argv, "-c") == "project_doc_max_bytes=0",
          argv)
    check("codex exec: worktree, workspace-write, json, last message file, no model",
          after(argv, "-C") == wt and after(argv, "-s") == "workspace-write"
          and "--json" in argv and after(argv, "-o") and "-m" not in argv
          and "--oss" not in argv, argv)
    t = (res or {}).get("tries", [{}])[0]
    check("codex tokens read from turn.completed; check passed",
          r.returncode == 0 and t.get("tokens_in") == 50 and t.get("tokens_out") == 3
          and t.get("check_rc") == 0, r.stderr + str(t))
    w.roles("| implementer | codex-ollama | qwen3.8:27b-q8_0 | |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    r, res = w.run("c2")
    argv = (w.calls() or [{"argv": []}])[0]["argv"]
    check("codex-ollama adds --oss --local-provider ollama -m <model>",
          "--oss" in argv and after(argv, "--local-provider") == "ollama"
          and after(argv, "-m") == "qwen3.8:27b-q8_0" and "--ignore-user-config" in argv,
          argv)

    # 4 — best-of-n: passing first, then fewest changed lines
    w.roles("| implementer | claude | sonnet | n=3 |")
    w.script({"write": {"app.txt": "FIXED\n", "extra.txt": "a\nb\nc\n"}},
             {"write": {"app.txt": "WRONG\n"}},
             {"write": {"app.txt": "FIXED\n"}})
    r, res = w.run("b1")
    tries = (res or {}).get("tries", [])
    check("best-of-n: three tries, each its own worktree",
          len(tries) == 3 and len({x["worktree"] for x in tries}) == 3
          and all(os.path.isdir(w.wt("b1", i)) for i in (1, 2, 3)), tries)
    check("best-of-n: changed lines and check per try",
          [x.get("changed_lines") for x in tries] == [5, 2, 2]
          and [x.get("check_rc") == 0 for x in tries] == [True, False, True], tries)
    check("best-of-n: winner is the passing try with the fewest changed lines",
          res and res.get("winner") == 3, res and res.get("winner"))

    # 5 — a harness that exits 0 and changes nothing
    w.roles("| implementer | claude | sonnet | |")
    w.script({"say": "all done!"})
    r, res = w.run("z1")
    t = (res or {}).get("tries", [{}])[0]
    check("exit 0 with no change: empty patch, check fails, no winner, exit 1",
          r.returncode == 1 and res and res["winner"] is None and t.get("exit") == 0
          and t.get("changed_lines") == 0 and t.get("check_rc") not in (0, None)
          and read(t["patch"]) == "", r.stdout + r.stderr)

    # 6 — timeout kills the worker's process group
    w.roles("| implementer | claude | sonnet | timeout=1 |")
    w.script({"sleep": 3, "write": {"late.txt": "outlived the timeout\n"}})
    t0 = time.time()
    r, res = w.run("t1")
    took = time.time() - t0
    t = (res or {}).get("tries", [{}])[0]
    time.sleep(3.5)
    check("timeout: exit recorded as \"timeout\", no winner",
          res and t.get("exit") == "timeout" and res["winner"] is None and took < 15,
          "took {:.1f}s; {}".format(took, r.stdout + r.stderr))
    check("timeout: the worker was killed, not left running",
          not os.path.exists(os.path.join(w.wt("t1", 1), "late.txt")))

    # 7 — a try that touches the record is flagged
    w.roles("| implementer | claude | sonnet | n=3 |")
    w.script({"write": {"app.txt": "FIXED\n", "witness.md": "# record\nforged\n"}},
             {"write": {"app.txt": "FIXED\n", ".soul/handoff.md": "cursor\n"}},
             {"write": {"app.txt": "FIXED\n", "docs/witness.md.txt": "fine\n"}})
    r, res = w.run("w1")
    tries = (res or {}).get("tries", [])
    check("record_touched: witness.md and .soul/ flagged, other files not",
          [x.get("record_touched") for x in tries] == [True, True, False], tries)
    check("record_touched: a try that touched the record never wins",
          (res or {}).get("winner") == 3, res)

    # 7a — Soul System's own record: findings/ and amendments/ count too
    w.script({"write": {"app.txt": "FIXED\n", "findings/F999.md": "forged\n"}},
             {"write": {"app.txt": "FIXED\n", "amendments/A999.md": "forged\n"}},
             {"write": {"app.txt": "FIXED\n", "docs/findings.txt": "fine\n"}})
    r, res = w.run("w2")
    tries = (res or {}).get("tries", [])
    stdin = (w.calls() or [{"stdin": ""}])[0]["stdin"]
    check("record_touched: findings/ and amendments/ flagged, docs/findings.txt not",
          [x.get("record_touched") for x in tries] == [True, True, False]
          and (res or {}).get("winner") == 3, tries)
    check("worker rules name findings/ and amendments/",
          "findings/" in stdin and "amendments/" in stdin, stdin)

    # 7a2 — no empty or timed-out winner, even when the check already passes at base
    w.roles("| implementer | claude | sonnet | |")
    w.script({"say": "nothing to do"})
    r, res = w.run("e1", check="true")
    check("check passes at base, try changed nothing: no winner, exit 1",
          r.returncode == 1 and res and res["winner"] is None
          and res["tries"][0]["check_rc"] == 0, (r.returncode, res and res["winner"]))
    w.roles("| implementer | claude | sonnet | timeout=1 |")
    w.script({"early": {"app.txt": "FIXED\n"}, "sleep": 5})
    r, res = w.run("e2", check="true")
    t = ((res or {}).get("tries") or [{}])[0]
    check("a timed-out try with a change and a passing check never wins",
          t.get("exit") == "timeout" and t.get("changed_lines", 0) > 0
          and res["winner"] is None, t)
    w.roles("| implementer | claude | sonnet | n=2 |")
    w.script({"write": {"app.txt": "FIXED\n"}}, {"say": "nothing to do"})
    r, res = w.run("e3", check="true")
    check("n=2, a real change and an empty try: the real change wins",
          res and res["winner"] == 1, res and [(x["changed_lines"], x["check_rc"])
                                               for x in res["tries"]])
    w.roles("| implementer | claude | sonnet | n=2 |")
    w.script({"write": {"app.txt": "FIXED\n"}, "exit": 3}, {"write": {"app.txt": "FIXED\n",
                                                                     "b.txt": "b\n"}})
    r, res = w.run("e4")
    check("a try that exited non-zero never wins, even with fewer lines and a pass",
          res and res["winner"] == 2, res and [(x["exit"], x["changed_lines"], x["check_rc"])
                                               for x in res["tries"]])

    # 7a3 — tokens: modelUsage summed across models when Claude reports it
    w.roles("| implementer | claude | sonnet | |")
    w.script({"write": {"app.txt": "FIXED\n"}, "model_usage": {
        "claude-sonnet": {"inputTokens": 10, "outputTokens": 500, "cacheReadInputTokens": 1000,
                          "cacheCreationInputTokens": 30},
        "claude-haiku": {"inputTokens": 5, "outputTokens": 26000,
                         "cacheReadInputTokens": 0, "cacheCreationInputTokens": 0}}})
    r, res = w.run("tk1")
    t = ((res or {}).get("tries") or [{}])[0]
    check("tokens from modelUsage across models (input + cache read + creation; output)",
          t.get("tokens_in") == 1045 and t.get("tokens_out") == 26500, t)

    # 7b — Claude Code reports the sandbox off: that try never wins
    w.roles("| implementer | claude | sonnet | |")
    w.script({"write": {"app.txt": "FIXED\n"},
              "stderr": "Sandbox disabled: sandbox is enabled but dependencies are missing\n"})
    r, res = w.run("sb1")
    t1 = ((res or {}).get("tries") or [{}])[0]
    check("sandbox reported off: try flagged, no winner, exit 1",
          t1.get("sandbox_inactive") is True and res.get("winner") is None
          and r.returncode == 1, (r.returncode, res))

    # 7c — no socat on PATH: a Claude worker is refused before anything starts
    gitonly = os.path.join(w.tmp, "gitonly")
    os.makedirs(gitonly, exist_ok=True)
    if not os.path.exists(os.path.join(gitonly, "git")):
        os.symlink(shutil.which("git"), os.path.join(gitonly, "git"))
    env = w.env(PATH=os.pathsep.join([w.bin, gitonly]))
    w.script({"write": {"app.txt": "FIXED\n"}})
    r, res = w.run("sb2", env=env)
    check("no bubblewrap/socat: refused with exit 2 naming them, no worker started",
          r.returncode == 2 and "socat" in r.stderr and not w.calls()
          and not os.path.exists(w.wt("sb2", 1)), (r.returncode, r.stderr))

    # 7c2 — dispatch's own git never trusts the worktree's .git: a worker that swaps it
    # for a repo of its own with a core.fsmonitor hook must not get that hook run by
    # dispatch, unconfined, on the host (the 2026-10-27 review)
    w.roles("| implementer | claude | sonnet | |")
    pwned = os.path.join(tmp, "PWNED")
    w.script({"write": {"app.txt": "FIXED\n"},
              "sh": "rm .git && git init -q . && git config core.fsmonitor "
                    "'touch {}; false'".format(pwned)})
    r, res = w.run("g1")
    t = ((res or {}).get("tries") or [{}])[0]
    patch = read(t["patch"]) if t.get("patch") and os.path.exists(t["patch"]) else ""
    check("a worker's own .git hook never runs in dispatch's git calls",
          not os.path.exists(pwned), "sentinel written by the worker's fsmonitor hook")
    check("the patch is still taken against the real base through the project's git",
          "+FIXED" in patch and t.get("changed_lines") == 2 and res.get("winner") == 1,
          (t, patch[:300]))

    # 7d — no bubblewrap: one try skips the selection check (the host's confined
    # re-run is the gate); best-of-n, which needs the check, is refused at start
    nobw = [d for d in (w.bin, gitonly) if os.path.exists(os.path.join(d, "bwrap"))]
    w.roles("| implementer | codex | default | |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    r, res = w.run("nb1", env=w.env(PATH=os.pathsep.join([w.bin, gitonly])))
    t = ((res or {}).get("tries") or [{}])[0]
    check("no bwrap, n=1: the check is skipped, not run bare; the try still wins",
          not nobw and r.returncode == 0 and t.get("check_rc") is None
          and res.get("winner") == 1 and not w.wraps()
          and not os.path.exists(os.path.join(w.proj, ".ai", "workflow-runs", "nb1",
                                              "try-1.check.log")),
          (nobw, r.returncode, r.stderr, t))
    w.roles("| implementer | codex | default | n=2 |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    r, res = w.run("nb2", env=w.env(PATH=os.pathsep.join([w.bin, gitonly])))
    check("no bwrap, n=2: refused with exit 2 naming bubblewrap, no worker started",
          r.returncode == 2 and "bubblewrap" in r.stderr and not w.calls()
          and not os.path.exists(w.wt("nb2", 1)), (r.returncode, r.stderr))

    # 8 — clean removes only its own run's worktrees and branches
    w.roles("| implementer | claude | sonnet | |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    w.run("r1")
    w.run("r10")
    r = w.dispatch("clean", "--run-id", "r1")
    branches = git(w.proj, "branch", "--list", "soul-wf/*").stdout
    listing = git(w.proj, "worktree", "list").stdout
    check("clean removes the run's worktree and branch",
          r.returncode == 0 and not os.path.exists(w.wt("r1", 1))
          and "soul-wf/r1-1" not in branches and w.wt("r1", 1) not in listing,
          r.stdout + r.stderr + branches)
    check("clean leaves a run whose id merely starts the same",
          os.path.isdir(w.wt("r10", 1)) and "soul-wf/r10-1" in branches, branches)
    check("clean keeps the run's evidence (result.json, patches)",
          os.path.exists(os.path.join(w.proj, ".ai", "workflow-runs", "r1", "result.json")))

    # 8a — clean --family: every run named <id>-<anything>, and only those
    w.run("r1-k1-a1")
    w.run("r1-r2")
    w.run("r10-k1-a1")
    r = w.dispatch("clean", "--run-id", "r1")
    check("clean without --family leaves <id>-k1-a1 and <id>-r2 runs alone",
          os.path.isdir(w.wt("r1-k1-a1", 1)) and os.path.isdir(w.wt("r1-r2", 1)),
          r.stdout + r.stderr)
    r = w.dispatch("clean", "--run-id", "r1", "--family")
    branches = git(w.proj, "branch", "--list", "soul-wf/*").stdout
    check("clean --family removes every r1-* worktree and branch",
          r.returncode == 0 and not os.path.exists(w.wt("r1-k1-a1", 1))
          and not os.path.exists(w.wt("r1-r2", 1)) and "soul-wf/r1-k1-a1-1" not in branches
          and "soul-wf/r1-r2-1" not in branches
          and "removed 2 worktree(s) and 2 branch(es)" in r.stdout,
          r.stdout + r.stderr + branches)
    check("clean --family r1 never touches r10-*",
          os.path.isdir(w.wt("r10", 1)) and os.path.isdir(w.wt("r10-k1-a1", 1))
          and "soul-wf/r10-1" in branches and "soul-wf/r10-k1-a1-1" in branches, branches)
    # a locked worktree stays, and so does its branch: report what was deleted
    w.run("lk1")
    git(w.proj, "worktree", "lock", w.wt("lk1", 1))
    r = w.dispatch("clean", "--run-id", "lk1")
    branches = git(w.proj, "branch", "--list", "soul-wf/*").stdout
    check("clean counts the branches it deleted, not those it tried",
          "soul-wf/lk1-1" in branches and "0 branch(es)" in r.stdout,
          r.stdout + r.stderr + branches)
    git(w.proj, "worktree", "unlock", w.wt("lk1", 1))

    # 8b — a project that does not ignore .ai/: dispatch keeps the tries out of git
    exclude = os.path.join(w.proj, ".git", "info", "exclude")
    check("a project that already ignores .ai/ gets no exclude line",
          ".ai/" not in (read(exclude) if os.path.exists(exclude) else ""))
    git(w.proj, "rm", "-q", "--cached", ".gitignore")
    os.remove(os.path.join(w.proj, ".gitignore"))
    git(w.proj, "commit", "-qm", "no ignore")
    w.script({"write": {"app.txt": "FIXED\n"}})
    w.run("x1")
    status = git(w.proj, "status", "--porcelain").stdout
    check("without an ignore rule: .ai/ goes to .git/info/exclude, git status stays clean",
          ".ai/" in read(exclude) and ".ai" not in status, status)

    # 9 — review: every reviewer, read-only, FINDING lines parsed
    w.roles("| reviewer | claude | opus | |", "| reviewer | codex | default | |")
    diff = os.path.join(tmp, "change.diff")
    write(diff, "DIFF-SENTINEL\n--- a/app.txt\n+++ b/app.txt\n@@\n-BUG\n+FIXED\n")
    w.script({"say": "Read it.\nFINDING: app.txt:1 — wrong word — FIXED is not tested\n"
                     "- **FINDING:** app.txt:2 — second — scenario two\n"
                     "1. FINDING: app.txt:3 — numbered — scenario three\n"
                     "2) **FINDING:** app.txt:4 — numbered too — scenario four\n"},
             {"say": "NO FINDINGS"})
    r = w.dispatch("review", "--role", "reviewer", "--brief", w.brief, "--diff", diff,
                   "--run-id", "v1")
    path = os.path.join(w.proj, ".ai", "workflow-runs", "v1", "review.json")
    res = json.loads(read(path)) if os.path.exists(path) else {}
    calls = w.calls()
    check("review runs every reviewer once", r.returncode == 0 and len(calls) == 2
          and [c["name"] for c in calls] == ["claude", "codex"], r.stdout + r.stderr)
    c0 = calls[0] if calls else {"argv": [], "cwd": "", "stdin": ""}
    c1 = calls[1] if len(calls) > 1 else {"argv": [], "cwd": ""}
    check("review claude: plan mode, read tools only, isolated, in the project",
          after(c0["argv"], "--permission-mode") == "plan"
          and after(c0["argv"], "--allowedTools") == "Read,Glob,Grep"
          and after(c0["argv"], "--model") == "opus"
          and after(c0["argv"], "--setting-sources") == "" and "--strict-mcp-config" in c0["argv"]
          and os.path.realpath(c0["cwd"]) == os.path.realpath(w.proj), c0["argv"])
    check("review prompt: brief, diff and the findings-only instruction",
          "GOAL-SENTINEL" in c0["stdin"] and "DIFF-SENTINEL" in c0["stdin"]
          and "FINDING: <file:line>" in c0["stdin"] and "NO FINDINGS" in c0["stdin"]
          and "never edit" in c0["stdin"], c0["stdin"])
    check("review codex: read-only sandbox, isolated, in the project",
          after(c1["argv"], "-s") == "read-only" and after(c1["argv"], "-C") == w.proj
          and "--ignore-user-config" in c1["argv"] and "--ignore-rules" in c1["argv"]
          and after(c1["argv"], "-c") == "project_doc_max_bytes=0", c1["argv"])
    revs = res.get("reviewers", [{}, {}])
    check("findings parsed per reviewer; NO FINDINGS is none",
          len(revs) == 2 and revs[0].get("findings") == [
              "app.txt:1 — wrong word — FIXED is not tested",
              "app.txt:2 — second — scenario two",
              "app.txt:3 — numbered — scenario three",
              "app.txt:4 — numbered too — scenario four"]
          and revs[0].get("verdict") == "findings"
          and revs[1].get("findings") == [] and revs[1].get("verdict") == "none", revs)
    check("review keeps each reviewer's raw text, exit, wall and tokens",
          len(revs) == 2 and all(os.path.exists(x.get("raw", "")) for x in revs)
          and revs[0].get("exit") == 0 and revs[0].get("tokens_in") == 120
          and isinstance(revs[1].get("wall_s"), (int, float))
          and (revs[0].get("harness"), revs[0].get("model")) == ("claude", "opus"), revs)
    check("review changes nothing in the project",
          git(w.proj, "status", "--porcelain").stdout.strip() == "?? .claude/"
          and read(os.path.join(w.proj, "app.txt")) == "BUG\n",
          git(w.proj, "status", "--porcelain").stdout)

    # 9a — every run and every reviewer leaves one dispatch event, won or not
    log = os.path.join(tmp, "events.jsonl")
    evs = [json.loads(l) for l in (read(log) if os.path.exists(log) else "").splitlines()]
    disp = [e["data"] for e in evs if e.get("type") == "soul.workflow.dispatch"]
    runs = {d["run_id"]: d for d in disp if d["mode"] == "run"}
    check("dispatch event per run: role, worker, rung, tries, won, time",
          runs.get("a1", {}).get("won") is True and runs["a1"].get("harness") == "claude"
          and runs["a1"].get("tries") == 1 and isinstance(runs["a1"].get("wall_s"), float),
          runs.get("a1"))
    check("a run with no winner, and a timeout, are logged too",
          runs.get("z1", {}).get("won") is False and runs.get("t1", {}).get("timeouts") == 1,
          (runs.get("z1"), runs.get("t1")))
    check("a review logs one dispatch event per reviewer",
          len([d for d in disp if d["mode"] == "review" and d["run_id"] == "v1"]) == 2, disp[-3:])

    # 9b — --workdir: a candidate's reviewers read the candidate's worktree
    cand = w.wt("r10", 1)
    w.script({"say": "NO FINDINGS"}, {"say": "NO FINDINGS"})
    r = w.dispatch("review", "--role", "reviewer", "--brief", w.brief, "--diff", diff,
                   "--run-id", "v2", "--workdir", cand)
    calls = w.calls()
    check("review --workdir: both reviewers read that folder, not the project",
          r.returncode == 0 and len(calls) == 2
          and os.path.realpath(calls[0]["cwd"]) == os.path.realpath(cand)
          and os.path.realpath(after(calls[1]["argv"], "-C")) == os.path.realpath(cand),
          [(c["cwd"], after(c["argv"], "-C")) for c in calls] or r.stderr)
    r = w.dispatch("review", "--role", "reviewer", "--brief", w.brief, "--diff", diff,
                   "--run-id", "v3", "--workdir", os.path.join(tmp, "nope"))
    check("review --workdir that is not a folder: usage error", r.returncode == 2, r.stderr)

    # 9c — the reviewer's sandbox fails closed too
    w.script({"say": "NO FINDINGS",
              "stderr": "Sandbox disabled: sandbox is enabled but dependencies are missing\n"},
             {"say": "NO FINDINGS"})
    r = w.dispatch("review", "--role", "reviewer", "--brief", w.brief, "--diff", diff,
                   "--run-id", "v4")
    calls = w.calls()
    rset = json.loads(after(calls[0]["argv"], "--settings") or "{}") if calls else {}
    check("review claude: sandbox settings fail closed",
          rset.get("sandbox", {}).get("failIfUnavailable") is True, rset)
    path = os.path.join(w.proj, ".ai", "workflow-runs", "v4", "review.json")
    revs = (json.loads(read(path)) if os.path.exists(path) else {}).get("reviewers", [{}, {}])
    check("review: a reviewer that says Sandbox disabled is flagged unconfined",
          revs[0].get("sandbox_inactive") is True and revs[0].get("verdict") == "unconfined"
          and revs[1].get("sandbox_inactive") is False and revs[1].get("verdict") == "none",
          revs)
    w.script({"say": "NO FINDINGS"})
    r = w.dispatch("review", "--role", "reviewer", "--brief", w.brief, "--diff", diff,
                   "--run-id", "v5", env=w.env(PATH=os.pathsep.join([w.bin, gitonly])))
    check("review: no bubblewrap/socat with a Claude reviewer is refused, none started",
          r.returncode == 2 and "socat" in r.stderr and not w.calls(), (r.returncode, r.stderr))

    # 10 — --workflow: the workflow file's ## Roles rows win over the shared table
    w.roles("| implementer | claude | sonnet | |", "| reviewer | claude | opus | |",
            "| reviewer | codex | default | |")
    write(os.path.join(w.proj, ".claude", "soul-workflows", "quick-fix.md"),
          "---\nname: quick-fix\ndescription: d\n---\n\n1. Step.\n\n## Roles\n\n"
          "| role | harness | model | settings |\n|---|---|---|---|\n"
          "| implementer | claude | opus | |\n| reviewer | codex | default | |\n")
    w.script({"write": {"app.txt": "FIXED\n"}})
    r, res = w.run("wf1", "--workflow", "quick-fix")
    argv = (w.calls() or [{"argv": []}])[0]["argv"]
    check("run --workflow: the workflow's implementer row runs, not the shared one",
          r.returncode == 0 and after(argv, "--model") == "opus"
          and (res or {}).get("model") == "opus", (r.returncode, r.stderr, argv))
    check("run --workflow: result.json names the workflow",
          (res or {}).get("workflow") == "quick-fix", res)
    a1 = json.loads(read(os.path.join(w.proj, ".ai", "workflow-runs", "a1", "result.json")))
    check("run without --workflow: result.json has no workflow field", "workflow" not in a1,
          a1.keys())
    w.script({"write": {"app.txt": "FIXED\n"}})
    r, res = w.run("wf2", "--workflow", "build-verify")
    argv = (w.calls() or [{"argv": []}])[0]["argv"]
    check("run --workflow build-verify: the shared table, the workflow named",
          r.returncode == 0 and after(argv, "--model") == "sonnet"
          and (res or {}).get("workflow") == "build-verify", (r.stderr, argv, res))
    w.script({"write": {"app.txt": "FIXED\n"}})
    r, res = w.run("wf3", "--workflow", "no-such-flow")
    check("run --workflow with an unknown name: exit 2, no worker, no worktree",
          r.returncode == 2 and "no workflow named 'no-such-flow'" in r.stderr
          and not w.calls() and not os.path.exists(w.wt("wf3", 1)) and res is None,
          (r.returncode, r.stderr))
    w.script({"say": "NO FINDINGS"})
    r = w.dispatch("review", "--role", "reviewer", "--brief", w.brief, "--diff", diff,
                   "--run-id", "wfv1", "--workflow", "quick-fix")
    calls = w.calls()
    path = os.path.join(w.proj, ".ai", "workflow-runs", "wfv1", "review.json")
    rv = json.loads(read(path)) if os.path.exists(path) else {}
    check("review --workflow: only the workflow's reviewer runs",
          r.returncode == 0 and [c["name"] for c in calls] == ["codex"]
          and [x["harness"] for x in rv.get("reviewers", [])] == ["codex"],
          (r.stderr, [c["name"] for c in calls]))
    check("review --workflow: review.json names the workflow", rv.get("workflow") == "quick-fix",
          rv)
    evs = [json.loads(l) for l in (read(log) if os.path.exists(log) else "").splitlines()]
    disp = [e["data"] for e in evs if e.get("type") == "soul.workflow.dispatch"]
    by = {(d["mode"], d["run_id"]): d for d in disp}
    check("dispatch events carry the workflow when it was given, and only then",
          by.get(("run", "wf1"), {}).get("workflow") == "quick-fix"
          and by.get(("run", "wf2"), {}).get("workflow") == "build-verify"
          and by.get(("review", "wfv1"), {}).get("workflow") == "quick-fix"
          and "workflow" not in by.get(("run", "a1"), {"workflow": 1})
          and "workflow" not in by.get(("review", "v1"), {"workflow": 1}),
          [(k, d.get("workflow")) for k, d in by.items()])

    effort_cases(w)
    build_verify_cases(w, gitonly)
    review_fix_cases()

    shutil.rmtree(tmp, ignore_errors=True)
    docs()
    print("\n{} failure(s)".format(len(FAILS)) if FAILS else "\nALL PASS")
    return 1 if FAILS else 0


def pairs(argv):
    return list(zip(argv, argv[1:]))


def events(w, kind):
    log = os.path.join(w.tmp, "events.jsonl")
    evs = [json.loads(l) for l in (read(log) if os.path.exists(log) else "").splitlines()]
    return [e["data"] for e in evs if e.get("type") == kind]


def effort_cases(w):
    """11 — `effort=`: a word per harness, passed as that harness's own flag."""
    w.roles("| implementer | claude | sonnet | effort=high |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    r, res = w.run("ef1")
    argv = (w.calls() or [{"argv": []}])[0]["argv"]
    check("effort: a claude row passes --effort <level>",
          r.returncode == 0 and ("--effort", "high") in pairs(argv), (r.stderr, argv))
    check("effort: result.json carries it, header and try",
          res and res.get("effort") == "high" and res["tries"][0].get("effort") == "high", res)
    run_ev = [d for d in events(w, "soul.workflow.dispatch") if d["run_id"] == "ef1"]
    check("effort: the dispatch event carries it when set",
          run_ev and run_ev[0].get("effort") == "high", run_ev)
    w.roles("| implementer | codex | default | effort=minimal |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    r, res = w.run("ef2")
    argv = (w.calls() or [{"argv": []}])[0]["argv"]
    check("effort: a codex row passes -c model_reasoning_effort=<level>",
          r.returncode == 0 and ("-c", "model_reasoning_effort=minimal") in pairs(argv)
          and ("-c", "project_doc_max_bytes=0") in pairs(argv), (r.stderr, argv))
    w.roles("| implementer | claude | sonnet | |", "| reviewer | codex | default | |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    r, res = w.run("ef3")
    argv = (w.calls() or [{"argv": []}])[0]["argv"]
    w.script({"say": "NO FINDINGS"})
    diff = os.path.join(w.tmp, "change.diff")
    w.dispatch("review", "--role", "reviewer", "--brief", w.brief, "--diff", diff,
               "--run-id", "ef4")
    cargv = (w.calls() or [{"argv": []}])[0]["argv"]
    run_ev = [d for d in events(w, "soul.workflow.dispatch") if d["run_id"] in ("ef3", "ef4")]
    check("effort unset: no --effort, no model_reasoning_effort, no event field",
          "--effort" not in argv and not any("model_reasoning_effort" in a for a in cargv)
          and res and res.get("effort") is None and len(run_ev) == 2
          and all("effort" not in d for d in run_ev), (argv, cargv, run_ev))
    roles_file = os.path.join(w.proj, ".claude", "soul-roles.md")
    for row, levels in (("| implementer | claude | sonnet | effort=minimal |",
                         "low, medium, high, xhigh, max"),
                        ("| implementer | codex | default | effort=max |",
                         "minimal, low, medium, high, xhigh")):
        w.roles(row)
        r = w.dispatch("roles")
        check("effort: an invalid level is a row error naming file:line and the levels "
              "({})".format(row.split("|")[2].strip()),
              r.returncode == 2 and roles_file + ":3:" in r.stderr and levels in r.stderr,
              r.stderr)
    w.roles("| implementer | claude-ollama | qwen3.8:27b-q8_0 | effort=low rung=1 |",
            "| reviewer | codex-ollama | qwen3.8:27b-q8_0 | effort=xhigh |")
    r = w.dispatch("roles", "--json")
    rows = json.loads(r.stdout or "[]")
    text = w.dispatch("roles").stdout
    check("effort: roles --json and the text view carry it ('-' when unset)",
          [x.get("effort") for x in rows] == ["low", "xhigh"]
          and "effort" in text.splitlines()[0], (rows, text))


def build_verify_cases(w, gitonly):
    """12–15 — build-verify: one call per round; repair; accept."""
    runs = os.path.join(w.proj, ".ai", "workflow-runs")
    head = git(w.proj, "rev-parse", "HEAD").stdout.strip()  # 8b committed after head

    def bundle(run_id):
        path = os.path.join(runs, run_id, "bundle.json")
        return json.loads(read(path)) if os.path.exists(path) else {}

    # 12 — the ladder: rung 1 fails twice, rung 2 wins; the recorder runs the check;
    # the reviewers read the winner's worktree; bundle.md has what the host needs
    w.roles("| implementer | claude | sonnet | |", "| implementer | claude | opus | effort=max |",
            "| reviewer | claude | opus | |", "| reviewer | codex | default | |")
    w.script({"write": {"app.txt": "WRONG\n"}}, {"write": {"app.txt": "WRONG\n"}},
             {"write": {"app.txt": "FIXED\n"}, "cost": 0.25},
             {"say": "FINDING: app.txt:1 — first — scenario one\n", "cost": 0.5},
             {"say": "FINDING: app.txt:1 — second — scenario two\n"})
    r = w.dispatch("build-verify", "--brief", w.brief, "--check", CHECK, "--run-id", "bv")
    calls = w.calls()
    b = bundle("bv")
    win = b.get("winner") or {}
    check("build-verify: rung 1's two attempts fail, rung 2 wins, exit 0",
          r.returncode == 0 and b.get("status") == "winner" and win.get("rung") == 2
          and win.get("run_id") == "bv-k2-a1"
          and [a["run_id"] for a in b.get("attempts", [])] == ["bv-k1-a1", "bv-k1-a2", "bv-k2-a1"],
          (r.returncode, r.stderr, b.get("status"), win))
    stdins = [c["stdin"] for c in calls]
    check("build-verify: attempt 2's brief carries the failure section; a new rung starts clean",
          len(stdins) >= 3 and "## The previous attempt failed" not in stdins[0]
          and "## The previous attempt failed" in stdins[1]
          and "try 1: exit 0, 2 changed line(s), check exit 1" in stdins[1]
          and "## The previous attempt failed" not in stdins[2]
          and stdins[1].startswith("GOAL-SENTINEL"), stdins[1:2])
    check("build-verify: rung 2 runs its row, effort included",
          len(calls) >= 3 and after(calls[2]["argv"], "--model") == "opus"
          and ("--effort", "max") in pairs(calls[2]["argv"]), calls[2:3] and calls[2]["argv"])
    rec = [d for d in events(w, "soul.delegation.checked") if d.get("run_id") == "bv-k2-a1"]
    d = rec[0] if rec else {}
    check("build-verify: the recorder recorded the winner's check, with every field",
          len(rec) == 1 and d["check"]["passed"] is True and d["check"]["observed"] is True
          and d["check"]["command"] == CHECK
          and d["worker"] == {"tier": "implementer", "tool": "claude", "model": "opus"}
          and (d.get("workflow"), d.get("role"), d.get("rung"), d.get("round"))
          == ("build-verify", "implementer", 2, 1)
          and d.get("step") == "GOAL-SENTINEL: make app.txt say FIXED.", rec)
    wt = os.path.realpath(w.wt("bv-k2-a1", 1))
    check("build-verify: both reviewers read the winner's worktree",
          len(calls) == 5 and os.path.realpath(calls[3]["cwd"]) == wt
          and os.path.realpath(after(calls[4]["argv"], "-C") or "") == wt
          and os.path.exists(os.path.join(runs, "bv-rev1", "review.json")),
          [(c["name"], c["cwd"]) for c in calls])
    md = r.stdout
    check("build-verify: bundle.md — status, row, check, patch, F-numbered findings, cost",
          "winner recorded passing" in md and "claude:opus · effort max · rung 2" in md
          and "recorder exit 0" in md and "+FIXED" in md
          and "F1 [claude:opus] app.txt:1 — first — scenario one" in md
          and "F2 [codex:default] app.txt:1 — second — scenario two" in md
          and "$0.2500" in md and "$0.5000" in md and "Reported cost: $0.7500" in md, md)
    check("build-verify: bundle.md names the next commands, and is saved as printed",
          "build-verify --repair-of bv --accepted" in md and "accept --run-id bv" in md
          and read(os.path.join(runs, "bv", "bundle.md")) == md, md[-800:])
    check("build-verify: bundle.json keeps the family, round, bases, briefs and check",
          b.get("family") == "bv" and b.get("round") == 1 and b.get("original_base") == head
          and b.get("check") == CHECK and b.get("workflow") == "build-verify"
          and read(b.get("original_brief", w.brief)) == read(w.brief)
          and win.get("harness") == "claude" and win.get("effort") == "max", b)

    # 13 — the recorder disagrees with the selection check: that attempt failed; with
    # no rung left, no winner (exit 1) and no review
    w.roles("| implementer | claude | sonnet | |", "| reviewer | claude | opus | |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    seen = "grep -qx FIXED app.txt && if [ -e .seen ]; then exit 1; else touch .seen; fi"
    r = w.dispatch("build-verify", "--brief", w.brief, "--check", seen, "--run-id", "nw")
    calls = w.calls()
    b = bundle("nw")
    rec = [d for d in events(w, "soul.delegation.checked") if d.get("run_id", "").startswith("nw-")]
    check("recorder fails a selected try: counted as that attempt failing, ladder goes on",
          [a.get("recorder_rc") for a in b.get("attempts", [])] == [1, 1]
          and [x["check"]["passed"] for x in rec] == [False, False]
          and len(calls) == 2 and "recorder's re-run" in calls[1]["stdin"],
          (b.get("attempts") and [a.get("recorder_rc") for a in b["attempts"]], len(calls)))
    check("no winner: exit 1, status no-winner, no review, bundle.md says so",
          r.returncode == 1 and b.get("status") == "no-winner" and b.get("winner") is None
          and b.get("review") is None and "no winner" in r.stdout
          and not os.path.exists(os.path.join(runs, "nw-rev1")), (r.returncode, r.stdout[:600]))

    # 13a — no bubblewrap: refused before any worker spends tokens (the recorder
    # confines every check, so the round could only end check-not-recorded)
    w.roles("| implementer | codex | default | |", "| reviewer | codex | default | |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    r = w.dispatch("build-verify", "--brief", w.brief, "--check", CHECK, "--run-id", "nb",
                   env=w.env(PATH=os.pathsep.join([w.bin, gitonly])))
    check("no bubblewrap: refused with exit 2 naming bubblewrap, no worker, no bundle",
          r.returncode == 2 and "bubblewrap" in r.stderr and len(w.calls()) == 0
          and not os.path.exists(os.path.join(runs, "nb", "bundle.json")),
          (r.returncode, r.stderr, r.stdout[:600]))
    check("build-verify: a family that already has a bundle is refused",
          w.dispatch("build-verify", "--brief", w.brief, "--check", CHECK, "--run-id",
                     "nw").returncode == 2)

    # 14 — repair: refusals first, with nothing recorded
    w.roles("| implementer | claude | sonnet | |", "| implementer | claude | opus | effort=max |",
            "| reviewer | claude | opus | |", "| reviewer | codex | default | |")
    acc = os.path.join(w.tmp, "accepted.txt")
    write(acc, "\n\n")
    w.script({"write": {"extra.txt": "round two\n"}})
    r = w.dispatch("build-verify", "--repair-of", "bv", "--accepted", acc)
    check("repair: an empty accepted file is refused", r.returncode == 2
          and "nothing accepted" in r.stderr and not w.calls(), r.stderr)
    write(acc, "F2: real\nF9 — not there\n")
    r = w.dispatch("build-verify", "--repair-of", "bv", "--accepted", acc)
    check("repair: an unknown finding id is refused, naming it", r.returncode == 2
          and "F9" in r.stderr and not w.calls(), r.stderr)
    fake = dict(bundle("bv"), round=3, run_id="fk-r3")
    write(os.path.join(runs, "fk-r3", "bundle.json"), json.dumps(fake))
    write(acc, "F2\n")
    r = w.dispatch("build-verify", "--repair-of", "fk-r3", "--accepted", acc)
    check("repair: refused at round 3 — two repair rounds are spent", r.returncode == 2
          and "two repair rounds are spent" in r.stderr and not w.calls(), r.stderr)
    r = w.dispatch("build-verify", "--repair-of", "nw", "--accepted", acc)
    check("repair: a round with no winner is refused", r.returncode == 2
          and "no recorded winner" in r.stderr, r.stderr)
    check("repair refusals record no tallies", not events(w, "soul.workflow.review"))

    # 14a — the repair round itself
    write(acc, "- F2: real defect\n")
    w.script({"write": {"extra.txt": "round two\n"}}, {"say": "NO FINDINGS"},
             {"say": "NO FINDINGS"})
    r = w.dispatch("build-verify", "--repair-of", "bv", "--accepted", acc)
    calls = w.calls()
    b = bundle("bv-r2")
    tallies = sorted((t["run_id"], t["reviewer"]["tool"], t["raised"], t["accepted"])
                     for t in events(w, "soul.workflow.review"))
    check("repair: one tally per reviewer of the previous round",
          tallies == [("bv-rev1", "claude", 1, 0), ("bv-rev1", "codex", 1, 1)], tallies)
    cand = git(w.proj, "rev-parse", "soul-wf/bv-k2-a1-1").stdout.strip()
    check("repair: the candidate is committed on its own worktree branch",
          git(w.proj, "log", "-1", "--format=%s", "soul-wf/bv-k2-a1-1").stdout.strip()
          == "candidate bv round 1" and cand != head
          and git(w.proj, "rev-parse", "HEAD").stdout.strip() == head, cand)
    stdin = calls[0]["stdin"] if calls else ""
    check("repair: the ladder starts at the previous winner's rung, from the candidate",
          r.returncode == 0 and calls and after(calls[0]["argv"], "--model") == "opus"
          and os.path.isdir(w.wt("bv-r2-k2-a1", 1))
          and git(w.wt("bv-r2-k2-a1", 1), "rev-parse", "HEAD").stdout.strip() == cand
          and b.get("base") == cand, (r.returncode, r.stderr, calls and calls[0]["argv"]))
    check("repair: the brief is the original plus the accepted findings, each with its note",
          stdin.startswith("GOAL-SENTINEL") and "## Accepted findings to fix" in stdin
          and "F2 [codex:default] app.txt:1 — second — scenario two" in stdin
          and "Host's note: real defect" in stdin and "scenario one" not in stdin
          and read(os.path.join(runs, "bv-r2", "brief.md")) in stdin, stdin)
    check("repair: bundle round 2, family and original base kept, review bv-rev2",
          b.get("round") == 2 and b.get("family") == "bv" and b.get("original_base") == head
          and (b.get("review") or {}).get("run_id") == "bv-rev2" and b.get("findings") == []
          and "accept --run-id bv-r2" in r.stdout, b)
    r = w.dispatch("build-verify", "--repair-of", "bv", "--accepted", acc)
    check("repair: the same round again is refused (it has a bundle)", r.returncode == 2
          and "already has a bundle" in r.stderr, r.stderr)

    # 15 — accept: both rounds' changes from the original base, applied, spot-checked,
    # the family cleaned
    r = w.dispatch("accept", "--run-id", "bv-r2")
    combined = read(os.path.join(runs, "bv-r2", "combined.patch")) \
        if os.path.exists(os.path.join(runs, "bv-r2", "combined.patch")) else ""
    check("accept: the combined patch is against the original base (both rounds)",
          "+FIXED" in combined and "+round two" in combined, combined)
    check("accept: applied to the project checkout",
          r.returncode == 0 and read(os.path.join(w.proj, "app.txt")) == "FIXED\n"
          and os.path.exists(os.path.join(w.proj, "extra.txt")), (r.returncode, r.stdout, r.stderr))
    spot = [d for d in events(w, "soul.delegation.checked") if d.get("run_id") == "bv-accept"]
    check("accept: the spot check is recorded, in the project, final round",
          len(spot) == 1 and spot[0]["check"]["passed"] is True and spot[0].get("round") == 2
          and spot[0]["worker"]["model"] == "opus", spot)
    tallies = [t for t in events(w, "soul.workflow.review") if t["run_id"] == "bv-rev2"]
    check("accept: the final round's tallies recorded, none accepted",
          len(tallies) == 2 and all(t["raised"] == 0 and t["accepted"] == 0 for t in tallies),
          tallies)
    listing = git(w.proj, "worktree", "list").stdout
    branches = git(w.proj, "branch", "--list", "soul-wf/bv-*").stdout
    check("accept: the family's worktrees and branches are gone",
          "/bv-" not in listing and not branches.strip() and "removed" in r.stdout,
          (listing, branches))
    r = w.dispatch("accept", "--run-id", "bv-r2")
    check("accept: a second accept is refused", r.returncode == 2, r.stderr)


def bv(w, run_id, *extra, check=CHECK, brief=None, env=None):
    return w.dispatch("build-verify", "--brief", brief or w.brief, "--check", check,
                      "--run-id", run_id, *extra, env=env)


def review_fix_cases():
    """16–24 — the 2026-10-28 review of v3.8.0: each defect it found, fixed."""
    def fresh(tag):
        return World(tempfile.mkdtemp(prefix="soul-dispatch-{}-".format(tag)))

    def bundle(w, run_id):
        path = os.path.join(w.proj, ".ai", "workflow-runs", run_id, "bundle.json")
        return json.loads(read(path)) if os.path.exists(path) else {}

    # 16 — clean --family X leaves family X-2 alone (accept cleans with it)
    w = fresh("fam")
    w.roles("| implementer | claude | sonnet | |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    bv(w, "X", "--no-review")
    bv(w, "X-2", "--no-review")
    r = w.dispatch("accept", "--run-id", "X")
    branches = git(w.proj, "branch", "--list", "soul-wf/*").stdout
    check("accept X leaves family X-2's worktree and branch",
          r.returncode == 0 and not os.path.exists(w.wt("X-k1-a1", 1))
          and os.path.isdir(w.wt("X-2-k1-a1", 1)) and "soul-wf/X-2-k1-a1-1" in branches,
          (r.returncode, r.stderr, branches))
    git(w.proj, "checkout", "--", ".")
    r = w.dispatch("accept", "--run-id", "X-2")
    check("then accept X-2 works", r.returncode == 0
          and read(os.path.join(w.proj, "app.txt")) == "FIXED\n", (r.returncode, r.stderr))
    for name in ("Y-head", "Y-zzz"):
        git(w.proj, "worktree", "add", "-q", "--detach",
            os.path.join(w.proj, ".ai", "worktrees", name), "HEAD")
    r = w.dispatch("clean", "--run-id", "Y", "--family")
    check("clean --family Y removes Y-head (the review workflow's), not Y-zzz",
          not os.path.exists(os.path.join(w.proj, ".ai", "worktrees", "Y-head"))
          and os.path.isdir(os.path.join(w.proj, ".ai", "worktrees", "Y-zzz")),
          r.stdout + r.stderr)
    shutil.rmtree(w.tmp, ignore_errors=True)

    # 17 — what the check leaves in a worktree is in neither the candidate commit,
    # the combined patch nor the project; round 1's change survives the repair
    w = fresh("art")
    w.roles("| implementer | claude | sonnet | |", "| reviewer | claude | opus | |")
    art = "grep -qx FIXED app.txt && if [ -f .git ]; then echo artefact > build.out; fi"
    w.script({"write": {"app.txt": "FIXED\n"}}, {"say": "FINDING: app.txt:1 — f — s\n"})
    r1 = bv(w, "art", check=art)
    acc = os.path.join(w.tmp, "acc.txt")
    write(acc, "F1\n")
    w.script({"write": {"extra.txt": "round two\n"}}, {"say": "NO FINDINGS"})
    r2 = w.dispatch("build-verify", "--repair-of", "art", "--accepted", acc)
    tree = git(w.proj, "ls-tree", "-r", "--name-only", "soul-wf/art-k1-a1-1").stdout.split()
    check("the candidate commit holds the try's patch, not the check's build.out",
          r1.returncode == 0 and r2.returncode == 0 and "app.txt" in tree
          and "build.out" not in tree and os.path.exists(os.path.join(w.wt("art-k1-a1", 1),
                                                                      "build.out"))
          and git(w.proj, "show", "soul-wf/art-k1-a1-1:app.txt").stdout == "FIXED\n",
          (r1.stderr, r2.stderr, tree))
    r = w.dispatch("accept", "--run-id", "art-r2")
    comb = os.path.join(w.proj, ".ai", "workflow-runs", "art-r2", "combined.patch")
    comb = read(comb) if os.path.exists(comb) else ""
    check("accept: the combined patch is the stored patches — no build.out, both rounds",
          r.returncode == 0 and "build.out" not in comb and "+FIXED" in comb
          and "+round two" in comb, (r.returncode, r.stderr, comb))
    check("accept: build.out never reaches the project",
          not os.path.exists(os.path.join(w.proj, "build.out"))
          and os.path.exists(os.path.join(w.proj, "extra.txt")), os.listdir(w.proj))
    shutil.rmtree(w.tmp, ignore_errors=True)

    # 18 — a non-Soul project with no SOUL_EVENT_LOG gets no .soul/; accept refuses
    # a subfolder of the checkout
    w = fresh("plain")
    git(w.proj, "rm", "-q", "witness.md")
    git(w.proj, "commit", "-qm", "not a Soul project")
    env = w.env()
    env.pop("SOUL_EVENT_LOG")
    w.roles("| implementer | claude | sonnet | |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    r = bv(w, "ns", "--no-review", env=env)
    sub = subprocess.run([sys.executable, _TOOL, "accept", "--run-id", "ns", "--project",
                          os.path.join(w.proj, "sub")], capture_output=True, text=True,
                         env=env, cwd=w.tmp)
    check("accept --project <subfolder>: refused, nothing applied",
          sub.returncode == 2 and "top level" in sub.stderr
          and read(os.path.join(w.proj, "app.txt")) == "BUG\n", sub.stderr)
    a = w.dispatch("accept", "--run-id", "ns", env=env)
    check("a non-Soul project gets no .soul/ from build-verify and accept",
          r.returncode == 0 and a.returncode == 0
          and not os.path.exists(os.path.join(w.proj, ".soul")),
          (r.returncode, a.returncode, r.stderr, a.stderr))
    shutil.rmtree(w.tmp, ignore_errors=True)

    w = fresh("misc")
    log = os.path.join(w.tmp, "events.jsonl")

    def evs(kind):
        return [json.loads(l)["data"] for l in (read(log) if os.path.exists(log) else "")
                .splitlines() if json.loads(l).get("type") == kind]

    # 19 — a brief whose first line is `---` (the step) reaches the recorder intact
    fm = os.path.join(w.tmp, "fm-brief.md")
    write(fm, "---\ntitle: x\n---\nmake app.txt say FIXED\n")
    w.roles("| implementer | claude | sonnet | |", "| reviewer | claude | opus | |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    r = bv(w, "fm", "--no-review", brief=fm)
    rec = [d for d in evs("soul.delegation.checked") if d.get("run_id") == "fm-k1-a1"]
    check("a step of `---` is recorded, not refused by the recorder's argparse",
          r.returncode == 0 and bundle(w, "fm").get("status") == "winner"
          and rec and rec[0].get("step") == "---", (r.returncode, r.stdout[-400:], rec))

    # 20 — a Latin-1 file in the patch: the bundle is still written
    w.script({"write": {"app.txt": "FIXED\n"}, "sh": "printf 'caf\\351\\n' > latin.txt"},
             {"say": "NO FINDINGS"})
    r = bv(w, "lt")
    check("a non-UTF-8 patch: review ran, bundle written, exit 0",
          r.returncode == 0 and bundle(w, "lt").get("status") == "winner"
          and "latin.txt" in r.stdout and len(w.calls()) == 2, (r.returncode, r.stderr[-600:]))

    # 21 — repair tallies only after the candidate is committed
    w.script({"write": {"app.txt": "FIXED\n"}}, {"say": "FINDING: app.txt:1 — f — s\n"})
    bv(w, "tc")
    w.dispatch("clean", "--run-id", "tc", "--family")
    acc = os.path.join(w.tmp, "acc.txt")
    write(acc, "F1\n")
    r = w.dispatch("build-verify", "--repair-of", "tc", "--accepted", acc)
    check("repair refused at the candidate commit records no tallies",
          r.returncode == 2 and not [t for t in evs("soul.workflow.review")
                                     if t["run_id"] == "tc-rev1"], (r.returncode, r.stderr))

    # 22 — a check that times out in the recorder is a recorded failure, not "not
    # recorded"
    w.roles("| implementer | claude | sonnet | timeout=2 |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    slow = "grep -qx FIXED app.txt && if [ -e .seen ]; then sleep 6; else touch .seen; fi"
    r = bv(w, "to", "--no-review", check=slow)
    b = bundle(w, "to")
    rec = [d for d in evs("soul.delegation.checked") if d.get("run_id", "").startswith("to-")]
    check("recorder timeout: counted as a failed attempt, recorded as timed out",
          r.returncode == 1 and b.get("status") == "no-winner"
          and [a["recorder_rc"] for a in b.get("attempts", [])] == [2, 2]
          and [d["check"]["timed_out"] for d in rec] == [True, True],
          (r.returncode, b.get("status"), rec))

    # 23 — accept: a patch that does not apply is refused, nothing applied; a spot
    # check that fails leaves the patch applied and prints the undo
    w.roles("| implementer | claude | sonnet | |")
    w.script({"write": {"app.txt": "FIXED\n"}})
    bv(w, "na", "--no-review")
    write(os.path.join(w.proj, "app.txt"), "LOCAL\n")
    r = w.dispatch("accept", "--run-id", "na")
    check("accept: a patch that does not apply here is refused, nothing applied",
          r.returncode == 2 and "does not apply" in r.stderr
          and read(os.path.join(w.proj, "app.txt")) == "LOCAL\n", (r.returncode, r.stderr))
    git(w.proj, "checkout", "--", ".")
    w.script({"write": {"app.txt": "FIXED\n"}})
    bv(w, "af", "--no-review", check="[ -f .git ] && " + CHECK)  # fails in the checkout
    r = w.dispatch("accept", "--run-id", "af")
    check("accept: a failing spot check exits 1, the patch stays, the undo is printed",
          r.returncode == 1 and "git apply -R" in r.stdout
          and read(os.path.join(w.proj, "app.txt")) == "FIXED\n", (r.returncode, r.stdout))
    git(w.proj, "checkout", "--", ".")

    # 24 — patches keep a/ b/ prefixes whatever the user's diff config says
    noprefix = w.env(GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="diff.noprefix",
                     GIT_CONFIG_VALUE_0="true")
    w.script({"write": {"app.txt": "FIXED\n"}})
    r = bv(w, "np", "--no-review", env=noprefix)
    patch = os.path.join(w.proj, ".ai", "workflow-runs", "np-k1-a1", "try-1.patch")
    patch = read(patch) if os.path.exists(patch) else ""
    a = w.dispatch("accept", "--run-id", "np", env=noprefix)
    comb = os.path.join(w.proj, ".ai", "workflow-runs", "np", "combined.patch")
    comb = read(comb) if os.path.exists(comb) else ""
    check("diff.noprefix set: try and combined patches keep a/ b/, accept applies",
          r.returncode == 0 and a.returncode == 0 and "--- a/app.txt" in patch
          and "+++ b/app.txt" in comb and read(os.path.join(w.proj, "app.txt")) == "FIXED\n",
          (r.returncode, a.returncode, a.stderr, patch[:300]))
    git(w.proj, "checkout", "--", ".")

    # 25 — clean's git runs none of the checkout's hooks (git 2.53 runs
    # reference-transaction on `branch -D`)
    # The host session may export core.hooksPath (GIT_CONFIG_COUNT/KEY/VALUE, as the
    # Soul secret guard does), which would hide the checkout's hooks from this case.
    plain = {k: v for k, v in w.env().items()
             if not k.startswith("GIT_CONFIG_") or k in ("GIT_CONFIG_GLOBAL",
                                                          "GIT_CONFIG_NOSYSTEM")}
    w.script({"write": {"app.txt": "FIXED\n"}})
    bv(w, "hk", "--no-review", env=plain)
    sentinel = os.path.join(w.tmp, "HOOK-RAN")
    hook = os.path.join(w.proj, ".git", "hooks", "reference-transaction")
    write(hook, "#!/bin/sh\ntouch {}\n".format(sentinel))
    os.chmod(hook, 0o755)
    git(w.proj, "branch", "ctl")
    subprocess.run(["git", "-C", w.proj, "branch", "-D", "ctl"], env=plain,
                   capture_output=True)
    live = os.path.exists(sentinel)  # control: plain git runs the hook here
    if live:
        os.remove(sentinel)
    r = w.dispatch("clean", "--run-id", "hk", "--family", env=plain)
    os.remove(hook)
    check("clean runs no hook of the checkout, and still deletes the branch",
          live and not os.path.exists(sentinel) and "1 branch(es)" in r.stdout,
          (live, r.stdout + r.stderr))
    shutil.rmtree(w.tmp, ignore_errors=True)


def section(text, start, end):
    """The text from the line holding `start` up to the next line holding `end`."""
    i = text.find(start)
    j = text.find(end, i + len(start)) if i >= 0 else -1
    return text[i:j if j >= 0 else None] if i >= 0 else ""


def docs():
    """The skill, the user guide and the tool's own help say what the code does
    (the 2026-10-27 review found each saying something no longer true)."""
    root = os.path.dirname(os.path.dirname(_TOOL))
    skill = " ".join(read(os.path.join(root, "skills", "soul-workflow", "SKILL.md")).split())
    guide = " ".join(read(os.path.join(root, "docs", "using-the-soul.md")).split())
    tool = read(_TOOL)
    step4 = section(skill, "### 4 ·", "### 5 ·")
    step7 = section(skill, "### 7 ·", "### 8 ·")
    step3 = section(skill, "### 3 ·", "### 4 ·")
    step5 = section(skill, "### 5 ·", "### 6 ·")
    check("skill: inside a workflow, implement and review go to its roles, not subagents",
          "never to this session's own subagents" in skill
          and "Outside a workflow run nothing here applies" in skill)
    page = " ".join(read(os.path.join(root, "docs", "workflows.md")).split())
    check("guide page: says what happens to the session's usual subagents",
          "usual subagents" in page and "Opus" in section(page, "## Your usual subagents", "##"))
    check("skill step 4: the recorder re-runs the check with --confine, patch read first",
          "--confine" in step4 and step4.find("patch") < step4.find("--confine"), step4[:600])
    check("skill step 7: the re-run is confined and comes after reading the patch",
          "--confine" in step7 and "patch" in step7
          and step7.find("patch") < step7.find("--confine"), step7)
    check("skill: apply the COMBINED change from the original base, not the last round's",
          "diff --binary --cached <original base>" in skill
          and "never only the last round's patch" in skill, section(skill, "### 6 ·", "### 8 ·"))
    check("skill: run ids -k<rung>-a<attempt>, -r<round>, -rev<round>; clean --family",
          all(s in skill for s in ("<id>-k<rung>-a<attempt>", "<id>-r<round>",
                                   "<id>-rev<round>", "clean --run-id <id> --family")), "")
    review = section(skill, "## review", "## Seeing how roles do")
    check("skill review workflow: a branch gets a worktree of <head> and --workdir",
          "<head>" in review and "worktree" in review and "--workdir" in review, review)
    check("skill: workers load no Soul record or project instructions, can still read",
          "load no Soul record or project instructions (they can still read files in "
          "their worktree)" in skill, section(skill, "What happens", "## The roles"))
    check("skill: the sandbox paragraph names the confined checks and the scoped writes",
          "--confine" in section(skill, "What happens", "## The roles")
          and "bubblewrap" in section(skill, "What happens", "## The roles"),
          section(skill, "What happens", "## The roles"))
    blocks = section(skill, "### Building blocks", "## review")
    check("skill: run and review commands pass --workflow <name>, built-ins included",
          "dispatch.py run --role implementer --workflow <name>" in blocks
          and "dispatch.py review --role reviewer --workflow <name>" in blocks
          and "--confine" in blocks and "built-ins included" in skill, blocks)
    step6 = section(skill, "### 6 ·", "### 7 ·")
    check("skill: the lean loop — one build-verify call per round, and why",
          "dispatch.py build-verify --workflow <name>" in step3
          and "experiments/2026-10-28-workflow-value/RESULT.md" in step3
          and "32 turns" in step3 and "--repair-of" in step6
          and "dispatch.py accept" in step7 and "bundle.md" in step4, (step3, step6))
    check("skill step 5: findings weighed against the patch, tallies by the next call",
          "against the patch" in step5 and "--repair-of" in step5
          and "do not record them by hand" in step5, step5)
    check("skill step 7: accept in the background, exit 2, tallies before the spot check",
          "background" in step7 and "Exit 2" in step7
          and step7.find("tallies") < step7.find("spot check)"), step7)
    check("skill step 4: check-not-recorded no longer blamed on a missing bubblewrap",
          "Check not recorded" in step4 and "no bubblewrap" not in step4, step4)
    template = read(os.path.join(root, "skills", "soul-workflow", "templates", "quick-fix.md"))
    check("quick-fix template: the record step points at the building blocks",
          "as in step 4" not in template and "Building blocks" in template, template)
    rules = section(skill, "What no workflow file can change", "A workflow file is")
    check("skill: no workflow file changes the recorded check or the patch read",
          "confined and recorded by the recorder" in rules
          and "reads every patch before `accept`" in rules
          and "`accept` re-runs the check on this checkout" in rules
          and "re-runs every check itself" not in skill, rules)
    roles = section(skill, "## The roles table", "## build-verify")
    check("skill roles: effort= and the codex default model/effort note",
          "`effort=`" in roles and "gpt-6.1-sol" in roles and "config.toml" in roles, roles)
    custom = section(skill, "## Custom workflows", "## Seeing how roles do")
    check("skill: a workflow's own ## Roles, the lookup order, and roles <name>",
          "## Roles" in custom and "/soul-workflow roles <name>" in skill
          and all(s in custom for s in ("`.claude/soul-roles.md`", "`~/.claude/soul-roles.md`",
                                        "built-in default")), custom)
    wguide = " ".join(read(os.path.join(root, "docs", "workflows.md")).split())
    part = section(wguide, "Different models for one workflow", "## When something goes wrong")
    check("workflows guide: one workflow's own models, lookup order, three workflows",
          "## Roles" in part and "security-check" in part and "quick-fix" in part
          and "build-verify" in part and "soul-roles.md" in part, part[:800])
    check("workflows guide: effort= and the codex default note, no host re-run claim",
          "`effort=`" in wguide and "gpt-6.1-sol" in wguide
          and "re-runs every check" not in wguide, "")
    check("guide: two reviewers by default — a fresh Claude and Codex when installed",
          "two reviewers by default — a fresh Claude and Codex when it is installed" in guide,
          section(guide, "Handing work to other models", "Moving to another"))
    helptext = " ".join(subprocess.run([sys.executable, _TOOL, "run", "--help"],
                                       capture_output=True, text=True).stdout.split())
    check("dispatch --check help no longer calls it the only Bash the worker may run",
          "--check" in helptext and "only Bash" not in helptext
          and "pick the winner" in helptext, helptext)
    check("worker_command has no unused check parameter",
          "def worker_command(row, workdir, mode, last_file=None)" in tool, "")
    head = tool[:tool.find('"""', tool.find('"""') + 3)]
    check("module docstring lists review --workdir and clean --family",
          "--workdir" in section(head, "review ", "clean ") and "--family" in head, head)
    check("module docstring lists build-verify, --repair-of, accept, and effort",
          "build-verify --brief" in head and "--repair-of" in head
          and "accept --run-id" in head and "`effort`" in head, head)
    for sub in ("build-verify", "accept"):
        r = subprocess.run([sys.executable, _TOOL, sub, "-h"], capture_output=True, text=True)
        check("dispatch {} -h prints its usage".format(sub),
              r.returncode == 0 and r.stdout.startswith("usage: dispatch.py " + sub), r.stderr)


def test_fence():
    assert main() == 0


if __name__ == "__main__":
    sys.exit(main())
