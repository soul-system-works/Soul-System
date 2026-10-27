"""Behaviour test for tools/confine.py (SOUL-I080; the 2026-10-27 review of v3.7.0).

FENCE: a check runs code a worker wrote, so it must not run with the host's powers.
`clean_env` passes only the allowlisted variables (PATH, HOME, USER, LOGNAME, LANG,
LC_*, TERM, TMPDIR, SHELL, OLLAMA_HOST) plus what the caller names — never the
host session's socket, token, session id, API keys or git config. `confine_argv`
wraps a command in bubblewrap with only the work folder and a private /tmp
writable, no network, and every existing secret folder (and the registered vault)
hidden; where it cannot confine it returns None, never a bare command.

The argv cases use an injected `which`, so they need no bubblewrap. When `bwrap` is
on this machine, one real case runs a check that tries to write outside its folder,
reach a listener on the host's loopback, and read a sentinel in a hidden secret
folder — each must fail confined and succeed unconfined (the control, so a pass is
not vacuous) — and to write inside, which must succeed. Its folders live under
/var/tmp, not /tmp, so the private /tmp alone cannot make the secret-folder case pass.

Run: python3 tools/test_confine.py  (exit 0 = PASS)
"""

import importlib.util
import os
import shutil
import socket
import subprocess
import sys
import tempfile

_TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "confine.py")
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else "  — " + str(detail)[:1500]))
    if not ok:
        FAILS.append(name)


