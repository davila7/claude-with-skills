---
title: "Lesson 07: Model and Effort"
---

Two frontmatter fields let you choose a different model and reasoning effort level for a specific skill, independent of the session defaults.

## The `model` field

```yaml
model: haiku
```

Valid values: `haiku`, `sonnet`, `opus`, a full model ID string (e.g., `claude-opus-4-5`), or `inherit`.

`inherit` is the default — the skill uses whatever model the current session is running on.

### When to override the model

**Use `haiku`** for tasks that are fast, well-defined, and do not require complex reasoning:
- Formatting a file according to a style guide
- Extracting specific fields from structured data
- Generating boilerplate from a template
- Simple one-shot transformations

**Use `sonnet`** for most coding tasks. This is the default for Claude Code bundled skills because it balances capability and speed well for the majority of development workflows.

**Use `opus`** for tasks that genuinely require extended reasoning:
- Architectural analysis or design decisions with significant tradeoffs
- Security audits where missing a subtle vulnerability has real consequences
- Root cause analysis for complex bugs where previous analysis attempts have failed
- Reviewing major changes to core infrastructure

### Cost tradeoff

These are illustrative multipliers, not exact pricing. Actual pricing varies by model generation and should be verified at anthropic.com/pricing:

| Model | Relative cost | Best for |
|---|---|---|
| Haiku | ~1x | Formatting, extraction, boilerplate |
| Sonnet | ~5x | Most coding tasks (session default) |
| Opus | ~25x | Architecture, security, complex debugging |

A skill that uses `model: opus` costs roughly 25 times more per invocation than a haiku skill. For a skill you run once for a serious security audit, that is worthwhile. For a skill you run after every file edit, haiku is almost certainly the right choice.

### The override is temporary

The model override applies only to the skill's turn. The next prompt in the session uses the session model, not the skill's model.

## The `effort` field

```yaml
effort: high
```

Valid values: `low`, `medium`, `high`, `xhigh`, `max`.

Effort controls how much extended reasoning the model applies before responding. Higher effort takes longer and costs more but produces better results on tasks that benefit from deeper thinking.

### When to override effort

**Use `effort: low`** for tasks where the answer is immediate and mechanical: a simple string transformation, a yes/no check, a code formatting pass.

**Use `effort: high` or `xhigh`** for tasks that benefit from the model considering multiple approaches before responding: architecture decisions, security analysis, optimizing a complex algorithm, or any task where the session default produces results that miss important considerations.

**Use `effort: max`** sparingly. This is the equivalent of asking the model to think as hard as it can. Reserve it for genuinely difficult problems where lower effort has already produced unsatisfactory results.

### Combining model and effort

The two fields are independent:

```yaml
model: opus
effort: high
```

This runs the most capable model with extended reasoning — appropriate for a security audit or a hard architectural question. It is also the most expensive combination.

```yaml
model: haiku
effort: low
```

This is the fastest and cheapest combination — appropriate for a formatting pass or a simple code generation task.

## Examples

- `examples/deep-analysis/` — uses `model: opus` and `effort: high` for architectural analysis and security reviews

## Next lesson

[Lesson 08: Combining options](../lesson-08-combining-options/)
