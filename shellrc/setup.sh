#!/usr/bin/env bash
# ~/bin/shellrc/setup.sh — one-time host setup for ~/bin shellrc dotfiles
# Usage: bash ~/bin/shellrc/setup.sh [-n]
#   -n  Dry run: show what would be done and check for problems; make no changes

DRYRUN=false
while getopts "n" opt; do
    case "$opt" in
        n) DRYRUN=true ;;
        *) echo "Usage: $0 [-n]" >&2; exit 1 ;;
    esac
done

SHELLRC_DIR="$(cd "$(dirname "$0")" && pwd)"
HOME_DIR="$HOME"

# Ordered pairs: "dotfile source_basename"
PAIRS=(
    ".zprofile        zprofile"
    ".zshrc           zshrc"
    ".bash_profile    bash_profile"
    ".bashrc          bashrc"
    ".shellrc.common  shellrc.common"
)

PROBLEMS=0

echo "=== shellrc setup ==="
echo "Source: $SHELLRC_DIR"
echo "Home:   $HOME_DIR"
if $DRYRUN; then
    echo "Mode:   DRY RUN — no changes will be made"
else
    echo "Mode:   LIVE"
fi
echo

# Sanity check: confirm we're in the right directory
if [ ! -f "$SHELLRC_DIR/shellrc.common" ]; then
    echo "ERROR: shellrc.common not found in $SHELLRC_DIR" >&2
    exit 1
fi

# Inspect current state and report what would change
for pair in "${PAIRS[@]}"; do
    dotfile="${pair%% *}"
    src_base="${pair##* }"
    dest="$HOME_DIR/$dotfile"
    target="$SHELLRC_DIR/$src_base"

    if [ ! -f "$target" ]; then
        echo "PROBLEM  $dotfile — source file missing: $target"
        PROBLEMS=$((PROBLEMS + 1))
    elif [ -L "$dest" ]; then
        current="$(readlink "$dest")"
        if [ "$current" = "$target" ]; then
            echo "OK       $dotfile -> $target"
        else
            echo "RELINK   $dotfile"
            echo "         current:  $current"
            echo "         will be:  $target"
        fi
    elif [ -f "$dest" ]; then
        echo "BACKUP   $dotfile (regular file — will be backed up before linking)"
        PROBLEMS=$((PROBLEMS + 1))
    else
        echo "LINK     $dotfile (not present — will be created)"
    fi
done

echo
if [ "$PROBLEMS" -gt 0 ] && $DRYRUN; then
    echo "Issues found above require attention before setup can complete cleanly."
fi

if $DRYRUN; then
    echo "Dry run complete. Re-run without -n to apply changes."
    exit 0
fi

# Abort on missing source files
for pair in "${PAIRS[@]}"; do
    src_base="${pair##* }"
    target="$SHELLRC_DIR/$src_base"
    if [ ! -f "$target" ]; then
        echo "ERROR: source file missing: $target" >&2
        exit 1
    fi
done

# Back up any regular (non-symlink) dotfiles before overwriting
BACKUP_DIR="$HOME_DIR/tmp/shellrc_backup_$(date +%Y%m%d_%H%M%S)"
needs_backup=false
for pair in "${PAIRS[@]}"; do
    dotfile="${pair%% *}"
    dest="$HOME_DIR/$dotfile"
    if [ -f "$dest" ] && [ ! -L "$dest" ]; then
        needs_backup=true
        break
    fi
done

if $needs_backup; then
    mkdir -p "$BACKUP_DIR"
    echo "Backing up regular files to: $BACKUP_DIR"
    for pair in "${PAIRS[@]}"; do
        dotfile="${pair%% *}"
        dest="$HOME_DIR/$dotfile"
        if [ -f "$dest" ] && [ ! -L "$dest" ]; then
            cp -a "$dest" "$BACKUP_DIR/"
            echo "  backed up: $dotfile"
        fi
    done
    echo
fi

# Create symlinks
echo "Creating symlinks..."
for pair in "${PAIRS[@]}"; do
    dotfile="${pair%% *}"
    src_base="${pair##* }"
    dest="$HOME_DIR/$dotfile"
    target="$SHELLRC_DIR/$src_base"
    ln -sfn "$target" "$dest"
    echo "  $dest -> $target"
done

# Verify
echo
echo "Verifying..."
ok=true
for pair in "${PAIRS[@]}"; do
    dotfile="${pair%% *}"
    src_base="${pair##* }"
    dest="$HOME_DIR/$dotfile"
    target="$SHELLRC_DIR/$src_base"
    actual="$(readlink "$dest" 2>/dev/null || true)"
    if [ "$actual" = "$target" ]; then
        echo "  OK   $dest"
    else
        echo "  FAIL $dest (got: $actual)"
        ok=false
    fi
done

echo
if $ok; then
    echo "Setup complete. Open a new terminal tab/window to load the new config."
else
    echo "Some links did not verify — check above." >&2
    exit 1
fi
