---
title: "Headless Mode Reference"
---

Using skills with `claude -p` for automation, CI/CD, and scripting.

---

## What Headless Mode Is

`claude -p "prompt"` runs Claude Code non-interactively: one prompt, one response, exit. There is no conversation, no session continuity, and no interactive UI. Skills are loaded and invocable exactly as in interactive mode, but the execution context is a single-shot process.

Headless mode is the right choice for:
- CI/CD pipelines (pull request descriptions, changelogs, release notes)
- Git hooks (commit message generation, pre-commit validation)
- Shell scripts that need language model reasoning
- Scheduled automation that runs without a human present
- Any workflow where you need Claude's output as input to another command

---

## Basic Patterns

Invoke a skill directly:

```bash
claude -p "/summarize-changes"
```

Invoke a skill with an argument:

```bash
claude -p "/fix-issue 123"
```

Pipe input to a skill — the piped content is prepended to the prompt:

```bash
git diff HEAD | claude -p "/review-diff"
```

Save output to a file:

```bash
claude -p "/changelog-entry" > /tmp/changelog.md
```

Use from a git hook — in `.git/hooks/prepare-commit-msg`:

```bash
#!/bin/bash
DIFF=$(git diff --staged)
echo "$DIFF" | claude -p "/commit-message" > "$1"
```

---

## Using Skills in CI

GitHub Actions example that generates a pull request description from a skill:

```yaml
- name: Generate PR description
  run: |
    claude -p "/pr-description" > pr-body.txt
    gh pr create \
      --body "$(cat pr-body.txt)" \
      --title "$(git log -1 --format=%s)"
```

Example with a diff passed in:

```yaml
- name: Review staged changes
  run: |
    git diff origin/main...HEAD | claude -p "/code-review" > review.txt
    cat review.txt
```

---

## Model Selection in Headless Mode

Override the model per invocation using `--model`:

```bash
# Fast and cheap for high-volume tasks
claude --model haiku -p "/commit-message"

# Powerful for complex analysis
claude --model opus -p "/deep-analysis"
```

If the skill frontmatter sets `model:`, the frontmatter value takes precedence over the session default but is overridden by an explicit `--model` flag on the command line.

---

## Permission Mode in Headless Mode

By default, Claude Code will prompt for tool permissions even in headless mode, which causes the process to block. Use `--allowedTools` to pre-approve specific tools:

```bash
# Pre-approve git commands
claude -p "/safe-commit" --allowedTools "Bash(git *)"

# Pre-approve read-only file access
claude -p "/analyze-codebase" --allowedTools "Read Grep Glob"

# Pre-approve multiple tool categories
claude -p "/deploy" --allowedTools "Bash(git *) Bash(kubectl *) Read"
```

For fully automated environments where the environment itself is trusted and tool prompting would break the pipeline:

```bash
claude --dangerously-skip-permissions -p "/automated-task"
```

Only use `--dangerously-skip-permissions` in isolated environments where you control what the skill does and trust the full execution path. Do not use it locally as a general convenience shortcut.

---

## Piping Multiple Contexts

Combine multiple sources of input using shell grouping:

```bash
# Error log and recent git history together
{ cat error.log; echo "---"; git log --oneline -10; } | claude -p "/diagnose-error"
```

```bash
# Two files compared
{ echo "=== BEFORE ==="; cat before.py; echo "=== AFTER ==="; cat after.py; } | claude -p "/explain-diff"
```

```bash
# Directory listing plus a specific file
{ ls -la src/; echo "---"; cat src/index.ts; } | claude -p "/suggest-refactor"
```

---

## Output Format

Skills invoked headlessly should produce clean output that downstream commands can consume. By default, Claude produces conversational responses with preamble and explanation. For automation, suppress this in the skill body.

Add to the skill body for headless-compatible output:

```
Output only the result. Do not include explanation, preamble, or any text other than the requested content.
```

For JSON output that will be parsed downstream:

```
Output valid JSON with no markdown fencing, no explanation, and no additional text.
```

For Markdown that will be passed to another tool:

```
Output Markdown only. Do not include any explanation before or after the Markdown content.
```

If you want one skill to work in both interactive and headless contexts, you can condition on the effort level:

```
If CLAUDE_EFFORT is low: output a concise one-paragraph result.
Otherwise: output a full structured response.
```

Then pass `--effort low` in headless invocations where you want terse output.

---

## Environment Variables for Headless Mode

| Variable | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` | Required if not set globally in the Claude Code config |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` | Disables background subagents; useful in resource-constrained CI environments |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | Overrides the skill description budget in characters; useful if many skills are installed and some are being dropped |

Example combining multiple variables:

```bash
ANTHROPIC_API_KEY="sk-..." \
CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1 \
SLASH_COMMAND_TOOL_CHAR_BUDGET=4000 \
claude -p "/generate-report"
```

---

## Headless-Compatible Skill Design

Skills intended for headless use benefit from these patterns:

**Explicit output format instructions.** Tell the skill exactly what format to produce and prohibit preamble. Claude's default conversational behavior degrades automation pipelines.

**No interactive prompts.** The skill body should not ask clarifying questions. If required information is missing, fail with a clear error message that goes to stderr, not an interactive question.

**Exit codes.** `claude -p` exits 0 on success and non-zero on failure. Use this in shell scripts:

```bash
if ! claude -p "/validate-config" < config.yaml; then
  echo "Config validation failed" >&2
  exit 1
fi
```

**Deterministic arguments.** Document required arguments clearly. In headless invocations, there is no opportunity to correct a mistyped argument interactively.

**Short skills for high-volume tasks.** Shorter skill bodies load faster and cost fewer tokens. If a skill runs thousands of times a day in CI, every token in the body costs money. Keep the body focused.
