#!/usr/bin/env bash

# NOTE: We get the passwort from gitlab-ci.

export OS_AUTH_URL=https://nova.credativ.com:5000/v2.0
export OS_TENANT_ID=27498e6ffaca49f7b57a14ef505e3098
export OS_TENANT_NAME="database"
unset OS_PROJECT_ID
unset OS_PROJECT_NAME
unset OS_USER_DOMAIN_NAME
export OS_USERNAME="app_dbteam"
export OS_REGION_NAME="regionOne"
if [ -z "$OS_REGION_NAME" ]; then unset OS_REGION_NAME; fi

# Use our own certificate
export OS_CACERT="$(dirname $0)/credativDeutschlandServerCA-chain.pem"
