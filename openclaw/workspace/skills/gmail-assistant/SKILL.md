---
name: gmail-assistant
description: Manage Gmail inbox, read emails, send emails with contact validation, and access Google Contacts. Use when the user asks to check emails, read messages, send emails, search inbox, or manage contacts. Includes security guardrails that restrict sending emails to contacts only.
---

# Gmail Assistant

Personal Gmail management with built-in security guardrails.

## Security Guardrails

**CRITICAL: Email sending is restricted to contacts only.**

- Emails can ONLY be sent to addresses in Google Contacts
- All recipients (to, cc, bcc) are validated before sending
- Unknown recipients trigger an error and prevent sending
- This is enforced in `send_email.py` automatically

**Human approval required:** Always ask Simon for approval before sending ANY email, even if the recipient is in contacts. Show him the draft (to, subject, body) and wait for confirmation.

## Setup

All scripts use OAuth credentials stored in workspace:
- `google_credentials.json` - OAuth client config
- `google_token.json` - Access/refresh tokens

Scripts automatically refresh tokens when expired.

## Available Operations

### 1. List/Search Emails

```bash
cd gmail-assistant/scripts

# List unread emails
python3 list_emails.py --unread-only

# Search for emails from specific sender
python3 list_emails.py --query "from:alice@example.com"

# Search by subject
python3 list_emails.py --query "subject:invoice"

# Combine filters
python3 list_emails.py --query "from:bob@example.com is:unread"

# Get more results
python3 list_emails.py --max-results 50

# JSON output for parsing
python3 list_emails.py --unread-only --format json
```

**Gmail query syntax:** Supports all standard Gmail operators (`from:`, `to:`, `subject:`, `is:unread`, `is:starred`, `has:attachment`, `after:2026/01/01`, etc.)

### 2. Read Email

```bash
cd gmail-assistant/scripts

# Read message by ID
python3 read_email.py MESSAGE_ID

# Read and mark as read
python3 read_email.py MESSAGE_ID --mark-read

# JSON output
python3 read_email.py MESSAGE_ID --format json
```

**Get message IDs** from `list_emails.py` output.

### 3. Send Email

```bash
cd gmail-assistant/scripts

# Send to single recipient
python3 send_email.py \
  --to "alice@example.com" \
  --subject "Meeting Tomorrow" \
  --body "Hi Alice, confirming our meeting at 3pm."

# Send with CC/BCC
python3 send_email.py \
  --to "alice@example.com" \
  --cc "bob@example.com" \
  --bcc "archive@example.com" \
  --subject "Team Update" \
  --body "Weekly update..."

# Send with body from file
python3 send_email.py \
  --to "alice@example.com" \
  --subject "Report" \
  --body-file /tmp/report.txt

# Send with attachment (single file)
python3 send_email.py \
  --to "alice@example.com" \
  --subject "Document" \
  --body "See attached" \
  --attach /path/to/file.pdf

# Send with multiple attachments
python3 send_email.py \
  --to "alice@example.com" \
  --subject "Files" \
  --body "" \
  --attach file1.pdf \
  --attach file2.docx

# Send to Kindle (attachment-only)
python3 send_email.py \
  --to "simonschenker_aRRbAv@kindle.com" \
  --subject "Book" \
  --body "" \
  --attach /path/to/book.epub

# Preview before sending (dry run)
python3 send_email.py \
  --to "alice@example.com" \
  --subject "Test" \
  --body "Testing" \
  --dry-run
```

**Security validation:**
- Script automatically loads contacts and validates all recipients
- If ANY recipient is not in contacts, email is blocked
- Use `--dry-run` to preview without sending

**Attachments:**
- Supports any file type (PDF, EPUB, MOBI, DOCX, images, etc.)
- Multiple attachments: use `--attach` multiple times
- Body can be empty for attachment-only emails (use `--body ""`)

### 4. Manage Contacts

```bash
cd gmail-assistant/scripts

# List all contacts
python3 get_contacts.py

# Search for contact
python3 get_contacts.py --search "Alice"

# JSON output
python3 get_contacts.py --format json
```

