#!/bin/bash
# Gladys automated backup script
# Creates encrypted tar of openclaw/ and uploads to Google Drive

set -e

WORKSPACE_DIR="/home/simon/gladys/openclaw/workspace"
GLADYS_DIR="/home/simon/gladys"
BACKUP_DIR="/home/simon/gladys-backups"
DRIVE_FOLDER_ID="1XZbJ7ilG4WRzDji4No0a884-KjGqcm7k"
TIMESTAMP=$(date +%Y%m%d-%H%M)
BACKUP_FILE="$BACKUP_DIR/gladys-backup-$TIMESTAMP.tar.gz.enc"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Require BACKUP_PASSPHRASE env var (set in openclaw/.env)
if [ -z "$BACKUP_PASSPHRASE" ]; then
    echo "Error: BACKUP_PASSPHRASE not set. Add it to openclaw/.env" >&2
    exit 1
fi
BACKUP_PASS="$BACKUP_PASSPHRASE"

# Create encrypted backup
echo "Creating backup: $BACKUP_FILE"
cd "$GLADYS_DIR" && tar -czf - openclaw/ | openssl enc -aes-256-cbc -salt -pbkdf2 -pass pass:"$BACKUP_PASS" -out "$BACKUP_FILE"

# Upload to Google Drive
echo "Uploading to Google Drive..."
cd "$WORKSPACE_DIR/skills/google-drive/scripts"
python3 upload_file.py "$BACKUP_FILE" --folder "$DRIVE_FOLDER_ID"

# Clean up local backup after successful upload
if [ $? -eq 0 ]; then
    echo "Upload successful, removing local backup"
    rm "$BACKUP_FILE"
    echo "Backup complete: gladys-backup-$TIMESTAMP.tar.gz.enc"
else
    echo "Upload failed, keeping local backup: $BACKUP_FILE"
    exit 1
fi
