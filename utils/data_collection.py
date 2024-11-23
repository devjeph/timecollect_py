# data_collection.py

"""
Retrieves data from a Google Sheet specified by spreadsheetId. 
Blank cells in the sheet are replaced with "0.00".

This script requires Google API credentials to be set up and 
environment variables for the spreadsheet ID and range. 
"""

import logging
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dotenv import load_dotenv  # Moved import to the top
from api_services.google_api import sheet_service

# Load environment variables
load_dotenv()


def get_data(creds, spreadsheet_id, range_name):
    """
    Retrieves data from Google Sheets and replaces blank values with "0.00".

    Args:
        creds: Google API credentials object.
        spreadsheet_id: The ID of the Google Sheet.
        range_name: The range of cells to retrieve data from (e.g., "Sheet1!A1:B10").

    Returns:
        A list of lists representing the data from the sheet,
        or an empty list if an error occurs.
    """
    try:
        service = build("sheets", "v4", credentials=creds, cache_discovery=False)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        )
        values = result.get("values", [])

        # Replace blank values with "0.00"
        for i, row in enumerate(values):
            for j, value in enumerate(row):
                if not value:  # Check if the cell value is empty
                    values[i][j] = "0.00"
        return values

    except HttpError as error:
        logging.error("An error occurred: %s", error)
        return []


if __name__ == "__main__":
    creds = sheet_service()
    data_values = get_data(
        creds, os.getenv("TEST_SPREADSHEET"), os.getenv("TEST_RANGE")
    )
    print(data_values)
