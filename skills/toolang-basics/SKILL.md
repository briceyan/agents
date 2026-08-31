---
name: toolang-basics
description: Explain or troubleshoot Toolang agents, programs, caps, runnables, roots, homes, and common CLI setup without redesigning the user's agent.
---

# Toolang Basics

Help the user understand or configure Toolang from the behavior they want.

Start by identifying the target:

- a local resident agent under the Toolang root
- a remote agent ref such as `owner/name`
- a standalone `.too` program
- a reusable cap: psyche, skill, service, or prompt

Keep these concepts separate:

- An agent owns a program, caps, jobs, state, and runtime files.
- An `agic` is one model/tool loop.
- A `flow` is a static sequence of run, filtering, ranking, parallelism, and
  control statements.
- Caps shape behavior or provide reusable resources; they are not runs.
- Root caps are shared, home caps belong to one agent, and `with` references
  travel with one program module.

For setup or troubleshooting:

1. Inspect the relevant `.too` file, cap files, and `toolang --help` or
   `caps --help` output before suggesting commands.
2. Check that the selected runnable matches the surface (`chat`, `default`, a
   named agic, or a named flow).
3. Check that every runnable expecting user input actually references `{{_}}`
   or passes `_` through its flow statements.
4. Check cap visibility and selection separately: a cap can exist without
   being selected by a runnable.
5. Prefer the current installed Toolang behavior and documentation over stale
   examples.

Preserve the user's chosen model, tools, services, and file layout unless the
requested behavior requires changing them.
