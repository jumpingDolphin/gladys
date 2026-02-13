#!/bin/bash
# List all projects from personal Todoist
# Usage: ./list_projects.sh

# Load token from .env
ENV_FILE="$HOME/gladys/openclaw/.env"
if [ -f "$ENV_FILE" ]; then
  source "$ENV_FILE"
fi

curl -s "https://api.todoist.com/api/v1/projects" \
  -H "Authorization: Bearer $TODOIST_PERSONAL_TOKEN"
