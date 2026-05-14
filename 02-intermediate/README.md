# Intermediate: Frontmatter, Arguments, and Dynamic Context

This section teaches the complete Claude Code Skills frontmatter reference and how to combine fields to build reliable, production-quality skills. By the end you will be able to write skills that control their own invocation, pre-approve tools, inject live context, restrict themselves to relevant file paths, and override the model and effort level for the task at hand.

## Prerequisites

You have completed the Basic section, or you can already write a working `SKILL.md` with `name`, `description`, and a body that does something useful.

## What you will learn

| Lesson | Topic |
|--------|-------|
| 01 — Frontmatter reference | Every field, its type, default, and when to use it |
| 02 — Invocation control | The `disable-model-invocation` and `user-invocable` matrix |
| 03 — Allowed tools | Pre-approving tools so Claude does not prompt during skill execution |
| 04 — Arguments | Positional args, named args, `argument-hint`, and shell-style quoting |
| 05 — Dynamic context | The `` !`command` `` syntax for injecting live shell output |
| 06 — Paths and shell | Auto-activating by file path and choosing a shell for injection commands |
| 07 — Model and effort | Overriding model and reasoning effort per skill |
| 08 — Combining options | A decision framework and complete real-world examples |

## How to use this section

Every example is a complete, runnable skill. Copy any example directory into `~/.claude/skills/` or your project's `.claude/skills/` and invoke it immediately.

```bash
cp -r lesson-02-invocation-control/examples/manual-only-deploy ~/.claude/skills/
```

Then open Claude Code and type `/manual-only-deploy`.

Lessons build on each other, but each one references only the specific fields it introduces so you can read them independently. If you already understand invocation control, skip to lesson 03.

## Exercises

The `exercises/` directory at the end of this section contains three hands-on challenges with worked solutions. Attempt the exercise before reading the solution.
