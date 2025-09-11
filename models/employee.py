from dataclasses import dataclass

@dataclass(frozen=True)
class Employee:
    """
    Represents an employee.
    'frozen=True' makes instances of this class immutable.
    """
    id: int
    name: str
    nickname: str
    spreadsheet_id: str
    team: str