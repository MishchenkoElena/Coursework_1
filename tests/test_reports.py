from datetime import datetime
from pathlib import Path

import pandas as pd

from src.reports import spending_by_category


# Тест с использованием декорированной функции
def test_spending_by_category(test_transactions):
    result = spending_by_category(test_transactions, "продукты")

    expected_result = pd.DataFrame({"Категория": "Продукты", "Сумма трат за 3 месяца": 2712.00}, index=[0])

    assert result.equals(expected_result)

    # Проверяем сохранение файла
    today = datetime.now().strftime("%Y%m%d")
    file_path = f"../reports/{today}.json"
    assert Path(file_path).exists()


# Тест с пустой категорией
def test_spending_by_category_empty_category(test_transactions):
    result = spending_by_category(test_transactions, "")
    assert result.empty


# Тест с некорректной категорией
def test_spending_by_category_invalid_category(test_transactions):
    result = spending_by_category(test_transactions, "несуществующая")
    assert result.empty


# Тест с пустым DataFrame
def test_spending_by_category_empty_dataframe():
    empty_df = pd.DataFrame(["Дата операции", "Сумма операции", "Категория"])
    result = spending_by_category(empty_df, "продукты")
    assert result.empty


# Тест с некорректной датой
def test_spending_by_category_invalid_date():
    invalid_date_df = pd.DataFrame(
        {"Дата операции": "некорректная_дата", "Сумма операции": -1712.00, "Категория": "Продукты"}, index=[0]
    )

    result = spending_by_category(invalid_date_df, "продукты")
    assert result.empty


# Тест с некорректным форматом даты
def test_spending_by_category_invalid_date_format():
    invalid_date_df = pd.DataFrame(
        {"Дата операции": ["2025-03-20 12:00:00"], "Сумма операции": [-1712.00], "Категория": ["Продукты"]}
    )

    result = spending_by_category(invalid_date_df, "продукты")

    # Проверяем, что результат пустой
    assert result.empty


# Тест с датой вне периода
def test_spending_by_category_out_of_range_date(test_transactions):
    result = spending_by_category(test_transactions, "продукты", "01.01.2023")
    assert result.empty
