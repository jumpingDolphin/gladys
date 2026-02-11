#!/usr/bin/env python3
"""List and search Gmail messages.

Usage:
    python3 list_emails.py [--query "SEARCH"] [--max-results N] [--unread-only]
    
Examples:
    # List unread emails
    python3 list_emails.py --unread-only
    
    # Search for emails from a specific sender
    python3 list_emails.py --query "from:alice@example.com"
    
    # List recent emails
    python3 list_emails.py --max-results 10
"""
import argparse
import json
from datetime import datetime
from gmail_auth import get_gmail_service

def list_messages(query='', max_results=20, unread_only=False):
    """List Gmail messages matching query."""
    service = get_gmail_service()
    
    # Build query
    if unread_only:
        query = f"is:unread {query}".strip()
    
    try:
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            return []
        
        # Fetch full message details
        detailed_messages = []
        for msg in messages:
            msg_detail = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'Subject', 'Date']
            ).execute()
            
            headers = {h['name']: h['value'] for h in msg_detail['payload']['headers']}
            
            detailed_messages.append({
                'id': msg_detail['id'],
                'threadId': msg_detail['threadId'],
                'snippet': msg_detail.get('snippet', ''),
                'from': headers.get('From', ''),
                'subject': headers.get('Subject', ''),
                'date': headers.get('Date', ''),
                'unread': 'UNREAD' in msg_detail.get('labelIds', [])
            })
        
        return detailed_messages
    
    except Exception as e:
        print(f"Error listing messages: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='List Gmail messages')
    parser.add_argument('--query', default='', help='Gmail search query')
    parser.add_argument('--max-results', type=int, default=20, help='Maximum results')
    parser.add_argument('--unread-only', action='store_true', help='Show only unread')
    parser.add_argument('--format', choices=['json', 'text'], default='text')
    args = parser.parse_args()
    
    messages = list_messages(args.query, args.max_results, args.unread_only)
    
    if args.format == 'json':
        print(json.dumps(messages, indent=2))
    else:
        if not messages:
            print("No messages found.")
        else:
            for i, msg in enumerate(messages, 1):
                unread_marker = '[UNREAD] ' if msg['unread'] else ''
                print(f"\n{i}. {unread_marker}{msg['subject']}")
                print(f"   From: {msg['from']}")
                print(f"   Date: {msg['date']}")
                print(f"   ID: {msg['id']}")
                print(f"   Preview: {msg['snippet'][:100]}...")

if __name__ == '__main__':
    main()
