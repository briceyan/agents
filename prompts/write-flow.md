---
params: output?, constraints?
---

Design a Toolang flow for the following goal.

Expected output: {{output}}
Constraints: {{constraints}}

Define small agics with explicit responsibilities and tools, show how `_` and
named locals move between steps, bound parallel work, and use filtering,
ranking, or refinement only when it improves the result. Every agic that needs
the caller's primary input must reference Toolang's primary-input template
placeholder. Return a complete parseable `.too` example plus a short explanation
and a representative test command.

Goal:
{{_}}
