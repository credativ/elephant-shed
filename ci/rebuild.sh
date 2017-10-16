#!/bin/bash

# This script prepares a rebuild of our debian package for testing
# purpose.
# It takes the last git tag and the number of commits since then.
# Based on this information it generates a new changelog entry.
#
# E.g.: If we have 2 commits since tag 1.1 the new changelog will
# represent version 1.1~2 which is lower than the actual version 1.1.

set -eu

export DEBFULLNAME="Gitlab CI (credativ)"
export DEBEMAIL="dbteam@credativ.com"

orig_version=$(dpkg-parsechangelog -S version)
commit_count=$(git log `git describe --tags --abbrev=0`..HEAD --oneline | wc -l)
new_version="${orig_version}~${commit_count}"

dch --force-bad-version -v ${new_version} "Automatic CI rebuild"
dch -r "Rebuild"
