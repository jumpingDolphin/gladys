---
name: backup-restore
description: Create encrypted backups of Gladys workspace and upload to Google Drive, or restore from backup. Use when creating manual backups, testing backup/restore, or recovering from backup archives.
---

# Backup & Restore

Automated encrypted backups of the entire Gladys system (`/home/simon/gladys/openclaw/`) to Google Drive.

## Quick Start

**Create backup:**
```bash
/home/simon/gladys/openclaw/workspace/skills/backup-restore/scripts/backup.sh
```

**Restore from backup:**
```bash
/home/simon/gladys/openclaw/workspace/skills/backup-restore/scripts/restore.sh <backup-file.tar.gz.enc>
```

## Backup Process

The backup script:
1. Creates encrypted tar archive of `/home/simon/gladys/openclaw/`
2. Uploads to Google Drive (folder ID: `1XZbJ7ilG4WRzDji4No0a884-KjGqcm7k`)
3. Removes local copy after successful upload
4. Uses AES-256-CBC encryption with passphrase from `.env`

**Encryption:** Requires `BACKUP_PASSPHRASE` in `/home/simon/gladys/openclaw/.env` (automatically sourced by script).

**Output:** Drive link and file ID printed on completion.

## Restore Process

The restore script:
1. Decrypts the backup archive using `BACKUP_PASSPHRASE`
2. Extracts to `/home/simon/gladys/openclaw/`
3. Requires confirmation before overwriting

**⚠️ Warning:** Restore overwrites existing files. Always backup current state first.

**Post-restore:** Restart OpenClaw (`openclaw gateway restart`) to load restored config.

## Automation

Automated backups run every 2 days via cron job (ID: `031f4ec4-183a-4e84-9f0b-3f1db8e9c9f4`).

**View schedule:**
```bash
openclaw cron list
```

**Manual trigger:**
```bash
openclaw cron run --job-id 031f4ec4-183a-4e84-9f0b-3f1db8e9c9f4
```

## Resources

### scripts/

- **backup.sh** - Create encrypted backup and upload to Drive
- **restore.sh** - Decrypt and restore from backup archive
