from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).parents[1] / "skills/docs-sync/scripts"
RESOLVER = (SCRIPTS / "resolve_target.py").read_text()
GATE = (SCRIPTS / "readiness.py").read_text()


class TargetResolutionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name)
        self.git("init", "--quiet", "--initial-branch=main")
        self.commit()
        self.previous = self.git("rev-parse", "HEAD")
        self.git("tag", "v0.3.6")
        self.commit()
        self.current = self.git("rev-parse", "HEAD")
        self.git("tag", "v0.4.0a9")
        self.git("tag", "-a", "v0.4.0a11", "-m", "test release")
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")

    def git(self, *arguments):
        environment = os.environ.copy()
        environment.update(
            GIT_AUTHOR_NAME="Documentation test",
            GIT_AUTHOR_EMAIL="docs@example.test",
            GIT_COMMITTER_NAME="Documentation test",
            GIT_COMMITTER_EMAIL="docs@example.test",
        )
        return subprocess.check_output(
            [
                "git",
                "-C",
                str(self.repo),
                "-c",
                "commit.gpgsign=false",
                "-c",
                "tag.gpgsign=false",
                "-c",
                "core.hooksPath=/dev/null",
                *arguments,
            ],
            env=environment,
            text=True,
            stderr=subprocess.PIPE,
        ).strip()

    def commit(self):
        self.git(
            "commit", "--quiet", "--allow-empty", "-m", "test: create source fixture"
        )

    def resolve(self, requested):
        output = StringIO()
        with (
            patch.object(sys, "argv", ["resolver", str(self.repo), requested]),
            redirect_stdout(output),
        ):
            exec(compile(RESOLVER, "resolve_target.py", "exec"), {})
        return json.loads(output.getvalue())

    def test_latest_includes_prereleases_and_peels_annotated_tags(self):
        for requested in ("", "latest"):
            with self.subTest(requested=requested):
                result = self.resolve(requested)
                self.assertEqual(result["ref"], "v0.4.0a11")
                self.assertEqual(result["sha"], self.current)

    def test_latest_excludes_tags_outside_origin_main(self):
        self.git("checkout", "--quiet", "-b", "unmerged")
        self.commit()
        self.git("tag", "v9.0.0")
        self.assertEqual(self.resolve("latest")["ref"], "v0.4.0a11")

    def test_stable_release_outranks_its_prerelease(self):
        self.git("tag", "v0.4.0")
        self.git("tag", "v0.4.0rc1")
        self.assertEqual(self.resolve("latest")["ref"], "v0.4.0")

    def test_specified_version_tag_commit_and_main_are_honored(self):
        for requested in ("0.3.6", "v0.3.6", self.previous):
            with self.subTest(requested=requested):
                result = self.resolve(requested)
                self.assertEqual(result["requested"], requested)
                self.assertEqual(result["sha"], self.previous)
        self.assertEqual(self.resolve("main")["sha"], self.current)

    def test_unknown_version_never_falls_back_to_latest(self):
        for requested in ("__missing_docs_trial_version__", "v9.9.9"):
            with (
                self.subTest(requested=requested),
                self.assertRaisesRegex(
                    SystemExit, "Unknown requested runtime revision"
                ),
            ):
                self.resolve(requested)

    def test_latest_without_a_release_tag_reports_failure(self):
        for tag in self.git("tag").splitlines():
            self.git("tag", "--delete", tag)
        with self.assertRaisesRegex(SystemExit, "No release tag"):
            self.resolve("latest")


class ReadinessGateTests(unittest.TestCase):
    required = (
        "docs typecheck",
        "cli generator suite",
        "api generator suite",
        "production build",
        "site and syntax browser tests",
        "dev navigation browser tests",
        "whitespace check",
        "internal link targets",
        "fragment and anchor targets",
        "copied source links",
        "navigation registration",
        "copy fidelity",
        "regeneration reproducibility",
        "cli reference coverage",
        "api reference totals",
        "public example parse",
        "diff scope",
        "originals untouched",
    )

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.manifest = {
            "status": "ready",
            "blockers": [],
            "verification": {
                "checks": [
                    {
                        "name": name,
                        "status": "pass",
                        "exit_code": 0,
                    }
                    for name in self.required
                ]
            },
        }

    def gate(self):
        path = self.directory / "run.json"
        path.write_text(json.dumps(self.manifest))
        report = self.directory / "report.md"
        report.write_text("# Docs refresh\n\n- **Status:** ready\n")
        output = StringIO()
        with patch.object(sys, "argv", ["gate", str(path)]), redirect_stdout(output):
            try:
                exec(compile(GATE, "readiness.py", "exec"), {})
            except SystemExit as error:
                exit_code = error.code
        return exit_code, json.loads(path.read_text()), report.read_text()

    def test_all_checks_pass(self):
        exit_code, manifest, report = self.gate()
        self.assertEqual(exit_code, 0)
        self.assertEqual(manifest["status"], "ready")
        self.assertIn("**Status:** ready", report)

    def test_nonzero_copy_check_blocks_even_when_marked_pass(self):
        check = next(
            c
            for c in self.manifest["verification"]["checks"]
            if c["name"] == "copy fidelity"
        )
        check["exit_code"] = 1
        exit_code, manifest, _ = self.gate()
        self.assertEqual(exit_code, 1)
        self.assertIn("copy fidelity", manifest["readiness_gate"]["failures"])

    def test_preexisting_example_failure_blocks_a_ready_claim(self):
        check = next(
            c
            for c in self.manifest["verification"]["checks"]
            if c["name"] == "public example parse"
        )
        check.update(status="pre-existing", exit_code=1)
        exit_code, manifest, report = self.gate()
        self.assertEqual(exit_code, 1)
        self.assertEqual(manifest["status"], "blocked")
        self.assertIn("public example parse", manifest["readiness_gate"]["failures"])
        self.assertIn("**Status:** blocked", report)
        self.assertNotIn("**Status:** ready", report)

    def test_missing_required_check_blocks_a_ready_claim(self):
        self.manifest["verification"]["checks"] = [
            c
            for c in self.manifest["verification"]["checks"]
            if c["name"] != "production build"
        ]
        exit_code, manifest, _ = self.gate()
        self.assertEqual(exit_code, 1)
        self.assertIn("production build", manifest["readiness_gate"]["failures"])

    def test_recorded_blockers_are_preserved_and_prevent_readiness(self):
        self.manifest["blockers"] = [{"reason": "Source fetch failed"}]
        exit_code, manifest, _ = self.gate()
        self.assertEqual(exit_code, 1)
        self.assertEqual(manifest["blockers"], self.manifest["blockers"])
        self.assertIn("recorded blockers", manifest["readiness_gate"]["failures"])


if __name__ == "__main__":
    unittest.main()
