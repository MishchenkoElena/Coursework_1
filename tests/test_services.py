import pandas as pd
import pytest

from src.services import read_transactions_from_excel


@pytest.fixture
def test_data():
    return {"Дата": ["2023-01-01", "2023-01-02"], "Сумма": [100, 200], "Описание": ["Оплата", "Возврат"]}


@pytest.fixture
def test_file(test_data, tmp_path):
    test_file = tmp_path / "test_transactions.xlsx"
    df = pd.DataFrame(test_data)
    df.to_excel(test_file, index=False)
    yield test_file
    test_file.unlink()


def test_read_valid_excel(test_file):
    """Тест чтения валидного Excel файла"""
    transactions = read_transactions_from_excel(test_file)

    assert isinstance(transactions, list)
    assert isinstance(transactions[0], dict)
    assert len(transactions) == 2
    assert transactions[0]["Дата"] == "2023-01-01"
    assert transactions[0]["Сумма"] == 100


def test_file_not_found():
    """Тест обработки ошибки отсутствия файла"""
    with pytest.raises(FileNotFoundError):
        read_transactions_from_excel("non_existent_file.xlsx")


# def test_invalid_excel_format(tmp_path):
#     """Тест обработки некорректного формата Excel"""
#     invalid_file = tmp_path / "invalid.txt"
#     invalid_file.write_text("Это не Excel файл")
#
#     with pytest.raises(pd.errors.ParserError):
#         read_transactions_from_excel(invalid_file)


def test_empty_excel_file(tmp_path):
    """Тест чтения пустого Excel файла"""
    empty_file = tmp_path / "empty.xlsx"
    pd.DataFrame().to_excel(empty_file, index=False)

    transactions = read_transactions_from_excel(empty_file)
    assert len(transactions) == 0


# Дополнительные проверки
def test_return_type(test_file):
    transactions = read_transactions_from_excel(test_file)
    assert isinstance(transactions, list)
    assert all(isinstance(item, dict) for item in transactions)


def test_data_integrity(test_file):
    transactions = read_transactions_from_excel(test_file)
    expected_keys = {"Дата", "Сумма", "Описание"}
    for transaction in transactions:
        assert set(transaction.keys()) == expected_keys
