---
title: "Lesson 08: Combining Options"
---

Individual frontmatter fields are straightforward. The challenge is deciding which combination to use for a specific skill. This lesson gives a decision framework and documents the most common mistakes.

## Decision framework

Work through these four questions in order:

### 1. Does this skill have side effects?

Side effects include: pushing to remote, sending messages, writing to external services, deleting files, running deployments, triggering CI jobs.

If yes: set `disable-model-invocation: true`. You do not want Claude triggering this automatically.

If no: leave it unset. Auto-invocation is safe and useful.

### 2. Is this a skill or background knowledge?

If the skill is an action (do X, generate Y, deploy Z): leave `user-invocable` at its default (true). The user should be able to invoke it.

If the skill is knowledge that shapes Claude's behavior (apply these conventions, use this response format, be aware of these constraints): set `user-invocable: false`. It should not appear in the `/` menu.

### 3. Does this skill need live data?

If yes: add `` !`cmd` `` injection for the specific data needed (git state, environment info, PR status, config values). Inject only what Claude needs — avoid injecting large outputs that inflate context size.

If no: skip injection.

### 4. Should this skill only activate for certain file types?

If yes: set `paths` with the appropriate glob patterns.

If no: leave it unset.

After answering these four questions, add `allowed-tools` for any tools the skill needs to use without prompting, and consider `model` and `effort` only if this skill has a clearly different cost/capability requirement than the session default.

---

## Common patterns

### Safe deploy workflow

```yaml
disable-model-invocation: true      # has side effects
argument-hint: [environment]        # user specifies the target
allowed-tools: Bash(npm *) Bash(git *)  # pre-approve needed commands
```

Body uses `$ARGUMENTS` for the target environment and `` !`git status` `` for a pre-flight check.

### Background knowledge skill

```yaml
user-invocable: false               # knowledge, not an action
# description covers all trigger keywords
```

Body contains the conventions, rules, or context. No arguments, no injection needed.

### Path-aware formatter

```yaml
paths: ["src/**", "lib/**"]         # only relevant for source files
allowed-tools: Bash(npx prettier *) # pre-approve the formatter
user-invocable: false               # activated by Claude after edits
```

Body describes the formatting rules and instructs Claude to run prettier after edits.

### Isolated research skill

```yaml
context: fork                       # run in isolated subagent
agent: Explore                      # use the Explore subagent
allowed-tools: Read Grep Glob       # read-only tools
```

Body describes the research task. The fork prevents large research output from polluting the main context.

---

## Common mistakes

### Setting both `disable-model-invocation: true` and `user-invocable: false`

```yaml
# Do not do this
disable-model-invocation: true
user-invocable: false
```

With both set, the skill is inaccessible:
- Claude cannot invoke it (description is not in Claude's context)
- You cannot invoke it (not in the `/` menu)

The only way to run it is `claude -p "/skill-name"` in headless mode. If that is intentional, document it explicitly in the description. If it is not intentional, you have created a skill no one can use.

### Forgetting `allowed-tools` on a skill with `disable-model-invocation: true`

```yaml
disable-model-invocation: true
# allowed-tools omitted
```

Without `allowed-tools`, Claude will ask for permission before every tool call during the skill run. For a deploy workflow with five git commands and two npm commands, that is seven prompts. The user has to click through all of them. Defeat the purpose of a structured workflow by adding `allowed-tools` for the specific commands the skill needs.

### Over-permitting `allowed-tools`

```yaml
allowed-tools: Bash(*)    # permits any bash command
```

This pre-approves every possible shell command. It defeats the purpose of scoping. List only the specific commands the skill needs, using the narrowest patterns that still work:

```yaml
allowed-tools: Bash(npm test) Bash(npm run build) Bash(git status) Bash(git tag *) Bash(git push *)
```

### Using `paths` for user-facing skills

If a user expects to type `/my-skill` and have it work anywhere, do not set `paths`. Path restrictions only reduce auto-invocation false positives — they do not add correctness. A deploy skill should not have `paths` set; it should work from any context.

---

## Examples

- `examples/safe-deploy/` — combines `disable-model-invocation`, `argument-hint`, `allowed-tools`, and dynamic injection into a complete deploy workflow
- `examples/on-edit-formatter/` — combines `paths`, `allowed-tools`, and `user-invocable: false` for a background formatter that runs after edits
