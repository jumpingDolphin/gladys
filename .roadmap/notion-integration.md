# Notion Integration

## 1. Accounts & Workspace

- Create a **team workspace** in Notion (e.g., "Gladys")
- Add both Simon (personal account) and Gladys (`simons.gladys.bot@gmail.com`) as members
- Simon manages the workspace; Gladys has member-level access for reading/writing

## 2. Internal Integration Setup

1. Go to <https://www.notion.so/my-integrations> (logged in as the workspace owner)
2. Create a new **internal integration** within the Gladys team workspace
3. Name it `gladys-bot` (or similar)
4. Capabilities needed:
   - Read content
   - Update content
   - Insert content
5. Copy the API token (starts with `ntn_`)

> Internal integrations are scoped to one workspace and don't require OAuth — just a token.

## 3. Database Structure

Create these databases in the workspace and **share each one with the `gladys-bot` integration** (Share > Invite > select the integration):

| Database | Purpose | Key Properties |
|----------|---------|----------------|
| **Tasks** | Action items Claude creates/tracks | Title, Status (To Do / In Progress / Done), Priority, Due Date, Project (relation) |
| **Projects** | Group related tasks | Title, Status, Description |

> Start minimal. Additional databases (e.g., Reminders, Notes) can be added later without changing the integration setup.

## 4. OpenClaw Config

Install the Notion skill:

```bash
clawdhub install notion
```

The skill reads `NOTION_API_TOKEN` from the environment. No additional config in `openclaw.json` is needed beyond ensuring the env var is set.

Usage examples the agent handles automatically:
- "Create a task: buy groceries" &rarr; new row in Tasks database
- "What's on my task list?" &rarr; query Tasks database, return results
- "Mark 'buy groceries' as done" &rarr; update Status property

## 5. Env Vars

```
NOTION_API_TOKEN=ntn_...
```

## 6. Recommendation

- Use a **single team workspace** with an **internal integration** — simplest setup, no OAuth flow needed
- Start with two databases (Tasks, Projects); expand only when a real need appears
- Share databases explicitly with the integration — Notion internal integrations have no access until invited
