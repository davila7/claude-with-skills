---
name: test-coverage-check
description: Check whether changed source files have corresponding test files. Use for code quality review before merging a PR, or when asked whether new code has tests.
context: fork
agent: Explore
allowed-tools: Grep Glob Read Bash(git diff *) Bash(find *)
---

Check whether changed source files have test coverage.

## Changed source files

!`git diff --name-only HEAD~1 2>/dev/null || git diff --name-only origin/main...HEAD 2>/dev/null || echo "none"`

Filter the list above to source files only. Exclude:
- Files already in test directories (`test/`, `spec/`, `__tests__/`, `tests/`)
- Files with `.test.`, `.spec.` in the name
- Non-source files: `.md`, `.json`, `.yaml`, `.yml`, `.lock`, `.txt`, `.env`, `.gitignore`
- Configuration files: `*.config.ts`, `*.config.js`, `vite.config.*`, `jest.config.*`

If the output was "none" or after filtering there are no source files, output: `COVERAGE FINDINGS: none — no changed source files detected`

## Check each source file

For each changed source file, derive candidate test file paths using these conventions:

Given source file `src/utils/parser.ts`, check for:
1. `src/utils/parser.test.ts`
2. `src/utils/parser.spec.ts`
3. `src/utils/__tests__/parser.ts`
4. `src/utils/__tests__/parser.test.ts`
5. `tests/utils/parser.test.ts`
6. `tests/utils/parser.spec.ts`
7. `test/utils/parser.test.ts`
8. `test/utils/parser.spec.ts`

Apply the same pattern for `.py`, `.js`, `.jsx`, `.tsx`, `.go`, `.rb` files, substituting the appropriate test file extension:
- Python: `_test.py` or `test_<name>.py`
- JavaScript/TypeScript: `.test.js`, `.spec.js`, `.test.ts`, `.spec.ts`
- Go: `_test.go` in the same directory
- Ruby: `_spec.rb` in `spec/`

Use Glob to check whether any of the candidate paths exist.

If a test file is found, use Grep to check whether it imports or requires the source file, or references the source file's name. If no import is found, mark as "test file exists but may not cover new changes".

## Output format

Output exactly:

```
COVERAGE FINDINGS:
- <source-file> — no test file found
- <source-file> — test file exists but may not cover new changes
```

Examples:
```
COVERAGE FINDINGS:
- src/auth/loginHandler.ts — no test file found
- src/utils/formatDate.ts — test file exists but may not cover new changes
```

If all changed source files have test files that reference them: output exactly `COVERAGE FINDINGS: none`

Do not add any prose before or after the findings block.
