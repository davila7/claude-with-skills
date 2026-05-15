---
title: "Skills vs Alternatives"
---

Claude Code gives you several ways to encode knowledge and behavior for the agent. Each mechanism has a different load model, scope, and purpose. Understanding the differences helps you choose the right tool for each situation.

## Comparison table

| Mechanism | Loads when | Best for | Context cost |
|---|---|---|---|
| `CLAUDE.md` | Every session | Project facts, conventions, always-on rules | Always paid |
| Agent Skills (`SKILL.md`) | On demand, when task matches | Procedures and workflows invoked occasionally | ~100 tokens at startup; full body on activation |
| Subagents | Explicitly launched | Tasks that would flood your context with output | Isolated — does not touch your context window |
| MCP servers | When tools are registered | Giving Claude callable functions (APIs, databases, CLIs) | Tool schema at startup; no body |
| Slash commands (legacy) | On invocation | Same as Skills — commands are Skills in `.claude/commands/` | Full body on invocation |

## CLAUDE.md vs Skills

`CLAUDE.md` is the right place for things that are always relevant: the programming language and style guide for a project, architectural decisions, the names of key files, how to run the test suite. Claude reads it at the start of every session in that directory.

Skills are the right place for things that are sometimes relevant: the procedure for writing a release announcement, the steps to audit an API for security issues, a workflow for triaging bug reports. If you put a 300-line procedure in `CLAUDE.md`, you pay for those 300 lines on every session whether you need them or not. Put it in a skill, and you pay ~100 tokens at startup and the full body only when the procedure is actually triggered.

The practical rule: if you would reach for the procedure less than half the time you open a given project, put it in a skill.

## Skills vs Subagents

When a skill activates, it runs inline in your current conversation. Claude reads the skill body and applies those instructions to the task at hand. Everything happens in the same context window — the instructions, the task, and the output all appear in the same thread.

Subagents run in an isolated context. Claude launches a separate agent with its own context window, delegates a task to it, and receives a result. The intermediate work — every tool call, every intermediate file read, every reasoning step — stays in the subagent's context and does not flood your main conversation.

Use a skill when you want Claude to follow a procedure on your current task and you want to see each step. Use a subagent when the task involves processing a large amount of intermediate output (scanning hundreds of files, calling an API repeatedly, generating a long report) and you only care about the final result.

## Skills vs MCP servers

MCP (Model Context Protocol) servers give Claude callable functions — the equivalent of adding new tools to the agent's toolbox. An MCP server might expose a function to query a database, send a message to Slack, or run a shell command with specific parameters. Claude calls the function; the MCP server executes it and returns a result.

Skills give Claude instructions — not new capabilities, but guidance on how to use existing capabilities. A skill might tell Claude exactly how to structure a git commit message, what questions to ask before writing a feature, or how to format a pull request description. Skills and MCP servers complement each other: you might have an MCP server that gives Claude access to your issue tracker, and a skill that tells Claude how to triage issues using that tool.

## Skills vs legacy slash commands

Claude Code's original mechanism for on-demand instructions was `.claude/commands/`, where each Markdown file became an invocable slash command. That mechanism still works. The difference is that files in `.claude/commands/` are commands — they support basic invocation but lack the frontmatter fields that skills support.

Skills in `.claude/skills/` get the full feature set: structured frontmatter with invocation control (`user-invocable`, `disable-model-invocation`), argument declarations (`arguments`, `argument-hint`), context isolation (`context: fork`), hook integration, and the three-stage progressive loading model described in [progressive-disclosure.md](progressive-disclosure.md).

If you have existing `.claude/commands/` files, they continue to work as before. When you want the extra features, move them to `.claude/skills/` and add a frontmatter block.
