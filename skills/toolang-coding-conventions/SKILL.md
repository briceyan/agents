---
name: toolang-coding-conventions
description: Use when authoring or reviewing Toolang `.too` files for clear naming, visible intent and data flow, natural-language instructions, concise types, useful documentation comments, and readable flows. This skill covers style; use `toolang-grammar` for language rules and `toolang-cli` for commands and operation.
---

# Toolang Coding Conventions

Write Toolang that explains itself. Prefer meaningful declarations, visible
inputs and data movement, and natural prose over comments or ceremony.

This skill answers how to write Toolang well. Use `toolang-grammar` to resolve
exact syntax, types, and execution semantics. Use `toolang-cli` for installing,
downloading, running, serving, and inspecting Toolang programs.

The rules needed for normal work are below. Consult
`references/authoring-conventions.md` only for the expanded examples and review
checklist. Apply only the structure that helps the artifact do real work.

## Naming

- Name an agent file for a recognizable role, such as `dev.too`,
  `doc-writer.too`, or `english-coach.too`.
- Name a standalone flow module with a verb phrase describing its outcome,
  such as `review-change.too` or `prepare-brief.too`.
- Use lowercase kebab-case for public filenames and lowercase snake_case for
  runnable names. Give agics and helper flows specific action verbs.
- Remember the distinction: an agent is a role a user talks to, a flow is work
  a user runs, and a runnable is an action within that work.

## Intent and input

Put `{{_}}` in every model request that should depend on the primary input.
Name the desired result, important constraints, and decision standard instead
of relying on conversational context or saying only "help the user."

Use an `agic` for one coherent model-and-tool interaction. Use a `flow` only
when stages, data transformation, selection, iteration, delegation, or
concurrency are meaningful. Keep standalone flow modules self-contained.

## Source style

- Write prompt bodies as direct, grammatical prose with normal capitalization
  and punctuation. Capitalize prose that begins with a reserved lowercase flow
  keyword, or use an explicit `run:` body.
- Use two spaces for structural indentation and let the canonical formatter
  decide declaration spacing and clause order.
- Arrange flows so the transformation of `_` reads from top to bottom. Bind
  the original input before a stage replaces `_` when it will be needed later.
- Bound concurrency and iteration deliberately. Add a stage only when it
  changes, evaluates, selects, combines, or delivers the work.
- Select only the models, tools, caps, recall, and other resources the runnable
  needs. Pure conversation or transformation should not acquire tools.

## Types and documentation

Omit default types unless an explicit contract adds information: omitted or
explicit `_` is `Part[]`, an untyped named parameter is `Text`, and an omitted
return is `Part[]`. Keep `()` for no input, `?` for optional parameters, and
explicit types for structured or otherwise non-default values.

Use `##!` for a concise program description and adjacent `##` comments for
consumer-facing declarations or flow stages. Use `#` only for short
human-facing rationale. Prefer a clearer name or body over a comment that
merely narrates syntax.

## Authoring workflow

1. Name the artifact for the role or outcome a user will recognize.
2. Make the user's input and the intended result visible before adding control
   flow.
3. Express a single model interaction as an `agic`; use a `flow` only when its
   stages, branching, iteration, selection, or concurrency carry meaning.
4. Add only the capabilities and annotations required by the work.
5. Read the source top to bottom as a short explanation of the job.
6. Remove redundant types, comments, stages, and instructions.
7. Format, parse, inspect generated help, and run a focused check with the same
   Toolang version and entry point the artifact targets.

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
