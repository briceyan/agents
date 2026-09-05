---
name: toolang-coding-conventions
description: Use when authoring or reviewing Toolang `.too` files for clear naming, visible intent and data flow, natural-language instructions, concise types, useful documentation comments, and readable flows. This skill covers style; use `toolang-grammar` for language rules and `toolang-cli` for commands and operation.
---

# Toolang Coding Conventions

Write Toolang that explains itself. Prefer meaningful declarations, explicit
inputs, and natural prose over comments or ceremony.

This skill answers how to write Toolang well. Use `toolang-grammar` to resolve
exact syntax, types, and execution semantics. Use `toolang-cli` for installing,
downloading, running, serving, and inspecting Toolang programs.

Before drafting or reviewing a `.too` file, read
`references/authoring-conventions.md`. Apply the rules that fit the artifact;
do not add structure merely to demonstrate language features.

## Authoring workflow

1. Name the artifact for the role or outcome a user will recognize.
2. Make the user's input and the intended result visible before adding control
   flow.
3. Express a single model interaction as an `agic`; use a `flow` only when its
   stages, branching, iteration, selection, or concurrency carry meaning.
4. Add only the capabilities and annotations required by the work.
5. Read the source top to bottom as a short explanation of the job.
6. Remove redundant types, comments, stages, and instructions.
7. Format and validate the result with the Toolang version it targets.

## Review priorities

Review in this order:

1. User intent is preserved, including an explicit `{{_}}` where the primary
   input is meant to affect a model request.
2. Names communicate roles and actions without requiring comments.
3. Flow stages describe a real work process and move the right value forward.
4. Natural-language bodies are direct, specific, and readable as prose.
5. Types and comments add information instead of repeating defaults or syntax.
6. Concurrency, iteration, and selected capabilities are bounded and justified
   by the task.

When a style recommendation conflicts with the target Toolang grammar or an
explicit repository convention, follow the grammar or repository and note the
exception.
