"""Behaviour test for tools/migrate.py (the /soul-migrate pack and receive helper).

FENCE: a move must arrive whole or stop. Every member is hashed against the
manifest and a tampered zip is refused; placement never overwrites (a non-empty
destination, an existing memory folder); credentials and rebuildable folders never
travel whatever the selection says; the memory folder is found by the cwd its
transcripts record, never by decoding a folder name (with no cwd match, the folder named
by encoding the path, marked unconfirmed). The round trip packs a fixture
repo with every kind of state git alone loses and compares it at a DIFFERENT path.
HOME and the Claude config/projects folders point into the temp dir, so the real
~/.claude is never read or written.

Run: python3 -m unittest tools/test_migrate.py -v
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import contextlib
import io
import unittest
import unittest.mock
import zipfile

_TOOL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrate.py")
_spec = importlib.util.spec_from_file_location("migrate", _TOOL)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def _git(cwd, *args, env):
    return subprocess.run(["git", "-C", cwd, *args], env=env, check=True,
                          capture_output=True, text=True).stdout


def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def _env(t):
    """An environment whose HOME, Claude folders and git config all live under t."""
    claude = os.path.join(t, "claude")
    env = dict(os.environ, HOME=os.path.join(t, "home"), CLAUDE_CONFIG_DIR=claude,
               CLAUDE_PROJECTS_DIR=os.path.join(claude, "projects"), GIT_AUTHOR_NAME="t",
               GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t",
               GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    os.makedirs(env["HOME"], exist_ok=True)
    return env


def _tree(root, skip=(".git",)):
    """{relpath: bytes} for every file under root, skipping the named top-level dirs."""
    out = {}
    for d, dirs, files in os.walk(root):
        if d == root:
            dirs[:] = [x for x in dirs if x not in skip]
        for f in files:
            p = os.path.join(d, f)
            with open(p, "rb") as fh:
                out[os.path.relpath(p, root)] = fh.read()
    return out


class RoundTrip(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="soul-migrate-test-")
        t = cls.tmp
        cls.env = env = _env(t)
        cls.claude, cls.projects = env["CLAUDE_CONFIG_DIR"], env["CLAUDE_PROJECTS_DIR"]
        cls.remote = os.path.join(t, "remote.git")
        subprocess.run(["git", "init", "-q", "--bare", cls.remote], env=env, check=True)
        cls.src = src = os.path.join(t, "old", "proj")
        os.makedirs(src)
        _git(src, "init", "-q", "-b", "main", env=env)
        _write(os.path.join(src, ".gitignore"), ".soul/\nnode_modules/\n.env\n")
        _write(os.path.join(src, "app.txt"), "v1\n")
        _write(os.path.join(src, "package.json"), json.dumps({"scripts": {"test": "node test.js && jest"}}))
        _write(os.path.join(src, "package-lock.json"), "{}\n")
        _git(src, "add", ".", env=env)
        _git(src, "commit", "-q", "-m", "init", env=env)
        _git(src, "remote", "add", "origin", cls.remote, env=env)
        _git(src, "push", "-q", "-u", "origin", "main", env=env)
        _git(src, "checkout", "-q", "-b", "feature", env=env)
        _write(os.path.join(src, "feature.txt"), "f\n")
        _git(src, "add", ".", env=env)
        _git(src, "commit", "-q", "-m", "feature", env=env)
        _git(src, "checkout", "-q", "main", env=env)
        _write(os.path.join(src, "extra.txt"), "committed, never pushed\n")
        _git(src, "add", ".", env=env)
        _git(src, "commit", "-q", "-m", "unpushed", env=env)
        _write(os.path.join(src, "app.txt"), "stashed\n")
        _git(src, "stash", "-q", env=env)
        _write(os.path.join(src, "app.txt"), "uncommitted edit\n")
        _write(os.path.join(src, "notes.txt"), "untracked\n")
        os.chmod(os.path.join(src, "notes.txt"), 0o600)
        _write(os.path.join(src, "run.sh"), "echo hi\n")
        os.chmod(os.path.join(src, "run.sh"), 0o700)
        with open(os.path.join(src, ".git", "info", "exclude"), "a") as f:
            f.write("scratch-local/\n")
        _write(os.path.join(src, ".soul", "witness.md"), "# Witness\nSOUL-1 record\n")
        _write(os.path.join(src, "node_modules", "pkg", "index.js"), "x\n")
        _write(os.path.join(src, ".env"), "SECRET=1\n")
        _write(os.path.join(src, "vendored", "lib.txt"), "nested\n")  # a nested repo
        _git(os.path.join(src, "vendored"), "init", "-q", env=env)
        cls.key = "-fake-key-for-proj"
        _write(os.path.join(cls.projects, cls.key, "s.jsonl"),
               json.dumps({"type": "summary"}) + "\n" + json.dumps({"cwd": src}) + "\n")
        _write(os.path.join(cls.projects, cls.key, "memory", "MEMORY.md"), "- remembered\n")
        _write(os.path.join(cls.projects, "-decoy", "s.jsonl"), json.dumps({"cwd": src + "-other"}) + "\n")
        # The folder named by the path, transcripts cleaned up: reported, but the cwd match wins.
        cls.name_key = src.replace("/", "-")
        _write(os.path.join(cls.projects, cls.name_key, "memory", "MEMORY.md"), "- by name\n")
        _write(os.path.join(cls.claude, "settings.json"),
               json.dumps({"enabledPlugins": {"soul-system@x": True, "off@y": False}}))
        cls.out = os.path.join(t, "out")
        cls.sel = os.path.join(t, "selection.json")
        # .env and node_modules are selected on purpose: the packer must drop them anyway.
        cls.selection = {"untracked": ["notes.txt", "run.sh", ".soul/", ".env", "node_modules", "vendored/"],
                         "include_rebuildable": False, "memory_key": cls.key,
                         "smoke": "python3 -c pass", "notes": "test"}
        _write(cls.sel, json.dumps(cls.selection))
        r = cls.run_tool("pack", src, "--out", cls.out, "--selection", cls.sel)
        assert r.returncode == 0, r.stderr
        cls.zip = next(line.split(None, 1)[1] for line in r.stdout.splitlines() if line.startswith("zip "))
        cls.zip_sha = next(line.split()[1] for line in r.stdout.splitlines() if line.startswith("sha256 "))
        cls.dest = os.path.join(t, "new", "moved")
        cls.placed = cls.run_tool("place", cls.zip, cls.dest, "--apply")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    @classmethod
    def run_tool(cls, *args):
        return subprocess.run([sys.executable, _TOOL, *args], env=cls.env, capture_output=True, text=True)

    def g(self, *args):
        return _git(self.dest, *args, env=self.env).strip()

    def test_inventory_finds_everything(self):
        r = self.run_tool("inventory", self.src, "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        inv = json.loads(r.stdout)
        self.assertTrue(inv["soul_project"])
        self.assertEqual({b["name"] for b in inv["git"]["branches"]}, {"main", "feature"})
        self.assertEqual(inv["git"]["no_upstream"], ["feature"])
        self.assertEqual(inv["git"]["stashes"], 1)
        self.assertEqual(inv["git"]["remotes"], {"origin": self.remote})
        self.assertIn("app.txt", inv["dirty"])
        by_path = {e["path"]: e for grp in inv["groups"] for e in grp["sample"]}
        self.assertEqual(by_path["notes.txt"]["git"], "untracked")
        self.assertEqual(by_path[".soul/"]["git"], "ignored")
        self.assertEqual(by_path[".env"]["class"], "credential")
        self.assertEqual(inv["credentials"], [".env"])
        self.assertEqual(inv["rebuildable"][0]["path"], "node_modules")
        self.assertEqual(inv["rebuildable"][0]["rebuild"], "npm ci")
        self.assertEqual([(m["key"], m["matched_by"]) for m in inv["memory"]],
                         [(self.key, "cwd"), (self.name_key, "name")])
        self.assertTrue(inv["memory"][0]["has_memory"])
        self.assertEqual(inv["nested_repos"], ["vendored"])
        self.assertEqual(inv["dependencies"]["plugins"], ["soul-system@x"])
        self.assertEqual(inv["dependencies"]["tools"], ["jest", "node"])
        human = self.run_tool("inventory", self.src)
        self.assertEqual(human.returncode, 0, human.stderr)
        self.assertIn("feature  no upstream set (may not be pushed)", human.stdout)
        self.assertIn("has upstream but 1 commits not pushed", human.stdout)
        self.assertGreaterEqual(inv["git"]["commits"], 3)
        self.assertIn("nested repo vendored — its history is not carried", human.stdout)
        self.assertIn(self.name_key + "  memory/ present  (found by folder name — unconfirmed",
                      human.stdout)

    def test_zip_contents(self):
        with zipfile.ZipFile(self.zip) as zf:
            names = set(zf.namelist())
            receive = zf.read("RECEIVE.md").decode()
            man = json.loads(zf.read("manifest.json"))
        self.assertTrue(os.path.basename(self.zip).startswith("proj-"))
        self.assertTrue({"repo.bundle", "worktree.patch", "files/notes.txt", "files/.soul/witness.md",
                         "memory/MEMORY.md", "RECEIVE.md", "manifest.json"} <= names)
        self.assertFalse([n for n in names if ".env" in n or "node_modules" in n])
        self.assertIn("node_modules - `npm ci`", receive)
        self.assertIn("- .env", receive)
        self.assertIn("python3 -c pass", receive)
        self.assertIn("/soul-migrate receive", receive)
        for item in (".git/hooks", "local .git/config settings", "refs/notes", "remote-tracking refs",
                     "empty folders", "file timestamps", "reflogs", "refs outside heads/tags/stash",
                     ".git/info/attributes", "sparse-checkout", ".git/git-crypt keys"):
            self.assertIn(item, receive.split("## Not carried")[1].split("##")[0])
        self.assertIn("- nested repo vendored — its history is not carried", receive)
        self.assertIn("files/vendored/lib.txt", names)
        self.assertFalse([n for n in names if n.startswith("files/vendored/.git")])
        self.assertEqual(man["project"]["old_path"], self.src)
        self.assertEqual(man["project"]["memory_key"], self.key)
        self.assertEqual(man["project"]["memory_matched_by"], "cwd")
        with zipfile.ZipFile(self.zip) as zf:
            self.assertEqual(zf.read("memory/MEMORY.md"), b"- remembered\n")

    def test_verify_and_tamper(self):
        self.assertEqual(self.run_tool("verify", self.zip).returncode, 0)
        self.assertEqual(self.run_tool("verify", self.zip, "--sha256", self.zip_sha).returncode, 0)
        self.assertEqual(self.run_tool("verify", self.zip, "--sha256", "0" * 64).returncode, 1)
        bad = os.path.join(self.tmp, "tampered.zip")
        with zipfile.ZipFile(self.zip) as src, zipfile.ZipFile(bad, "w") as dst:
            for item in src.infolist():
                data = src.read(item.filename)
                dst.writestr(item, b"changed\n" if item.filename == "files/notes.txt" else data)
        r = self.run_tool("verify", bad)
        self.assertEqual(r.returncode, 1)
        self.assertIn("hash mismatch: files/notes.txt", r.stderr)
        r = self.run_tool("place", bad, os.path.join(self.tmp, "never"), "--apply")
        self.assertEqual(r.returncode, 1)
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "never")))

    def test_place_restores_the_tree(self):
        self.assertEqual(self.placed.returncode, 0, self.placed.stderr)
        want = {k: v for k, v in _tree(self.src).items()
                if not k.startswith(("node_modules", "vendored/.git/")) and k != ".env"}
        self.assertEqual(_tree(self.dest), want)
        with open(os.path.join(self.dest, "app.txt")) as f:
            self.assertEqual(f.read(), "uncommitted edit\n")
        self.assertTrue(os.path.isfile(os.path.join(self.dest, ".soul", "witness.md")))
        self.assertFalse(os.path.exists(os.path.join(self.dest, "node_modules")))
        self.assertFalse(os.path.exists(os.path.join(self.dest, ".env")))

    def test_place_restores_git_state(self):
        self.assertEqual(set(self.g("for-each-ref", "--format=%(refname:short)", "refs/heads").split()),
                         {"main", "feature"})
        self.assertEqual(self.g("symbolic-ref", "--short", "HEAD"), "main")
        self.assertEqual(self.g("remote"), "origin")
        self.assertEqual(self.g("remote", "get-url", "origin"), self.remote)
        self.assertEqual(self.g("config", "branch.main.merge"), "refs/heads/main")
        r = subprocess.run(["git", "-C", self.dest, "config", "branch.feature.remote"], env=self.env)
        self.assertEqual(r.returncode, 1)  # feature had no upstream and still has none
        self.assertEqual(len(self.g("stash", "list").splitlines()), 1)
        self.assertEqual(self.g("show", "stash@{0}:app.txt"), "stashed")

    def test_place_keeps_only_the_exec_bit_and_carries_exclude(self):
        umask = os.umask(0)
        os.umask(umask)
        mode = lambda rel: os.stat(os.path.join(self.dest, rel)).st_mode & 0o777
        self.assertEqual(mode("notes.txt"), 0o644 & ~umask)  # was 0o600
        self.assertEqual(mode("run.sh"), 0o755 & ~umask)  # was 0o700
        with open(os.path.join(self.dest, ".git", "info", "exclude")) as f:
            self.assertIn("scratch-local/", f.read())

    def test_pack_stops_on_two_memory_folders(self):
        # The cwd match and the folder named by the path both hold memory/: no silent pick.
        sel = os.path.join(self.tmp, "no-key.json")
        _write(sel, json.dumps(dict(self.selection, memory_key=None)))
        out = os.path.join(self.tmp, "out-two-memory")
        r = self.run_tool("pack", self.src, "--out", out, "--selection", sel)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("memory_key", r.stderr)
        self.assertIn(self.key, r.stderr)
        self.assertIn(self.name_key, r.stderr)
        self.assertFalse(os.path.exists(out) and os.listdir(out))

    def test_place_refuses_non_empty_dest(self):
        full = os.path.join(self.tmp, "full")
        _write(os.path.join(full, "keep.txt"), "mine\n")
        r = self.run_tool("place", self.zip, full, "--apply")
        self.assertEqual(r.returncode, 1)
        self.assertEqual(os.listdir(full), ["keep.txt"])

    def conflict_zip(self):
        """The round-trip zip plus files/package.json, a path the clone already holds."""
        z = os.path.join(self.tmp, "conflict.zip")
        with zipfile.ZipFile(self.zip) as src, zipfile.ZipFile(z, "w") as dst:
            man = json.loads(src.read("manifest.json"))
            for name in src.namelist():
                if name != "manifest.json":
                    dst.writestr(name, src.read(name))
            dst.writestr("files/package.json", "{}")
            man["members"].append({"path": "files/package.json", "sha256": _mod.hashlib.sha256(
                b"{}").hexdigest(), "bytes": 2, "mode": 0o644})
            dst.writestr("manifest.json", json.dumps(man))
        return z

    def test_self_check_refuses_what_place_would(self):
        with unittest.mock.patch.dict(os.environ, self.env), self.assertRaises(_mod.Stop) as cm:
            _mod.self_check(self.conflict_zip())
        self.assertIn("a tracked path is already there: package.json", str(cm.exception))

    def test_place_stops_on_conflict_with_cloned_tree(self):
        # A files/ member that the clone already holds (a tracked path) must stop, not overwrite.
        z = self.conflict_zip()
        dest = os.path.join(self.tmp, "conflict-dest")
        r = self.run_tool("place", z, dest, "--apply")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("exists, not overwriting", r.stderr)
        with open(os.path.join(dest, "package.json")) as f:
            self.assertIn("scripts", f.read())  # the tracked file, untouched
        self.assertFalse(os.path.exists(os.path.join(dest, "notes.txt")))  # no file was written

    def test_place_preview_writes_nothing(self):
        dest = os.path.join(self.tmp, "preview")
        r = self.run_tool("place", self.zip, dest)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("PREVIEW", r.stdout)
        self.assertFalse(os.path.exists(dest))

    def test_place_memory_then_refuses_second(self):
        key = "-new-home-moved"
        r = self.run_tool("place-memory", self.zip, "--key=" + key, "--apply")
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(os.path.join(self.projects, key, "memory", "MEMORY.md")) as f:
            self.assertEqual(f.read(), "- remembered\n")
        r = self.run_tool("place-memory", self.zip, "--key", key, "--apply")  # the spaced form too
        self.assertEqual(r.returncode, 1)
        self.assertIn("already exists", r.stderr)

    def test_out_inside_project_refused(self):
        r = self.run_tool("pack", self.src, "--out", os.path.join(self.src, "sub"), "--selection", self.sel)
        self.assertEqual(r.returncode, 2)
        self.assertFalse(os.path.exists(os.path.join(self.src, "sub")))

    def test_memory_key(self):
        r = self.run_tool("memory-key", "/home/me/My-Proj")
        self.assertEqual(r.stdout.strip(), "-home-me-My-Proj")
        r = self.run_tool("memory-key", "/home/me/my_proj.v2")  # "_" observed as "-"
        self.assertEqual(r.stdout.strip(), "-home-me-my-proj-v2")


class Units(unittest.TestCase):
    def test_is_exec_ignores_drvfs_0777(self):
        d = tempfile.mkdtemp(prefix="soul-migrate-test-")
        self.addCleanup(shutil.rmtree, d)
        for name, body, mode, want in (("plain", b"x", 0o777, False),
                                       ("script", b"#!/bin/sh\n", 0o777, True),
                                       ("tool", b"x", 0o755, True),
                                       ("doc", b"x", 0o644, False)):
            path = os.path.join(d, name)
            with open(path, "wb") as fh:
                fh.write(body)
            os.chmod(path, mode)
            with open(path, "rb") as fh:
                self.assertEqual(_mod.is_exec(fh), want, name)
                self.assertEqual(fh.read(), body, name)  # position restored

    def test_credentials(self):
        for rel in (".env", ".env.local", "id_rsa", "deploy/server.pem", "config/credentials.json",
                    "secrets/db.txt", "github_token", "token.json", "api-tokens.txt",
                    ".envrc", "prod.env", ".mcp.json", ".pgpass", "web/.htpasswd", "vault.kdbx",
                    "terraform.tfstate", "terraform.tfstate.backup", "prod.tfvars", "putty.ppk",
                    "AuthKey.p8", "id_ed25519_sk", "home/.ssh/known_hosts", "home/.kube/config",
                    ".docker/config.json", "service-account-prod.json", "auth.json",
                    "db_password.txt", "apikey.txt", "my_api_key", ".claude/settings.local.json"):
            self.assertTrue(_mod.is_credential(rel), rel)
        for rel in ("tokenizer.py", "README.md", "src/env.py", "notes/keys.md", "config",
                    "docs/config.json", ".claude/settings.json", "src/environment.py"):
            self.assertFalse(_mod.is_credential(rel), rel)

    def test_rebuildable(self):
        self.assertEqual(_mod.rebuild_group("node_modules/"), "node_modules")
        self.assertEqual(_mod.rebuild_group("web/node_modules/a/b.js"), "web/node_modules")
        self.assertEqual(_mod.rebuild_group("android/app/build/x.o"), "android/app/build")
        self.assertEqual(_mod.rebuild_group("pkg/__pycache__/m.pyc"), "pkg/__pycache__")
        self.assertIsNone(_mod.rebuild_group("src/build"))  # a FILE named build
        self.assertIsNone(_mod.rebuild_group("src/main.py"))
        with tempfile.TemporaryDirectory(prefix="soul-migrate-test-") as d:
            _write(os.path.join(d, "web", "package-lock.json"), "{}")
            self.assertEqual(_mod.rebuild_cmd(d, "web/node_modules"), "cd web && npm ci")
            self.assertEqual(_mod.rebuild_cmd(d, "node_modules"), "npm install")
            _write(os.path.join(d, "requirements.txt"), "")
            self.assertIn("pip install -r requirements.txt", _mod.rebuild_cmd(d, ".venv"))
            _write(os.path.join(d, "y", "yarn.lock"), "")
            _write(os.path.join(d, "p", "pnpm-lock.yaml"), "")
            self.assertEqual(_mod.rebuild_cmd(d, "y/node_modules"), "cd y && yarn install --frozen-lockfile")
            self.assertEqual(_mod.rebuild_cmd(d, "p/node_modules"), "cd p && pnpm install --frozen-lockfile")
            self.assertEqual(_mod.rebuild_cmd(d, "infra/.terraform"), "cd infra && terraform init")
        for name in ("target", ".terraform", ".cache", "coverage"):
            self.assertEqual(_mod.rebuild_group(name + "/x"), name)

    def test_out_dir(self):
        with tempfile.TemporaryDirectory(prefix="soul-migrate-test-") as d:
            p = os.path.join(d, "proj")
            os.makedirs(p)
            self.assertTrue(_mod.out_ok(p, os.path.join(p, ".ai", "migrate-out")))
            self.assertTrue(_mod.out_ok(p, os.path.join(d, "elsewhere")))
            self.assertTrue(_mod.out_ok(p, p + "-sibling"))
            self.assertFalse(_mod.out_ok(p, p))
            self.assertFalse(_mod.out_ok(p, os.path.join(p, ".ai")))

    def test_memory_found_by_name_without_transcripts(self):
        with tempfile.TemporaryDirectory(prefix="soul-migrate-test-") as d:
            proj, projects = os.path.join(d, "my_proj"), os.path.join(d, "projects")
            os.makedirs(proj)
            _write(os.path.join(projects, proj.replace("/", "-"), "memory", "MEMORY.md"), "- m\n")
            _write(os.path.join(projects, "-other", "s.jsonl"), json.dumps({"cwd": d}) + "\n")
            with unittest.mock.patch.dict(os.environ, {"CLAUDE_PROJECTS_DIR": projects}):
                found = _mod.find_memory(proj)
            self.assertEqual([(m["key"], m["matched_by"], m["has_memory"]) for m in found],
                             [(proj.replace("/", "-"), "name", True)])

    def test_memory_found_by_alphanumeric_key(self):
        # Observed rule: every non-alphanumeric character becomes "-" ("_" included).
        with tempfile.TemporaryDirectory(prefix="soul-migrate-test-") as d:
            proj, projects = os.path.join(d, "my_proj"), os.path.join(d, "projects")
            os.makedirs(proj)
            key = _mod.re.sub(r"[^A-Za-z0-9]", "-", proj)
            _write(os.path.join(projects, key, "memory", "MEMORY.md"), "- m\n")
            with unittest.mock.patch.dict(os.environ, {"CLAUDE_PROJECTS_DIR": projects}):
                found = _mod.find_memory(proj)
            self.assertEqual([(m["key"], m["matched_by"]) for m in found], [(key, "name")])

    def test_memory_name_match_recording_another_cwd_skipped(self):
        with tempfile.TemporaryDirectory(prefix="soul-migrate-test-") as d:
            proj, projects = os.path.join(d, "my_proj"), os.path.join(d, "projects")
            os.makedirs(proj)
            key = _mod.memory_key(proj)
            _write(os.path.join(projects, key, "memory", "MEMORY.md"), "- m\n")
            _write(os.path.join(projects, key, "s.jsonl"), json.dumps({"cwd": "/elsewhere"}) + "\n")
            with unittest.mock.patch.dict(os.environ, {"CLAUDE_PROJECTS_DIR": projects}):
                self.assertEqual(_mod.find_memory(proj), [])

    def test_memory_key_false_packs_no_memory(self):
        two = [{"key": k, "matched_by": "name", "path": k, "has_memory": True} for k in ("-a", "-b")]
        self.assertIsNone(_mod.pick_memory(two, {"memory_key": False}))

    def test_write_members_streams(self):
        with tempfile.TemporaryDirectory(prefix="soul-migrate-test-") as d:
            z, target = os.path.join(d, "x.zip"), os.path.join(d, "dest", "big.bin")
            with zipfile.ZipFile(z, "w") as zf:
                zf.writestr("files/big.bin", b"payload")
            with unittest.mock.patch.object(_mod.zipfile.ZipFile, "read",
                                            side_effect=AssertionError("whole-member read")):
                _mod.write_members(z, [(target, {"path": "files/big.bin"})])
            with open(target, "rb") as f:
                self.assertEqual(f.read(), b"payload")

    def test_strip_userinfo(self):
        self.assertEqual(_mod.strip_userinfo("https://me:pw@host/x.git"), ("https://host/x.git", True))
        self.assertEqual(_mod.strip_userinfo("https://tok@host/x.git"), ("https://host/x.git", True))
        for url in ("git@host:me/x.git", "ssh://git@host/x.git", "/srv/x.git", "https://host/x"):
            self.assertEqual(_mod.strip_userinfo(url), (url, False))
        self.assertEqual(_mod.strip_userinfo("https://[bad/x"), ("https://[bad/x", None))

    def test_git_runs_without_optional_locks_or_lfs_smudge(self):
        done = subprocess.CompletedProcess([], 0, b"", b"")
        with unittest.mock.patch.object(_mod.subprocess, "run", return_value=done) as run:
            _mod.git(".", "status")
        env = run.call_args.kwargs["env"]
        self.assertEqual((env["GIT_OPTIONAL_LOCKS"], env["GIT_LFS_SKIP_SMUDGE"]), ("0", "1"))

    def test_plan_refuses_traversal_case_and_escaping_links(self):
        with tempfile.TemporaryDirectory(prefix="soul-migrate-test-") as d:
            z = os.path.join(d, "x.zip")
            with zipfile.ZipFile(z, "w") as zf:
                zf.writestr("files/A.txt", "1")
                zf.writestr("files/a.txt", "2")
                zf.writestr("files/out", "../../etc")
            dest = os.path.join(d, "dest")
            man = {"members": [{"path": "files/A.txt"}, {"path": "files/a.txt"},
                               {"path": "files/out", "symlink": True}]}
            with self.assertRaises(_mod.Stop) as cm:
                _mod.plan_targets(z, dest, man, "files/")
            self.assertIn("case collision", str(cm.exception))
            self.assertIn("symlink escapes", str(cm.exception))
            self.assertFalse(os.path.exists(dest))
            self.assertFalse(_mod.rel_ok("../x"))
            self.assertFalse(_mod.rel_ok("/abs"))
            self.assertFalse(_mod.rel_ok("a/.git/config"))


class Edges(unittest.TestCase):
    """One small repo per test, for the states the round trip does not hold."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="soul-migrate-test-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.env = _env(self.tmp)
        self.src = os.path.join(self.tmp, "src")
        os.makedirs(self.src)
        self.git("init", "-q", "-b", "main")
        _write(os.path.join(self.src, "a.txt"), "a\n")
        self.commit()

    def git(self, *args, cwd=None):
        return _git(cwd or self.src, *args, env=self.env)

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-q", "-m", "c")

    def run_tool(self, *args):
        return subprocess.run([sys.executable, _TOOL, *args], env=self.env, capture_output=True,
                              text=True, timeout=120)

    def inventory(self, project=None):
        r = self.run_tool("inventory", project or self.src, "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout)

    def pack(self, selection=None, out="out", project=None):
        sel = os.path.join(self.tmp, out + ".json")
        _write(sel, json.dumps(selection or {}))
        r = self.run_tool("pack", project or self.src, "--out", os.path.join(self.tmp, out),
                          "--selection", sel)
        zpath = next((ln.split(None, 1)[1] for ln in r.stdout.splitlines() if ln.startswith("zip ")), None)
        return r, zpath

    def place(self, zpath):
        dest = os.path.join(self.tmp, "dest")
        r = self.run_tool("place", zpath, dest, "--apply")
        self.assertEqual(r.returncode, 0, r.stderr)
        return dest

    def names(self, zpath):
        with zipfile.ZipFile(zpath) as zf:
            return set(zf.namelist())

    def test_patch_ignores_user_diff_config(self):
        cfg = os.path.join(self.tmp, "gitconfig")
        _write(cfg, "[diff]\n\texternal = echo\n\tnoprefix = true\n[color]\n\tui = always\n")
        self.env["GIT_CONFIG_GLOBAL"] = cfg
        _write(os.path.join(self.src, "a.txt"), "changed\n")
        r, zpath = self.pack()
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(os.path.join(self.place(zpath), "a.txt")) as f:
            self.assertEqual(f.read(), "changed\n")

    def test_linked_worktree_is_named_and_its_gitfile_skipped(self):
        _write(os.path.join(self.src, ".gitignore"), ".wt/\n")
        self.commit()
        self.git("worktree", "add", "-q", os.path.join(self.src, ".wt", "side"), "-b", "side")
        inv = self.inventory()
        self.assertEqual(inv["nested_repos"], [])
        human = self.run_tool("inventory", self.src).stdout
        self.assertIn("linked worktree", human)
        self.assertNotIn("nested repo", human)
        r, zpath = self.pack({"untracked": [".wt/"]})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn(".wt/side/.git (git link file", r.stdout)
        self.assertFalse([n for n in self.names(zpath) if n.endswith("/.git")])
        self.assertIn("files/.wt/side/a.txt", self.names(zpath))

    def test_pack_removes_its_zip_when_the_self_check_fails(self):
        _write(os.path.join(self.src, "a.txt"), "changed\n")
        real = _mod.git
        fake = lambda cwd, *args, **kw: b"not a patch\n" if args[:1] == ("diff",) else real(cwd, *args, **kw)
        out, sel = os.path.join(self.tmp, "out"), os.path.join(self.tmp, "sel.json")
        _write(sel, "{}")
        with unittest.mock.patch.dict(os.environ, self.env), \
                unittest.mock.patch.object(_mod, "git", fake), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()) as err:
            rc = _mod.main(["pack", self.src, "--out", out, "--selection", sel])
        self.assertEqual(rc, 1)
        self.assertIn("apply", err.getvalue())
        self.assertEqual(os.listdir(out), [])

    def test_remote_credentials_are_stripped(self):
        self.git("remote", "add", "mirror", "https://me:hunter2@example.invalid/x.git")
        self.git("remote", "add", "box", "git@example.invalid:me/x.git")
        inv = self.inventory()
        self.assertEqual(inv["git"]["remotes"], {"mirror": "https://example.invalid/x.git",
                                                 "box": "git@example.invalid:me/x.git"})
        self.assertIn("remote mirror had an embedded credential (removed)", inv["credentials"])
        r, zpath = self.pack()
        self.assertEqual(r.returncode, 0, r.stderr)
        with zipfile.ZipFile(zpath) as zf:
            self.assertFalse([n for n in zf.namelist() if b"hunter2" in zf.read(n)])
        self.assertEqual(self.git("remote", "get-url", "mirror", cwd=self.place(zpath)).strip(),
                         "https://example.invalid/x.git")

    def test_lfs_warning(self):
        _write(os.path.join(self.src, ".gitattributes"), "*.bin filter=lfs diff=lfs merge=lfs -text\n")
        self.commit()
        human = self.run_tool("inventory", self.src).stdout
        self.assertIn("run `git lfs pull`", human)
        self.assertIn("never pushed to the LFS server are unrecoverable", human)

    def test_shallow_clone_refused(self):
        _write(os.path.join(self.src, "b.txt"), "b\n")
        self.commit()
        shallow = os.path.join(self.tmp, "shallow")
        subprocess.run(["git", "clone", "-q", "--depth", "1", "file://" + self.src, shallow],
                       env=self.env, check=True)
        r, zpath = self.pack(project=shallow)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("git fetch --unshallow", r.stderr)
        self.assertIsNone(zpath)

    def test_flagged_files_carry_their_content_and_flag(self):
        for name in ("conf.txt", "local.txt"):
            _write(os.path.join(self.src, name), "base\n")
        self.commit()
        self.git("update-index", "--skip-worktree", "conf.txt")
        self.git("update-index", "--assume-unchanged", "local.txt")
        _write(os.path.join(self.src, "conf.txt"), "mine\n")
        _write(os.path.join(self.src, "local.txt"), "mine too\n")
        self.assertEqual(self.inventory()["flagged"], [{"path": "conf.txt", "flag": "skip-worktree"},
                                                       {"path": "local.txt", "flag": "assume-unchanged"}])
        r, zpath = self.pack()
        self.assertEqual(r.returncode, 0, r.stderr)
        dest = self.place(zpath)
        for name, text in (("conf.txt", "mine\n"), ("local.txt", "mine too\n")):
            with open(os.path.join(dest, name)) as f:
                self.assertEqual(f.read(), text)
        self.assertEqual(self.git("ls-files", "-v", "conf.txt", "local.txt", cwd=dest).split(),
                         ["S", "conf.txt", "h", "local.txt"])

    def test_rebuildable_inside_a_normal_folder_is_its_own_group(self):
        _write(os.path.join(self.src, ".gitignore"), "tools/\n")
        self.commit()
        _write(os.path.join(self.src, "tools", "keep.txt"), "k\n")
        _write(os.path.join(self.src, "tools", "build", "out.o"), "o\n")
        self.assertEqual([r["path"] for r in self.inventory()["rebuildable"]], ["tools/build"])
        r, zpath = self.pack({"untracked": ["tools/"]})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("files/tools/keep.txt", self.names(zpath))
        self.assertNotIn("files/tools/build/out.o", self.names(zpath))

    def test_credential_like_path_forced_in_only_by_name(self):
        _write(os.path.join(self.src, "docs", "secretary.md"), "s\n")
        _write(os.path.join(self.src, "docs", "plain.md"), "p\n")
        r, zpath = self.pack({"untracked": ["docs/"]}, out="default")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("files/docs/secretary.md", self.names(zpath))
        r, zpath = self.pack({"untracked": ["docs/"], "include_credential_like": ["docs/secretary.md"]},
                             out="forced")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("files/docs/secretary.md", self.names(zpath))

    def test_inventory_json_is_summarised(self):
        _write(os.path.join(self.src, "many", "keep.txt"), "k\n")
        self.commit()
        for i in range(25):
            _write(os.path.join(self.src, "many", "f{:02}.txt".format(i)), "x\n")
        for name in ("a.txt", "b.txt"):
            _write(os.path.join(self.src, "fresh", name), "x\n")
        inv = self.inventory()
        self.assertNotIn("entries", inv)
        groups = {g["path"]: g for g in inv["groups"]}
        self.assertEqual((groups["many/"]["count"], len(groups["many/"]["sample"])), (25, 20))
        self.assertEqual([e["path"] for e in groups["fresh/"]["sample"]], ["fresh/"])
        self.assertEqual(groups["fresh/"]["count"], 2)

    def test_sizes_counted_once_and_without_old_zips(self):
        _write(os.path.join(self.src, ".gitignore"), "*.log\n.ai/\n")
        self.commit()
        _write(os.path.join(self.src, "new", "x.txt"), "xx\n")
        _write(os.path.join(self.src, "new", "y.log"), "yyyy\n")
        _write(os.path.join(self.src, ".ai", "plan.md"), "pp\n")
        _write(os.path.join(self.src, ".ai", "migrate-out", "old.zip"), "z" * 100)
        # A folder and a file inside it both listed (git 2.43 here does not; review reported
        # it): simulated by adding the child to the ignored listing.
        real = _mod.git
        fake = lambda cwd, *a, **kw: real(cwd, *a, **kw) + ("new/y.log\0" if "--ignored" in a else "")
        with unittest.mock.patch.dict(os.environ, self.env), unittest.mock.patch.object(_mod, "git", fake):
            groups = {g["path"]: g for g in _mod.inventory(self.src)["groups"]}
        self.assertEqual(groups["new/"]["bytes"], 8)
        self.assertEqual(groups[".ai/"]["bytes"], 3)

    def test_odd_files_skipped_with_a_reason(self):
        _write(os.path.join(self.src, "odd", "ok.txt"), "ok\n")
        os.mkfifo(os.path.join(self.src, "odd", "pipe"))
        with open(os.path.join(os.fsencode(self.src), b"odd", b"bad\xff.txt"), "w") as f:
            f.write("b\n")
        _write(os.path.join(self.src, " lead.txt"), "space\n")
        r, zpath = self.pack({"untracked": ["odd/", " lead.txt"]})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("odd/pipe (not a regular file)", r.stdout)
        self.assertIn("(name is not valid UTF-8)", r.stdout)
        self.assertTrue({"files/odd/ok.txt", "files/ lead.txt"} <= self.names(zpath))


    def receive(self, zpath):
        with zipfile.ZipFile(zpath) as zf:
            return zf.read("RECEIVE.md").decode()

    def test_flagged_credential_stays_home(self):
        _write(os.path.join(self.src, "deploy.pem"), "base\n")
        self.commit()
        self.git("update-index", "--skip-worktree", "deploy.pem")
        _write(os.path.join(self.src, "deploy.pem"), "real key\n")
        self.assertIn("deploy.pem", self.inventory()["credentials"])
        r, zpath = self.pack()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("files/deploy.pem", self.names(zpath))
        self.assertIn("- deploy.pem", self.receive(zpath).split("## Credentials")[1].split("##")[0])

    def test_credential_like_named_alone_is_carried(self):
        _write(os.path.join(self.src, "secretary.md"), "s\n")
        r, zpath = self.pack({"include_credential_like": ["secretary.md"]})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("files/secretary.md", self.names(zpath))

    def test_escaping_symlink_in_memory_left_out(self):
        folder = os.path.join(self.env["CLAUDE_PROJECTS_DIR"], "-k")
        _write(os.path.join(folder, "s.jsonl"), json.dumps({"cwd": self.src}) + "\n")
        _write(os.path.join(folder, "memory", "MEMORY.md"), "- m\n")
        os.symlink(os.path.join(self.tmp, "outside"), os.path.join(folder, "memory", "out"))
        r, zpath = self.pack()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("memory/out (symlink leaves the project)", r.stdout)
        r = self.run_tool("place-memory", zpath, "--key=-new", "--apply")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_case_pair_placed_on_a_case_sensitive_disk(self):
        if _mod.case_insensitive(self.tmp):
            self.skipTest("temp folder is on a case-insensitive disk")
        for name in ("A.txt", "a.txt"):
            _write(os.path.join(self.src, name), name)
        r, zpath = self.pack({"untracked": ["A.txt"]})
        self.assertEqual(r.returncode, 0, r.stderr)
        with open(os.path.join(self.place(zpath), "A.txt")) as f:
            self.assertEqual(f.read(), "A.txt")

    def test_remotes_read_from_config(self):
        self.git("remote", "add", "origin", "https://example.invalid/x.git")
        self.git("config", "remote.origin.pushurl", "https://me:hunter2@example.invalid/push.git")
        self.git("config", "remote.origin.promisor", "true")
        self.git("config", "remote.origin.partialclonefilter", "blob:none")  # `remote -v`: [blob:none]
        inv = self.inventory()
        self.assertEqual(inv["git"]["remotes"], {"origin": "https://example.invalid/x.git"})
        self.assertIn("remote origin had an embedded credential (removed)", inv["credentials"])
        self.assertIn("partial clone", self.run_tool("inventory", self.src).stdout)
        r, zpath = self.pack()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.git("remote", "get-url", "--push", "origin", cwd=self.place(zpath)).strip(),
                         "https://example.invalid/push.git")

    def test_staged_split_and_an_untracked_former_file(self):
        _write(os.path.join(self.src, "b.txt"), "b\n")
        self.commit()
        self.git("rm", "-q", "--cached", "b.txt")  # still on disk, now untracked
        _write(os.path.join(self.src, "a.txt"), "staged\n")
        self.git("add", "a.txt")
        _write(os.path.join(self.src, "a.txt"), "unstaged\n")
        r, zpath = self.pack({"untracked": ["b.txt"]})
        self.assertEqual(r.returncode, 0, r.stderr)
        dest = self.place(zpath)
        self.assertEqual(self.git("show", ":a.txt", cwd=dest), "staged\n")
        with open(os.path.join(dest, "a.txt")) as f:
            self.assertEqual(f.read(), "unstaged\n")
        self.assertTrue(os.path.isfile(os.path.join(dest, "b.txt")))
        self.assertEqual(self.git("ls-files", "b.txt", cwd=dest), "")

    @unittest.skipIf(os.geteuid() == 0, "root reads everything")
    def test_unreadable_skipped_and_named(self):
        new = os.path.join(self.src, "new")
        _write(os.path.join(new, "ok.txt"), "ok\n")
        _write(os.path.join(new, "closed.txt"), "c\n")
        _write(os.path.join(new, "locked", "x.txt"), "x\n")
        os.chmod(os.path.join(new, "closed.txt"), 0)
        os.chmod(os.path.join(new, "locked"), 0)
        self.addCleanup(os.chmod, os.path.join(new, "locked"), 0o755)
        self.assertEqual(self.inventory()["unreadable"], {"new/closed.txt": "not readable",
                                                          "new/locked": "folder not readable"})
        r, zpath = self.pack({"untracked": ["new/"]})
        self.assertEqual(r.returncode, 0, r.stderr)
        for named in ("new/closed.txt (not readable)", "new/locked (folder not readable)"):
            self.assertIn(named, r.stdout)
            self.assertIn(named, self.receive(zpath))
        self.assertIn("files/new/ok.txt", self.names(zpath))

    def test_left_out_collapses_rebuildable_and_skips_tracked(self):
        _write(os.path.join(self.src, ".gitignore"), "node_modules/\n")
        _write(os.path.join(self.src, "docs", "tracked.md"), "t\n")
        self.commit()
        _write(os.path.join(self.src, "docs", "new.md"), "n\n")
        for f in ("a/x.js", "b/y.js"):
            _write(os.path.join(self.src, "node_modules", f), "x\n")
        r, zpath = self.pack({"untracked": ["node_modules/", "docs/"]})
        self.assertEqual(r.returncode, 0, r.stderr)
        for text in (r.stdout, self.receive(zpath)):
            self.assertIn("node_modules (rebuildable)", text)
            self.assertNotIn("x.js", text)
            self.assertNotIn("docs/tracked.md", text)

    def test_patches_ignore_whitespace_and_submodule_config(self):
        cfg = os.path.join(self.tmp, "gitconfig")
        _write(cfg, "[apply]\n\twhitespace = error\n[diff]\n\tsubmodule = log\n")
        self.env["GIT_CONFIG_GLOBAL"] = cfg
        head = self.git("rev-parse", "HEAD").strip()
        self.git("update-index", "--add", "--cacheinfo", "160000," + head + ",sub")
        self.git("commit", "-q", "-m", "gitlink")
        self.git("update-index", "--cacheinfo", "160000," + "1" * 40 + ",sub")  # staged bump
        _write(os.path.join(self.src, "a.txt"), "trailing  \n")
        r, zpath = self.pack()
        self.assertEqual(r.returncode, 0, r.stderr)
        dest = self.place(zpath)
        self.assertIn("1" * 40, self.git("ls-files", "-s", "sub", cwd=dest))
        with open(os.path.join(dest, "a.txt")) as f:
            self.assertEqual(f.read(), "trailing  \n")

    def test_dirty_tracked_credential_listed(self):
        _write(os.path.join(self.src, "prod.env"), "A=1\n")
        self.commit()
        _write(os.path.join(self.src, "prod.env"), "A=2\n")
        self.assertEqual(self.inventory()["credentials"], [
            "prod.env  (tracked file with uncommitted changes — the change travels in the patch)"])

    def test_operation_in_progress_warned(self):
        _write(os.path.join(self.src, ".git", "MERGE_HEAD"), self.git("rev-parse", "HEAD"))
        self.assertIn("MERGE_HEAD present: operation in progress",
                      self.run_tool("inventory", self.src).stdout)

    def test_place_ignores_the_receivers_default_remote_name(self):
        r, zpath = self.pack()
        self.assertEqual(r.returncode, 0, r.stderr)
        cfg = os.path.join(self.tmp, "gitconfig")
        _write(cfg, "[clone]\n\tdefaultRemoteName = upstream\n")
        self.env["GIT_CONFIG_GLOBAL"] = cfg
        self.place(zpath)

    def test_unparseable_remote_flagged(self):
        self.git("remote", "add", "bad", "https://[bad/x")
        self.assertIn("remote bad could not be parsed — check it for credentials by hand",
                      self.inventory()["credentials"])

    def test_selection_types_checked(self):
        for sel in (["x"], {"untracked": "x"}, {"memory_key": True}, {"smoke": 1}):
            r, _ = self.pack(sel)
            self.assertEqual(r.returncode, 2, sel)
            self.assertIn("--selection", r.stderr)
        r = self.run_tool("pack", "--help")
        for field in ("untracked", "include_rebuildable", "include_credential_like",
                      "memory_key", "smoke", "notes"):
            self.assertIn(field, r.stdout)


if __name__ == "__main__":
    unittest.main()
