import json

import pandas as pd
import pytest

from src.services import investment_bank, read_transactions_from_excel


# Тест чтения корректного Excel файла
def test_read_valid_excel(test_file):
    transactions = read_transactions_from_excel(test_file)

    assert isinstance(transactions, list)
    assert isinstance(transactions[0], dict)
    assert len(transactions) == 18
    assert transactions[0]["Дата операции"] == "01.01.2025 00:00:00"
    assert transactions[0]["Сумма операции"] == 100


# Тест обработки ошибки отсутствия файла
def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_transactions_from_excel("non_existent_file.xlsx")


# Тест чтения пустого Excel файла
def test_empty_excel_file(tmp_path):
    empty_file = tmp_path / "empty.xlsx"
    pd.DataFrame().to_excel(empty_file, index=False)

    transactions = read_transactions_from_excel(empty_file)
    assert len(transactions) == 0


# Базовый тест с валидными данными
def test_investment_bank_valid(valid_transactions):
    month = "2025-03"
    limit = 50
    expected_result = {"Месяц": "2025-03", "Лимит округления": 50, "Общая сумма накоплений за месяц": 139.00}

    result = investment_bank(month, valid_transactions, limit)
    assert json.loads(result) == expected_result


# Тест с некорректным форматом месяца
def test_investment_bank_invalid_month():
    month = "2025/03"
    limit = 50
    transactions = []

    with pytest.raises(ValueError, match="Неверный формат данных"):
        investment_bank(month, transactions, limit)


# Тест с пустым списком транзакций
def test_investment_bank_empty_transactions():
    month = "2025-03"
    limit = 50
    transactions = []

    expected_result = {"Месяц": "2025-03", "Лимит округления": 50, "Общая сумма накоплений за месяц": 0.00}

    result = investment_bank(month, transactions, limit)
    assert json.loads(result) == expected_result


# Тест с некорректной датой
def test_investment_bank_invalid_transactions():
    month = "2025-03"
    limit = 50
    transactions = [{"Неверная_дата": "20.03.2025 12:00:00", "Сумма операции": -1712.00}]

    with pytest.raises(KeyError):
        investment_bank(month, transactions, limit)


# Тест с транзакциями из месяца, отсутствующего в списке транзакций
def test_investment_bank_different_month(valid_transactions):
    month = "2025-04"
    limit = 50

    expected_result = {"Месяц": "2025-04", "Лимит округления": 50, "Общая сумма накоплений за месяц": 0.00}

    result = investment_bank(month, valid_transactions, limit)
    assert json.loads(result) == expected_result


# Тест с нулевым лимитом
def test_investment_bank_zero_limit():
    month = "2025-03"
    limit = 0
    transactions = []

    with pytest.raises(ValueError) as exc_info:
        investment_bank(month, transactions, limit)
    assert str(exc_info.value) == "Лимит округления должен быть больше 0"


def test_investment_bank_negative_limit():
    month = "2025-03"
    limit = -50
    transactions = []

    with pytest.raises(ValueError, match="Лимит округления должен быть больше 0"):
        investment_bank(month, transactions, limit)
