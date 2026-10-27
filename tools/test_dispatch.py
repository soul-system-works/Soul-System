"""Behaviour test for tools/dispatch.py run / review / clean (SOUL-I080).

FENCE: a worker gets the brief and nothing of the host's context. A Claude worker
starts with the isolation the 2026-10-27 probe verified (no setting sources, strict
MCP, every CLAUDE.md in reach excluded, auto-memory off) and with the host's
Anthropic routing removed — a host running on a local model must not send the
worker there by inheritance — while the Ollama route sets it on purpose; a Codex
worker skips user config, rules and AGENTS.md. Each try works in its own worktree
on its own branch and is never committed; the patch holds untracked files too;
best-of-n picks a passing try with the fewest changed lines; a hung worker is
killed with its whole process group and recorded as "timeout"; a try that touches
the record is flagged; reviewers run read-only and their FINDING lines are parsed;
`clean` removes only its own run's worktrees and branches.

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
import json, os, sys, time
log = os.environ["STUB_LOG"]
name = os.path.basename(sys.argv[0])
args = sys.argv[1:]
n = len([f for f in os.listdir(log) if f.startswith("call-")])
stdin = sys.stdin.read()
work = args[args.index("-C") + 1] if "-C" in args else os.getcwd()
with open(os.path.join(log, "call-%03d.json" % n), "w") as f:
    json.dump({{"name": name, "argv": args, "env": dict(os.environ), "cwd": os.getcwd(),
               "stdin": stdin}}, f)
plan = json.load(open(os.environ["STUB_PLAN"]))
act = plan[min(n, len(plan) - 1)]
time.sleep(act.get("sleep", 0))
for rel, text in act.get("write", {{}}).items():
    p = os.path.join(work, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(text)
say = act.get("say", "done")
sys.stderr.write(act.get("stderr", ""))
if name == "claude":
    print(json.dumps({{"type": "result", "result": say, "usage": {{
        "input_tokens": 100, "cache_read_input_tokens": 20, "output_tokens": 7}}}}))
else:
    open(args[args.index("-o") + 1], "w").write(say)
    print(json.dumps({{"type": "thread.started"}}))
    print(json.dumps({{"type": "turn.completed", "usage": {{
        "input_tokens": 50, "cached_input_tokens": 10, "output_tokens": 3}}}}))
sys.exit(act.get("exit", 0))
'''


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
        os.makedirs(self.home)
        os.makedirs(self.bin)
        os.makedirs(self.log)
        stub = STUB.format(python=sys.executable)
        for name in ("claude", "codex"):
            write(os.path.join(self.bin, name), stub)
            os.chmod(os.path.join(self.bin, name), 0o755)
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
        shutil.rmtree(self.log)
        os.makedirs(self.log)
        write(self.plan, json.dumps(list(acts)))

    def calls(self):
        out = []
        for f in sorted(os.listdir(self.log)):
            out.append(json.loads(read(os.path.join(self.log, f))))
        return out

    def env(self, **extra):
        env = {k: v for k, v in _GIT_ENV.items() if not k.startswith("ANTHROPIC_")}
        env.update(HOME=self.home, PATH=os.pathsep.join([self.bin, "/usr/bin", "/bin"]),
                   STUB_LOG=self.log, STUB_PLAN=self.plan)
        env.update(extra)
        return env

    def dispatch(self, *args, env=None, timeout=120):
        return subprocess.run([sys.executable, _TOOL, *args, "--project", self.proj],
                              capture_output=True, text=True, env=env or self.env(),
                              cwd=self.tmp, timeout=timeout)

    def run(self, run_id, *extra, env=None):
        r = self.dispatch("run", "--role", "implementer", "--brief", self.brief,
                          "--check", CHECK, "--run-id", run_id, *extra, env=env)
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
                     ANTHROPIC_AUTH_TOKEN="ollama", ANTHROPIC_API_KEY="sk-host")
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
    check("claude: full Bash for the implementer (the sandbox is the boundary)",
          after(argv, "--allowedTools") == "Read,Write,Edit,Glob,Grep,Bash", argv)
    sset = json.loads(after(argv, "--settings") or "{}")
    check("claude: sandbox on, auto-allow inside it, no unsandboxed escape",
          sset.get("sandbox") == {"enabled": True, "autoAllowBashIfSandboxed": True,
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
    r, res = w.run("o1", "--rung", "2")
    call = (w.calls() or [{"argv": [], "env": {}}])[0]
    env = call["env"]
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
    r, res = w.run("c1")
    call = (w.calls() or [{"argv": []}])[0]
    argv = call["argv"]
    wt = w.wt("c1", 1)
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
                     "- **FINDING:** app.txt:2 — second — scenario two\n"},
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
              "app.txt:2 — second — scenario two"]
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

    shutil.rmtree(tmp, ignore_errors=True)
    print("\n{} failure(s)".format(len(FAILS)) if FAILS else "\nALL PASS")
    return 1 if FAILS else 0


def test_fence():
    assert main() == 0


if __name__ == "__main__":
    sys.exit(main())
