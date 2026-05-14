# Lesson 02: Supporting Scripts with ${CLAUDE_SKILL_DIR}

Skills can do more than instruct Claude — they can ship working code alongside those instructions. When a task involves complex file generation, binary output, or reusable processing logic, a bundled script is the right tool. This lesson explains when to bundle, how the path resolution works, and how to structure scripts that cooperate with Claude effectively.

## The ${CLAUDE_SKILL_DIR} variable

`${CLAUDE_SKILL_DIR}` is always available in the skill body and in any `` !`command` `` dynamic context block. It resolves to the absolute path of the directory that contains the skill's `SKILL.md` file — that is, the skill's root directory.

This variable is critical for bundled scripts. Without it, you would have to hardcode installation paths:

```bash
# Wrong — breaks when the skill is installed anywhere other than this exact path
python3 ~/.claude/skills/my-skill/scripts/generate.py

# Wrong — breaks when the skill is installed at project scope or in a plugin
python3 .claude/skills/my-skill/scripts/generate.py

# Right — works at user scope, project scope, plugin scope, any location
python3 ${CLAUDE_SKILL_DIR}/scripts/generate.py
```

The variable is set by Claude Code at skill load time, not at shell startup. You do not need to export it or add it to your shell configuration.

## When to bundle a script

Bundle a script when the task:

- **Generates non-text output.** HTML files, images, binary formats — these cannot be produced by Claude describing instructions. A working generator script is the only reliable approach.
- **Has significant reusable logic.** A script that parses a custom log format, applies a scoring algorithm, or performs multi-step file transformations is worth shipping with the skill rather than having Claude re-derive the logic each invocation.
- **Requires exact reproducibility.** If the same input must always produce the same output, encode the logic in a script rather than relying on Claude to apply consistent instructions.
- **Processes many files in a loop.** Claude can write a shell loop, but a Python script with proper error handling, progress output, and atomic writes is more robust.

Write inline instructions (without a script) when:

- The task is a one-liner or a simple shell pipeline
- The logic is different every time and cannot be templated
- The script would be shorter than the explanation of what it does

## Script language guidelines

**Python 3** is the best default for bundled scripts. It is available on every platform where Claude Code runs, the standard library covers file I/O, JSON, HTTP, and HTML generation without any installation, and the code is readable enough for users to audit it.

- Declare dependencies explicitly. If the script requires third-party libraries, check for them at the top and print a `pip install` command if they are missing. See `extract.py` in lesson 01 for this pattern.
- Use only the standard library when possible. A script with no external dependencies installs immediately.
- Add a module docstring with usage instructions. Claude reads these when deciding how to invoke the script.

**Bash scripts** work well for shell pipelines where the logic is primarily about combining standard Unix tools. Declare them in `allowed-tools` with `Bash(bash ${CLAUDE_SKILL_DIR}/scripts/*.sh)` or a similar glob.

## How Claude uses bundled scripts

Claude invokes scripts using the `Bash` tool, not the `Read` tool. The script source code does not enter Claude's context unless it is explicitly read with `Read`. This is a form of progressive disclosure: the implementation is free until someone asks how it works.

The skill body tells Claude:
1. What the script does
2. How to invoke it (the exact command, arguments, and flags)
3. What to do with its output

Claude executes the command and uses the output. It does not need to understand the implementation.

## The codebase-visualizer example

The `examples/codebase-visualizer/` directory demonstrates this pattern with a visual output generator. The skill body is 20 lines. The script is ~150 lines of HTML generation code that would be impractical to describe in instructions. Claude invokes the script with one command and reports the output path.

Install and try it:

```bash
cp -r examples/codebase-visualizer ~/.claude/skills/
```

Open Claude Code in any project and type `/codebase-visualizer`. The script generates an interactive HTML file and opens it in the browser.

## Next lesson

[Lesson 03: Skills calling subagents](../lesson-03-skill-calls-subagent/README.md)
