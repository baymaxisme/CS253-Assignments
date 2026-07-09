#!/bin/bash

# check if correct number of arguments are passed
if [ $# -ne 3 ]; then
echo "usage: bash detect.sh <clean_log.csv> <whitelist.txt> <output_file>"
exit 1
fi

#input arguments
log_file="$1"
whitelist_file="$2"
output_file="$3"

#clear output file(to ac=void appending old data)
> "$output_file"

awk -F',' '
/Failed password/ {
#awk will only run the following code if the line contains the phrase Failed password.
#It loops through every column (i) in the line.
#If a column contains ip=, it splits that column at the = sign.
#The second half (arr[2]) is the actual IP address.
#count[ip]++ adds 1 to a scorecard for that specific IP.
    for(i=1; i<=NF; i++) {
        if($i ~ /ip=/) {
            split($i, arr, "=")
            ip = arr[2]
            gsub(/ /, "", ip)   # remove spaces
            count[ip]++
        }
    }
}
# After reading the whole file (END), it looks at its scorecard. If any IP failed more than 10 times, it prints the IP and the count.
END {
    for (ip in count) {
        if (count[ip] > 10) {
            print ip, count[ip]
        }
    }
}
' "$log_file" | while read ip cnt
do
    is_whitelisted=0   # Check whitelist manually
# Loop through whitelist file
# This opens whitelist.txt. It compares the Bad IP ($ip) against every Allowed IP ($wip) in that file. If they match, it sets is_whitelisted to 1 and stops looking (break).
    while read wip
    do
        if [ "$ip" = "$wip" ]; then
        is_whitelisted=1
        break
        fi
    done < "$whitelist_file"

# If NOT whitelisted → block it
# If the IP was not found in the whitelist (it’s still 0), it writes a command to the output file.
    if [ $is_whitelisted -eq 0 ]; then
        echo "iptables -A INPUT -s $ip -j DROP # Blocked after $cnt failed attempts" >> "$output_file"
    fi
done

echo "firewall rules written to $output_file"
