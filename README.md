# claude-with-skills

<img width="1055" height="564" alt="Screenshot 2026-05-15 at 09 53 22" src="https://github.com/user-attachments/assets/4c0ba288-e1c5-4299-b5f6-57a3c9c982b4" />

A progressive course for developers who want to stop pasting the same instructions into Claude and start shipping reusable, portable Agent Skills. 

Whether you are tired of re-explaining your release process every Monday, migrating existing slash commands to the new Skills format, building a plugin for your team, or just learning what Claude Code can do — this repo takes you from your first `SKILL.md` to advanced patterns like forked context, dynamic injection, and headless automation.

## Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/davila7/claude-with-skills.git
cd claude-with-skills

# 2. Install the hello-skill example into your personal skills directory
bash scripts/install-examples.sh src/content/docs/01-basic/lesson-01-anatomy/examples/hello-skill personal

# 3. Open Claude Code and invoke the skill
claude
# then type:
/hello-skill
```

That is it. You have just installed and invoked your first Agent Skill.

## Learning path

| Level | Section | Outcome |
|---|---|---|
| Introduction | [00-introduction/](src/content/docs/00-introduction/index.md) | Understand what skills are, how they load, and how they compare to CLAUDE.md, subagents, and MCP |
| Basic | [01-basic/](src/content/docs/01-basic/index.md) | Write a skill from scratch, add frontmatter, invoke it by name and with arguments |
| Intermediate | [02-intermediate/](src/content/docs/02-intermediate/index.md) | Use supporting files, dynamic context injection, forked context, and hooks |
| Advanced | [03-advanced/](src/content/docs/03-advanced/index.md) | Build agent-driven skills, headless pipelines, plugin packaging, and cross-tool portability |

You can also browse the course as a **website** built with [Astro Starlight](https://starlight.astro.build):

```bash
npm install
npm run dev    # then open http://localhost:4321/
```

## How to run examples

### Interactive mode

```bash
claude
```

Inside the interactive session, invoke any installed skill by name:

```
/skill-name
/skill-name argument
```

### Headless mode

Pass a prompt directly with `-p`. Claude processes it and exits.

```bash
# Invoke a skill by name
claude -p "/skill-name"

# Invoke a skill with an argument
claude -p "/skill-name argument"

# Pipe context into a skill
echo "content to process" | claude -p "/skill-name"
```

Headless mode is useful in scripts, CI pipelines, and Makefile targets where you want Claude to perform a task without an interactive session. Output goes to stdout.

## AgentSkills open standard vs Claude Code

Skills follow the [AgentSkills.io open standard](https://agentskills.io). The standard defines three portable fields that every compliant tool understands:

```yaml
---
name: your-skill-name
description: What the skill does and when to invoke it.
allowed-tools:
  - Bash
  - Read
---
```

If you write only these fields, your skill runs unchanged in Cursor, GitHub Copilot, Gemini CLI, and any other AgentSkills-compatible tool.

Claude Code implements the full standard and adds a superset of extra fields for finer control:

| Field | What it does |
|---|---|
| `disable-model-invocation` | Prevent automatic activation; require explicit invocation |
| `user-invocable` | Control whether users can invoke the skill by typing `/skill-name` |
| `argument-hint` | Hint shown to the user when the skill expects an argument |
| `arguments` | Declare named, typed arguments with descriptions |
| `paths` | Restrict the skill to specific file paths or patterns |
| `shell` | Run a shell command and inject the output into context |
| `context: fork` | Execute the skill in an isolated context window |
| `agent` | Configure subagent behavior |
| `hooks` | Attach lifecycle hooks (before, after, on-error) |
| `model` | Specify which Claude model to use for this skill |
| `effort` | Control reasoning effort (low / medium / high) |

Dynamic context injection with `` !`command` `` and `${CLAUDE_SKILL_DIR}` are also Claude Code-specific. These extra fields are silently ignored by tools that do not support them, so your skill degrades gracefully in other environments.

## Reference

- [Frontmatter cheatsheet](src/content/docs/reference/frontmatter-cheatsheet.md) — every field, its type, and an example value
- [Headless mode guide](src/content/docs/reference/headless-mode.md) — flags, patterns, piping, and CI integration
- [Troubleshooting](src/content/docs/reference/troubleshooting.md) — skill not found, invocation not working, context issues

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for naming conventions, frontmatter rules, and PR expectations.

## License

MIT License. See [LICENSE](LICENSE).
