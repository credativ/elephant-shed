#!/usr/bin/env bash

# This script assumes that all OS_* variables are set and valid.

set -u

if [ $# -lt 1 ]; then
    cat <<EOF 1>&2
Usage: $0 <instance>

	Where <instance> could be either a machine name or UUID.
EOF
    exit 1
fi

INSTANCE=$1
# Better save than sorry.
test -n $INSTANCE
if [ $? -ne 0 ]; then
    echo "Instance variable is empty, not going any further." 1>&2
    exit 2
fi

which openstack > /dev/null
if [ $? -ne 0 ]; then
    echo "Could not find openstack client utilities." 1>&2
    exit 3
fi

openstack server list | grep -q " $INSTANCE "
if [ $? -ne 0 ]; then
    echo "Instance \"$INSTANCE\" does not exist, exiting."
    exit 0
fi

# If we get here a instance with name / UUID $INSTANCE does exist.
openstack server delete "$INSTANCE"
if [ $? -ne 0 ]; then
    echo "Something went wrong removing the instance \"$INSTANCE\"." 1>&2
    exit 4
fi

echo "Instance \"$INSTANCE\" removed successfully."
