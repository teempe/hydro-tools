# hydro-tools

Python tools for reading, processing, and validating hydrological data published by [IMGW-PIB](https://danepubliczne.imgw.pl/) (the Polish Institute of Meteorology and Water Management).

The reader currently targets the IMGW-PIB hydrological data format. Hydrological date conversion can also be used with custom column names.

> **Status:** early development (0.3.0). Reading and parsing IMGW hydrological CSV files, hydrological-to-calendar date conversion, and basic data validation are implemented and covered by automated tests.

## Features

Currently implemented:

- reading standard IMGW hydrological CSV files
- automatic character encoding detection
- automatic CSV delimiter detection
- support for nested IMGW CSV files
- assignment of IMGW column names
- extraction of river/lake codes from water-body names
- conversion of numeric IMGW columns
- normalization of IMGW missing-value and sentinel conventions
- hydrological-year to calendar-date conversion
- validation of invalid or inconsistent date components
- detection of duplicate station/date observations
- detection of missing measurement observations
- detection of negative flow values
- structured validation summary with issue counts and percentages

Planned:

- multi-year workflows
- CLI validation and inspection commands
- formatted quality reports

## Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/teempe/hydro-tools.git
cd hydro-tools
pip install -e .
```

For development, including the test suite and coverage tools:

```bash
pip install -e ".[dev]"
```

## Quick start

### Reading IMGW data

```python
from imgw_hydro_tools.reader import read_imgw_data

df = read_imgw_data("data/codz_2024.csv")

print(df.head())
```

The reader automatically detects the file encoding and CSV delimiter. An encoding can also be supplied explicitly:

```python
df = read_imgw_data(
    "data/codz_2024.csv",
    encoding="cp1250",
)
```

The returned DataFrame uses IMGW column names, extracts the river/lake code into `KDKRZK`, converts numeric IMGW columns to numeric types, and normalizes known IMGW missing-value conventions.

### Converting hydrological dates

In the Polish hydrological calendar, the year starts on 1 November. November and December of hydrological year *Y* therefore fall in calendar year *Y - 1*.

```python
from imgw_hydro_tools.date import hydro_to_calendar_date

df["date"] = hydro_to_calendar_date(df)
```

By default, the function uses the IMGW columns:

- `COROKH` — hydrological year
- `COMSCK` — calendar month
- `CODZIEN` — calendar day

Custom column names can also be supplied:

```python
df["date"] = hydro_to_calendar_date(
    df,
    hydro_year_col="hydro_year",
    month_col="month",
    day_col="day",
)
```

### Validating IMGW data

The validation module provides focused checks that return boolean masks or DataFrames aligned with the input data:

```python
from imgw_hydro_tools.validation import (
    find_duplicate_observations,
    find_invalid_dates,
    find_missing_observations,
    find_negative_flows,
    validation_summary,
)

invalid_dates = find_invalid_dates(df)
duplicates = find_duplicate_observations(df)
missing = find_missing_observations(df)
negative_flows = find_negative_flows(df)
```

A structured summary combines the validation results into counts and percentages:

```python
summary = validation_summary(df)

print(summary)
```

The summary reports missing values for `COSTAN`, `COPRZP`, and `COPTMP`, together with counts of invalid dates, duplicate observations, and negative flow values.

## Development

Run the complete test suite with [pytest](https://docs.pytest.org/):

```bash
pytest
```

Run the test suite with coverage:

```bash
pytest --cov=imgw_hydro_tools --cov-report=term-missing
```

## Requirements

- Python >= 3.10
- pandas >= 2.0
- charset-normalizer >= 3.0

Development dependencies additionally include:

- pytest >= 7.0
- pytest-mock >= 3.0
- pytest-cov >= 5.0

## License

[MIT](LICENSE)
