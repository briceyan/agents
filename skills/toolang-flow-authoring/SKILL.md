---
name: toolang-flow-authoring
description: Design, write, or debug Toolang flows with correct input propagation, bindings, concurrency, typed outputs, and bounded model work.
---

# Toolang Flow Authoring

Use a flow when the task benefits from a predictable multi-step pipeline rather
than one open-ended model/tool loop.

Workflow:

1. Define the observable final output and the primary input type.
2. Split work into small agics with one responsibility and explicit tool
   ceilings.
3. Decide which intermediate values belong in `_` and which must be named with
   `let` for later steps.
4. Add parallelism only for independent items and set a concrete `par` bound.
5. Use filtering, ranking, or review only when it changes the final result.
6. Declare structured or textual output types where they make boundaries more
   reliable.
7. Parse the complete program and run one small, representative input.

Always make user-input propagation visible. An agic that accepts primary input
must reference `{{_}}`; a flow must pass `_` into a statement or save it before
overwriting it. Missing `{{_}}` is valid syntax but usually means the user's
request never reaches the model.

Read [references/flow-patterns.md](references/flow-patterns.md) when selecting
statements or checking how values move through a flow.
