import argparse
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


def create_birthday_event(birthday: Dict[str, int | str], year: int) -> Event:
    """
    Create an iCalendar event for a birthday.

    Args:
        birthday (Dict[str, int | str]): Birthday information.
        year (int): The year to convert the lunar date into solar date.

    Returns:
        Event: iCalendar event object.
    """
    # Convert lunar date to solar date
    lunar_date = Lunar(year, birthday['month'], birthday['day'], isleap=False)
    solar_date = Converter.Lunar2Solar(lunar_date)

    # Create a new event for the birthday
    event = Event()
    event.add('summary', f"{birthday['name']}'s birthday", parameters={'CHARSET': 'UTF-8'})
    event.add('dtstart', solar_date.to_date())
    event.add('dtend', solar_date.to_date() + timedelta(days=1))
    # event.add('rrule', {'freq': 'yearly'})
    event.add('dtstamp', datetime.now())
    return event


def generate_ics(birthdays: List[Dict[str, int | str]], output_file_path: str, start_year: int, end_year: int) -> None:
    """
    Generate an ICS file from a list of lunar birthdays.

    Args:
        birthdays (List[Dict[str, int | str]]): List of birthday information.
        output_file_path (str): Path to save the output ICS file.
        start_year (int): The starting year for generating events.
        end_year (int): The ending year for generating events.
    """
    # Create a new calendar
    cal = Calendar()
    cal.add('prodid', '-//Haeward//Lunar Birthdays//CN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('charset', 'UTF-8')

    for birthday in birthdays:
        for year in range(start_year, end_year + 1):
            try:
                event = create_birthday_event(birthday, year)
                cal.add_component(event)
            except DateNotExist:
                print(f"Warning: Invalid lunar date: {birthday['year']}-{birthday['month']}-{birthday['day']}")

    # Write the calendar to an ICS file
    with open(output_file_path, 'wb') as f:
        f.write(cal.to_ical())


def main():
    current_year = datetime.now().year
    parser = argparse.ArgumentParser(description="Generate ICS files for lunar birthdays.")
    parser.add_argument('input_csv', help="Path to the input CSV file containing lunar birthdays.")
    parser.add_argument('output_ics_prefix', help="Prefix for the output ICS files.")
    parser.add_argument('--years', type=int, default=50,help="Number of years to generate (default: 50).")
    parser.add_argument('--start-year', type=int, default=current_year,
                        help="Start year for generating events (default: current year).")
    parser.add_argument('--batch-size', type=int, default=50, help="Number of years per ICS file (default: 50).")

    args = parser.parse_args()

    lunar_birthdays = read_lunar_birthdays(args.input_csv)

    for year in range(args.start_year, args.start_year + args.years, args.batch_size):
        end_year = min(year + args.batch_size - 1, args.start_year + args.years - 1)
        if year == end_year:
            output_file_path = f"{args.output_ics_prefix}_{year}.ics"
        else:
            output_file_path = f"{args.output_ics_prefix}_{year}-{end_year}.ics"
        generate_ics(lunar_birthdays, output_file_path, year, end_year)
        print(f"ICS file generated successfully: {output_file_path}")


if __name__ == '__main__':
    main()
