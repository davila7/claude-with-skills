---
title: "commit-message"
name: commit-message
description: Generate a conventional commit message for the current staged git changes. Use when the user wants to commit, asks for a commit message, or asks what to write for a commit.
allowed-tools: Bash(git diff *) Bash(git status *)
---

## Instructions

1. Run `git diff --staged` to see exactly what is staged for the next commit.

2. Run `git status --short` to understand the full scope of changes (staged and unstaged) and identify the files involved.

3. If nothing is staged, tell the user there is nothing staged and suggest they run `git add` first. Stop here.

4. Choose the correct Conventional Commits type based on the diff:
   - `feat`: a new feature or capability visible to users or callers
   - `fix`: a bug fix
   - `docs`: documentation changes only
   - `style`: formatting, whitespace, missing semicolons — no logic change
   - `refactor`: code restructuring with no behavior change and no new feature
   - `test`: adding or correcting tests
   - `chore`: build system, dependency updates, tooling, CI config

5. Determine the scope from the changed files. The scope is optional but useful when the change is clearly isolated to one module, package, or layer (for example, `api`, `auth`, `db`, `cli`). Omit it if the change is broad.

6. Write the subject line:
   - Format: `type(scope): description` or `type: description` if no scope
   - Imperative mood: "add", "fix", "remove" — not "added", "fixes", "removing"
   - Maximum 72 characters
   - No period at the end

7. If the diff is non-trivial (more than one logical change, or a change whose motivation is not obvious from the code), add a body:
   - Blank line after the subject
   - Bullet points explaining **why** the change was made, not what it does (the diff already shows what)
   - Keep each bullet under 72 characters

8. Output only the commit message text. No surrounding explanation, no markdown code block wrapping.
