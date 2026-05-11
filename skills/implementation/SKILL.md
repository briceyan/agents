---
description: Use when implementing a code change or adding a focused feature.
---

# Implementation

Use this skill for scoped code changes.

Workflow:
1. Define the behavior change in one sentence.
2. Update the owning module first, using existing patterns.
3. Add or adjust focused tests when behavior changes.
4. Keep public APIs narrow and avoid forwarding-only abstractions.
5. Re-run the relevant checks after edits.

Prefer durable, readable code over cleverness. Keep unrelated cleanup out of
the change unless it is necessary to complete the task safely.
