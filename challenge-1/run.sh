#!/bin/bash

# Count all lines with 500 HTTP code.
count_lines_500=$(grep -E ' HTTP/[0-9].[0-9] 500 ' sample.log | wc -l)
echo "Number of lines with HTTP status code 500: $count_lines_500"

# Count all GET requests from yoko to /rrhh location and if it was successful (200).
count_get_yoko_rrhh=$(awk '$2=="yoko" && $5=="200" && $6=="\"GET" && $7=="/rrhh\""' sample.log | wc -l)
echo "Number of GET requests from yoko to /rrhh: $count_get_yoko_rrhh"

# How many requests go to /?
count_requests_root=$(awk '$7=="/\""' sample.log | wc -l)
echo "Number of requests (GET|POST|etc.) to /: $count_requests_root"

# Count all lines without 5XX HTTP code.
count_lines_without_5xx=$(grep -Ev ' HTTP/[0-9].[0-9] 5[0-9][0-9] ' sample.log | wc -l)
echo "Number of lines without 5XX HTTP status code: $count_lines_without_5xx"

# Replace all 503 HTTP codes by 500, how many requests have a 500 HTTP code?
# Not using -i as it needs argument '' when used in MacOS, so we will create a
# temp file and replace the original one with it.
sed -E 's/(HTTP\/[0-9.]+ )503 /\1500 /' sample.log > sample_temp.log
mv sample_temp.log sample.log
count_lines_500=$(grep -E ' HTTP/[0-9].[0-9] 500 ' sample.log | wc -l)
echo "Number of lines with HTTP status code 500 after replacement: $count_lines_500"