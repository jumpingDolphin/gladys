#!/usr/bin/env python3
"""Read data from Google Sheet.

Usage:
    python3 read_sheet.py SHEET_ID [--range "Sheet1!A1:C10"] [--format csv|json]
"""
import argparse
import json
import csv
import sys
from google_auth import get_sheets_service

def read_sheet(sheet_id, range_name='Sheet1'):
    """Read sheet data."""
    service = get_sheets_service()
    
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        return values
    
    except Exception as e:
        print(f"Error reading sheet: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description='Read Google Sheet data')
    parser.add_argument('sheet_id', help='Spreadsheet ID')
    parser.add_argument('--range', default='Sheet1', help='Range to read (e.g., Sheet1!A1:C10)')
    parser.add_argument('--format', choices=['csv', 'json', 'text'], default='text')
    args = parser.parse_args()
    
    data = read_sheet(args.sheet_id, args.range)
    
    if data is None:
        exit(1)
    
    if not data:
        print("No data found.", file=sys.stderr)
        exit(0)
    
    if args.format == 'json':
        print(json.dumps(data, indent=2))
    elif args.format == 'csv':
        writer = csv.writer(sys.stdout)
        writer.writerows(data)
    else:
        # Text table format
        for row in data:
            print('\t'.join(str(cell) for cell in row))

if __name__ == '__main__':
    main()
