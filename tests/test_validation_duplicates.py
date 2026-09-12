import pytest
import pandas as pd
from typing import NamedTuple

from imgw_hydro_tools import validation


DUPLICATE_KEY_COLUMNS = ["PSKDSZS", "COROKH", "COMSCK", "CODZIEN"]


class TestCase(NamedTuple):
    dataframe: pd.DataFrame
    expected: pd.Series


@pytest.fixture
def dataframe_with_no_duplicates() -> TestCase:
    df = pd.DataFrame(
        [
            [150190340, "KRAKÓW-BIELANY", "Wisła", 2023, 5, 3, 159.0, pd.NA, pd.NA, 3, 2],
            [150190170, "PUSTYNIA", "Wisła", 2023, 6, 28, 222.0, pd.NA, pd.NA, 4, 2],
            [150190360, "LAS", "Wisła", 2023, 7, 6, 191.0, pd.NA, pd.NA, 5, 2],
            [149190230, "CZERNICHÓW-PROM", "Wisła", 2023, 3, 28, 211.0, 58.2, pd.NA, 1, 2],
            [150200130, "JAGODNIKI", "Wisła", 2023, 4, 5, 260.0, 252.0, pd.NA, 2, 2],
            [150200150, "KARSY", "Wisła", 2023, 3, 20, 267.0, 317.0, pd.NA, 1, 2],
            [150210020, "SZCZUCIN", "Wisła", 2023, 9, 28, 235.0, 366.0, pd.NA, 7, 2],
            [150210150, "KOŁO", "Wisła", 2023, 2, 4, 118.0, 105.0, pd.NA, 12, 2],
            [150210170, "SANDOMIERZ", "Wisła", 2023, 4, 24, 411.0, 940.0, 1.4, 2, 2],
            [150210190, "ZAWICHOST", "Wisła", 2023, 10, 25, 231.0, 240.0, 19.4, 8, 2],
        ],
        columns=[
            "PSKDSZS", "PSNZWP", "KDNRZK", "COROKH", "COMSCH", "CODZIEN", 
            "COSTAN", "COPRZP", "COPTMP", "COMSCK", "KDKRZK"
        ]
    )
    expected = pd.Series(
        [False, False, False, False, False, False, False, False, False, False], 
        index=df.index, 
        dtype=bool
    )
    return TestCase(dataframe=df, expected=expected)


@pytest.fixture
def dataframe_with_two_duplicates(
    dataframe_with_no_duplicates: TestCase
    ) -> TestCase:

    df = dataframe_with_no_duplicates.dataframe.copy()
    duplicate = df.loc[8]
    df.loc[7] = duplicate
    expected = pd.Series(
        [False, False, False, False, False, False, False, True, True, False], 
        index=df.index, 
        dtype=bool
    )
    return TestCase(dataframe=df, expected=expected)


@pytest.fixture
def dataframe_with_four_duplicates(
    dataframe_with_no_duplicates: TestCase
    ) -> TestCase:

    df = dataframe_with_no_duplicates.dataframe.copy()
    duplicate = df.loc[8]
    df.loc[0] = duplicate
    df.loc[5] = duplicate
    df.loc[7] = duplicate
    expected = pd.Series(
        [True, False, False, False, False, True, False, True, True, False],
        index=df.index,
        dtype=bool,
    )
    return TestCase(dataframe=df, expected=expected)


@pytest.fixture
def dataframe_with_duplicate_keys_and_different_measurements(
    dataframe_with_no_duplicates: TestCase
    ) -> TestCase:

    df = dataframe_with_no_duplicates.dataframe.copy()
    duplicate = df.loc[8]
    df.loc[5] = duplicate
    df.loc[5, ["COSTAN", "COPRZP", "COPTMP"]] = [267.0, 317.0, 1.5]
    expected = pd.Series(
        [False, False, False, False, False, True, False, False, True, False],
        index=df.index,
        dtype=bool,
    )
    return TestCase(dataframe=df, expected=expected)


@pytest.fixture
def dataframe_with_same_date_different_stations(
    dataframe_with_no_duplicates: TestCase
    ) -> TestCase:

    df = dataframe_with_no_duplicates.dataframe.copy()
    date_columns = ["COROKH", "COMSCK", "CODZIEN"]
    df.loc[1, date_columns] = df.loc[0, date_columns]
    expected = pd.Series(
        [False, False, False, False, False, False, False, False, False, False],
        index=df.index,
        dtype=bool
    )
    return TestCase(dataframe=df, expected=expected)


