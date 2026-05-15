---
title: "explain-code"
name: explain-code
description: Explains code in plain language for someone unfamiliar with the programming language. Use when asked to explain code, walk through logic, describe what a function does, or when the user says "explain this" or "walk me through this".
---

## Instructions

1. Identify the code to explain. In order of priority:
   - Code the user just pasted or attached in this conversation
   - The last file that was opened or discussed
   - If it is unclear, ask the user to paste or point to the specific code before proceeding

2. Identify the programming language. Do not assume from the file extension alone — check the syntax if the extension is missing or ambiguous.

3. Explain the code in plain language covering these three areas:

   **Overall purpose** — What does this code do? What problem does it solve or what action does it perform? State this in one or two sentences without using the function or variable names as a substitute for explanation.

   **Main data flow** — How does data move through the code? What comes in, what happens to it, and what comes out? For a function: inputs, transformations, output. For a class: how instances are created and how their state changes. For a script: what it reads, what it produces.

   **Non-obvious logic** — Is there any behavior that would surprise a competent programmer reading this for the first time? Flag things like: side effects, error suppression, hardcoded assumptions, subtle timing dependencies, or clever bitwise operations.

4. Use an analogy if it genuinely makes the concept clearer. Do not force one if the code is self-explanatory once described directly.

5. Limit the explanation to what was asked. If the user pointed to one function, explain that function. Do not expand to the surrounding architecture unless asked.

6. Do not restate the obvious. If a function is named `calculateTax` and it calculates tax, skip the sentence saying "this function calculates tax" and go directly to how it does it.
