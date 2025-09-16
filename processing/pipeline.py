import logging
from dataclasses import astuple

from config import settings
from services.google_sheets import GoogleSheetsService
from models.employee import Employee
from processing.transformer import TimesheetTransformer
from utils.date_helper import generate_week_datasets
from utils.excel_exporter import export_to_excel

class DataPipeline:
    """
    Orchestrates the data collection, transformation, and export processes.
    """

    def __init__(self, sheets_service: GoogleSheetsService):
        self.sheets_service = sheets_service
        self.project_data = []
        self.week_datasets: list[dict] = []

    def _setup(self):
        """
        Fetches common data needed for the pipeline run
        """
        logging.info("Pipeline setup: Fetching project and date data...")
        if settings.PROJECT_SPREADSHEET_ID is None:
            raise ValueError("PROJECT_SPREADSHEET_ID must not be None")
        if settings.PROJECT_RANGE is None:
            raise ValueError("PROJECT_RANGE must not be None")
        self.project_data = self.sheets_service.get_data(
            settings.PROJECT_SPREADSHEET_ID, settings.PROJECT_RANGE
        )
        self.week_datasets = generate_week_datasets(
            settings.WEEK_DATASET_START_YEAR,
            settings.WEEK_DATASET_START_MONTH,
            settings.WEEK_DATASET_START_DAY,
        ) # type: ignore
        logging.info("Pipeline setup completed.")

    def _fetch_employees(self, sheet_name: str) -> list[Employee]:
        """
        Fetches employee data from a specified Google Sheet.

        Args:
            sheet_name (str): The name of the sheet to fetch employee data from.

        Returns:
            list[Employee]: A list of Employee objects.
        """
        if settings.EMPLOYEES_SPREADSHEET_ID is None:
            raise ValueError("EMPLOYEES_SPREADSHEET_ID must not be None")
        employee_data = self.sheets_service.get_data(
            settings.EMPLOYEES_SPREADSHEET_ID, f"{sheet_name}!A:E"
        )

        if not employee_data:
            logging.warning(f"No employee data found in sheet: {sheet_name}")
            return []
        
        employees = []
        for row in employee_data:
            if not any(row): continue  # Skip empty rows
            try:
                employees.append(Employee(
                    id=int(row[0]),
                    name=row[1],
                    nickname=row[2],
                    spreadsheet_id=row[4],
                    team=row[3]
                ))
            except (IndexError, ValueError) as e:
                logging.warning(f"Skipping invalid row in employee data: {row}. Error: {e}")
        return employees
    
    def run(self):
        """
        Executes the full data processing pipeline.
        """

        if not self.sheets_service.service:
            logging.critical("Google Sheets service is not initialized. Aborting pipeline.")
            return
        
        self._setup()
        transformer = TimesheetTransformer(
            self.week_datasets,
            self.project_data,
            settings.COLUMNS_TO_DELETE
        )

        for sheet_name in settings.SHEET_NAMES_TO_PROCESS:
            logging.info(f"Processing sheet: {sheet_name}")
            employees = self._fetch_employees(sheet_name)
            final_data_for_sheet = []

            for employee in employees:
                logging.info(f"Processing employee: {employee.nickname}...")
                raw_data = self.sheets_service.get_data(
                    employee.spreadsheet_id,
                    f"{sheet_name}!{settings.TIMESHEET_DATA_RANGE}"
                )
                transformed_entries = transformer.transform(raw_data, employee)
                # Convert list to dataclass objects to a list of tuples for Excel export
                final_data_for_sheet.extend([astuple(entry) for entry in transformed_entries])

                logging.info(f"[{sheet_name}]-[🧑🏽 {employee.nickname.ljust(10)} ] ✅ OK.")

            if final_data_for_sheet:
                export_to_excel(final_data_for_sheet, sheet_name)
            else:
                logging.warning(f"No data to export for sheet: {sheet_name}. Skipping export.")



