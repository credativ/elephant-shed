#!/bin/bash

set -eu

DISTRIBUTION="$1"
SERVER="http://172.26.251.70:8080"

set -x
curl -fX PUT -H 'Content-Type: application/json' --data '{"ForceOverwrite":true}' $SERVER/api/publish/:./$DISTRIBUTION
