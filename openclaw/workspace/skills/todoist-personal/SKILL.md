# Todoist Personal Skill

Manage Simon's personal Todoist tasks.

## Purpose

Simple wrapper scripts for Simon's personal Todoist account using the correct REST API v1 endpoints.

## Configuration

Token: `${TODOIST_PERSONAL_TOKEN}` from `openclaw/.env`

**Projects:**
- Inbox: `6fxjfC8p5mX2mWGW`
- Shopping: `6fxm5M23qmp9VVHQ`
- Entertainment: `6fxm5M4RMGHXH9mR`
- Family & Friends: `6fxm5M82CPxc3xJW`
- Tech & Work: `6fxm5M9JxM9FHxfP`
- Tasks: `6fxm5MHv6f32X9gx`

## Scripts

### `scripts/add_task.sh`
Add a task to a project.
```bash
./add_task.sh "Task content" [project_id]
# Default project: Inbox
```

### `scripts/list_tasks.sh`
List tasks from a project.
```bash
./list_tasks.sh [project_id]
# Default: Inbox
```

### `scripts/list_projects.sh`
List all projects.
```bash
./list_projects.sh
```

## Examples

```bash
# Add to inbox
./add_task.sh "Call the doctor"

# Add to shopping list
./add_task.sh "Vis Torx T4 #amazon" 6fxm5M23qmp9VVHQ

# List inbox tasks
./list_tasks.sh

# List all projects
./list_projects.sh
```

## API Reference

- **Endpoint:** `https://api.todoist.com/api/v1/`
- **Auth:** `Authorization: Bearer ${TODOIST_PERSONAL_TOKEN}`
- **Format:** JSON
