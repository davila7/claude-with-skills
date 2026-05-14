# Introduction: What Are Agent Skills?

An Agent Skill is a `SKILL.md` file that packages procedural knowledge for an AI agent. Instead of pasting the same block of instructions into every conversation, you write those instructions once, store them in a well-known directory, and the agent loads them on demand whenever the task calls for it.

The concept is defined by the [AgentSkills.io open standard](https://agentskills.io), which means a skill you write today will work in Claude Code, Cursor, GitHub Copilot, Gemini CLI, and any other tool that adopts the standard. Claude Code implements the full standard and adds a superset of extra fields for tighter control over invocation, context isolation, and tooling.

## The core idea

A skill is a self-contained unit of knowledge. The `SKILL.md` file tells the agent what to do and how to do it. When you install a skill and the right task comes up, the agent reads the file and follows the instructions — the same way you would read a runbook before executing a procedure you do not do every day.

## The three sections of a SKILL.md

**Frontmatter** — YAML between `---` delimiters at the top of the file. At minimum, this includes a `name` and a `description`. The description is what the agent reads at startup to decide whether to activate the skill. Additional fields control allowed tools, invocation mode, argument handling, and more.

**Body** — Markdown instructions after the frontmatter. This is where you write the procedure: steps, decision rules, output format expectations, error-handling notes. Keep it under 500 lines so it loads quickly and stays focused.

**Supporting files** — Any files in subdirectories alongside `SKILL.md` (typically `references/`, `scripts/`, `assets/`). These are not loaded automatically; the agent reads them only when the instructions explicitly reference them. This keeps startup cost low.

## Why Skills instead of CLAUDE.md?

`CLAUDE.md` loads on every session. That is the right choice for project facts, coding conventions, and architectural decisions that apply to everything the agent does in a given repo. It is the wrong choice for long procedures that are only relevant occasionally — they consume context tokens whether you need them or not.

Skills load on demand. The agent pays roughly 100 tokens per skill at startup (just the name and description), then loads the full body only when a matching task arrives. If you have 20 skills installed and only two are relevant today, the other 18 cost almost nothing.

## The open standard and portability

The AgentSkills.io open standard defines the minimum portable fields: `name`, `description`, and `allowed-tools`. If you use only these fields, your skill runs unchanged in every compatible tool. Claude Code adds extra fields — `disable-model-invocation`, `user-invocable`, `argument-hint`, `arguments`, `paths`, `shell`, `context`, `agent`, `hooks`, `model`, `effort`, and dynamic context injection — but those fields are ignored gracefully by tools that do not support them.

## Continue reading

- [Progressive disclosure: how Skills load in three stages](progressive-disclosure.md)
- [Skills vs alternatives: CLAUDE.md, subagents, MCP, slash commands](skills-vs-alternatives.md)
- [Setup: prerequisites and workspace configuration](setup.md)
