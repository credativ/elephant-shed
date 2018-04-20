#!/bin/bash

set -eu

. "$(dirname $0)/aptly.conf"

SERVER="http://172.26.251.70:8080"

set -x
curl -fX POST "$SERVER/api/repos/$LOCAL_REPO/file/elephant-shed?forceReplace=1"
