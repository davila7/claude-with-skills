# Lesson 05: Dynamic Context Injection

Dynamic context injection lets you run shell commands when a skill is invoked and embed the output directly in the skill body before Claude sees it. This is the mechanism that makes skills aware of the current git state, environment versions, open pull requests, or any other live data.

## The syntax

### Inline: single command

Use backtick syntax prefixed with `!`:

```
!`git status --short`
```

Claude Code runs this command when the skill is invoked, captures stdout, and replaces the entire `` !`...` `` expression with the output. Claude sees the output, not the command.

### Multi-line: fenced code block

For commands that span multiple lines or produce structured output, use a fenced block opened with `` ```! `` instead of the usual `` ``` ``:

````
```!
echo "OS: $(uname -s)"
echo "Node: $(node --version)"
echo "Git: $(git version)"
```
````

Everything inside the block is passed to the shell as a script. The stdout of the entire script replaces the block.

## What Claude sees

You write:
```
The current git status is:
!`git status --short`
```

Claude sees (at invocation time):
```
The current git status is:
 M src/auth.ts
 M src/routes/login.ts
?? src/temp.js
```

Claude never sees the original command. It only sees the output.

## When injection runs

Commands run at skill invocation time, in the project directory (the directory where Claude Code was opened). They run before Claude's turn begins. Claude cannot influence what commands run or what output they produce.

## Failures

If a command exits with a non-zero status, the error output (stderr) replaces the placeholder. Claude sees the error message and can respond to it — for example, "git status failed: not a git repository" is visible to Claude and it can explain the problem to the user.

## Disabling injection

If `disableSkillShellExecution: true` is set in Claude Code settings, all `` !`cmd` `` placeholders are replaced with the literal string `[shell execution disabled]` rather than running the command. Skills that depend on injection will still load, but they will not have live data.

## Key use cases

**Git state**: Inject `git status`, `git diff --stat`, or `git log --oneline -10` so Claude knows exactly what has changed without asking.

**Environment info**: Inject Node version, Python version, OS details for debugging or compatibility checks.

**File contents**: Inject a config file or package.json version field to avoid having Claude read it separately.

**GitHub CLI**: Inject `gh pr view`, `gh issue view`, or `gh run list` output to give Claude live context about the project's CI state.

## Examples

- `examples/git-diff-summary/` — injects staged and unstaged diff before asking Claude to summarize
- `examples/env-report/` — uses a multi-line block to capture the full environment
- `examples/pr-summary/` — injects multiple `gh` CLI outputs for a complete PR overview

## Next lesson

[Lesson 06: Paths and shell](../lesson-06-paths-and-shell/README.md)
