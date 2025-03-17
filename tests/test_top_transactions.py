import pandas as pd

from src.utils import get_top_transactions


def test_get_top_transactions(test_df):
    # Вызываем тестируемую функцию
    result = get_top_transactions(test_df)

    # Проверяем формат результата
    assert isinstance(result, list)
    assert len(result) == 5

    # Проверяем структуру каждой транзакции
    for transaction in result:
        assert set(transaction.keys()) == {"date", "amount", "category", "description"}
        assert isinstance(transaction["date"], str)
        assert isinstance(transaction["amount"], float)
        assert isinstance(transaction["category"], str)
        assert isinstance(transaction["description"], str)

    # Проверяем сортировку и округление
    expected_amounts = [1500.79, 1200.46, 1000.57, 800.11, 500.12]
    assert [transaction["amount"] for transaction in result] == expected_amounts

    # Проверяем формат даты
    expected_dates = ["03.01.2025", "05.01.2025", "01.01.2025", "06.01.2025", "02.01.2025"]
    assert [transaction["date"] for transaction in result] == expected_dates


def test_get_top_transactions_less_than_5(test_df):
    # Берем только 3 транзакции
    small_df = test_df.head(3)
    result = get_top_transactions(small_df)

    # Проверяем количество результатов
    assert len(result) == 3


def test_get_top_transactions_empty_df():
    empty_df = pd.DataFrame(columns=["Дата операции", "Сумма платежа", "Категория", "Описание"])
    result = get_top_transactions(empty_df)

    # Проверяем результат
    assert result == []
