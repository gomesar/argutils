#!/bin/bash
#

path="$1"
days_ago="$(($2 - 1))"
cut_time=`date -d "$days_ago days ago" '+%Y-%m-%d 00:00:00'`

echo "Path:   '$path'"
echo "Before: '$cut_time'  (Today: $(date '+%Y-%m-%d %H:%M:%S'))"
echo -e "\tConfirm? (y/other)"
read confirm

if [[ "$confirm" != "y" ]]; then
    echo "Quitting"
    exit 0
else
    find "$path" -daystart -mtime +"$days_ago" -type f -delete -print
fi
