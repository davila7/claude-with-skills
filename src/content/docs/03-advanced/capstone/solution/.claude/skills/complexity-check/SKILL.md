---
title: "complexity-check"
name: complexity-check
description: "Find overly complex code: files over 300 lines, functions over 50 lines, deeply nested conditions (4+ levels), and magic numbers. Use for code quality reviews, pre-release checks, or when asked to assess code maintainability."
context: fork
agent: Explore
allowed-tools: "Grep Glob Read Bash(find *) Bash(wc *)"
---

Check the codebase for complexity violations.

## Changed files

!`git diff --name-only HEAD~1 2>/dev/null || git diff --name-only origin/main...HEAD 2>/dev/null || echo "all"`

Focus on the changed files listed above. If "all", check the entire codebase.

## Check 1: Large files

Find source files over 300 lines (exclude node_modules, dist, .git, vendor, coverage, build):

```bash
find . \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.tsx" -o -name "*.jsx" -o -name "*.go" -o -name "*.rb" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/dist/*" \
  -not -path "*/.git/*" \
  -not -path "*/vendor/*" \
  -not -path "*/coverage/*" \
  -not -path "*/build/*" \
  | xargs wc -l 2>/dev/null | sort -rn | head -20
```

Flag any file with more than 300 lines.

## Check 2: Long functions

Read each changed source file (or sample the largest files if "all"). Scan for function or method definitions and estimate the line count between consecutive definitions. Flag any function that appears to span more than 50 lines.

Look for these definition patterns:
- Python: `def ` or `async def `
- TypeScript/JavaScript: `function `, `async function `, `=> {`, `): void {`, `): Promise<`
- Go: `func `
- Ruby: `def `

If a definition is followed by the next definition more than 50 lines later, flag the first function.

## Check 3: Deep nesting

Search changed files for lines with 4 or more levels of indentation inside conditional or loop structures. Use these grep patterns (adjust for tab vs space indentation):

For 4-space indentation (16+ spaces):
```
grep -n "^                " <file>
```

For tab indentation (4+ tabs):
```
grep -n "^\t\t\t\t" <file>
```

Flag files where deeply nested lines appear inside `if`, `for`, `while`, or `switch` blocks.

## Check 4: Magic numbers

Search changed files for numeric literals (other than 0, 1, -1, 2, 100, 1000) used directly in conditions or calculations without a named constant. Look for patterns like:
- `if x > 42:`
- `* 3600`
- `% 7 ==`
- `timeout = 30`

Exclude test files and configuration files where literal values are expected.

## Output format

Output exactly:

```
COMPLEXITY FINDINGS:
- <file>:<line> — <description>
```

Examples:
```
COMPLEXITY FINDINGS:
- src/auth/handler.ts:1 — file is 412 lines (limit: 300)
- src/auth/handler.ts:87 — function processLogin is approximately 63 lines (limit: 50)
- src/utils/parser.py:145 — 5 levels of nesting detected
- src/config.ts:23 — magic number 86400 (consider: SECONDS_PER_DAY)
```

If no findings: output exactly `COMPLEXITY FINDINGS: none`

Do not add any prose before or after the findings block.
