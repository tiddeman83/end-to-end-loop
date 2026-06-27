#!/usr/bin/env bash
# Install end-to-end-loop skill to ~/.agents/skills/end-to-end-loop/
# Run from the repo root: bash scripts/install.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_DIR="$HOME/.agents/skills/end-to-end-loop"

echo "Installing end-to-end-loop skill to $SKILL_DIR ..."

mkdir -p "$SKILL_DIR/references" "$SKILL_DIR/agents"

cp "$REPO_ROOT/SKILL.md" "$SKILL_DIR/SKILL.md"
cp "$REPO_ROOT/references/"*.md "$SKILL_DIR/references/"
cp "$REPO_ROOT/agents/openai.yaml" "$SKILL_DIR/agents/openai.yaml"

echo "Done. Reload your agent session to pick up changes."
