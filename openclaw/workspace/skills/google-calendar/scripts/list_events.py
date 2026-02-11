#!/usr/bin/env python3
"""List and search Google Calendar events.

Usage:
    python3 list_events.py [--calendar primary] [--max N] [--days-ahead N] [--query "text"]
    
Examples:
    # List next 10 events
    python3 list_events.py --max 10
    
    # Events in next 7 days
    python3 list_events.py --days-ahead 7
    
    # Search for events
    python3 list_events.py --query "meeting"
    
    # Specific calendar
    python3 list_events.py --calendar "work@example.com"
"""
import argparse
import json
from datetime import datetime, timedelta
from google_auth import get_calendar_service

def list_events(calendar_id='primary', max_results=10, days_ahead=None, query=None):
    """List calendar events."""
    service = get_calendar_service()
    
    # Build time range
    now = datetime.utcnow().isoformat() + 'Z'
    time_max = None
    if days_ahead:
        future = datetime.utcnow() + timedelta(days=days_ahead)
        time_max = future.isoformat() + 'Z'
    
    try:
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime',
            q=query
        ).execute()
        
        events = events_result.get('items', [])
        return events
    
    except Exception as e:
        print(f"Error listing events: {e}")
        return []

def format_datetime(dt_str):
    """Format ISO datetime to readable string."""
    if not dt_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return dt_str

def main():
    parser = argparse.ArgumentParser(description='List Google Calendar events')
    parser.add_argument('--calendar', default='primary', help='Calendar ID')
    parser.add_argument('--max', type=int, default=10, dest='max_results', help='Max results')
    parser.add_argument('--days-ahead', type=int, help='Limit to N days in future')
    parser.add_argument('--query', help='Search query')
    parser.add_argument('--format', choices=['json', 'text'], default='text')
    args = parser.parse_args()
    
    events = list_events(args.calendar, args.max_results, args.days_ahead, args.query)
    
    if args.format == 'json':
        print(json.dumps(events, indent=2))
    else:
        if not events:
            print("No upcoming events found.")
        else:
            for i, event in enumerate(events, 1):
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                
                print(f"\n{i}. {event.get('summary', 'Untitled')}")
                print(f"   Start: {format_datetime(start)}")
                print(f"   End: {format_datetime(end)}")
                print(f"   ID: {event['id']}")
                
                if event.get('location'):
                    print(f"   Location: {event['location']}")
                if event.get('description'):
                    desc = event['description'][:100]
                    print(f"   Description: {desc}...")
            
            print(f"\nTotal: {len(events)} events")

if __name__ == '__main__':
    main()
