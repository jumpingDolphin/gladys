#!/bin/bash
# Add task to personal Todoist
# Usage: ./add_task.sh "Task content" [project_id]

CONTENT="$1"
PROJECT_ID="${2:-6fxjfC8p5mX2mWGW}"  # Default: Inbox

if [ -z "$CONTENT" ]; then
  echo "Usage: $0 \"Task content\" [project_id]"
  exit 1
fi

# Load token from .env
ENV_FILE="$HOME/gladys/openclaw/.env"
if [ -f "$ENV_FILE" ]; then
  source "$ENV_FILE"
fi

curl -s -X POST "https://api.todoist.com/api/v1/tasks" \
  -H "Authorization: Bearer $TODOIST_PERSONAL_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"content\":\"$CONTENT\",\"project_id\":\"$PROJECT_ID\"}"
