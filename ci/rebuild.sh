#!/bin/bash

# This script prepares a rebuild of our debian package for testing purposes.

set -eu

DISTTAG="$1"
IS_RELEASE_BUILD="${2:-}" # leave empty for CI build

export DEBFULLNAME="credativ GmbH"
export DEBEMAIL="dbteam@credativ.com"

orig_version=$(dpkg-parsechangelog -S version)
if [ "$IS_RELEASE_BUILD" ]; then
  new_version="${orig_version}~$DISTTAG+1"
else
  date="$(date -u +%Y%m%d.%H%M%S)"
  new_version="${orig_version}~$DISTTAG~${date}"
fi

dch --force-bad-version -v ${new_version} "Automatic CI rebuild"
dch -r "Build for $DISTTAG"
