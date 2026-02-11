#!/usr/bin/env python3
"""Create folder in Google Drive.

Usage:
    python3 create_folder.py FOLDER_NAME [--parent PARENT_FOLDER_ID]
"""
import argparse
from google_auth import get_drive_service

def create_folder(name, parent_id=None):
    """Create folder in Drive."""
    service = get_drive_service()
    
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    
    if parent_id:
        file_metadata['parents'] = [parent_id]
    
    try:
        folder = service.files().create(
            body=file_metadata,
            fields='id, name, webViewLink'
        ).execute()
        
        return folder
    
    except Exception as e:
        print(f"Error creating folder: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Create folder in Google Drive')
    parser.add_argument('name', help='Folder name')
    parser.add_argument('--parent', help='Parent folder ID')
    args = parser.parse_args()
    
    folder = create_folder(args.name, args.parent)
    
    if folder:
        print(f"✅ Folder created!")
        print(f"   Name: {folder['name']}")
        print(f"   ID: {folder['id']}")
        print(f"   Link: {folder.get('webViewLink', 'N/A')}")
    else:
        exit(1)

if __name__ == '__main__':
    main()
