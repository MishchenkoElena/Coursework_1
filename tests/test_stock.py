import json
import os
from unittest.mock import mock_open, patch

import requests

from src.utils import get_stock_prices


@patch("requests.get")
def test_get_stock_prices_success(mock_get):
    # Имитация ответа API
    mock_response = {"symbol": "AAPL", "price": 150.25}
    mock_get.return_value.json.return_value = [mock_response]  # Важно: данные должны быть в списке
    mock_get.return_value.status_code = 200

    test_settings = {"user_stocks": ["AAPL"]}
    test_settings_file = "test_settings.json"

    # Создаем временный файл настроек
    with open(test_settings_file, "w") as f:
        json.dump(test_settings, f)

    result = get_stock_prices(test_settings_file)

    assert len(result) == 1
    assert result[0] == {"stock": "AAPL", "price": 150.25}

    # Удаляем тестовый файл настроек
    os.remove(test_settings_file)


@patch("requests.get")
def test_get_stock_prices_error(mock_get):
    # Тестирование ошибки API
    mock_get.side_effect = requests.RequestException("API Error")

    test_settings = {"user_stocks": ["AAPL"]}
    test_settings_file = "test_settings.json"

    # Создаем временный файл настроек
    with open(test_settings_file, "w") as f:
        json.dump(test_settings, f)

    result = get_stock_prices(test_settings_file)

    assert len(result) == 1
    assert result[0] == {"stock": "AAPL", "price": None}

    # Удаляем тестовый файл настроек
    os.remove(test_settings_file)


@patch("requests.get")
def test_get_stock_prices_invalid_file(mock_open):
    # Тест с использованием некорректного файла настроек
    test_settings = {}

    mock_file = mock_open(read_data=json.dumps(test_settings))
    mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(test_settings)

    with patch("builtins.open", mock_file):
        result = get_stock_prices("test_file.json")

    assert len(result) == 0


@patch("requests.get")
def test_get_stock_prices_empty_currencies(mock_get):
    # Тест с использованием пустого файла настроек
    test_settings = {"user_stocks": []}

    with patch("builtins.open", mock_open(read_data=json.dumps(test_settings))):
        result = get_stock_prices("empty_currencies.json")
        assert result == []
