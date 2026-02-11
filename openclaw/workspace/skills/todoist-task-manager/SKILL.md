# Todoist Task Manager Skill

Track Gladys's progress on complex tasks using Todoist as a visibility layer.

## Purpose

When running multi-step tasks, this skill lets me:
- Create tasks in Todoist with my plan in the description
- Log progress as comments in real-time
- Move tasks between sections (In Progress → Waiting → Done)
- Give you visibility without scrolling through chat logs

## Configuration

All config is in `config.env`:
- **Project:** Gladys workspace (ID: 2367060736)
- **Sections:**
  - 🟡 In Progress (215068135)
  - 🟠 Waiting (215068138)
  - 🟢 Done (215068145)

## Scripts

### `scripts/todoist_api.sh`
Core API wrapper. Usage:
```bash
./todoist_api.sh <endpoint> <method> [data_json]
```

### `scripts/sync_task.sh`
Create or update tasks. Usage:
```bash
./sync_task.sh <content> <status> [task_id] [description] [labels]
```
Status: "In Progress" | "Waiting" | "Done"

### `scripts/add_comment.sh`
Add progress logs. Usage:
```bash
./add_comment.sh <task_id> <comment_text>
```

## Usage Pattern

For complex tasks:
1. Create task with plan: `sync_task.sh "Build X" "In Progress" "" "Plan: Step 1...\nStep 2..."`
2. Log progress: `add_comment.sh <task_id> "✅ Step 1 complete"`
3. Mark done: `sync_task.sh "Build X" "Done" <task_id>`

## Security

Token stored in `config.env`. Keep it private.