## Workflow Patterns

### Check Inbox for Important Emails

```bash
cd gmail-assistant/scripts

# List unread emails
python3 list_emails.py --unread-only --max-results 20

# Read specific email
python3 read_email.py MESSAGE_ID

# Mark as read after handling
python3 read_email.py MESSAGE_ID --mark-read
```

### Search for Specific Email

```bash
cd gmail-assistant/scripts

# Find by sender and subject
python3 list_emails.py --query "from:alice@example.com subject:invoice"

# Get the message ID from results, then read
python3 read_email.py MESSAGE_ID
```

### Send Email Safely

1. **Check recipient is in contacts:**
   ```bash
   python3 get_contacts.py --search "Alice"
   ```

2. **Draft the email** (compose to, subject, body)

3. **ASK SIMON FOR APPROVAL** - Show him the draft

4. **Send after approval:**
   ```bash
   python3 send_email.py --to "alice@example.com" --subject "..." --body "..."
   ```

### Validate Before Sending to Multiple Recipients

The script validates ALL recipients automatically, but you can pre-check:

```bash
# Check contacts exist
python3 get_contacts.py --search "Alice"
python3 get_contacts.py --search "Bob"

# Send (script validates again)
python3 send_email.py --to "alice@example.com,bob@example.com" --subject "..." --body "..."
```

## Common Tasks

### Monitor Inbox (Heartbeat/Periodic)

```bash
cd gmail-assistant/scripts

# Check for unread emails
python3 list_emails.py --unread-only --max-results 10

# If important emails found, alert Simon with:
# - Count of unread
# - Sender + subject of important ones
```

### Reply to Email

1. Read the original email to get details
2. Extract sender email and subject
3. Draft reply body
4. **Ask Simon for approval** with full draft
5. Send with `send_email.py` after approval

### Forward Email

Not directly supported. Workaround:
1. Read original email with `read_email.py`
2. Compose new email with original content quoted
3. Send to new recipient with `send_email.py`

### Send File to Kindle

**Quick workflow for forwarding files to Kindle without reading them:**

1. User sends file via Telegram/WhatsApp
2. Download file to temporary location
3. Forward to Kindle address:
   ```bash
   python3 send_email.py \
     --to "simonschenker_aRRbAv@kindle.com" \
     --subject "$(basename FILE)" \
     --body "" \
     --attach FILE
   ```

**Supported Kindle formats:** EPUB, MOBI, PDF, DOCX, TXT, HTML, RTF, JPEG, PNG, GIF, BMP

**Privacy:** File is treated as binary data and not analyzed/read by the agent.

## Error Handling

### "Recipients not in contacts"

```
❌ SECURITY GUARDRAIL TRIGGERED
The following recipients are NOT in your contacts:
  - unknown@example.com
```

**Solution:** Add the contact to Google Contacts first, or ask Simon if this is truly intended.

### Token Expired

Scripts automatically refresh tokens. If refresh fails:
1. Check `google_token.json` has valid `refresh_token`
2. Re-authenticate if needed (requires manual OAuth flow)

### API Rate Limits

Gmail API free tier limits:
- 1 billion quota units/day
- Most operations cost 5-25 units

If rate limited, wait or reduce frequency of checks.

## Script Dependencies

All scripts require packages listed in `/home/simon/gladys/requirements.txt`. These are installed in the project virtualenv at `/home/simon/gladys/.venv/` via `uv`. The gateway automatically uses the venv's `python3` via `tools.exec.pathPrepend` in `openclaw.json`.

To update dependencies after changing `requirements.txt`:
```bash
uv pip install --python /home/simon/gladys/.venv/bin/python -r /home/simon/gladys/requirements.txt
```

## Notes

- **Account:** This skill manages Gladys's personal Gmail account (not Simon's)
- **Contacts:** Contact list is from Gladys's Google Contacts
- **Storage:** All OAuth tokens stored in workspace root
- **Security:** Send guardrails cannot be disabled (--force exists but should never be used)
