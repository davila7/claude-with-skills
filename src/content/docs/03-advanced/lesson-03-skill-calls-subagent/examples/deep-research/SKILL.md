---
title: "deep-research"
name: deep-research
description: Research a technical topic thoroughly by exploring the codebase and summarizing findings. Use when asked to investigate how something works, research an area of the codebase, trace a data flow, or understand a component in depth.
context: fork
agent: Explore
argument-hint: [topic or question]
---

Research the following topic thoroughly: $ARGUMENTS

## Steps

1. Identify the scope of the research. Parse the topic into concrete searchable terms: class names, function names, file name patterns, configuration keys, or framework-specific terms.

2. Search broadly before reading deeply:
   - Use Grep to search for the most distinctive identifiers (class names, function names, error strings)
   - Use Glob to find files by name pattern (e.g., `*auth*`, `*middleware*`, `*.config.*`)
   - Prioritize files that appear in multiple search results — they are likely central to the topic

3. Read the most relevant files completely. Do not skim. Missing a detail in a critical file leads to incorrect conclusions.

4. For key files, check recent git history to understand why things are the way they are:
   ```
   git log --oneline --follow -20 <filepath>
   ```
   Read the most informative commit messages. If a commit message references a PR or issue number, note it.

5. Follow import and dependency chains one level deep. If the main file imports from three other modules, read those modules too.

6. Synthesize findings into a structured report with these sections:

   **Overview**
   What this system or component does, in two to four sentences. Write for someone who has never touched this codebase.

   **Key files**
   A table: file path | one-line description of its role. Include every file you read that was materially relevant.

   **How it works**
   The main flow, data structures, and key design decisions. Use concrete terms: function names, type names, config keys. Reference file paths and approximate line numbers for the most important details.

   **Recent changes**
   What changed in the last 20 commits in the relevant area, and why (based on commit messages and diff context).

   **Open questions**
   Anything that is unclear from the code alone and would benefit from asking a team member or reading documentation. Be specific.

7. Be precise. If you are uncertain, say so. Do not infer things that are not in the code.
