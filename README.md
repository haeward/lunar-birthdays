# Lunar Birthdays

Lunar Birthdays is a Python tool that converts lunar calendar birthdays to the solar calendar and generates ICS files for easy import into Google Calendar.

## Features

- Convert lunar calendar birthdays to solar calendar dates
- Generate ICS files compatible with most calendar applications
- Handle recurring yearly events

## Dependencies

- [icalendar](https://github.com/collective/icalendar)
- [LunarCalendar](https://github.com/wolfhong/LunarCalendar)

## Installation

### Clone the repository

```shell
git clone https://github.com/haeward/lunar-birthdays.git
cd lunar-birthdays
```

### Install the required dependencies

```shell
pip install -r requirements.txt
```

## Usage

Prepare a CSV file with lunar birthday information. The CSV should have the following columns:

- name: Person's name
- year: Lunar year of birth
- month: Lunar month of birth
- day: Lunar day of birth

Example:

```text
name,year,month,day
John Doe,1990,8,15
Jane Smith,1985,2,10
```

Run the script:

```shell
python main.py <input_csv> <output_ics>
```

Replace `<input_csv>` with the path to your input CSV file and `<output_ics>` with the desired output path for the ICS file.

Import the generated ICS file into Google Calendar.

Example:

```shell
python main.py example.csv example.ics
```

This command will read lunar birthdays from `example.csv` and generate an ICS file named `example.ics`.
