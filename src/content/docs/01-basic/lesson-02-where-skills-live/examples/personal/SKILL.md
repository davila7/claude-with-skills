---
title: "personal-greeting"
name: personal-greeting
description: Demonstrates the personal scope for Claude Code skills. Use when testing personal-scoped skills or when the user wants to understand the difference between personal and project skill scopes.
---

## Instructions

This skill is installed at the personal scope. Its expected location on disk is:

```
~/.claude/skills/personal-greeting/SKILL.md
```

Tell the user the following:

1. This is an example of a personal-scoped skill. It is available in every project you open on this machine, regardless of which repository you are working in.

2. Personal skills live at `~/.claude/skills/`. Each skill is a directory with a `SKILL.md` file inside. The directory name must match the `name` field in the frontmatter.

3. Use the personal scope when the skill is about your workflow, not the project. Good candidates for personal skills:
   - Your commit message style preferences
   - Your preferred code review checklist
   - Shortcuts for tools you use everywhere (explain-code, summarize-changes, etc.)

4. Use the project scope (`.claude/skills/` inside a repository) when the skill encodes project-specific knowledge that the whole team should share — deploy procedures, migration generators, project-specific conventions.

5. If both scopes have a skill with the same name, the personal scope wins. You can always override a project skill with your own personal version.

Do not ask the user any follow-up questions unless they ask one first.
