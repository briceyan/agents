# Idiomatic Toolang Patterns

Use these as decision rules, not mandatory templates.

## Start with the smallest runnable

For one model/tool loop, keep one default agic:

```too
agic:
  Answer the user's request directly.
  {{_}}
```

Do not add a flow that only calls the same agic once. Use a flow when the
sequence itself is meaningful:

```too
flow default(_: Text) -> Text:
  run draft
  run review
  run revise
```

Use `()` when a runnable intentionally accepts no caller input. Otherwise an
omitted parameter list implies primary input `_ : Part[]`.

## Make data movement obvious

`_` is the current pipeline value. Let statements should explain retained
context, not rename every intermediate result:

```too
flow research(_: Text) -> Text:
  let question:
    {{_}}

  scatter 6 expand
  map investigate par 4
  gather synthesize
```

Here `question` is useful because later agics need the original request after
`_` becomes queries, evidence, and findings. Avoid names such as `result1` or
`next_value` that do not explain why the value is retained.

## Keep agics focused

An agic should have one observable responsibility and a clear output shape:

```too
agic relevant(_: Part[], question: Part[]) -> Boolean:
  tools = none

  Question: {{question}}
  Candidate: {{_}}

  Return true only when the candidate helps answer the question.
```

Do not ask one agic to research, compare, draft, review, and publish unless that
work is intentionally one open-ended loop. Separate steps when the boundary is
useful for concurrency, filtering, retry, inspection, or reuse.

## Choose named and inline work deliberately

Use a named agic when it is reused, needs tools or recall, has a typed contract,
or deserves independent inspection. Use an inline body for a short one-off
model transformation:

```too
flow summarize(_: Text) -> Text:
  run:
    Extract the three decisions from {{_}}.
```

Named helpers should describe outcomes: `extract_findings`, `score_relevance`,
or `assemble_plan`. Avoid structural names such as `step1` and `processor`.

## Match the flow statement to the shape

| Need | Prefer |
| --- | --- |
| One run expands one item into a list | `scatter` |
| Several independent runs produce a list | `storm` |
| Transform every list item | `map` |
| One run merges a list | `gather` |
| Sequentially fold items into an accumulator | `settle` |
| Filter items with a Boolean decision | `keep` or `drop` |
| Order items with a numeric decision | `rank` |

Use positional `keep/drop` when no model judgment is needed. Do not spend model
calls to perform deterministic selection.

## Make resource boundaries local

Select only what the runnable uses:

```too
agic search(_: Part[]):
  recall = none
  tools = web/*

  Find current primary sources for {{_}}.
```

`tools = none` is useful for pure transformations. `recall = none` is useful
when each item must be judged independently. Avoid repeating directives when
normal inheritance already expresses the intended policy.

Attach public caps with `with`, then select them by their resolved local name.
Keep a cap external when it is independently reusable; keep a short,
program-specific instruction in the `.too` file.

## Type boundaries that affect execution

Declare outputs when the runtime or the next statement depends on their shape:

- `Text[]` for an expander consumed as a list
- `Boolean` for filters and stopping checks
- `Number` for ranking
- `Text` for a final textual flow result
- a struct for a stable multi-field record

Do not add types solely to make a simple conversational agic look formal.

## Bound work visibly

```too
map investigate par 4

repeat 2:
  run improve
```

Parallelism is for independent items and should have a concrete limit. Repeats
must be bounded by a small count, a meaningful `until`, or both. Avoid review
loops whose stopping condition is only "make it better."

## Keep modules self-contained

`agent.too` and each `flows/<name>.too` file are complete programs. A flow
module does not inherit structs, agics, caps, contexts, or instructions from
another module. Put a helper beside the flow that owns it or make the behavior
an explicitly referenced cap.

## Document intent, not syntax

Use `##!` for the program's purpose and `##` for the semantic node or statement
that follows. Comments should explain why a stage exists, its decision rule, or
its safety boundary. Do not narrate self-evident syntax such as "run the next
agic."

## Final simplification pass

Before considering a program complete, ask:

1. Can one declaration be removed without losing a behavior boundary?
2. Is every retained name meaningful to a reader?
3. Does every input appear where it is consumed?
4. Is `_` overwritten only after anything that needs its previous value saves
   it?
5. Are model calls used only where judgment or generation is required?
6. Are concurrency, repetition, tools, and recall bounded intentionally?
7. Can the default runnable be found without knowing hidden configuration?
