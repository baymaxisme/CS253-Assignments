#!/bin/bash

# Check input
if [ $# -ne 1 ]; then
    echo "Usage: bash timeline.sh <clean_log.csv>"
    exit 1
fi

log_file="$1"

awk -F',' '
/Failed password/ {

    # First field contains timestamp
    timestamp = $1

    # Split date and time
    split(timestamp, arr, " ")

    time = arr[2]   # HH:MM:SS

    # Extract hour (first 2 characters)
    hour = substr(time, 1, 2)

    count[hour]++
}

END {
    # Loop from 00 to 23 for sorted output
    for (i = 0; i < 24; i++) {

        # Format hour as 2 digits
        h = sprintf("%02d", i)

        if (h in count) {
            printf("Hour %s: %d failed attempts\n", h, count[h])
        }
    }
}
' "$log_file"
