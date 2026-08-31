#!/usr/bin/env python3
"""Validate public Toolang agents and capability files."""

from __future__ import annotations

from pathlib import Path
import re

import frontmatter
from toolang.base.types.message import TextPart
from toolang.catalog.cap import CapFile
from toolang.lang.ast import Program
from toolang.lang.input import resolve_input_parts


ROOT = Path(__file__).resolve().parents[1]
CAP_FILES = {
    "psyche": ("psyches", "*.md"),
    "prompt": ("prompts", "*.md"),
    "service": ("services", "*.md"),
    "skill": ("skills", "*/SKILL.md"),
}
WITH_REF = re.compile(r"^with (psyche|prompt|service|skill) briceyan/([^\s]+)$")
PROMPT_NAME = re.compile(r"^[A-Za-z_][\w-]*$")


def main() -> None:
    agents = sorted(ROOT.glob("*.too"))
    if not agents:
        raise ValueError("catalog has no public agents")

    for path in agents:
        source = path.read_text(encoding="utf-8")
        program = Program.from_source(source)
        if program.find_agic("default") is None and program.find_flow("default") is None:
            raise ValueError(f"{path.name} has no default runnable")
        _validate_local_refs(path, source)
        if path.name == "dev.too":
            _validate_dev_input(program)

    cap_count = 0
    for kind, (directory, pattern) in CAP_FILES.items():
        for path in sorted((ROOT / directory).glob(pattern)):
            name = path.parent.name if kind == "skill" else path.stem
            content = path.read_text(encoding="utf-8")
            CapFile.parse(content, kind=kind, name=name, path=path)
            if kind == "prompt":
                _validate_prompt(name, content)
            cap_count += 1

    print(f"Validated {len(agents)} agents and {cap_count} caps.")


def _validate_local_refs(path: Path, source: str) -> None:
    for line in source.splitlines():
        match = WITH_REF.fullmatch(line.strip())
        if match is None:
            continue
        kind, name = match.groups()
        directory, _pattern = CAP_FILES[kind]
        target = (
            ROOT / directory / name / "SKILL.md"
            if kind == "skill"
            else ROOT / directory / f"{name}.md"
        )
        if not target.is_file():
            raise ValueError(f"{path.name} references missing local {kind}: {name}")


def _validate_dev_input(program: Program) -> None:
    agic = program.find_agic("default")
    if agic is None:
        raise ValueError("dev.too has no default agic")
    parts = tuple(
        part
        for message in agic.messages
        for part in resolve_input_parts(
            message.content,
            values={"_": (TextPart("USER_INPUT_SENTINEL"),)},
            types={"_": "Part[]"},
        )
    )
    if not any(
        "USER_INPUT_SENTINEL" in part.text
        for part in parts
        if isinstance(part, TextPart)
    ):
        raise ValueError("dev.too does not forward primary user input")


def _validate_prompt(name: str, content: str) -> None:
    if PROMPT_NAME.fullmatch(name) is None:
        raise ValueError(f"invalid prompt name: {name}")
    post = frontmatter.loads(content)
    lines = ["prompt validation_prompt:"]
    params = post.metadata.get("params")
    if params is not None:
        lines.extend((f"  params = {params}", ""))
    lines.extend(f"  {line}" if line else "" for line in post.content.splitlines())
    program = Program.from_source("\n".join(lines) + "\n")
    prompt = program.caps[0]
    arguments = " ".join(f"{parameter.name}=example" for parameter in prompt.params)
    call = f"$validation_prompt {arguments} -- PROMPT_INPUT_SENTINEL"
    parts = resolve_input_parts(call, program=program)
    if not any(
        "PROMPT_INPUT_SENTINEL" in part.text
        for part in parts
        if isinstance(part, TextPart)
    ):
        raise ValueError(f"prompt {name} does not forward attached input")


if __name__ == "__main__":
    main()
