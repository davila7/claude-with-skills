---
name: rename-symbol
description: Rename a code symbol (variable, function, class) across a specified scope.
disable-model-invocation: true
argument-hint: [old-name] [new-name] [file|module|project]
arguments: [old-name, new-name, scope]
allowed-tools: Grep Glob Read Bash(sed *) Bash(git diff *)
---

## Rename symbol

Rename `$old-name` to `$new-name` within scope: `$scope`.

Valid scopes: `file`, `module`, `project`. If `$scope` is not one of these three values, stop and report: "Invalid scope '$scope'. Use file, module, or project."

### Step 1: Determine the search area

**`file` scope**: Search only the current file being edited, or the specific file the user mentioned in the task context. If the file cannot be determined, ask the user for the path before proceeding.

**`module` scope**: Search the directory containing the current file and its immediate subdirectories (one level deep). Exclude `node_modules/`, `__pycache__/`, `.git/`, `dist/`, and `build/`.

**`project` scope**: Search the entire project from the root. Exclude `node_modules/`, `__pycache__/`, `.git/`, `dist/`, `build/`, and any directory listed in `.gitignore` that represents build output.

### Step 2: Search for all occurrences

Use grep with a word-boundary pattern to find occurrences of `$old-name`. The pattern must match whole words only — it must not match `$old-name` when it appears as part of a longer identifier.

For most languages, use:
```
grep -rn "\b$old-name\b" <search-area> --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --include="*.py" --include="*.go" --include="*.rb" --include="*.java"
```

Adjust the `--include` flags based on the file types in the project. Check which extensions are present before running grep.

If zero occurrences are found, stop and report: "No occurrences of '$old-name' found in the $scope scope."

### Step 3: Show a preview

Before making any changes, show the user the full list of files and lines that will be modified:

```
Found N occurrences of '$old-name' in M files:

src/auth/login.ts:14:  function $old-name(user: User) {
src/auth/login.ts:28:  return $old-name(currentUser);
src/auth/index.ts:3:   export { $old-name } from './login';
```

Then ask: "Rename all occurrences? (yes/no)"

Wait for confirmation before proceeding. If the user says no or provides any response other than yes, stop and report: "Rename cancelled."

### Step 4: Make the replacements

For each file that contains occurrences, apply the substitution using a word-boundary-aware sed pattern:

```
sed -i '' "s/\b$old-name\b/$new-name/g" <file>
```

On Linux, omit the empty string after `-i`:
```
sed -i "s/\b$old-name\b/$new-name/g" <file>
```

Process files one at a time. If sed fails for a specific file, report the error for that file and continue with the remaining files.

### Step 5: Show the diff

After all replacements are made, run:
```
git diff
```

Show the output so the user can verify the changes are correct.

Report a summary:
```
Renamed '$old-name' to '$new-name'.
Files modified: M
Total occurrences replaced: N
```

### Notes

- Do not rename occurrences in comments or string literals unless they are clearly references to the symbol (e.g., JSDoc `@param oldName` references). When in doubt, flag the occurrence in the preview and let the user decide.
- Do not rename file names even if they contain the symbol name. File renaming requires separate handling.
- If the project uses TypeScript, a language server rename via the editor is safer for type-checked renames. Note this at the end of the summary.
