---
name: toolang-cap-authoring
description: Create or revise Toolang psyche, skill, service, and prompt caps with valid layout, metadata, scope, and public references.
---

# Toolang Cap Authoring

Design one focused cap that changes an agent's decisions or gives it a reusable
resource. Do not use caps as a dumping ground for general documentation.

Workflow:

1. Choose the kind from the behavior: stable judgment for `psyche`, a
   conditional workflow for `skill`, an MCP connection for `service`, or a
   reusable input template for `prompt`.
2. Choose scope: root for shared local use, agent home for one resident agent,
   or a program-level `with` reference for a portable public dependency.
3. Inspect nearby caps and current Toolang validation rules before writing.
4. Write the smallest complete definition with a discriminating trigger or
   invocation shape.
5. Attach and select it explicitly where required.
6. Validate the cap and run one realistic invocation.

When writing a cap, read [references/cap-formats.md](references/cap-formats.md)
for the current file layouts, public shorthand, and examples.

Do not add unsupported frontmatter, embed credentials, or assume that making a
cap visible automatically selects it for every runnable.
