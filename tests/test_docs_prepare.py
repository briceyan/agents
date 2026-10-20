from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
from io import StringIO
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).parents[1] / "skills/docs-sync/scripts/prepare.py"
SPEC = importlib.util.spec_from_file_location("docs_prepare", SCRIPT)
PREPARE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREPARE)


class PreparationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.environment = {
            "GIT_AUTHOR_NAME": "Docs test",
            "GIT_AUTHOR_EMAIL": "docs@example.test",
            "GIT_COMMITTER_NAME": "Docs test",
            "GIT_COMMITTER_EMAIL": "docs@example.test",
            "GIT_CONFIG_COUNT": "3",
        }
        self.docs, self.runtime, self.grammar = [
            self.directory / name
            for name in ("toolang-docs", "toolang", "tree-sitter-toolang")
        ]
        for index, repo in enumerate((self.docs, self.runtime, self.grammar)):
            self.environment[f"GIT_CONFIG_KEY_{index}"] = (
                f"url.{repo.as_uri()}.insteadOf"
            )
            self.environment[f"GIT_CONFIG_VALUE_{index}"] = (
                f"https://github.com/openhat-ai/{repo.name}.git"
            )
        self.patcher = patch.dict(os.environ, self.environment)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        for index, repo in enumerate((self.docs, self.runtime, self.grammar)):
            repo.mkdir()
            self.git(repo, "init", "--quiet", "--initial-branch=main")
            self.git(
                repo,
                "remote",
                "add",
                "origin",
                f"https://github.com/openhat-ai/{repo.name}.git",
            )
            self.git(
                repo, "commit", "--quiet", "--allow-empty", "-m", "test: create fixture"
            )
        (self.runtime / "pyproject.toml").write_text(
            '[project]\nversion = "0.4.0a11"\ndependencies = ["tree-sitter-toolang==0.4.0a6"]\n'
        )
        self.git(self.runtime, "add", "pyproject.toml")
        self.git(self.runtime, "commit", "--quiet", "-m", "test: pin grammar")
        self.git(self.runtime, "tag", "v0.4.0a11")
        self.git(self.grammar, "tag", "v0.4.0-alpha.6")

    def git(self, repo, *args):
        return subprocess.check_output(
            [
                "git",
                "-C",
                str(repo),
                "-c",
                "commit.gpgsign=false",
                "-c",
                "tag.gpgsign=false",
                "-c",
                "core.hooksPath=/dev/null",
                *args,
            ],
            text=True,
            stderr=subprocess.PIPE,
        ).strip()

    def prepare(self, version):
        with redirect_stdout(StringIO()):
            path = PREPARE.prepare(self.docs, self.runtime, self.grammar, version)
        return path, json.loads(path.read_text())

    def test_repeated_runs_pin_versions_and_keep_originals_unchanged(self):
        heads = {
            repo: self.git(repo, "rev-parse", "HEAD")
            for repo in (self.docs, self.runtime, self.grammar)
        }
        first_path, first = self.prepare("latest")
        second_path, second = self.prepare("0.4.0a11")
        self.assertEqual(first["status"], "prepared")
        self.assertEqual(second["status"], "prepared")
        self.assertNotEqual(first_path, second_path)
        self.assertNotEqual(first["docs_branch"], second["docs_branch"])
        self.assertEqual(first["runtime_sha"], heads[self.runtime])
        self.assertEqual(first["grammar_sha"], heads[self.grammar])
        self.assertEqual(first["grammar_version"], "0.4.0a6")
        for repo, sha in heads.items():
            self.assertEqual(self.git(repo, "rev-parse", "HEAD"), sha)
            self.assertEqual(
                self.git(repo, "status", "--porcelain", "--", ".", ":!.toolang"), ""
            )
        self.assertEqual(
            self.git(Path(first["worktrees"]["toolang"]), "branch", "--show-current"),
            "",
        )

    def test_unknown_revision_creates_a_blocked_manifest_without_worktrees(self):
        path, manifest = self.prepare("v9.9.9")
        self.assertTrue(path.is_file())
        self.assertEqual(manifest["status"], "blocked")
        self.assertEqual(manifest["worktrees"], {})
        self.assertIn("Unknown requested runtime revision", manifest["blockers"][0])

    def test_missing_exact_grammar_pin_is_not_replaced_with_main(self):
        self.git(self.grammar, "tag", "--delete", "v0.4.0-alpha.6")
        _, manifest = self.prepare("latest")
        self.assertEqual(manifest["status"], "blocked")
        self.assertEqual(manifest["worktrees"], {})
        self.assertIn("Missing or ambiguous grammar tag", manifest["blockers"][0])


if __name__ == "__main__":
    unittest.main()
