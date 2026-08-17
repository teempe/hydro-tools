import csv
from io import StringIO
from pathlib import Path

import pandas as pd
from charset_normalizer import from_bytes


IMGW_COLUMNS = ["PSKDSZS", "PSNZWP", "KDNRZK", "COROKH", "COMSCH", "CODZIEN", "COSTAN", "COPRZP", "COPTMP", "COMSCK"]
NUMERIC_COLUMNS = ['COROKH', 'COMSCH', 'CODZIEN', 'COSTAN', 'COPRZP', 'COPTMP', 'COMSCK']


def _get_encoding(path: str | Path) -> str:
    """Detect a file's character encoding. Raises ValueError if undetectable."""
    
    with Path(path).open("rb") as f:
        result = from_bytes(f.read()).best()
    if result is None:
        raise ValueError(f"Could not detect encoding for: {path}")
    return result.encoding


def _get_dialect(path: str | Path, encoding: str = "utf-8") -> csv.Dialect:
    """Detect a file's dialect. Raises ValueError if the dialect cannot be determined."""
    
    with Path(path).open("r", encoding=encoding, newline="") as file_in:
        try:
            dialect = csv.Sniffer().sniff(file_in.read(1024))
        except csv.Error as e:
            raise ValueError(f"Could not detect CSV dialect for: {path}") from e          
    return dialect


def _parse_nested_csv(path: str | Path, encoding: str = "utf-8") -> pd.DataFrame:
    """Parse the nested IMGW CSV format into a DataFrame of strings."""
    
    rows = []
    
    with Path(path).open("r", encoding=encoding, newline="") as input_file:
        input_reader = csv.reader(input_file)
        for line in input_reader:
            parsed_rows = next(csv.reader(StringIO(line[0]), delimiter=","))
            rows.append(parsed_rows)
        
    return pd.DataFrame(rows, dtype="string")


def _set_column_names(df: pd.DataFrame) -> None:
    """Assign column names to the DataFrame in place. Uses the default IMGW column codes."""
    df.columns = IMGW_COLUMNS


def _extract_river_code(df: pd.DataFrame) -> None:
    """Extract a numeric code in trailing parentheses into KDKRZK; 
    names without a code are left unchanged, with a missing value as the code
    """
    df["KDKRZK"] = df["KDNRZK"].str.extract(r"\((\d+)\)$", expand=False)
    df["KDNRZK"] = df["KDNRZK"].str.replace(r"\((\d+)\)$", "", regex=True).str.strip()


def _set_column_dtypes(df: pd.DataFrame) -> None:
    """Convert numeric IMGW columns to numbers in place. Non-numeric values become NaN (errors="coerce")."""
    numeric_columns = NUMERIC_COLUMNS
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors="coerce")


def read_imgw_data(path: str | Path, encoding: str | None = None) -> pd.DataFrame:
    """Read an IMGW hydrological data file into a typed DataFrame.
 
    Handles both the regular multi-column CSV format and the malformed
    single-column format (where each row is a nested, double-quoted CSV
    string). The file's encoding and delimiter are detected automatically
    unless an encoding is provided.
 
    The returned DataFrame has IMGW column names, an extracted river/lake
    code column (KDKRZK), and numeric columns converted to numbers.
    Validating the *values* is left to separate validation tools.
 
    Parameters
    ----------
    path : str or pathlib.Path
        Path to the IMGW data file.
    encoding : str, optional
        File encoding. If None, it is detected automatically.
 
    Returns
    -------
    pandas.DataFrame
        Parsed and typed data with IMGW column names.
 
    Raises
    ------
    ValueError
        If the encoding or CSV dialect cannot be determined.
 
    Examples
    --------
    >>> df = read_imgw_data("codz_2023.csv")
    >>> df.columns.tolist()
    ['PSKDSZS', 'PSNZWP', 'KDNRZK', 'COROKH', 'COMSCH', 'CODZIEN',
     'COSTAN', 'COPRZP', 'COPTMP', 'COMSCK', 'KDKRZK']
    """
    if encoding is None:
        encoding = _get_encoding(path)
    
    delimiter = _get_dialect(path, encoding=encoding).delimiter
    
    df = pd.read_csv(path, encoding=encoding, delimiter=delimiter, header=None, dtype="string", na_filter=False)
    
    _, ncolumns = df.shape
    if ncolumns == 1:
        df = _parse_nested_csv(path, encoding)

    _set_column_names(df)
    _extract_river_code(df)
    _set_column_dtypes(df)
    
    return df
