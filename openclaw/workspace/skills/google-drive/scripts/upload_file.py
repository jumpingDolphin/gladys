#!/usr/bin/env python3
"""Upload file to Google Drive.

Usage:
    python3 upload_file.py FILE_PATH [--name "Custom Name"] [--folder FOLDER_ID] [--description "..."]
"""
import argparse
import os
from googleapiclient.http import MediaFileUpload
from google_auth import get_drive_service

def upload_file(file_path, name=None, folder_id=None, description=None):
    """Upload file to Drive."""
    service = get_drive_service()
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return None
    
    # Use filename if name not specified
    if not name:
        name = os.path.basename(file_path)
    
    # Build file metadata
    file_metadata = {'name': name}
    if folder_id:
        file_metadata['parents'] = [folder_id]
    if description:
        file_metadata['description'] = description
    
    # Upload
    try:
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink, size'
        ).execute()
        
        return file
    
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Upload file to Google Drive')
    parser.add_argument('file_path', help='Path to file to upload')
    parser.add_argument('--name', help='Custom name for uploaded file')
    parser.add_argument('--folder', help='Folder ID to upload to')
    parser.add_argument('--description', help='File description')
    args = parser.parse_args()
    
    print(f"Uploading {args.file_path}...")
    file = upload_file(args.file_path, args.name, args.folder, args.description)
    
    if file:
        print(f"\n✅ File uploaded successfully!")
        print(f"   Name: {file['name']}")
        print(f"   ID: {file['id']}")
        print(f"   Size: {file.get('size', 'N/A')} bytes")
        print(f"   Link: {file.get('webViewLink', 'N/A')}")
    else:
        exit(1)

if __name__ == '__main__':
    main()
