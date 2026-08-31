# Toolang Public Agents and Caps

This repository contains public Toolang agents and composable caps that can be
used directly through the `briceyan/<name>` shorthand.

## Try an Agent

No clone is required:

```sh
uvx toolang run briceyan/dev
uvx toolang run briceyan/research
uvx toolang run briceyan/plan
uvx toolang run briceyan/toolang
```

| Agent | Best for | First prompt to try |
| --- | --- | --- |
| `briceyan/dev` | Repository-aware implementation, debugging, and review | `Find the cause of the failing test, make the smallest fix, and verify it.` |
| `briceyan/research` | Source-backed research with parallel search and synthesis | `Compare the strongest current approaches to evaluating coding agents.` |
| `briceyan/plan` | Dependency-aware product and engineering delivery plans | `Plan a six-week beta for a developer tool with a four-person team.` |
| `briceyan/toolang` | Toolang setup, cap authoring, and flow design | `Create a flow that researches alternatives, ranks evidence, and writes a brief.` |

Clone an agent when you want to customize it:

```sh
toolang clone briceyan/dev my-dev
too my-dev chat
```

## Add a Cap

Caps can be attached to an existing resident agent:

```sh
caps alice skill add briceyan/bug-fix
caps alice skill add briceyan/toolang-flow-authoring
caps alice psyche add briceyan/source-aware
caps alice prompt add briceyan/code-review
caps alice service add briceyan/github
```

The public catalog currently includes:

- Psyches: `concise`, `decision-ready`, `safety`, `senior-engineer`, and
  `source-aware`.
- Coding skills: `bug-fix`, `codebase-navigation`, `git-workflow`,
  `implementation`, `review`, and `verification`.
- Outcome skills: `delivery-planning` and `research-synthesis`.
- Toolang authoring skills: `toolang-basics`, `toolang-cap-authoring`, and
  `toolang-flow-authoring`.
- Services: `context7` and `github`.

## Use a Prompt

After adding a prompt cap, start a chat and invoke it with `$<name>` in agent
input:

```sh
caps alice prompt add briceyan/code-review
too alice chat
```

Then enter:

```text
$code-review focus=security --
Review the authentication changes in this branch.
```

Available prompt examples are:

- `bug-fix`
- `code-review`
- `deep-research`
- `implementation-plan`
- `write-cap`
- `write-flow`

## Reference Caps from an Agent

A portable `.too` program can reference public caps without installing them
into a resident agent first:

```too
with psyche briceyan/concise
with skill briceyan/verification

agic:
  psyches = concise
  skills = verification

  Complete this request and verify the result:
  {{_}}
```

Declaring primary input does not automatically place it in a model message.
Use `{{_}}` explicitly in every agic that needs the user's request, or preserve
and pass `_` deliberately inside a flow.

## Contributing

Keep every addition focused on a realistic outcome. New agents should include
a useful first-run prompt, bound expensive parallel work, and reuse caps where
that makes behavior easier to understand. New caps should remain independently
useful through the public shorthand.

Validate the catalog before opening a pull request:

```sh
uv run --python 3.11 \
  --with 'toolang @ git+https://github.com/openhat-ai/toolang.git@main' \
  python scripts/validate_catalog.py
```
