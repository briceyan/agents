---
name: bug-fix
description: Diagnose and fix reproducible software defects with a minimal root-cause change and regression coverage.
---

# Bug Fix

Use this workflow when the requested outcome is to correct broken behavior.

1. Reproduce the reported behavior with the smallest realistic case.
2. Record the expected and actual result before editing.
3. Trace the failing path and compare plausible causes against evidence.
4. Apply the smallest change at the component that owns the behavior.
5. Add a regression test that fails before the fix and passes after it.
6. Run focused checks, then the repository's required default verification.

Preserve unrelated user changes. Do not turn a bug fix into a refactor unless
the root cause cannot be corrected safely without one. If reproduction is not
possible, report what was tested and what evidence is still missing instead of
claiming the defect is fixed.
