import pandas as pd
import pytest


#
# @pytest.fixture
# def test_data():
#     return {"Дата операции": ["2025-01-01", "2025-01-02"], "Сумма операции": [100, 200], "Описание": ["Оплата",
#                                                                                                     "Возврат"]}


@pytest.fixture
def test_file(test_data, tmp_path):
    test_file = tmp_path / "test_transactions.xlsx"
    df = pd.DataFrame(test_data)
    df.to_excel(test_file, index=False)
    yield test_file
    test_file.unlink()


@pytest.fixture
def valid_transactions():
    return [
        {"Дата операции": "20.03.2025 12:00:00", "Сумма операции": -1712.00},
        {"Дата операции": "25.03.2025 15:00:00", "Сумма операции": -49.00},
        {"Дата операции": "05.03.2025 10:00:00", "Сумма операции": -1000.00},
        {"Дата операции": "15.03.2025 14:00:00", "Сумма операции": -100.00},
    ]


@pytest.fixture
def test_transactions():
    return pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(
                ["20.03.2025 12:00:00", "25.03.2025 15:00:00", "05.03.2025 10:00:00"], format="%d.%m.%Y %H:%M:%S"
            ),
            "Сумма операции": [-1712.00, -49.00, -1000.00],
            "Категория": ["Продукты", "Транспорт", "Продукты"],
        }
    )


@pytest.fixture
def test_data():
    return {
        "Дата операции": [
            "01.01.2025 00:00:00",
            "02.01.2025 00:00:00",
            "03.01.2025 00:00:00",
            "04.01.2025 00:00:00",
            "05.01.2025 00:00:00",
            "06.01.2025 00:00:00",
            "07.01.2025 00:00:00",
            "08.01.2025 00:00:00",
            "09.01.2025 00:00:00",
            "10.01.2025 00:00:00",
            "11.01.2025 00:00:00",
            "12.01.2025 00:00:00",
            "13.01.2025 00:00:00",
            "14.01.2025 00:00:00",
            "15.01.2025 12:00:00",
            "01.02.2025 12:00:00",
            "15.02.2025 12:00:00",
            "01.03.2025 12:00:00",
        ],
        "Сумма операции": [100, 200, 300, 400, 500, 600, 700, 800, 900, 750, 320, 850, 120, 1200, 940, 710, 300, 400],
    }


@pytest.fixture
def test_df():
    data = {
        "Дата операции": pd.to_datetime(
            ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", "2025-01-05", "2025-01-06"]
        ),
        "Сумма платежа": [1000.567, 500.123, 1500.789, 200.999, 1200.456, 800.111],
        "Категория": ["Продукты", "Транспорт", "Продукты", "Развлечения", "Продукты", "Транспорт"],
        "Описание": [
            "Покупка в магазине",
            "Оплата проезда",
            "Покупка продуктов",
            "Кинотеатр",
            "Супермаркет",
            "Автобус",
        ],
    }
    return pd.DataFrame(data)
