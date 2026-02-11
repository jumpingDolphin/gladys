---
name: google-docs
description: Create, read, and edit Google Docs. Use when the user needs to create documents, read document content, or append text to existing docs.
---

# Google Docs Manager

Create and manage Google Docs via API.

## Setup

Uses OAuth credentials from workspace:
- `google_credentials.json` - OAuth client config
- `google_token.json` - Access/refresh tokens

Scripts automatically refresh tokens when expired.

## Available Operations

### 1. Create Document

```bash
cd google-docs/scripts

# Create blank document
python3 create_doc.py "Meeting Notes"

# Create with initial content
python3 create_doc.py "Report" --content "This is the introduction..."
```

### 2. Read Document

```bash
cd google-docs/scripts

# Read document content
python3 read_doc.py DOC_ID

# JSON output
python3 read_doc.py DOC_ID --format json
```

**Get DOC_ID:** From the URL of the doc: `https://docs.google.com/document/d/DOC_ID/edit`

### 3. Append Text

```bash
cd google-docs/scripts

# Append text
python3 append_text.py DOC_ID "New paragraph text"

# Append from file
python3 append_text.py DOC_ID --file /path/to/text.txt
```

## Workflow Patterns

### Create and Populate Document

```bash
cd google-docs/scripts

# Create document
python3 create_doc.py "Project Summary" --content "# Project Summary\n\n"
# Note the DOC_ID from output

# Add more content
python3 append_text.py DOC_ID "Section 1: Overview\n\nLorem ipsum..."
python3 append_text.py DOC_ID "\n\nSection 2: Details\n\n..."
```

### Read and Process Document

```bash
cd google-docs/scripts

# Read content
python3 read_doc.py DOC_ID > /tmp/content.txt

# Process locally (grep, sed, etc.)
grep "important" /tmp/content.txt
```

### Copy Document Content

```bash
cd google-docs/scripts

# Read source doc
python3 read_doc.py SOURCE_DOC_ID --format json > /tmp/source.json

# Extract text and create new doc
SOURCE_TEXT=$(jq -r '.text' /tmp/source.json)
python3 create_doc.py "Copy of Document" --content "$SOURCE_TEXT"
```

## Common Tasks

### Create Meeting Notes Template

```bash
cd google-docs/scripts

python3 create_doc.py "Team Meeting $(date +%Y-%m-%d)" \
  --content "# Team Meeting - $(date +%Y-%m-%d)\n\n## Attendees\n\n## Agenda\n\n## Notes\n\n## Action Items\n\n"
```

### Append Daily Log Entry

```bash
cd google-docs/scripts

python3 append_text.py LOG_DOC_ID "\n\n## $(date +%Y-%m-%d)\n\n- Task completed\n- Issue resolved\n"
```

### Search and Read Docs

```bash
# First use google-drive skill to find doc
cd ../google-drive/scripts
python3 list_files.py --query "name contains 'report' and mimeType='application/vnd.google-apps.document'"

# Then read with google-docs
cd ../google-docs/scripts
python3 read_doc.py DOC_ID
```

## Limitations

**Current implementation supports:**
- Creating new documents
- Reading full text content
- Appending text to end

**Not yet implemented (can be added if needed):**
- Formatting (bold, italic, etc.)
- Inserting text at specific positions
- Deleting content
- Tables, images, lists
- Comments, suggestions
- Sharing/permissions

For advanced formatting, use the Drive skill to download as DOCX, edit locally, then re-upload.

## Script Dependencies

All scripts require:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Notes

- **Account:** Gladys's personal Google account (not Simon's)
- **Storage:** Docs count against 15GB Drive quota
- **Collaboration:** Documents are private by default; share manually via web UI if needed
- **Rate limits:** 300 requests/minute per user (more than enough)
