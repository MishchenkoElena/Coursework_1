import os
import tempfile
from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import get_data_period


def test_monthly_range(test_data):
    date_string = "2025-01-15 12:00:00"
    expected_start = pd.Timestamp(2025, 1, 1, 0, 0, 0)
    expected_end = pd.to_datetime(date_string)

    df = pd.DataFrame(test_data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    with patch("pandas.read_excel", return_value=df):
        result = get_data_period(date_string, "M")

    assert len(result) == 15
    assert result["Дата операции"].min() == expected_start
    assert result["Дата операции"].max() == expected_end


def test_yearly_range(test_data):
    date_string = "2025-01-15 12:00:00"
    expected_start = pd.Timestamp(2025, 1, 1, 0, 0, 0)
    expected_end = pd.to_datetime(date_string)

    df = pd.DataFrame(test_data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    with patch("pandas.read_excel", return_value=df):
        result = get_data_period(date_string, "Y")

    assert len(result) == 15
    assert result["Дата операции"].min() == expected_start
    assert result["Дата операции"].max() == expected_end


def test_weekly_range(test_data):
    date_string = "2025-01-15 12:00:00"
    expected_start = pd.Timestamp(2025, 1, 13, 0, 0, 0)  # Понедельник недели
    expected_end = pd.to_datetime(date_string)

    df = pd.DataFrame(test_data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    with patch("pandas.read_excel", return_value=df):
        result = get_data_period(date_string, "W")

    assert len(result) == 3
    assert result["Дата операции"].min() == expected_start
    assert result["Дата операции"].max() == expected_end


def test_all_range(test_data):
    date_string = "2025-01-15 12:00:00"
    expected_end = pd.to_datetime(date_string)

    df = pd.DataFrame(test_data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    with patch("pandas.read_excel", return_value=df):
        result = get_data_period(date_string, "ALL")

    assert len(result) == 15
    assert result["Дата операции"].max() == expected_end
    assert result["Дата операции"].min() == pd.Timestamp(2025, 1, 1, 0, 0, 0)
    assert (result["Дата операции"] <= expected_end).all()


def test_invalid_period():
    date_string = "2025-01-15 12:00:00"
    invalid_range = "INVALID"

    with pytest.raises(ValueError, match="Invalid period"):
        get_data_period(date_string, invalid_range)


def test_invalid_date_format():
    invalid_date_string = "2025-01-15"  # Неверный формат даты

    with pytest.raises(ValueError, match="time data"):
        get_data_period(invalid_date_string)


def test_parser_error():
    date_string = "2025-01-15 12:00:00"

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        tmp.write(b"invalid excel content")

    with pytest.raises(ValueError) as exc_info:
        get_data_period(date_string, tmp.name)

    os.remove(tmp.name)
    assert "Invalid period" in str(exc_info.value)
