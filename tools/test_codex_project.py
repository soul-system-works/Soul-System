"""Check instruction wiring preserves existing projects and detects stale paths.

Run: python3 -B -m unittest discover -s tools -p 'test_codex_project.py' -v
"""

from contextlib import redirect_stderr
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("codex_project", Path(__file__).with_name("codex-project.py"))
wiring = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wiring)


class ProjectWiring(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.project = Path(self.temporary.name)

    def test_existing_instructions_and_claude_file_survive_idempotent_wiring(self):
        original = "# Project\n\nKeep the public API stable.\n"
        (self.project / "AGENTS.md").write_text(original)
        claude = self.project / "CLAUDE.md"
        claude.write_text("@existing/contract.md\n**Stage:** released\n")
        before = claude.read_bytes()
        target = wiring.wire(self.project)
        once = target.read_bytes()
        wiring.wire(self.project)
        self.assertEqual(once, target.read_bytes())
        self.assertTrue(target.read_text().startswith(original))
        self.assertEqual(claude.read_bytes(), before)
        self.assertTrue(wiring.status(self.project)["contract_matches_installed"])
        self.assertFalse((self.project / ".soul").exists())

    def test_override_is_active_and_base_instructions_are_untouched(self):
        base = self.project / "AGENTS.md"
        base.write_text("Base instructions\n")
        override = self.project / "AGENTS.override.md"
        override.write_text("Active instructions\n")
        self.assertEqual(wiring.wire(self.project), override)
        self.assertEqual(base.read_text(), "Base instructions\n")
        self.assertTrue(wiring.status(self.project)["contract_readable"])

    def test_crlf_content_outside_block_survives(self):
        target = self.project / "AGENTS.md"
        prefix = b"# Windows project\r\nKeep this spacing.  \r\n"
        target.write_bytes(prefix)
        wiring.wire(self.project)
        target.write_bytes(target.read_bytes() + b"\r\nTrailing rules.\r\n")
        wiring.wire(self.project)
        self.assertTrue(target.read_bytes().startswith(prefix))
        self.assertTrue(target.read_bytes().endswith(b"\r\nTrailing rules.\r\n"))

    def test_empty_override_does_not_hide_existing_base_rules(self):
        base = self.project / "AGENTS.md"
        base.write_text("Keep project rules active.\n")
        override = self.project / "AGENTS.override.md"
        override.write_text("\n\n")
        self.assertEqual(wiring.wire(self.project), base)
        self.assertTrue(base.read_text().startswith("Keep project rules active.\n"))
        self.assertEqual(override.read_text(), "\n\n")

    def test_malformed_markers_refuse_without_writing(self):
        target = self.project / "AGENTS.md"
        for text in (wiring.START, wiring.END, wiring.START * 2 + wiring.END * 2, wiring.END + wiring.START):
            target.write_text(text)
            with self.assertRaises(ValueError):
                wiring.wire(self.project)
            self.assertEqual(target.read_text(), text)

    def test_missing_reference_is_a_gap(self):
        self.assertFalse(wiring.status(self.project)["contract_readable"])
        target = wiring.wire(self.project)
        text = target.read_text()
        reference = wiring.contract_reference(text)
        target.write_text(text.replace(str(reference), str(self.project / "missing.md")))
        self.assertFalse(wiring.status(self.project)["contract_readable"])

    def test_different_contract_is_stale(self):
        target = wiring.wire(self.project)
        other = self.project / "old-contract.md"
        other.write_text("Old instructions\n")
        text = target.read_text()
        reference = wiring.contract_reference(text)
        target.write_text(text.replace(str(reference), str(other)))
        status = wiring.status(self.project)
        self.assertTrue(status["contract_readable"])
        self.assertFalse(status["contract_matches_installed"])
        self.assertIn("unknown", status["gate"])

    def test_symlink_is_not_followed_for_writes(self):
        other = self.project / "outside.md"
        other.write_text("Keep\n")
        (self.project / "AGENTS.md").symlink_to(other)
        with self.assertRaises(ValueError):
            wiring.wire(self.project)
        self.assertEqual(other.read_text(), "Keep\n")

    def test_source_repo_cannot_be_initialized(self):
        with self.assertRaises(ValueError):
            wiring.wire(wiring.ROOT)

    def test_source_repo_is_recognised_by_content_not_path(self):
        # The helper usually runs from the installed cache, where ROOT is never
        # the source checkout; a ROOT comparison guarded nothing there.
        clone = self.project / "clone"
        (clone / "findings" / "open").mkdir(parents=True)
        (clone / "operations").mkdir()
        (clone / "operations" / "CLAUDE.md").write_text("contract\n")
        (clone / "SYSTEM-VERSION.md").write_text("2\n")
        with self.assertRaises(ValueError):
            wiring.wire(clone)
        self.assertFalse((clone / "AGENTS.md").exists())
        # An adopting project with an empty findings/open/ is not the source repo.
        (clone / "SYSTEM-VERSION.md").unlink()
        self.assertEqual(wiring.wire(clone), clone / "AGENTS.md")

    def cache_install(self, version="9.9.9", contract="contract\n"):
        home = self.project / "codex-home"
        root = home / "plugins" / "cache" / "mkt" / "soul-system" / version
        (root / "operations").mkdir(parents=True)
        (root / "operations" / "CLAUDE.md").write_text(contract)
        return home, root

    def wire_from(self, root):
        target = self.project / "adopter"
        target.mkdir(exist_ok=True)
        err = io.StringIO()
        with patch.object(wiring, "ROOT", root), redirect_stderr(err):
            wiring.wire(target)
        return wiring.contract_reference((target / "AGENTS.md").read_text()), err.getvalue()

    def test_versioned_cache_only_is_pinned_with_warning(self):
        home, root = self.cache_install()
        reference, err = self.wire_from(root)
        self.assertEqual(reference, root / "operations" / "CLAUDE.md")
        self.assertIn("pinned to plugin version 9.9.9", err)
        self.assertIn("re-run $soul-system:soul-init", err)

    def test_local_marketplace_source_is_preferred(self):
        home, root = self.cache_install()
        source = self.project / "checkout"
        (source / "operations").mkdir(parents=True)
        (source / "operations" / "CLAUDE.md").write_text("contract\n")
        (home / "config.toml").write_text(
            f'[marketplaces.mkt]\nsource_type = "local"\nsource = "{source}"\n')
        reference, err = self.wire_from(root)
        self.assertEqual(reference, source / "operations" / "CLAUDE.md")
        self.assertEqual(err, "")

    def test_git_marketplace_tmp_clone_is_not_used(self):
        # Unversioned but under .tmp with undocumented permanence: a reference that
        # could vanish silently is worse than a pinned one that warns (SOUL-F038).
        home, root = self.cache_install()
        clone = home / ".tmp" / "marketplaces" / "mkt"
        (clone / "operations").mkdir(parents=True)
        (clone / "operations" / "CLAUDE.md").write_text("contract\n")
        reference, err = self.wire_from(root)
        self.assertEqual(reference, root / "operations" / "CLAUDE.md")
        self.assertIn("pinned to plugin version 9.9.9", err)

    def test_different_unversioned_contract_falls_back_to_pinned(self):
        home, root = self.cache_install()
        source = self.project / "checkout"
        (source / "operations").mkdir(parents=True)
        (source / "operations" / "CLAUDE.md").write_text("newer contract\n")
        (home / "config.toml").write_text(
            f'[marketplaces.mkt]\nsource_type = "local"\nsource = "{source}"\n')
        reference, err = self.wire_from(root)
        self.assertEqual(reference, root / "operations" / "CLAUDE.md")
        self.assertIn("pinned to plugin version 9.9.9", err)

    def test_reference_is_absolute_even_under_home(self):
        home, root = self.cache_install()
        with patch.object(Path, "home", return_value=self.project):
            reference, _ = self.wire_from(root)
        self.assertTrue(reference.is_absolute())
        self.assertNotIn("`~/", (self.project / "adopter" / "AGENTS.md").read_text())

    def test_missing_installed_contract_prevents_wiring(self):
        with patch.object(wiring, "ROOT", self.project / "missing-plugin"):
            with self.assertRaises(OSError):
                wiring.wire(self.project)
        self.assertFalse((self.project / "AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()
