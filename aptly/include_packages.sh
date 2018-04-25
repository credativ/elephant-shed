#!/bin/bash

set -eu

REPO="$1"
SERVER="http://172.26.251.70:8080"

set -x
curl -fX POST "$SERVER/api/repos/$REPO/file/$REPO?forceReplace=1"
