#!/usr/bin/env python3
"""Run worker-written code with less of the host in reach (SOUL-I080).

A /soul-workflow check runs code a worker wrote — its tests, its build — so the host
must not run it with the host's own powers. Two helpers, stdlib only:

  clean_env(extra=None)        an allowlisted environment: nothing the host session
                               holds (messaging socket and token, session id, API
                               keys, GH_TOKEN, GIT_CONFIG_*, SOUL_GUARD_*, routing)
                               reaches the child unless named in `extra`
  confine_argv(argv, workdir, project=None)
                               argv wrapped in bubblewrap: the whole filesystem
                               read-only except `workdir` (its .git and .soul kept
                               read-only) and a private /tmp, no network, the
                               secret folders hidden; None when it
                               cannot confine (not Linux, or no `bwrap` on PATH)

The 2026-10-27 fresh-context review of v3.7.0 found the selection check in
dispatch.py running a worker's code with the host's full environment and no
confinement — the worker itself was sandboxed, the check that ran its code was not.

SECRET_DIRS is the one list of folders a worker or a check may not read; dispatch.py
spells it as Claude Code permission rules, this module as real paths to hide.
"""

import importlib.util
import os
import shutil
import sys

ENV_KEEP = ("PATH", "HOME", "USER", "LOGNAME", "LANG", "TERM", "TMPDIR", "SHELL",
            "OLLAMA_HOST")
SECRET_DIRS = (".ssh", ".gnupg", ".aws", ".config/gh", ".claude", ".codex", ".config/soul")
_HERE = os.path.dirname(os.path.abspath(__file__))


def clean_env(extra=None):
    """The allowlisted environment: ENV_KEEP and LC_* from this process, plus `extra`."""
    env = {k: v for k, v in os.environ.items() if k in ENV_KEEP or k.startswith("LC_")}
    env.update(extra or {})
    return env


def _vault_tool():
    """tools/vault.py, loaded by path, not by `import vault`: a caller loaded through
    importlib has no tools/ on sys.path, and a failed import here would silently leave
    the vault readable. Raises when it cannot load."""
    spec = importlib.util.spec_from_file_location("soul_vault",
                                                  os.path.join(_HERE, "vault.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def registered_vault():
    """The vault folder this machine registered (tools/vault.py), or None."""
    try:
        v = _vault_tool().registered_vault()
    except Exception:
        return None
    return os.path.realpath(os.path.expanduser(v)) if v else None


def linked_vaults(workdir):
    """The vaults that a `.soul` link in `workdir`, or in any folder above it, points
    into, as real paths. A project may link to a vault that is not the registered one,
    and that vault holds other projects' records too (SOUL-I092). Folders above count
    because dispatch's worktrees sit in <project>/.ai/worktrees/, and git keeps the
    .soul link out of a worktree."""
    try:
        tool = _vault_tool()
    except Exception:
        return []
    out, d = [], os.path.realpath(workdir)
    while True:
        v = tool.linked_vault(d)
        if v and os.path.realpath(v) not in out:
            out.append(os.path.realpath(v))
        parent = os.path.dirname(d)
        if parent == d:
            return out
        d = parent


def secret_paths(workdir=None, project=None):
    """SECRET_DIRS under this HOME, the registered vault and the vaults the .soul links
    of the work folder, and of the project when the caller knows it, point into — as
    real paths. The project counts on its own: a work folder outside it (a review's
    --workdir) has no link above it, and walking from there alone left the project's
    vault readable (the review of v3.13.0)."""
    home = os.path.expanduser("~")
    out = [os.path.realpath(os.path.join(home, d)) for d in SECRET_DIRS]
    linked = []
    for start in (workdir, project):
        if start:
            linked += linked_vaults(start)
    for v in [registered_vault()] + linked:
        if v and v not in out:
            out.append(v)
    return out


def confine_argv(argv, workdir, which=shutil.which, platform=None, project=None):
    """`argv` under bubblewrap with only `workdir` (and a fresh /tmp) writable, no
    network, and every existing secret folder covered by an empty tmpfs (`project`,
    when given, adds the vault its .soul links into: secret_paths). None when it
    cannot confine: the caller decides whether to skip or refuse, never to run the
    check bare in its place."""
    if not (platform or sys.platform).startswith("linux"):
        return None
    bwrap = which("bwrap")
    if not bwrap:
        return None
    workdir = os.path.realpath(workdir)
    cmd = [bwrap, "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
           "--tmpfs", "/tmp", "--bind", workdir, workdir, "--unshare-net",
           "--die-with-parent", "--new-session", "--chdir", workdir]
    # The work folder's own .git and .soul stay read-only: accept's spot check runs in
    # the host's checkout, and a check with write access there could plant
    # .git/hooks/*, edit .git/config or write the Soul record (the 2026-10-28 review
    # of v3.8.0). In a worktree .git is a file, and its admin folder is read-only
    # under `/` already. A symlink is bound at its target when that lies inside the
    # work folder; a target outside it is read-only already.
    for name in (".git", ".soul"):
        target = os.path.realpath(os.path.join(workdir, name))
        if target.startswith(workdir + os.sep) and os.path.exists(target):
            cmd += ["--ro-bind", target, target]
    for d in secret_paths(workdir, project):
        if os.path.isdir(d):
            cmd += ["--tmpfs", d]
    # The host session's sockets live here (cc-socks: Claude Code's messaging socket,
    # which takes a user message given its token). The token is in no file a check
    # can read (/proc/<pid>/environ is denied inside bwrap — probed 2026-10-27), but a
    # check has no business near the socket either: hide the whole folder.
    run_user = "/run/user/{}".format(os.getuid())
    if os.path.isdir(run_user):
        cmd += ["--tmpfs", run_user]
    return cmd + list(argv)
