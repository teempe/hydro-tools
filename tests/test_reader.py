import pytest
import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

from imgw_hydro_tools import reader


###############################################################################
## PARSING CSV TO DATAFRAME
###############################################################################

# fixtures
@pytest.fixture
def typical_csv_comma_cp1250(tmp_path):
    content = (
        "150170040,OŁAWA,Odra (1),2023,01,01,185,99999.999,99.9,11\n"
        "150170040,OŁAWA,Odra (1),2023,01,02,188,99999.999,99.9,11\n"
        "150170040,OŁAWA,Odra (1),2023,01,03,188,99999.999,99.9,11\n"
        "149180020,CHAŁUPKI,Odra (1),2024,01,01,113,25.400,,11\n"
        "149180020,CHAŁUPKI,Odra (1),2024,01,02,109,23.300,,11\n"
        "149180020,CHAŁUPKI,Odra (1),2024,01,03,120,30.000,,11\n")
    csv_path = tmp_path / "data.csv"
    csv_path.write_text(content, encoding="cp1250")

    return csv_path


@pytest.fixture
def typical_csv_semicolon_utf8(tmp_path):
    content = (
        "150170040;OŁAWA;Odra (1);2023;01;01;185;99999.999;99.9;11\n"
        "150170040;OŁAWA;Odra (1);2023;01;02;188;99999.999;99.9;11\n"
        "150170040;OŁAWA;Odra (1);2023;01;03;188;99999.999;99.9;11\n"
        "149180020;CHAŁUPKI;Odra (1);2024;01;01;113;25.400;;11\n"
        "149180020;CHAŁUPKI;Odra (1);2024;01;02;109;23.300;;11\n"
        "149180020;CHAŁUPKI;Odra (1);2024;01;03;120;30.000;;11\n")
    csv_path = tmp_path / "data.csv"
    csv_path.write_text(content, encoding="utf-8")

    return csv_path


@pytest.fixture
def nested_csv_comma_cp1250(tmp_path):
    content = (
        '"150170040,OŁAWA,Odra (1),2023,01,01,185,99999.999,99.9,11"\n'
        '"150170040,OŁAWA,Odra (1),2023,01,02,188,99999.999,99.9,11"\n'
        '"150170040,OŁAWA,Odra (1),2023,01,03,188,99999.999,99.9,11"\n'
        '"149180020,CHAŁUPKI,Odra (1),2024,01,01,113,25.400,,11"\n'
        '"149180020,CHAŁUPKI,Odra (1),2024,01,02,109,23.300,,11"\n'
        '"149180020,CHAŁUPKI,Odra (1),2024,01,03,120,30.000,,11"\n')
    csv_path = tmp_path / "data.csv"
    csv_path.write_text(content, encoding="cp1250")

    return csv_path


@pytest.fixture
def expected_result():
    expected_df =  pd.DataFrame([
            ["150170040", "OŁAWA", "Odra", 2023, 1, 1, 185, 99999.999, 99.9, 11, "1"],
            ["150170040", "OŁAWA", "Odra", 2023, 1, 2, 188, 99999.999, 99.9, 11, "1"],
            ["150170040", "OŁAWA", "Odra", 2023, 1, 3, 188, 99999.999, 99.9, 11, "1"],
            ["149180020", "CHAŁUPKI", "Odra", 2024, 1, 1, 113, 25.400, pd.NA, 11, "1"],
            ["149180020", "CHAŁUPKI", "Odra", 2024, 1, 2, 109, 23.300, pd.NA, 11, "1"],
            ["149180020", "CHAŁUPKI", "Odra", 2024, 1, 3, 120, 30.000, pd.NA, 11, "1"]
        ],
        columns=["PSKDSZS", "PSNZWP", "KDNRZK", "COROKH", "COMSCH", "CODZIEN", "COSTAN", "COPRZP", "COPTMP", "COMSCK", "KDKRZK"]
    )
    return expected_df


# _get_encoding tests
def test_get_encoding_raises_value_error_when_encoding_cannot_be_determined(tmp_path, mocker):
    file_content = b"any test content"
    source_path = tmp_path / "data.csv"
    source_path.write_bytes(file_content)

    mock_from_bytes = mocker.patch("imgw_hydro_tools.reader.from_bytes")
    mock_from_bytes.return_value.best.return_value = None

    with pytest.raises(ValueError, match="Could not detect encoding"):
        reader._get_encoding(source_path)

    mock_from_bytes.assert_called_once_with(file_content)


