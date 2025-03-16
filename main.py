from typing import Any

import pandas as pd

from src.reports import spending_by_category
from src.services import investment_bank, read_transactions_from_excel
from src.views import home_page


def main() -> Any:
    """Функция для запуска функциональностей всего проекта"""
    print("Функция для запуска всего проекта")


if __name__ == "__main__":
    print("\nГЛАВНАЯ\n")
    date_string = input('Введите дату в формате "YYYY-MM-DD HH:MM:SS" для расчета накоплений:\n')
    result = home_page(date_string)
    print(result)

    print("\nСЕРВИСЫ.ИНВЕСТКОПИЛКА\n")
    month = input('Введите месяц  в формате "ГГГГ-MM" для расчета накоплений:\n')
    limit = int(input("Введите предел, до которого нужно округлять суммы операций (10, 50 или 100):\n"))
    input_file = "data/operations.xlsx"
    transactions = read_transactions_from_excel(input_file)
    result = investment_bank(month, transactions, limit)
    print(result)

    print("\nОТЧЕТЫ.ТРАТЫ ПО КАТЕГОРИЯМ\n")
    input_file = "data/operations.xlsx"
    category = input("Выберите категорию для расчета суммы трат за 3 месяца:\n").lower()
    date = input('Введите дату окончания периода для анализа трат по категории в формате "ГГГГ-ММ-ДД":\n')
    transactions_df = pd.read_excel(input_file)
    result = spending_by_category(transactions_df, category, date)
    print(result)
