---
title: "security-scan"
name: security-scan
description: "Scan the codebase for common security issues: hardcoded secrets, SQL injection vectors, XSS, unvalidated inputs, and insecure defaults. Use before deploying, as part of code quality review, or when asked to check for security issues."
context: fork
agent: Explore
allowed-tools: "Grep Glob Read Bash(git diff *) Bash(git log *)"
---

Run a security scan on this codebase.

## Changed files (focus here first)

!`git diff --name-only HEAD~1 2>/dev/null || git diff --name-only origin/main...HEAD 2>/dev/null || echo "all files — no git diff available"`

Prioritize scanning the files listed above. If the output says "all files", scan the entire codebase.

## Security checks

For each check, search the changed files first. If changed files is "all files", search the entire codebase excluding `node_modules/`, `dist/`, `.git/`, `vendor/`, and `*.min.js`.

### 1. Hardcoded secrets

Search for patterns like `password=`, `api_key=`, `secret=`, `token=`, `passwd=`, `private_key=` followed by a literal value (not a variable reference or environment variable lookup).

Exclude:
- Files in `test/`, `spec/`, `__tests__/` directories
- Files ending in `.example`, `.sample`, `.template`
- Lines that contain `process.env`, `os.environ`, `getenv`, `${`, `$(`, or `config.get`

### 2. SQL injection risk

Search for SQL keywords (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `WHERE`, `FROM`) appearing inside f-strings (Python), template literals (JavaScript/TypeScript), or string concatenation patterns where a variable is embedded directly. Look for patterns like:
- `f"SELECT ... {variable}`
- `` `SELECT ... ${variable}` ``
- `"SELECT " + variable`

### 3. XSS vectors

Search `.js` and `.ts` files for `innerHTML` being assigned a value that includes a variable: `element.innerHTML = `, `.innerHTML +=`. Flag any assignment that does not call a sanitization function (`DOMPurify.sanitize`, `sanitize(`, `escapeHtml(`).

### 4. Unvalidated inputs

Search for patterns where request body or parameters are passed directly to a database function without an intervening validation step. Look for `req.body.`, `request.data`, `request.form`, `params[` in close proximity (within 5 lines) to database calls (`query(`, `execute(`, `find(`, `.save(`, `.create(`).

### 5. Insecure defaults

Search for:
- `DEBUG = True` or `DEBUG=True` (Python)
- `NODE_ENV` not set to `production` in deployment configuration files
- `verify=False` in Python requests calls
- CORS configured to allow all origins: `cors({ origin: '*' })`, `Access-Control-Allow-Origin: *` in non-development config files

## Output format

Output exactly:

```
SECURITY FINDINGS:
- [CRITICAL|HIGH|MEDIUM|LOW] <file>:<line> — <description>
```

Use these severity levels:
- CRITICAL: hardcoded secret or SQL injection
- HIGH: XSS or unvalidated input in an auth path
- MEDIUM: unvalidated input in a non-auth path, `DEBUG=True` in a deployed config
- LOW: insecure default that is acceptable in development but not production

If no findings: output exactly `SECURITY FINDINGS: none`

Do not add any prose before or after the findings block.
