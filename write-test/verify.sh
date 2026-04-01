#!/bin/bash
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOC="$DIR/doc.md"

if [ ! -f "$DOC" ]; then
    echo "ERROR: $DOC not found"; exit 1
fi

echo "=== Document ==="
echo
cat "$DOC"
echo
echo "=== Integrity Checks ==="
echo

FAIL=0

# Parse header stats
total_turns=$(grep "^Total turns completed:" "$DOC" | awk '{print $4}')
slots_header=$(grep "^Slots occupied:" "$DOC" | awk '{print $3}')

# Count actual slot lines
actual_slots=$(grep -cE '^ ?[0-9]+: agent-' "$DOC" 2>/dev/null || echo "0")

# 1. Slots occupied header matches actual count
if [ "$slots_header" = "$actual_slots" ]; then
    echo "PASS: Slots occupied header ($slots_header) matches actual slot lines ($actual_slots)"
else
    echo "FAIL: Slots occupied header ($slots_header) != actual slot lines ($actual_slots)"
    FAIL=1
fi

# 2. Slot Registry is sorted with no duplicates
prev=0
sort_ok=1
while IFS= read -r line; do
    num=$(echo "$line" | grep -oE '^ *[0-9]+' | tr -d ' ')
    [ -z "$num" ] && continue
    if [ "$num" -le "$prev" ]; then
        echo "FAIL: Sort/duplicate violation — slot $num at or before slot $prev"
        FAIL=1; sort_ok=0
    fi
    prev=$num
done < <(grep -E '^ ?[0-9]+: agent-' "$DOC" 2>/dev/null || true)
[ "$sort_ok" -eq 1 ] && echo "PASS: Slot Registry sorted, no duplicates"

# 3. Per-agent turn sum matches Total turns completed
agent_sum=0
while IFS= read -r line; do
    n=$(echo "$line" | grep -oE '[0-9]+ turns' | awk '{print $1}')
    [ -n "$n" ] && agent_sum=$((agent_sum + n))
done < <(grep -E '^agent-[a-z]+: [0-9]+ turns' "$DOC" 2>/dev/null || true)

if [ "$agent_sum" = "$total_turns" ]; then
    echo "PASS: Per-agent turn sum ($agent_sum) == Total turns completed ($total_turns)"
else
    echo "FAIL: Per-agent turn sum ($agent_sum) != Total turns completed ($total_turns)"
    FAIL=1
fi

# 4. Show per-agent log summaries if available
echo
echo "=== Agent Logs ==="
for log in "$DIR"/agent-*.log; do
    [ -f "$log" ] || continue
    name=$(basename "$log" .log)
    total=$(wc -l < "$log" | tr -d ' ')
    successes=$(grep -c "status=SUCCESS" "$log" 2>/dev/null || echo 0)
    retries=$(grep -c "status=CAS_RETRY" "$log" 2>/dev/null || echo 0)
    echo "$name: $total log lines, $successes successes, $retries CAS retries"
done

echo
if [ "$FAIL" -eq 0 ]; then
    echo "ALL CHECKS PASSED"
else
    echo "INTEGRITY VIOLATIONS DETECTED"
    exit 1
fi
