#!/usr/bin/env python3
"""Append text to end of Google Doc.

Usage:
    python3 append_text.py DOC_ID "Text to append"
    python3 append_text.py DOC_ID --file input.txt
"""
import argparse
from google_auth import get_docs_service

def append_text(doc_id, text):
    """Append text to document."""
    service = get_docs_service()
    
    try:
        # Get current document to find end index
        doc = service.documents().get(documentId=doc_id).execute()
        end_index = doc['body']['content'][-1]['endIndex'] - 1
        
        # Append text
        requests = [{
            'insertText': {
                'location': {'index': end_index},
                'text': text
            }
        }]
        
        service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()
        
        return True
    
    except Exception as e:
        print(f"Error appending text: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Append text to Google Doc')
    parser.add_argument('doc_id', help='Document ID')
    parser.add_argument('text', nargs='?', help='Text to append')
    parser.add_argument('--file', help='Read text from file')
    args = parser.parse_args()
    
    # Get text from file or argument
    if args.file:
        with open(args.file, 'r') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("Error: Must provide text or --file")
        exit(1)
    
    if append_text(args.doc_id, text):
        print("✅ Text appended successfully!")
    else:
        exit(1)

if __name__ == '__main__':
    main()
