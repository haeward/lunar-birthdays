import csv
import sys
from typing import Dict, List, TypedDict, cast

from icalendar import Calendar, Event
from lunarcalendar import Converter, Lunar, DateNotExist
from datetime import datetime, timedelta


class BirthdayRow(TypedDict):
    """
    Represents a row in the CSV file containing birthday information.

    This TypedDict defines the structure of each row in the input CSV file.
    It specifies the expected keys and their corresponding value types.

    Attributes:
        name (str): The name of the person whose birthday is being recorded.
        year (str): The lunar year of birth, stored as a string to preserve leading zeros.
        month (str): The lunar month of birth, stored as a string (1-12 or 01-12).
        day (str): The lunar day of birth, stored as a string (1-31 or 01-31).

    Note:
        Although year, month, and day are typically numeric values, they are defined
        as strings here to match the CSV format and preserve any leading zeros.
        These will be converted to integers when processing the data.
    """
    name: str
    year: str
    month: str
    day: str


def read_lunar_birthdays(file_path: str) -> List[Dict[str, int | str]]:
    """
    Read lunar birthdays from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        List[Dict[str, int | str]]: List of dictionaries containing birthday information.
    """
    birthdays = []
    try:
        with open(file_path, mode='r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                birthday_row = cast(BirthdayRow, row)
                birthdays.append({
                    'name': birthday_row['name'],
                    'year': int(birthday_row['year']),
                    'month': int(birthday_row['month']),
                    'day': int(birthday_row['day']),
                })
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid data in CSV file. {str(e)}")
        sys.exit(1)
    return birthdays


def create_birthday_event(birthday: Dict[str, int | str]) -> Event:
    """
    Create an iCalendar event for a birthday.

    Args:
        birthday (Dict[str, int | str]): Birthday information.

    Returns:
        Event: iCalendar event object.
    """
    # Convert lunar date to solar date
    lunar_date = Lunar(birthday['year'], birthday['month'], birthday['day'], isleap=False)
    solar_date = Converter.Lunar2Solar(lunar_date)

    # Create a new event for the birthday
    event = Event()
    event.add('summary', f"{birthday['name']}'s birthday")
    event.add('dtstart', solar_date.to_date())
    event.add('dtend', solar_date.to_date() + timedelta(days=1))
    event.add('rrule', {'freq': 'yearly'})
    event.add('dtstamp', datetime.now())
    return event


def generate_ics_file(birthdays: List[Dict[str, int | str]], output_file_path: str) -> None:
    """
    Generate an ICS file from a list of lunar birthdays.

    Args:
        birthdays (List[Dict[str, int | str]]): List of birthday information.
        output_file_path (str): Path to save the output ICS file.
    """
    # Create a new calendar
    cal = Calendar()
    cal.add('prodid', '-//Haeward//Lunar Birthdays//CN')
    cal.add('version', '2.0')

    for birthday in birthdays:
        try:
            event = create_birthday_event(birthday)
            cal.add_component(event)
        except DateNotExist:
            print(f"Warning: Invalid lunar date: {birthday['year']}-{birthday['month']}-{birthday['day']}")

    # Write the calendar to an ICS file
    with open(output_file_path, 'wb') as f:
        f.write(cal.to_ical())


def main(input_csv_path: str, output_ics_path: str) -> None:
    """
    Main function to read lunar birthdays and generate an ICS file.

    Args:
        input_csv_path (str): Path to the input CSV file.
        output_ics_path (str): Path to save the output ICS file.
    """
    lunar_birthdays = read_lunar_birthdays(input_csv_path)
    generate_ics_file(lunar_birthdays, output_ics_path)
    print(f"ICS file generated successfully: {output_ics_path}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_csv> <output_ics>")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_ics = sys.argv[2]
    main(input_csv, output_ics)
