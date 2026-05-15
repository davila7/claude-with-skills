---
title: "Exercise 02: Run a Skill Without the UI"
---

## Goal

Use `claude -p` to invoke the `summarize-changes` skill from the terminal without opening the interactive Claude Code interface.

## Prerequisites

- The `summarize-changes` skill installed at `~/.claude/skills/summarize-changes/SKILL.md`
  (copy it from `../lesson-05-invoking/examples/summarize-changes/`)
- A git repository with at least one uncommitted change
- `claude` available in your PATH

## Step 1: Prepare a repository with changes

Find a git repository you are working in, or create a throwaway one:

```bash
mkdir /tmp/skill-test && cd /tmp/skill-test
git init
echo "hello" > hello.txt
git add hello.txt
git commit -m "initial"
echo "world" >> hello.txt
```

Now `hello.txt` has an unstaged change. The skill will summarize it.

## Step 2: Run the skill headlessly

From inside the repository directory:

```bash
claude -p "/summarize-changes"
```

Claude Code starts, activates the skill, injects the diff output, produces a summary, and exits. You should see the summary printed to stdout.

## Step 3: Capture the output to a file

```bash
claude -p "/summarize-changes" > summary.txt
cat summary.txt
```

The output is now in `summary.txt`. This is useful in CI pipelines where you want a diff summary saved as an artifact.

## Step 4: Run the commit-message skill and use the output

Install the `commit-message` skill if you have not already:

```bash
cp -r path/to/lesson-03-repetitive-tasks/examples/commit-message ~/.claude/skills/
```

Stage a change and run:

```bash
git add hello.txt
COMMIT_MSG=$(claude -p "/commit-message")
echo "$COMMIT_MSG"
```

If the output looks correct, use it:

```bash
git commit -m "$COMMIT_MSG"
```

## What `claude -p` does differently

`claude -p` exits after one turn. There is no back-and-forth. This means:

- Skills that ask clarifying questions do not work well headlessly — Claude will ask a question and then the process exits before you can answer
- Output is printed to stdout, so it can be piped or captured with standard shell tools
- The exit code is 0 on success and non-zero on error, so you can use `&&` and `||` in scripts
- It is safe to use in CI/CD because the process always terminates

## Stretch goal

Write a shell alias that stages all changes and generates a commit message in one command:

```bash
alias smart-commit='git add -A && git commit -m "$(claude -p "/commit-message")"'
```

Add this to your shell profile to make it permanent. Note: be careful with `git add -A` in real projects — review what is staged before committing.
