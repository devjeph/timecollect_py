""" connects to"""
import logging
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def sheet_service():
    """Connect to Google Sheets API"""
    credentials = None
    if os.path.exists('./google_credentials/token.json'):
        credentials = Credentials.from_authorized_user_file('./google_credentials/token.json', [os.getenv('SCOPES')])

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './google_credentials/credentials.json', [os.getenv('SCOPES')])
            credentials = flow.run_local_server(port=0)
        with open('./google_credentials/token.json', 'w', encoding="utf-8") as token:
            token.write(credentials.to_json())
    
    return credentials

if __name__ == '__main__':
    credentials = sheet_service()
    if credentials:
        logging.info("Connected to Google Sheets API")
    else:
        logging.error("Failed to connect to Google Sheets API")
    