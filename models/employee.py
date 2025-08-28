# models/employee.py


class Employee:
    """
    Represents an employee with their ID, name, nickname, spreadsheet ID, and team.

    Attributes:
        employee_id (int): The unique identifier for the employee.
        employee_name (str): The full name of the employee.
        employee_nickname (str): The nickname of the employee.
        spreadsheet_id (str): The ID of the spreadsheet associated with the employee.
        team (str): The team the employee belongs to.
    """

    # constructor
    def __init__(
        self, employee_id, employee_name, employee_nickname, spreadsheet_id, team
    ):
        """
        Initializes a new Employee object.

        Args:
            employee_id (int): The unique identifier for the employee.
            employee_name (str): The full name of the employee.
            employee_nickname (str): The nickname of the employee.
            spreadsheet_id (str): The ID of the Google Spreadsheet associated with the employee.
            team (str): The team the employee belongs to.
        """
        self.id = employee_id
        self.name = employee_name
        self.nickname = employee_nickname
        self.spreadsheet_id = spreadsheet_id
        self.team = team
