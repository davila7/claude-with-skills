---
name: code-quality-audit
description: Run a comprehensive code quality audit covering security, performance, and maintainability. Use for quarterly audits, pre-release reviews, or when onboarding to a large codebase.
context: fork
agent: Explore
---

Run a comprehensive code quality audit of this codebase.

## Audit areas

Investigate each area systematically. Search broadly before drawing conclusions — read files, grep for patterns, and check multiple directories.

### Security

Look for common security issues:

- Hardcoded secrets: search for `password=`, `api_key=`, `secret=`, `token=` followed by a literal string value in non-test, non-example files
- SQL injection vectors: string concatenation or f-strings/template literals that embed variables directly into SQL query strings
- XSS: direct `innerHTML` assignment in JavaScript or TypeScript files without sanitization
- Insecure defaults: `DEBUG=True`, `CORS allow *`, `verify=False` in requests calls, `NODE_ENV` not set to production in deployment config

### Performance

Look for patterns that commonly cause performance problems:

- N+1 query patterns: a database call inside a loop
- Synchronous operations that could be async: blocking I/O in a path that handles concurrent requests
- Large files read entirely into memory: `fs.readFileSync`, `open().read()` on files that are not guaranteed to be small

### Maintainability

- Functions over 50 lines: read source files and estimate function lengths
- Files over 300 lines: use `find . -name "*.py" -o -name "*.ts" -o -name "*.js" | xargs wc -l | sort -rn | head -20` (exclude node_modules, dist, .git)
- Deeply nested conditionals: more than 4 levels of if/for/while nesting
- Magic numbers: numeric literals used directly in conditions without a named constant

### Dependencies

Read `package.json`, `requirements.txt`, or `go.mod`. Note:
- Packages listed as deprecated in their README or comments in the file
- Packages with obvious CVE mentions in README or lock file comments
- Packages pinned to very old major versions (e.g., a major version more than 2 behind current)

## Output format

Return a structured report with these sections:

**Executive summary** — three bullet points covering the most important findings across all areas.

**Findings by area** — for each area (Security, Performance, Maintainability, Dependencies):
- Critical: must fix before release
- Warning: should fix soon
- Suggestion: worth addressing when time permits

Each finding must include a specific `file:line` reference. Do not list findings without a location.

**Top 3 recommended fixes** — the three findings that would have the greatest positive impact, in priority order, with a brief rationale for each.

If an audit area has no findings, state "No issues found" for that area rather than omitting it.
