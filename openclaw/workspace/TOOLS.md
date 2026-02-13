# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Contacts & Groups Registry

**Centralized in Google Contacts** (backed up, synced across devices)

### Contacts with Telegram IDs
- **Simon Schenker** (`simonschenker@gmail.com`): 7273735518
- **Agnes** (`agnes.alvesdesouza@gmail.com`): 2072813705
- **Michael** (Michi): 14423006

### Telegram Groups
- **Patates**: -5285631663
- **Transcriber**: -5134142498

**Management:** Use `skills/google-contacts/` scripts
- `list-contacts.js` — show all contacts with Telegram IDs
- `add-telegram-id.js` — add/update Telegram ID for existing contact
- `create-contact.js` — create new contact with Telegram ID
- `manage-groups.js` — add/list groups (stored in special "Gladys Groups" contact)
- `lookup-for-allowlist.js "Name"` — lookup contact for allowlist management (returns JSON)

**Natural language allowlist management:**

When Simon says "add [Name] to allowlist":
1. Run: `node skills/google-contacts/lookup-for-allowlist.js "Name"`
2. Parse JSON response
3. If `found: true` and `hasTelegramId: true`:
   - Show: "Found {name} ({email}, Telegram ID: {telegramId}). Add to which allowlist? (main / transcriber)"
   - Wait for answer
   - If main: use `gateway` tool with `action: config.patch` to add `telegramId` to `channels.telegram.allowFrom`
   - If transcriber: add to `channels.telegram.accounts.transcriber.allowFrom`
   - Restart happens automatically
4. If not found or no Telegram ID:
   - Tell Simon and offer to create contact or add ID

## Communication Preferences

### Agnes (agnes.alvesdesouza@gmail.com)
- **Language:** French
- **Notes:** Simon's partner
- **Telegram ID:** 2072813705

## Google Calendar

**Default workflow when creating events:**
- Always invite `simonschenker@gmail.com` to events
- For family-related events, also invite `agnes.alvesdesouza@gmail.com`
- I have read access to Simon's calendar (simonschenker@gmail.com)
- I own/manage simons.gladys.bot@gmail.com calendar

**Heartbeat checks:** Monitor Simon's calendar for upcoming events

## Gmail & Google Services

**Skills Location:** `skills/gmail-assistant/`, `skills/google-drive/`, `skills/google-docs/`, `skills/google-sheets/`, `skills/google-calendar/`, `skills/google-places/`

**Guardrails:**
- Only send/reply to people in contacts
- Always ask Simon for approval before sending ANY email
- **Contact creation requires Simon's approval** — never add contacts without asking first

**Kindle forwarding:**
- Kindle address: `simonschenker_aRRbAv@kindle.com` (in contacts)
- When Simon sends files via Telegram/WhatsApp: forward directly to Kindle without reading/analyzing
- Supported formats: EPUB, MOBI, PDF, DOCX, TXT, HTML, RTF, images

**OAuth Setup:**
- Project: `gladys-system`
- Credentials: `google_credentials.json` + `google_token.json`
- Scopes: gmail.modify, contacts, drive, docs, calendar, spreadsheets, tasks, photos, cloud-platform (includes Places API)

**Usage:**
- Gmail: List emails, read messages, send with contact validation
- Drive: List/search files, upload/download, create folders
- Docs: Create documents, read content, append text
- Sheets: Create spreadsheets, read/write data, append rows
- Calendar: List events, create/update/delete calendar entries
- Places: Search restaurants, cafes, shops by name or location

## Python & UV Environment

**Package Manager:** UV (modern, fast Python package manager)
- **UV binary:** `/home/simon/.local/bin/uv` (version 0.10.2)
- **Project root:** `/home/simon/gladys/`
- **Config:** `pyproject.toml` + `uv.lock`

**Virtual Environment:**
- **Location:** `/home/simon/gladys/.venv`
- **Python:** 3.12.3
- **PATH:** `.venv/bin` is prepended (via OpenClaw config `tools.exec.pathPrepend`)

**Installed packages (via UV):**
- google-auth
- google-auth-oauthlib
- google-auth-httplib2
- google-api-python-client
- matplotlib

**Commands:**
```bash
# Install/sync dependencies (from pyproject.toml)
cd /home/simon/gladys && uv sync

# Add new package
cd /home/simon/gladys && uv add package-name

# Run python with venv active
python3 script.py  # PATH already includes .venv/bin

# Check UV status
uv --version
python3 -m pip list  # pip still exists for compatibility
```

**Note:** pip is present in the venv (UV doesn't remove it), but UV should be used for package management. Both work, UV is faster.

## Todoist

**API Version:** REST API v1 (correct endpoint fixed 2026-02-13)
- **Base URL:** `https://api.todoist.com/api/v1/`
- **Common endpoints:** `/tasks`, `/projects`, `/labels`, `/comments`, etc.
- **Method:** Standard REST (GET, POST, PUT, DELETE) with JSON body
- **Auth:** `Authorization: Bearer TOKEN` header

**⚠️ Common mistake:** Using `/rest/v2/` or `/sync/v9/` returns "deprecated" message. Always use `/api/v1/`.

**Personal Todoist (Simon's):**
- Token: `${TODOIST_PERSONAL_TOKEN}` (in openclaw/.env)
- Default project: Inbox (ID: `6fxjfC8p5mX2mWGW`)
- Projects:
  - Inbox: `6fxjfC8p5mX2mWGW`
  - Shopping: `6fxm5M23qmp9VVHQ`
  - Entertainment: `6fxm5M4RMGHXH9mR`
  - Family & Friends: `6fxm5M82CPxc3xJW`
  - Tech & Work: `6fxm5M9JxM9FHxfP`
  - Tasks: `6fxm5MHv6f32X9gx`

**Gladys Workspace (Task Tracking):**
- Token: `${TODOIST_WORKSPACE_TOKEN}` (in openclaw/.env)
- Project: Gladys workspace (ID: `6fxjfVH63x9xg5G7`)

**Strategy:**
- Simon's todos → Personal Todoist
- Gladys's task tracking → Gladys Workspace
- Keep them in sync, no duplication

**Example commands:**
```bash
# Add task
curl -X POST "https://api.todoist.com/api/v1/tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Task text","project_id":"PROJECT_ID"}'

# List tasks
curl "https://api.todoist.com/api/v1/tasks?project_id=PROJECT_ID" \
  -H "Authorization: Bearer $TOKEN"

# List projects
curl "https://api.todoist.com/api/v1/projects" \
  -H "Authorization: Bearer $TOKEN"
```

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
