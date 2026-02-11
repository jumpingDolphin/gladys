#!/bin/bash
# Usage: ./sync_task.sh <task_content> <status> [task_id] [description] [labels_json_array]
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../config.env"

CONTENT=$1
STATUS=$2
TASK_ID=$3
DESCRIPTION=$4
LABELS=$5

case $STATUS in
  "In Progress") SECTION_ID="$SECTION_IN_PROGRESS" ;;
  "Waiting")     SECTION_ID="$SECTION_WAITING" ;;
  "Done")        SECTION_ID="$SECTION_DONE" ;;
  *)             SECTION_ID="" ;;
esac

PAYLOAD="{\"content\": \"$CONTENT\""
[ -n "$SECTION_ID" ] && PAYLOAD="$PAYLOAD, \"section_id\": \"$SECTION_ID\""
[ -n "$PROJECT_ID" ] && [ -z "$TASK_ID" ] && PAYLOAD="$PAYLOAD, \"project_id\": \"$PROJECT_ID\""
if [ -n "$DESCRIPTION" ]; then
  ESC_DESC=$(echo "$DESCRIPTION" | sed ':a;N;$!ba;s/\n/\\n/g' | sed 's/"/\\"/g')
  PAYLOAD="$PAYLOAD, \"description\": \"$ESC_DESC\""
fi
[ -n "$LABELS" ] && PAYLOAD="$PAYLOAD, \"labels\": $LABELS"
PAYLOAD="$PAYLOAD}"

if [ -n "$TASK_ID" ]; then
  "$SCRIPT_DIR/todoist_api.sh" "tasks/$TASK_ID" POST "$PAYLOAD"
else
  "$SCRIPT_DIR/todoist_api.sh" "tasks" POST "$PAYLOAD"
fi
