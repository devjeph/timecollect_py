""" app.py """

import os
import datetime as dt

if os.path.exists("./logs/main_app.log"):
    os.remove("./logs/main_app.log")

import logging
from api_services.google_api import sheet_service
from utils.data_collection import get_data
from utils.transform_data import transform_data
from utils.get_week_types import set_types
from utils.excel import export

from models.employee import Employee
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    """function that will connect to Google Sheet API"""
    creds = sheet_service()

    # Dynamically pull the start date for the timesheet year from .env
    start_year = int(os.getenv("TIMESHEET_START_YEAR", 2025))
    start_month = int(os.getenv("TIMESHEET_START_MONTH", 12))
    start_day = int(os.getenv("TIMESHEET_START_DAY", 28))

    datasets = set_types(start_year, start_month, start_day)

    # Calculate the most recent Saturday relative to today
    today = dt.date.today()
    days_since_saturday = (today.weekday() - 5) % 7
    last_saturday = today - dt.timedelta(days=days_since_saturday)

    if creds:
        logging.info("🌐 Connected to Google API.")

        project_data = get_data(
            creds, 
            os.getenv("PROJECT_SPREADSHEET"), 
            os.getenv("PROJECT_RANGE")
        )

        # --- Fetch and parse Holiday DB ---
        holiday_raw_data = get_data(
            creds,
            os.getenv("PROJECT_SPREADSHEET"), 
            "holidayDB!A:A"
        )

        # Construct an O(1) lookup set for holiday exclusions
        holidays = set()
        for row in holiday_raw_data:
            if row and row[0]:
                try:
                    # Parse YYYY/MM/DD format
                    date_parts = str(row[0]).strip().split('/')
                    if len(date_parts) == 3:
                        h_year, h_month, h_day = map(int, date_parts)
                        holidays.add(dt.date(h_year, h_month, h_day))
                except ValueError:
                    # Bypass headers or malformed date strings
                    pass

        logging.info("📝 Timesheet collection started...")

        # Safe parsing of sheet names with fallback and whitespace stripping
        raw_sheets = os.getenv("SHEET_NAMES","")
        sheet_names = [s.strip() for s in raw_sheets.split(",") if s.strip()]

        for sheet_name in sheet_names:
            employees = []
            excel_sheet = []
            employee_data = get_data(
                creds, 
                os.getenv("EMPLOYEES_SPREADSHEET"), 
                f"{sheet_name}!A:E"
            )
            if not employee_data:
                logging.error("No employee data collected.")

            for employee in employee_data:
                if employee:
                    employee_object = Employee(
                        int(employee[0]),
                        employee[1],
                        employee[2],
                        employee[4],
                        employee[3],
                    )
                    employees.append(employee_object)

            logging.info(f"Collecting timesheet [{sheet_name}] data")

            for employee in employees:
                data = get_data(creds, employee.spreadsheet_id, f"{sheet_name}!A7:BU39")

                # --- Validate Column M (excluding weekends, future dates, and holidays) ---
                for row_idx, row in enumerate(data):
                    if len(row) > 12:
                        try:
                            row_year = int(row[0])
                            row_month = int(row[1])
                            row_day = int(row[2])
                            row_date = dt.date(row_year, row_month, row_day)
                        except (ValueError, IndexError, TypeError):
                            continue
                            
                        # Filter out dates past the most recent Saturday
                        if row_date > last_saturday:
                            continue

                        # Bypass the check if the date intersects with a known holiday
                        if row_date in holidays:
                            continue

                        # Check Column D (index 3) for the day of the week
                        day_of_week = str(row[3]).strip() if len(row) > 3 else ""
                        if day_of_week in ["土", "日"]:
                            continue
                            
                        val_str = row[12]
                        try:
                            val_float = float(val_str) if val_str and val_str != "0.00" else 0.0
                            if val_float < 8.0:
                                logging.warning(
                                    f"ALERT [{sheet_name}] - Employee: {employee.nickname} | "
                                    f"Date: {row_date} | Column M value ({val_float}) < 8.0 on a regular workday."
                                )
                        except ValueError:
                            pass
                # --------------------------------------------------------------------------

                transformed_data = transform_data(
                    datasets, data, employee, project_data
                )

                excel_sheet += transformed_data
                
                logging.info(
                    f"[{sheet_name}]-[ {'*' * (15-len(employee.nickname))} {employee.nickname} ] ✅ Data Processed."
                )

            export(excel_sheet, sheet_name)



if __name__ == "__main__":
    main()
