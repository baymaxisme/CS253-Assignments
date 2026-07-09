#!/bin/bash

#check input
if [ $# -ne 1 ]; then
    echo "Usage: bash report.sh <clean_log.csv>"
    exit 1
fi

log_file="$1"

# Print header
echo "Target Port Analysis"
echo "----------------------"

# Process the file using awk
awk -F',' '
/Failed password/ {

    # Loop through all fields to find "port="
    for(i=1; i<=NF; i++) {
        if($i ~ /port=/) {
            split($i, arr, "=")
            port = arr[2]

            # remove spaces (important!)
            gsub(/ /, "", port)

            count[port]++
        }
    }
}

END {
    # Print result
    for (p in count) {
        printf("Port %s : %d attempts\n", p, count[p])
    }
}
' "$log_file"
