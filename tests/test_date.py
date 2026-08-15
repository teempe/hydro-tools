import pandas as pd
import pytest
from imgw_hydro_tools.data import hydro_to_calendar_date


def test_january_stays_same_year():
    df = pd.DataFrame({"MCROKH": [2024], "MCMSCK": [1], "MCDZIK": [1]})
    result = hydro_to_calendar_date(df)
    assert result.iloc[0] == pd.Timestamp("2024-01-01")

def test_october_stays_same_year():
    df = pd.DataFrame({"MCROKH": [2025], "MCMSCK": [10], "MCDZIK": [31]})
    result = hydro_to_calendar_date(df)
    assert result.iloc[0] == pd.Timestamp("2025-10-31")

def test_november_goes_previous_year():
    df = pd.DataFrame({"MCROKH": [2020], "MCMSCK": [11], "MCDZIK": [1]})
    result = hydro_to_calendar_date(df)
    assert result.iloc[0] == pd.Timestamp("2019-11-01")

def test_december_goes_previous_year():
    df = pd.DataFrame({"MCROKH": [2018], "MCMSCK": [12], "MCDZIK": [31]})
    result = hydro_to_calendar_date(df)
    assert result.iloc[0] == pd.Timestamp("2017-12-31")

def test_leap_year_returns_valid_date():
    df = pd.DataFrame({"MCROKH": [2024], "MCMSCK": [2], "MCDZIK": [29]})
    result = hydro_to_calendar_date(df)
    assert result.iloc[0] == pd.Timestamp("2024-02-29")

def test_invalid_leap_year_raises_value_error():
    df = pd.DataFrame({"MCROKH": [2023], "MCMSCK": [2], "MCDZIK": [29]})
    with pytest.raises(ValueError):
        hydro_to_calendar_date(df)

def test_vector_operation():
    df = pd.DataFrame({"MCROKH": [2024, 2024, 2024, 2024], "MCMSCK": [10, 11, 12, 1], "MCDZIK": [31, 1, 31, 1]})
    expected = pd.Series([pd.Timestamp("2024-10-31"), pd.Timestamp("2023-11-01"), pd.Timestamp("2023-12-31"), pd.Timestamp("2024-01-01")])
    result = hydro_to_calendar_date(df)
    pd.testing.assert_series_equal(expected, result)

def test_missing_year_column_raises_key_error():
    df = pd.DataFrame({"MCMSCK": [10], "MCDZIK": [15]}) # MCROKH missing
    with pytest.raises(KeyError, match="Missing required columns: MCROKH"):
        hydro_to_calendar_date(df)

def test_missing_month_column_raises_key_error():
    df = pd.DataFrame({"MCROKH": [2026], "MCDZIK": [31]})  # MCMSCK missing
    with pytest.raises(KeyError, match="Missing required columns: MCMSCK"):
        hydro_to_calendar_date(df)

def test_missing_day_column_raises_key_error():
    df = pd.DataFrame({"MCROKH": [2019], "MCMSCK": [12]})  # MCDZIK missing
    with pytest.raises(KeyError, match="Missing required columns: MCDZIK"):
        hydro_to_calendar_date(df)

def test_custom_column_names():
    df = pd.DataFrame({"hydro_year": [2024], "month": [11], "day": [1]})
    result = hydro_to_calendar_date(df, hydro_year_col="hydro_year", month_col="month", day_col="day")
    assert result.iloc[0] == pd.Timestamp("2023-11-01")

def test_empty_dataframe_returns_empty_series():
    df = pd.DataFrame(columns=["MCROKH", "MCMSCK", "MCDZIK"])
    result = hydro_to_calendar_date(df)
    assert result.empty

def test_errors_set_to_coerce_returns_nat():
    df = pd.DataFrame({"MCROKH": [2020], "MCMSCK": [15], "MCDZIK": [-5]})
    result = hydro_to_calendar_date(df, errors="coerce")
    assert pd.isna(result.iloc[0])

def test_errors_set_to_raise_raises_value_error():
    df = pd.DataFrame({"MCROKH": [2020], "MCMSCK": [15], "MCDZIK": [-5]})
    with pytest.raises(ValueError):
        hydro_to_calendar_date(df, errors="raise")
