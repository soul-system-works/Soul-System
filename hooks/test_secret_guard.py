"""Fence for the secret guard (SOUL-I070): git runs the check; credentials block,
names only warn.

FENCE: every case drives REAL git in a temp repo, with the session's env config set
exactly as the SessionStart hook sets it (its generated env file is sourced in
`sh -c`). The first build predicted git from the command text, and two
fresh-context reviews broke the prediction with shell forms (cd in a subshell,
GIT_DIR, pushd, aliases, comments, backslash-newline, quoted heredocs, files made
in the same command); those exact forms are here and must BLOCK, because git — not
a parser — now runs the check. A credential must block before the repo's own hook
runs; the repo's own hooks (git-lfs pre-push) must still run with the same
arguments and input, and their exit status must stand. A private name must WARN
and never block — SOUL-175 recorded the Body declining a mechanical
forbidden-strings guard. A credential may get through only VISIBLY (SOUL-178/185:
the by-hand scan missed twice): each unchecked path must say NOT checked. A
NAME-MAP name must never be printed (SOUL-169/175). Leaks this answers: SOUL-151
(work email in author metadata), SOUL-169/175/178 (real names in record text and a
commit subject).

Every "silent" or "allowed" assertion follows a case where the same fixture
produced the finding, so removing a check fails a test rather than passing it
vacuously. HOME, TMPDIR, CLAUDE_PLUGIN_DATA and git config are isolated; `gh` is a
stub; PATH holds only symlinks to the tools named (no /bin). The fake credential
is assembled at runtime so this file holds none.

Run: python3 hooks/test_secret_guard.py  (exit 0 = fence holds)
"""

import importlib.util
import json
import os
import random
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import textwrap
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(_HERE, "secret-guard.py")
CODEX = os.path.join(_HERE, "codex.py")
SKILL = os.path.join(_HERE, "..", "skills", "soul-init", "SKILL.md")
GITLEAKS = shutil.which("gitleaks") or os.path.expanduser("~/.local/bin/gitleaks")

FAKE_AWS = "AK" + "IA" + "QYLPMN5HHHFPZAM2"          # gitleaks rule: aws-access-token
KEYLINE = f'aws_access_key_id = "{FAKE_AWS}"'
NAME = "Zephyrine Holdings"                        # invented; on no real list
SURROUNDING = "quarterly pricing memo"             # must never be echoed
MAPNAME = "Quorvexian"                             # invented NAME-MAP identifier
MISSING = "Soul secret check NOT running — plugin path missing"
BYPASS = "Soul secret guard: this command bypasses git hooks — NOT checked"

OUTPUTS = []   # every captured output; checked for the secret at the end

_spec = importlib.util.spec_from_file_location("sg", HOOK)
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)


def _bin(tmp, name, targets):
    """A PATH directory holding only symlinks/scripts named in targets."""
    d = os.path.join(tmp, name)
    os.makedirs(d)
    for tool, target in targets.items():
        if isinstance(target, str) and os.path.exists(target):
            os.symlink(target, os.path.join(d, tool))
        elif isinstance(target, tuple):  # ("script", text)
            p = os.path.join(d, tool)
            with open(p, "w") as fh:
                fh.write(target[1])
            os.chmod(p, 0o755)
    return d


class Env:
    def __init__(self, tmp):
        self.tmp = tmp
        self.home = os.path.join(tmp, "home")
        self.state = os.path.join(tmp, "state")
        self.data = os.path.join(tmp, "plugin-data")
        self.envfile = os.path.join(tmp, "claude-env.sh")
        for d in (os.path.join(self.home, ".claude"), self.state, self.data):
            os.makedirs(d)
        self.gh_log = os.path.join(tmp, "gh.log")
        sleep = shutil.which("sleep")
        self.gh = {vis: _bin(tmp, "gh-" + vis.lower(), {"gh": ("script", (
            f'#!/bin/sh\necho "$@" >> "{self.gh_log}"\necho \'{{"visibility":"{vis}"}}\'\n'))})
            for vis in ("PUBLIC", "PRIVATE")}
        self.gh["HANG"] = _bin(tmp, "gh-hang", {"gh": ("script", f"#!/bin/sh\nexec {sleep} 30\n")})
        # Only git, python3, sh and bash — never a system dir that might hold gitleaks.
        self.base = _bin(tmp, "base", {"git": shutil.which("git"), "python3": sys.executable,
                                       "sh": shutil.which("sh"), "bash": shutil.which("bash"),
                                       "cat": shutil.which("cat"),
                                       "git-lfs": shutil.which("git-lfs") or ""})
        self.pidfile = os.path.join(tmp, "slow-gitleaks.pid")
        self.gl = {"real": _bin(tmp, "gl", {"gitleaks": GITLEAKS}), "none": None,
                   "slow": _bin(tmp, "glslow", {"gitleaks": (
                       "script", f'#!/bin/sh\necho $$ > "{self.pidfile}"\nexec {sleep} 30\n')})}
        self.codex_home = os.path.join(tmp, "codex-home")
        os.makedirs(self.codex_home)

    def env(self, vis="PUBLIC", gitleaks="real", **extra):
        path = [self.gh[vis], self.base] + ([self.gl[gitleaks]] if self.gl[gitleaks] else [])
        return {"PATH": os.pathsep.join(path), "HOME": self.home, "TMPDIR": self.state,
                "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
                "LANG": "C.UTF-8", "CLAUDE_PLUGIN_DATA": self.data, **extra}

    def names(self, text):
        with open(os.path.join(self.home, ".claude", "soul-private-names.txt"), "w") as fh:
            fh.write(text)

    @property
    def stable(self):
        return sg.stable_dir(self.data)   # one folder per plugin copy (N3)


def fake_private_key(seed):
    """A runtime-assembled fake RSA key block (gitleaks rule: private-key)."""
    r = random.Random(seed)
    body = "".join(r.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/") for _ in range(256))
    kind = "RSA " + "PRIVATE " + "KEY"
    return ("-----BEGIN " + kind + "-----\n" + "\n".join(body[i:i + 64] for i in range(0, 256, 64))
            + "\n-----END " + kind + "-----")


def plain_git(repo, *args, env=None):
    """git WITHOUT the session env: a hand commit/setup step, no guard."""
    e = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", **(env or {})}
    for k in [k for k in e if k.startswith("GIT_CONFIG_") and k not in ("GIT_CONFIG_GLOBAL", "GIT_CONFIG_NOSYSTEM")]:
        del e[k]
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True, env=e)


def make_repo(tmp, name, soul=True, email="dev@example.com", origin="https://github.com/example/repo.git"):
    repo = os.path.join(tmp, name)
    os.makedirs(repo)
    plain_git(repo, "init", "-q", "-b", "main")
    plain_git(repo, "config", "user.email", email)
    plain_git(repo, "config", "user.name", "Dev")
    if origin:
        plain_git(repo, "remote", "add", "origin", origin)
    if soul:
        write(repo, "witness.md", "# Witness\n")
    write(repo, "README.md", "readme\n")
    plain_git(repo, "add", ".")
    plain_git(repo, "commit", "-qm", "init")
    return repo


def write(repo, rel, text):
    path = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def recorder(path, log, code=0):
    """A fake repo hook (git-lfs shaped) that records its args and stdin."""
    write(os.path.dirname(path), os.path.basename(path),
          f'#!/bin/sh\necho "ARGS:$*" >> "{log}"\nwhile IFS= read -r l; do echo "IN:$l" >> "{log}"; done\n'
          f"exit {code}\n")
    os.chmod(path, 0o755)


def sh(E, cwd, command, shell="sh", envfile=None, **envkw):
    """Run `command` the way a session's Bash would: env file sourced first."""
    t0 = time.monotonic()
    r = subprocess.run([os.path.join(E.base, shell), "-c", f". '{envfile or E.envfile}'\n{command}"],
                       cwd=cwd, capture_output=True, text=True, env=E.env(**envkw), timeout=120)
    out = r.stdout + r.stderr
    OUTPUTS.append(out)
    return r.returncode, out, time.monotonic() - t0


def slurp(path):
    return open(path).read() if os.path.exists(path) else ""


def rm(path):
    if os.path.exists(path):
        os.remove(path)


def unlock(path):
    """The wrapper folder is read-only by design; a test that tampers must unlock it."""
    os.chmod(os.path.dirname(path), 0o700)
    if os.path.exists(path):
        os.chmod(path, 0o644)


def head(repo):
    return plain_git(repo, "rev-parse", "HEAD").stdout.strip()


def session_start(E, cwd, session="s1", envfile=None, **envkw):
    payload = {"hook_event_name": "SessionStart", "cwd": cwd, "session_id": session, "source": "startup"}
    r = subprocess.run([sys.executable, "-B", HOOK, "--session-start"], input=json.dumps(payload),
                       capture_output=True, text=True,
                       env=E.env(CLAUDE_ENV_FILE=envfile or E.envfile, **envkw))
    OUTPUTS.append(r.stdout + r.stderr)
    return r


def pretool(E, cwd, command):
    payload = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "cwd": cwd,
               "session_id": "s1", "tool_input": {"command": command}}
    r = subprocess.run([sys.executable, "-B", HOOK], input=json.dumps(payload),
                       capture_output=True, text=True, env=E.env())
    OUTPUTS.append(r.stdout + r.stderr)
    return json.loads(r.stdout) if r.stdout.strip() else None


