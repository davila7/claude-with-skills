---
title: "jsdoc-writer"
name: jsdoc-writer
description: Add JSDoc comments to JavaScript or TypeScript functions that are missing documentation. Use when asked to document functions, add JSDoc, or improve code comments.
---

## Instructions

Identify the functions or methods that are missing JSDoc comments. If the user specified a file, focus on that file. Otherwise, focus on whatever code is currently being discussed.

For each undocumented function, write a JSDoc block following these rules:

### Content rules

1. Read the function signature to determine parameter names and infer types from usage context, TypeScript annotations, or surrounding code.

2. Write a concise `@description` (one line maximum) that explains what the function does. If the function name already makes this completely obvious (`isAuthenticated`, `formatDate`), skip the description line and let the `@param` and `@returns` tags carry the documentation.

3. Write one `@param` tag per parameter:
   - Include the type in curly braces: `@param {string} name`
   - Add a short description after the parameter name
   - Mark optional parameters with a `?` suffix or bracket notation: `@param {string} [name]`

4. Write `@returns` with the return type and a brief description of what is returned and under what conditions. If the function returns void or never returns a meaningful value, omit `@returns`.

5. Write `@throws` if the function throws an exception under documented conditions: `@throws {TypeError} If name is not a string`.

6. Do not add `@author`, `@date`, `@version`, or other lifecycle metadata — these are noisy and go stale quickly.

### Style rules

- Explain the **why** only when the behavior would surprise a reader who knows JavaScript and the domain. Do not describe what the code does — the code already shows that.
- Keep descriptions short. If a description needs more than one sentence, the function probably does too much.
- Use the existing codebase's type vocabulary. If the codebase calls something a `UserId`, use `UserId`, not `string`.

### Output format

Print the function name as a heading, then the completed JSDoc block. If the function already has a JSDoc block that is incomplete, print the corrected version.

Example output format:

```
getUserById

/**
 * Fetches a user record by its unique identifier.
 * Returns null if no user with that ID exists.
 *
 * @param {string} id - The user's unique identifier.
 * @returns {Promise<User | null>} The user record, or null if not found.
 * @throws {DatabaseError} If the database connection fails.
 */
```
