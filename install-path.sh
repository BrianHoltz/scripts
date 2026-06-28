#!/bin/bash
# SPDX-FileCopyrightText: 2026 Brian Holtz
# SPDX-License-Identifier: MIT
#
# install-path.sh - Add /Users/brian/bin to your shell RC file
#
# Usage: /Users/brian/bin/install-path.sh
#
# Adds an export PATH line to your ~/.zshrc (or ~/.bashrc) so that
# brian's tools (rsynk, safewrite, fhold, etc.) are available in your PATH.
#
# Run this once, then restart your shell or source your RC file.

set -e

# Detect shell RC target. Prefer existing ~/.zshrc, then ~/.bashrc,
# otherwise create ~/.zshrc (default shell on modern macOS).
rc_file="$HOME/.zshrc"
if [ ! -f "$rc_file" ]; then
    if [ -f "$HOME/.bashrc" ]; then
        rc_file="$HOME/.bashrc"
    else
        touch "$rc_file"
    fi
fi

# Check if already installed
if grep -q '/Users/brian/bin' "$rc_file"; then
    echo "✓ /Users/brian/bin already in $rc_file"
    exit 0
fi

# Add to PATH
cat >> "$rc_file" <<'EOF'

# Added by install-path.sh - access to brian's bin tools
export PATH="/Users/brian/bin:$PATH"
EOF

echo "✓ Added /Users/brian/bin to $rc_file"
echo ""
echo "Next steps:"
echo "  • Restart your shell, or"
echo "  • Run: source $rc_file"
echo ""
echo "Then verify: which rsynk"
