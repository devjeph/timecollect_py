# utils/get_week_types.py

import datetime as dt

days_of_week = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def get_name(datasets, year, month, day):
    """
    Determines the "Week Type" for a given date based on a list of date ranges.

    Args:
      datasets: A list of dictionaries, where each dictionary has keys
                "Start Date", "End Date", and "Week Type".
      _year: The year of the target date.
      _month: The month of the target date.
      _day: The day of the target date.

    Returns:
      The "Week Type" string corresponding to the target date, or the
      "Week Type" of the last date range in the datasets if no match is found.
    """
    target_date = dt.date(year, month, day)
    for index, data in enumerate(datasets):
        start_date = data["Start Date"]
        end_date = data["End Date"]

        # Check if the target date falls within the current date range
        if start_date <= target_date <= end_date:
            return datasets[index]["Week Type"]

    # If no matching date range is found, return none
    return None


def set_types(year, month, day):
    """
    Generates a list of datasets with start dates, end dates, week numbers, and week types.

    This function appears to rely on another function called `set_dates` (not defined here)
    to generate the necessary date information. It then structures this information into
    a list of dictionaries.

    Args:
      year: The year for generating the dates.
      month: The month for generating the dates.
      day: The day for generating the dates.

    Returns:
        A list of dictionaries, where each dictionary represents a dataset with the following keys:
        "Start Date": The start date of the period (presumably a datetime.date object).
        "End Date": The end date of the period (presumably a datetime.date object).
        "Week Number": The week number within the specified period.
        "Week Type":  A type associated with the week (e.g., "A", "B", "C").

    Note: This documentation assumes the existence of a function `set_dates` that returns
          a tuple of four lists: start dates, end dates, week numbers, and week types.
    """
    dates = set_dates(year, month, day)

    datasets = [
        {
            "Start Date": start,
            "End Date": end,
            "Week Number": week,
            "Week Type": type,
        }
        for start, end, week, type in zip(dates[0], dates[1], dates[2], dates[3])
    ]

    return datasets


def set_name(start_date, end_date):
    """
    Generates week names in a specific format based on start and end dates.

    The week names are generated using a combination of month numbers and letters,
    with special handling for cases where the start and end dates fall in different months or years.

    Args:
      start_date: The start date of the week (datetime.date object).
      end_date: The end date of the week (datetime.date object).

    Returns:
      A string representing the week name in the defined format.
      Returns "Invalid date" if a ValueError occurs during processing.

    Example:
      If start_date is January 1st and end_date is January 7th, the function
      would return "1B" (assuming the year is not relevant in this example).

    Week Name Generation Logic:
      - Generally uses the start month and a letter (A, B, C, etc.) based on the
        start date's day within the month.
      - If the start and end dates are in different months and years, it uses the
        end month and the letter 'A'.
      - If the start month is January, it adjusts the letter assignment.
      - If the start and end dates are in different months but the same year, it uses
        a format like "1to2" (for January to February).
      - If the start and end dates fall within the same week, it uses the standard
        month and letter format.
    """
    try:
        start_week = start_date.isocalendar().week
        end_week = end_date.isocalendar().week
        start_month = start_date.month
        end_month = end_date.month

        week_name = f"{start_month}{chr(ord('A') + (start_date.day - 1) // 7)}"

        if (start_month != end_month) and (start_date.year != end_date.year):
            week_name = f"{end_month}{chr(ord('A'))}"

        if start_month == 1:
            week_name = f"{start_month}{chr(ord('B') + (start_date.day - 1) // 7)}"

        if (start_month != end_month) and (start_date.year == end_date.year):
            week_name = f"{start_month}to{end_month}"

        if start_week == end_week:
            week_name = f"{start_month}{chr(ord('A') + (start_date.day - 1) // 7)}"

        return week_name
    except ValueError:
        return "Invalid date"


def set_dates(year, month, day):
    """
    Calculates the dates of Sundays and Saturdays for two years, starting from a given date.

    Args:
      year: The year of the starting date.
      month: The month of the starting date.
      day: The day of the starting date.

    Returns:
      A list containing three lists: Sundays, Saturdays, and corresponding week indices.
      Returns an empty list if the input date is not a Sunday.
    """
    sundays = []
    saturdays = []
    week_indices = []
    week_names = []

    start_date = dt.date(year, month, day)
    what_day = days_of_week[start_date.weekday()]

    # Validate if the input date is a Sunday
    if what_day != "Sunday":
        print(f"Date must be a Sunday. You inputted a {what_day}.")
        return []

    for week_index in range(104):
        sunday = start_date + dt.timedelta(days=(week_index * 7))
        saturday = sunday + dt.timedelta(days=6)

        week_type = set_name(sunday, saturday)

        if sunday.year >= year + 2:
            break

        sundays.append(sunday)
        saturdays.append(saturday)
        week_indices.append(week_index + 1)
        week_names.append(week_type)

    week_names[-1] = "12to1"
    return [sundays, saturdays, week_indices, week_names]


if __name__ == "__main__":
    datasets = set_types(2023, 12, 31)
    week_type = get_name(datasets, 2024, 11, 23)
    print(week_type)
