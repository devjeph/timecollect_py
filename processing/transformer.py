from models.employee import Employee
from models.timesheet import TimesheetEntry
from utils.date_helper import get_week_type_for_date

class TimesheetTransformer:
    """
    Transforms raw employee timesheet data into a structured format.
    """

    def __init__(self, week_datasets: list[dict], project_data: list[list[str]], columns_to_delete: list[int]):
        self.week_datasets = week_datasets
        # Create a fast lookup dictionary for project clients
        self.project_lookup = {proj[0]: proj[2] for proj in project_data if len(proj) > 3}
        self.columns_to_delete = sorted(columns_to_delete, reverse=True)

    def _delete_columns(self, data: list[list[str]]) -> list[list[str]]:
        """
        Deletes specified columns safely from each row.
        """
        for row in data:
            for col_index in self.columns_to_delete:
                if col_index < len(row):
                    del row[col_index]
        return data
    
    def _get_client(self, project_code: str) -> str:
        """
        Retrieves the client name for a given project code.
        """
        return self.project_lookup.get(project_code, "YTP")
    
    def transform(self, raw_data: list[list[str]], employee: Employee) -> list[TimesheetEntry]:
        """
        The main transformation function that processes raw timesheet data.
        """
        if not raw_data or len(raw_data) < 3:
            return []
        
        cleaned_data = self._delete_columns(raw_data)

        # Your original transformation logic, now clearer
        cleaned_data[1][:9] = cleaned_data[0][:9]
        work_data = ["日付"] * 3 + ["間接"] * 8 + ["直接"] * 40

        for i in range(3):
            for j in [12, 16, 20, 24,28,32,36,40,44,48]:
                if j - 1 < len(cleaned_data[0]) and i + j < len(cleaned_data[0]):
                    cleaned_data[0][i + j] = cleaned_data[0][j - 1]

        transformed_entries = []
        for row_idx, row_values in enumerate(cleaned_data[2:], start=1):
            try:
                year, month, day = int(row_values[0]), int(row_values[1]), int(row_values[2])
                week_type = get_week_type_for_date(self.week_datasets, year, month, day)
            except (ValueError, IndexError):
                continue

            for col_idx in range(3, len(row_values)):
                try:
                    worked_hours = float(row_values[col_idx])
                    if worked_hours == 0.0:
                        continue

                    project_code = str(cleaned_data[0][col_idx])
                    entry = TimesheetEntry(
                        client=self._get_client(project_code),
                        row_number=row_idx,
                        year=year,
                        month=month,
                        day=day,
                        week_type=str(week_type),
                        employee_name=employee.nickname,
                        project_code=project_code,
                        task_type=str(cleaned_data[1][col_idx]),
                        work_type=str(work_data[col_idx]),
                        employee_team=employee.team,
                        worked_hours=worked_hours
                    )
                    transformed_entries.append(entry)
                except (ValueError, IndexError):
                    continue
        return transformed_entries