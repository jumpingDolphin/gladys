# Email & Google Integration

> **Status:** Gmail, Drive, and Docs are now working via OAuth (Feb 2026). The `gog` skill is installed and configured.

## 1. Account

- `simons.gladys.bot@gmail.com` — dedicated Gladys Google account
- Isolates agent activity from personal files and email

## 2. Google Cloud Project Setup

1. Create GCP project (e.g., "Gladys")
2. Enable APIs:
   - Gmail API
   - Google Drive API
   - Google Docs API
3. Configure OAuth consent screen (External, publish to production)
4. Create OAuth 2.0 client ID (Desktop app type)
5. Download credentials JSON

### Required OAuth scopes

| Scope | Purpose |
|-------|---------|
| `gmail.readonly` | Read email messages |
| `gmail.modify` | Modify messages (labels, read status) |
| `gmail.compose` | Draft emails |
| `gmail.send` | Send emails |
| `drive.file` | Access only files created by or shared with the app |
| `documents` | Google Docs read/write |

## 3. Email in OpenClaw — Two Uses

### As a skill (agent sends/reads email on demand)

- **Option A: secure-gmail skill** — uses Gmail API via OAuth directly
- **Option B: gog skill** (Google Workspace) — `clawdhub install gog`, covers Gmail + Drive + Docs in one skill

### As a channel (bidirectional email chat)

- Community email channel plugin, or Gmail Pub/Sub for real-time push notifications
- Whitelist allowed senders for security

## 4. Google Docs & Drive in OpenClaw

- Same OAuth credentials, same GCP project
- Share target Docs/Drive folders with `simons.gladys.bot@gmail.com`
- The **gog skill** covers this too (Gmail + Drive + Docs unified)

## 5. Credentials

OAuth credentials managed as files (not env vars):
- `openclaw/workspace/google_credentials.json` — OAuth client ID + secret
- `openclaw/workspace/google_token.json` — access token + refresh token (auto-refreshed)

## 6. Recommendation

- ~~Use the **gog skill** for unified Gmail + Drive + Docs access through one OAuth flow~~ **Done** — gog skill installed and working.
- Add email as a channel later if bidirectional email chat is wanted
