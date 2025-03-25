import json
import os
from unittest.mock import mock_open, patch

import requests

from src.utils import get_currency_rates


@patch("requests.get")
def test_get_currency_rates_success(mock_get):
    # Тест вывода корректного результата
    mock_response = {"success": True, "rates": {"USD": 85.0, "EUR": 90.0}}
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.status_code = 200

    test_settings = {"user_currencies": ["USD", "EUR"]}
    test_settings_file = "test_settings.json"

    # Создаем временный файл настроек
    with open(test_settings_file, "w") as f:
        json.dump(test_settings, f)

    result = get_currency_rates(test_settings_file)

    assert len(result) == 2
    assert result[0] == {"currency": "USD", "rate": 85.0}
    assert result[1] == {"currency": "EUR", "rate": 90.0}

    # Удаляем тестовый файл настроек
    os.remove(test_settings_file)


@patch("requests.get")
def test_get_currency_rates_api_error(mock_get):
    # Тестирование ошибки API
    mock_get.side_effect = requests.RequestException("API Error")

    test_settings = {"user_currencies": ["USD", "EUR"]}
    test_settings_file = "test_settings.json"

    # Создаем временный файл настроек
    with open(test_settings_file, "w") as f:
        json.dump(test_settings, f)

    result = get_currency_rates(test_settings_file)

    assert len(result) == 2
    assert result[0] == {"currency": "USD", "rate": None}
    assert result[1] == {"currency": "EUR", "rate": None}

    # Удаляем тестовый файл настроек
    os.remove(test_settings_file)


@patch("requests.get")
def test_get_currency_rates_invalid_file(mock_get):
    # Тест с использованием некорректного файла настроек
    test_settings = {}

    with patch("builtins.open", mock_open(read_data=json.dumps(test_settings))):
        result = get_currency_rates("test_file.json")

    assert len(result) == 0


@patch("requests.get")
def test_get_currency_rates_empty_currencies(mock_get):
    # Тест с использованием пустого файла настроек
    test_settings = {"user_currencies": []}

    with patch("builtins.open", mock_open(read_data=json.dumps(test_settings))):
        result = get_currency_rates("empty_currencies.json")

    assert result == []
