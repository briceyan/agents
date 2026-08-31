# Toolang Cap Formats

The cap name comes from the file or directory name.

## Psyche

Path: `psyches/<name>.md`

Use plain Markdown for stable behavior preferences that should apply across
many runs.

## Skill

Path: `skills/<name>/SKILL.md`

```md
---
name: focused-workflow
description: Use when a request requires this specific workflow.
---

# Focused Workflow

Write the decisions, constraints, and workflow that materially improve the
agent's behavior.
```

Keep the description short and discriminating. Put substantial conditional
detail in `references/` and link it from `SKILL.md`.

## Service

Path: `services/<name>.md`

```md
---
description: Use when the task needs this MCP service.
transport: http
target: https://example.com/mcp
headers:
  Authorization: Bearer $API_TOKEN
---

Document useful tools, resources, and authentication expectations.
```

For `stdio`, set `transport: stdio`, write `target` as one argv command line,
and list required environment variable names in `env`. Never put secret values
in the cap.

## Prompt

Path: `prompts/<name>.md`

```md
---
params: focus?
---

Review the following input.

Focus: {{focus}}

{{_}}
```

Invoke it from input as `$name focus=security -- Review this change`. Use
`{{_}}` for the prompt's attached input.

## Public References

In an agent program:

```too
with skill owner/name
with psyche owner/name
with service owner/name
with prompt owner/name
```

For a resident agent:

```sh
caps AGENT skill add owner/name
caps AGENT psyche add owner/name
caps AGENT service add owner/name
caps AGENT prompt add owner/name
```
