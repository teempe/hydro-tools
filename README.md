# hydro-tools

Python tools for parsing, cleaning and validating hydrological data published by [IMGW-PIB](https://danepubliczne.imgw.pl/) (the Polish Institute of Meteorology and Water Management).

The tools use IMGW-PIB column names by default, while allowing custom column mappings for other datasets.

> **Status:** early development (0.1). The first building block — hydrological-to-calendar date conversion — is in place and covered by automated tests. Parsing, completeness checks and multi-year statistics are planned.

## Installation

Clone the repository and install in editable mode:

```bash
git clone https://github.com/teempe/hydro-tools.git
cd hydro-tools
pip install -e .
```

For development (including the test suite):

```bash
pip install -e ".[dev]"
```

## Quick start

Convert hydrological-year date columns into calendar dates. In the Polish hydrological calendar the year starts on 1 November, so November and December of hydrological year *Y* fall in calendar year *Y − 1* — the function handles this rule automatically.

```python
import pandas as pd
from imgw_hydro_tools.date import hydro_to_calendar_date

df = pd.DataFrame({
    "MCROKH": [2024, 2024, 2024],   # hydrological year
    "MCMSCK": [10, 11, 1],          # calendar month
    "MCDZIK": [31, 1, 15],          # calendar day
})

df["date"] = hydro_to_calendar_date(df)
print(df["date"].tolist())
# [Timestamp('2024-10-31'), Timestamp('2023-11-01'), Timestamp('2024-01-15')]
```

The default column names (`MCROKH`, `MCMSCK`, `MCDZIK`) follow the IMGW-PIB format. For other data, pass the column names explicitly:

```python
hydro_to_calendar_date(df, hydro_year_col="year", month_col="month", day_col="day")
```

## Development

Run the test suite with [pytest](https://docs.pytest.org/):

```bash
pytest
```

## Requirements

Python ≥ 3.10 · pandas

## License

[MIT](LICENSE)
