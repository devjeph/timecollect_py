import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
CREDENTIALS_DIR = os.path.join(BASE_DIR, 'google_credentials')

# File paths
LOG_FILE_PATH = os.path.join(LOGS_DIR, 'main_app.log')
TOKEN_PATH = os.path.join(CREDENTIALS_DIR, 'token.json')
CREDENTIALS_PATH = os.path.join(CREDENTIALS_DIR, 'credentials.json')
EXCEL_OUTPUT_PATH = os.path.join('D:\Documents\TimeCollect\2025\TimeCollect_2.0.xlsx')

# Google API
SCOPES = [os.getenv("SCOPES")]
PROJECT_SPREADSHEET_ID = os.getenv("PROJECT_SPREADSHEET_ID")
PROJECT_RANGE = os.getenv("PROJECT_RANGE")
EMPLOYEES_SPREADSHEET_ID = os.getenv("EMPLOYEES_SPREADSHEET_2025")

# Data Processing
SHEET_NAMES_TO_PROCESS = ["202509", "202510"]
TIMESHEET_DATA_RANGE = "A7:BT39"

COLUMNS_TO_DELETE = [
    3,4,5,6,7,8,9,10,11,12,21,26,31,36,41,46,51,56,61,66,71
]

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}