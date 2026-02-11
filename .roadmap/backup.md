# Backup & Restore

> Strategy for backing up Gladys/OpenClaw state beyond what git tracks.
> Companion to [`roadmap.md`](../roadmap.md).

## What's where

| Data | Backed up by | Location |
|------|-------------|----------|
| Agent definition (IDENTITY, SOUL, skills, scripts) | **Git** | `openclaw/workspace/*.md`, `skills/*/` |
| Project files (roadmap, scripts, CLAUDE.md) | **Git** | repo root |
| Secrets (.env, auth-profiles, OAuth tokens) | **Google Drive** | `openclaw/.env`, `openclaw/agents/*/agent/auth-profiles.json`, `openclaw/workspace/google_*.json` |
| Runtime state (sessions, memory, media) | **Google Drive** | `openclaw/agents/*/sessions/`, `openclaw/workspace/memory/`, `openclaw/media/` |
| SQLite databases | **Google Drive** | `openclaw/**/*.sqlite` |
| OpenClaw config | **Google Drive** | `openclaw/openclaw.json` |

## Google Drive backup

- **Account:** `simons.gladys.bot@gmail.com`
- **Quota:** 15 GB free (current usage: ~46 MB for all of `openclaw/`)
- **Strategy:** Differential — only upload changed files since last backup
- **Target folder:** `gladys-backups/` on Drive

### What to back up

Everything in `openclaw/` that git does NOT track:

```
openclaw/.env                          # secrets
openclaw/openclaw.json                 # config (has ${VAR} refs, not secrets)
openclaw/agents/*/agent/auth-profiles.json  # model API keys
openclaw/agents/*/sessions/            # conversation history
openclaw/workspace/google_*.json       # OAuth credentials
openclaw/workspace/memory/             # daily agent memory
openclaw/workspace/out/                # generated media
openclaw/workspace/skills/*/config.env # skill secrets
openclaw/media/                        # Telegram media (largest: ~27 MB)
openclaw/identity/                     # device keys
openclaw/devices/                      # pairing state
openclaw/**/*.sqlite                   # vector indexes
```

### Implementation plan

- [ ] Create `scripts/backup.sh` — uses Google Drive API (via Node.js, since no pip) to:
  1. List files modified since last backup timestamp
  2. Upload changed files to `gladys-backups/YYYY-MM-DD/` folder on Drive
  3. Record timestamp for next differential run
- [ ] Add cron job or systemd timer for daily backup (e.g. 03:00 UTC)
- [ ] Add `openclaw` heartbeat task to report backup status in daily brief
- [ ] Test restore procedure: download from Drive → place in `openclaw/`

### Restore procedure (manual for now)

1. Clone the git repo (gets agent definition + project files)
2. Download latest backup folder from Google Drive
3. Place files back into `openclaw/` preserving directory structure
4. `chmod 600 openclaw/.env openclaw/agents/*/agent/auth-profiles.json`
5. `chmod 700 openclaw/ openclaw/identity/`
6. `openclaw doctor --repair`
7. `systemctl --user restart openclaw-gateway`

## Growth estimate

| Data | Growth rate | Notes |
|------|-----------|-------|
| Sessions | ~1-5 MB/day | Depends on usage |
| Media | Variable | Telegram images/files |
| Memory | ~1 KB/day | Daily markdown files |
| SQLite | Slow | Vector index grows with memory |

At current rates, 15 GB should last well over a year. Monitor quarterly.
