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

### Prepare a CSV file with lunar birthday information

The CSV should have the following columns:

- name: Person's name
- year: Lunar year of birth
- month: Lunar month of birth
- day: Lunar day of birth
- is_lunar: Whether the birthday is lunar or not

Example:

```text
name,year,month,day,is_lunar
John Doe,1990,8,15,1
Jane Smith,1985,2,10,0
```

### Run the script

```shell
python lunar_birthdays.py <input_csv> <output_ics> [--years YEARS] [--start-year START_YEAR] [--batch-size BATCH_SIZE]
```

#### Parameters

- `<input_csv>`: Required. The path to the input CSV file containing lunar birthday information.
- `<output_ics_prefix>`: Required. The prefix name for the output ICS file. The generated ICS files will be named based on this prefix and the corresponding year range.
- `--years YEARS`: Optional. The number of years for which to generate events. The default is 50 years.
- `--start-year START_YEAR`: Optional. The starting year for generating events. The default is the current year.
- `--batch-size BATCH_SIZE`: Optional. The number of years included in each ICS file. The default is 50 years. If the years parameter exceeds the batch-size, multiple ICS files will be generated.

Replace `<input_csv>` with the path to your input CSV file and `<output_ics>` with the desired output path for the ICS file. Finally, import the generated ICS file into Google Calendar.

#### Example Usage

- Generate a single ICS file for the default 50 years, starting from the current year:

```shell
python lunar_birthdays.py example.csv lunar-birthdays
```

- Generate ICS files for 100 years, starting from 2025, with each file covering 50 years:

```shell
python lunar_birthdays.py example.csv lunar-birthdays --years 100 --start-year 2025
```

- Generate ICS files from the year 2000 to 2049, with each file covering 10 years:

```shell
python lunar_birthdays.py example.csv lunar-birthdays --years 50 --start-year 2000 --batch-size 10
```
