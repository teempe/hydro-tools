import pandas as pd


DATE_COLUMNS = ["COROKH", "COMSCH", "CODZIEN", "COMSCK"]
OBSERVATION_KEY = ["PSKDSZS", "COROKH", "COMSCK", "CODZIEN"]
OBSERVATION_COLUMNS = ["COSTAN", "COPRZP", "COPTMP"]
FLOW_OBSERVATION_COLUMN = "COPRZP"


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


def find_duplicate_observations(df: pd.DataFrame) -> pd.Series:
    """
    Identify duplicate IMGW observations for the same station and date.

    A row is considered a duplicate if another row has the same station code,
    hydrological year, calendar month, and day. Measurement values are not
    considered when identifying duplicate observations.

    Parameters
    ----------
    df : pandas.DataFrame
        Data containing the IMGW observation key columns ``PSKDSZS``,
        ``COROKH``, ``COMSCK``, and ``CODZIEN``.

    Returns
    -------
    pandas.Series
        Boolean mask aligned with ``df.index``. ``True`` indicates a duplicate
        observation and ``False`` a unique observation.

    Raises
    ------
    KeyError
        If any required observation key column is missing from the DataFrame.
    """
    
    missing_columns = [column for column in OBSERVATION_KEY if column not in df.columns]
    if missing_columns:
        raise KeyError(f"Required columns are missing: {', '.join(missing_columns)}")

    is_duplicate = df.duplicated(subset=OBSERVATION_KEY, keep=False)
    has_na_key = df[OBSERVATION_KEY].isna().any(axis=1)
    is_duplicate[has_na_key] = False

    return is_duplicate


def find_missing_observations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify missing IMGW measurement observations.

    A measurement is considered missing if its value is missing in any of the
    IMGW measurement columns ``COSTAN``, ``COPRZP``, or ``COPTMP``.

    Parameters
    ----------
    df : pandas.DataFrame
        Data containing the IMGW measurement columns ``COSTAN``, ``COPRZP``,
        and ``COPTMP``.

    Returns
    -------
    pandas.DataFrame
        Boolean DataFrame aligned with ``df.index`` and containing the
        measurement columns ``COSTAN``, ``COPRZP``, and ``COPTMP``.
        ``True`` indicates a missing observation and ``False`` a present
        observation.

    Raises
    ------
    KeyError
        If any required measurement column is missing from the DataFrame.
    """

    missing_columns = [column for column in OBSERVATION_COLUMNS if column not in df.columns]
    if missing_columns:
        raise KeyError(f"Required columns are missing: {', '.join(missing_columns)}")

    return df[OBSERVATION_COLUMNS].isna()


def find_negative_flows(df: pd.DataFrame) -> pd.Series:
    """
    Identify IMGW observations with negative flow values.

    A flow observation is considered invalid if the value in ``COPRZP`` is
    less than zero. Missing flow observations are not considered negative.

    Parameters
    ----------
    df : pandas.DataFrame
        Data containing the IMGW flow measurement column ``COPRZP``.

    Returns
    -------
    pandas.Series
        Boolean mask aligned with ``df.index``. ``True`` indicates a negative
        flow value and ``False`` a non-negative or missing flow value.

    Raises
    ------
    KeyError
        If the required ``COPRZP`` column is missing from the DataFrame.
    """

    if FLOW_OBSERVATION_COLUMN not in df.columns:
        raise KeyError(f"Required column is missing: {FLOW_OBSERVATION_COLUMN}")

    result = df[FLOW_OBSERVATION_COLUMN] < 0
    result = result.fillna(False)
    result = result.astype(bool)
    result.name = None

    return result


def validation_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize IMGW data validation results.

    The summary includes missing measurement counts and percentages for
    ``COSTAN``, ``COPRZP``, and ``COPTMP``, as well as counts and percentages
    of invalid dates, duplicate observations, and negative flow values.

    Parameters
    ----------
    df : pandas.DataFrame
        Data containing the IMGW date, observation key, and measurement
        columns required by the validation functions.

    Returns
    -------
    pandas.DataFrame
        Validation summary containing ``category``, ``check``, ``count``,
        and ``percent`` columns.

    Raises
    ------
    KeyError
        If any column required by the underlying validation checks is missing.
    """

    missing = find_missing_observations(df)
    invalid_dates = find_invalid_dates(df)
    duplicates = find_duplicate_observations(df)
    negative_flows = find_negative_flows(df)

    rows = [
        ["missing", "COSTAN", missing["COSTAN"].sum()],
        ["missing", "COPRZP", missing["COPRZP"].sum()],
        ["missing", "COPTMP", missing["COPTMP"].sum()],
        ["issues", "invalid_dates", invalid_dates.sum()],
        ["issues", "duplicate_observations", duplicates.sum()],
        ["issues", "negative_flows", negative_flows.sum()]
    ]

    summary = pd.DataFrame(
        rows,
        columns = ["category", "check", "count"]
    )

    total_rows = len(df)
    summary["percent"] = summary["count"] / total_rows * 100
    
    return summary
