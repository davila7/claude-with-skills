# Lesson 04: Subagents Preloading Skills

The previous lesson showed how a skill can spawn a subagent. This lesson inverts the relationship: a subagent is defined with a list of skills to inject into its startup context. The subagent starts already knowing those conventions, patterns, and procedures — it does not need to discover them during execution.

## The skills field in subagent definitions

Subagents are defined as Markdown files in `.claude/agents/`. The frontmatter supports a `skills` field:

```yaml
---
name: api-developer
description: Implement REST API endpoints following team conventions.
tools: Read, Edit, Write, Bash, Grep, Glob
model: sonnet
skills:
  - api-conventions
  - error-handling
---
```

When Claude Code starts this subagent, it injects the full content of each listed skill into the subagent's context before the subagent begins its task. The subagent can reference those skills immediately, without needing to read files, invoke skills, or ask for guidance.

## When to use this pattern

Use `skills:` in a subagent definition when:

- **The subagent always needs specific conventions.** A `code-reviewer` subagent should always know the team's code style guide. Hardcoding that dependency in the subagent definition is more reliable than hoping the subagent discovers the right skill.

- **You want pre-loaded expertise, not runtime discovery.** When the skill content is short and always relevant, injecting it at startup is cheaper than waiting for the subagent to detect it is needed and load it mid-task.

- **The skill is `user-invocable: false`.** Background knowledge skills — architecture notes, API conventions, style guides — are not meant for users to invoke directly. But a subagent can preload them even though users cannot. The `skills:` field bypasses the user-facing restriction.

## What preloading means

`skills:` controls what is injected into the subagent's starting context. It does not restrict what skills the subagent can use. The subagent can still discover and invoke any other project or user skill via the Skill tool during execution. `skills:` is about what the subagent knows from the start, not about what it is allowed to use later.

## Constraints

- **Cannot preload skills with `disable-model-invocation: true`.** Those skills are explicitly flagged as not invocable by Claude. The preloading mechanism uses the same pool of Claude-invocable skills.
- **Missing skills are skipped.** If a listed skill is not installed in the project or at user scope, Claude Code skips it with a warning. The subagent starts anyway, without that skill's content.
- **Preloaded content counts against context.** Every skill you preload is injected into the subagent's starting context. Preload only what is genuinely always-needed. If a skill is only needed in 20% of cases, let the subagent discover it on demand rather than paying the context cost on every run.

## Comparison with context: fork

| Dimension | `context: fork` in a skill | `skills:` in a subagent |
|-----------|---------------------------|------------------------|
| Who sets up the relationship | The skill's frontmatter | The subagent's frontmatter |
| What the subagent starts with | SKILL.md body as task | Subagent's markdown body as system prompt |
| Pre-injected content | CLAUDE.md only | Listed skills (full content) |
| Who spawns whom | Skill spawns a subagent | Main session delegates to subagent |

The two patterns can work together: a skill can use `context: fork` to spawn a subagent that is defined with `skills:`. The subagent then has both the task from the skill body and the pre-loaded expertise from its `skills:` list.

## The api-developer example

The `examples/api-developer/` directory contains a complete, working example of this pattern. It includes:

- `.claude/agents/api-developer.md` — the subagent definition, which preloads two skills
- `.claude/skills/api-conventions/SKILL.md` — REST API conventions (not user-invocable)
- `.claude/skills/error-handling/SKILL.md` — error handling patterns (not user-invocable)

Install the example into a project:

```bash
cp -r examples/api-developer/.claude /path/to/your/project/.claude
```

When Claude Code delegates work to the `api-developer` subagent, the subagent starts with both convention skills already loaded. It applies them without being told to look them up.

## Next steps

The remaining advanced lessons (05-08) cover:
- Chaining skills in an orchestration skill
- Context window budget management across many active skills
- Lifecycle hooks for automation
- Packaging skills into a plugin for team distribution

## Back

[Advanced section overview](../README.md)
