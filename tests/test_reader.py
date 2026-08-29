import pytest
import pandas as pd

from imgw_hydro_tools import reader


@pytest.fixture
def csv_comma_cp1250(tmp_path):
    content = (
        "150190340,KRAKÓW-BIELANY,Wisła (2),2023,09,01,9999,99999.999,99.9,07\n"
        "150190340,KRAKÓW-BIELANY,Wisła 2,2023,09,02,NULL,NULL,NULL,07\n"
        "150190340,KRAKÓW-BIELANY,Wisła (),2023,09,03,,,,07\n"
        "150190340,KRAKÓW-BIELANY,Wisła,2023,09,04,150,200,19,07\n")
    csv_comma_cp1250 = tmp_path / "data.csv"
    csv_comma_cp1250.write_text(content, encoding="cp1250")
    return csv_comma_cp1250


@pytest.fixture
def csv_semicolon_utf8(tmp_path):
    content = (
        "150190340;KRAKÓW-BIELANY;Wisła (2);2023;09;01;9999;99999.999;99.9;07\n"
        "150190340;KRAKÓW-BIELANY;Wisła 2;2023;09;02;NULL;NULL;NULL;07\n"
        "150190340;KRAKÓW-BIELANY;Wisła ();2023;09;03;;;;07\n"
        "150190340;KRAKÓW-BIELANY;Wisła;2023;09;04;150;200;19;07\n")
    csv_semicolon_utf8 = tmp_path / "data.csv"
    csv_semicolon_utf8.write_text(content, encoding="utf-8")
    return csv_semicolon_utf8


@pytest.fixture
def csv_comma_cp1250_nested(tmp_path):
    content = (
        '"150190340,KRAKÓW-BIELANY,Wisła (2),2023,09,01,9999,99999.999,99.9,07"\n'
        '"150190340,KRAKÓW-BIELANY,Wisła 2,2023,09,02,NULL,NULL,NULL,07"\n'
        '"150190340,KRAKÓW-BIELANY,Wisła (),2023,09,03,,,,07"\n'
        '"150190340,KRAKÓW-BIELANY,Wisła,2023,09,04,150,200,19,07"\n')
    csv_comma_cp1250_nested = tmp_path / "data.csv"
    csv_comma_cp1250_nested.write_text(content, encoding="cp1250")
    return csv_comma_cp1250_nested


@pytest.fixture
def df_raw():
    df_raw = pd.DataFrame(
        [
            ["150190340", "KRAKÓW-BIELANY", "Wisła (2)", "2023", "09", "01", "9999", "99999.999", "99.9", "07"],
            ["150190340", "KRAKÓW-BIELANY", "Wisła 2", "2023", "09", "02", "NULL", "NULL", "NULL", "07"],
            ["150190340", "KRAKÓW-BIELANY", "Wisła ()", "2023", "09", "03", "", "", "", "07"],
            ["150190340", "KRAKÓW-BIELANY", "Wisła", "2023", "09", "04", "150", "200", "19", "07"]
        ],
        dtype="string"
    )
    return df_raw


@pytest.fixture
def df_with_column_names():
    df_with_column_names = pd.DataFrame(
        [
            ["150190340", "KRAKÓW-BIELANY", "Wisła (2)", "2023", "09", "01", "9999", "99999.999", "99.9", "07"],
            ["150190340", "KRAKÓW-BIELANY", "Wisła 2", "2023", "09", "02", "NULL", "NULL", "NULL", "07"],
            ["150190340", "KRAKÓW-BIELANY", "Wisła ()", "2023", "09", "03", "", "", "", "07"],
            ["150190340", "KRAKÓW-BIELANY", "Wisła", "2023", "09", "04", "150", "200", "19", "07"]
        ],
        dtype="string",
        columns=["PSKDSZS", "PSNZWP", "KDNRZK", "COROKH", "COMSCH", "CODZIEN", "COSTAN", "COPRZP", "COPTMP", "COMSCK"]
    )
    return df_with_column_names


@pytest.fixture
def df_with_river_code():
    df_with_river_code = pd.DataFrame(
        [
            ["150190340", "KRAKÓW-BIELANY", "Wisła", "2023", "09", "01", "9999", "99999.999", "99.9", "07", "2"],
            ["150190340", "KRAKÓW-BIELANY", "Wisła 2", "2023", "09", "02", "NULL", "NULL", "NULL", "07", pd.NA],
            ["150190340", "KRAKÓW-BIELANY", "Wisła ()", "2023", "09", "03", "", "", "", "07", pd.NA],
            ["150190340", "KRAKÓW-BIELANY", "Wisła", "2023", "09", "04", "150", "200", "19", "07", pd.NA]
        ],
        dtype="string",
        columns=["PSKDSZS", "PSNZWP", "KDNRZK", "COROKH", "COMSCH", "CODZIEN", "COSTAN", "COPRZP", "COPTMP", "COMSCK", "KDKRZK"]
    )
    return df_with_river_code


