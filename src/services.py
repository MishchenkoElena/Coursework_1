import json
import os
import logging
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

from src.logger import get_logger

# Настройка логирования
logger = get_logger("services", "../logs/services.log", logging.INFO)


def read_transactions_from_excel(input_file: str) -> List[Dict[str, Any]]:
    """Функция читает транзакции из Excel-файла и возвращает их в виде списка словарей"""
    try:
        df = pd.read_excel(input_file)

        logger.info("Преобразуем DataFrame в список словарей")
        transactions = df.to_dict(orient="records")

    except FileNotFoundError:
        logging.error(f"Файл не найден: {input_file}")
        raise
    except pd.errors.ParserError as e:
        logging.error(f"Ошибка при чтении Excel файла: {e}")
        raise
    return transactions


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму, которая могла бы быть отложена в Инвесткопилку за указанный месяц
    """

    try:
        target_month = datetime.strptime(month, "%Y-%m")
        total_savings = 0

        logger.debug(
            "Рассчитываем сумму накоплений для Инвесткопилки по каждой операции и общую сумму накоплений за " "месяц"
        )
        for transaction in transactions:

            transaction_date = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")

            if (
                    transaction_date.year == target_month.year
                    and transaction_date.month == target_month.month
                    and transaction["Сумма операции"] < 0
            ):
                amount = abs(transaction["Сумма операции"])
                saving = limit - (amount % limit)
                total_savings += saving

                logging.debug(
                    f"Дата операции: {transaction['Дата операции']}, сумма: {transaction['Сумма операции']}, "
                    f"накопление: {saving}, Общая сумма накоплений за месяц: {total_savings}"
                )

            result_data = {
                "Месяц": month,
                "Лимит округления": limit,
                "Общая сумма накоплений за месяц": round(total_savings, 2),
            }

            result_json = json.dumps(result_data, ensure_ascii=False, indent=4)

        return result_json

    except ValueError as e:
        logging.error(f"Ошибка при обработке данных: {e}")
        raise ValueError("Неверный формат данных")

# # Пример использования
# if __name__ == "__main__":
#     input_file = os.path.abspath('../data/operations.xlsx')
#     transactions = read_transactions_from_excel(input_file)
#     result = investment_bank("2021-10", transactions, 50)
#     print(result)
