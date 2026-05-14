---
name: code-review-checklist
description: Review code against a standard checklist covering security, correctness, performance, and readability. Use when asked to review code, check a PR, or audit changes.
---

## Instructions

Work through each category in the checklist below. For each item, either confirm it passes or flag the specific file and line number where the issue appears.

### 1. Security

- Hardcoded secrets: check for API keys, passwords, tokens, or credentials embedded in the code
- Input validation: confirm that inputs from external sources (user input, API responses, file contents) are validated before use
- SQL injection: check that any database queries use parameterized statements or an ORM, never raw string concatenation with user input
- Authentication and authorization: if the code touches access control, verify that checks happen server-side and cannot be bypassed by the caller

### 2. Correctness

- Edge cases: null values, empty collections, zero, negative numbers, empty strings — does the code handle these?
- Error paths: are errors caught at the right level? Are they handled or propagated with enough context to debug?
- Off-by-one: check loop bounds and index arithmetic
- Concurrency: if the code runs in a concurrent environment, check for shared mutable state without proper synchronization

### 3. Performance

- N+1 queries: check for database queries inside loops
- Unnecessary work: repeated computation of the same value, re-fetching data that was already fetched
- Memory: large allocations inside tight loops, unbounded collections that grow with input size

### 4. Readability

- Naming: variables, functions, and classes should communicate intent without needing a comment
- Comments: comments should explain why, not what. Flag comments that describe what the code does (the code shows that already) and missing comments where the intent is non-obvious
- Function length: flag functions that do more than one thing or that span more than roughly 40 lines without a clear reason
- Magic numbers: unexplained numeric or string literals that should be named constants

### 5. Tests

- Happy path coverage: does the test suite exercise the main success case?
- Edge case coverage: are the edge cases identified in the Correctness section tested?
- Test clarity: do test names describe the behavior being tested, not the implementation?
- Mocks and stubs: are external dependencies properly isolated in unit tests?

## Output format

Group findings by category. Under each category heading, list specific issues with file name and line number where applicable. If a category has no findings, write "No issues found." at the end of each category.

If the code passes all checks, say so clearly after listing the categories.
