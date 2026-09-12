---
name: toolang-coding-conventions
description: Use when designing, authoring, formatting, or reviewing Toolang agents, agics, flows, caps, prompts, and `.too` examples. Load the canonical conventions for style; use `toolang-grammar` for syntax and `toolang-cli` for commands.
---

# Toolang Coding Conventions

Use the canonical [Toolang authoring conventions](https://toolang.ai/reference/toolang-conventions)
for naming, structure, defaults, messages, flow design, comments, and resource
selection. This skill intentionally does not carry a second convention manual.

Before authoring or reviewing Toolang source:

1. Load the sections relevant to the requested artifact.
2. Apply them as style guidance without treating them as grammar.
3. Preserve the user's intent and stable source order unless the requested
   change requires otherwise.
4. Validate the result with the target parser and formatter.

If the website is unavailable but an authorized checkout of `toolang-docs` is
present, use `docs/pages/reference/toolang-conventions.mdx` from that checkout.
If neither source is accessible, say that the current conventions could not be
loaded rather than relying on a remembered copy.
