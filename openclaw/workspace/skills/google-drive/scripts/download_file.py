#!/usr/bin/env python3
"""Download file from Google Drive.

Usage:
    python3 download_file.py FILE_ID [--output PATH]
"""
import argparse
import io
from googleapiclient.http import MediaIoBaseDownload
from google_auth import get_drive_service

def download_file(file_id, output_path=None):
    """Download file from Drive."""
    service = get_drive_service()
    
    try:
        # Get file metadata
        file_meta = service.files().get(fileId=file_id, fields='name, mimeType').execute()
        file_name = file_meta['name']
        mime_type = file_meta.get('mimeType', '')
        
        # Use file name if output not specified
        if not output_path:
            output_path = file_name
        
        # Handle Google Workspace files (Docs, Sheets, etc.)
        if mime_type.startswith('application/vnd.google-apps'):
            # Export as appropriate format
            export_formats = {
                'application/vnd.google-apps.document': ('application/pdf', '.pdf'),
                'application/vnd.google-apps.spreadsheet': ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx'),
                'application/vnd.google-apps.presentation': ('application/pdf', '.pdf'),
            }
            
            if mime_type in export_formats:
                export_mime, ext = export_formats[mime_type]
                if not output_path.endswith(ext):
                    output_path += ext
                
                request = service.files().export_media(fileId=file_id, mimeType=export_mime)
            else:
                print(f"Warning: Cannot export {mime_type}, trying direct download...")
                request = service.files().get_media(fileId=file_id)
        else:
            # Regular file download
            request = service.files().get_media(fileId=file_id)
        
        # Download
        fh = io.FileIO(output_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"Download {int(status.progress() * 100)}%")
        
        fh.close()
        return output_path
    
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Download file from Google Drive')
    parser.add_argument('file_id', help='Drive file ID')
    parser.add_argument('--output', help='Output file path')
    args = parser.parse_args()
    
    path = download_file(args.file_id, args.output)
    
    if path:
        print(f"\n✅ File downloaded to: {path}")
    else:
        exit(1)

if __name__ == '__main__':
    main()
