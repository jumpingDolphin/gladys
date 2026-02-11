#!/usr/bin/env python3
"""Add a contact to Google Contacts via People API.

Usage:
    python3 add_contact.py --name "Contact Name" --email "email@example.com"
"""
import argparse
from gmail_auth import get_people_service

def add_contact(name, email):
    """Add a new contact to Google Contacts."""
    service = get_people_service()
    
    contact = {
        'names': [{
            'givenName': name
        }],
        'emailAddresses': [{
            'value': email
        }]
    }
    
    result = service.people().createContact(body=contact).execute()
    
    return result

def main():
    parser = argparse.ArgumentParser(description='Add contact to Google Contacts')
    parser.add_argument('--name', required=True, help='Contact name')
    parser.add_argument('--email', required=True, help='Contact email address')
    args = parser.parse_args()
    
    print(f"Adding contact: {args.name} <{args.email}>")
    result = add_contact(args.name, args.email)
    
    print(f"✓ Contact added successfully")
    print(f"  Resource name: {result.get('resourceName', 'N/A')}")

if __name__ == '__main__':
    main()
