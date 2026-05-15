---
title: "codebase-visualizer"
name: codebase-visualizer
description: Generate an interactive HTML tree visualization of the current project's file structure, with file sizes, color-coded file types, and a sidebar summary. Use when exploring a new repository, understanding project layout, identifying large files, or getting an overview of a codebase.
allowed-tools: Bash(python3 *) Bash(open *) Bash(xdg-open *)
---

Generate an interactive collapsible HTML tree of the project.

## Usage

Run the visualizer script from the project root:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/visualize.py .
```

This creates `codebase-map.html` in the current directory and opens it in the default browser.

## What it shows

- Collapsible directory tree — click any folder to expand or collapse it
- File sizes displayed next to each file name
- Color-coded dots for file types (.js, .ts, .py, .go, .rs, and more)
- Directory size totals (sum of all files within)
- Sidebar summary: total file count, directory count, total size, number of unique file types
- Bar chart of the top 8 file types by total size

Ignored automatically: `.git`, `node_modules`, `__pycache__`, `.venv`, `venv`, `dist`, `build`, and any directory or file whose name starts with `.`.

## Instructions

1. Run the command above from the root of the project you want to visualize.
2. Report the absolute path of the generated file.
3. The script opens the file in the default browser automatically. If it does not open, tell the user to open the reported path manually.
4. If Python 3 is not available, report the error from the command and stop.
