import pandas as pd

from src.utils import get_cards_data


def test_get_cards_data_empty_df():
    # Создаем пустой DataFrame с нужными колонками
    empty_df = pd.DataFrame(columns=["Номер карты", "Сумма платежа"])
    result = get_cards_data(empty_df)
    assert result == []


def test_get_cards_data_single_card():
    # Создаем DataFrame с одной картой и несколькими транзакциями
    data = {"Номер карты": [4276123456789012, 4276123456789012], "Сумма платежа": [-1000, -2000]}
    df = pd.DataFrame(data)
    expected = [{"last_digits": "9012", "total_spent": 3000, "cashback": 30}]
    result = get_cards_data(df)
    assert result == expected


def test_get_cards_data_multiple_cards():
    # Создаем DataFrame с несколькими картами
    data = {
        "Номер карты": [4276123456789012, 5469123456789012, 4276123456789012],
        "Сумма платежа": [-1000, -500, -2000],
    }
    df = pd.DataFrame(data)
    expected = [
        {"last_digits": "9012", "total_spent": 3000, "cashback": 30},
        {"last_digits": "9012", "total_spent": 500, "cashback": 5},
    ]
    result = get_cards_data(df)
    assert sorted(result, key=lambda x: x["last_digits"]) == sorted(expected, key=lambda x: x["last_digits"])


def test_get_cards_data_no_negative_transactions():
    # Создаем DataFrame без отрицательных транзакций
    data = {"Номер карты": [4276123456789012, 4276123456789012], "Сумма платежа": [1000, 2000]}
    df = pd.DataFrame(data)
    result = get_cards_data(df)
    assert result == []
