""" app.py """

import os

if os.path.exists("./logs/main_app.log"):
    os.remove("./logs/main_app.log")

import logging
from api_services.google_api import sheet_service
from utils.data_collection import get_data
from utils.transform_data import transform_data
from utils.get_week_types import set_types

from models.employee import Employee
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    filename="./logs/main_app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    """function that will connect to Google Sheet API"""
    creds = sheet_service()
    datasets = set_types(2023, 12, 31)

    if creds:
        employees = []

        sheet_names = ["202411", "202412"]

        for sheet_name in sheet_names:
            employee_data = get_data(
                creds, os.getenv("EMPLOYEES_SPREADSHEET"), f"{sheet_name}!A:E"
            )
            if not employee_data:
                logging.error("No employee data collected.")

            for employee in employee_data:
                if employee:
                    object = Employee(
                        int(employee[0]),
                        employee[1],
                        employee[2],
                        employee[4],
                        employee[3],
                    )
                    employees.append(object)

            logging.info(f"Collecting timesheet [{sheet_name}] data")

            for employee in employees:
                logging.info(
                    f"Collecting timesheet [{sheet_name}]-[{employee.nickname}] data"
                )
                data = get_data(creds, employee.spreadsheet_id, f"{sheet_name}!A7:AT39")
                transformed_data = transform_data(datasets, data, employee)
                print(len(transformed_data))


if __name__ == "__main__":
    main()
