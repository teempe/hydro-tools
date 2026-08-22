import pandas as pd
import pytest

from imgw_hydro_tools.date import hydro_to_calendar_date


def test_january_stays_same_year():
    df = pd.DataFrame({"COROKH": [2024], "COMSCK": [1], "CODZIEN": [1]})
    result = hydro_to_calendar_date(df)
    assert result.iloc[0] == pd.Timestamp("2024-01-01")

def test_october_stays_same_year():
    df = pd.DataFrame({"COROKH": [2025], "COMSCK": [10], "CODZIEN": [31]})
    result = hydro_to_calendar_date(df)
    assert result.iloc[0] == pd.Timestamp("2025-10-31")

def test_november_goes_previous_year():
    df = pd.DataFrame({"COROKH": [2020], "COMSCK": [11], "CODZIEN": [1]})
    result = hydro_to_calendar_date(df)
    assert result.iloc[0] == pd.Timestamp("2019-11-01")

def test_december_goes_previous_year():
    df = pd.DataFrame({"COROKH": [2018], "COMSCK": [12], "CODZIEN": [31]})
    result = hydro_to_calendar_date(df)
    assert result.iloc[0] == pd.Timestamp("2017-12-31")

def test_leap_year_returns_valid_date():
    df = pd.DataFrame({"COROKH": [2024], "COMSCK": [2], "CODZIEN": [29]})
    result = hydro_to_calendar_date(df)
    assert result.iloc[0] == pd.Timestamp("2024-02-29")

def test_invalid_leap_year_raises_value_error():
    df = pd.DataFrame({"COROKH": [2023], "COMSCK": [2], "CODZIEN": [29]})
    with pytest.raises(ValueError):
        hydro_to_calendar_date(df)

def test_vector_operation():
    df = pd.DataFrame({"COROKH": [2024, 2024, 2024, 2024], "COMSCK": [10, 11, 12, 1], "CODZIEN": [31, 1, 31, 1]})
    expected = pd.Series([pd.Timestamp("2024-10-31"), pd.Timestamp("2023-11-01"), pd.Timestamp("2023-12-31"), pd.Timestamp("2024-01-01")])
    result = hydro_to_calendar_date(df)
    pd.testing.assert_series_equal(expected, result)

def test_missing_year_column_raises_key_error():
    df = pd.DataFrame({"COMSCK": [10], "CODZIEN": [15]}) # COROKH missing
    with pytest.raises(KeyError, match="Missing required columns: COROKH"):
        hydro_to_calendar_date(df)

def test_missing_month_column_raises_key_error():
    df = pd.DataFrame({"COROKH": [2026], "CODZIEN": [31]})  # COMSCK missing
    with pytest.raises(KeyError, match="Missing required columns: COMSCK"):
        hydro_to_calendar_date(df)

def test_missing_day_column_raises_key_error():
    df = pd.DataFrame({"COROKH": [2019], "COMSCK": [12]})  # CODZIEN missing
    with pytest.raises(KeyError, match="Missing required columns: CODZIEN"):
        hydro_to_calendar_date(df)

def test_custom_column_names():
    df = pd.DataFrame({"hydro_year": [2024], "month": [11], "day": [1]})
    result = hydro_to_calendar_date(df, hydro_year_col="hydro_year", month_col="month", day_col="day")
    assert result.iloc[0] == pd.Timestamp("2023-11-01")

def test_empty_dataframe_returns_empty_series():
    df = pd.DataFrame(columns=["COROKH", "COMSCK", "CODZIEN"])
    result = hydro_to_calendar_date(df)
    assert result.empty

def test_errors_set_to_coerce_returns_nat():
    df = pd.DataFrame({"COROKH": [2020], "COMSCK": [15], "CODZIEN": [-5]})
    result = hydro_to_calendar_date(df, errors="coerce")
    assert pd.isna(result.iloc[0])

def test_errors_set_to_raise_raises_value_error():
    df = pd.DataFrame({"COROKH": [2020], "COMSCK": [15], "CODZIEN": [-5]})
    with pytest.raises(ValueError):
        hydro_to_calendar_date(df, errors="raise")
