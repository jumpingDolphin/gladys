#!/bin/bash
# Gladys restore script
# Restores from encrypted backup archive

set -e

WORKSPACE_DIR="/home/simon/gladys/openclaw/workspace"
GLADYS_DIR="/home/simon/gladys"

# Display usage
usage() {
    echo "Usage: $0 <backup-file.tar.gz.enc>"
    echo "  Decrypts and extracts backup to /home/simon/gladys/"
    echo "  Requires BACKUP_PASSPHRASE in environment or openclaw/.env"
    exit 1
}

# Check arguments
if [ $# -ne 1 ]; then
    usage
fi

BACKUP_FILE="$1"

# Verify backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE" >&2
    exit 1
fi

# Source .env if BACKUP_PASSPHRASE not already set
if [ -z "$BACKUP_PASSPHRASE" ]; then
    ENV_FILE="/home/simon/gladys/openclaw/.env"
    if [ -f "$ENV_FILE" ]; then
        export $(grep -v '^#' "$ENV_FILE" | grep BACKUP_PASSPHRASE | xargs)
    fi
fi

# Require BACKUP_PASSPHRASE
if [ -z "$BACKUP_PASSPHRASE" ]; then
    echo "Error: BACKUP_PASSPHRASE not set. Add it to openclaw/.env or set in environment" >&2
    exit 1
fi

BACKUP_PASS="$BACKUP_PASSPHRASE"

# Warning
echo "⚠️  WARNING: This will overwrite files in /home/simon/gladys/openclaw/"
echo "   Backup file: $BACKUP_FILE"
echo ""
read -p "Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

# Decrypt and extract
echo "Decrypting and extracting backup..."
cd "$GLADYS_DIR"
openssl enc -d -aes-256-cbc -pbkdf2 -pass pass:"$BACKUP_PASS" -in "$BACKUP_FILE" | tar -xzf -

echo "✅ Restore complete"
echo "   Extracted to: $GLADYS_DIR/openclaw/"
echo ""
echo "Next steps:"
echo "  1. Verify files: ls -la $GLADYS_DIR/openclaw/"
echo "  2. Restart OpenClaw: openclaw gateway restart"
