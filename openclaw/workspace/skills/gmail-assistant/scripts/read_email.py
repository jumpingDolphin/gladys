#!/usr/bin/env python3
"""Read a specific Gmail message.

Usage:
    python3 read_email.py MESSAGE_ID [--mark-read]
"""
import argparse
import base64
import json
from gmail_auth import get_gmail_service

def get_message_body(payload):
    """Extract message body from payload."""
    body = ""
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                if 'data' in part['body']:
                    body += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            elif part['mimeType'] == 'text/html' and not body:
                # Fallback to HTML if no plain text
                if 'data' in part['body']:
                    body += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
            elif 'parts' in part:
                # Recursive for nested parts
                body += get_message_body(part)
    elif 'body' in payload and 'data' in payload['body']:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    
    return body

def read_message(message_id, mark_read=False):
    """Read a Gmail message by ID."""
    service = get_gmail_service()
    
    try:
        msg = service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()
        
        headers = {h['name']: h['value'] for h in msg['payload']['headers']}
        body = get_message_body(msg['payload'])
        
        result = {
            'id': msg['id'],
            'threadId': msg['threadId'],
            'from': headers.get('From', ''),
            'to': headers.get('To', ''),
            'subject': headers.get('Subject', ''),
            'date': headers.get('Date', ''),
            'body': body,
            'snippet': msg.get('snippet', ''),
            'labels': msg.get('labelIds', [])
        }
        
        # Mark as read if requested
        if mark_read and 'UNREAD' in result['labels']:
            service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            result['labels'].remove('UNREAD')
        
        return result
    
    except Exception as e:
        print(f"Error reading message: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Read a Gmail message')
    parser.add_argument('message_id', help='Message ID to read')
    parser.add_argument('--mark-read', action='store_true', help='Mark message as read')
    parser.add_argument('--format', choices=['json', 'text'], default='text')
    args = parser.parse_args()
    
    msg = read_message(args.message_id, args.mark_read)
    
    if not msg:
        exit(1)
    
    if args.format == 'json':
        print(json.dumps(msg, indent=2))
    else:
        print(f"From: {msg['from']}")
        print(f"To: {msg['to']}")
        print(f"Subject: {msg['subject']}")
        print(f"Date: {msg['date']}")
        print(f"\n{'-' * 80}\n")
        print(msg['body'])

if __name__ == '__main__':
    main()
