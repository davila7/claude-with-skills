# Contributing

Thank you for contributing to claude-with-skills. This guide covers the conventions you need to follow so that examples remain consistent and lessons stay useful.

## Adding a skill example

### Naming conventions

- Skill directories must use lowercase letters, digits, and hyphens only. No underscores, no uppercase.
- The directory name becomes the default skill name, so keep it descriptive and short: `git-commit-helper`, not `my-great-skill-v2-final`.
- Maximum 64 characters for the name field in frontmatter (AgentSkills spec limit).

### Required files

Every skill example directory must contain a `SKILL.md` file. Without it, the install script will refuse to copy the skill. A `README.md` explaining what the skill does, how to install it, and what to expect from a sample interaction is also required.

### Frontmatter rules (AgentSkills open standard)

The YAML frontmatter block at the top of `SKILL.md` must include at minimum:

```yaml
---
name: your-skill-name
description: One to three sentences explaining what the skill does and when to invoke it.
---
```

Rules from the AgentSkills spec:

- `name`: lowercase, hyphens allowed, 1-64 characters, must be unique within a skills directory.
- `description`: plain text, non-empty, maximum 1024 characters. Write this for the model, not for humans — Claude reads it at startup to decide whether to activate the skill.
- `allowed-tools`: optional list of tool names the skill is permitted to use.

Claude Code-specific fields (`disable-model-invocation`, `user-invocable`, `argument-hint`, `arguments`, `paths`, `shell`, `context`, `agent`, `hooks`, `model`, `effort`) are documented in `reference/frontmatter-cheatsheet.md`. Use them only when the standard fields are not sufficient.

### Skill body

Keep the body under 500 lines / 5000 tokens. If your skill requires extensive reference material, put it in a `references/` subdirectory and link to it from the skill body. Claude will only load those files when it explicitly reads them.

## Adding a lesson

Lessons live in numbered section directories (`00-introduction/`, `01-basic/`, etc.). Each lesson is a Markdown file inside the appropriate section. Follow the existing structure: start with a one-paragraph overview, use H2 headings for each major concept, and end with a link to the next lesson or section README.

## Pull request expectations

- The skill must be runnable: copy it into `~/.claude/skills/` and invoke it with `/skill-name`. If it requires arguments, show a working example in the README.
- The lesson must be complete and accurate. No placeholder text.
- Run `bash scripts/install-examples.sh <skill-dir> personal` to confirm the install script works with your example.
- Keep PRs focused: one skill example or one lesson change per PR.
- Commit messages should be in English, imperative mood, and describe what changed and why.