def load():
    spec = importlib.util.spec_from_file_location("confine", _TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Env:
    """Swap os.environ for the duration of a block."""

    def __init__(self, env):
        self.env = env

    def __enter__(self):
        self.saved = dict(os.environ)
        os.environ.clear()
        os.environ.update(self.env)

    def __exit__(self, *exc):
        os.environ.clear()
        os.environ.update(self.saved)


def opt(argv, flag):
    """Every value that follows `flag` in argv."""
    return [argv[i + 1] for i, a in enumerate(argv[:-1]) if a == flag]


def main():
    c = load()
    tmp = tempfile.mkdtemp(prefix="soul-confine-test-")
    home = os.path.join(tmp, "home")
    for d in (".ssh", ".claude", ".config/gh"):
        os.makedirs(os.path.join(home, d))

    # 1 — clean_env keeps the allowlist and drops the host's powers
    host = {"PATH": "/usr/bin:/bin", "HOME": home, "USER": "u", "LOGNAME": "u",
            "LANG": "C.UTF-8", "LC_ALL": "C", "LC_CTYPE": "C", "TERM": "xterm",
            "TMPDIR": "/tmp", "SHELL": "/bin/sh", "OLLAMA_HOST": "127.0.0.1:11434",
            "CLAUDE_CODE_MESSAGING_SOCKET": "/s", "CLAUDE_CODE_MESSAGING_TOKEN": "t",
            "CLAUDE_CODE_SESSION_ID": "sid", "GH_TOKEN": "gh", "OPENAI_API_KEY": "sk",
            "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "core.x", "SOUL_GUARD_CWD": "/",
            "CODEX_COMPANION_SESSION_ID": "x", "ANTHROPIC_API_KEY": "sk-ant",
            "ANTHROPIC_BASE_URL": "http://h", "CLAUDE_CODE_USE_BEDROCK": "1",
            "DBUS_SESSION_BUS_ADDRESS": "unix:x"}
    with Env(host):
        env = c.clean_env()
        env2 = c.clean_env({"ANTHROPIC_API_KEY": ""})
    keep = {"PATH", "HOME", "USER", "LOGNAME", "LANG", "LC_ALL", "LC_CTYPE", "TERM",
            "TMPDIR", "SHELL", "OLLAMA_HOST"}
    check("clean_env: exactly the allowlist (LC_* included)", set(env) == keep,
          sorted(set(env) ^ keep))
    check("clean_env: values kept as they were", all(env[k] == host[k] for k in keep), env)
    check("clean_env: extra is added on top", env2.get("ANTHROPIC_API_KEY") == ""
          and set(env2) == keep | {"ANTHROPIC_API_KEY"}, env2)

    # 2 — confine_argv: None where it cannot confine, never a bare command
    with Env({"HOME": home, "PATH": "/usr/bin"}):
        check("confine_argv: None off Linux",
              c.confine_argv(["true"], tmp, which=lambda n: "/x/bwrap", platform="darwin") is None)
        check("confine_argv: None with no bwrap on PATH",
              c.confine_argv(["true"], tmp, which=lambda n: None, platform="linux") is None)

    # 3 — the bubblewrap argv: read-only root, private /tmp, only the work folder
    # writable, no network, its own session, secret folders hidden, then the command
    work = os.path.join(tmp, "work")
    os.makedirs(work)
    vault = os.path.join(tmp, "vault")
    os.makedirs(vault)
    os.makedirs(os.path.join(home, ".config", "soul"), exist_ok=True)
    with open(os.path.join(home, ".config", "soul", "vault"), "w") as f:
        f.write(vault + "\n")
    with Env({"HOME": home, "PATH": "/usr/bin"}):
        argv = c.confine_argv(["/bin/sh", "-c", "make test"], work,
                              which=lambda n: "/x/bwrap", platform="linux")
    argv = argv or []
    rw = os.path.realpath(work)
    check("confine_argv: bwrap first, the command last, untouched",
          argv[:1] == ["/x/bwrap"] and argv[-3:] == ["/bin/sh", "-c", "make test"], argv)
    check("confine_argv: / read-only, /dev, /proc, a private /tmp",
          argv[1:4] == ["--ro-bind", "/", "/"] and opt(argv, "--dev") == ["/dev"]
          and opt(argv, "--proc") == ["/proc"] and "/tmp" in opt(argv, "--tmpfs"), argv)
    i = argv.index("--bind") if "--bind" in argv else -1
    check("confine_argv: only the work folder bound writable, and run there",
          argv.count("--bind") == 1 and argv[i + 1:i + 3] == [rw, rw]
          and opt(argv, "--chdir") == [rw], argv)
    check("confine_argv: no network, dies with its parent, own session",
          all(f in argv for f in ("--unshare-net", "--die-with-parent", "--new-session")), argv)
    hidden = opt(argv, "--tmpfs")
    want = [os.path.realpath(os.path.join(home, d)) for d in (".ssh", ".claude", ".config/gh")]
    check("confine_argv: every existing secret folder hidden, as real paths",
          all(p in hidden for p in want), hidden)
    check("confine_argv: the registered vault hidden too", os.path.realpath(vault) in hidden,
          hidden)
    check("confine_argv: a secret folder that does not exist is not mounted",
          os.path.realpath(os.path.join(home, ".aws")) not in hidden, hidden)
    check("confine_argv: the secret folders come after the work folder's bind",
          all(argv.index(p) > i for p in want), argv)

    shutil.rmtree(tmp, ignore_errors=True)

    # 4 — real confinement, when bubblewrap is here
    if not (sys.platform.startswith("linux") and shutil.which("bwrap")):
        print("SKIP real confinement: no bwrap on this machine (or not Linux)")
    else:
        real_case(c)

    print("\n{} failure(s)".format(len(FAILS)) if FAILS else "\nALL PASS")
    return 1 if FAILS else 0


PROBE = r'''
import os, socket, sys
what, arg = sys.argv[1], sys.argv[2]
try:
    if what == "write":
        open(arg, "w").write("x\n")
    elif what == "read":
        open(arg).read()
    elif what == "net":
        s = socket.create_connection(("127.0.0.1", int(arg)), timeout=3)
        s.close()
except Exception as e:
    print(type(e).__name__, e)
    sys.exit(1)
print("OK")
'''


def real_case(c):
    base = "/var/tmp" if os.access("/var/tmp", os.W_OK) else None
    tmp = tempfile.mkdtemp(prefix="soul-confine-real-", dir=base)
    if base is None:
        print("NOTE /var/tmp not writable: the secret-folder case may pass on /tmp alone")
    home = os.path.join(tmp, "home")
    work = os.path.join(tmp, "work")
    os.makedirs(os.path.join(home, ".ssh"))
    os.makedirs(work)
    sentinel = os.path.join(home, ".ssh", "id_sentinel")
    with open(sentinel, "w") as f:
        f.write("SECRET-SENTINEL\n")
    probe = os.path.join(work, "probe.py")
    with open(probe, "w") as f:
        f.write(PROBE)
    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    listener.listen(8)
    port = str(listener.getsockname()[1])
    cases = [("write inside", "write", os.path.join(work, "in.txt"), True),
             ("write outside", "write", os.path.join(tmp, "outside.txt"), False),
             ("reach the host's loopback", "net", port, False),
             ("read a hidden secret folder", "read", sentinel, False)]
    try:
        with Env(dict(os.environ, HOME=home)):
            env = c.clean_env()
            for name, what, arg, confined_ok in cases:
                cmd = [sys.executable, probe, what, arg]
                free = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True,
                                      timeout=30)
                for p in (os.path.join(tmp, "outside.txt"),):
                    if os.path.exists(p):
                        os.remove(p)
                argv = c.confine_argv(cmd, work)
                boxed = subprocess.run(argv, cwd=work, env=env, capture_output=True, text=True,
                                       timeout=30)
                got_ok = boxed.returncode == 0
                if confined_ok:
                    check("real bwrap: " + name + " succeeds", got_ok,
                          boxed.stdout + boxed.stderr)
                else:
                    check("real bwrap: " + name + " works unconfined (control)",
                          free.returncode == 0, free.stdout + free.stderr)
                    check("real bwrap: " + name + " fails confined", not got_ok
                          and "SECRET" not in boxed.stdout, boxed.stdout + boxed.stderr)
            run_user = "/run/user/{}".format(os.getuid())
            if os.path.isdir(run_user) and os.listdir(run_user):
                seen = subprocess.run(c.confine_argv(["/bin/ls", "-A", run_user], work),
                                      cwd=work, env=env, capture_output=True, text=True,
                                      timeout=30)
                check("real bwrap: the session socket folder ({}) is empty inside"
                      .format(run_user), seen.returncode == 0 and not seen.stdout.strip(),
                      seen.stdout + seen.stderr)
            check("real bwrap: nothing written outside the work folder",
                  not os.path.exists(os.path.join(tmp, "outside.txt")))
    finally:
        listener.close()
        shutil.rmtree(tmp, ignore_errors=True)


def test_fence():
    assert main() == 0


if __name__ == "__main__":
    sys.exit(main())
