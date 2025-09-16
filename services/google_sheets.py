import os
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import settings

class GoogleSheetsService:
    """Service to interact with Google Sheets API."""

    def __init__(self):
        self.creds = self._authenticate()
        if self.creds:
            self.service = build('sheets', 'v4', credentials=self.creds, cache_discovery=False)
            logging.info("Google Sheets service initialized successfully.")
        else:
            self.service = None
            logging.error("Failed to initialize Google Sheets service due to authentication failure.")

    def _authenticate(self):
        """Handles user authentication for Google Sheets API."""

        creds = None
        if os.path.exists(settings.TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(settings.TOKEN_PATH, settings.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(settings.CREDENTIALS_PATH, settings.SCOPES)
                creds = flow.run_local_server(port=0)

            with open(settings.TOKEN_PATH, 'w', encoding="utf-8") as token:
                token.write(creds.to_json())

        return creds
    
    def get_data(self, spreadsheet_id: str, range_name: str) -> list[list[str]]:
        """Fetches data from a specified range in a Google Sheet.

        Args:
            spreadsheet_id (str): The ID of the spreadsheet to fetch data from.
            range_name (str): The A1 notation of the values to retrieve."""
        if not self.service:
            logging.error("Google Sheets service is not available.")
            return []
        try:
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
            values = result.get('values', [])

            if not values:
                logging.info('No data found.')
                return []
            
            # Pad rows to ensure consistent structure
            max_cols = max(len(row) for row in values)
            processed_values = []
            for row in values:
                padded_row = row + ['0.00'] * (max_cols - len(row))
                processed_values.append(['0.00'] if not cell else cell for cell in padded_row)

            return processed_values
        except HttpError as err:
            logging.error(f"An API error occurred for sheet '{spreadsheet_id}': {err}")
            return []