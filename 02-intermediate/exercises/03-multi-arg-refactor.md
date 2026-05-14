# Exercise 03: Multi-argument Symbol Rename

Create a skill that takes three named arguments and renames a symbol across a specified scope. This exercise focuses on the `arguments` field, named argument references in the body, and safe find-and-replace logic.

## Goal

The skill takes three arguments:
1. `old-name` — the current name of the symbol
2. `new-name` — the name to replace it with
3. `scope` — where to search: `file`, `module`, or `project`

Example invocations:
```
/rename-symbol MyClass MyService file
/rename-symbol getUserById fetchUserById module
/rename-symbol legacyConfig appConfig project
```

## What to write

The skill must:

1. Declare named arguments in frontmatter: `arguments: [old-name, new-name, scope]`
2. Use `$old-name`, `$new-name`, and `$scope` in the body (not `$0`, `$1`, `$2`)
3. Set `disable-model-invocation: true` — renaming is a side-effect action
4. Set `argument-hint: [old-name] [new-name] [file|module|project]`
5. Include `allowed-tools` for the tools it needs (grep, sed, git diff, etc.)

## Scope definitions

**`file`**: Rename only within the current file or the file explicitly mentioned in the task.

**`module`**: Rename within the directory containing the current file and its immediate subdirectories.

**`project`**: Rename across the entire project, excluding `node_modules/`, `.git/`, `dist/`, and `build/`.

## Safety requirements

The skill must NOT rename substrings. `MyClass` must not rename `MyClassExtended` or `loadMyClass`. Use word boundary patterns in your grep and sed commands.

The skill must show the user a preview before making any changes, and ask for confirmation.

## Validation

Write the skill and test it on a small project:
1. Create a file with a symbol used in three places.
2. Invoke the skill with `file` scope.
3. Confirm it previews the changes correctly.
4. Confirm it does not rename partial matches.
5. Confirm `git diff` shows only the expected changes after confirmation.

## Solution

A worked solution is in `solutions/03-rename-symbol/SKILL.md`.
