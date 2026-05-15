---
title: "Lesson 03: Skills Calling Subagents"
---

Some tasks are best isolated from your main conversation. When a skill needs to read dozens of files, scan large logs, or explore a codebase deeply, that work would crowd your working context with output that may be irrelevant to what you do next. `context: fork` solves this by running the skill in a separate subagent whose context is isolated from yours.

## How context: fork works

When you invoke a skill that has `context: fork` in its frontmatter, Claude Code does not run the skill inline. Instead, it:

1. Creates a new subagent with a fresh context (no conversation history)
2. Sends the rendered SKILL.md body as the subagent's task prompt
3. Runs the subagent to completion
4. Returns a summary of the result to your main conversation

The subagent's full working context — all the files it reads, all the shell output it sees — never enters your main context. You get back a summary, not the raw output.

## The agent field

The `agent` field selects which subagent type runs the skill:

| Agent | Tools available | Model | Use for |
|-------|----------------|-------|---------|
| `Explore` | Read, Grep, Glob, Bash (read-only) | Haiku | Research, codebase exploration, analysis |
| `Plan` | Read-only tools | Session model | Pre-flight checks, planning tasks |
| `general-purpose` | All tools | Session model | Tasks that need to write or execute |
| Custom name | Defined in `.claude/agents/` | As configured | Team-specific workflows |

If `agent` is omitted when `context: fork` is set, `general-purpose` is used.

## What the subagent can and cannot see

The subagent starts with a fresh context. It does not see:

- Your conversation history
- Files you have read in the current session
- Previous skill outputs
- Any context from the main conversation

It does see:

- The rendered SKILL.md body (with `$ARGUMENTS` substituted)
- `CLAUDE.md` from the project and user directories (the same background context it would always load)
- The file system — it can read any file you have access to

**Implication:** Write the SKILL.md body as a self-contained task. Do not assume the subagent knows anything you know. If the task requires a specific file path, argument, or background fact, it must appear in the body or in `$ARGUMENTS`.

## The agent field without context: fork

If you set `agent` but not `context: fork`, the `agent` field is ignored. The skill runs inline in your main conversation as normal.

## The key constraint: subagents cannot spawn subagents

A skill running under `context: fork` cannot itself use `context: fork` to spawn further subagents. Delegation is one level deep only. All orchestration must happen in the main conversation.

This means: if you want to parallelize work across multiple subagents, the orchestrator must be an inline skill (no `context: fork`) that instructs the main Claude session to spawn multiple subagents. See the `parallel-investigator` example below.

## Contrast: inline vs forked

| Behavior | No context: fork | context: fork |
|----------|-----------------|---------------|
| Sees conversation history | Yes | No |
| Shares context with main | Yes | No |
| Output stays in main context | Yes | Summary only |
| Can spawn further subagents | Via main session | No |
| Good for | Tasks that need history | Large research tasks |

## Examples in this lesson

### deep-research

`examples/deep-research/SKILL.md` uses `context: fork` with `agent: Explore`. Invoke it with a topic or question and it produces a structured report on how that system works in the codebase. The research output (potentially hundreds of lines of file contents and grep results) stays in the subagent and never loads into your main session.

```
/deep-research authentication middleware
```

### parallel-investigator

`examples/parallel-investigator/SKILL.md` does NOT use `context: fork`. Instead, it runs inline and instructs the main Claude session to spawn two separate Explore subagents in parallel. This pattern lets the skill orchestrate multiple workers while respecting the constraint that forked subagents cannot themselves fork further.

Use this pattern when you need two or more research threads and want results combined into a single comparison report.

## Next lesson

[Lesson 04: Subagents preloading skills](../lesson-04-subagent-uses-skills/)
