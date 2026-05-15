---
title: "safe-commit"
name: safe-commit
description: Stage all changes and create a conventional commit with a generated message. Use when ready to commit and want automated staging and commit message generation.
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git diff *) Bash(git status *)
---

## Safe commit workflow

### Step 1: Check current state

Run:
```
git status
```

Show the output. If there is nothing to commit (working tree clean), stop and report that there are no changes to commit.

### Step 2: Review what will be committed

If there are staged changes, run:
```
git diff --staged
```

If there are no staged changes but there are unstaged changes, run:
```
git add -A
```

Then confirm: "Staged all changes. Run `git diff --staged` to review."

Run `git diff --staged` and show the output.

### Step 3: Generate a conventional commit message

Analyze the staged diff and write a commit message following the Conventional Commits format:

```
<type>(<scope>): <short summary>

<body — optional, only if the why is not obvious from the diff>
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `style`.

Rules:
- Summary line: 72 characters maximum, imperative mood ("add" not "adds" or "added")
- Scope: the module, component, or file area affected (optional but recommended)
- Body: explain why, not what — the diff already shows what

Present the proposed commit message to the user before committing.

### Step 4: Commit

After presenting the message, run:
```
git commit -m "<generated message>"
```

If the commit fails (for example, a pre-commit hook rejects it), report the hook output verbatim and stop. Do not retry with a different message unless the user asks.

### Step 5: Confirm

Show the result:
```
git status
```

Report the commit hash from the output of the commit command and confirm the working tree is clean.
