from datetime import datetime
from unittest.mock import patch

from src.utils import get_greeting


@patch("src.utils.datetime")
def test_day_greeting(mock_datetime):
    mock_datetime.now.return_value = datetime(2025, 3, 23, 15, 10, 0)
    assert get_greeting() == "Добрый день"


@patch("src.utils.datetime")
def test_evening_greeting(mock_datetime):
    mock_datetime.now.return_value = datetime(2025, 3, 23, 20, 15, 0)
    assert get_greeting() == "Добрый вечер"


@patch("src.utils.datetime")
def test_night_greeting(mock_datetime):
    mock_datetime.now.return_value = datetime(2025, 3, 23, 3, 25, 0)
    assert get_greeting() == "Доброй ночи"
