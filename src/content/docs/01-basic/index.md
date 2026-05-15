---
title: "Basic: Understanding and Writing Skills"
---

This section teaches the fundamentals of Claude Code Skills. By the end you will know what a skill looks like, where to put it, why skills exist, and how to invoke them both interactively and from scripts.

## What you will learn

| Lesson | Topic |
|--------|-------|
| 01 — Anatomy | The three parts of a SKILL.md file: frontmatter, body, supporting files |
| 02 — Where skills live | The four scopes, how override order works, and live reload behavior |
| 03 — Repetitive tasks | Converting a pasted prompt into a reusable skill |
| 04 — Documentation skills | Encoding output format alongside knowledge for consistent results |
| 05 — Invoking skills | Auto-invocation, direct `/skill-name` invocation, and `claude -p` headless mode |

## Prerequisites

- Claude Code installed and available in your terminal (`claude --version` should print a version number)
- A terminal and a text editor
- Basic familiarity with YAML (you do not need to be an expert — frontmatter is simple key-value pairs)

## How to use this section

Every example in this section is a complete, working skill. You can copy any example directory straight into `~/.claude/skills/` and invoke it immediately.

```
cp -r lesson-01-anatomy/examples/hello-skill ~/.claude/skills/
```

Then open Claude Code in any project and type `/hello-skill`.

The lessons are designed to be read in order, but each one stands on its own if you already know the preceding concepts. Start with lesson 01 if you are new to skills, or jump to lesson 05 if you just need to understand invocation.
