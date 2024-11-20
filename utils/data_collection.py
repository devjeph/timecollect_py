""" 
After successfully connects with Google Sheet API, 
this will gather values from google sheet with spreadsheetId.
"""
import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import services.google_api



# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_data(spreadsheet_id, range_name):
    """
    Retrieves data from Google Sheets and replaces blank values with "0.00"
    """
    credentials = services.google_api.sheet_service()
    try:
        service = build("sheets", "v4", credentials=credentials, cache_discovery=False)

        # Calling Sheets API
        sheet = service.spreadsheets() # This is correct
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get("values", [])

        # Replace blank values with 0.00
        for i, row in enumerate(values):
            for j, value in enumerate(row):
                if not value:
                    values[i][j] = '0.00'

        return values

    except HttpError as error:
        logging.error("An error occurred: %s", error)
        return []

if __name__ == "__main__":
    data_values = run_data('1gBCnhREhrI8WmClCXkOxpRhn7T97Qics1Ori3cev0ss', "202411!A7:AT39")
    print(data_values)