def main():
    failures = []
    passed = [0]

    def check(cond, msg):
        if cond:
            passed[0] += 1
        else:
            failures.append(msg)

    if not os.path.exists(GITLEAKS):
        print("FAIL  gitleaks not installed — the credential cases cannot run (install gitleaks >= 8.19)")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmp:
        E = Env(tmp)
        E.names(f"# test list\n{NAME} => CLIENT-Z\nQX\nzephyrine.example\nC# Guild\nAnthe\n")

        # 0. SessionStart in a Soul repo installs the stable dir and writes the env file;
        # in a non-Soul cwd it does neither.
        r1 = make_repo(tmp, "r1")
        plain_dir = os.path.join(tmp, "plain")
        os.makedirs(plain_dir)
        r = session_start(E, plain_dir, envfile=os.path.join(tmp, "plain-env.sh"))
        check(not os.path.exists(os.path.join(tmp, "plain-env.sh")) and r.stdout.strip() == "",
              "SCOPE: SessionStart armed the guard outside a Soul project")
        # A wrapper an older version shipped (owned) and someone else's file (not owned).
        os.makedirs(E.stable)
        write(E.stable, "reference-transaction", "#!/bin/sh\n" + sg.OWNED + "\nexit 0\n")
        write(E.stable, "my-notes.txt", "not ours\n")
        r = session_start(E, r1)
        check(r.returncode == 0 and r.stdout.strip() == "", f"START: SessionStart was not silent when armed: {r.stdout}")
        wrappers = set(os.listdir(E.stable)) if os.path.isdir(E.stable) else set()
        check({"pre-commit", "pre-applypatch", "commit-msg", "pre-push", "post-checkout", "post-commit",
               "post-merge", "post-rewrite", "pre-receive", "update", "post-update"} <= wrappers,
              "INSTALL: the stable dir lacks standard hook wrappers (repo hooks would silently stop)")
        check(not {"push-to-checkout", "reference-transaction", "post-index-change"} & wrappers,
              "INSTALL: a costly or semantics-changing wrapper is installed (D2 / push-to-checkout)")
        check("my-notes.txt" in wrappers, "INSTALL: install() removed a file it does not own")
        check(os.stat(E.stable).st_mode & 0o222 == 0
              and os.stat(os.path.join(E.stable, "pre-push")).st_mode & 0o222 == 0,
              "READ-ONLY: the wrapper folder or a wrapper is writable after install (H1)")
        with open(E.envfile) as fh:
            first = fh.read()
        session_start(E, r1)
        with open(E.envfile) as fh:
            check(fh.read() == first, "IDEMPOTENT: a second SessionStart appended the env block again")

        # 1. Env file idempotence: sourced twice adds one entry; an existing count is respected.
        rc, out, _ = sh(E, r1, f". '{E.envfile}'\necho \"N=$GIT_CONFIG_COUNT K=$GIT_CONFIG_KEY_0\"")
        check("N=1 K=core.hooksPath" in out, f"IDEMPOTENT: sourcing the env file twice gave {out.strip()!r}")
        rc, out, _ = sh(E, r1, f". '{E.envfile}'\necho \"N=$GIT_CONFIG_COUNT K=$GIT_CONFIG_KEY_1\"\n"
                        "git config user.name\ngit rev-parse --git-path hooks",
                        GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="user.name", GIT_CONFIG_VALUE_0="Preset")
        check("N=2 K=core.hooksPath" in out and "Preset" in out and E.stable in out,
              f"COUNT: a pre-existing GIT_CONFIG_COUNT=1 was not respected: {out.strip()!r}")

        # 1b. A session started in a subfolder of a Soul repo is armed (walk up, M2).
        deep = os.path.join(r1, "deep", "er")
        os.makedirs(deep)
        sub_env = os.path.join(tmp, "sub-env.sh")
        r = session_start(E, deep, envfile=sub_env)
        check(r.stdout.strip() == "" and "core.hooksPath" in slurp(sub_env),
              f"SCOPE: a session started in a subfolder of a Soul repo was not armed: {r.stdout!r}")

        # 1c. SessionStart verifies arming (M5): too-old git, and an env file that does not
        # leave git's hooks path at the folder, both say NOT armed.
        oldgit = _bin(tmp, "oldgit", {"git": ("script", (
            f'#!/bin/sh\n[ "$1" = --version ] && {{ echo "git version 2.20.1"; exit 0; }}\n'
            f'exec "{shutil.which("git")}" "$@"\n'))})
        old_env = E.env(CLAUDE_ENV_FILE=os.path.join(tmp, "old-env.sh"))
        old_env["PATH"] = oldgit + os.pathsep + old_env["PATH"]
        r = subprocess.run([sys.executable, "-B", HOOK, "--session-start"], capture_output=True, text=True,
                           input=json.dumps({"hook_event_name": "SessionStart", "cwd": r1, "session_id": "old"}),
                           env=old_env)
        OUTPUTS.append(r.stdout)
        check("NOT armed" in r.stdout and "older than 2.31" in r.stdout, f"ARMING: git 2.20 was not refused: {r.stdout!r}")
        r = session_start(E, r1, envfile=os.path.join(tmp, "params-env.sh"),
                          GIT_CONFIG_PARAMETERS="'core.hookspath'='/elsewhere'")
        check("NOT armed" in r.stdout and "/elsewhere" in r.stdout,
              f"ARMING: an env where git's hooks path is not the folder was not reported: {r.stdout!r}")

        # 1d. M3: the snippet arms only while the folder exists — silently otherwise.
        gone_env = os.path.join(tmp, "gone-env.sh")
        write(tmp, "gone-env.sh", sg.env_snippet(os.path.join(tmp, "no-such-dir"), "s", r1))
        rc, out, _ = sh(E, r1, "echo \"N=${GIT_CONFIG_COUNT:-unset} H=$(git config core.hooksPath)\"", envfile=gone_env)
        check(rc == 0 and out.strip() == "N=unset H=", f"MISSING-DIR: the snippet armed a folder that does not exist: {out!r}")

        # 1e. L5: leading zeros are stripped; a non-number is not armed, with a notice, no shell error.
        rc, out, _ = sh(E, r1, "echo \"N=$GIT_CONFIG_COUNT K=$GIT_CONFIG_KEY_1\"; git config user.name",
                        GIT_CONFIG_COUNT="01", GIT_CONFIG_KEY_0="user.name", GIT_CONFIG_VALUE_0="Zeroed")
        check(rc == 0 and "N=2 K=core.hooksPath" in out and "Zeroed" in out, f"COUNT: GIT_CONFIG_COUNT=01 mishandled: {out!r}")
        rc, out, _ = sh(E, r1, "echo \"N=$GIT_CONFIG_COUNT\"", GIT_CONFIG_COUNT="abc")
        check(rc == 0 and "N=abc" in out and "NOT armed for this command" in out,
              f"COUNT: a non-numeric GIT_CONFIG_COUNT was not left alone with a notice: {out!r}")

        # 1f. H1: an installer writing into git's hooks path fails loudly inside a session;
        # PreToolUse reinstalls a modified or missing folder and says so; installers get a notice.
        rc, out, _ = sh(E, r1, 'printf "#!/bin/sh\\n" > "$(git rev-parse --git-path hooks)/pre-push"')
        check(rc != 0, "READ-ONLY: a hook installer overwrote a wrapper inside the session")
        target = os.path.join(E.stable, "pre-commit")
        unlock(target)
        write(E.stable, "pre-commit", "#!/bin/sh\nexit 0\n")
        out = pretool(E, r1, "ls")
        check(out is not None and "modified — reinstalled" in out["systemMessage"]
              and sg.OWNED in slurp(target) and os.stat(target).st_mode & 0o222 == 0,
              f"REINSTALL: a modified wrapper was not restored and reported: {out!r}")
        os.chmod(E.stable, 0o700)
        shutil.rmtree(E.stable)
        out = pretool(E, r1, "ls")
        check(out is not None and "missing — reinstalled" in out["systemMessage"] and os.path.isdir(E.stable),
              f"REINSTALL: a missing folder was not reinstalled and reported: {out!r}")
        if not os.path.isdir(E.stable):   # keep the rest of the fence running
            sg.install(E.data)
        check(pretool(E, r1, "ls") is None, "NOISE: an intact folder drew a PreToolUse message")
        for form in ("git lfs install", "pre-commit install", "npx husky init", "git config core.hooksPath .husky",
                     "lefthook install", "git lfs track '*.bin'"):
            out = pretool(E, r1, form)
            check(out is not None and "run hook installers outside an AI session" in out["systemMessage"],
                  f"NOTICE: hook installer {form!r} drew no notice")

        # 2. Staged credential → blocked by git's own pre-commit; the value is never printed.
        write(r1, "cfg.py", KEYLINE + "\n")
        before = head(r1)
        rc, out, _ = sh(E, r1, "git add cfg.py && git commit -m 'add config'")
        check(rc != 0 and "BLOCKED" in out and head(r1) == before, "MISS: staged AWS key did not block the commit")
        check("aws-access-token" in out and ".gitleaksignore" in out and "Do NOT add" in out,
              "MISS: block message lacks the rule or the owner-only override")
        plain_git(r1, "reset", "-q")

        # 3. The reviewers' escapes: every one now reaches git's hook and blocks.
        sub = os.path.join(r1, "sub")
        os.makedirs(sub)
        sibling = os.path.join(tmp, "sibling")
        os.makedirs(sibling)
        write(r1, "do-commit.sh", "git add -A\ngit commit -qm scripted\n")
        forms = [
            ("cd in a subshell", r1, "sh", "(cd sub && true) && git add . && git commit -m x"),
            ("GIT_DIR/GIT_WORK_TREE", sibling, "sh",
             "GIT_DIR=../r1/.git GIT_WORK_TREE=../r1 git add -A && "
             "GIT_DIR=../r1/.git GIT_WORK_TREE=../r1 git commit -m x"),
            ("pushd", r1, "bash", "pushd sub >/dev/null\ngit add -A\ngit commit -m x"),
            ("git alias", r1, "sh", "git add -A && git -c alias.k=commit k -m x"),
            ("trailing # comment line", r1, "sh", "git add -A && git commit -m x\n# commit done"),
            ("backslash-newline", r1, "sh", "git add -A && git \\\n  commit -m x"),
            ("quoted <<EOF message", r1, "sh", "git add -A && git commit -F - <<'EOF'\nfix: the 12\" display\nEOF"),
            ("a script file", r1, "sh", "sh do-commit.sh"),
            ("commit -a over a tracked file", r1, "sh", f"printf '%s\\n' '{KEYLINE}' >> README.md && git commit -am x"),
        ]
        for label, cwd, shell, form in forms:
            before = head(r1)
            rc, out, _ = sh(E, cwd, form, shell=shell)
            check(rc != 0 and "BLOCKED" in out and head(r1) == before, f"ESCAPE: {label} was not blocked: {out[-300:]!r}")
            plain_git(r1, "reset", "-q")
        plain_git(r1, "checkout", "-q", "--", "README.md")
        os.remove(os.path.join(r1, "do-commit.sh"))
        # A file created by the same command.
        os.remove(os.path.join(r1, "cfg.py"))
        before = head(r1)
        rc, out, _ = sh(E, r1, f"printf '%s\\n' '{KEYLINE}' > new.py && git add new.py && git commit -qm new")
        check(rc != 0 and "BLOCKED" in out and head(r1) == before,
              "ESCAPE: a credential file created by the same command was not blocked")
        plain_git(r1, "reset", "-q")
        os.remove(os.path.join(r1, "new.py"))

        # 4. Bypass notice (warn only, Claude PreToolUse): --no-verify noticed; a plain commit silent.
        out = pretool(E, r1, "git commit --no-verify -m x")
        check(out is not None and BYPASS in json.dumps(out, ensure_ascii=False)
              and "permissionDecision" not in json.dumps(out),
              "NOTICE: --no-verify was not noticed (or the notice tried to decide)")
        check(pretool(E, r1, "git commit -m 'no verify needed'") is None, "NOISE: plain commit drew a bypass notice")
        check(pretool(E, plain_dir, "git commit --no-verify -m x") is None, "SCOPE: bypass notice outside a Soul project")
        for form in ("git commit -nm x", "git -c core.hooksPath=/dev/null commit -m x",
                     "unset GIT_CONFIG_COUNT; git commit -m x", "env -i git commit -m x",
                     "git commit --no-veri -m x", "git push --no-v", "git -C sub commit -n -m x",
                     "SOUL_GUARD_ACTIVE=x git commit -m x", "export SOUL_GUARD_BUDGET=0; git push",
                     "env SOUL_GUARD_CWD=/ git commit -m x", "unset SOUL_GUARD_SESSION",
                     "SOUL_GUARD_X+=1 git commit -m x", "printf -v SOUL_GUARD_ACTIVE %s x; git commit -m x",
                     "read SOUL_GUARD_ACTIVE < f; git commit -m x", "export -n SOUL_GUARD_CWD",
                     "env -u SOUL_GUARD_SESSION git commit -m x"):
            out = pretool(E, r1, form)
            check(out is not None and BYPASS in json.dumps(out, ensure_ascii=False), f"NOTICE: missed {form!r}")

        for form in ("git log -n 3", "git push -n origin main", "git commit -m 'no-verify docs'"):
            out = pretool(E, r1, form)
            check(out is None, f"NOISE: {form!r} drew a bypass notice")

        # 5. Push: an unpushed credential commit (made by hand, outside the session) is blocked;
        # the remote is unchanged; the repo's own pre-push (fake git-lfs) never runs for it.
        bare = os.path.join(tmp, "remote.git")
        subprocess.run(["git", "init", "-q", "--bare", bare], check=True)
        r5 = make_repo(tmp, "r5")
        plain_git(r5, "config", "remote.origin.pushurl", bare)
        lfs_log = os.path.join(tmp, "lfs.log")
        recorder(os.path.join(r5, ".git", "hooks", "pre-push"), lfs_log)
        rc, out, _ = sh(E, r5, "git push -q origin main")
        check(rc == 0 and os.path.exists(lfs_log), f"CHAIN: a clean push failed or skipped the repo's pre-push: {out!r}")
        rec = slurp(lfs_log)
        main_sha = head(r5)
        check(f"ARGS:origin {bare}" in rec and f"IN:refs/heads/main {main_sha} refs/heads/main " in rec,
              f"CHAIN: the repo's pre-push did not get git's args and ref lines: {rec!r}")
        rm(lfs_log)
        write(r5, "cfg.py", KEYLINE + "\n")
        plain_git(r5, "add", "cfg.py")
        plain_git(r5, "commit", "-qm", "by hand")
        remote_before = plain_git(bare, "rev-parse", "main").stdout
        rc, out, _ = sh(E, r5, "git push origin main")
        check(rc != 0 and "BLOCKED" in out and "push" in out, "MISS: push of an unpushed credential commit was not blocked")
        check(plain_git(bare, "rev-parse", "main").stdout == remote_before, "MISS: the remote moved despite the block")
        check(not os.path.exists(lfs_log), "ORDER: the repo's pre-push ran although the guard had blocked")
        # First push of a new branch, and a glob refspec.
        plain_git(r5, "checkout", "-q", "-b", "feature")
        rc, out, _ = sh(E, r5, "git push -u origin feature")
        check(rc != 0 and "BLOCKED" in out, "MISS: the first push of a new branch was not scanned")
        rc, out, _ = sh(E, r5, "git push origin 'refs/heads/*:refs/heads/*'")
        check(rc != 0 and "BLOCKED" in out, "MISS: a glob refspec push passed a credential commit")
        check(plain_git(bare, "for-each-ref", "--format=%(refname:short)", "refs/heads").stdout.strip() == "main", "MISS: a blocked branch reached the remote")
        plain_git(r5, "checkout", "-q", "main")
        plain_git(r5, "branch", "-q", "-D", "feature")
        plain_git(r5, "reset", "-q", "--hard", "HEAD~1")

        # 6. The repo's own hook's non-zero exit stands.
        plain_git(r5, "commit", "-q", "--allow-empty", "-m", "clean")
        recorder(os.path.join(r5, ".git", "hooks", "pre-push"), lfs_log, code=7)
        rc, out, _ = sh(E, r5, "git push origin main")
        check(rc != 0 and plain_git(bare, "rev-parse", "main").stdout == remote_before,
              "CHAIN: the repo's pre-push exit 7 did not stop the push")
        recorder(os.path.join(r5, ".git", "hooks", "pre-push"), lfs_log)
        rc, out, _ = sh(E, r5, "git push -q origin main")
        check(rc == 0 and "BLOCKED" not in out and out.strip() == "",
              f"NOISE: a clean push with nothing to report printed {out!r}")
        rm(lfs_log)

        # 7. Names on push (public): an author email and a message, warned; the push goes through.
        plain_git(r5, "commit", "-q", "--allow-empty", "-m", f"note for {NAME}",
                  env={"GIT_AUTHOR_EMAIL": "dev@zephyrine.example"})
        rc, out, _ = sh(E, r5, "git push origin main")
        check(rc == 0 and f'"{NAME}"' in out and "message" in out and "author/committer email" in out
              and "zephyrine.example" in out, f"MISS: names/email on push did not warn (or blocked): {out!r}")
        check(plain_git(bare, "rev-parse", "main").stdout.strip() == head(r5), "WRONG: a name warning stopped the push")
        check(f"IN:refs/heads/main {head(r5)}" in slurp(lfs_log), "CHAIN: lfs did not get the ref line after a warning")

        # 8. Repo-local core.hooksPath and a non-guard hook (post-commit) are chained.
        r8 = make_repo(tmp, "r8")
        local_log = os.path.join(tmp, "local.log")
        recorder(os.path.join(r8, ".myhooks", "pre-commit"), local_log)
        recorder(os.path.join(r8, ".myhooks", "post-commit"), local_log)
        plain_git(r8, "config", "core.hooksPath", ".myhooks")
        rc, out, _ = sh(E, r8, "git commit -q --allow-empty -m ok")
        rec = slurp(local_log)
        check(rc == 0 and rec.count("ARGS:") == 2, f"CHAIN: repo-local core.hooksPath hooks did not both run: {rec!r}")

        # 9. Non-Soul repo: the same staged key blocks while Soul-scoped, passes once not,
        # and the repo's own pre-commit still runs.
        r9 = make_repo(tmp, "r9")
        own_log = os.path.join(tmp, "own.log")
        recorder(os.path.join(r9, ".git", "hooks", "pre-commit"), own_log)
        write(r9, "cfg.py", KEYLINE + "\n")
        plain_git(r9, "add", "cfg.py")
        rc, out, _ = sh(E, r9, "git commit -m x")
        check(rc != 0 and "BLOCKED" in out, "FIXTURE: the scope case did not block while Soul-scoped")
        plain_git(r9, "rm", "-q", "--cached", "witness.md")
        os.remove(os.path.join(r9, "witness.md"))
        rc, out, _ = sh(E, r9, "git commit -qm x")
        check(rc == 0 and "Soul secret" not in out, f"SCOPE: the guard ran in a non-Soul repo: {out!r}")
        check(os.path.exists(own_log), "CHAIN: the non-Soul repo's own pre-commit did not run")

        # 10. Plugin root missing → fail open loudly AND still chain.
        pointer = os.path.join(E.stable, "plugin-root")
        unlock(pointer)
        with open(pointer, "w") as fh:
            fh.write(os.path.join(tmp, "gone") + "\n")
        rm(own_log)
        write(r9, "witness.md", "# Witness\n")
        write(r9, "cfg2.py", KEYLINE + "\n")
        plain_git(r9, "add", "witness.md", "cfg2.py")
        rc, out, _ = sh(E, r9, "git commit -qm gone")
        check(rc == 0 and MISSING in out and "/soul-init" in out, f"SILENT: a missing plugin path did not fail open loudly: {out!r}")
        check(os.path.exists(own_log), "CHAIN: with the plugin path missing, the repo's own hook did not run")
        out = pretool(E, r1, "ls")
        check(out is not None and "modified — reinstalled" in out["systemMessage"], "REINSTALL: a tampered pointer was not restored")

        # 10b. N2: a marker set from outside never skips the wrapper's check.
        write(r9, "cfg3.py", KEYLINE + "\n")
        plain_git(r9, "add", "cfg3.py")
        before = head(r9)
        for mark in (f"pre-commit:{os.path.realpath(r9)}", f"pre-commit:{os.path.realpath(r9)}:1"):
            rc, out, _ = sh(E, r9, f"SOUL_GUARD_ACTIVE='{mark}' git commit -qm marked")
            check(rc != 0 and "BLOCKED" in out and head(r9) == before,
                  f"BYPASS: a preset SOUL_GUARD_ACTIVE={mark!r} skipped the check: {out!r}")
        plain_git(r9, "reset", "-q")

        # 11. Names in a commit (public): staged file, path, -m (commit-msg), author;
        # never the surrounding line. Private: silent. gh hang: treated public, in budget.
        r11 = make_repo(tmp, "r11", email="dev@zephyrine.example")
        write(r11, "notes.md", f"The {SURROUNDING} for {NAME.upper()} is here.\n")
        plain_git(r11, "add", "notes.md")
        rc, out, _ = sh(E, r11, "git commit -qm notes")
        check(rc == 0 and f'"{NAME}"' in out and "file notes.md" in out and "CLIENT-Z" in out,
              f"MISS: name in a staged file did not warn (or blocked): {out!r}")
        check(SURROUNDING not in out, "LEAK: name warning echoed the surrounding line")
        check("author/committer email" in out and "PUBLIC repo" in out,
              "MISS: author email on the list did not warn in a public repo (SOUL-151 shape)")
        plain_git(r11, "config", "user.email", "dev@example.com")
        rc, out, _ = sh(E, r11, f"git commit -q --allow-empty -m 'Ship for {NAME}'")
        check(rc == 0 and "commit message" in out and f'"{NAME}"' in out, "MISS: name in the commit message did not warn")
        rc, out, _ = sh(E, r11, f"git commit -q --allow-empty -m x -m '# for {NAME}'")
        check(rc == 0 and "commit message" in out and f'"{NAME}"' in out,
              f"MISS: a '#' line that git keeps (-m, no editor) was dropped before the name check: {out!r}")
        rc, out, _ = sh(E, r11, f"export SOUL_GUARD_SESSION=s-priv\ngit commit -q --allow-empty -m 'Ship for {NAME}'",
                        vis="PRIVATE")
        check(rc == 0 and out.strip() == "", f"NOISE: name warning fired in a private repo: {out!r}")
        open(E.gh_log, "w").close()
        for m in ("a", "b"):
            sh(E, r11, f"export SOUL_GUARD_SESSION=s-cache\ngit commit -q --allow-empty -m '{m} {NAME}'")
        with open(E.gh_log) as fh:
            check(len(fh.readlines()) == 1, "CACHE: gh was asked more than once per repo per session")
        rc, out, took = sh(E, r11, f"export SOUL_GUARD_SESSION=s-hang\ngit commit -q --allow-empty -m 'for {NAME}'",
                           vis="HANG")
        check(rc == 0 and f'"{NAME}"' in out and "treated as public" in out and took < 20,
              f"HANG: a hung gh was not treated as public within budget ({took:.1f}s): {out!r}")

        # 12. Whole-word matching, `C# Guild`, `!` allowed phrases, names in paths.
        write(r11, "words.md", "the pantheon, the QXR module, a preqx run\n")
        plain_git(r11, "add", "words.md")
        rc, out, _ = sh(E, r11, "git commit -qm w")
        check('"Anthe"' not in out and '"QX"' not in out, f"NOISE: an entry matched inside a word: {out!r}")
        write(r11, "x/anthe-notes.md", "plain\n")
        write(r11, "guild.md", "joined the C# Guild\n")
        plain_git(r11, "add", ".")
        rc, out, _ = sh(E, r11, "git commit -qm p")
        check('"Anthe"' in out and "file x/anthe-notes.md" in out,
              "MISS: an entry as its own path segment (x/<entry>-notes.md) did not warn")
        check('"C# Guild"' in out, "PARSE: `C# Guild` was cut at '#' (a comment only starts a line)")
        E.names(f"{NAME} => CLIENT-Z\n!{NAME} v. State (2019)\n")
        write(r11, "cite.md", f"See {NAME} v. State (2019).\n")
        plain_git(r11, "add", "cite.md")
        rc, out, _ = sh(E, r11, "git commit -qm c")
        check(f'"{NAME}"' not in out, "NOISE: an allowed phrase still warned")
        write(r11, "cite.md", f"See {NAME} v. State (2019); also {NAME} alone.\n")
        plain_git(r11, "add", "cite.md")
        rc, out, _ = sh(E, r11, "git commit -qm c2")
        check(f'"{NAME}"' in out, "OVER-MASK: the allowed phrase hid a bare use of the name")
        E.names(f"# test list\n{NAME} => CLIENT-Z\nQX\nzephyrine.example\nC# Guild\nAnthe\n")

        # 13. A name-list file staged → warn (private repos too); its staged deletion does not.
        write(r11, ".soul/private-names.txt", "Somebody\n")
        plain_git(r11, "add", ".soul/private-names.txt")
        rc, out, _ = sh(E, r11, "export SOUL_GUARD_SESSION=s-priv\ngit commit -qm lists", vis="PRIVATE")
        check(rc == 0 and "private-name list is staged" in out, "MISS: a staged name-list file did not warn")
        plain_git(r11, "rm", "-q", "--cached", ".soul/private-names.txt")
        rc, out, _ = sh(E, r11, "export SOUL_GUARD_SESSION=s-priv\ngit commit -qm untrack", vis="PRIVATE")
        check("private-name list is staged" not in out, "NOISE: removing a name list from git warned that it was staged")
        os.remove(os.path.join(r11, ".soul", "private-names.txt"))

        # 14. Override files: compared by bytes with HEAD — untracked, ignored and
        # skip-worktree all reported; an owner-approved entry clears the finding.
        r14 = make_repo(tmp, "r14")
        write(r14, "cfg.py", KEYLINE + "\n")
        plain_git(r14, "add", "cfg.py")
        write(r14, ".gitleaksignore", "cfg.py:aws-access-token:1\n")
        rc, out, _ = sh(E, r14, "git commit -qm untracked-ignore")
        check(rc == 0 and ".gitleaksignore differs from HEAD" in out,
              f"SILENT: an untracked .gitleaksignore cleared a finding without saying so: {out!r}")
        plain_git(r14, "reset", "-q", "--soft", "HEAD~1")
        write(r14, ".git/info/exclude", ".gitleaksignore\n")
        rc, out, _ = sh(E, r14, "git commit -qm ignored-ignore")
        check(rc == 0 and ".gitleaksignore differs from HEAD" in out, "SILENT: an excluded .gitleaksignore was not reported")
        plain_git(r14, "reset", "-q", "--soft", "HEAD~1")
        plain_git(r14, "reset", "-q")
        write(r14, ".git/info/exclude", "")
        write(r14, ".gitleaksignore", "# none yet\n")
        plain_git(r14, "add", ".gitleaksignore")
        plain_git(r14, "commit", "-qm", "empty ignore")
        plain_git(r14, "update-index", "--skip-worktree", ".gitleaksignore")
        write(r14, ".gitleaksignore", "cfg.py:aws-access-token:1\n")
        plain_git(r14, "add", "cfg.py")
        rc, out, _ = sh(E, r14, "git commit -qm skip-worktree")
        check(rc == 0 and ".gitleaksignore differs from HEAD" in out, "SILENT: a skip-worktree .gitleaksignore was not reported")
        plain_git(r14, "reset", "-q", "--soft", "HEAD~1")
        write(r14, ".gitleaksignore", "# none yet\n")
        rc, out, _ = sh(E, r14, "git commit -qm committed-ignore")
        check(rc != 0 and "BLOCKED" in out and "differs from HEAD" not in out,
              "FIXTURE: with the override equal to HEAD the finding did not block")
        rc, out, _ = sh(E, r14, "git commit -qm env-config", GITLEAKS_CONFIG=os.devnull)
        check("$GITLEAKS_CONFIG is set" in out, "SILENT: $GITLEAKS_CONFIG was not reported")
        # Inline gitleaks:allow does not clear a finding.
        write(r14, "cfg.py", KEYLINE + "  # gitleaks:allow\n")
        plain_git(r14, "add", "cfg.py")
        rc, out, _ = sh(E, r14, "git commit -qm allow-comment")
        check(rc != 0 and "BLOCKED" in out, "BYPASS: an inline gitleaks:allow comment cleared a finding")

        # 15. Time-out keeps a found credential blocking; says what was not fully checked.
        rc, out, took = sh(E, r14, "export SOUL_GUARD_SESSION=s-timeout\ngit commit -qm slow",
                           vis="HANG", SOUL_GUARD_BUDGET="3")
        check(rc != 0 and "BLOCKED" in out and "timed out" in out and "NOT fully checked" in out and took < 20,
              f"TIMEOUT: a found credential did not keep blocking after the budget ran out ({took:.1f}s): {out!r}")
        plain_git(r14, "reset", "-q")

        # 16. gitleaks missing → a loud line on every run; one event per repo per session.
        write(r14, "ok.txt", "fine\n")
        plain_git(r14, "add", "ok.txt")
        outs = [sh(E, r14, "export SOUL_GUARD_SESSION=s-nogl\ngit commit -q --allow-empty -m n", gitleaks="none")
                for _ in range(2)]
        check(all(o[0] == 0 and "credential scan NOT running" in o[1] for o in outs),
              "SILENT: gitleaks missing was not reported on every hook run")
        events = os.path.join(r14, ".soul", "events.jsonl")
        lines = open(events).read().splitlines() if os.path.exists(events) else []
        check(len(lines) == 1 and json.loads(lines[0])["type"] == "soul.secret_guard.unavailable",
              f"EVENT: expected one soul.secret_guard.unavailable event, found {len(lines)}")

        # 17. Soul System source repo: NAME-MAP names warn by REF id only and are never
        # printed — not in a path segment, a gitleaks File field, or the repo's own name.
        rs = make_repo(tmp, f"{MAPNAME.lower()}-src")
        write(rs, "findings/open/.keep", "")
        write(rs, "operations/CLAUDE.md", "contract\n")
        write(rs, "SYSTEM-VERSION.md", "2\n")
        nmap = ("| Token | Real identifier(s) | What |\n|---|---|---|\n"
                f"| REF-01 | `{MAPNAME}`, `qvx-old` (ids → `NEW-TOKEN`), `x` (→ `zundermark`) | test |\n")
        write(rs, "registry/NAME-MAP.md", nmap)
        write(rs, f"docs/{MAPNAME.lower()}-notes.md", f"about {MAPNAME.lower()}\n")
        write(rs, f"{MAPNAME}-cfg.py", KEYLINE + "\n")
        plain_git(rs, "add", "docs", f"{MAPNAME}-cfg.py")
        rc, out, _ = sh(E, rs, "git commit -qm d")
        check(rc != 0 and "NAME-MAP REF-01" in out and "BLOCKED" in out,
              f"MISS: the source-repo fixture did not warn and block: {out!r}")
        check(MAPNAME.lower() not in out.lower(), "LEAK: a NAME-MAP name was printed (path, File field or repo name)")
        check("[REF-01]" in out, "REDACT: the redacted segment does not carry its REF token")
        check("did not parse" not in out, "NOISE: a well-formed NAME-MAP reported unparsed rows")
        plain_git(rs, "reset", "-q")
        write(rs, "doc.md", "renamed to NEW-TOKEN\n")
        plain_git(rs, "add", "doc.md")
        rc, out, _ = sh(E, rs, "git commit -qm t")
        check("REF-01" not in out, "NOISE: a codename on the replacement side was treated as a name")
        write(rs, "doc.md", "zundermark\n")
        plain_git(rs, "add", "doc.md")
        rc, out, _ = sh(E, rs, "git commit -qm z")
        check("REF-01" in out, "MISS: a non-codename right of the arrow was skipped (must count as a name)")
        write(rs, "registry/NAME-MAP.md", nmap + "| ref 02 | `Veltrandor` | reshaped |\n")
        write(rs, "doc.md", "v2\n")
        plain_git(rs, "add", "doc.md")
        rc, out, _ = sh(E, rs, "git commit -qm r")
        check("1 table row(s) holding identifiers did not parse" in out,
              "SILENT: an unparsed NAME-MAP row dropped its names without saying so")

        # 18. Codex (D1): PreToolUse never rewrites or decides — notices only; SessionStart says
        # whether the owner's opt-in is present; the opt-in's variables do arm git.
        r18 = make_repo(tmp, "r18")
        write(r18, "cfg.py", KEYLINE + "\n")
        cmd = "git add . && git commit -m x"
        payload = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "cwd": r18, "session_id": "cx",
                   "turn_id": "t1", "tool_use_id": "call-1", "tool_input": {"command": cmd}}
        cenv = {**E.env(), "PLUGIN_DATA": E.data, "CODEX_HOME": E.codex_home}

        def codex(pl):
            r = subprocess.run([sys.executable, "-B", CODEX], input=json.dumps(pl),
                               capture_output=True, text=True, env=cenv)
            OUTPUTS.append(r.stdout + r.stderr)
            return [json.loads(ln) for ln in r.stdout.splitlines() if ln.strip()]

        outs = codex(payload)
        check(not any("updatedInput" in json.dumps(o) or "permissionDecision" in json.dumps(o) for o in outs),
              f"CODEX: PreToolUse rewrote or decided a command (D1): {outs!r}")
        outs = codex({**payload, "tool_input": {"command": "git commit --no-verify -m x"}})
        check(len(outs) == 1 and BYPASS in outs[0].get("systemMessage", ""), "CODEX: --no-verify drew no bypass notice")
        ss = {"hook_event_name": "SessionStart", "cwd": r18, "session_id": "cx"}
        ctx = (codex(ss) or [{}])[0].get("hookSpecificOutput", {}).get("additionalContext", "")
        check("NOT armed under Codex" in ctx and "shell_environment_policy" in ctx and E.stable in ctx,
              "CODEX: SessionStart did not say the guard is not armed and how to opt in")
        write(E.codex_home, "config.toml", sg.codex_opt_in(E.stable) + "\n")
        ctx = (codex(ss) or [{}])[0].get("hookSpecificOutput", {}).get("additionalContext", "")
        check("routes git hooks" in ctx and "NOT armed" not in ctx, "CODEX: the opt-in config was not recognised")
        before = head(r18)
        rr = subprocess.run([os.path.join(E.base, "sh"), "-c", cmd], cwd=r18, capture_output=True, text=True,
                            env=E.env(GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="core.hooksPath",
                                      GIT_CONFIG_VALUE_0=E.stable))
        OUTPUTS.append(rr.stdout + rr.stderr)
        check(rr.returncode != 0 and "BLOCKED" in rr.stderr and head(r18) == before,
              "CODEX: the opt-in's three variables did not arm git")
        plain_git(r18, "reset", "-q")

        # 19. gitleaks exits 0 when its own git call fails; the guard calls that an error.
        old_path = os.environ.get("PATH", "")
        os.environ["PATH"] = E.gl["real"] + os.pathsep + old_path
        try:
            check(sg.gitleaks(r18, log_opts="nonexistent..HEAD")[2], "SILENT: a gitleaks run over a bad range was taken as clean")
            check(not sg.gitleaks(r18)[2], "NOISE: a clean gitleaks run was reported as an error")
        finally:
            os.environ["PATH"] = old_path

        # 22. L2: `git am` of a patch carrying a credential is blocked (pre-applypatch).
        r22 = make_repo(tmp, "r22")
        plain_git(r22, "checkout", "-q", "-b", "p")
        write(r22, "cfg.py", KEYLINE + "\n")
        plain_git(r22, "add", "cfg.py")
        plain_git(r22, "commit", "-qm", "key patch")
        patch = plain_git(r22, "format-patch", "-1", "-o", tmp).stdout.strip()
        plain_git(r22, "checkout", "-q", "main")
        before = head(r22)
        rc, out, _ = sh(E, r22, f"git am -q '{patch}'")
        check(rc != 0 and "BLOCKED" in out and head(r22) == before, f"MISS: git am applied a credential patch: {out[-200:]!r}")
        subprocess.run(["git", "-C", r22, "am", "--abort"], capture_output=True, env=E.env())

        # 23. M2: a repo whose top is not a Soul project is checked when the session's own
        # folder lies inside it and is one — and only then.
        r23 = make_repo(tmp, "r23", soul=False)
        write(r23, "proj/witness.md", "# W\n")
        write(r23, "cfg.py", KEYLINE + "\n")
        plain_git(r23, "add", "cfg.py")
        rc, out, _ = sh(E, r23, f"export SOUL_GUARD_CWD='{os.path.join(r23, 'proj')}'\ngit commit -qm in")
        check(rc != 0 and "BLOCKED" in out, "SCOPE: the session's Soul folder inside a repo did not put the repo in scope")
        rc, out, _ = sh(E, r23, f"export SOUL_GUARD_CWD='{r1}'\ngit commit -qm out")
        check(rc == 0 and "Soul secret" not in out, "SCOPE: a session folder outside the repo put it in scope")

        # 23b. A Soul vault is in scope from a session in another folder: a credential is
        # blocked and a listed name warned, as in any repo of unknown visibility (I079).
        rv = make_repo(tmp, "rv", soul=False)
        write(rv, "vault.md", "\ufeff# My renamed vault\n")  # scoped on structure, not title
        write(rv, "projects/p/soul/w.md", f"met {NAME}\n")
        write(rv, "projects/p/soul/private-names.txt", "Somebody\n")
        plain_git(rv, "add", "-A")
        rc, out, _ = sh(E, rv, f"export SOUL_GUARD_CWD='{r1}'\ngit commit -qm name")
        check(rc == 0 and f'"{NAME}"' in out, f"VAULT: a private name in a Soul vault was not warned: rc={rc} {out[-300:]!r}")
        check("private-name list is staged" not in out and "projects/p/soul/private-names.txt" not in out,
              f"VAULT: a project's name list kept in the vault was flagged: {out[-300:]!r}")
        write(rv, "projects/p/soul/cfg.md", KEYLINE + "\n")
        plain_git(rv, "add", "-A")
        rc, out, _ = sh(E, rv, f"export SOUL_GUARD_CWD='{r1}'\ngit commit -qm cred")
        check(rc != 0 and "BLOCKED" in out, f"VAULT: a credential committed to a Soul vault was not blocked: {out[-200:]!r}")
        plain_git(rv, "reset", "-q", "--hard")

        # 24. --own-hooks-dir resolves a relative core.hooksPath against the worktree top (M2).
        os.makedirs(os.path.join(r8, "a", "b"))
        rc, own, _ = sh(E, os.path.join(r8, "a", "b"), f"python3 '{HOOK}' --own-hooks-dir")
        check(own.strip() == os.path.join(r8, ".myhooks"), f"OWN-DIR: relative core.hooksPath resolved to {own.strip()!r}")

        # 25. L3: a linked worktree of the source repo reads NAME-MAP from the main worktree; a
        # clone without it says NAME-MAP names are NOT checked.
        plain_git(rs, "reset", "-q")
        plain_git(rs, "add", "findings", "operations", "SYSTEM-VERSION.md")
        plain_git(rs, "commit", "-qm", "source layout")
        wt = os.path.join(tmp, "rs-wt")
        plain_git(rs, "worktree", "add", "-q", wt)
        write(wt, "w.md", f"about {MAPNAME.lower()}\n")
        plain_git(wt, "add", "w.md")
        rc, out, _ = sh(E, wt, "git commit -qm w")
        check("NAME-MAP REF-01" in out and MAPNAME.lower() not in out.lower(),
              f"NAME-MAP: a linked worktree did not read the main worktree's map: {out!r}")
        clone = os.path.join(tmp, "rs-clone")
        plain_git(tmp, "clone", "-q", rs, clone)
        plain_git(clone, "config", "user.email", "dev@example.com")
        plain_git(clone, "config", "user.name", "Dev")
        rc, out, _ = sh(E, clone, "git commit -q --allow-empty -m c")
        check("NAME-MAP names are NOT checked" in out, f"SILENT: a clone without NAME-MAP did not say so: {out!r}")

        # 26. L4: an old remote tip this repo has is excluded (batched cat-file) even when the
        # push names a URL, so an already-pushed credential does not block a clean push.
        r26 = make_repo(tmp, "r26")
        bare26 = os.path.join(tmp, "remote26.git")
        subprocess.run(["git", "init", "-q", "--bare", bare26], check=True)
        write(r26, "cfg.py", KEYLINE + "\n")
        plain_git(r26, "add", "cfg.py")
        plain_git(r26, "commit", "-qm", "old key, already public")
        plain_git(r26, "push", "-q", bare26, "main")
        plain_git(r26, "commit", "-q", "--allow-empty", "-m", "clean")
        rc, out, _ = sh(E, r26, f"git push -q '{bare26}' main")
        check(rc == 0 and "BLOCKED" not in out, f"RANGE: a URL push re-scanned commits already on the remote: {out!r}")
        # A long ref list is read in linear time (20000 deletion lines through the wrapper).
        lines = "".join(f"refs/heads/b{i} {'0' * 40} refs/heads/b{i} {'1' * 40}\n" for i in range(20000))
        t0 = time.monotonic()
        r = subprocess.run([os.path.join(E.stable, "pre-push"), "origin", bare26], input=lines, cwd=r26,
                           capture_output=True, text=True, env=E.env(), timeout=120)
        took = time.monotonic() - t0
        check(r.returncode == 0 and took < 15, f"STDIN: 20000 ref lines took {took:.1f}s through the pre-push wrapper")

        # 27. Ctrl-C / SIGTERM: the guard kills gitleaks' process group instead of leaving it running.
        write(r22, "cfg.py", KEYLINE + "\n")
        plain_git(r22, "add", "cfg.py")
        rm(E.pidfile)
        proc = subprocess.Popen([sys.executable, "-B", HOOK, "--git-hook", "pre-commit"], cwd=r22,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=E.env(gitleaks="slow"))
        for _ in range(100):
            if os.path.exists(E.pidfile) and slurp(E.pidfile).strip():
                break
            time.sleep(0.1)
        child = int(slurp(E.pidfile).strip() or 0)
        proc.send_signal(signal.SIGTERM)
        proc.wait(timeout=10)
        alive = True
        for _ in range(30):
            try:
                os.kill(child, 0)
                time.sleep(0.1)
            except ProcessLookupError:
                alive = False
                break
        check(child and not alive, "SIGNAL: gitleaks kept running after the guard was terminated")
        plain_git(r22, "reset", "-q")

        # 28. N1: credentials in messages. A -m message blocks at commit-msg; the owner's
        # message fingerprint clears it; a hand-made commit's message and an annotated tag's
        # message block at push. Never the value.
        r28 = make_repo(tmp, "r28")
        bare28 = os.path.join(tmp, "remote28.git")
        subprocess.run(["git", "init", "-q", "--bare", bare28], check=True)
        plain_git(r28, "config", "remote.origin.pushurl", bare28)
        plain_git(r28, "push", "-q", "origin", "main")
        before = head(r28)
        rc, out, _ = sh(E, r28, f"git commit -q --allow-empty -m 'deploy: use key {FAKE_AWS}'")
        check(rc != 0 and "BLOCKED" in out and "commit message" in out and head(r28) == before,
              f"MISS: a credential in a -m message was committed: {out!r}")
        fp = re.search(r"fingerprint (message:aws-access-token:[0-9a-f]{16})", out)
        check(fp is not None, f"MISS: a message finding carries no stable fingerprint: {out!r}")
        if fp:
            write(r28, ".gitleaksignore", fp.group(1) + "\n")
            rc, out, _ = sh(E, r28, f"git commit -q --allow-empty -m 'deploy: use key {FAKE_AWS}'")
            check(rc == 0 and ".gitleaksignore differs from HEAD" in out,
                  f"OVERRIDE: the owner's message fingerprint did not clear the finding: {out!r}")
            plain_git(r28, "reset", "-q", "--hard", before)
            rm(os.path.join(r28, ".gitleaksignore"))
        plain_git(r28, "commit", "-q", "--allow-empty", "-m", f"by hand: key {FAKE_AWS}")
        rc, out, _ = sh(E, r28, "git push origin main")
        check(rc != 0 and "BLOCKED" in out and "message" in out
              and plain_git(bare28, "rev-parse", "main").stdout.strip() == before,
              f"MISS: a credential in an outgoing commit message was pushed: {out!r}")
        plain_git(r28, "reset", "-q", "--hard", before)
        plain_git(r28, "tag", "-a", "v1", "-m", f"release key {FAKE_AWS}")
        rc, out, _ = sh(E, r28, "git push origin v1")
        check(rc != 0 and "BLOCKED" in out and "tag v1 message" in out
              and not plain_git(bare28, "tag", "--list").stdout.strip(),
              f"MISS: a credential in an annotated tag's message was pushed: {out!r}")
        plain_git(r28, "tag", "-d", "v1")
        plain_git(r28, "tag", "-a", "inner", "-m", f"inner key {FAKE_AWS}")
        plain_git(r28, "tag", "-a", "outer", "inner", "-m", "a clean outer tag")
        plain_git(r28, "tag", "-d", "inner")
        rc, out, _ = sh(E, r28, "git push origin outer")
        check(rc != 0 and "BLOCKED" in out and "tag inner message" in out
              and not plain_git(bare28, "tag", "--list").stdout.strip(),
              f"MISS: a credential in a tag that a pushed tag points at went through: {out!r}")
        plain_git(r28, "tag", "-d", "outer")
        # Fingerprints cover the whole finding: two different private keys, two ids; the
        # same key gives the same id at commit-msg and at pre-push.
        fps = []
        for seed in (1, 2):
            write(tmp, f"keymsg{seed}.txt", f"rotate deploy key\n\n{fake_private_key(seed)}\n")
            rc, out, _ = sh(E, r28, f"git commit -q --allow-empty -F '{os.path.join(tmp, f'keymsg{seed}.txt')}'")
            m = re.search(r"fingerprint (message:private-key:[0-9a-f]{16})", out)
            check(rc != 0 and m is not None, f"MISS: a private key in a message did not block: {out!r}")
            fps.append(m.group(1) if m else None)
        check(fps[0] and fps[1] and fps[0] != fps[1], f"FINGERPRINT: two different keys share an id: {fps!r}")
        plain_git(r28, "commit", "-q", "--allow-empty", "-F", os.path.join(tmp, "keymsg1.txt"))
        rc, out, _ = sh(E, r28, "git push origin main")
        m = re.search(r"fingerprint (message:private-key:[0-9a-f]{16})", out)
        check(rc != 0 and m is not None and m.group(1) == fps[0],
              f"FINGERPRINT: the same key gave another id at push than at commit: {out!r}")
        plain_git(r28, "reset", "-q", "--hard", before)

        # 29. N4/fix 4: a push by URL to origin's own URL uses origin's tracking refs; a URL
        # matching no configured remote is a first push (all history, first-push message).
        # A space in the path breaks neither.
        r29 = make_repo(tmp, "r29")
        origin29 = os.path.join(tmp, "space dir", "origin.git")
        os.makedirs(os.path.dirname(origin29))
        subprocess.run(["git", "init", "-q", "--bare", origin29], check=True)
        plain_git(r29, "remote", "set-url", "origin", origin29)
        write(r29, "old.py", KEYLINE + "\n")
        plain_git(r29, "add", "old.py")
        plain_git(r29, "commit", "-qm", "old key, already on origin")
        plain_git(r29, "push", "-q", "origin", "main")
        plain_git(r29, "checkout", "-q", "-b", "feat")
        plain_git(r29, "commit", "-q", "--allow-empty", "-m", "clean")
        rc, out, _ = sh(E, r29, f"git push -q '{origin29}' feat")
        check(rc == 0 and "BLOCKED" not in out and "FAILED" not in out,
              f"RANGE: a push to origin's own URL re-scanned origin's history, or failed on a space: {out!r}")
        clean_tip = head(r29)
        write(r29, "new.py", KEYLINE + "\n")
        plain_git(r29, "add", "new.py")
        plain_git(r29, "commit", "-qm", "new key")
        rc, out, _ = sh(E, r29, f"git push '{origin29}' feat")
        check(rc != 0 and "BLOCKED" in out and "FAILED" not in out
              and subprocess.run(["git", "-C", origin29, "rev-parse", "-q", "--verify", "feat"],
                                 capture_output=True, text=True).stdout.strip() == clean_tip,
              f"MISS: a URL push with a space in the path did not block a new credential: {out!r}")
        plain_git(r29, "reset", "-q", "--hard", clean_tip)
        unknown = os.path.join(tmp, "space dir", "mirror2.git")
        subprocess.run(["git", "init", "-q", "--bare", unknown], check=True)
        rc, out, _ = sh(E, r29, f"git push '{unknown}' feat")
        check(rc != 0 and "BLOCKED" in out and "First push to this remote" in out,
              f"FIRST-PUSH: a URL push to an unknown mirror skipped history already on origin: {out!r}")

        # 30. N5: a first push to a remote with no tracking refs checks all history and says so.
        mirror = os.path.join(tmp, "mirror.git")
        subprocess.run(["git", "init", "-q", "--bare", mirror], check=True)
        plain_git(r29, "remote", "add", "mirror", mirror)
        rc, out, _ = sh(E, r29, "git push mirror main")
        check(rc != 0 and "BLOCKED" in out and "First push to this remote" in out,
              f"FIRST-PUSH: a first push carrying an old credential was not explained: {out!r}")

        # 31. N3: two plugin copies (an update while another session stays open) keep
        # separate folders, so PreToolUse never flaps between them.
        copy = os.path.join(tmp, "plugin-copy")
        os.makedirs(os.path.join(copy, "hooks"))
        for f in ("secret-guard.py", "pre-completion-verify.py"):
            shutil.copy(os.path.join(_HERE, f), os.path.join(copy, "hooks", f))
        copy_hook = os.path.join(copy, "hooks", "secret-guard.py")

        def pretool_with(hook):
            r = subprocess.run([sys.executable, "-B", hook], capture_output=True, text=True, env=E.env(),
                               input=json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Bash", "cwd": r1,
                                                 "session_id": "s1", "tool_input": {"command": "ls"}}))
            OUTPUTS.append(r.stdout)
            return r.stdout.strip()

        pretool_with(copy_hook)                     # first install of the copy's own folder
        flaps = [pretool_with(h) for h in (HOOK, copy_hook, HOOK, copy_hook)]
        check(not any(flaps), f"FLAP: two plugin copies kept reinstalling each other's folder: {flaps!r}")

        # 32. A ref that names a blob or tree (directly, at the end of a tag chain, or a raw
        # object id) is NOT scanned and says so in one line — no content, no command. The tag
        # messages on the way are still scanned; a commit beside it is still checked; a
        # normal tag to a commit draws no such line.
        r32 = make_repo(tmp, "r32")
        bare32 = os.path.join(tmp, "remote32.git")
        subprocess.run(["git", "init", "-q", "--bare", bare32], check=True)
        plain_git(r32, "remote", "set-url", "origin", bare32)
        plain_git(r32, "push", "-q", "origin", "main")

        def obj(text):
            write(tmp, "obj32.txt", text)
            return plain_git(r32, "hash-object", "-w", os.path.join(tmp, "obj32.txt")).stdout.strip()

        def mktree(entries):
            return subprocess.run(["git", "-C", r32, "mktree"], text=True, capture_output=True, check=True,
                                  input="".join(f"{m} {t} {o}\t{n}\n" for m, t, o, n in entries)).stdout.strip()

        keyblob = obj("UNIQUE-BLOB-CONTENT-MARKER\n" + KEYLINE + "\n")
        tree = mktree([("100644", "blob", keyblob, "cfg.py")])
        nested = mktree([("040000", "tree", tree, "deep")])
        p12 = mktree([("100644", "blob", obj("UNIQUE-BLOB-CONTENT-MARKER binary-ish\n"), "cert.p12")])
        evil = "a'$(cat>PWNED</dev/null)'b"
        plain_git(r32, "tag", "-a", "ab", keyblob, "-m", "clean")
        plain_git(r32, "tag", "lb", keyblob)
        plain_git(r32, "tag", "-a", "at", tree, "-m", "clean")
        plain_git(r32, "tag", "lt", tree)
        plain_git(r32, "tag", "nt", nested)
        plain_git(r32, "tag", "-a", "inner32", keyblob, "-m", "clean")
        plain_git(r32, "tag", "-a", "chain", "inner32", "-m", "clean")
        plain_git(r32, "tag", "-d", "inner32")
        plain_git(r32, "tag", "pk", p12)
        plain_git(r32, "tag", evil, keyblob)
        cases = [(f"refs/tags/{t}", f"refs/tags/{t}", k) for t, k in
                 (("ab", "blob"), ("lb", "blob"), ("at", "tree"), ("lt", "tree"), ("nt", "tree"),
                  ("chain", "blob"), ("pk", "tree"), (evil, "blob"))]
        cases.append((f"{keyblob}:refs/heads/x", f"object {keyblob} -> refs/heads/x", "blob"))
        for spec, label, kind in cases:
            rc, out, _ = sh(E, r32, f"git push -q origin {shlex.quote(spec)}")
            check(f"NOT checked — {label} points at a {kind}; only commits and tag messages are scanned "
                  "on push. Do not push it until its content has been checked." in out,
                  f"SILENT: a pushed {kind} ({label!r}) passed without its NOT checked line: {out!r}")
            check("UNIQUE-BLOB-CONTENT-MARKER" not in out and "aws_access_key_id" not in out
                  and "cfg.py" not in out and "cert.p12" not in out and "gitleaks stdin" not in out,
                  f"LEAK: the blob/tree notice printed content or a command ({label!r}): {out!r}")
        found = [os.path.join(d, f) for d, _, fs in os.walk(tmp) for f in fs if f == "PWNED"]
        check(not found, f"INJECTION: a crafted tag name ran a command: {found!r}")
        check(sg._printable("refs/tags/a\nb") == "refs/tags/a\\x0ab",
              "NOTICE: a control character in a ref would split the NOT checked line")
        # An annotated tag to a blob whose MESSAGE holds a key still blocks.
        plain_git(r32, "tag", "-a", "mk", keyblob, "-m", f"release key {FAKE_AWS}")
        rc, out, _ = sh(E, r32, "git push origin mk")
        check(rc != 0 and "BLOCKED" in out and "tag mk message" in out,
              f"MISS: a key in the message of a tag to a blob went through: {out!r}")
        # A normal tag to a commit draws no NOT checked line.
        plain_git(r32, "tag", "-a", "rel", "main", "-m", "a release")
        rc, out, _ = sh(E, r32, "git push -q origin rel")
        check(rc == 0 and "NOT checked" not in out, f"NOISE: a tag to a commit drew a NOT checked line: {out!r}")
        # A credential commit pushed beside a blob tag is still checked.
        write(r32, "cfg.py", KEYLINE + "\n")
        plain_git(r32, "add", "cfg.py")
        plain_git(r32, "commit", "-qm", "key beside a blob tag")
        plain_git(r32, "tag", "lb2", keyblob)
        rc, out, _ = sh(E, r32, "git push origin main lb2")
        check(rc != 0 and "BLOCKED" in out and "cfg.py:1 (commit" in out and "refs/tags/lb2 points at a blob" in out,
              f"MISS: a commit pushed alongside a blob tag went unchecked: {out!r}")
        plain_git(r32, "reset", "-q", "--hard", "HEAD~1")

        # 33. Sixth review fix 2: a remote whose pushurl differs from its url, or a URL that
        # matches only a pushurl, is a first push — the url's tracking refs say nothing
        # about the pushurl. The fetch url itself still uses them.
        r33 = make_repo(tmp, "r33")
        old33 = os.path.join(tmp, "tri-old.git")
        new33 = os.path.join(tmp, "tri-new.git")
        for b in (old33, new33):
            subprocess.run(["git", "init", "-q", "--bare", b], check=True)
        write(r33, "old.py", KEYLINE + "\n")
        plain_git(r33, "add", "old.py")
        plain_git(r33, "commit", "-qm", "old key")
        plain_git(r33, "remote", "add", "tri", old33)
        plain_git(r33, "push", "-q", "tri", "main")
        plain_git(r33, "fetch", "-q", "tri")
        plain_git(r33, "config", "remote.tri.pushurl", new33)
        plain_git(r33, "checkout", "-q", "-b", "nb")
        plain_git(r33, "commit", "-q", "--allow-empty", "-m", "clean")
        rc, out, _ = sh(E, r33, "git push tri nb")
        check(rc != 0 and "BLOCKED" in out and "First push to this remote" in out,
              f"PUSHURL: a push to a pushurl other than the url trusted the url's tracking refs: {out!r}")
        rc, out, _ = sh(E, r33, f"git push '{new33}' nb")
        check(rc != 0 and "BLOCKED" in out and "First push to this remote" in out,
              f"PUSHURL: a by-URL push matching only a pushurl trusted that remote's refs: {out!r}")
        rc, out, _ = sh(E, r33, f"git push -q '{old33}' nb")
        check(rc == 0 and "BLOCKED" not in out, f"PUSHURL: a by-URL push to the fetch url ignored its refs: {out!r}")

        def remote33(name, urls, pushurls=()):
            plain_git(r33, "remote", "add", name, urls[0])
            for u in urls[1:]:
                plain_git(r33, "config", "--add", f"remote.{name}.url", u)
            for u in pushurls:
                plain_git(r33, "config", "--add", f"remote.{name}.pushurl", u)
            plain_git(r33, "fetch", "-q", name)

        def branch33(b):
            plain_git(r33, "checkout", "-q", "-b", b, "nb")
            plain_git(r33, "commit", "-q", "--allow-empty", "-m", f"clean {b}")

        extra = os.path.join(tmp, "tri-extra.git")
        extra2 = os.path.join(tmp, "tri-extra2.git")
        for b in (extra, extra2):
            subprocess.run(["git", "init", "-q", "--bare", b], check=True)
        # pushurl == url: the tracking refs describe the push target.
        remote33("same", [old33], [old33])
        branch33("nb-same")
        rc, out, _ = sh(E, r33, "git push -q same nb-same")
        check(rc == 0 and "BLOCKED" not in out, f"PUSHURL: pushurl == url did not use the tracking refs: {out!r}")
        # Two pushurls (one of them elsewhere): a first push.
        remote33("twop", [old33], [old33, extra])
        branch33("nb-twop")
        rc, out, _ = sh(E, r33, "git push twop nb-twop")
        check(rc != 0 and "BLOCKED" in out and "First push to this remote" in out,
              f"PUSHURL: two pushurls trusted the fetch url's refs: {out!r}")
        # Several urls: git fetches from the first and pushes to all — a first push by name,
        # and a by-URL push to a later url is one too.
        remote33("multi", [old33, extra2])
        branch33("nb-multi")
        rc, out, _ = sh(E, r33, "git push multi nb-multi")
        check(rc != 0 and "BLOCKED" in out and "First push to this remote" in out,
              f"MULTI-URL: a remote with several urls trusted its tracking refs (by name): {out!r}")
        rc, out, _ = sh(E, r33, f"git push '{extra2}' nb-multi")
        check(rc != 0 and "BLOCKED" in out and "First push to this remote" in out,
              f"MULTI-URL: a by-URL push to a remote's second url trusted its tracking refs: {out!r}")

        # 34. A tag chain deeper than 10 says NOT checked.
        plain_git(r32, "tag", "-a", "d0", "main", "-m", "d0")
        for i in range(1, 12):
            plain_git(r32, "tag", "-a", f"d{i}", f"d{i - 1}", "-m", f"d{i}")
        rc, out, _ = sh(E, r32, "git push -q origin d11")
        check("nests more than 10 tags deep" in out and "NOT checked" in out,
              f"SILENT: a tag chain deeper than 10 was not reported: {out!r}")

        # 35. A pre-push input over 64 KB (600 refs) reaches the repo's own hook byte-identical.
        r35 = make_repo(tmp, "r35")
        subprocess.run(["git", "-C", r35, "update-ref", "--stdin"], check=True, text=True, capture_output=True,
                       input="".join(f"create refs/heads/branch-{i:04d}-padding-to-make-it-long {head(r35)}\n"
                                     for i in range(600)),
                       env={**os.environ, "GIT_CONFIG_GLOBAL": os.devnull})
        got = os.path.join(tmp, "prepush-input.txt")
        write(os.path.join(r35, ".git", "hooks"), "pre-push", f'#!/bin/sh\ncat >> "{got}"\n')
        os.chmod(os.path.join(r35, ".git", "hooks", "pre-push"), 0o755)
        a35, b35 = os.path.join(tmp, "r35-a.git"), os.path.join(tmp, "r35-b.git")
        for b in (a35, b35):
            subprocess.run(["git", "init", "-q", "--bare", b], check=True)
        plain_git(r35, "push", "-q", a35, "refs/heads/*:refs/heads/*")
        direct = slurp(got)
        rm(got)
        rc, out, _ = sh(E, r35, f"git push -q '{b35}' 'refs/heads/*:refs/heads/*'")
        via = slurp(got)
        check(rc == 0 and len(direct) > 65536 and via == direct,
              f"STDIN: the chained pre-push got {len(via)} bytes, git gives {len(direct)} directly")

        # 36. Real git-lfs (skipped when absent): an LFS object uploads through the chained
        # pre-push to a local bare remote.
        if shutil.which("git-lfs"):
            r36 = make_repo(tmp, "r36")
            plain_git(r36, "lfs", "install", "--local")
            plain_git(r36, "lfs", "track", "*.bin")
            write(r36, "d.bin", "lfs payload for the fence\n")
            plain_git(r36, "add", ".gitattributes", "d.bin")
            plain_git(r36, "commit", "-qm", "lfs object")
            bare36 = os.path.join(tmp, "remote36.git")
            subprocess.run(["git", "init", "-q", "--bare", bare36], check=True)
            plain_git(r36, "remote", "set-url", "origin", bare36)
            rc, out, _ = sh(E, r36, "git push -q origin main")
            uploaded = [f for _, _, fs in os.walk(os.path.join(bare36, "lfs")) for f in fs]
            check(rc == 0 and len(uploaded) == 1, f"LFS: the chained git-lfs pre-push uploaded {uploaded!r}: {out!r}")
        else:
            print("SKIP  git-lfs not installed — the real-lfs case did not run")

        # 20. /soul-init's hand-commit hooks: block without a session, fail open loudly when the
        # plugin is gone, and do not run twice when the session's wrapper chains to them.
        skill = open(SKILL, encoding="utf-8").read()
        block = re.search(r"```sh\n( *#!/bin/sh\n *# Soul System secret check.*?)\n *```", skill, re.S)
        check(block is not None, "MISS: /soul-init no longer carries the hand-commit hook text")
        if block:
            body = textwrap.dedent(block.group(1)) + "\n"
            r20 = make_repo(tmp, "r20")
            rc, own, _ = sh(E, r20, f"python3 '{HOOK}' --own-hooks-dir")
            own = own.strip()
            check(own == os.path.join(r20, ".git", "hooks"),
                  f"OWN-DIR: --own-hooks-dir answered {own!r}, not the repo's own hooks dir")

            def install_hand(root):
                for hk in ("pre-commit", "commit-msg", "pre-push"):
                    p = os.path.join(r20, ".git", "hooks", hk)
                    write(os.path.dirname(p), hk, body.replace("<derived-root>", root).replace("<hook>", hk))
                    os.chmod(p, 0o755)

            install_hand(os.path.dirname(_HERE))
            write(r20, "cfg.py", KEYLINE + "\n")
            plain_git(r20, "add", "cfg.py")
            res = subprocess.run(["git", "-C", r20, "commit", "-qm", "hand"], capture_output=True, text=True,
                                 env=E.env())
            OUTPUTS.append(res.stdout + res.stderr)
            check(res.returncode != 0 and "BLOCKED" in res.stderr, "MISS: the hand-commit hook did not block a credential")
            res = subprocess.run(["git", "-C", r20, "commit", "-qm", "hand"], capture_output=True, text=True,
                                 env=E.env(SOUL_GUARD_ACTIVE=f"pre-commit:{os.path.realpath(r20)}:1"))
            OUTPUTS.append(res.stdout + res.stderr)
            check(res.returncode != 0 and "BLOCKED" in res.stderr,
                  "BYPASS: a forged marker (another process ID) made the hand hook skip the check")
            plain_git(r20, "reset", "-q")
            write(r20, "n.md", f"for {NAME}\n")
            plain_git(r20, "add", "n.md")
            rc, out, _ = sh(E, r20, "git commit -qm once")
            check(rc == 0 and out.count("private names in what this") == 1,
                  f"DOUBLE: the session wrapper and the hand hook both ran the check: {out!r}")
            install_hand(os.path.join(tmp, "gone"))
            plain_git(r20, "add", "cfg.py")
            res = subprocess.run(["git", "-C", r20, "commit", "-qm", "hand"], capture_output=True, text=True,
                                 env=E.env())
            OUTPUTS.append(res.stdout + res.stderr)
            check(res.returncode == 0 and "NOT running" in res.stderr and "/soul-init" in res.stderr,
                  "SILENT: a hand hook with a missing plugin path did not fail open loudly")
            install_hand(os.path.dirname(_HERE))
            plain_git(r20, "reset", "-q")

            # Fix 1: a session armed from a plugin copy that was then deleted — the wrapper
            # says "plugin path missing", and the live hand hook it chains to must check.
            doomed = os.path.join(tmp, "doomed-copy")
            os.makedirs(os.path.join(doomed, "hooks"))
            for f in ("secret-guard.py", "pre-completion-verify.py"):
                shutil.copy(os.path.join(_HERE, f), os.path.join(doomed, "hooks", f))
            doomed_env = os.path.join(tmp, "doomed-env.sh")
            r = subprocess.run([sys.executable, "-B", os.path.join(doomed, "hooks", "secret-guard.py"),
                                "--session-start"], capture_output=True, text=True,
                               input=json.dumps({"hook_event_name": "SessionStart", "cwd": r20, "session_id": "d"}),
                               env=E.env(CLAUDE_ENV_FILE=doomed_env))
            OUTPUTS.append(r.stdout)
            shutil.rmtree(doomed)
            write(r20, "cfg9.py", KEYLINE + "\n")
            plain_git(r20, "add", "cfg9.py")
            before = head(r20)
            rc, out, _ = sh(E, r20, "git commit -qm doomed", envfile=doomed_env)
            check(MISSING in out and rc != 0 and "BLOCKED" in out and head(r20) == before,
                  f"MARKER: with the wrapper's plugin copy gone, the hand hook skipped its check: {out!r}")

            # Fix 3: forged markers with hand hooks only (no session): `exec git` and
            # `bash -c` give git the shell's PID; only the hook's PARENT may match.
            forged = [("sh", "SOUL_GUARD_ACTIVE=\"pre-commit:$(pwd -P):$$\"; export SOUL_GUARD_ACTIVE; exec git commit -qm f"),
                      ("bash", "bash -c 'SOUL_GUARD_ACTIVE=\"pre-commit:$(pwd -P):$$\" exec git commit -qm f'")]
            for shell, cmd in forged:
                res = subprocess.run([os.path.join(E.base, shell), "-c", cmd], cwd=r20, capture_output=True,
                                     text=True, env=E.env())
                OUTPUTS.append(res.stdout + res.stderr)
                check(res.returncode != 0 and "BLOCKED" in res.stderr and head(r20) == before,
                      f"MARKER: a forged marker ({shell}, exec git) skipped the hand hook's check: {res.stderr!r}")
            plain_git(r20, "reset", "-q")
            rm(os.path.join(r20, "cfg9.py"))
            bare20 = os.path.join(tmp, "remote20.git")
            subprocess.run(["git", "init", "-q", "--bare", bare20], check=True)
            plain_git(r20, "remote", "set-url", "origin", bare20)
            plain_git(r20, "push", "-q", "--no-verify", "origin", "main")
            plain_git(r20, "commit", "-q", "--no-verify", "--allow-empty", "-m", f"by hand: key {FAKE_AWS}")
            res = subprocess.run([os.path.join(E.base, "sh"), "-c",
                                  "SOUL_GUARD_ACTIVE=\"pre-push:$(pwd -P):$$\"; export SOUL_GUARD_ACTIVE; "
                                  "exec git push -q origin main"], cwd=r20, capture_output=True, text=True, env=E.env())
            OUTPUTS.append(res.stdout + res.stderr)
            check(res.returncode != 0 and "BLOCKED" in res.stderr
                  and plain_git(bare20, "rev-parse", "main").stdout.strip() == before,
                  f"MARKER: a forged pre-push marker (exec git) skipped the hand hook's check: {res.stderr!r}")
            plain_git(r20, "reset", "-q", "--hard", before)
            # A session's pre-push wrapper execs the hand pre-push: one check, not two.
            plain_git(r20, "commit", "-q", "--no-verify", "--allow-empty", "-m", f"note for {NAME}")
            rc, out, _ = sh(E, r20, "git push -q origin main")
            check(rc == 0 and out.count("private names in what this") == 1,
                  f"DOUBLE: the pre-push wrapper and the hand pre-push both ran the check: {out!r}")

    # 21. No secret value in any output; this file carries no detectable credential.
    joined = "\n".join(OUTPUTS)
    check(FAKE_AWS not in joined and "AK" + "IA" not in joined, "LEAK: a secret value appeared in hook output")
    # One path per run: `gitleaks dir` takes a single [path]. Given two, it did not scan
    # just those files — it ran for minutes from /tmp and failed in folders holding fake
    # keys (observed 2026-10-20) — so the old two-path check proved nothing about them.
    for path in (os.path.abspath(__file__), HOOK):
        scan = subprocess.run([GITLEAKS, "dir", "--no-banner", "--redact", "-l", "error", path],
                              capture_output=True, text=True, cwd=os.path.dirname(path))
        check(scan.returncode == 0, f"SELF: gitleaks flags {os.path.basename(path)}")

    if failures:
        for f in failures:
            print(f"FAIL  {f}")
        print(f"{passed[0]}/{passed[0] + len(failures)} passed")
        sys.exit(1)
    print(f"PASS  {passed[0]}/{passed[0]} — git runs the check (escapes, aliases, scripts, GIT_DIR, "
          "same-command files, push incl. new branch and globs block); repo hooks chain with args, "
          "input and exit status; names warn only, public repos only; NAME-MAP names never printed; "
          "every unchecked path says NOT checked")


if __name__ == "__main__":
    main()
