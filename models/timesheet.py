from dataclasses import dataclass

@dataclass
class TimesheetEntry:
    """
    Represents a single row in the final excel export.
    """
    client: str
    row_number: int
    year: int
    month: int
    day: int
    week_type: str
    employee_name: str
    project_code: str
    task_type: str
    work_type: str
    employee_team: str
    worked_hours: float