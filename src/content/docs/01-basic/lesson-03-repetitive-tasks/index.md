---
title: "Lesson 03: Skills for Repetitive Tasks"
---

The most common reason to create a skill is a task you keep doing the same way. If you have pasted the same block of instructions into a conversation more than three times, that block belongs in a skill.

## The "I keep pasting this" trigger

A good candidate for a skill is any task where you find yourself:

- Pasting a paragraph of instructions at the start of a task ("When you write commit messages, always use conventional commits format, and keep the subject under 72 chars, and...")
- Copying a section of CLAUDE.md into a conversation because it has grown into a multi-step procedure
- Explaining the same process to a new team member who uses Claude Code

If the instruction block is always the same, make it a skill. If it varies every time (because the task context changes), it is not a good skill candidate.

## When to extract a skill from CLAUDE.md

CLAUDE.md loads on every session. That is correct for facts that apply to everything: the stack, the architecture, the testing framework. It is wrong for long procedures that are only relevant once in a while.

Extract a procedure from CLAUDE.md into a skill when:

1. The procedure has grown beyond three or four steps
2. It is only relevant for specific occasions (releasing, reviewing, committing)
3. You want to make it team-shareable via version control without cluttering CLAUDE.md

## Before and after

**Before — pasting this every time you want a commit message:**

> When writing a commit message, use the Conventional Commits format. The type should be one of feat, fix, docs, style, refactor, test, or chore. The scope is optional and goes in parentheses. The subject line must be in imperative mood and under 72 characters. If the change is complex, add a blank line and then bullet points explaining why, not what. Only output the commit message, nothing else.

**After — type `/commit-message`.**

The skill stores those instructions once. You never paste them again. The output is consistent because the instructions are identical every time.

## Examples in this lesson

| Skill | What it does |
|-------|--------------|
| `commit-message` | Generates a Conventional Commits message from staged changes |
| `code-review-checklist` | Reviews code against a structured checklist |
| `changelog-entry` | Drafts a Keep a Changelog entry from git history |
| `pr-description` | Writes a PR description with summary, motivation, and test plan |

Each one is a complete, working skill. Copy any of them to `~/.claude/skills/` or `.claude/skills/` to use it.

## Next lesson

[Lesson 04: Documentation skills](../lesson-04-documentation-skills/)
