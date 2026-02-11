"""Gmail authentication utilities."""
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

WORKSPACE_DIR = Path(__file__).parent.parent.parent.parent
TOKEN_PATH = WORKSPACE_DIR / "google_token.json"
CREDENTIALS_PATH = WORKSPACE_DIR / "google_credentials.json"

def get_credentials():
    """Load and refresh credentials if needed."""
    if not TOKEN_PATH.exists():
        raise FileNotFoundError(f"Token file not found: {TOKEN_PATH}")
    
    with open(TOKEN_PATH, 'r') as f:
        token_data = json.load(f)
    
    creds = Credentials.from_authorized_user_info(token_data)
    
    # Refresh if expired
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save refreshed token
        with open(TOKEN_PATH, 'w') as f:
            json.dump(json.loads(creds.to_json()), f, indent=2)
    
    return creds

def get_gmail_service():
    """Get authenticated Gmail API service."""
    creds = get_credentials()
    return build('gmail', 'v1', credentials=creds)

def get_people_service():
    """Get authenticated People API service."""
    creds = get_credentials()
    return build('people', 'v1', credentials=creds)
