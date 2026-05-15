---
title: "readme-generator"
name: readme-generator
description: Generate a README.md for the current project by analyzing the codebase structure, package files, and existing documentation. Use when asked to write a README, create documentation, or document the project.
allowed-tools: Read Bash(ls *) Bash(find *) Bash(cat package.json) Bash(cat pyproject.toml) Bash(cat Cargo.toml)
---

## Instructions

### Step 1: Detect the project type

Check for language and framework indicators in this order:

- `package.json` — Node.js / JavaScript / TypeScript project
- `pyproject.toml` or `setup.py` — Python project
- `go.mod` — Go project
- `Cargo.toml` — Rust project
- `build.gradle` or `pom.xml` — Java / Kotlin project
- `*.gemspec` or `Gemfile` — Ruby project

Read whichever file is found to extract the project name, version, description, and dependencies.

### Step 2: Read the entry point

Based on the project type, read the main entry point:

- Node.js: check the `main` field in package.json, or look for `src/index.ts`, `src/index.js`, `index.ts`, `index.js`
- Python: look for `__main__.py`, the module directory, or the entry point in pyproject.toml
- Go: `main.go` or `cmd/<name>/main.go`
- Rust: `src/main.rs` or `src/lib.rs`

Read the first 80 lines to understand what the project does.

### Step 3: Survey the structure

Run `ls -1` at the project root and at the `src/` (or equivalent) directory if it exists. Note top-level directories that give structure clues (cli/, api/, lib/, tests/, docs/, examples/).

### Step 4: Write the README

Produce a README.md with the following sections in this order. Include a section only if there is real content for it — do not leave placeholder text in any section except Badges.

```markdown
# Project Name

One sentence describing what the project does and who it is for.

## Badges

<!-- Add badges here: build status, coverage, version, license -->

## Installation

Commands to install the project. Use the package manager detected in step 1.

## Usage

The minimal example to get something working. Show a command or code snippet.
If the project has a CLI, show the most common command.
If it is a library, show an import and a basic function call.

## Configuration

If the project has configuration options (environment variables, config files, flags),
list the important ones with their defaults and descriptions.

## Contributing

Brief instructions: how to set up a dev environment, how to run tests, how to submit a change.

## License

State the license. Read the LICENSE file if present to confirm.
```

After writing the README, tell the user which sections have placeholder content (Badges) and which sections they should review for accuracy (Usage examples especially benefit from human review).
