# Frontmatter Cheatsheet

Quick reference for all SKILL.md frontmatter fields.

---

## All Fields

### AgentSkills.io Open Standard (Portable)

These fields are defined by the AgentSkills.io open standard. Skills using only these fields remain portable across compatible runtimes.

| Field | Type/Format | Default | What it does | Use when |
|---|---|---|---|---|
| `name` | string, lowercase-hyphens, max 64 chars | directory name | Display name and `/name` command alias | Always — set it explicitly to decouple from directory naming |
| `description` | string, max 1024 chars | first paragraph of SKILL.md body | Tells Claude what the skill does and when to invoke it | Always — Claude reads this to decide on auto-invocation |
| `license` | string | none | Declares the license of the skill content | Distributing or publishing the skill publicly |
| `compatibility` | string, max 500 chars | none | Documents environment requirements such as OS, runtime, or required tools | Skill requires specific tools, OS, or environment that may not be universally available |
| `metadata` | key-value map | none | Arbitrary structured data attached to the skill (version, author, tags, etc.) | Tracking version, authorship, or custom tags without polluting the description |
| `allowed-tools` | space-separated string of tool names | none | Pre-approves listed tools so they never prompt during the skill | Skill needs specific tools and interruptions would break the workflow |

### Claude Code-Only Fields

These fields are understood by Claude Code but are not part of the AgentSkills.io portable standard. They will be ignored or cause errors in other runtimes.

| Field | Type/Format | Default | What it does | Use when |
|---|---|---|---|---|
| `when_to_use` | string | none | Additional trigger phrases appended to the description for auto-invocation matching | You need extra keywords without making the main description verbose |
| `argument-hint` | string | none | Short hint shown in the autocomplete UI next to the skill name | Skill accepts arguments and you want users to know what to type |
| `arguments` | string or list of strings | none | Named argument positions mapped to `$name` variables in the skill body | Skill takes multiple distinct arguments and named references are clearer than index-based |
| `disable-model-invocation` | boolean | `false` | Hides the skill from Claude entirely; only a user can invoke it with `/name` | Side-effect workflows (deploy, send, delete) where you must control timing |
| `user-invocable` | boolean | `true` | When set to `false`, hides the skill from the `/` menu | Background knowledge skills that Claude should use but users never invoke directly |
| `model` | string | inherits session model | Overrides the model used for this skill's execution turn | Deep analysis that needs a larger model (opus) or a trivial task that can use a cheaper one (haiku) |
| `effort` | string: `low`, `medium`, `high`, `xhigh`, or `max` | inherits session effort | Overrides the reasoning effort for this skill's turn | Tasks that need ultrathink-level reasoning or simple generation that does not need extended thinking |
| `context` | string: `fork` | none | Runs the skill in an isolated subagent so it does not pollute the main context | Long or exploratory skills whose intermediate steps should not persist in the main conversation |
| `agent` | string | `general-purpose` | Specifies the subagent type when `context: fork` is set | You want an Explore-style read-only subagent or another specific agent persona |
| `hooks` | map | none | Lifecycle hooks scoped to this skill (pre-tool, post-tool, on-exit, etc.) | Auto-formatting output, validating results, or sending notifications on specific tool use |
| `paths` | list of glob patterns | none | Auto-activates or restricts the skill to sessions involving matching files | Language-specific or domain-specific skills that should only surface for relevant files |
| `shell` | string: `bash` or `powershell` | `bash` | Overrides the shell used for `!`cmd`` inline execution blocks | Windows-only skills that use PowerShell commands |

---

## Invocation Mode Matrix

Controls who can invoke the skill and what appears in context.

| Frontmatter | User `/name` | Claude auto-invokes | Description in context | When full body loads |
|---|---|---|---|---|
| (default) | Yes | Yes | Yes | When invoked by either user or Claude |
| `disable-model-invocation: true` | Yes | No | No | When user invokes with `/name` |
| `user-invocable: false` | No | Yes | Yes | When Claude invokes automatically |
| Both `disable-model-invocation: true` AND `user-invocable: false` | No | No | No | Never — skill is permanently inaccessible |

---

## String Substitution Quick Reference

| Syntax | Expands to |
|---|---|
| `$ARGUMENTS` | Full argument string exactly as typed after the skill name |
| `$ARGUMENTS[0]` or `$0` | First whitespace-split argument (0-indexed, respects shell quoting) |
| `$ARGUMENTS[1]` or `$1` | Second argument |
| `$name` | Named argument from position defined in `arguments` frontmatter |
| `${CLAUDE_SESSION_ID}` | UUID identifying the current Claude Code session |
| `${CLAUDE_EFFORT}` | Current effort level string: `low`, `medium`, `high`, `xhigh`, or `max` |
| `${CLAUDE_SKILL_DIR}` | Absolute path to the directory containing the SKILL.md file |

---

## Common Patterns

Pre-flight check — run a shell command inline and include its output in context:

```
!`git status --short`
```

Multi-line shell block — run multiple commands as a block:

````
```!
git fetch origin
git log --oneline origin/main..HEAD
```
````

Run a bundled script from the skill directory — always use `${CLAUDE_SKILL_DIR}` so the path works at any scope:

```
Bash: python3 ${CLAUDE_SKILL_DIR}/scripts/my_script.py
```

Skill runs in an isolated subagent to avoid polluting main context:

```yaml
context: fork
agent: Explore
```

Subagent preloads a skill so it is available inside the forked context — in the agent definition file, add:

```yaml
skills: [skill-name]
```
