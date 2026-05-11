---
description: Use when GitHub repository, issue, pull request, review, or CI context matters.
transport: http
target: https://mcp.github.com/mcp
headers:
  Authorization: Bearer $GITHUB_TOKEN
---

Use this service for GitHub-backed work:
- repository and branch context
- pull request metadata and comments
- issue triage
- CI and review follow-up
- PR creation or update workflows

Require `GITHUB_TOKEN` in the local environment before connecting.
