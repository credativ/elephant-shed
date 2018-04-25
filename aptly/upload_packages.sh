#!/bin/bash

set -eu

REPO="$1"
FILES_PATTERN=".*\.(deb|changes|dsc|tgz|tar\.xz|tar\.gz|tar\.bz2)"
SERVER="http://172.26.251.70:8080"

cmd="curl -fX POST"

if [ -d "${2:-}" ]; then
    DIR="$2"
    files=$(find "$DIR" -maxdepth 1 -regextype posix-egrep -regex "$FILES_PATTERN")
else
    shift
    files="$@"
fi

for file in $files; do
    cmd+=" -F file=@\"$file\""
done

echo -e "Uploading the following files:\n$files"

# no trailing slash!
cmd+=" $SERVER/api/files/$REPO"

set -x
$cmd
