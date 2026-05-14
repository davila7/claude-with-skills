# Advanced: Progressive Disclosure, Bundled Scripts, and Subagent Orchestration

This section is for practitioners who have completed the Basic and Intermediate sections. You already know every frontmatter field. This section is about architecture: how to structure skills that scale, how to bundle reusable scripts, and how to coordinate work across isolated subagents.

## Prerequisites

You have completed the Intermediate section or you can write a SKILL.md with full frontmatter control, including `context: fork`, `agent`, `allowed-tools`, and `user-invocable`. You are comfortable with Python 3 and basic shell scripting.

## What you will learn

| Lesson | Topic |
|--------|-------|
| 01 — Progressive disclosure | SKILL.md as a navigator: keep context cost low as skill complexity grows |
| 02 — Supporting scripts | Bundle and invoke scripts from within skills using `${CLAUDE_SKILL_DIR}` |
| 03 — Skills calling subagents | Use `context: fork` and the `agent` field to spawn isolated subagents |
| 04 — Subagents preloading skills | The `skills:` field in subagent definitions for pre-injected domain knowledge |
| 05 — Skills orchestrating skills | One skill instructing Claude to invoke other skills in sequence |
| 06 — Context window mastery | Discovery budget, body lifecycle, auto-compaction, and tuning knobs |
| 07 — Hooks in skills | `PreToolUse` and `PostToolUse` hooks defined in skill frontmatter |
| 08 — Plugins and distribution | Packaging skills as a plugin with `plugin.json` for team distribution |
| Capstone | A multi-skill, subagent-backed code quality bot built from scratch |

## Learning outcomes

By the end of this section you will be able to:

1. Structure skills for progressive disclosure so context cost stays low at scale — the navigator pattern keeps SKILL.md under 80 lines while making hundreds of lines of reference material available on demand.
2. Bundle and invoke scripts from within skills using `${CLAUDE_SKILL_DIR}`, the variable that always resolves to the directory containing `SKILL.md` regardless of installation location.
3. Spawn isolated subagents from a skill using `context: fork` — understand when forked context helps, when it hurts, and what a subagent can and cannot see.
4. Preload skills into a subagent's startup context using the `skills:` field in a subagent definition file, so the subagent carries domain knowledge from the moment it starts.
5. Chain skills together in an orchestration skill — understand which patterns require the main conversation and which can delegate to workers.
6. Manage context window budget across many active skills — know the three stages of context loading, the discovery budget, and how to tune it with settings.
7. Add lifecycle hooks to skills for automation — run `PreToolUse` and `PostToolUse` shell commands outside Claude's turn.
8. Package skills into a plugin for team distribution — the plugin directory layout, `plugin.json` manifest, and security restrictions.
9. Build a complete multi-skill, subagent-backed system from scratch in the capstone project.

## Key constraint to keep in mind

Subagents cannot spawn other subagents. If a skill uses `context: fork`, the forked subagent cannot itself use `context: fork` to spawn further subagents. All delegation flows must go through the main conversation. The orchestrator lives in the main session; workers live in forked subagents.

## How to use this section

Each lesson directory contains a `README.md` explaining the concept and one or more complete, working example skills. The examples are designed to be installed and tested, not just read.

```bash
cp -r lesson-01-progressive-disclosure-in-practice/examples/pdf-toolkit ~/.claude/skills/
```

Lessons are ordered by concept dependency: lesson 01 (disclosure) informs lesson 02 (scripts), which both feed into lessons 03 and 04 (subagents).

## Lessons

- [Lesson 01: Progressive disclosure in practice](lesson-01-progressive-disclosure-in-practice/README.md)
- [Lesson 02: Supporting scripts with ${CLAUDE_SKILL_DIR}](lesson-02-supporting-scripts/README.md)
- [Lesson 03: Skills calling subagents](lesson-03-skill-calls-subagent/README.md)
- [Lesson 04: Subagents preloading skills](lesson-04-subagent-uses-skills/README.md)
- [Lesson 05: Skills orchestrating skills](lesson-05-skills-orchestrating-skills/README.md)
- [Lesson 06: Context window mastery](lesson-06-context-window-mastery/README.md)
- [Lesson 07: Hooks in skills](lesson-07-hooks-in-skills/README.md)
- [Lesson 08: Plugins and distribution](lesson-08-plugins-and-distribution/README.md)
- [Capstone: Code Quality Bot](capstone/README.md)
