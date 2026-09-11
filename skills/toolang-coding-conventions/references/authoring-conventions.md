# Toolang Authoring Conventions

These conventions guide authoring style. They do not introduce syntax or
replace `toolang-grammar` or `toolang-cli`.

## Let the source explain itself

Use clear names, visible data movement, and natural prose. Add a comment only
when it gives a consumer useful documentation or records rationale that the
source cannot express directly.

Prefer the smallest artifact that solves the problem. A public example should
be useful as written, not exist only to showcase a language feature.

## Name roles and actions

Use lowercase kebab-case for public filenames and lowercase snake_case for
runnable names.

- Name an agent file for a recognizable professional or personal role, such as
  `dev.too`, `doc-writer.too`, or `english-coach.too`.
- Name a standalone flow module with a verb phrase that describes its outcome,
  such as `review-change.too`, `plan-delivery.too`, or `prepare-brief.too`.
- Name agics and helper flows with specific action verbs, such as
  `investigate`, `check_claim`, or `rewrite_section`.
- Avoid broad platform, technology, or topic names when they do not tell the
  user what the artifact does.

An agent is a role a user talks to. A flow is work the user runs. A runnable is
an action within that work.

## Make intent and input visible

Write the instruction so the agent cannot overlook the user's primary input.
Reference `{{_}}` wherever the current input is meant to influence a model
request.

```too
agic review:
  Review {{_}}. Identify correctness risks, explain their impact, and propose
  the smallest safe fixes.
```

Do not rely on conversational context to imply the task when the body can name
it directly. If a flow will replace the current value before it needs the
original input, bind the original to a meaningful local name first.

State the desired result, important constraints, and decision standard. Avoid
generic instructions such as “help the user” when the artifact has a more
specific job.

## Choose the right runnable

Use an `agic` for one coherent model interaction. Use a `flow` when the work has
meaningful stages or when Toolang should coordinate expansion, parallel work,
filtering, ranking, reduction, or revision.

Do not split a short instruction into a flow merely to look sophisticated. Do
not hide a real multi-stage process inside one oversized agic merely to keep the
file short.

Keep standalone flow modules self-contained. Put a helper beside the flow that
owns it unless it is intentionally a public capability.

## Write natural language naturally

Prompt bodies, agic messages, and implicit runs should read as ordinary prose:

- Start English sentences with normal capitalization.
- End sentences with appropriate punctuation.
- Prefer direct verbs and concrete outcomes.
- Use blank lines to separate prose from explicit flow statements.
- Keep each paragraph focused on one instruction or decision.

An implicit run is prose written directly as a flow statement. When prose would
start with a lowercase statement-boundary keyword, capitalize it or use an
explicit inline `run`. Write `Until ...` or `run: Until ...`, not lowercase
`until ...`.

```too
flow research:
  Identify the important uncertainties in {{_}}.

  storm 8 in 4 lanes using investigate
  sort descending by confidence

  Write an answer supported by the strongest findings.
```

These capitalization and punctuation rules are conventions. The grammar
separately reserves lowercase statement-boundary keywords; prose may begin with
interpolation, quoted text, numbers, or languages without English letter case.

## Make flows read as work

Arrange a flow so a reader can follow the transformation of the current value
from top to bottom. Each stage should earn its place by changing, evaluating,
selecting, combining, or delivering the work.

Use concurrency for independent work and give it an intentional bound. Use
iteration only when the stopping condition or fixed limit is clear. Prefer
named helpers when an operation has a reusable contract; prefer inline prose
when the operation is short and local to the flow.

```too
flow investigate_question:
  ## Generate independent lines of inquiry
  storm 8 in 4 lanes using investigate

  ## Remove findings that cannot be supported
  keep if:
    Return true when the finding has verifiable evidence.

  ## Prioritize the strongest evidence
  sort descending by confidence

  Synthesize the retained findings in {{_}} into a concise, supported answer.
```

Stage descriptions should explain purpose, not translate syntax. “Generate
independent lines of inquiry” is useful; “Run investigate eight times” is not.

## Omit default types

Leave out parameter and return types when Toolang's defaults already state the
contract:

- an omitted parameter list implies a primary `_` input of `Part[]`;
- an explicit untyped `_` also defaults to `Part[]`;
- an untyped named parameter defaults to `Text`; and
- an omitted return type defaults to `Part[]`.

Prefer:

```too
agic transform:
  Transform {{_}}.

agic rewrite(_, instruction):
  Rewrite {{_}} according to {{instruction}}.
```

over:

```too
agic transform(_: Part[]) -> Part[]:
  Transform {{_}}.

agic rewrite(_: Part[], instruction: Text) -> Part[]:
  Rewrite {{_}} according to {{instruction}}.
```

Add a type only when it differs from the default or communicates a contract the
surrounding syntax does not determine. Keep `()` when a runnable intentionally
accepts no primary input, and keep `?` when a named parameter is optional.

Do not repeat a return type that the consuming context determines. Inline
runnables after `if` and `by` already imply `Boolean` and `Number` results:

```too
keep if:
  Return true when the current item is actionable.

sort descending by:
  Score the current item by priority.
```

## Use documentation comments deliberately

Use `##` for text a consumer may display. Put it immediately above the
declaration or flow statement it describes, with no blank line between them.
Prefer one concise line.

```too
## Review a change and return prioritized findings.
agic review -> ReviewResult:
  Review {{_}}.
```

A runnable description names its capability or result. It should not repeat
the declaration name, parameters, or return type.

Inside a flow, a `##` comment describes the purpose of a stage for plans,
progress, or other UI. Start it with an action verb.

Use `##!` only when the complete program or its parent needs a description. A
source file should rarely need more than one parent documentation comment.

Use `#` for short, human-only rationale or constraints:

```too
# Keep this limit within the provider quota.
storm 8 in 4 lanes using investigate
```

Avoid comments that narrate syntax, long design notes, and frequent inline
comments. Prefer a better name or clearer source whenever it can remove a
comment.

## Keep capabilities narrow

Give a runnable only the models, tools, skills, services, recall, or other
resources its task needs. Pure conversation or transformation should not gain
tools by accident. Keep external effects visible in the responsible stage and
avoid giving every helper the complete agent capability set.

## Review checklist

- Does the filename describe a recognizable role or runnable outcome?
- Does every public runnable name a clear action?
- Is `{{_}}` present wherever the user's primary input should affect a request?
- Does an agic represent one coherent model interaction?
- Does each flow stage perform meaningful work on the right value?
- Are concurrency and iteration bounded and purposeful?
- Does the authored prose read naturally?
- Can any type annotation be omitted without losing information?
- Does each `##` provide useful consumer-facing text and touch its target?
- Does each `#` explain rationale or a constraint rather than restating code?
- Can clearer source, a better name, or a smaller artifact remove anything?
