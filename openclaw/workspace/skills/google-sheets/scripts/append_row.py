#!/usr/bin/env python3
"""Append rows to Google Sheet.

Usage:
    python3 append_row.py SHEET_ID --row '["Col1", "Col2", "Col3"]'
    python3 append_row.py SHEET_ID --csv-file data.csv
"""
import argparse
import json
import csv
from google_auth import get_sheets_service

def append_rows(sheet_id, values, range_name='Sheet1'):
    """Append rows to sheet."""
    service = get_sheets_service()
    
    try:
        body = {'values': values}
        result = service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        
        return result
    
    except Exception as e:
        print(f"Error appending rows: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Append rows to Google Sheet')
    parser.add_argument('sheet_id', help='Spreadsheet ID')
    parser.add_argument('--range', default='Sheet1', help='Sheet name (e.g., Sheet1)')
    parser.add_argument('--row', help='Single row as JSON array (e.g., ["A","B","C"])')
    parser.add_argument('--rows', help='Multiple rows as JSON array (e.g., [["A1","B1"],["A2","B2"]])')
    parser.add_argument('--csv-file', help='Read rows from CSV file')
    args = parser.parse_args()
    
    # Get data
    if args.csv_file:
        with open(args.csv_file, 'r') as f:
            reader = csv.reader(f)
            values = list(reader)
    elif args.rows:
        values = json.loads(args.rows)
    elif args.row:
        values = [json.loads(args.row)]
    else:
        print("Error: Must provide --row, --rows, or --csv-file")
        exit(1)
    
    result = append_rows(args.sheet_id, values, args.range)
    
    if result:
        print(f"✅ Rows appended successfully!")
        print(f"   Updated cells: {result.get('updates', {}).get('updatedCells', 0)}")
        print(f"   Updated range: {result.get('updates', {}).get('updatedRange', '')}")
    else:
        exit(1)

if __name__ == '__main__':
    main()
