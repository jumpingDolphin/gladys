# Google Contacts Integration

Manage Telegram IDs and other metadata via Google Contacts API.

## Features

- **Store Telegram IDs** in Google Contacts (custom field: `telegramId`)
- **Query contacts** by name, email, or Telegram ID
- **Group registry** via special contact "Gladys Groups"
- **Backup** — data lives in Google Contacts, synced across devices

## Setup

1. OAuth credentials already configured via `google:manual` auth profile
2. People API scope: `https://www.googleapis.com/auth/contacts`

## Usage

### Add/Update Telegram ID

```bash
node add-telegram-id.js --name "Agnes" --telegram-id "2072813705"
node add-telegram-id.js --email "hi@simonschenker.com" --telegram-id "7273735518"
```

### Query Contact

```bash
# By name
node query-contact.js --name "Agnes"

# By Telegram ID
node query-contact.js --telegram-id "2072813705"

# List all contacts with Telegram IDs
node list-contacts.js
```

### Manage Groups

Groups are stored as structured JSON in a special contact's notes field.

```bash
# Add group
node add-group.js --name "Patates" --id "-5285631663"

# List groups
node list-groups.js
```

## API Scripts

All scripts in this skill directory use Google People API v1:
- Endpoint: `https://people.googleapis.com/v1/people`
- Auth: OAuth2 via `google_token.json`

## Data Schema

### Contact with Telegram ID

```json
{
  "names": [{ "displayName": "Agnes" }],
  "userDefined": [
    {
      "key": "Telegram ID",
      "value": "2072813705"
    }
  ]
}
```

### Groups Registry Contact

Name: "Gladys Groups"  
Notes:
```json
{
  "groups": {
    "patates": { "id": "-5285631663", "name": "Patates" },
    "transcriber": { "id": "-5134142498", "name": "Transcriber" }
  }
}
```
