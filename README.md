# hydro-tools

Python tools for reading and processing hydrological data published by [IMGW-PIB](https://danepubliczne.imgw.pl/) (the Polish Institute of Meteorology and Water Management).

The reader currently targets the IMGW-PIB hydrological data format. Hydrological date conversion can also be used with custom column names.

> **Status:** early development (0.2.0). Reading and parsing IMGW hydrological CSV files and hydrological-to-calendar date conversion are implemented and covered by automated tests. Data validation, completeness checks and multi-year workflows are planned.

## Features

Currently implemented:

- reading standard IMGW hydrological CSV files
- automatic character encoding detection
- automatic CSV delimiter detection
- support for nested IMGW CSV files
- assignment of IMGW column names
- extraction of river/lake codes from water-body names
- conversion of numeric IMGW columns
- hydrological-year to calendar-date conversion

Planned:

- data validation
- handling missing-value and sentinel conventions
- completeness checks
- multi-year workflows

## Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/teempe/hydro-tools.git
cd hydro-tools
pip install -e .
```

For development, including the test suite:

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

The returned DataFrame uses IMGW column names, extracts the river/lake code into `KDKRZK`, and converts numeric IMGW columns to numeric types.

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

## Development

Run the test suite with [pytest](https://docs.pytest.org/):

```bash
pytest
```

## Requirements

- Python >= 3.10
- pandas >= 2.0
- charset-normalizer >= 3.0

Development dependencies additionally include:

- pytest >= 7.0
- pytest-mock >= 3.0

## License

[MIT](LICENSE)
