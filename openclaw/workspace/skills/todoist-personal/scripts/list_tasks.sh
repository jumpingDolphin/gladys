#!/bin/bash
# List tasks from personal Todoist
# Usage: ./list_tasks.sh [project_id]

PROJECT_ID="${1:-6fxjfC8p5mX2mWGW}"  # Default: Inbox

# Load token from .env
ENV_FILE="$HOME/gladys/openclaw/.env"
if [ -f "$ENV_FILE" ]; then
  source "$ENV_FILE"
fi

curl -s "https://api.todoist.com/api/v1/tasks?project_id=$PROJECT_ID" \
  -H "Authorization: Bearer $TODOIST_PERSONAL_TOKEN"
