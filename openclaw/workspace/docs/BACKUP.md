# Backup Documentation

## Current Setup (tar + Google Drive)

**Schedule:** Every 2 days (48 hours)  
**Method:** Full encrypted tar backup  
**Storage:** Google Drive (folder ID: `1XZbJ7ilG4WRzDji4No0a884-KjGqcm7k`)  
**Size:** ~32MB per backup  

### Files

- **Script:** `/home/simon/gladys/openclaw/workspace/scripts/backup.sh`
- **Passphrase:** `BACKUP_PASSPHRASE` in `openclaw/.env`
- **Cron job:** Automated via OpenClaw cron (ID: `031f4ec4-183a-4e84-9f0b-3f1db8e9c9f4`)

### How It Works

1. Creates encrypted tar: `openclaw/` → `gladys-backup-YYYYMMDD-HHMM.tar.gz.enc`
2. Encryption: AES-256-CBC via openssl, salted, pbkdf2
3. Uploads to Google Drive
4. Deletes local copy after successful upload
5. Google Drive keeps version history automatically

### Restore

```bash
# 1. Download backup from Google Drive
# 2. Decrypt and extract:
openssl enc -aes-256-cbc -d -pbkdf2 -in gladys-backup-*.tar.gz.enc -out restored.tar.gz
# Enter passphrase (BACKUP_PASSPHRASE from openclaw/.env)
tar -xzf restored.tar.gz
```

### Passphrase

Stored as `BACKUP_PASSPHRASE` in `openclaw/.env`. Same passphrase for all backups.

⚠️ **Keep this safe!** Without it, backups are unrecoverable. Do not commit to git.

---

## Future: Restic (not implemented)

**Why consider restic:**
- Deduplication: only backs up changed data
- Snapshot-based: each backup is a full snapshot, stored as deltas
- Space-efficient: 32MB today, maybe 2MB tomorrow
- Built-in encryption
- Works with rclone → Google Drive

**When to migrate:**
- Workspace grows beyond 100MB
- Want daily or hourly backups
- Need more granular restore points

**Setup steps (for future reference):**
1. Install restic + rclone
2. Configure rclone for Google Drive
3. Initialize restic repo: `restic -r rclone:gdrive:gladys-backups init`
4. Replace backup.sh with restic commands
5. Set retention policy (daily/weekly/monthly snapshots)

**Current decision:** Stick with tar — simple, reliable, adequate for 32MB every 2 days.
