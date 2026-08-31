# Toolang Flow Patterns

## Sequential pipeline

```too
flow default(_: Text) -> Text:
  run analyze
  run draft
  run verify
```

Each `run` replaces `_` with its result.

## Preserve caller input

```too
flow default(_: Text) -> Text:
  let request:
    {{_}}

  run draft
  run review
```

Named locals such as `request` remain available to agics that declare a
matching parameter.

## Fan out, transform, and gather

```too
flow default(_: Text) -> Text:
  let topic:
    {{_}}

  scatter 6 expand
  map investigate par 4
  keep relevant par 4
  rank score top 8 par 4
  gather synthesize
```

- `scatter` creates a list.
- `map` transforms list items and may run independent items in parallel.
- `keep` filters by a Boolean agic.
- `rank` scores and retains the strongest items.
- `gather` reduces the list to one result.

## Bounded refinement

```too
flow default(_: Text) -> Text:
  run draft
  repeat 2:
    run improve
```

Use a fixed small repeat count. Avoid unbounded loops and review stages that do
not have a distinct quality criterion.

## Input rule

```too
agic draft(_: Part[]) -> Text:
  tools = none

  Request:
  {{_}}
```

Declaring `_` does not automatically insert it into a model message. Reference
`{{_}}` explicitly.
