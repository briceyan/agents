"""Resolve source revisions and create one isolated documentation refresh run."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tomllib
from uuid import uuid4

from packaging.version import InvalidVersion, Version


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def snapshot(repo: Path) -> dict[str, str]:
    return {
        "head": git(repo, "rev-parse", "HEAD"),
        "status": git(
            repo,
            "status",
            "--porcelain",
            "--untracked-files=all",
            "--",
            ".",
            ":!.toolang",
        ),
    }


def prepare(
    docs: Path,
    runtime: Path | None,
    grammar: Path | None,
    requested: str,
    directory: Path | None = None,
) -> Path:
    docs = Path(git(docs.resolve(), "rev-parse", "--show-toplevel"))
    primary = Path(
        git(docs, "worktree", "list", "--porcelain")
        .splitlines()[0]
        .removeprefix("worktree ")
    )
    repos = {
        "docs": docs,
        "runtime": runtime or primary.parent / "toolang",
        "grammar": grammar or primary.parent / "tree-sitter-toolang",
    }
    repos = {key: path.resolve() for key, path in repos.items()}
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + str(uuid4())
    directory = (
        directory.resolve() if directory else docs / ".toolang/docs-refresh" / run_id
    )
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "run.json"
    if path.exists():
        raise ValueError("Run manifest already exists: " + str(path))
    manifest = {
        "status": "resolving",
        "run_id": run_id,
        "run_dir": str(directory),
        "requested_version": requested,
        "invocation_workdir": str(docs),
        "original_checkout_paths": {key: str(repo) for key, repo in repos.items()},
        "original_heads": {},
        "original_statuses": {},
        "worktrees": {},
        "copied_sources": [],
        "repairs": [],
        "checks": [],
        "blockers": [],
    }

    def save():
        path.write_text(json.dumps(manifest, indent=2) + "\n")

    def command(repo: Path, args: list[str]) -> str:
        result = subprocess.run(
            args,
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=600,
        )
        with (directory / "commands.log").open("a") as log:
            log.write(
                f"\n$ {shlex.join(args)}\nCWD: {repo}\n{result.stdout}{result.stderr}\nExit: {result.returncode}\n"
            )
        if result.returncode:
            raise RuntimeError(
                f"{shlex.join(args)} exited {result.returncode}: {result.stderr.strip()}"
            )
        return result.stdout.strip()

    save()
    try:
        names = {
            "docs": "toolang-docs",
            "runtime": "toolang",
            "grammar": "tree-sitter-toolang",
        }
        for key, repo in repos.items():
            origin = git(repo, "config", "--get", "remote.origin.url")
            expected = "github.com[:/]openhat-ai/" + names[key] + r"(?:\.git)?/?$"
            if not re.search(expected, origin):
                raise ValueError(f"Unexpected {key} origin: {origin}")
            baseline = snapshot(repo)
            manifest["original_heads"][key] = baseline["head"]
            manifest["original_statuses"][key] = baseline["status"]
        for key in ("runtime", "grammar"):
            command(repos[key], ["git", "fetch", "origin", "--tags"])
        command(docs, ["git", "fetch", "origin", "main"])
        resolved = json.loads(
            command(
                docs,
                [
                    sys.executable,
                    str(Path(__file__).with_name("resolve_target.py")),
                    str(repos["runtime"]),
                    requested,
                ],
            )
        )
        manifest["runtime_sha"] = resolved["sha"]
        manifest["runtime_ref"] = resolved["ref"]
        project = tomllib.loads(
            git(repos["runtime"], "show", resolved["sha"] + ":pyproject.toml")
        )["project"]
        manifest["runtime_version"] = project["version"]
        pins = [
            re.fullmatch(r"tree-sitter-toolang\s*==\s*([^; ]+)(?:\s*;.*)?", dep)
            for dep in project["dependencies"]
        ]
        pins = [pin[1] for pin in pins if pin]
        if len(pins) != 1:
            raise ValueError("Expected one exact tree-sitter-toolang dependency")
        matches = []
        for tag in git(repos["grammar"], "tag").splitlines():
            try:
                if Version(tag.removeprefix("v")) == Version(pins[0]):
                    matches.append(
                        (tag, git(repos["grammar"], "rev-parse", tag + "^{commit}"))
                    )
            except InvalidVersion:
                continue
        if not matches or len({sha for _, sha in matches}) != 1:
            raise ValueError("Missing or ambiguous grammar tag for " + pins[0])
        manifest.update(
            grammar_version=pins[0],
            grammar_ref=matches[0][0],
            grammar_sha=matches[0][1],
            docs_base_sha=git(docs, "rev-parse", "origin/main"),
        )
        branch = (
            "codex/docs-sync-"
            + re.sub(r"[^A-Za-z0-9._-]", "-", project["version"])
            + "-"
            + run_id
        )
        manifest["docs_branch"] = branch
        for key, name, sha in (
            ("runtime", "toolang", manifest["runtime_sha"]),
            ("grammar", "tree-sitter-toolang", manifest["grammar_sha"]),
        ):
            target = directory / name
            command(
                repos[key], ["git", "worktree", "add", "--detach", str(target), sha]
            )
            manifest["worktrees"][name] = str(target)
            save()
        target = directory / "toolang-docs"
        command(
            docs,
            [
                "git",
                "worktree",
                "add",
                "--no-track",
                "-b",
                branch,
                str(target),
                manifest["docs_base_sha"],
            ],
        )
        manifest["worktrees"]["toolang-docs"] = str(target)
        manifest["status"] = "prepared"
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        manifest["status"] = "blocked"
        manifest["blockers"].append(str(error))
    save()
    print(
        json.dumps(
            {
                "manifest": str(path),
                "status": manifest["status"],
                "blockers": manifest["blockers"],
            }
        )
    )
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs-repo", type=Path, default=Path.cwd())
    parser.add_argument("--runtime-repo", type=Path)
    parser.add_argument("--grammar-repo", type=Path)
    parser.add_argument("--version", default="")
    parser.add_argument("--run-dir", type=Path)
    args = parser.parse_args()
    manifest = prepare(
        args.docs_repo, args.runtime_repo, args.grammar_repo, args.version, args.run_dir
    )
    raise SystemExit(
        1 if json.loads(manifest.read_text())["status"] == "blocked" else 0
    )
