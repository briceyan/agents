---
name: toolang-cli
description: Use when installing, invoking, inspecting, running, serving, or troubleshooting Toolang through `toolang`, `too`, `caps`, or `uv run toolang`, including version selection, script output, agents, caps, work, chat, and workspaces. This skill covers commands; use `toolang-grammar` for language syntax.
---

# Toolang CLI

Use one confirmed Toolang entry point for an entire operation. Command shape,
parser behavior, and generated script help can differ across versions.

## Choose the active entry point

In a Toolang source checkout managed by uv, prefer the project environment:

```sh
uv run toolang --version
uv run toolang --help
```

Use `uv run toolang` as the command prefix for every later check or run in that
checkout. This exercises the current working tree and its locked dependencies.
Confirm the checkout from the authorized workspace's `pyproject.toml` and
`uv.lock`; do not search unrelated parent directories for a different copy.
Outside a source checkout, use the available installed entry point and verify
it first:

```sh
toolang --version
toolang --help
```

`too` is an alias for `toolang`; `caps` is the cap-oriented entry point. Do not
silently switch between a global executable and `uv run toolang`. When a
version mismatch is relevant, report the exact prefix and version that
produced each observation. In remote chat, distinguish the local Chat process
version from the executor version shown by the runtime.

`--dev [PATH]` has a different purpose: it selects a built Toolang wheel for a
new guest sandbox. It does not make the controlling CLI run source from the
checkout. Use `uv run toolang` for the development controller; build a wheel
and add `--dev dist` only when that development version must also run inside a
new guest.

## Run local scripts

The generated script command is:

```text
toolang SCRIPT RUNNABLE [OPTIONS] [NAME=VALUE...] [-- INPUT | -]
```

Inspect the generated interface instead of guessing it:

```sh
toolang example.too --help
toolang example.too main --help
toolang example.too main -o - -- "primary input"
```

Replace the prefix with `uv run toolang` in a development checkout. `-o -` or
`--out -` prints the final value to stdout; without an output option the result
is stored and normal stdout may be empty. `-o PATH` writes the result to a
file. Named runnable inputs use `name=value`. Use `--` to disambiguate primary
input, `-` for explicit stdin, or omit input to read piped stdin.

`toolang run AGENT` is not script execution. It starts an agent runtime in the
foreground. Never recommend `toolang run file.too` for a local runnable.

## Work with agents

Common lifecycle commands are:

```sh
toolang new alice
toolang clone SOURCE [TARGET]
toolang list
toolang alice info
toolang alice run
toolang alice start
toolang alice stop
toolang alice chat
```

Agent selectors may be local names, `agent:name`, supported owner/name
shorthand, or canonical URLs. A local script can also provide agent-style
commands such as `toolang ./agent.too chat`; confirm them through its help.

## Caps, work, and workspaces

Manage `psyche`, `skill`, `service`, and `prompt` caps at root scope or under an
agent:

```sh
toolang skill list
toolang alice skill add OWNER/NAME
toolang alice caps
```

Each cap command supports the operations advertised by its own `--help`, such
as `list`, `new`, `edit`, `delete`, `add`, `remove`, and `template`.

Use `toolang AGENT task ...` for one-time work and `toolang AGENT chore ...`
for recurring work. Use `toolang AGENT workspace list|add|remove` for explicit
workspace grants. Filesystem tools address a configured workspace with
`workspace://NAME/path` or their `workspace` argument. Never bypass a missing
grant with `..`, an absolute host path, shell redirection, or a shell command.

## Chat and run controls

Inside terminal Chat, slash commands update or inspect the session. Important
forms include `/model`, `/runnable`, `/agic`, `/flow`, `/allow`, `/limit`,
`/models`, `/tools`, `/caps`, `/agics`, `/flows`, `/output`, `/show`, and
`/exit`. Leading colon forms such as `:model`, `:agic`, and `:allow` apply only
to the submitted run. Use `/help` and `:?` for the active version's complete
forms.

Models and run permissions can also be supplied by generated command options,
including `--model`, `--allow`, `--limit`, and `--sandbox`. Read the selected
runnable's help because accepted options and named arguments are generated from
that runnable and the active Toolang version.

## Diagnostic discipline

For a CLI failure, capture the command prefix, `--version`, working directory,
target file or agent selector, generated help, exit status, stdout, and stderr.
Reproduce with the smallest relevant command. Keep validation on the same
entry point; a global installation passing does not validate a development
checkout, and the reverse is also true.
