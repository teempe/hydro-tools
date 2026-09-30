import pytest
import pandas as pd
from typing import NamedTuple

from imgw_hydro_tools import validation


OBSERVATION_COLUMNS = ["COSTAN", "COPRZP", "COPTMP"]


class TestCase(NamedTuple):
    dataframe: pd.DataFrame
    expected: pd.DataFrame


@pytest.fixture
def dataframe_with_no_missing_observations() -> TestCase:
    df = pd.DataFrame(
        {
            "COSTAN": [150.0, 200.0, 250.0],
            "COPRZP": [10.0, 20.0, 30.0],
            "COPTMP": [5.0, 10.0, 15.0]
        }
    )

    expected = pd.DataFrame(
        {
            "COSTAN": [False, False, False],
            "COPRZP": [False, False, False],
            "COPTMP": [False, False, False]
        },
        index=df.index,
        dtype=bool
    )

    return TestCase(dataframe=df, expected=expected)


@pytest.fixture
def dataframe_with_missing_observations() -> TestCase:
    df = pd.DataFrame(
        {
            "COSTAN": [150.0, pd.NA, 250.0, pd.NA],
            "COPRZP": [pd.NA, 20.0, 30.0, pd.NA],
            "COPTMP": [5.0, 10.0, pd.NA, pd.NA]
        }
    )

    expected = pd.DataFrame(
        {
            "COSTAN": [False, True, False, True],
            "COPRZP": [True, False, False, True],
            "COPTMP": [False, False, True, True]
        },
        index=df.index,
        dtype=bool
    )

    return TestCase(dataframe=df, expected=expected)


@pytest.fixture
def dataframe_with_custom_index(
    dataframe_with_no_missing_observations: TestCase
    ) -> TestCase:

    df = dataframe_with_no_missing_observations.dataframe.copy()
    df.index = [10, 20, 30]

    expected = pd.DataFrame(
        {
            "COSTAN": [False, False, False],
            "COPRZP": [False, False, False],
            "COPTMP": [False, False, False]
        },
        index=df.index,
        dtype=bool
    )
    
    return TestCase(dataframe=df, expected=expected)


@pytest.fixture
def dataframe_with_all_columns() -> TestCase:
    df = pd.DataFrame(
        [
            [150210020, "SZCZUCIN", "Wisła", 2023, 9, 28, 235.0, 366.0, 16, 7, 2],
            [150210150, "KOŁO", "Wisła", 2023, 2, 4, 118.0, 105.0, pd.NA, 12, 2],
            [150210170, "SANDOMIERZ", "Wisła", 2023, 4, 24, pd.NA, 940.0, 1.4, 2, 2],
            [150210190, "ZAWICHOST", "Wisła", 2023, 10, 25, 231.0, pd.NA, 19.4, 8, 2]
        ],
        columns=[
            "PSKDSZS", "PSNZWP", "KDNRZK", "COROKH", "COMSCH", "CODZIEN", 
            "COSTAN", "COPRZP", "COPTMP", "COMSCK", "KDKRZK"
        ]
    )

    expected = pd.DataFrame(
            [   
                [False, False, False],
                [False, False, True],
                [True, False, False],
                [False, True, False]
            ],
            columns=[
                "COSTAN", "COPRZP", "COPTMP"
            ],
            index=df.index,
            dtype=bool
        )

    return TestCase(dataframe=df, expected=expected)


# @pytest.mark.skip(reason="TDD: missing observations validation not implemented yet")
@pytest.mark.parametrize("missing_column", OBSERVATION_COLUMNS)
def test_find_missing_observations_raises_error_when_observation_column_is_missing(
        dataframe_with_no_missing_observations: TestCase,
        missing_column: str
    )-> None:

    df = dataframe_with_no_missing_observations.dataframe.drop(columns=[missing_column])
    with pytest.raises(KeyError):
        validation.find_missing_observations(df)


# @pytest.mark.skip(reason="TDD: missing observations validation not implemented yet")
def test_find_missing_observations_preserves_dataframe_index(
        dataframe_with_custom_index: TestCase
    ) -> None:

    result = validation.find_missing_observations(
        dataframe_with_custom_index.dataframe
    )
    pd.testing.assert_frame_equal(
        result,
        dataframe_with_custom_index.expected
    )


# @pytest.mark.skip(reason="TDD: missing observations validation not implemented yet")
def test_find_missing_observations_returns_expected_dataframe_for_no_missing_observations(
        dataframe_with_no_missing_observations: TestCase
    ) -> None:

    result = validation.find_missing_observations(
        dataframe_with_no_missing_observations.dataframe
    )
    pd.testing.assert_frame_equal(
        result,
        dataframe_with_no_missing_observations.expected
    )


# @pytest.mark.skip(reason="TDD: missing observations validation not implemented yet")
def test_find_missing_observations_returns_expected_dataframe_for_missing_observations(
        dataframe_with_missing_observations: TestCase
    ) -> None:

    result = validation.find_missing_observations(
        dataframe_with_missing_observations.dataframe
    )
    pd.testing.assert_frame_equal(
        result,
        dataframe_with_missing_observations.expected
    )


# @pytest.mark.skip(reason="TDD: missing observations validation not implemented yet")
def test_find_missing_observations_returns_only_measurement_columns(
        dataframe_with_all_columns: TestCase,
    ) -> None:

    result = validation.find_missing_observations(
        dataframe_with_all_columns.dataframe
    )
    pd.testing.assert_frame_equal(
        result,
        dataframe_with_all_columns.expected
    )

