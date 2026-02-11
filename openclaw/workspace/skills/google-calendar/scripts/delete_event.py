#!/usr/bin/env python3
"""Delete Google Calendar event.

Usage:
    python3 delete_event.py EVENT_ID [--calendar primary]
"""
import argparse
from google_auth import get_calendar_service

def delete_event(event_id, calendar_id='primary'):
    """Delete calendar event."""
    service = get_calendar_service()
    
    try:
        service.events().delete(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
        
        return True
    
    except Exception as e:
        print(f"Error deleting event: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Delete Google Calendar event')
    parser.add_argument('event_id', help='Event ID to delete')
    parser.add_argument('--calendar', default='primary', help='Calendar ID')
    args = parser.parse_args()
    
    if delete_event(args.event_id, args.calendar):
        print(f"✅ Event deleted: {args.event_id}")
    else:
        exit(1)

if __name__ == '__main__':
    main()
