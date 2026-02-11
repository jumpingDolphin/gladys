#!/usr/bin/env python3
"""Get contacts from Google People API.

Usage:
    python3 get_contacts.py [--format json|text] [--search NAME]
"""
import argparse
import json
from gmail_auth import get_people_service

def get_all_contacts():
    """Fetch all contacts with email addresses."""
    service = get_people_service()
    contacts = []
    
    page_token = None
    while True:
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=1000,
            personFields='names,emailAddresses',
            pageToken=page_token
        ).execute()
        
        connections = results.get('connections', [])
        for person in connections:
            names = person.get('names', [])
            emails = person.get('emailAddresses', [])
            
            if names and emails:
                name = names[0].get('displayName', '')
                for email in emails:
                    contacts.append({
                        'name': name,
                        'email': email.get('value', '')
                    })
        
        page_token = results.get('nextPageToken')
        if not page_token:
            break
    
    return contacts

def main():
    parser = argparse.ArgumentParser(description='Get contacts from Google People API')
    parser.add_argument('--format', choices=['json', 'text'], default='text',
                       help='Output format')
    parser.add_argument('--search', help='Search for contact by name')
    args = parser.parse_args()
    
    contacts = get_all_contacts()
    
    # Filter if search term provided
    if args.search:
        search_lower = args.search.lower()
        contacts = [c for c in contacts if search_lower in c['name'].lower()]
    
    if args.format == 'json':
        print(json.dumps(contacts, indent=2))
    else:
        for contact in contacts:
            print(f"{contact['name']} <{contact['email']}>")
        print(f"\nTotal: {len(contacts)} contacts")

if __name__ == '__main__':
    main()
