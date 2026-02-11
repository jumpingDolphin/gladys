# Gmail Assistant Setup

## Python Dependencies

The skill requires Google API client libraries. Install with:

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

Or if pip is not available:
```bash
apt-get install python3-pip  # On Debian/Ubuntu
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Verify Installation

```bash
python3 -c "from google.oauth2.credentials import Credentials; print('✓ Google libraries installed')"
```

## OAuth Credentials

Already set up in workspace:
- `google_credentials.json` - OAuth client config (from Google Cloud Console)
- `google_token.json` - Access/refresh tokens (auto-refreshed)

### Scopes Enabled

The token includes these scopes:
- `gmail.modify` - Read, send, and modify emails
- `contacts` - Access Google Contacts (People API)
- `drive`, `documents`, `calendar`, `spreadsheets`, `tasks`, `photoslibrary.readonly` - Other Google services

## Testing the Setup

```bash
cd gmail-assistant/scripts

# Test contacts access
python3 get_contacts.py

# Test Gmail access
python3 list_emails.py --max-results 5

# If successful, you should see your contacts/emails
```

## Troubleshooting

### "No module named google"
Install dependencies (see above).

### "Token expired" / "Refresh token invalid"
Re-authenticate with Google OAuth flow:
1. Visit Google Cloud Console
2. Generate new credentials
3. Run OAuth flow to get new token
4. Save to `google_token.json`

### "403 Forbidden" / "Insufficient Permission"
Check that required scopes are enabled in `google_token.json`.

### Rate Limits
Gmail API quotas:
- 1 billion quota units/day (free tier)
- Sending: 100 messages/day (free tier)
- If exceeded, wait 24h or request quota increase
