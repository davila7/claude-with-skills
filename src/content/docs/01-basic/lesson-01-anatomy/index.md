---
title: "Lesson 01: The Anatomy of a SKILL.md"
---

A `SKILL.md` file has three distinct parts. Understanding each one is the foundation for writing skills that work reliably.

## Part 1: YAML frontmatter

The frontmatter sits between `---` delimiters at the very top of the file. It is the only required section that follows a strict format. The agent reads frontmatter at startup — before a task arrives — to decide whether the skill is relevant.

```
---
name: my-skill
description: Does X. Use when the user asks about Y or Z.
---
```

The frontmatter block closes with another `---` line. Everything after that closing delimiter is the body.

### The name field

- Lowercase letters, digits, and hyphens only. No spaces, underscores, or uppercase letters.
- Maximum 64 characters.
- Must match the name of the directory that contains the `SKILL.md` file. If your directory is `git-commit-helper/`, the name field must be `git-commit-helper`.
- Must be unique within a skills directory (personal scope, project scope, etc.).

Valid examples: `commit-message`, `code-review-checklist`, `adr-writer`

Invalid examples: `Commit_Message`, `my skill`, `generate-a-conventional-commit-message-for-the-staged-changes`

### The description field

- Plain text. Maximum 1024 characters.
- Write it for the model, not for humans. The agent scans descriptions to decide whether to activate a skill without being explicitly asked.
- The most effective descriptions contain two things: **what the skill does** and **when to use it**. Include keywords that a user might naturally type.

Good description: `Generate a conventional commit message for the staged git changes. Use when the user wants to commit, asks for a commit message, or asks what to write for a commit.`

Weak description: `Helps with commits.`

The weak version has no trigger keywords. A user typing "what should my commit message say?" probably will not trigger it reliably.

### Optional frontmatter fields

Claude Code supports additional fields beyond the AgentSkills standard. The most useful ones at the basic level:

- `allowed-tools`: a list of tools the skill may use. Restricting tools limits accidental side effects and surfaces what the skill actually needs. Example: `allowed-tools: Bash(git diff *) Bash(git status *)`.

A full reference is in `reference/frontmatter-cheatsheet.md` at the root of this repository.

## Part 2: The body

Everything after the closing `---` of the frontmatter is the body. This is Markdown, and it is where you write the procedure the agent will follow.

The body is only loaded when the skill is activated. At startup, the agent pays roughly 100 tokens per installed skill (name + description only). The full body is loaded on demand, so a 200-line procedure costs nothing in sessions where the skill is not needed.

Practical rules for body content:

- Write steps in imperative form: "Run git diff --staged" rather than "You should run git diff --staged".
- Be explicit about the output format. If you want a bullet list, say so. If you want only the commit message with no surrounding explanation, say that too.
- Keep the body under 500 lines. Long skills load slowly and are harder to maintain.
- Use headings to organize multi-phase procedures (gather context, analyze, produce output).

## Part 3: Supporting files

A skill directory can contain files other than `SKILL.md`. These are not loaded automatically. The agent reads them only when the body explicitly instructs it to.

A typical layout might look like:

```
my-skill/
  SKILL.md
  references/
    style-guide.md
    error-codes.txt
  scripts/
    validate.sh
```

If the body says "Read references/style-guide.md before writing", the agent loads that file on demand. This keeps startup cost low while still making rich reference material available.

## Minimal valid structure

```
---
name: hello-skill
description: Does one specific thing. Use when the user asks for that thing or mentions these keywords.
---

## Instructions

1. Step one.
2. Step two.
3. Output the result.
```

That is a complete, deployable skill. The example in `examples/hello-skill/` demonstrates this minimal structure.

## Next lesson

[Lesson 02: Where skills live](../lesson-02-where-skills-live/)