@pytest.fixture
def dataframe_with_same_station_different_dates(
    dataframe_with_no_duplicates: TestCase
    ) -> TestCase:

    df = dataframe_with_no_duplicates.dataframe.copy()
    df.loc[1, "PSKDSZS"] = df.loc[0, "PSKDSZS"]
    expected = pd.Series(
        [False, False, False, False, False, False, False, False, False, False],
        index=df.index,
        dtype=bool
    )
    return TestCase(dataframe=df, expected=expected)


@pytest.fixture
def dataframe_with_custom_index(
    dataframe_with_no_duplicates: TestCase
    ) -> TestCase:

    df = dataframe_with_no_duplicates.dataframe.copy()
    df.index = list(range(10, 110, 10))
    expected = pd.Series(
        [False, False, False, False, False, False, False, False, False, False],
        index=df.index,
        dtype=bool
    )
    return TestCase(dataframe=df, expected=expected)


@pytest.fixture
def dataframe_with_incomplete_duplicate_keys(
    dataframe_with_no_duplicates: TestCase,
) -> TestCase:
    df = dataframe_with_no_duplicates.dataframe.copy()
    duplicate = df.loc[0]
    df.loc[1] = duplicate
    df.loc[[0, 1], "COMSCK"] = pd.NA
    expected = pd.Series(
        [False, False, False, False, False, False, False, False, False, False],
        index=df.index,
        dtype=bool,
    )
    return TestCase(dataframe=df, expected=expected)


def test_find_duplicate_observations_returns_expected_series_for_no_duplicates(
    dataframe_with_no_duplicates: TestCase
    ) -> None:

    result = validation.find_duplicate_observations(
        dataframe_with_no_duplicates.dataframe
    )
    pd.testing.assert_series_equal(
        result, 
        dataframe_with_no_duplicates.expected
    )


def test_find_duplicate_observations_returns_expected_series_for_duplicate_records(
    dataframe_with_two_duplicates: TestCase
    ) -> None:

    result = validation.find_duplicate_observations(
        dataframe_with_two_duplicates.dataframe
    )
    pd.testing.assert_series_equal(
        result, 
        dataframe_with_two_duplicates.expected
    )


def test_find_duplicate_observations_returns_expected_series_for_more_than_two_duplicate_records(
    dataframe_with_four_duplicates: TestCase
    ) -> None:

    result = validation.find_duplicate_observations(
        dataframe_with_four_duplicates.dataframe
    )
    pd.testing.assert_series_equal(
        result,
        dataframe_with_four_duplicates.expected
    )


def test_find_duplicate_observations_returns_expected_series_for_duplicate_keys_with_different_measurements(
    dataframe_with_duplicate_keys_and_different_measurements: TestCase
    ) -> None:

    result = validation.find_duplicate_observations(
        dataframe_with_duplicate_keys_and_different_measurements.dataframe
    )
    pd.testing.assert_series_equal(
        result,
        dataframe_with_duplicate_keys_and_different_measurements.expected
    )


def test_find_duplicate_observations_returns_expected_series_for_same_date_different_stations(
    dataframe_with_same_date_different_stations: TestCase
    ) -> None:

    result = validation.find_duplicate_observations(
        dataframe_with_same_date_different_stations.dataframe
    )
    pd.testing.assert_series_equal(
        result,
        dataframe_with_same_date_different_stations.expected
    )


def test_find_duplicate_observations_returns_expected_series_for_same_station_different_dates(
    dataframe_with_same_station_different_dates: TestCase
    ) -> None:

    result = validation.find_duplicate_observations(
        dataframe_with_same_station_different_dates.dataframe
    )
    pd.testing.assert_series_equal(
        result,
        dataframe_with_same_station_different_dates.expected
    )


def test_find_duplicate_observations_preserves_dataframe_index(
    dataframe_with_custom_index: TestCase
    ) -> None:

    result = validation.find_duplicate_observations(
        dataframe_with_custom_index.dataframe
    )
    pd.testing.assert_series_equal(
        result,
        dataframe_with_custom_index.expected
    )


@pytest.mark.parametrize("missing_column", DUPLICATE_KEY_COLUMNS)
def test_find_duplicate_observations_raises_error_when_key_column_is_missing(
    dataframe_with_no_duplicates: TestCase,
    missing_column: str
) -> None:

    df = dataframe_with_no_duplicates.dataframe.drop(columns=[missing_column])
    with pytest.raises(KeyError):
        validation.find_duplicate_observations(df)


def test_find_duplicate_observations_does_not_mark_incomplete_keys_as_duplicates(
    dataframe_with_incomplete_duplicate_keys: TestCase
) -> None:
    
    result = validation.find_duplicate_observations(
        dataframe_with_incomplete_duplicate_keys.dataframe
    )

    pd.testing.assert_series_equal(
        result,
        dataframe_with_incomplete_duplicate_keys.expected
    )
