---
name: toolang-cli
description: Use when installing, invoking, inspecting, running, serving, or troubleshooting Toolang through `toolang`, `too`, `caps`, or a development entry point. Load the canonical CLI manual and confirm the active executable. Use `toolang-grammar` for `.too` syntax.
---

# Toolang CLI

Use the canonical [Toolang CLI reference](https://toolang.ai/reference/toolang-cli)
for commands and options. This skill intentionally does not carry a second CLI
manual.

For each operation:

1. Resolve the intended executable and command prefix. In a uv-managed Toolang
   checkout this is normally `uv run toolang`; an installed environment may
   use `toolang` or `too`.
2. Confirm that exact target with `--version` and `--help`.
3. Load the relevant canonical manual section, then inspect command-specific or
   generated script help before forming the invocation.
4. Keep the same prefix throughout validation and execution.

The runtime protocol identifies the current executor. A shell command may
resolve a different global installation, so report versions with their command
prefixes and do not let one silently stand in for the other. If published docs
and active help differ, follow the active target and identify the discrepancy.
Do not invent a command when neither source is available.
