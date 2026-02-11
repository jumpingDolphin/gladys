#!/usr/bin/env python3
"""Read content from Google Doc.

Usage:
    python3 read_doc.py DOC_ID [--format text|json]
"""
import argparse
import json
from google_auth import get_docs_service

def read_document(doc_id):
    """Read document content."""
    service = get_docs_service()
    
    try:
        doc = service.documents().get(documentId=doc_id).execute()
        
        # Extract text content
        content = []
        for element in doc.get('body', {}).get('content', []):
            if 'paragraph' in element:
                for text_run in element['paragraph'].get('elements', []):
                    if 'textRun' in text_run:
                        content.append(text_run['textRun'].get('content', ''))
        
        return {
            'id': doc['documentId'],
            'title': doc.get('title', ''),
            'text': ''.join(content)
        }
    
    except Exception as e:
        print(f"Error reading document: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Read Google Doc content')
    parser.add_argument('doc_id', help='Document ID')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    args = parser.parse_args()
    
    doc = read_document(args.doc_id)
    
    if not doc:
        exit(1)
    
    if args.format == 'json':
        print(json.dumps(doc, indent=2))
    else:
        print(f"Title: {doc['title']}")
        print(f"ID: {doc['id']}")
        print(f"\n{'-' * 80}\n")
        print(doc['text'])

if __name__ == '__main__':
    main()