def test_get_encoding_returns_detected_encoding(tmp_path, mocker):
    file_content = b"any test content"
    source_path = tmp_path / "data.csv"
    source_path.write_bytes(file_content)

    detected = mocker.Mock(encoding = "cp1250")

    mock_from_bytes = mocker.patch("imgw_hydro_tools.reader.from_bytes")
    mock_from_bytes.return_value.best.return_value = detected

    assert reader._get_encoding(source_path) == "cp1250"
    mock_from_bytes.assert_called_once_with(file_content)


# _get_dialect tests
def test_get_dialect_raises_value_error_when_dialect_cannot_be_determined(tmp_path, mocker):
    file_content = "any test content"
    source_path = tmp_path / "data.csv"
    source_path.write_text(file_content, encoding="utf-8")

    mocker.patch.object(reader.csv.Sniffer, "sniff", side_effect=reader.csv.Error())
    
    with pytest.raises(ValueError, match="Could not detect CSV dialect"):
        reader._get_dialect(source_path)


def test_get_dialect_returns_detected_dialect(typical_csv_semicolon_utf8):
    dialect = reader._get_dialect(typical_csv_semicolon_utf8) 
    assert dialect.delimiter == ";"


def test_get_dialect_returns_detected_dialect_in_nested_csv(nested_csv_comma_cp1250):
    dialect = reader._get_dialect(nested_csv_comma_cp1250, encoding="cp1250") 
    assert dialect.delimiter == ","


# _parse_nested_csv tests
def test_parse_nested_csv_returns_unpacked_dataframe(nested_csv_comma_cp1250):

    expected_df =  pd.DataFrame([
            ["150170040", "OŁAWA", "Odra (1)", "2023", "01", "01", "185", "99999.999", "99.9", "11"],
            ["150170040", "OŁAWA", "Odra (1)", "2023", "01", "02", "188", "99999.999", "99.9", "11"],
            ["150170040", "OŁAWA", "Odra (1)", "2023", "01", "03", "188", "99999.999", "99.9", "11"],
            ["149180020", "CHAŁUPKI", "Odra (1)", "2024", "01", "01", "113", "25.400", "", "11"],
            ["149180020", "CHAŁUPKI", "Odra (1)", "2024", "01", "02", "109", "23.300", "", "11"],
            ["149180020", "CHAŁUPKI", "Odra (1)", "2024", "01", "03", "120", "30.000", "", "11"]
        ],
        dtype="string"
    )

    result = reader._parse_nested_csv(nested_csv_comma_cp1250, encoding="cp1250")
    pd.testing.assert_frame_equal(result, expected_df)


###############################################################################
## PRELIMINARY CLEANING DATAFRAME
###############################################################################


# _extract_river_code tests
def test_extract_river_code():
    river_code_df = pd.DataFrame(
        [
            ["150190340","KRAKÓW-BIELANY","Wisła (2)","2020","09","01","200","99999.999","99.9","07"],
            ["150190340","KRAKÓW-BIELANY","Wisła 2","2020","09","02",'178',"99999.999","99.9","07"],
            ["150190340","KRAKÓW-BIELANY","Wisła ()","2020","09","03",'202',"99999.999","99.9","07"],
            ["150190340","KRAKÓW-BIELANY","Wisła","2020","09","04",'183',"99999.999","99.9","07"],
            ["154220060","OLECKO","Jez. Olecko Wielkie (2626139)","2020","09","01",'241',"99999.999","99.9","07"],
            ["154220060","OLECKO","Jez. Olecko Wielkie 2626139","2020","09","02",'241',"99999.999","99.9","07"],
            ["154220060","OLECKO","Jez. Olecko Wielkie ()","2020","09","03",'240',"99999.999","99.9","07"],
            ["154220060","OLECKO","Jez. Olecko Wielkie","2020","09","04",'239',"99999.999","99.9","07"]
        ],
        columns=["PSKDSZS", "PSNZWP", "KDNRZK", "COROKH", "COMSCH", "CODZIEN", "COSTAN", "COPRZP", "COPTMP", "COMSCK"]
    )

    expected_result = pd.DataFrame(
        [
            ["150190340","KRAKÓW-BIELANY","Wisła","2020","09","01","200","99999.999","99.9","07", "2"],
            ["150190340","KRAKÓW-BIELANY","Wisła 2","2020","09","02",'178',"99999.999","99.9","07", np.nan],
            ["150190340","KRAKÓW-BIELANY","Wisła ()","2020","09","03",'202',"99999.999","99.9","07", np.nan],
            ["150190340","KRAKÓW-BIELANY","Wisła","2020","09","04",'183',"99999.999","99.9","07", np.nan],
            ["154220060","OLECKO","Jez. Olecko Wielkie","2020","09","01",'241',"99999.999","99.9","07", "2626139"],
            ["154220060","OLECKO","Jez. Olecko Wielkie 2626139","2020","09","02",'241',"99999.999","99.9","07", np.nan],
            ["154220060","OLECKO","Jez. Olecko Wielkie ()","2020","09","03",'240',"99999.999","99.9","07", np.nan],
            ["154220060","OLECKO","Jez. Olecko Wielkie","2020","09","04",'239',"99999.999","99.9","07", np.nan]
        ],
        columns=["PSKDSZS", "PSNZWP", "KDNRZK", "COROKH", "COMSCH", "CODZIEN", "COSTAN", "COPRZP", "COPTMP", "COMSCK", "KDKRZK"]
    )

    reader._extract_river_code(river_code_df)
    pd.testing.assert_frame_equal(river_code_df, expected_result)


