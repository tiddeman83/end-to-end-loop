#!/usr/bin/env bash
# Install the minimal end-to-end-loop runtime to ~/.agents/skills/end-to-end-loop/
# Run from the repo root: bash scripts/install.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_DIR="$HOME/.agents/skills/end-to-end-loop"

echo "Installing end-to-end-loop skill to $SKILL_DIR ..."

while IFS= read -r relative_path; do
  mkdir -p "$SKILL_DIR/$(dirname "$relative_path")"
  cp "$REPO_ROOT/$relative_path" "$SKILL_DIR/$relative_path"
done < <(
  python3 -c 'import json, pathlib, sys; data = json.loads(pathlib.Path(sys.argv[1]).read_text()); print("\n".join(data["profiles"]["runtime"]))' "$REPO_ROOT/runtime-package.json"
)

echo "Done. Reload your agent session to pick up changes."
