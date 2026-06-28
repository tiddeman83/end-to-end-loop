#!/usr/bin/env bash
# Install end-to-end-loop skill to ~/.agents/skills/end-to-end-loop/
# Run from the repo root: bash scripts/install.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_DIR="$HOME/.agents/skills/end-to-end-loop"

echo "Installing end-to-end-loop skill to $SKILL_DIR ..."

mkdir -p "$SKILL_DIR/references" "$SKILL_DIR/agents" "$SKILL_DIR/scripts" "$SKILL_DIR/skills" "$SKILL_DIR/evals"

cp "$REPO_ROOT/SKILL.md" "$SKILL_DIR/SKILL.md"
cp "$REPO_ROOT/VERSION" "$SKILL_DIR/VERSION"
cp "$REPO_ROOT/.gitignore" "$SKILL_DIR/.gitignore"
cp "$REPO_ROOT/AGENTS.md" "$SKILL_DIR/AGENTS.md"
cp "$REPO_ROOT/.hermes.md" "$SKILL_DIR/.hermes.md"
mkdir -p "$SKILL_DIR/.github/workflows"
cp "$REPO_ROOT/.github/workflows/validate.yml" "$SKILL_DIR/.github/workflows/validate.yml"
cp "$REPO_ROOT/references/"*.md "$SKILL_DIR/references/"
cp "$REPO_ROOT/agents/openai.yaml" "$SKILL_DIR/agents/openai.yaml"
cp -R "$REPO_ROOT/skills/." "$SKILL_DIR/skills/"
cp -R "$REPO_ROOT/evals/." "$SKILL_DIR/evals/"
cp "$REPO_ROOT/scripts/validate_skill.py" "$SKILL_DIR/scripts/validate_skill.py"
cp "$REPO_ROOT/scripts/install.sh" "$SKILL_DIR/scripts/install.sh"
cp "$REPO_ROOT/scripts/telemetry_record.py" "$SKILL_DIR/scripts/telemetry_record.py"
cp "$REPO_ROOT/scripts/telemetry_aggregate.py" "$SKILL_DIR/scripts/telemetry_aggregate.py"
cp "$REPO_ROOT/scripts/test_telemetry_privacy.py" "$SKILL_DIR/scripts/test_telemetry_privacy.py"

echo "Done. Reload your agent session to pick up changes."
