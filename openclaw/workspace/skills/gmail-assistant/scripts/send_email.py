#!/usr/bin/env python3
"""Send email via Gmail API with contact validation.

SECURITY GUARDRAILS:
- Only allows sending to email addresses that exist in contacts
- Validates all recipients (to, cc, bcc) against contacts
- Requires explicit --force flag to bypass (for emergency use only)

Usage:
    python3 send_email.py --to "email@example.com" --subject "Subject" --body "Body text"
    python3 send_email.py --to "email@example.com" --subject "Subject" --body-file message.txt
    python3 send_email.py --to "alice@example.com" --cc "bob@example.com" --subject "Subject" --body "Text"
    python3 send_email.py --to "kindle@example.com" --subject "Document" --attach "/path/to/file.pdf"
"""
import argparse
import base64
import json
import mimetypes
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from gmail_auth import get_gmail_service
from get_contacts import get_all_contacts

def validate_recipients(recipients, contacts, force=False):
    """
    Validate that all recipients are in contacts.
    
    Args:
        recipients: List of email addresses
        contacts: List of contact dicts with 'email' keys
        force: If True, skip validation
    
    Returns:
        (valid, unknown_emails) tuple
    """
    if force:
        return True, []
    
    contact_emails = {c['email'].lower() for c in contacts}
    unknown = [r for r in recipients if r.lower() not in contact_emails]
    
    return len(unknown) == 0, unknown

def parse_recipients(recipient_string):
    """Parse comma-separated email addresses."""
    if not recipient_string:
        return []
    return [email.strip() for email in recipient_string.split(',')]

def send_email(to, subject, body, cc=None, bcc=None, attachments=None, force=False, dry_run=False):
    """Send email via Gmail API with optional attachments."""
    # Parse recipients
    to_list = parse_recipients(to)
    cc_list = parse_recipients(cc) if cc else []
    bcc_list = parse_recipients(bcc) if bcc else []
    all_recipients = to_list + cc_list + bcc_list
    
    if not all_recipients:
        print("ERROR: No recipients specified")
        return False
    
    # Load contacts for validation
    print("Loading contacts for validation...")
    contacts = get_all_contacts()
    print(f"Loaded {len(contacts)} contacts")
    
    # Validate recipients
    valid, unknown = validate_recipients(all_recipients, contacts, force)
    
    if not valid:
        print("\n❌ SECURITY GUARDRAIL TRIGGERED")
        print("The following recipients are NOT in your contacts:")
        for email in unknown:
            print(f"  - {email}")
        print("\nEmail NOT sent. Add these contacts first, or use --force to override (not recommended).")
        return False
    
    print("✓ All recipients validated against contacts")
    
    # Create message
    message = MIMEMultipart()
    message['to'] = to
    if cc:
        message['cc'] = cc
    if bcc:
        message['bcc'] = bcc
    message['subject'] = subject
    
    # Add body
    message.attach(MIMEText(body, 'plain'))
    
    # Add attachments
    if attachments:
        for file_path in attachments:
            if not os.path.exists(file_path):
                print(f"⚠️  Attachment not found: {file_path}")
                continue
            
            filename = os.path.basename(file_path)
            print(f"Attaching: {filename} ({os.path.getsize(file_path)} bytes)")
            
            # Guess MIME type
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'
            
            main_type, sub_type = content_type.split('/', 1)
            
            with open(file_path, 'rb') as f:
                part = MIMEBase(main_type, sub_type)
                part.set_payload(f.read())
            
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            message.attach(part)
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    if dry_run:
        print("\n🔍 DRY RUN - Email would be sent:")
        print(f"To: {to}")
        if cc:
            print(f"CC: {cc}")
        if bcc:
            print(f"BCC: {bcc}")
        print(f"Subject: {subject}")
        print(f"\nBody:\n{body}")
        if attachments:
            print(f"\nAttachments: {', '.join(os.path.basename(a) for a in attachments)}")
        return True
    
    # Send
    service = get_gmail_service()
    try:
        sent_message = service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()
        
        print(f"\n✅ Email sent successfully!")
        print(f"Message ID: {sent_message['id']}")
        return True
    
    except Exception as e:
        print(f"\n❌ Error sending email: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Send email via Gmail with contact validation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
SECURITY NOTES:
  This script enforces a guardrail: emails can only be sent to addresses
  that exist in your Google Contacts. This prevents accidental sends to
  unknown recipients.
  
  Use --force to bypass (not recommended).
        """
    )
    parser.add_argument('--to', required=True, help='Recipient email (comma-separated for multiple)')
    parser.add_argument('--cc', help='CC recipients (comma-separated)')
    parser.add_argument('--bcc', help='BCC recipients (comma-separated)')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--body', help='Email body text (use empty string for attachments-only)')
    parser.add_argument('--body-file', help='Read body from file')
    parser.add_argument('--attach', action='append', help='Attach file (can be used multiple times)')
    parser.add_argument('--force', action='store_true', 
                       help='DANGEROUS: Skip contact validation')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be sent without sending')
    args = parser.parse_args()
    
    # Get body from file or arg (allow empty for attachments-only emails)
    if args.body_file:
        with open(args.body_file, 'r') as f:
            body = f.read()
    elif args.body is not None:
        body = args.body
    else:
        # Default to empty body if only attachments
        body = ""
    
    success = send_email(
        args.to,
        args.subject,
        body,
        cc=args.cc,
        bcc=args.bcc,
        attachments=args.attach,
        force=args.force,
        dry_run=args.dry_run
    )
    
    exit(0 if success else 1)

if __name__ == '__main__':
    main()
