from unittest.mock import patch

import pandas as pd
import pytest

from src.views import main_page, get_cards, get_hello_str, get_top_transactions


@pytest.mark.parametrize('hour, hello', [
    (6, "Доброе утро"),
    (13, "Добрый день"),
    (18, "Добрый вечер"),
    (2, "Доброй ночи")])
def test_get_hello_str(hour, hello):
    assert get_hello_str(hour) == hello


def test_get_cards():
    test_data = {
        "Номер карты": ["*1234", "*5678"],
        "Сумма платежа": [-1000, -2000]
    }
    df = pd.DataFrame(test_data)

    result = get_cards(df)

    assert len(result) == 2
    assert result[0]["last_digits"] == "1234"
    assert result[0]["total_spent"] == -1000
    assert result[0]["cashback"] == 10.0
    assert result[1]["last_digits"] == "5678"
    assert result[1]["total_spent"] == -2000
    assert result[1]["cashback"] == 20.0


def test_get_top_transactions():
    test_data = {
        "Дата платежа": ["2023-01-01", "2023-01-02"],
        "Сумма платежа": [-500, -1000],
        "Категория": ["Еда", "Транспорт"],
        "Описание": ["Ресторан", "Такси"]
    }
    df = pd.DataFrame(test_data)

    result = get_top_transactions(df)

    assert len(result) == 2
    assert result[0]["date"] == "2023-01-01"
    assert result[0]["amount"] == -500
    assert result[0]["category"] == "Еда"
    assert result[0]["description"] == "Ресторан"
    assert result[1]["date"] == "2023-01-02"
    assert result[1]["amount"] == -1000
    assert result[1]["category"] == "Транспорт"
    assert result[1]["description"] == "Такси"


@patch("src.views.get_transactions_xlsx")
@patch("src.views.get_currency_rates")
@patch("src.views.get_stock_prices")
def test_main_page(mock_stock, mock_currency, mock_transactions):
    test_df = pd.DataFrame({
        "Номер карты": ["*1234", "*1234", "*5678"],
        "Сумма платежа": [-100, -200, -300],
        "Дата платежа": ["2023-01-01", "2023-01-02", "2023-01-03"],
        "Категория": ["A", "B", "C"],
        "Описание": ["Desc1", "Desc2", "Desc3"]
    })
    mock_transactions.return_value = test_df
    mock_currency.return_value = {"USD": 75.0}
    mock_stock.return_value = {"AAPL": 150.0}

    result = main_page("2023-01-01 14:00:00")

    assert result["greeting"] == "Добрый день"
    assert len(result["cards"]) == 2
    assert len(result["top_transactions"]) == 3
    assert result["currency_rates"] == {"AAPL": 150.0}

