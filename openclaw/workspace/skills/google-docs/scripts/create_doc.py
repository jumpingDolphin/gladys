#!/usr/bin/env python3
"""Create a new Google Doc.

Usage:
    python3 create_doc.py "Document Title" [--content "Initial content"]
"""
import argparse
from google_auth import get_docs_service, get_drive_service

def create_doc(title, initial_content=None):
    """Create new Google Doc."""
    docs_service = get_docs_service()
    drive_service = get_drive_service()
    
    try:
        # Create document
        doc = docs_service.documents().create(body={'title': title}).execute()
        doc_id = doc['documentId']
        
        # Add initial content if provided
        if initial_content:
            requests = [{
                'insertText': {
                    'location': {'index': 1},
                    'text': initial_content
                }
            }]
            docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
        
        # Get web link
        file_meta = drive_service.files().get(
            fileId=doc_id,
            fields='webViewLink'
        ).execute()
        
        return {
            'id': doc_id,
            'title': doc['title'],
            'link': file_meta.get('webViewLink', '')
        }
    
    except Exception as e:
        print(f"Error creating document: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Create new Google Doc')
    parser.add_argument('title', help='Document title')
    parser.add_argument('--content', help='Initial content')
    args = parser.parse_args()
    
    doc = create_doc(args.title, args.content)
    
    if doc:
        print(f"✅ Document created!")
        print(f"   Title: {doc['title']}")
        print(f"   ID: {doc['id']}")
        print(f"   Link: {doc['link']}")
    else:
        exit(1)

if __name__ == '__main__':
    main()
