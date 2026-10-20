---
name: docs-toc
description: Revise a documentation site's table of contents using the current navigation and pages plus Toolang design documents and implementation; identify missing or overlapping pages without writing their content.
---

# Organize the documentation table of contents

Use the caller's optional `requirements`, `runtime_repo`, and `toc` (default
`vocs.config.ts`). Resolve paths against the invocation workdir. Reuse its
dedicated worktree; from a primary checkout or main/master, create a dedicated
`codex/docs-toc-*` worktree from HEAD and transfer the current navigation bytes.
Preserve the original checkout and unrelated changes. Keep evidence and reports
in a unique `.toolang/docs-toc/TIMESTAMP-UUID/` directory.
Resolve the actual workdir with `pwd`; keep all helpers and logs in that unique
directory. Do not inspect prior runs or use shared lab or `/tmp` paths.

## Gather evidence

- Read repository instructions, the complete navigation configuration, existing
  page titles/headings, relevant entry pages, and redirect rules. Identify every
  current route, its audience, and whether it is generated, copied, or authored.
- Inspect the selected Toolang checkout's `docs/design/` and code. Trace the
  public commands, authored language, capabilities, configuration, and runtime
  boundaries that readers need. The code resolves discrepancies with design
  docs. Do not turn old plans or internal package names into public features.
- For bundled dependencies such as tree-sitter, inspect the version pinned by
  the selected runtime and the corresponding local tag/revision. A different
  version checked out in a sibling clone is not an implementation discrepancy.
- Record the runtime HEAD and relevant dirty files. Use this checkout as it
  stands; do not fetch, reset, or select a different release. Resolve an omitted
  runtime path to the sibling of the docs repository's primary checkout.

## Revise the structure

Organize around reader tasks and concept dependencies, with a path from getting
started to task guides and detailed references. Keep public documentation and
maintainer design material distinct where their audiences differ. Preserve
established URLs and useful ordering unless requirements justify a change.
Give repeated topics a canonical page. Do not mirror the source tree or add
one page per design document.

Update the specified TOC file. Focused navigation-test expectation changes are
also allowed when required by an intentional group/order change; preserve every
existing route and interaction assertion. Record these changes explicitly.
Navigation may link only to existing pages;
proposed pages belong in the content plan until written. Do not create empty
pages, rewrite content, rename files, or remove redirects in this workflow.
If the structure needs those changes, list them as follow-up work. An already
suitable TOC may remain unchanged when the evidence supports that decision.

Keep `content-plan.md` concise: one revised tree, one current-page mapping, and
one prioritized job table. State evidence once; do not repeat full writing
specifications or generate a separate essay for every page. Include:

- The revised tree, including clearly marked proposed pages that are absent
  from the active navigation.
- A mapping of current pages to their canonical place, with rationale only for
  meaningful moves or retained overlaps.
- Prioritized job IDs, targets, rationale, and owner (`sync_docs`, `write_docs`,
  or human decision). Give each writing job exactly one target file. Split
  related multi-page work into jobs with explicit dependencies.
- Evidence for material gaps and any unresolved coverage questions.

Write `jobs.json` alongside it with `runtime_repo` and a `jobs` array. Each job
has `id`, `owner`, `file`, `requirements` (a concise string), `sources` (a concise
string identifying evidence in the selected runtime or docs repo), and
`depends_on` (job IDs). The `write_docs` entries must map directly to the writer's
arguments; never bundle multiple targets into `file` or ask that writer to edit
navigation. Missing proposed pages may be writing targets, but requirements
must not link to other absent pages until their dependencies are written.

## Review and verify

Review the complete resulting navigation against the evidence and page map.
Check that no current route disappears accidentally, no new dead route is
registered, and generated references remain discoverable. Validate types,
links/fragments, build, and relevant navigation tests using the repository's
commands. Preserve honest failures from existing pages; do not remove coverage,
skip tests, or change unrelated content to make checks pass. Fix in-scope findings and rerun
affected checks, up to three passes.

Write `report.md` with source revision, changed structure and rationale,
coverage findings, review corrections, actual checks/results, blockers, and the
content-plan and jobs paths. Do not commit, push, open a PR, merge, or deploy.
Return the TOC/output worktree, report, plan and jobs paths, status, and a short
summary.
