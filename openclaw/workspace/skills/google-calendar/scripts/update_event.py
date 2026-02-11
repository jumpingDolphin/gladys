#!/usr/bin/env python3
"""Update Google Calendar event.

Usage:
    python3 update_event.py EVENT_ID [--summary "New title"] [--start "..."] [--location "..."]
    
Examples:
    # Change title
    python3 update_event.py abc123 --summary "Updated Meeting Title"
    
    # Reschedule
    python3 update_event.py abc123 --start "2026-02-15T15:00:00" --end "2026-02-15T16:00:00"
    
    # Update location
    python3 update_event.py abc123 --location "Conference Room B"
"""
import argparse
from google_auth import get_calendar_service

def update_event(event_id, calendar_id='primary', summary=None, start=None, 
                 end=None, description=None, location=None, attendees=None):
    """Update calendar event."""
    service = get_calendar_service()
    
    try:
        # Get existing event
        event = service.events().get(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
        
        # Update fields
        if summary:
            event['summary'] = summary
        if description:
            event['description'] = description
        if location:
            event['location'] = location
        
        # Update attendees if provided
        if attendees:
            # Get existing attendees or create new list
            existing_attendees = event.get('attendees', [])
            # Add new attendees
            for email in attendees:
                if not any(a['email'] == email for a in existing_attendees):
                    existing_attendees.append({'email': email})
            event['attendees'] = existing_attendees
        
        # Update times if provided
        if start:
            event['start'] = {'dateTime': start, 'timeZone': 'UTC'}
        if end:
            event['end'] = {'dateTime': end, 'timeZone': 'UTC'}
        
        # Apply update (sendUpdates to notify attendees)
        updated_event = service.events().update(
            calendarId=calendar_id,
            eventId=event_id,
            body=event,
            sendUpdates='all'  # Send invites to attendees
        ).execute()
        
        return updated_event
    
    except Exception as e:
        print(f"Error updating event: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Update Google Calendar event')
    parser.add_argument('event_id', help='Event ID to update')
    parser.add_argument('--summary', help='New event title')
    parser.add_argument('--start', help='New start datetime (ISO format)')
    parser.add_argument('--end', help='New end datetime')
    parser.add_argument('--description', help='New description')
    parser.add_argument('--location', help='New location')
    parser.add_argument('--attendees', nargs='+', help='Email addresses to add as attendees')
    parser.add_argument('--calendar', default='primary', help='Calendar ID')
    args = parser.parse_args()
    
    event = update_event(
        args.event_id,
        calendar_id=args.calendar,
        summary=args.summary,
        start=args.start,
        end=args.end,
        description=args.description,
        location=args.location,
        attendees=args.attendees
    )
    
    if event:
        print(f"✅ Event updated!")
        print(f"   Title: {event['summary']}")
        print(f"   ID: {event['id']}")
        if 'attendees' in event:
            print(f"   Attendees: {', '.join([a['email'] for a in event['attendees']])}")
        print(f"   Link: {event.get('htmlLink', 'N/A')}")
    else:
        exit(1)

if __name__ == '__main__':
    main()
