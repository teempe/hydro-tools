import pytest
import pandas as pd
from typing import NamedTuple

from imgw_hydro_tools import validation


class TestCase(NamedTuple):
    dataframe: pd.DataFrame
    expected: pd.DataFrame


@pytest.fixture
def dataframe_without_validation_issues() -> TestCase:
    df = pd.DataFrame(
        [
            [150190340, "KRAKÓW-BIELANY", "Wisła", 2023, 5, 3, 159.0, 100.0, 18.0, 3, 2],
            [150190170, "PUSTYNIA", "Wisła", 2023, 6, 28, 222.0, 120.0, 17.5, 4, 2],
            [150190360, "LAS", "Wisła", 2023, 7, 6, 191.0, 130.0, 19.0, 5, 2],
            [149190230, "CZERNICHÓW-PROM", "Wisła", 2023, 3, 28, 211.0, 58.2, 20.4, 1, 2],
            [150200130, "JAGODNIKI", "Wisła", 2023, 4, 5, 260.0, 252.0, 21.2, 2, 2],
            [150200150, "KARSY", "Wisła", 2023, 3, 20, 267.0, 317.0, 18.0, 1, 2],
            [150210020, "SZCZUCIN", "Wisła", 2023, 9, 28, 235.0, 366.0, 23.5, 7, 2],
            [150210150, "KOŁO", "Wisła", 2023, 2, 4, 118.0, 105.0, 2.5, 12, 2],
            [150210170, "SANDOMIERZ", "Wisła", 2023, 4, 24, 411.0, 940.0, 1.4, 2, 2],
            [150210190, "ZAWICHOST", "Wisła", 2023, 10, 25, 231.0, 240.0, 19.4, 8, 2],
        ],
        columns=[
            "PSKDSZS", "PSNZWP", "KDNRZK", "COROKH", "COMSCH", "CODZIEN", 
            "COSTAN", "COPRZP", "COPTMP", "COMSCK", "KDKRZK"
        ]
    )
    expected = pd.DataFrame(
        [
            ["missing", "COSTAN", 0, 0.0],
            ["missing", "COPRZP", 0, 0.0],
            ["missing", "COPTMP", 0, 0.0],
            ["issues", "invalid_dates", 0, 0.0],
            ["issues", "duplicate_observations", 0, 0.0],
            ["issues", "negative_flows", 0, 0.0]
        ],
        columns=["category", "check", "count", "percent"]
    )
    return TestCase(dataframe=df, expected=expected)


@pytest.fixture
def dataframe_with_validation_issues() -> TestCase:
    df = pd.DataFrame(
        [
            [150190340, "KRAKÓW-BIELANY", "Wisła", 2023, 5, 3, 159.0, pd.NA, pd.NA, 3, 2],
            [150190170, "PUSTYNIA", "Wisła", 2023, 6, 28, 222.0, pd.NA, pd.NA, 4, 2],
            [150190360, "LAS", "Wisła", 2023, 7, 6, 191.0, pd.NA, pd.NA, 5, 2],
            [149190230, "CZERNICHÓW-PROM", "Wisła", 2023, 3, 28, 211.0, 58.2, pd.NA, 1, 2],
            [150200130, "JAGODNIKI", "Wisła", 2023, 4, 31, 260.0, 252.0, pd.NA, 2, 2],
            [150200150, "KARSY", "Wisła", 2023, 3, 20, 267.0, -317.0, pd.NA, 1, 2],
            [150210020, "SZCZUCIN", "Wisła", 2023, 9, 28, pd.NA, 366.0, pd.NA, 7, 2],
            [150210170, "KOŁO", "Wisła", 2023, 4, 24, 118.0, 105.0, pd.NA, 2, 2],
            [150210170, "SANDOMIERZ", "Wisła", 2023, 4, 24, 411.0, 940.0, 1.4, 2, 2],
            [150210190, "ZAWICHOST", "Wisła", 2023, 10, 25, 231.0, 240.0, 19.4, 8, 2]
        ],
        columns=[
            "PSKDSZS", "PSNZWP", "KDNRZK", "COROKH", "COMSCH", "CODZIEN", 
            "COSTAN", "COPRZP", "COPTMP", "COMSCK", "KDKRZK"
        ]
    )
    expected = pd.DataFrame(
        [
            ["missing", "COSTAN", 1, 10.0],
            ["missing", "COPRZP", 3, 30.0],
            ["missing", "COPTMP", 8, 80.0],
            ["issues", "invalid_dates", 1, 10.0],
            ["issues", "duplicate_observations", 2, 20.0],
            ["issues", "negative_flows", 1, 10.0]
        ],
        columns=["category", "check", "count", "percent"]
    )
    return TestCase(dataframe=df, expected=expected)


# @pytest.mark.skip(reason="TDD: validation summary not implemented yet")
def test_validation_summary_returns_expected_dataframe_for_input_without_validation_issues(
        dataframe_without_validation_issues: TestCase
    ) -> None:

    result = validation.validation_summary(
        dataframe_without_validation_issues.dataframe
    )
    pd.testing.assert_frame_equal(
        result,
        dataframe_without_validation_issues.expected
    )


# @pytest.mark.skip(reason="TDD: validation summary not implemented yet")
def test_validation_summary_returns_expected_dataframe_for_input_with_validation_issues(
        dataframe_with_validation_issues: TestCase
    ) -> None:

    result = validation.validation_summary(
        dataframe_with_validation_issues.dataframe
    )
    pd.testing.assert_frame_equal(
        result,
        dataframe_with_validation_issues.expected
    )
