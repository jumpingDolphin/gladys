---
name: google-drive
description: Manage Google Drive files and folders. List, search, upload, download files, and create folders. Use when the user needs to work with files in Google Drive.
---

# Google Drive Manager

Manage files and folders in Google Drive via API.

## Setup

Uses OAuth credentials from workspace:
- `google_credentials.json` - OAuth client config
- `google_token.json` - Access/refresh tokens

Scripts automatically refresh tokens when expired.

## Available Operations

### 1. List and Search Files

```bash
cd google-drive/scripts

# List recent files
python3 list_files.py --max 20

# Search by name
python3 list_files.py --query "name contains 'report'"

# Search by type (Google Docs)
python3 list_files.py --query "mimeType='application/vnd.google-apps.document'"

# List files in specific folder
python3 list_files.py --folder FOLDER_ID

# JSON output
python3 list_files.py --format json
```

**Drive query syntax:**
- `name contains 'text'` - Search by name
- `mimeType='type'` - Filter by MIME type
- `'folder_id' in parents` - Files in specific folder
- `modifiedTime > '2026-01-01T00:00:00'` - Modified after date
- Combine with `and` / `or`

**Common MIME types:**
- Google Docs: `application/vnd.google-apps.document`
- Google Sheets: `application/vnd.google-apps.spreadsheet`
- Google Slides: `application/vnd.google-apps.presentation`
- Folders: `application/vnd.google-apps.folder`
- PDFs: `application/pdf`

### 2. Upload Files

```bash
cd google-drive/scripts

# Upload file
python3 upload_file.py /path/to/file.pdf

# Upload with custom name
python3 upload_file.py /path/to/file.pdf --name "Report 2026.pdf"

# Upload to specific folder
python3 upload_file.py /path/to/file.pdf --folder FOLDER_ID

# Upload with description
python3 upload_file.py /path/to/file.pdf --description "Monthly report"
```

### 3. Download Files

```bash
cd google-drive/scripts

# Download by file ID
python3 download_file.py FILE_ID

# Download to specific path
python3 download_file.py FILE_ID --output /tmp/downloaded.pdf
```

**Google Workspace files (Docs, Sheets, Slides):**
- Automatically exported to appropriate format:
  - Docs → PDF
  - Sheets → XLSX
  - Slides → PDF

### 4. Create Folders

```bash
cd google-drive/scripts

# Create folder in root
python3 create_folder.py "Project Files"

# Create subfolder
python3 create_folder.py "Subfolder" --parent PARENT_FOLDER_ID
```

## Workflow Patterns

### Find and Download File

```bash
cd google-drive/scripts

# Search for file
python3 list_files.py --query "name contains 'report'"

# Copy file ID from results, then download
python3 download_file.py FILE_ID --output /tmp/report.pdf
```

### Upload and Organize

```bash
cd google-drive/scripts

# Create folder
python3 create_folder.py "2026 Reports"
# Note the folder ID from output

# Upload file to that folder
python3 upload_file.py /path/to/report.pdf --folder FOLDER_ID
```

### Search by Date

```bash
cd google-drive/scripts

# Files modified in last 7 days
python3 list_files.py --query "modifiedTime > '2026-02-04T00:00:00'"

# Files created this month
python3 list_files.py --query "createdTime > '2026-02-01T00:00:00'"
```

## Common Tasks

### Backup File from Drive

```bash
cd google-drive/scripts

# List files
python3 list_files.py --query "name contains 'important'"

# Download file
python3 download_file.py FILE_ID --output ~/backups/important_file.pdf
```

### Upload Multiple Files to Folder

```bash
cd google-drive/scripts

# Create destination folder
python3 create_folder.py "Batch Upload"
FOLDER_ID="..." # from output

# Upload each file
for file in /path/to/files/*; do
    python3 upload_file.py "$file" --folder $FOLDER_ID
done
```

## Script Dependencies

All scripts require:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Notes

- **Account:** Gladys's personal Google Drive (not Simon's)
- **Permissions:** Read/write access to all Drive files
- **Storage:** Free tier = 15GB shared across Drive, Gmail, Photos
- **Rate limits:** 12,000 requests/minute (more than enough)
