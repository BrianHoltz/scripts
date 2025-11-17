#!/bin/bash

# Check for input arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <input-file-1.json> [<input-file-2.json> ...]"
    exit 1
fi

# Process all input files with jq
# Extract date, weight, bmi, and fat as TSV
# Convert date format from MM/DD/YY to YYYY-MM-DD
# Handle missing bmi or fat values by printing empty string
# Then, using sort and awk, filter out only the lowest weight for each date
jq -r '.[] | "\(.date)\t\(.weight)\t\(.bmi // "")\t\(.fat // "")"' "$@" | \
while IFS=$'\t' read -r date weight bmi fat; do
    # Convert date to desired format
    IFS="/" read -r month day year <<< "$date"
    new_date="20$year-$month-$day"
    echo -e "$new_date\t$weight\t$bmi\t$fat"
done | sort -t$'\t' -k1,1 -k2,2n | awk -F'\t' '!seen[$1]++'
exit 0
