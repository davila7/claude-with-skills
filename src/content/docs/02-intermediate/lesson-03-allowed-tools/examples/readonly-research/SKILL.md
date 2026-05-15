---
title: "readonly-research"
name: readonly-research
description: Research the codebase to answer a question without making any changes. Use when exploring code, understanding architecture, or investigating how something works.
allowed-tools: Read Grep Glob Bash(find *) Bash(git log *) Bash(git show *)
user-invocable: false
---

## Codebase research

Research the codebase to answer the question or complete the investigation. Do not modify any files. Do not create files. Do not run tests or build commands.

### Step 1: Clarify the question

If `$ARGUMENTS` is empty or ambiguous, state the research question you are answering before proceeding. If the question is clear, proceed directly.

### Step 2: Search for relevant files

Start broad, then narrow. Use a combination of approaches:

- `grep -r "<term>" --include="*.ts" --include="*.js" -l` to find files containing a keyword
- `glob("src/**/*.ts")` or similar to list files in a known area
- `find . -name "<filename>" -not -path "*/node_modules/*"` for specific filenames

Search for the primary concept, then for related symbols, then for tests that exercise the relevant code.

### Step 3: Read the most relevant files

Read the files that are most likely to answer the question. Prioritize:
1. The module or function directly named in the question
2. Its callers and dependents (to understand how it is used)
3. Its tests (to understand expected behavior)
4. Any relevant configuration or type definitions

Avoid reading files speculatively. Only read a file if there is a specific reason it could answer the question.

### Step 4: Check git history if relevant

If the question is about why something is the way it is, or when a change was made, use:
```
git log --oneline --follow -20 <file>
git show <commit-hash>
```

### Step 5: Synthesize findings

Present a clear answer to the research question with:
- The specific answer (yes/no, the function name, the file path, etc.)
- Supporting evidence with file:line references for every specific claim
- Areas of uncertainty: files you could not access, code paths you could not trace, or ambiguities in the implementation

Format the response for the user's question, not as a generic research report. If the user asked "where is the auth logic?", answer that directly, then provide supporting detail.
