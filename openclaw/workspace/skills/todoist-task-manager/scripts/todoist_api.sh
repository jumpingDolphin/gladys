#!/bin/bash
# Usage: ./todoist_api.sh <endpoint> <method> [data_json]
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../config.env"

ENDPOINT=$1
METHOD=$2
DATA=$3

# Note: Todoist API v1 uses the /sync endpoint with POST commands
# This script is deprecated and should be replaced with sync-based calls
if [ -z "$DATA" ]; then
  curl -s -X "$METHOD" "https://api.todoist.com/api/v1/$ENDPOINT" \
    -H "Authorization: Bearer $TODOIST_TOKEN"
else
  curl -s -X "$METHOD" "https://api.todoist.com/api/v1/$ENDPOINT" \
    -H "Authorization: Bearer $TODOIST_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$DATA"
fi
