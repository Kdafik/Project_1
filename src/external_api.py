import logging
import os
import json

import requests
from dotenv import load_dotenv


dir_path = "../logs"
if not os.path.isdir(dir_path):
    os.mkdir(path=dir_path)


logger = logging.getLogger("external_api")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/external_api.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_stock_prices() -> list:
    """Функция, которая использует API для получения
        курса валют и возвращает список из курсов валют,
        указанных в пользовательском файле user_settings.json"""

    load_dotenv()
    logger.info("Открытие пользовательского файла")
    with open('../user_settings.json') as f:
        logger.info("Чтение данных из файла")
        data = json.load(f)

    stock_prices = []
    for stock in data["user_stocks"]:
        logger.info(f"Использование API для получения информации об {stock}")
        headers = {"ticker": stock,
        "X-Api-Key": os.getenv("API_KEY_PRICE")}
        api_url = "https://api.api-ninjas.com/v1/sp500"
        response = requests.get(api_url, headers).json()
        stock_prices.append({"stock": response[0]["ticker"],
                             "price": int(response[0]["cik"])})

    return stock_prices


def get_currency_rates() -> list:
    """Функция, которая использует API для получения
        стоимости акций из S&P500 и возвращает список из акций,
        указанных в пользовательском файле user_settings.json"""

    load_dotenv()
    logger.info("Открытие пользовательского файла")
    with open('../user_settings.json') as f:
        logger.info("Чтение данных из файла")
        data = json.load(f)

    currency_rates = []

    for currency in data["user_currencies"]:
        logger.info(f"Использование API для получения курса {currency}")
        headers = {
            "get": "rates",
            "pairs": f"{currency}RUB",
            "key": os.getenv("API_KEY_RATE")
        }
        api_url = "https://currate.ru/api/?"
        response = requests.get(api_url, headers).json()
        currency_rates.append({"currency": currency, "rate": round(float(response["data"][f"{currency}RUB"]), 2)})
    return currency_rates
