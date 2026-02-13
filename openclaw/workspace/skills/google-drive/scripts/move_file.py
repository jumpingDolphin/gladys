#!/usr/bin/env python3
"""
Move a Google Drive file to a folder
"""
import sys
import argparse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth import get_credentials


def move_file(file_id, folder_id):
    """Move file to specified folder"""
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    
    # Retrieve the existing parents to remove
    file = service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    
    # Move the file to the new folder
    file = service.files().update(
        fileId=file_id,
        addParents=folder_id,
        removeParents=previous_parents,
        fields='id, name, parents'
    ).execute()
    
    print(f"✅ Moved '{file.get('name')}' to folder")
    print(f"   File ID: {file.get('id')}")
    print(f"   New parent: {folder_id}")
    return file


def main():
    parser = argparse.ArgumentParser(description='Move a Google Drive file to a folder')
    parser.add_argument('file_id', help='ID of file to move')
    parser.add_argument('folder_id', help='ID of destination folder')
    
    args = parser.parse_args()
    
    try:
        move_file(args.file_id, args.folder_id)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
