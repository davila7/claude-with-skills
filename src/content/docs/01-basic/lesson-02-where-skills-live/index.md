---
title: "Lesson 02: Where Skills Live"
---

Skills can be installed at four different scopes. The scope determines which projects can use a skill and who controls it.

## The four scopes

| Scope | Directory | Availability | Who manages it |
|-------|-----------|--------------|----------------|
| Enterprise | Set by organization policy | All users in the organization | Platform administrator |
| Personal | `~/.claude/skills/` | All projects on your machine | You |
| Project | `.claude/skills/` (in repo root) | This project only | Anyone with repo access |
| Plugin | Loaded by an MCP plugin | Depends on plugin | Plugin author |

In practice, most individual developers use two scopes: personal for tools they always want available, and project for team-shared workflows.

## Override order

When two skills share the same name, higher scopes win. The order from highest to lowest priority is:

```
Enterprise > Personal > Project > Plugin
```

If you have a personal skill named `code-review-checklist` and the project also has `.claude/skills/code-review-checklist/SKILL.md`, your personal version is used. This lets you override shared skills with your own versions without modifying the project.

This also means a skill author publishing a project skill cannot override a developer's personal skill of the same name — which is intentional.

## Personal skills

Install a skill at `~/.claude/skills/<skill-name>/SKILL.md`.

Personal skills are available in every project you open. Use this scope for skills that are about your workflow rather than a specific project — code review preferences, commit message style, personal productivity shortcuts.

```
~/.claude/skills/
  commit-message/
    SKILL.md
  code-review-checklist/
    SKILL.md
  explain-code/
    SKILL.md
```

## Project skills

Install a skill at `.claude/skills/<skill-name>/SKILL.md` inside a repository.

Project skills are visible to everyone who works on the project. Commit the `.claude/skills/` directory to version control so the skill ships with the codebase. Use this scope for workflow knowledge that is specific to this project — release procedures, architecture conventions, team-specific review checklists.

```
my-project/
  .claude/
    skills/
      deploy-staging/
        SKILL.md
      generate-migration/
        SKILL.md
  src/
  ...
```

## Live reload behavior

Editing a `SKILL.md` file that is already in a watched directory takes effect in the current Claude Code session without a restart. The agent re-reads the file the next time the skill is invoked.

Creating a brand-new skills directory (for example, adding `.claude/skills/` to a project that did not have it before) requires restarting Claude Code. The watcher is set up at session start and will not pick up a newly created root directory mid-session.

Summary:
- Edit existing skill file -> takes effect immediately on next invocation
- Create new skills directory -> requires restart

## Examples

The `examples/` directory in this lesson contains one skill for each of the two common individual scopes:

- `examples/personal/SKILL.md` — a skill meant to be installed at `~/.claude/skills/`
- `examples/project/SKILL.md` — a skill meant to be committed to `.claude/skills/`

Both are fully functional. Copy either one to the appropriate directory to see it work.

## Next lesson

[Lesson 03: Converting repetitive tasks into skills](../lesson-03-repetitive-tasks/)
