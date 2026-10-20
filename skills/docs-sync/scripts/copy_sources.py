"""Copy the two pinned upstream documents with reproducible MDX adaptations."""

from __future__ import annotations

import json
import posixpath
import re
import sys
from pathlib import Path
from urllib.parse import quote, urlsplit


def render(source: str, *, title: str, repo: str, sha: str, path: str) -> str:
    base = f"https://github.com/{repo}"

    def link(match: re.Match[str]) -> str:
        target = match[2]
        if urlsplit(target).scheme or target.startswith(("#", "/", "//")):
            return match[0]
        relative, separator, fragment = target.partition("#")
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), relative))
        target = f"{base}/blob/{sha}/{quote(resolved, safe='/')}"
        if separator:
            target += "#" + fragment
        return f"[{match[1]}]({target})"

    # Keep fenced code and inline code exact; MDX syntax outside code is escaped.
    lines = source.splitlines(keepends=True)
    fence = None
    result = []
    for line in lines:
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            result.append(line)
            continue
        if fence:
            result.append(line)
            continue
        chunks = re.split(r"(`+[^`\n]*`+)", line)
        for index in range(0, len(chunks), 2):
            text = re.sub(r"\[([^\]]+)\]\(([^\s)]+)\)", link, chunks[index])
            text = text.replace("<", "&lt;").replace(">", "&gt;")
            text = text.replace("{", "\\{").replace("}", "\\}")
            chunks[index] = text
        result.append("".join(chunks))
    body = "".join(result)
    body = re.sub(r"\A# [^\n]+\n", "", body, count=1).lstrip("\n")
    source_url = f"{base}/blob/{sha}/{path}"
    return f"# {title}\n\nSource: [{repo}/{path}]({source_url}) at `{sha}`.\n\n{body.rstrip()}\n"


def copy(manifest_path: Path) -> None:
    manifest = json.loads(manifest_path.read_text())
    if manifest["status"] == "blocked":
        raise SystemExit("Preparation is blocked; no files copied")
    worktrees = manifest["worktrees"]
    copies = (
        (
            "toolang",
            "runtime_sha",
            "docs/authoring.md",
            "docs/pages/docs/toolang-conventions.mdx",
            "Authoring conventions",
        ),
        (
            "tree-sitter-toolang",
            "grammar_sha",
            "GRAMMAR.md",
            "docs/pages/reference/toolang-grammar.mdx",
            "Grammar",
        ),
    )
    manifest["copied_sources"] = []
    for name, sha_key, source, destination, title in copies:
        text = (Path(worktrees[name]) / source).read_text()
        target = Path(worktrees["toolang-docs"]) / destination
        target.write_text(
            render(
                text,
                title=title,
                repo=f"openhat-ai/{name}",
                sha=manifest[sha_key],
                path=source,
            )
        )
        manifest["copied_sources"].append(
            {
                "source": source,
                "destination": destination,
                "sha": manifest[sha_key],
                "transformations": [
                    "title",
                    "pinned source banner",
                    "relative links",
                    "MDX escaping outside code",
                ],
            }
        )
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(
        json.dumps(
            {
                "manifest": str(manifest_path),
                "copied_sources": manifest["copied_sources"],
            }
        )
    )


if __name__ == "__main__":
    copy(Path(sys.argv[1]))
