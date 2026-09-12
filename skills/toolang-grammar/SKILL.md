---
name: toolang-grammar
description: Use when reading, explaining, authoring, or repairing Toolang `.too` syntax, runnable signatures, content interpolation, capabilities, or flow semantics. This skill covers the language; use `toolang-cli` for commands and `toolang-coding-conventions` for style.
---

# Toolang Grammar

Treat the installed or checked-out Toolang parser as the final authority. Use
this field guide for current syntax, then parse and format with the exact
Toolang version that will run the file. Do not revive removed syntax such as
`use`, `rank`, `par`, `top`, or `bottom`.

## Program shape

A `.too` program may declare `agent`, external caps with `with`, `struct`,
`context`, `instruct`, inline `psyche`, `skill`, `service`, or `prompt` caps,
`task`, `chore`, `agic`, and `flow`. Agics and flows share one runnable
namespace.

Resident modules are `agent.too` and direct `flows/<name>.too` files. Every
module is independent. An agent module exports all its runnables. A flow module
exports exactly one flow: unnamed `flow:` or a flow whose name matches the file
stem. An unnamed agic is locally named `default`; an unnamed flow is locally
named `main`.

External caps use `with KIND REF`. A declaration must still select the cap in
its matching directive before it becomes active:

```too
with skill briceyan/toolang-grammar

agic explain:
  skills = toolang-grammar

  Explain the Toolang source in {{_}}.
```

## Signatures and values

```text
agic [NAME] [(PARAMETERS)] [-> TYPE]:
flow [NAME] [(PARAMETERS)] [-> TYPE]:
```

- Omitted parameters mean one required primary input `_ : Part[]`.
- `()` means no input. Explicit `_` also defaults to `Part[]`.
- Named parameters follow `_` when it is present; an omitted type is `Text`.
- `name?` is optional. `_` cannot be optional.
- Omitted output is `Part[]`.
- Built-ins are `Text`, `Number`, `Boolean`, `Json`, `Part`, `Part[]`, declared
  structs, and arrays written `T[]`.

`_` is both the primary parameter and a flow's current-value local. Reference
inputs explicitly with `{{_}}` and named values with `{{name}}`. A flow value
statement replaces `_`; `let name = STATEMENT` binds the result to `name`;
`let STATEMENT` discards it. `let name = CONTENT` stores evaluated content
without starting a child run.

## Agics and content

An agic body may select `models`, `psyches`, `skills`, `services`, `tools`,
`recall`, `hands`, and `handoffs`, then define `context`, `instruct`, and model
messages such as `user:` and `assistant:`. An omitted tools directive inherits
the available tools; use `tools = none` when the runnable must not call tools.

Content supports interpolation, `$prompt` calls, and whole-line `@PATH`
includes. To make a leading marker literal, double it: `@@`, `$$`, `//`, or
`::`. `context` supplies information; `instruct` supplies behavioral policy;
`user` carries the user's request.

## Flow statements

Flows execute top to bottom. Bare prose is shorthand for an inline `run`.

```text
run RUNNABLE                 run: CONTENT
seek AGENT RUNNABLE          seek AGENT: CONTENT
ask: CONTENT
scatter N using EXPANDER
storm N [in P lanes] using MAPPER
gather using MERGER
settle using REDUCER
map [in P lanes] using MAPPER
keep first|last N            drop first|last N
keep [in P lanes] if FILTER  drop [in P lanes] if FILTER
sort ascending|descending [in P lanes] by SCORER
repeat N time|times: ... [until: CONTENT]
repeat: ... until: CONTENT
```

The named runnable can be replaced by an inline `: CONTENT` body. `scatter`
and `gather` each use one child run to reshape a value. `storm`, `map`, filters,
and sorting run once per produced or current item; `in P lanes` bounds their
independent work while preserving result order. `settle` reduces sequentially.
`scatter N` does not enforce or truncate the returned list length.

Inline `keep`, `drop`, and `until` return `Boolean`; inline `sort ... by`
returns `Number`. Their generated evaluators have no tools or recall, so use a
named agic when evaluation needs either. Counts are non-negative; lane counts
are positive. Use singular `time` and `lane` only for numeric value 1.

## Comments and validation

`##!` documents the complete program. An adjacent `##` documents the next
declaration or flow statement at the same indentation. `#` is a human-only
comment. A blank line breaks `##` attachment.

For authored or repaired files, require all of these before claiming success:

1. Parse with the target Toolang entry point.
2. Confirm canonical formatting.
3. Inspect `toolang FILE --help` and `toolang FILE RUNNABLE --help`.
4. Run a focused example when its model and external effects are available.

Do not infer acceptance from appearance alone; parsing, semantic validation,
and generated runnable help catch different mistakes.
