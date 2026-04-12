#!/bin/bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOC="$DIR/doc.md"

# Wipe previous run artifacts
rm -f "$DIR"/agent-*.log 2>/dev/null || true

# Initialize fresh document
cat > "$DOC" << 'DOCEOF'
# Write Coordination Test

## Stats
Total turns completed: 0
Slots occupied: 0 of 20

## Slot Registry
DOCEOF

echo "Initialized: $DOC"
echo "Previous agent logs cleared."
echo "Ready — start agents now."
