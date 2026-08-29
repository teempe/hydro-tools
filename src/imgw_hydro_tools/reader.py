import csv
from pathlib import Path
from io import StringIO

import pandas as pd
from charset_normalizer import from_bytes


IMGW_COLUMNS = ["PSKDSZS", "PSNZWP", "KDNRZK", "COROKH", "COMSCH", "CODZIEN", "COSTAN", "COPRZP", "COPTMP", "COMSCK"]
STRING_COLUMNS = ["PSKDSZS", "PSNZWP", "KDNRZK", "KDKRZK"]
INT_COLUMNS = ["COROKH", "COMSCH", "CODZIEN", "COMSCK"]
FLOAT_COLUMNS = ["COSTAN", "COPRZP", "COPTMP"]


def _get_file_encoding(path: str | Path) -> str:
    """Detect a file's character encoding. Raises ValueError if undetectable."""
    
    with Path(path).open("rb") as f:
        charset = from_bytes(f.read()).best()
    if charset is None:
        raise ValueError(f"Could not detect charset for {path}")
    return charset.encoding


def _get_csv_delimiter(path: str | Path, encoding: str) -> str:
    """Detect a file's dialect. Returns delimiter. Raises ValueError if the dialect cannot be determined."""
    
    with Path(path).open("r", encoding=encoding) as f:
        try:
            dialect = csv.Sniffer().sniff(f.read(1024))
        except csv.Error as e:
            raise ValueError(f"Could not detect dialect for {path}") from e
    return dialect.delimiter


def _read_raw_data(path: str | Path, encoding: str, delimiter: str) -> pd.DataFrame:
    """Reads raw data from csv file. Returns dataframe of strings."""
    
    return pd.read_csv(path, encoding=encoding, delimiter=delimiter, header=None, dtype="string", keep_default_na=False)


def _parse_nested_csv(path: str | Path, encoding: str) -> pd.DataFrame:
    """Parse the nested IMGW CSV format into a DataFrame of strings."""
    
    rows = []
    with Path(path).open("r", encoding=encoding, newline="") as input_file:
        input_reader = csv.reader(input_file)
        for line in input_reader:
            parsed_rows = next(csv.reader(StringIO(line[0]), delimiter=","))
            rows.append(parsed_rows)
        
    return pd.DataFrame(rows, dtype="string")


def _set_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Assign column names to the DataFrame. Uses the default IMGW column codes."""
    
    df_tmp = df.copy()
    df_tmp.columns = IMGW_COLUMNS
    return df_tmp


def _extract_river_code(df: pd.DataFrame) -> pd.DataFrame:
    """Extract a numeric code in trailing parentheses into KDKRZK. Names without a code are left unchanged"""
    
    df_tmp = df.copy()
    df_tmp["KDKRZK"] = df_tmp["KDNRZK"].str.extract(r"\((\d+)\)$", expand=False)
    df_tmp["KDNRZK"] = df_tmp["KDNRZK"].str.replace(r"\((\d+)\)$", "", regex=True).str.strip()
    return df_tmp


def _convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert numeric IMGW columns to numbers. Non-numeric values become pandas missing values (errors="coerce")."""
    
    df_tmp = df.copy()
    for column in INT_COLUMNS:
        df_tmp[column] = pd.to_numeric(df_tmp[column], errors="coerce").astype("Int64")

    for column in FLOAT_COLUMNS:
        df_tmp[column] = pd.to_numeric(df_tmp[column], errors="coerce").astype("Float64")

    return df_tmp


def _normalize_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """Replace IMGW missing-data sentinel values to pandas missing values."""
    
    df_tmp = df.copy()

    df_tmp["COSTAN"] = df_tmp["COSTAN"].mask(df_tmp["COSTAN"] >= 9999)
    df_tmp["COPRZP"] = df_tmp["COPRZP"].mask(df_tmp["COPRZP"] >= 99999)
    df_tmp["COPTMP"] = df_tmp["COPTMP"].mask(df_tmp["COPTMP"] >= 99)
    
    return df_tmp


def read_imgw_data(path: str | Path, *, encoding: str | None = None, delimiter: str | None = None) -> pd.DataFrame:
    """
    Read and normalize an IMGW daily hydrological data file.

    The function reads hydrological CSV data published by IMGW-PIB and
    returns a typed DataFrame ready for further processing.

    It handles both standard multi-column CSV files and the nested
    single-column CSV format found in some IMGW datasets. File encoding
    and delimiter are detected automatically unless supplied explicitly.

    During parsing, the function:

    - assigns standard IMGW column names,
    - extracts the river or lake code from the water-body name,
    - converts numeric columns to nullable numeric dtypes,
    - converts non-numeric values in numeric columns to missing values,
    - replaces IMGW missing-data sentinel values with missing values.

    The returned DataFrame uses the following dtypes:

    - ``PSKDSZS``, ``PSNZWP``, ``KDNRZK``, ``KDKRZK``: ``string``
    - ``COROKH``, ``COMSCH``, ``CODZIEN``, ``COMSCK``: ``Int64``
    - ``COSTAN``, ``COPRZP``, ``COPTMP``: ``Float64``

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the IMGW hydrological CSV file.
    encoding : str, optional
        Character encoding of the input file. If None, the encoding is
        detected automatically.
    delimiter : str, optional
        CSV delimiter. If None, the delimiter is detected automatically.

    Returns
    -------
    pandas.DataFrame
        Parsed and normalized IMGW hydrological data.

    Raises
    ------
    ValueError
        If the file encoding or CSV delimiter cannot be detected.

    Examples
    --------
    >>> df = read_imgw_data("codz_2024.csv")
    >>> df.head()

    The encoding or delimiter can also be provided explicitly:

    >>> df = read_imgw_data(
    ...     "codz_2024.csv",
    ...     encoding="cp1250",
    ...     delimiter=",",
    ... )
    """
    
    encoding = _get_file_encoding(path) if encoding is None else encoding
    delimiter = _get_csv_delimiter(path, encoding) if delimiter is None else delimiter
    
    df = _read_raw_data(path, encoding, delimiter)
    _, ncolumns = df.shape
    if ncolumns == 1:
        df = _parse_nested_csv(path, encoding)
    
    df = _set_column_names(df)
    df = _extract_river_code(df)
    df = _convert_numeric_columns(df)
    df = _normalize_missing_data(df)
    return df
