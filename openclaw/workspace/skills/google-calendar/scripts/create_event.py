#!/usr/bin/env python3
"""Create Google Calendar event.

Usage:
    python3 create_event.py --summary "Meeting" --start "2026-02-15T14:00:00" --end "2026-02-15T15:00:00"
    python3 create_event.py --summary "All day event" --date "2026-02-20"
    
Examples:
    # Meeting with time
    python3 create_event.py \
      --summary "Team Standup" \
      --start "2026-02-12T10:00:00" \
      --end "2026-02-12T10:30:00" \
      --description "Daily sync" \
      --location "Zoom"
    
    # All-day event
    python3 create_event.py \
      --summary "Vacation" \
      --date "2026-03-01" \
      --date-end "2026-03-08"
    
    # Quick event (1 hour from now)
    python3 create_event.py --summary "Quick sync" --duration 60
"""
import argparse
from datetime import datetime, timedelta
from google_auth import get_calendar_service

def create_event(summary, start=None, end=None, date=None, date_end=None, 
                 duration=None, description=None, location=None, 
                 attendees=None, calendar_id='primary'):
    """Create calendar event."""
    service = get_calendar_service()
    
    event = {'summary': summary}
    
    # Add attendees if provided
    if attendees:
        event['attendees'] = [{'email': email} for email in attendees]
    
    # Handle all-day event
    if date:
        event['start'] = {'date': date}
        if date_end:
            event['end'] = {'date': date_end}
        else:
            # Single day event
            event['end'] = {'date': date}
    
    # Handle timed event
    elif start:
        # If duration given, calculate end
        if duration and not end:
            start_dt = datetime.fromisoformat(start)
            end_dt = start_dt + timedelta(minutes=duration)
            end = end_dt.isoformat()
        
        event['start'] = {'dateTime': start, 'timeZone': 'UTC'}
        event['end'] = {'dateTime': end, 'timeZone': 'UTC'}
    
    # Quick event (duration from now)
    elif duration:
        now = datetime.utcnow()
        start = now.isoformat() + 'Z'
        end_dt = now + timedelta(minutes=duration)
        end = end_dt.isoformat() + 'Z'
        
        event['start'] = {'dateTime': start, 'timeZone': 'UTC'}
        event['end'] = {'dateTime': end, 'timeZone': 'UTC'}
    
    else:
        print("Error: Must provide --start/--end, --date, or --duration")
        return None
    
    # Optional fields
    if description:
        event['description'] = description
    if location:
        event['location'] = location
    
    try:
        created_event = service.events().insert(
            calendarId=calendar_id,
            body=event,
            sendUpdates='all' if attendees else 'none'  # Send invites if attendees present
        ).execute()
        
        return created_event
    
    except Exception as e:
        print(f"Error creating event: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Create Google Calendar event')
    parser.add_argument('--summary', required=True, help='Event title')
    parser.add_argument('--start', help='Start datetime (ISO format: 2026-02-15T14:00:00)')
    parser.add_argument('--end', help='End datetime')
    parser.add_argument('--date', help='All-day event date (YYYY-MM-DD)')
    parser.add_argument('--date-end', help='All-day event end date (exclusive)')
    parser.add_argument('--duration', type=int, help='Duration in minutes (for quick events)')
    parser.add_argument('--description', help='Event description')
    parser.add_argument('--location', help='Event location')
    parser.add_argument('--attendees', nargs='+', help='Email addresses to invite')
    parser.add_argument('--calendar', default='primary', help='Calendar ID')
    args = parser.parse_args()
    
    event = create_event(
        args.summary,
        start=args.start,
        end=args.end,
        date=args.date,
        date_end=args.date_end,
        duration=args.duration,
        description=args.description,
        location=args.location,
        attendees=args.attendees,
        calendar_id=args.calendar
    )
    
    if event:
        print(f"✅ Event created!")
        print(f"   Title: {event['summary']}")
        print(f"   ID: {event['id']}")
        if 'attendees' in event:
            print(f"   Attendees: {', '.join([a['email'] for a in event['attendees']])}")
        print(f"   Link: {event.get('htmlLink', 'N/A')}")
    else:
        exit(1)

if __name__ == '__main__':
    main()
