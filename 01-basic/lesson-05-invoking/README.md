# Lesson 05: Invoking Skills

There are three ways to invoke a skill. Each one suits a different situation.

## The three invocation modes

| Mode | How to trigger | Best for |
|------|---------------|----------|
| Auto-invocation | Write naturally; Claude matches description keywords | Everyday interactive use |
| Direct invocation | Type `/skill-name` in the Claude Code prompt | When you know exactly which skill you want |
| Headless mode | Run `claude -p "/skill-name"` in a terminal | Scripts, CI/CD, automation |

## 1. Auto-invocation

Claude reads the description of every installed skill at startup. When you type a task, Claude compares your words to those descriptions and activates the best matching skill automatically.

For this to work reliably, the skill description needs trigger keywords that match how you naturally phrase the task:

```yaml
description: Generate a conventional commit message for the staged changes.
             Use when the user wants to commit, asks for a commit message,
             or asks what to write for a commit.
```

With this description, any of these user messages would likely activate the skill:

- "What should I write for my commit?"
- "Generate a commit message"
- "I want to commit these changes"

Auto-invocation is the most ergonomic mode for interactive sessions. You do not have to remember skill names.

## 2. Direct invocation

Type `/skill-name` to activate a skill immediately, regardless of whether your message matches the description.

```
/commit-message
/code-review-checklist
/adr-writer
```

Direct invocation is useful when:

- You want a specific skill but did not phrase the task in a way that would auto-trigger it
- Multiple skills could match and you want a specific one
- You are testing a new skill and want to be sure it activates

## 3. Headless mode with `claude -p`

`claude -p` runs Claude Code non-interactively: one prompt in, one response out, then exit. This makes skills scriptable.

### Basic usage

```bash
# Invoke a skill from the command line
claude -p "/summarize-changes"

# Invoke a skill with an argument
claude -p "/fix-issue 123"
```

### Piping input

```bash
# Pipe code to a skill
cat src/utils.ts | claude -p "/code-review-checklist"

# Pipe an error log for analysis
cat error.log | claude -p "analyze this error and suggest a fix"

# Pipe git diff to get a commit message
git diff --staged | claude -p "/commit-message"
```

### Capturing output

```bash
# Save the output to a file
claude -p "/summarize-changes" > summary.txt

# Use the output in a script
COMMIT_MSG=$(claude -p "/commit-message")
git commit -m "$COMMIT_MSG"

# Run in CI to generate a changelog entry
claude -p "/changelog-entry" >> CHANGELOG.md
```

### Why `claude -p` exits after one turn

`claude -p` is designed for automation. It reads the prompt, produces a response, and exits. There is no follow-up turn. This makes it safe to use in scripts — the process always terminates, and the exit code reflects success or failure.

Because there is no follow-up turn, skills used in headless mode should produce complete, self-contained output. A skill that asks a clarifying question is unusable headlessly. When writing skills intended for both interactive and headless use, make the output complete without interaction, and use default behavior when context is ambiguous.

## The example in this lesson

`examples/summarize-changes/SKILL.md` demonstrates dynamic context injection — a Claude Code feature where a line in the skill body runs a command and injects its output before Claude reads the skill.

The line:

```
!`git diff HEAD`
```

runs `git diff HEAD` at skill activation time and replaces the line with the actual diff output. Claude reads the diff as part of the skill body, not as a separate tool call. This is useful for providing context that the skill always needs.

## Next steps

At this point you have covered all five basic concepts:

1. What a SKILL.md looks like (anatomy)
2. Where to install skills (scopes)
3. How to convert repetitive prompts into skills
4. How to encode documentation format as a skill
5. How to invoke skills interactively and headlessly

The exercises in `../exercises/` give you two hands-on tasks to reinforce these concepts. After that, the `02-intermediate/` section covers argument handling, context isolation, and more advanced skill patterns.
