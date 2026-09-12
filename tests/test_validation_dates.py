import pytest
import pandas as pd

from imgw_hydro_tools import validation


@pytest.fixture
def valid_dates_not_leap_year():
    msch = list(range(1, 13))
    msck = [11, 12, *range(1, 11)]
    dzien = [30,31,31,28,31,30,31,30,31,31,30,31]
    
    df = pd.DataFrame(
        {
            "COROKH": 2023,
            "COMSCH": msch,
            "COMSCK": msck,
            "CODZIEN": dzien
        },
        dtype="Int64"
    )
    return df


@pytest.fixture
def valid_dates_leap_year(valid_dates_not_leap_year):
    df = valid_dates_not_leap_year.copy()
    df["COROKH"] = 2024
    df.loc[df["COMSCK"]==2, "CODZIEN"] = 29
    return df


@pytest.fixture
def result_for_valid_dates():
    return pd.Series([False]*12)


def test_find_invalid_dates_returns_expected_series_for_valid_leap_year_dates(valid_dates_leap_year, result_for_valid_dates):
    result = validation.find_invalid_dates(valid_dates_leap_year)
    pd.testing.assert_series_equal(result, result_for_valid_dates)


def test_find_invalid_dates_returns_expected_series_for_valid_not_leap_year_dates(valid_dates_not_leap_year, result_for_valid_dates):
    result = validation.find_invalid_dates(valid_dates_not_leap_year)
    pd.testing.assert_series_equal(result, result_for_valid_dates)


# @pytest.mark.skip(reason="TDD: missing column validation not implemented yet")
@pytest.mark.parametrize("missing_column", ["COROKH", "COMSCH", "CODZIEN", "COMSCK"])
def test_find_invalid_dates_raises_error_when_column_is_missing(valid_dates_not_leap_year, missing_column):
    df = valid_dates_not_leap_year.drop(columns=[missing_column])
    with pytest.raises(KeyError):
        validation.find_invalid_dates(df)


# @pytest.mark.skip(reason="TDD: invalid day validation not implemented yet")
def test_find_invalid_dates_returns_expected_series_for_invalid_days(valid_dates_not_leap_year):
    df = valid_dates_not_leap_year.copy()
    df["CODZIEN"] = [0,31,31,29,31,31,32,30,31,pd.NA,30,31]

    expected = pd.Series([True,False,False,True,False,True,True,False,False,True,False,False], dtype=bool)
    result = validation.find_invalid_dates(df)

    pd.testing.assert_series_equal(result, expected)


# @pytest.mark.skip(reason="TDD: invalid hydro month validation not implemented yet")
def test_find_invalid_dates_returns_expected_series_for_invalid_hydro_month(valid_dates_not_leap_year):
    df = valid_dates_not_leap_year.copy()
    df["COMSCH"] = [1,2,0,4,5,13,7,8,pd.NA,10,11,12]

    expected = pd.Series([False,False,True,False,False,True,False,False,True,False,False,False], dtype=bool)
    result = validation.find_invalid_dates(df)

    pd.testing.assert_series_equal(result, expected)


# @pytest.mark.skip(reason="TDD: invalid calendar month validation not implemented yet")
def test_find_invalid_dates_returns_expected_series_for_invalid_calendar_month(valid_dates_not_leap_year):
    df = valid_dates_not_leap_year.copy()
    df["COMSCK"] = [11,12,0,2,3,13,5,6,pd.NA,8,9,10]

    expected = pd.Series([False,False,True,False,False,True,False,False,True,False,False,False], dtype=bool)
    result = validation.find_invalid_dates(df)

    pd.testing.assert_series_equal(result, expected)


# @pytest.mark.skip(reason="TDD: missing hydro year validation not implemented yet")
def test_find_invalid_dates_returns_expected_series_for_missing_hydro_year(valid_dates_not_leap_year):
    df = valid_dates_not_leap_year.copy()
    df.iloc[4, 0] = pd.NA
    df.iloc[9, 0] = pd.NA

    expected = pd.Series([False,False,False,False,True,False,False,False,False,True,False,False], dtype=bool)
    result = validation.find_invalid_dates(df)

    pd.testing.assert_series_equal(result, expected)


# @pytest.mark.skip(reason="TDD: inconsistent hydro calendar month validation not implemented yet")
def test_find_invalid_dates_returns_expected_series_for_inconsistent_hydro_calendar_month(valid_dates_not_leap_year):
    df = valid_dates_not_leap_year.copy()
    df["COMSCH"] = [1, 3, 2,4,5,6,7,8,9,10,11,12]
    df["COMSCK"] = [11,12,1,2,3,4,5,6,7,9, 8, 10]

    expected = pd.Series([False,True,True,False,False,False,False,False,False,True,True,False], dtype=bool)
    result = validation.find_invalid_dates(df)

    pd.testing.assert_series_equal(result, expected)


# @pytest.mark.skip(reason="TDD: find invalid dates function not implemented yet")
def test_find_invalid_dates_preserves_dataframe_index(valid_dates_not_leap_year,):
    df = valid_dates_not_leap_year.copy()
    df.index = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]

    result = validation.find_invalid_dates(df)

    pd.testing.assert_index_equal(result.index, df.index)


# @pytest.mark.skip(reason="TDD: find invalid dates function not implemented yet")
def test_find_invalid_dates_returns_expected_series_for_mixed_errors_given(valid_dates_not_leap_year):
    df = valid_dates_not_leap_year.copy()
    df.loc[0, "CODZIEN"] = 0
    df.loc[1, "COMSCK"] = 13
    df.loc[2, "COMSCH"] = pd.NA
    df.loc[3, "COROKH"] = pd.NA
    df.loc[4, "COMSCK"] = 5
    df.loc[4, "COMSCH"] = 3
    df.loc[5, "CODZIEN"] = 32
    df.loc[5, "COROKH"] = pd.NA

    expected = pd.Series([True,True,True,True,True,True,False,False,False,False,False,False], dtype=bool)
    result = validation.find_invalid_dates(df)

    pd.testing.assert_series_equal(result, expected)
