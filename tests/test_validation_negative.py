import pytest
import pandas as pd
from typing import NamedTuple

from imgw_hydro_tools import validation


class TestCase(NamedTuple):
    dataframe: pd.DataFrame
    expected: pd.Series


@pytest.fixture
def dataframe_with_no_negative_flows() -> TestCase:
    df = pd.DataFrame(
        {
            "COPRZP": [10.0, 20.0, 30.0, 150.0]
        }
    )

    expected = pd.Series(
        [False, False, False, False], 
        index=df.index, 
        dtype=bool
    )

    return TestCase(dataframe=df, expected=expected)


@pytest.fixture
def dataframe_with_negative_flows() -> TestCase:
    df = pd.DataFrame(
        {
            "COPRZP": [-10.0, 0.0,-30.0, 150.0]
        }
    )

    expected = pd.Series(
        [True, False, True, False], 
        index=df.index, 
        dtype=bool
    )

    return TestCase(dataframe=df, expected=expected)


@pytest.fixture
def dataframe_with_negative_flows_and_missing_values() -> TestCase:
    df = pd.DataFrame(
        {
            "COPRZP": [-10.0, pd.NA,-30.0, 150.0]
        }
    )

    expected = pd.Series(
        [True, False, True, False], 
        index=df.index, 
        dtype=bool
    )

    return TestCase(dataframe=df, expected=expected)


@pytest.fixture
def dataframe_with_custom_index(
    dataframe_with_no_negative_flows: TestCase
    ) -> TestCase:

    df = dataframe_with_no_negative_flows.dataframe.copy()
    df.index = [10, 20, 30, 40]

    expected = pd.Series(
            [False, False, False, False], 
            index=df.index, 
            dtype=bool
        )
    
    return TestCase(dataframe=df, expected=expected)


@pytest.fixture
def dataframe_with_all_columns() -> TestCase:
    df = pd.DataFrame(
        [
            [150210020, "SZCZUCIN", "Wisła", 2023, 9, 28, 235.0, 366.0, 16, 7, 2],
            [150210150, "KOŁO", "Wisła", 2023, 2, 4, 118.0, -105.0, pd.NA, 12, 2],
            [150210170, "SANDOMIERZ", "Wisła", 2023, 4, 24, pd.NA, 940.0, 1.4, 2, 2],
            [150210190, "ZAWICHOST", "Wisła", 2023, 10, 25, 231.0, pd.NA, 19.4, 8, 2]
        ],
        columns=[
            "PSKDSZS", "PSNZWP", "KDNRZK", "COROKH", "COMSCH", "CODZIEN", 
            "COSTAN", "COPRZP", "COPTMP", "COMSCK", "KDKRZK"
        ]
    )

    expected = pd.Series(
        [False, True, False, False], 
        index=df.index, 
        dtype=bool
    )

    return TestCase(dataframe=df, expected=expected)


# @pytest.mark.skip(reason="TDD: negative flow observations validation not implemented yet")
def test_find_negative_flows_raises_error_when_flow_column_is_missing(
        dataframe_with_no_negative_flows: TestCase
    ) -> None:

    df = dataframe_with_no_negative_flows.dataframe.drop(columns=["COPRZP"])
    with pytest.raises(KeyError):
        validation.find_negative_flows(df)


# @pytest.mark.skip(reason="TDD: negative flow observations validation not implemented yet")
def test_find_negative_flows_preserves_dataframe_index(
        dataframe_with_custom_index: TestCase
    ) -> None:

    result = validation.find_negative_flows(
        dataframe_with_custom_index.dataframe
    )
    pd.testing.assert_series_equal(
        result,
        dataframe_with_custom_index.expected
    )


# @pytest.mark.skip(reason="TDD: negative flow observations validation not implemented yet")
def test_find_negative_flows_returns_expected_series_for_no_negative_flows(
        dataframe_with_no_negative_flows: TestCase
    ) -> None:

    result = validation.find_negative_flows(
        dataframe_with_no_negative_flows.dataframe
    )
    pd.testing.assert_series_equal(
        result,
        dataframe_with_no_negative_flows.expected
    )


# @pytest.mark.skip(reason="TDD: negative flow observations validation not implemented yet")
def test_find_negative_flows_returns_expected_series_for_negative_flows(
        dataframe_with_negative_flows: TestCase
    ) -> None:

    result = validation.find_negative_flows(
        dataframe_with_negative_flows.dataframe
    )
    pd.testing.assert_series_equal(
        result,
        dataframe_with_negative_flows.expected
    )


# @pytest.mark.skip(reason="TDD: negative flow observations validation not implemented yet")
def test_find_negative_flows_returns_expected_series_for_negative_flows_ignoring_missing_values(
        dataframe_with_negative_flows_and_missing_values: TestCase
    ) -> None:

    result = validation.find_negative_flows(
        dataframe_with_negative_flows_and_missing_values.dataframe
    )
    pd.testing.assert_series_equal(
        result,
        dataframe_with_negative_flows_and_missing_values.expected
    )


# @pytest.mark.skip(reason="TDD: negative flow observations validation not implemented yet")
def test_find_negative_flows_returns_expected_series_for_full_dataframe(
        dataframe_with_all_columns: TestCase,
    ) -> None:

    result = validation.find_negative_flows(
        dataframe_with_all_columns.dataframe
    )
    pd.testing.assert_series_equal(
        result,
        dataframe_with_all_columns.expected
    )

