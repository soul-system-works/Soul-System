#!/usr/bin/env python3
"""Install this checkout in a temporary Codex home and check actual discovery.

Requires the local Codex CLI. Does not invoke a model, change normal Codex config,
trust hooks, or prove a live SessionStart/Stop cycle. All writes are temporary.
"""

import json
import os
from pathlib import Path
import queue
import subprocess
import tempfile
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = "soul-system@soul-system-codex"


def check():
    with tempfile.TemporaryDirectory(prefix="soul-codex-check-") as temporary:
        base = Path(temporary)
        task_codex_home = base / "config"
        task_codex_home.mkdir()
        project = base / "project"
        project.mkdir()
        env = {**os.environ, "CODEX_HOME": str(task_codex_home)}

        def cli(*args):
            result = subprocess.run(
                ["codex", *args], env=env, capture_output=True, text=True, timeout=60,
            )
            if result.returncode:
                raise RuntimeError(f"codex {' '.join(args)}: {result.stderr}")
            return json.loads(result.stdout)

        cli("plugin", "marketplace", "add", str(ROOT), "--json")
        listing = cli("plugin", "list", "--marketplace", "soul-system-codex", "--available", "--json")
        if not any(p["pluginId"] == PLUGIN for p in listing["available"]):
            raise RuntimeError("Plugin not discovered in local marketplace")
        installed = cli("plugin", "add", PLUGIN, "--json")
        installed_root = Path(installed["installedPath"])
        manifest = json.loads((installed_root / ".codex-plugin/plugin.json").read_text())
        if manifest["hooks"] != "./hooks/codex.json":
            raise RuntimeError("Codex manifest must select the Codex hook adapter")
        for relative in ("hooks/codex.json", "hooks/codex.py", "operations/CLAUDE.md",
                         "operations/codex.md", "tools/codex-project.py"):
            if not (installed_root / relative).is_file():
                raise RuntimeError(f"Installed package is missing {relative}")
        expected = {"soul-system:" + path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        for source in (ROOT / "skills").glob("*/SKILL.md"):
            explicit = "disable-model-invocation: true" in source.read_text().split("---", 2)[1]
            if explicit:
                policy = installed_root / "skills" / source.parent.name / "agents/openai.yaml"
                if not policy.is_file() or "allow_implicit_invocation: false" not in policy.read_text():
                    raise RuntimeError(f"Missing Codex explicit-invocation policy for {source.parent.name}")

        with (base / "server.log").open("w+") as log:
            server = subprocess.Popen(
                ["codex", "app-server", "--stdio"], env=env, cwd=project,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=log,
                text=True, bufsize=1,
            )
            messages = queue.Queue()

            def receive():
                for line in server.stdout:
                    messages.put(json.loads(line))

            reader = threading.Thread(target=receive, daemon=True)
            reader.start()

            def request(identifier, method, params):
                server.stdin.write(json.dumps({"id": identifier, "method": method, "params": params}) + "\n")
                server.stdin.flush()
                deadline = time.monotonic() + 40
                while time.monotonic() < deadline:
                    try:
                        message = messages.get(timeout=1)
                    except queue.Empty:
                        if server.poll() is not None:
                            raise RuntimeError("Codex app-server exited before responding")
                        continue
                    if message.get("id") == identifier:
                        if "error" in message:
                            raise RuntimeError(message["error"])
                        return message["result"]
                raise TimeoutError(method)

            try:
                initialized = request(1, "initialize", {
                    "clientInfo": {"name": "soul-plugin-check", "version": "0.1"},
                    "capabilities": {"experimentalApi": True},
                })
                server.stdin.write(json.dumps({"method": "initialized"}) + "\n")
                server.stdin.flush()
                loaded = request(2, "skills/list", {"cwds": [str(project)], "forceReload": True})
                entry = loaded["data"][0]
                errors = [e for e in entry["errors"] if "soul-" in e.get("path", "")]
                skills = {s["name"] for s in entry["skills"] if s.get("pluginId") == PLUGIN and s["enabled"]}
                if errors or skills != expected:
                    raise RuntimeError({"errors": errors, "expected": sorted(expected), "loaded": sorted(skills)})
                hook_result = request(3, "hooks/list", {"cwds": [str(project)]})["data"][0]
                hooks = [h for h in hook_result["hooks"] if h.get("pluginId") == PLUGIN]
                events = {h["eventName"] for h in hooks}
                expected_events = {"sessionStart", "preToolUse", "postToolUse", "stop"}
                if hook_result["errors"] or events != expected_events:
                    raise RuntimeError({"hook_errors": hook_result["errors"], "events": sorted(events)})
                if any(not h["sourcePath"].endswith("/hooks/codex.json") for h in hooks):
                    raise RuntimeError("Codex discovered the wrong hook configuration")
                print(json.dumps({
                    "result": "PASS", "client": initialized["userAgent"],
                    "marketplace": "discovered", "installation": "passed",
                    "skills_loaded": sorted(skills), "skill_errors": errors,
                    "hook_events_discovered": sorted(events),
                    "hook_trust": sorted({h["trustStatus"] for h in hooks}),
                    "hook_runtime": "not exercised or trusted by this check",
                }, indent=2))
            finally:
                server.stdin.close()
                try:
                    server.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait(timeout=5)
                reader.join(timeout=1)
                server.stdout.close()


if __name__ == "__main__":
    check()
