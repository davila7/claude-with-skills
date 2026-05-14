#!/usr/bin/env bash
# install-examples.sh
#
# Installs a Claude Code skill example into either the personal or project
# skills directory.
#
# Usage:
#   bash scripts/install-examples.sh <skill-dir> <scope>
#
#   skill-dir  Path to the skill example directory (must contain SKILL.md)
#   scope      Where to install: "personal" or "project"
#
# Examples:
#   bash scripts/install-examples.sh examples/hello-skill personal
#   bash scripts/install-examples.sh examples/git-commit-helper project

set -euo pipefail

# ---------------------------------------------------------------------------
# Argument validation
# ---------------------------------------------------------------------------

if [[ $# -ne 2 ]]; then
  echo "Error: expected exactly 2 arguments." >&2
  echo "Usage: $0 <skill-dir> <scope>" >&2
  echo "  scope must be 'personal' or 'project'" >&2
  exit 1
fi

SKILL_SOURCE="$1"
SCOPE="$2"

# Resolve to an absolute path so the script works from any working directory.
SKILL_SOURCE="$(cd "$SKILL_SOURCE" 2>/dev/null && pwd)" || {
  echo "Error: directory not found: $1" >&2
  exit 1
}

# Confirm the source contains a SKILL.md file (AgentSkills requirement).
if [[ ! -f "$SKILL_SOURCE/SKILL.md" ]]; then
  echo "Error: SKILL.md not found in $SKILL_SOURCE" >&2
  echo "Every skill directory must contain a SKILL.md file." >&2
  exit 1
fi

# Derive the skill name from the directory basename.
SKILL_NAME="$(basename "$SKILL_SOURCE")"

# ---------------------------------------------------------------------------
# Determine the destination directory
# ---------------------------------------------------------------------------

case "$SCOPE" in
  personal)
    DEST_BASE="$HOME/.claude/skills"
    ;;
  project)
    DEST_BASE="$(pwd)/.claude/skills"
    ;;
  *)
    echo "Error: scope must be 'personal' or 'project', got: $SCOPE" >&2
    exit 1
    ;;
esac

DEST="$DEST_BASE/$SKILL_NAME"

# ---------------------------------------------------------------------------
# Install
# ---------------------------------------------------------------------------

# Create the destination base directory if it does not exist yet.
mkdir -p "$DEST_BASE"

# If a previous installation exists, remove it so we get a clean copy.
if [[ -d "$DEST" ]]; then
  echo "Replacing existing installation at $DEST"
  rm -rf "$DEST"
fi

cp -r "$SKILL_SOURCE" "$DEST"

# ---------------------------------------------------------------------------
# Confirmation
# ---------------------------------------------------------------------------

echo ""
echo "Skill installed successfully."
echo "  Name : $SKILL_NAME"
echo "  Scope: $SCOPE"
echo "  Path : $DEST"
echo ""
echo "To invoke the skill, open Claude Code and type:"
echo "  /$SKILL_NAME"
echo ""
echo "Or in headless mode:"
echo "  claude -p \"/$SKILL_NAME\""
