#!/usr/bin/env python3
"""Create a new Google Sheet.

Usage:
    python3 create_sheet.py "Sheet Title"
"""
import argparse
from google_auth import get_sheets_service, get_drive_service

def create_sheet(title):
    """Create new Google Sheet."""
    sheets_service = get_sheets_service()
    drive_service = get_drive_service()
    
    try:
        # Create spreadsheet
        spreadsheet = sheets_service.spreadsheets().create(
            body={'properties': {'title': title}}
        ).execute()
        
        sheet_id = spreadsheet['spreadsheetId']
        
        # Get web link
        file_meta = drive_service.files().get(
            fileId=sheet_id,
            fields='webViewLink'
        ).execute()
        
        return {
            'id': sheet_id,
            'title': spreadsheet['properties']['title'],
            'link': file_meta.get('webViewLink', '')
        }
    
    except Exception as e:
        print(f"Error creating spreadsheet: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Create new Google Sheet')
    parser.add_argument('title', help='Spreadsheet title')
    args = parser.parse_args()
    
    sheet = create_sheet(args.title)
    
    if sheet:
        print(f"✅ Spreadsheet created!")
        print(f"   Title: {sheet['title']}")
        print(f"   ID: {sheet['id']}")
        print(f"   Link: {sheet['link']}")
    else:
        exit(1)

if __name__ == '__main__':
    main()
