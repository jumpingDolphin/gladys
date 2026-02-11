#!/usr/bin/env python3
"""Write data to Google Sheet.

Usage:
    python3 write_sheet.py SHEET_ID --range "Sheet1!A1" --data '[["A1", "B1"], ["A2", "B2"]]'
    python3 write_sheet.py SHEET_ID --range "Sheet1!A1" --csv-file data.csv
"""
import argparse
import json
import csv
from google_auth import get_sheets_service

def write_sheet(sheet_id, range_name, values):
    """Write data to sheet."""
    service = get_sheets_service()
    
    try:
        body = {'values': values}
        result = service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        
        return result
    
    except Exception as e:
        print(f"Error writing to sheet: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Write data to Google Sheet')
    parser.add_argument('sheet_id', help='Spreadsheet ID')
    parser.add_argument('--range', required=True, help='Range to write (e.g., Sheet1!A1)')
    parser.add_argument('--data', help='JSON array of rows (e.g., [["A1","B1"],["A2","B2"]])')
    parser.add_argument('--csv-file', help='Read data from CSV file')
    args = parser.parse_args()
    
    # Get data from JSON or CSV
    if args.csv_file:
        with open(args.csv_file, 'r') as f:
            reader = csv.reader(f)
            values = list(reader)
    elif args.data:
        values = json.loads(args.data)
    else:
        print("Error: Must provide --data or --csv-file")
        exit(1)
    
    result = write_sheet(args.sheet_id, args.range, values)
    
    if result:
        print(f"✅ Data written successfully!")
        print(f"   Updated cells: {result.get('updatedCells', 0)}")
        print(f"   Updated range: {result.get('updatedRange', '')}")
    else:
        exit(1)

if __name__ == '__main__':
    main()
