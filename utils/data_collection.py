# utils/data_collection.py
import logging
import os
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

from api_services.google_api import sheet_service

load_dotenv()

def get_data(creds, spreadsheet_id, range_name, delay=0.5, max_retries=3):
    """
    Retrieves data from Google Sheets, replaces blank values with "0.00",
    and implements an exponential backoff retry strategy for 503/429 errors.
    """
    # Optional pacing delay to mitigate rate-limiting flags during high-volume batch processing
    if delay > 0:
        time.sleep(delay)
        
    try:
        service = build("sheets", "v4", credentials=creds, cache_discovery=False)
        sheet = service.spreadsheets()
    except Exception as e:
        logging.error("Failed to build Google Sheets service: %s", e)
        return []

    for n in range(max_retries):
        try:
            request = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name)
            result = request.execute()
            
            values = result.get("values", [])
            
            # Replace blank values with "0.00"
            for i, row in enumerate(values):
                for j, value in enumerate(row):
                    if not value:  # Check if the cell value is empty
                        values[i][j] = "0.00"
                        
            return values
            
        except HttpError as error:
            status_code = error.resp.status
            # Trap 429 (Too Many Requests) and 5xx (Server-side Errors including 503)
            if status_code == 429 or status_code >= 500:
                wait_time = (2 ** n) + 1  # Exponential backoff: 2s, 3s, 5s...
                logging.warning(
                    f"API Error {status_code} for range {range_name}. "
                    f"Retrying in {wait_time} seconds (Attempt {n + 1} of {max_retries})..."
                )
                time.sleep(wait_time)
            else:
                # Immediate fail for client errors (e.g., 400 Bad Request, 404 Not Found)
                logging.error("An error occurred: %s", error)
                return []
                
    logging.error(f"Max retries ({max_retries}) exceeded for range {range_name}.")
    return []

if __name__ == "__main__":
    creds = sheet_service()
    data_values = get_data(
        creds, os.getenv("TEST_SPREADSHEET"), os.getenv("TEST_RANGE")
    )
    print(data_values)