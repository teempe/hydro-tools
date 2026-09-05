import pandas as pd


DATE_COLUMNS = ["COROKH", "COMSCH", "CODZIEN", "COMSCK"]


def find_invalid_dates(df: pd.DataFrame) -> pd.Series:
    """
    Identify rows with invalid or inconsistent IMGW date components.

    A row is considered invalid if any required date component is missing,
    outside its valid range, inconsistent between the hydrological and
    calendar month, or does not represent a valid calendar date.

    Parameters
    ----------
    df : pandas.DataFrame
        Data containing the IMGW date columns ``COROKH``, ``COMSCH``,
        ``COMSCK``, and ``CODZIEN``.

    Returns
    -------
    pandas.Series
        Boolean mask aligned with ``df.index``. ``True`` indicates an
        invalid date and ``False`` a valid date.

    Raises
    ------
    KeyError
        If any required date column is missing from the DataFrame.
    """

    missing_columns = [column for column in DATE_COLUMNS if column not in df.columns]
    if missing_columns:
        raise KeyError(f"Required columns are missing: {', '.join(missing_columns)}")

    df = df[DATE_COLUMNS].copy()
    df.fillna(0, inplace=True)

    is_invalid = pd.Series(False, index=df.index, dtype="bool")

    is_invalid_comsch = (df["COMSCH"] < 1) | (df["COMSCH"] > 12)

    dtime = pd.to_datetime(
        {
            "year": df["COROKH"], 
            "month": df["COMSCK"], 
            "day": df["CODZIEN"]
        },
        errors="coerce"
    )
    is_invalid_date = dtime.isna()

    expected_calendar_month = df["COMSCH"].apply(
        lambda item: item + 10 if item <= 2 else item - 2
    )
    is_misaligned = expected_calendar_month != df["COMSCK"]

    is_invalid[is_invalid_comsch | is_invalid_date | is_misaligned] = True

    return is_invalid
