"""Behavior tests for catalog reconciliation and guarded recovery."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

SCRIPT = Path(__file__).with_name("skills_registry.py")
if not SCRIPT.is_file():
    SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "skills_registry.py"
sys.path.insert(0, str(SCRIPT.parent))
from skills_registry import archive_owned_sources  # noqa: E402


class RegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.codex = root / "C" / ".codex"
        self.agents = root / "C" / ".agents"
        self.utilities = root / "E" / "utilitarios"
        self.projects = root / "projects"
        self.catalog = self.codex / "skills-registry" / "CODEX_SKILLS_REGISTRY.md"
        self.mirror = self.utilities / "CODEX_SKILLS_REGISTRY.md"
        self.history = self.utilities / "codex-skills-backup" / "catalog-history"
        self._skill(self.codex / "skills" / "alpha", "alpha", "1.0.0")
        self._skill(self.projects / "client" / ".agents" / "skills" / "beta", "beta", "1")

    @staticmethod
    def _skill(directory: Path, name: str, version: str) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Help with {name}.\nmetadata:\n  version: '{version}'\n---\n\n# {name}\n",
            encoding="utf-8",
        )

    def run_command(self, command: str, *extra: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--codex-home", str(self.codex), "--agents-home", str(self.agents),
             "--utilities", str(self.utilities), "--project-root", str(self.projects), command, *extra],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, expect, result.stdout + result.stderr)
        return result

    def test_reconcile_detects_external_install_update_and_removal(self) -> None:
        self.run_command("reconcile", "--no-plugins")
        first = json.loads((self.codex / "skills-registry" / "skills-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual({item["name"] for item in first["skills"]}, {"alpha", "beta"})
        self.assertEqual(self.catalog.read_bytes(), self.mirror.read_bytes())
        self.run_command("verify")

        self._skill(self.codex / "skills" / "alpha", "alpha", "1.1.0")
        self._skill(self.agents / "skills" / "gamma", "gamma", "2")
        self.run_command("reconcile", "--no-plugins", "--event", "update")
        second = json.loads((self.codex / "skills-registry" / "skills-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual({item["name"] for item in second["skills"]}, {"alpha", "beta", "gamma"})
        self.assertGreaterEqual(len(list(self.history.glob("*.md"))), 2)
        self.run_command("verify")

        (self.projects / "client" / ".agents" / "skills" / "beta" / "SKILL.md").unlink()
        self.run_command("reconcile", "--no-plugins", "--event", "remove")
        third = json.loads((self.codex / "skills-registry" / "skills-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual({item["name"] for item in third["skills"]}, {"alpha", "gamma"})

    def test_tampered_primary_is_never_overwritten_by_backup(self) -> None:
        self.run_command("reconcile", "--no-plugins")
        self.catalog.write_text(self.catalog.read_text(encoding="utf-8") + "manual change\n", encoding="utf-8")
        before = self.catalog.read_bytes()
        self.run_command("reconcile", "--no-plugins", expect=1)
        self.assertEqual(self.catalog.read_bytes(), before)
        self.run_command("verify", expect=1)

    def test_restore_requires_hash_and_explicit_apply(self) -> None:
        self.run_command("reconcile", "--no-plugins")
        original = self.catalog.read_bytes()
        snapshot = next(self.history.glob("*.md"))
        expected = snapshot.with_suffix(".sha256").read_text(encoding="utf-8").strip()
        self._skill(self.codex / "skills" / "alpha", "alpha", "2.0.0")
        self.run_command("reconcile", "--no-plugins")
        self.run_command("restore", "--snapshot-id", snapshot.stem, "--expected-sha256", expected, expect=1)
        self.run_command("restore", "--snapshot-id", snapshot.stem, "--expected-sha256", "0" * 64, "--apply", expect=1)
        self.run_command("restore", "--snapshot-id", snapshot.stem, "--expected-sha256", expected, "--apply")
        self.assertEqual(self.catalog.read_bytes(), original)
        self.run_command("verify")

    def test_stale_guard_avoids_repeated_scan(self) -> None:
        self.run_command("reconcile", "--no-plugins")
        result = self.run_command("reconcile", "--no-plugins", "--if-stale-days", "7")
        self.assertIn("SKIP", result.stdout)

    def test_owned_source_archive_contains_tracked_scripts_and_blocks_secrets(self) -> None:
        repo = self.utilities / "dev-assistant"
        (repo / "scripts").mkdir(parents=True)
        (repo / "SKILL.md").write_text("---\nname: dev-assistant\ndescription: Test.\n---\n", encoding="utf-8")
        (repo / "scripts" / "check.ps1").write_text("Write-Output 'ok'\n", encoding="utf-8")
        for args in (("init",), ("config", "user.name", "Registry Test"), ("config", "user.email", "registry@example.invalid"),
                     ("add", "SKILL.md", "scripts/check.ps1"), ("commit", "-m", "test source")):
            result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        backup = self.utilities / "codex-skills-backup"
        warnings = archive_owned_sources(self.utilities, backup)
        self.assertFalse(any("dev-assistant" in item and "bloqueado" in item for item in warnings))
        package = next((backup / "owned-sources" / "dev-assistant").glob("*.zip"))
        with ZipFile(package) as archive:
            self.assertIn("scripts/check.ps1", archive.namelist())
        self.assertTrue(package.with_suffix(".sha256").is_file())

        (repo / ".env").write_text("SECRET=example\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", ".env"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-m", "test blocked file"], check=True, capture_output=True)
        warnings = archive_owned_sources(self.utilities, backup)
        self.assertTrue(any("dev-assistant" in item and "bloqueado" in item for item in warnings))


if __name__ == "__main__":
    unittest.main()
