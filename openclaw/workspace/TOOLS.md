# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Communication Preferences

### Agnes (agnes.alvesdesouza@gmail.com)
- **Language:** French
- **Notes:** Simon's partner

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

## Todoist

**API Version:** v1 (migrated from deprecated v2 on 2026-02-12)
- **Endpoint:** `https://api.todoist.com/api/v1/sync`
- **Method:** POST with `commands` array
- All IDs changed during migration (old v2 IDs no longer work)

**Personal Todoist (Simon's):**
- Token: `${TODOIST_PERSONAL_TOKEN}` (in openclaw/.env)
- Default project: Inbox (ID: `6fxjfC8p5mX2mWGW`)
- Labels: `#shopping`, `#amazon`, `#groceries`, `#errands`, `#work`, `#personal`
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
- Config: `skills/todoist-task-manager/config.env`

**Strategy:**
- Simon's todos → Personal Todoist
- Gladys's task tracking → Gladys Workspace
- Keep them in sync, no duplication

**Example command (add task):**
```bash
curl -s "https://api.todoist.com/api/v1/sync" \
  -H "Authorization: Bearer $TOKEN" \
  -d 'commands=[{"type":"item_add","temp_id":"'$(uuidgen)'","uuid":"'$(uuidgen)'","args":{"content":"Task text","project_id":"PROJECT_ID"}}]'
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
