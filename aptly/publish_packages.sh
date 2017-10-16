#!/bin/bash

set -eu

. "$(dirname $0)/aptly.conf"

set -x
curl -X PUT -H 'Content-Type: application/json' --data '{"ForceOverwrite":true}' $SERVER/api/publish/:./$DISTRIBUTION
