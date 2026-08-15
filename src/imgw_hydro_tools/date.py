from typing import Literal
import pandas as pd


def hydro_to_calendar_date(df: pd.DataFrame,
                           *,
                           hydro_year_col: str = "MCROKH", 
                           month_col: str = "MCMSCK", 
                           day_col: str = "MCDZIK", 
                           errors: Literal["raise", "coerce"] = "raise") -> pd.Series:
    """Convert hydrological-year date columns into calendar dates.
 
    In the Polish hydrological calendar the year starts on 1 November, so
    November and December of hydrological year *Y* fall in calendar year
    *Y - 1*. This function applies that rule and builds a proper datetime
    for each row.
 
    The year, month and day columns are expected to contain numeric date 
    components.

    The default column names (``MCROKH``, ``MCMSCK``, ``MCDZIK``) follow the
    official IMGW-PIB data format for hydrological monthly observations, so the
    function works out of the box on raw IMGW data. Pass the corresponding
    arguments to use it with differently named columns.
 
    Parameters
    ----------
    df : pandas.DataFrame
        Input data containing the year, month and day columns.
    hydro_year_col : str, default "MCROKH"
        Name of the column holding the hydrological year.
    month_col : str, default "MCMSCK"
        Name of the column holding the calendar month (1-12).
    day_col : str, default "MCDZIK"
        Name of the column holding the calendar day.
    errors : {"raise", "coerce"}, default "raise"
        Passed through to :func:`pandas.to_datetime`. With ``"coerce"``,
        unparseable dates become ``NaT``; with ``"raise"`` they raise.
 
    Returns
    -------
    pandas.Series
        Series of calendar dates (``datetime64``). Rows that cannot be converted are ``NaT`` when
        ``errors="coerce"``.
 
    Raises
    ------
    KeyError
        If any of the required columns is missing from ``df``.
    ValueError
        If the date components cannot be converted to a valid calendar date and ``errors="raise"``.
 
    Examples
    --------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"MCROKH": [2024], "MCMSCK": [11], "MCDZIK": [1]})
    >>> hydro_to_calendar_date(df).iloc[0]
    Timestamp('2023-11-01 00:00:00')
    """

    required = [hydro_year_col, month_col, day_col]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns: {', '.join(missing)}")

    calendar_year = df[hydro_year_col].where(df[month_col] <= 10, df[hydro_year_col]-1)

    return pd.to_datetime(
        {
            "year": calendar_year,
            "month": df[month_col],
            "day": df[day_col]
        },
        errors=errors
    )