@pytest.fixture
def df_with_numeric_types():
    df_with_numeric_types = pd.DataFrame(
        [
            ["150190340", "KRAKÓW-BIELANY", "Wisła", 2023, 9, 1, 9999, 99999.999, 99.9, 7, "2"],
            ["150190340", "KRAKÓW-BIELANY", "Wisła 2", 2023, 9, 2, pd.NA, pd.NA, pd.NA, 7, pd.NA],
            ["150190340", "KRAKÓW-BIELANY", "Wisła ()", 2023, 9, 3, pd.NA, pd.NA, pd.NA, 7, pd.NA],
            ["150190340", "KRAKÓW-BIELANY", "Wisła", 2023, 9, 4, 150, 200, 19, 7, pd.NA]
        ],
        columns=["PSKDSZS", "PSNZWP", "KDNRZK", "COROKH", "COMSCH", "CODZIEN", "COSTAN", "COPRZP", "COPTMP", "COMSCK", "KDKRZK"]
    )

    df_with_numeric_types = df_with_numeric_types.astype(
        {
            "PSKDSZS": "string",
            "PSNZWP": "string",
            "KDNRZK": "string",
            "COROKH": "Int64",
            "COMSCH": "Int64",
            "CODZIEN": "Int64",
            "COSTAN": "Float64",
            "COPRZP": "Float64",
            "COPTMP": "Float64",
            "COMSCK": "Int64",
            "KDKRZK": "string",
        }
    )

    return df_with_numeric_types


@pytest.fixture
def df_normalized():
    df_normalized = pd.DataFrame(
        [
            ["150190340", "KRAKÓW-BIELANY", "Wisła", 2023, 9, 1, pd.NA, pd.NA, pd.NA, 7, "2"],
            ["150190340", "KRAKÓW-BIELANY", "Wisła 2", 2023, 9, 2, pd.NA, pd.NA, pd.NA, 7, pd.NA],
            ["150190340", "KRAKÓW-BIELANY", "Wisła ()", 2023, 9, 3, pd.NA, pd.NA, pd.NA, 7, pd.NA],
            ["150190340", "KRAKÓW-BIELANY", "Wisła", 2023, 9, 4, 150, 200, 19, 7, pd.NA]
        ],
        columns=["PSKDSZS", "PSNZWP", "KDNRZK", "COROKH", "COMSCH", "CODZIEN", "COSTAN", "COPRZP", "COPTMP", "COMSCK", "KDKRZK"]
    )

    df_normalized = df_normalized.astype(
        {
            "PSKDSZS": "string",
            "PSNZWP": "string",
            "KDNRZK": "string",
            "COROKH": "Int64",
            "COMSCH": "Int64",
            "CODZIEN": "Int64",
            "COSTAN": "Float64",
            "COPRZP": "Float64",
            "COPTMP": "Float64",
            "COMSCK": "Int64",
            "KDKRZK": "string",
        }
    )
    return df_normalized


# _get_file_encoding
def test_get_file_encoding_raises_value_error_when_encoding_cannot_be_determined(csv_comma_cp1250, mocker):
    mock_from_bytes = mocker.patch.object(reader, "from_bytes")
    mock_from_bytes.return_value.best.return_value = None

    with pytest.raises(ValueError):
        reader._get_file_encoding(csv_comma_cp1250)

    mock_from_bytes.assert_called_once_with(csv_comma_cp1250.read_bytes())


def test_get_file_encoding_returns_detected_encoding(csv_comma_cp1250, mocker):
    mock_from_bytes = mocker.patch.object(reader, "from_bytes")
    mock_from_bytes.return_value.best.return_value = mocker.Mock(encoding = "cp1250")

    assert reader._get_file_encoding(csv_comma_cp1250) == "cp1250"
    mock_from_bytes.assert_called_once_with(csv_comma_cp1250.read_bytes())


# _get_csv_delimiter
def test_get_csv_delimiter_raises_value_error_when_dialect_cannot_be_determined(csv_semicolon_utf8, mocker):
    mocker.patch.object(reader.csv.Sniffer, "sniff", side_effect=reader.csv.Error())    
    with pytest.raises(ValueError):
        reader._get_csv_delimiter(csv_semicolon_utf8, "utf-8")


