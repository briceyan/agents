---
name: toolang-idiomatic-authoring
description: Write or review concise, readable, idiomatic Toolang programs without turning simple agent behavior into unnecessary declarations or flow machinery.
---

# Idiomatic Toolang Authoring

Make the program read like a direct description of the agent's behavior.
Prefer the smallest language construct that preserves the intended boundary.

Core decisions:

- Use one unnamed `agic:` for a simple conversational agent.
- Introduce a `flow` only when ordered stages, fan-out, selection, aggregation,
  or bounded refinement are part of the behavior.
- Give an agic one model responsibility. Split it when the output becomes a
  meaningful input boundary for another step.
- Treat `_` as the value moving through a flow. Create a named local only when
  the original or intermediate value must survive after `_` changes.
- Put caller input visibly into the message with `{{_}}`; declaring `_` alone
  does not forward it.
- Omit declarations, directives, types, and configuration that merely restate
  Toolang defaults.
- Narrow tools, recall, models, and caps only when the runnable needs a real
  boundary. Keep resource policy next to the runnable it governs.
- Use typed outputs at control or data boundaries, such as `Boolean` filters,
  `Number` scorers, arrays for fan-out, and structs for durable records.
- Bound parallelism and repetition. Make cost and stopping behavior visible in
  the source.
- Prefer reusable caps for behavior that applies across programs; keep
  program-specific instructions in the program.

Before finishing, read the program top to bottom and remove any name, layer, or
step that does not help a reader predict execution. Then parse the complete
program and run one representative input.

For construct choices, layout, and focused before/after examples, read
[references/idioms.md](references/idioms.md).
