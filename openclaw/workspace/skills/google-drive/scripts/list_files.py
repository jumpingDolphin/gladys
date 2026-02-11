#!/usr/bin/env python3
"""List and search Google Drive files.

Usage:
    python3 list_files.py [--query "SEARCH"] [--max N] [--folder FOLDER_ID]
    
Examples:
    # List recent files
    python3 list_files.py --max 20
    
    # Search by name
    python3 list_files.py --query "name contains 'report'"
    
    # List files in specific folder
    python3 list_files.py --folder 1ABC...XYZ
    
    # Search by type
    python3 list_files.py --query "mimeType='application/vnd.google-apps.document'"
"""
import argparse
import json
from google_auth import get_drive_service

def list_files(query='', max_results=100, folder_id=None):
    """List Drive files matching query."""
    service = get_drive_service()
    
    # Build query
    q_parts = []
    if query:
        q_parts.append(query)
    if folder_id:
        q_parts.append(f"'{folder_id}' in parents")
    q_parts.append("trashed=false")  # Exclude trash
    
    q = ' and '.join(q_parts)
    
    try:
        results = service.files().list(
            q=q,
            pageSize=max_results,
            fields="files(id, name, mimeType, createdTime, modifiedTime, size, webViewLink, owners)",
            orderBy="modifiedTime desc"
        ).execute()
        
        files = results.get('files', [])
        return files
    
    except Exception as e:
        print(f"Error listing files: {e}")
        return []

def format_size(size_bytes):
    """Format file size in human-readable format."""
    if not size_bytes:
        return "N/A"
    
    size = int(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def main():
    parser = argparse.ArgumentParser(description='List Google Drive files')
    parser.add_argument('--query', default='', help='Drive search query')
    parser.add_argument('--max', type=int, default=100, dest='max_results', help='Max results')
    parser.add_argument('--folder', help='Folder ID to list files from')
    parser.add_argument('--format', choices=['json', 'text'], default='text')
    args = parser.parse_args()
    
    files = list_files(args.query, args.max_results, args.folder)
    
    if args.format == 'json':
        print(json.dumps(files, indent=2))
    else:
        if not files:
            print("No files found.")
        else:
            for i, file in enumerate(files, 1):
                size = format_size(file.get('size'))
                mime = file.get('mimeType', '').split('.')[-1]
                print(f"\n{i}. {file['name']}")
                print(f"   ID: {file['id']}")
                print(f"   Type: {mime}")
                print(f"   Size: {size}")
                print(f"   Modified: {file.get('modifiedTime', 'N/A')}")
                print(f"   Link: {file.get('webViewLink', 'N/A')}")
            print(f"\nTotal: {len(files)} files")

if __name__ == '__main__':
    main()