def test_get_csv_delimiter_returns_detected_delimiter(csv_semicolon_utf8):
    delimiter = reader._get_csv_delimiter(csv_semicolon_utf8, "utf-8") 
    assert delimiter == ";"


def test_get_csv_delimiter_returns_detected_dialect_in_nested_csv(csv_comma_cp1250_nested):
    delimiter = reader._get_csv_delimiter(csv_comma_cp1250_nested, "cp1250") 
    assert delimiter == ","


# _read_raw_data
def test_read_raw_data_returns_dataframe(csv_comma_cp1250, df_raw):
    result = reader._read_raw_data(csv_comma_cp1250, "cp1250", ",")
    pd.testing.assert_frame_equal(result, df_raw)


# _parse_nested_csv
def test_parse_nested_csv_returns_unpacked_dataframe(csv_comma_cp1250_nested, df_raw):
    result = reader._parse_nested_csv(csv_comma_cp1250_nested, "cp1250")
    pd.testing.assert_frame_equal(result, df_raw)


# _set_column_names
def test_set_column_names_returns_df_with_column_names(df_raw, df_with_column_names):
    result = reader._set_column_names(df_raw)
    pd.testing.assert_frame_equal(result, df_with_column_names)


# _extract_river_code
def test_extract_river_code_returns_expected_dataframe(df_with_column_names, df_with_river_code):
    result = reader._extract_river_code(df_with_column_names)
    pd.testing.assert_frame_equal(result, df_with_river_code)


# _convert_numeric_columns
def test_convert_numeric_columns_returns_expected_dataframe(df_with_river_code, df_with_numeric_types):
    result = reader._convert_numeric_columns(df_with_river_code)
    pd.testing.assert_frame_equal(result, df_with_numeric_types)


# _normalize_missing_data
def test_normalize_missing_data_converts_sentinels_to_nan(df_with_numeric_types, df_normalized):
    result = reader._normalize_missing_data(df_with_numeric_types)
    pd.testing.assert_frame_equal(result, df_normalized)


# Public API - read_imgw_data
def test_read_imgw_data_reads_comma_csv(csv_comma_cp1250, df_normalized):
    result = reader.read_imgw_data(csv_comma_cp1250)
    pd.testing.assert_frame_equal(result, df_normalized)


def test_read_imgw_data_reads_semicolon_csv(csv_semicolon_utf8, df_normalized):
    result = reader.read_imgw_data(csv_semicolon_utf8)
    pd.testing.assert_frame_equal(result, df_normalized)


def test_read_imgw_data_reads_nested_csv(csv_comma_cp1250_nested, df_normalized):
    result = reader.read_imgw_data(csv_comma_cp1250_nested)
    pd.testing.assert_frame_equal(result, df_normalized)


def test_read_imgw_data_does_not_detect_encoding_when_provided(csv_comma_cp1250, mocker):
    mock_encoding = mocker.patch.object(reader, "_get_file_encoding")
    mock_delimiter = mocker.patch.object(reader, "_get_csv_delimiter", return_value=",")

    reader.read_imgw_data(csv_comma_cp1250, encoding="cp1250")

    mock_encoding.assert_not_called()
    mock_delimiter.assert_called_once_with(csv_comma_cp1250, "cp1250")


def test_read_imgw_data_does_not_detect_delimiter_when_provided(csv_comma_cp1250, mocker):
    mock_encoding = mocker.patch.object(reader, "_get_file_encoding", return_value="cp1250")
    mock_delimiter = mocker.patch.object(reader, "_get_csv_delimiter")

    reader.read_imgw_data(csv_comma_cp1250, delimiter=",")

    mock_encoding.assert_called_once_with(csv_comma_cp1250)
    mock_delimiter.assert_not_called()


def test_read_imgw_data_does_not_detect_delimiter_and_encoding_when_provided(csv_comma_cp1250, mocker):
    mock_encoding = mocker.patch.object(reader, "_get_file_encoding")
    mock_delimiter = mocker.patch.object(reader, "_get_csv_delimiter")

    reader.read_imgw_data(csv_comma_cp1250, encoding="cp1250", delimiter=",")

    mock_encoding.assert_not_called()
    mock_delimiter.assert_not_called()


def test_read_imgw_data_detects_delimiter_and_encoding_when_not_provided(csv_comma_cp1250, mocker):
    mock_encoding = mocker.patch.object(reader, "_get_file_encoding", return_value="cp1250")
    mock_delimiter = mocker.patch.object(reader, "_get_csv_delimiter", return_value=",")

    reader.read_imgw_data(csv_comma_cp1250)

    mock_encoding.assert_called_once_with(csv_comma_cp1250)
    mock_delimiter.assert_called_once_with(csv_comma_cp1250, "cp1250")
