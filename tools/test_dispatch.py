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

    shutil.rmtree(tmp, ignore_errors=True)
    docs()
    print("\n{} failure(s)".format(len(FAILS)) if FAILS else "\nALL PASS")
    return 1 if FAILS else 0


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


def test_fence():
    assert main() == 0


if __name__ == "__main__":
    sys.exit(main())
