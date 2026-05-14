# Setup: Prerequisites and Workspace Configuration

This page walks through everything you need before running the examples in this course.

## Prerequisites

**Claude Code** must be installed and authenticated.

Check your installation:

```bash
claude --version
```

If the command is not found, install Claude Code from [claude.ai/code](https://claude.ai/code) and follow the authentication steps before continuing.

## Where skills can live

Claude Code looks for skills in four locations, checked in this order. A skill found earlier in the list takes precedence over a skill with the same name found later.

| Scope | Path | Who it applies to |
|---|---|---|
| Enterprise | Set by your organization's admin config | All users in the organization |
| Personal | `~/.claude/skills/` | You, across all projects |
| Project | `<project-root>/.claude/skills/` | Anyone who opens that project |
| Plugin | Provided by a Claude Code plugin | Users who have the plugin installed |

For this course, you will use the personal scope (`~/.claude/skills/`) for most examples so that the skills are available regardless of which directory you are in.

## Install the hello-skill example

### Manual installation

```bash
# Create the personal skills directory if it does not exist
mkdir -p ~/.claude/skills

# Copy the hello-skill example
cp -r examples/hello-skill ~/.claude/skills/
```

### Using the install script

The `scripts/install-examples.sh` script handles validation and copying:

```bash
bash scripts/install-examples.sh examples/hello-skill personal
```

The script will confirm the installation path and print the command to invoke the skill.

## Confirm a skill is loaded

Open Claude Code in interactive mode:

```bash
claude
```

Then type:

```
what skills are available?
```

Claude will list the skills it found at startup, including `hello-skill` if the installation succeeded. You can also invoke it directly:

```
/hello-skill
```

## Headless mode basics

Headless mode (`claude -p`) runs Claude Code non-interactively — useful for scripts, CI pipelines, and chaining commands. Claude processes the prompt, writes output to stdout, and exits.

```bash
claude -p "summarize the last 5 git commits"
```

Use headless mode when you want to automate a task or integrate Claude into a shell pipeline. Use interactive mode when you are exploring, iterating, or want to have a back-and-forth conversation.

## Invoking skills in headless mode

There are three common patterns:

**Pattern 1 — Invoke by name:**

```bash
claude -p "/hello-skill"
```

**Pattern 2 — Invoke with an argument:**

```bash
claude -p "/hello-skill World"
```

**Pattern 3 — Pipe input as context:**

```bash
echo "some context or data" | claude -p "/hello-skill"
```

The piped content arrives as stdin. Skills can read it via the `${stdin}` placeholder or by referencing the input in their instructions. This is useful when the skill needs to process a file, a command's output, or a block of text you have already prepared.

## Next steps

With your environment set up and `hello-skill` confirmed working, continue to the first section:

- [01-basic](../01-basic/README.md) — writing your first real skill from scratch
