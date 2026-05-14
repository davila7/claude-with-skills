# Lesson 03: Allowed Tools

The `allowed-tools` field pre-approves a set of tools so Claude does not ask permission to use them during a skill run. This lesson explains the syntax, the exact behavior, and the tradeoffs.

## What allowed-tools does

Without `allowed-tools`, every tool call during a skill run triggers a permission prompt. The user sees "Claude wants to run `git status`. Allow?" before anything happens.

With `allowed-tools`, the listed tools are pre-approved for the duration of the skill. Claude uses them without prompting. The user already consented by invoking the skill.

This matters most for skills with `disable-model-invocation: true`. If the user has to respond to five permission prompts mid-workflow, the skill is no better than typing the commands manually.

## Syntax

Space-separated tool names in the frontmatter:

```yaml
allowed-tools: Read Grep Glob
```

For Bash, you can scope the approval to specific command patterns:

```yaml
allowed-tools: Bash(git *) Bash(npm test) Read
```

- `Bash(git *)` — any git subcommand
- `Bash(npm test)` — only `npm test`, not `npm install`
- `Bash(npx eslint *)` — any eslint invocation via npx
- `Bash(find *)` — any find command

The pattern after `Bash(` is matched against the full command string. Use `*` as a wildcard.

## What allowed-tools does NOT do

`allowed-tools` does not restrict which tools Claude can use. It only determines which tools skip the permission prompt. If a skill body leads Claude to call a tool not in `allowed-tools`, that tool will prompt as usual — it will not be blocked.

If you want to prevent Claude from using a tool entirely, that is a different configuration (project permissions, not skill frontmatter).

## Common patterns

### Read-only research

```yaml
allowed-tools: Read Grep Glob
```

Pre-approves the three tools needed to explore a codebase without writing anything. Claude can read files, search for patterns, and list directories without prompting.

### Git operations

```yaml
allowed-tools: Bash(git *) Bash(git diff *) Bash(git log *)
```

Pre-approves all git subcommands. Useful for skills that inspect git history, check status, or create commits.

### Scoped npm

```yaml
allowed-tools: Bash(npm test) Bash(npm run build) Bash(npm run lint)
```

Pre-approves specific npm scripts without permitting arbitrary npm commands like `npm install` or `npm publish`.

## Project skills and the trust dialog

When a skill is installed at the project scope (`.claude/skills/`), the user sees a workspace trust dialog the first time they open the project in Claude Code. Accepting the dialog is what enables `allowed-tools` to take effect for project-scoped skills. Personal skills (`~/.claude/skills/`) do not require this step.

## Examples

- `examples/safe-commit/` — git operations pre-approved for a commit workflow
- `examples/readonly-research/` — read-only tools pre-approved for codebase research

## Next lesson

[Lesson 04: Arguments](../lesson-04-arguments/README.md)
