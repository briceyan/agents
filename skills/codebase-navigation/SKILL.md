---
name: codebase-navigation
description: Use when a task requires understanding an existing repository before editing.
---

# Codebase Navigation

Use this skill before making code changes in an unfamiliar area.

Workflow:
1. Inspect repository status and avoid touching unrelated changes.
2. Find the relevant modules with fast search tools.
3. Read nearby tests, docs, and call sites before editing.
4. Identify the smallest change surface that satisfies the request.
5. State important assumptions when the code does not make them obvious.

Prefer `rg`, targeted file reads, and existing project scripts over broad
manual exploration.
