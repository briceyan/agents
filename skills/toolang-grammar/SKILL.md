---
name: toolang-grammar
description: Required before reading, explaining, authoring, or repairing Toolang `.too` syntax and semantics. Load the canonical grammar before producing source. Use `toolang-cli` for commands and `toolang-coding-conventions` for style.
---

# Toolang Grammar

Use the canonical [Toolang grammar reference](https://toolang.ai/reference/toolang-grammar)
for language syntax and semantics. This skill intentionally does not carry a
second grammar manual.

Before explaining or producing `.too` source:

1. Identify the Toolang version that will parse the file.
2. Load the relevant sections of the canonical reference.
3. If the target is a development checkout or differs from the published
   version, inspect that target's parser and tests; the target implementation
   wins.
4. Parse and format the result with that same target version. Inspect generated
   runnable help and run a focused example when practical.

Do not infer Toolang syntax from YAML, another workflow language, an old
example, or the skill catalog summary. If neither the canonical reference nor
the target implementation is accessible, state that limitation instead of
inventing syntax.