# _set_column_dtypes tests
@pytest.fixture
def dtypes_df():
    return pd.DataFrame(
        [
            ["150190340","KRAKÓW-BIELANY","Wisła","2020","09","01","200","99999.999","NA","07", "2"],
            ["150190340","KRAKÓW-BIELANY","Wisła 2","2020","09","02",'178',"99999.999","99.9","07", np.nan],
            ["150190340","KRAKÓW-BIELANY","Wisła ()","2020","09","03",'202',"99999.999","missing","07", np.nan],
            ["150190340","KRAKÓW-BIELANY","Wisła","2020","09","04",'183',"99999.999","99.9","07", np.nan],
            ["154220060","OLECKO","Jez. Olecko Wielkie","2020","09","01",'241',"99999.999","","07", "2626139"],
            ["154220060","OLECKO","Jez. Olecko Wielkie 2626139","2020","09","02",'241',"99999.999","99.9","07", np.nan],
            ["154220060","OLECKO","Jez. Olecko Wielkie ()","2020","09","03",'240',"99999.999","99.9","07", np.nan],
            ["154220060","OLECKO","Jez. Olecko Wielkie","2020","09","04",'239',"99999.999","99.9","07", np.nan]
        ],
        columns=["PSKDSZS", "PSNZWP", "KDNRZK", "COROKH", "COMSCH", "CODZIEN", "COSTAN", "COPRZP", "COPTMP", "COMSCK", "KDKRZK"]
    )


def test_set_column_dtypes_converts_numeric_columns(dtypes_df):
    reader._set_column_dtypes(dtypes_df)

    numeric_columns = reader.NUMERIC_COLUMNS
    for column in numeric_columns:
        assert is_numeric_dtype(dtypes_df[column])


def test_set_column_dtypes_preserves_non_numeric_columns(dtypes_df):
    non_numeric_columns = [column 
                           for column in dtypes_df.columns 
                           if column not in reader.NUMERIC_COLUMNS]

    expected_df = dtypes_df[non_numeric_columns].copy()
    
    reader._set_column_dtypes(dtypes_df)
    pd.testing.assert_frame_equal(dtypes_df[non_numeric_columns], expected_df)


def test_set_column_dtypes_coerces_invalid_values_to_nan(dtypes_df):
    reader._set_column_dtypes(dtypes_df)

    assert pd.isna(dtypes_df.loc[0, "COPTMP"])
    assert pd.isna(dtypes_df.loc[2, "COPTMP"])
    assert pd.isna(dtypes_df.loc[4, "COPTMP"])


def test_set_column_dtypes_preserves_numeric_sentinel_values(dtypes_df):
    reader._set_column_dtypes(dtypes_df)

    assert dtypes_df.loc[0, "COPRZP"] == 99999.999
    assert dtypes_df.loc[1, "COPTMP"] == 99.9


###############################################################################
## TEST PUBLIC FUNCTION
###############################################################################


# read_imgw_data tests
def test_read_imgw_data_reads_comma_csv(typical_csv_comma_cp1250, expected_result):
    result = reader.read_imgw_data(typical_csv_comma_cp1250)
    pd.testing.assert_frame_equal(result, expected_result, check_dtype=False)


def test_read_imgw_data_reads_semicolon_csv(typical_csv_semicolon_utf8, expected_result):
    result = reader.read_imgw_data(typical_csv_semicolon_utf8)
    pd.testing.assert_frame_equal(result, expected_result, check_dtype=False)


def test_read_imgw_data_reads_nested_csv(nested_csv_comma_cp1250, expected_result):
    result = reader.read_imgw_data(nested_csv_comma_cp1250)
    pd.testing.assert_frame_equal(result, expected_result, check_dtype=False)
