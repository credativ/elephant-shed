#!/bin/bash

set -eu

. "$(dirname $0)/aptly.conf"

cmd="curl -X POST"

if [ -d "${1:-}" ]; then
    DIR="$1"
    files=$(find "$DIR" -maxdepth 1 -regextype posix-egrep -regex "$FILES_PATTERN")
else
    files="$@"
fi

for file in $files; do
    cmd+=" -F file=@\"$file\""
done

echo -e "Uploading the following files:\n$files"

# no trailing slash!
cmd+=" $SERVER/api/files/elephant-shed"

set -x
$cmd
