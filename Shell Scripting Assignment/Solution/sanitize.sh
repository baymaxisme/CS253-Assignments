#!/bin/bash

# check if input argument is provided
if [ $# -ne 1 ]; then
echo "usage: bash sanitize.sh <input_log_file>"
exit 1
fi

# store input file name
input_file="$1"

# output file name
output_file="clean_log.csv"

sed '
/\[CORRUPT-DATA\]/d;              # Delete corrupted lines
s/user=root/user=SYS_ADMIN/g;     # Replace root user
s/user=admin/user=SYS_ADMIN/g;    # Replace admin user
s/|/,/g                           # Replace pipe with comma
' "$input_file" > "$output_file"


echo "sanitized log saved as $output_file"
