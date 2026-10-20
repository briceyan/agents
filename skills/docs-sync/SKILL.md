---
name: docs-sync
description: "Synchronize the Toolang documentation site from a latest or explicit runtime revision: copy pinned upstream files, regenerate references, repair failing generators, and verify the output in isolated worktrees."
---

# Synchronize documentation sources

Run only the stage requested by the entrypoint: **prepare**, **generate**, or
**verify**. Pass the absolute `run.json` path between stages. Keep every log and
helper inside that run's unique directory. Read the manifest first; after a
blocked stage, preserve evidence and stop further mutation or investigation.
The verify stage may still produce a report and compute the blocked result.

Never edit original checkouts or runtime implementation. Follow repository
instructions. Use `gh` for GitHub access, without changing the active account or
reading credentials. Do not commit, push, modify PRs, merge, or deploy.
Intermediate replies contain only the manifest path, status, and a brief summary.

Start from the current inputs. Do not inspect prior run directories, manifests,
or reports. Never use a shared `/tmp` pointer, helper, or log; every path belongs
to this invocation's unique run directory. Resolve the actual workdir with `pwd`.

The bundled helpers are [prepare.py](scripts/prepare.py),
[resolve_target.py](scripts/resolve_target.py),
[copy_sources.py](scripts/copy_sources.py), and [readiness.py](scripts/readiness.py).
Use the bundle Source Ref supplied by the entrypoint to fetch these files from
the **same revision**, with `gh api` and the raw media type. Save exact bytes
under the run's `helpers/` directory. Do not reimplement their logic or fetch
scripts from mutable main. Each helper is invoked with `python3`, except the
preparer and resolver, which need
`uv run --no-project --python 3.11 --with packaging python`.

## Prepare

Read the docs checkout's instructions and README. Before network access, create
`WORKDIR/.toolang/docs-refresh/TIMESTAMP-UUID/helpers/`. Fetch all four helpers
there. Run the preparer with `--docs-repo WORKDIR --run-dir RUN_DIRECTORY
--version REQUESTED_VERSION` and explicit source paths only when supplied.
Pass the requested version unchanged as one argv value; use an empty string
when omitted. Use its returned manifest path, not another directory or pointer.
If helper acquisition fails, write a blocked manifest with the requested inputs
and exact error in this same run directory.

The preparer resolves omitted clones beside the primary docs checkout, verifies
origins, snapshots originals, fetches refs, resolves the literal runtime target
and its exact grammar pin, and creates unique source/output worktrees. It writes
a manifest even on resolution failure. A nonzero result blocks this stage:
do not catch it as a latest request, substitute grammar main, modify the helper,
or continue copying. Missing/ambiguous grammar pins also block the run.

Read instructions in these worktrees. Run `copy_sources.py MANIFEST` to copy
runtime `docs/authoring.md` to `docs/pages/docs/toolang-conventions.mdx` and
grammar `GRAMMAR.md` to `docs/pages/reference/toolang-grammar.mdx`. The script
preserves source content, changes H1s, adds pinned source links, rewrites
relative links, and escapes MDX outside code. Do not paraphrase copied content.

When the grammar differs, regenerate and test the detached grammar checkout
using its own instructions; generated tracked files must remain unchanged.
Synchronize only `docs/syntaxes/toolang.tmLanguage.ts` and its focused syntax
tests to this grammar. Do not repair upstream grammar or runtime behavior.
Record commands and exit codes; finish with status `copied` or `blocked`.

## Generate

Write the shared pin `scripts/toolang-source.txt` as
`git+https://github.com/openhat-ai/toolang@RUNTIME_SHA`. Install docs dependencies
with the frozen Bun lockfile. Run both commands in the docs output worktree:

```sh
python3 scripts/gen-cli-ref.py --entrypoint toolang -o docs/pages/reference/toolang-cli.mdx
python3 scripts/gen-api-ref.py -o docs/pages/reference/agent-api.mdx
```

Capture separate logs and actual return codes. Successful exit is insufficient:
compare CLI root and advertised `more` commands with reference sections, and
compare every OpenAPI operation/schema with the API page. Missing coverage is
a generator failure. Final generation uses the shared pin, not an unrecorded
local package.

For failure, reproduce it and inspect the matching implementation, generator,
and tests. Repair only `scripts/gen-cli-ref.py`, `scripts/gen-api-ref.py`, and
their existing test files. Add an offline regression that fails before the fix
and passes after it. Preserve coverage and inert OpenAPI loading; never start
services, hide errors, weaken tests, downgrade the revision, or patch runtime
code. Allow up to three repair attempts per generator. Network/auth/install
failures are environment blockers, not compatibility bugs.

Rerun affected tests after repairs. Run both generator suites and repeat both
generations; require byte-identical output. Record reproductions, fixes,
regressions, commands, coverage, and hashes. Set status `generated` or `blocked`.

## Verify

If already blocked, write `report.md` using recorded evidence and retain the
blocker. Do not inspect originals or guess missing worktree metadata.
Otherwise follow the docs README: typecheck, both generator suites, production
build, site/syntax browser tests, and dev navigation tests. Run whitespace,
link/fragment, source-link, navigation, copy-fidelity, regeneration, and scope
checks. Parse all `public/*.too` examples with the pinned runtime. Existing
failures still prevent readiness; distinguish them accurately and keep them
outside this workflow's repair scope. Fix only introduced defects in copied
pages, highlighting, or generators.

Record `verification.checks` with exact names below, status `pass`, `failed`,
or `not_run`, an actual `exit_code`, and evidence/log paths:

```text
docs typecheck
cli generator suite
api generator suite
production build
site and syntax browser tests
dev navigation browser tests
whitespace check
internal link targets
fragment and anchor targets
copied source links
navigation registration
copy fidelity
regeneration reproducibility
cli reference coverage
api reference totals
public example parse
diff scope
originals untouched
```

Check original HEADs and statuses against their recorded baseline, allowing
only this run's ignored artifacts. Review the complete diff and copied/generated
content for accuracy and omissions. Record findings and corrections. Write
`report.md` with `- **Status:** pending`, versions/SHAs, output worktree/branch,
changes, repairs, checks, findings, and blockers. Run `readiness.py MANIFEST`
without modifying its code. Its exit 1 is a valid blocked result; never overwrite
its computed status. Missing evidence must remain a failure. Return the computed
status, absolute report/worktree paths, and failed checks.
