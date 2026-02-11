---
name: google-calendar
description: Manage Google Calendar events. List, create, update, and delete calendar events. Use when the user needs to check schedule, add events, or manage their calendar.
---

# Google Calendar Manager

Manage calendar events via Google Calendar API.

## Setup

Uses OAuth credentials from workspace:
- `google_credentials.json` - OAuth client config
- `google_token.json` - Access/refresh tokens

Scripts automatically refresh tokens when expired.

## Available Operations

### 1. List Events

```bash
cd google-calendar/scripts

# List next 10 events
python3 list_events.py --max 10

# Events in next 7 days
python3 list_events.py --days-ahead 7

# Search for events
python3 list_events.py --query "meeting"

# Specific calendar
python3 list_events.py --calendar "work@example.com"

# JSON output
python3 list_events.py --format json
```

### 2. Create Event

```bash
cd google-calendar/scripts

# Timed event
python3 create_event.py \
  --summary "Team Meeting" \
  --start "2026-02-15T14:00:00" \
  --end "2026-02-15T15:00:00" \
  --description "Weekly sync" \
  --location "Zoom"

# All-day event
python3 create_event.py \
  --summary "Conference" \
  --date "2026-03-10"

# Multi-day event
python3 create_event.py \
  --summary "Vacation" \
  --date "2026-04-01" \
  --date-end "2026-04-08"

# Quick event (1 hour from now)
python3 create_event.py \
  --summary "Quick sync" \
  --duration 60
```

**Datetime format:** ISO 8601 (e.g., `2026-02-15T14:00:00`)  
**Date format:** YYYY-MM-DD (e.g., `2026-02-15`)

### 3. Update Event

```bash
cd google-calendar/scripts

# Change title
python3 update_event.py EVENT_ID --summary "New Title"

# Reschedule
python3 update_event.py EVENT_ID \
  --start "2026-02-16T10:00:00" \
  --end "2026-02-16T11:00:00"

# Update location
python3 update_event.py EVENT_ID --location "Conference Room B"

# Update multiple fields
python3 update_event.py EVENT_ID \
  --summary "Updated Meeting" \
  --location "Online" \
  --description "New details"
```

**Get EVENT_ID:** From `list_events.py` output

### 4. Delete Event

```bash
cd google-calendar/scripts

# Delete event
python3 delete_event.py EVENT_ID
```

## Workflow Patterns

### Check Today's Schedule

```bash
cd google-calendar/scripts

# Today's events
python3 list_events.py --days-ahead 1
```

### Schedule Meeting

```bash
cd google-calendar/scripts

# Create meeting
python3 create_event.py \
  --summary "Client Call" \
  --start "2026-02-12T15:00:00" \
  --end "2026-02-12T16:00:00" \
  --location "Phone" \
  --description "Discuss Q1 results"
```

### Find and Reschedule Event

```bash
cd google-calendar/scripts

# Find event
python3 list_events.py --query "standup"
# Note EVENT_ID from output

# Reschedule
python3 update_event.py EVENT_ID \
  --start "2026-02-13T09:00:00" \
  --end "2026-02-13T09:30:00"
```

### Weekly Schedule Check

```bash
cd google-calendar/scripts

# Next 7 days
python3 list_events.py --days-ahead 7 --max 50
```

## Common Tasks

### Add Reminder for Tomorrow

```bash
cd google-calendar/scripts

# Tomorrow at 9 AM
python3 create_event.py \
  --summary "Follow up on email" \
  --start "2026-02-12T09:00:00" \
  --end "2026-02-12T09:15:00"
```

### Block Focus Time

```bash
cd google-calendar/scripts

python3 create_event.py \
  --summary "Focus Time - Do Not Disturb" \
  --start "2026-02-12T14:00:00" \
  --end "2026-02-12T16:00:00"
```

### Check Availability

```bash
cd google-calendar/scripts

# Events in specific time range
python3 list_events.py --days-ahead 3 | grep "2026-02-14"
```

## Multiple Calendars

By default, scripts use your primary calendar. To use a different calendar:

```bash
# List calendars (use google-drive skill to search)
cd ../google-drive/scripts
python3 list_files.py --query "mimeType='application/vnd.google-apps.calendar'"

# Use specific calendar ID
cd ../google-calendar/scripts
python3 list_events.py --calendar "your-calendar-id@group.calendar.google.com"
```

## Timezones

All times use UTC by default. To use local times, specify timezone in ISO format:
```
2026-02-15T14:00:00+01:00  # CET
2026-02-15T14:00:00-05:00  # EST
```

Or convert to UTC before creating events.

## Limitations

**Current implementation supports:**
- Listing/searching events
- Creating events (timed and all-day)
- Updating event details
- Deleting events

**Not yet implemented (can be added if needed):**
- Recurring events
- Event reminders/notifications
- Attendees and invitations
- Event colors
- Attachments

For advanced features, use the Calendar web UI or extend the scripts.

## Script Dependencies

All scripts require:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Notes

- **Account:** Gladys's personal Google Calendar (not Simon's)
- **Primary calendar:** Default calendar for the account
- **Rate limits:** 1 million requests/day (more than enough)
- **Sharing:** Events are private by default
