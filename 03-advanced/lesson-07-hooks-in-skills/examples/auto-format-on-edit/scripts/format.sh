#!/usr/bin/env bash
# format.sh — PostToolUse hook for auto-format-on-edit
#
# Reads hook input from stdin, extracts the edited file path,
# and runs Prettier and ESLint on it if applicable.
#
# Always exits 0. PostToolUse hooks must not block.

set -euo pipefail

# Read the full JSON input from stdin
INPUT=$(cat)

# Extract file path from the hook input.
# PostToolUse for Edit/Write includes tool_response.filePath (Edit)
# and tool_input.file_path (Write). Try both.
FILE_PATH=""

# Try tool_response.filePath first (Edit tool)
if command -v python3 >/dev/null 2>&1; then
  FILE_PATH=$(echo "$INPUT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
# PostToolUse Edit provides filePath in tool_response
path = data.get('tool_response', {}).get('filePath', '')
if not path:
    # Write tool provides file_path in tool_input
    path = data.get('tool_input', {}).get('file_path', '')
print(path)
" 2>/dev/null || echo "")
else
  # Fallback: use grep for basic extraction if python3 is not available
  FILE_PATH=$(echo "$INPUT" | grep -o '"filePath":"[^"]*"' | head -1 | sed 's/"filePath":"//;s/"//' || echo "")
  if [ -z "$FILE_PATH" ]; then
    FILE_PATH=$(echo "$INPUT" | grep -o '"file_path":"[^"]*"' | head -1 | sed 's/"file_path":"//;s/"//' || echo "")
  fi
fi

# Exit early if no file path was found
if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# Exit early if the file does not exist
if [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

# Skip files in node_modules, dist, .git, coverage, or build directories
case "$FILE_PATH" in
  */node_modules/*|*/dist/*|*/.git/*|*/coverage/*|*/build/*|*/.next/*)
    exit 0
    ;;
esac

# Determine the file extension
EXTENSION="${FILE_PATH##*.}"

# Recognized extensions for Prettier
PRETTIER_EXTENSIONS="js ts jsx tsx css json md mjs cjs"

# Check if this extension should be formatted
SHOULD_FORMAT=false
for EXT in $PRETTIER_EXTENSIONS; do
  if [ "$EXTENSION" = "$EXT" ]; then
    SHOULD_FORMAT=true
    break
  fi
done

if [ "$SHOULD_FORMAT" = "false" ]; then
  exit 0
fi

# Run Prettier if available
if command -v npx >/dev/null 2>&1; then
  # Check if prettier is available in this project
  if npx --no-install prettier --version >/dev/null 2>&1; then
    npx --no-install prettier --write "$FILE_PATH" >/dev/null 2>&1 || true
  fi
fi

# Run ESLint --fix for script files only
SCRIPT_EXTENSIONS="js ts jsx tsx mjs cjs"
SHOULD_LINT=false
for EXT in $SCRIPT_EXTENSIONS; do
  if [ "$EXTENSION" = "$EXT" ]; then
    SHOULD_LINT=true
    break
  fi
done

if [ "$SHOULD_LINT" = "true" ]; then
  if command -v npx >/dev/null 2>&1; then
    # Check if eslint is available in this project
    if npx --no-install eslint --version >/dev/null 2>&1; then
      npx --no-install eslint --fix "$FILE_PATH" >/dev/null 2>&1 || true
    fi
  fi
fi

# PostToolUse hooks must always exit 0
exit 0
