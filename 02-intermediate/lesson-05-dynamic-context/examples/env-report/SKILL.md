---
name: env-report
description: Report the current development environment: Node, Python, OS, git state. Use when debugging environment issues, onboarding, or checking system compatibility.
---

## Environment snapshot

```!
echo "OS: $(uname -s) $(uname -r)"
echo "Node: $(node --version 2>/dev/null || echo 'not installed')"
echo "npm: $(npm --version 2>/dev/null || echo 'not installed')"
echo "Python: $(python3 --version 2>/dev/null || echo 'not installed')"
echo "Git: $(git --version)"
echo "Git branch: $(git branch --show-current 2>/dev/null || echo 'not in a repo')"
echo "Git status: $(git status --short 2>/dev/null | head -5)"
```

---

Review the environment snapshot above and report:

### Version summary

List each tool with its installed version, or note that it is not installed.

### Compatibility concerns

Flag any of the following:

- Node.js below version 18 (end-of-life, missing fetch API and other modern features)
- npm below version 9
- Python below version 3.9
- Git below version 2.30
- Missing tools that the project likely needs (check for `package.json`, `requirements.txt`, or `pyproject.toml` in the working directory to determine what tools are required)

### Git state summary

If git status output is present:
- Summarize any uncommitted changes (number of modified, untracked, or staged files)
- Note the current branch

### Recommendations

List any concrete steps the user should take to resolve version incompatibilities or missing tools. Include the specific install command where applicable (for example, `nvm install 20` or `brew install node`).

If everything looks compatible and no issues are found, say so clearly.
