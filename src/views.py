from datetime import datetime
import logging
import os

from pandas.core.interchange.dataframe_protocol import DataFrame

from src.utils import get_transactions_xlsx
from src.external_api import get_currency_rates, get_stock_prices


dir_path = "../logs"
if not os.path.isdir(dir_path):
    os.mkdir(path=dir_path)


logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/views.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_hello_str(time: int) -> str:
    """Функция, которая принимает на вход время
        и возвращает строку с корректным приветствием"""

    if 5 < time < 12:
        return "Доброе утро"
    elif 11 < time < 18:
        return "Добрый день"
    elif 17 < time < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_cards(df: DataFrame) -> list:
    """Функция, которая принимает на вход DataFrame
        и возвращает список карт и информацию о них"""

    cards = []
    for index, row in df.iterrows():
        cards.append({
            "last_digits": row["Номер карты"][1:],
            "total_spent": row["Сумма платежа"],
            "cashback": round(-1*row["Сумма платежа"]/100, 2)
            })
    return cards


def get_top_transactions(df: DataFrame) -> list:
    """Функция, которая принимает на вход DataFrame
        и возвращает список из транзакций"""

    transactions = []
    for index, row in df.iterrows():
        transactions.append({
            "date": row["Дата платежа"],
            "amount": row["Сумма платежа"],
            "category": row["Категория"],
            "description": row["Описание"]
        })
    return transactions


def main_page(str_date: str) -> dict:
    """Функция главной страницы, которая принимает на вход строку с датой
        и временем в формате YYYY-MM-DD HH:MM:SS и возвращает JSON-ответ"""

    data = {}
    logger.info("Определение времени суток и запись приветственного сообщения")
    try:
        date = datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        logger.error(f"Некорректный формат времени: {str_date}")
        raise ValueError
    data["greeting"] = get_hello_str(date.time().hour)

    try:
        logger.info("Начало работы с файлом")
        df = get_transactions_xlsx("../data/operations.xlsx")
    except FileNotFoundError as err:
        logger.error(f"Ошибка открытия файла: {str(err)}")
        raise FileNotFoundError("404")

    df = df[df["Сумма платежа"] < 0]
    top_transactions = df.sort_values(by="Сумма платежа").head(5)
    df = df.groupby("Номер карты").sum().reset_index()
    logger.info("Заполнение словаря данными")
    data["cards"] = get_cards(df)
    data["top_transactions"] = get_top_transactions(top_transactions)
    data["currency_rates"] = get_currency_rates()
    data["currency_rates"] = get_stock_prices()

    return data
