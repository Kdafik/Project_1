import logging
import os
from datetime import datetime, timedelta
from typing import Optional

from pandas import DataFrame, to_datetime


dir_path = "../logs"
if not os.path.isdir(dir_path):
    os.mkdir(path=dir_path)


logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/reports.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def spending_by_category(df: DataFrame,
                         category: str,
                         date_str: Optional[str] = None) -> DataFrame:
    """Принимает DataFrame, строку с категорией и датой в формате 'dd.mm.YYYY',
        в случае если не передали дату, то использует текущую дату,
        и возвращает DataFrame с транзакциями по заданной категории
        за последние три месяца(от переданной даты)"""

    logger.info("Определение диапазона, в котором отбирать транзакции")
    if date_str is None:
        date = datetime.now().date()
    else:
        date = datetime.strptime(date_str, "%d.%m.%Y")

    past_date = date - timedelta(days=30*3)

    logger.info("Фильтрация транзакций по категории и дате")
    df["Дата платежа"] = to_datetime(df["Дата платежа"], format="%d.%m.%Y")
    df = df[df["Категория"] == category]
    filtered_transactions = df.loc[(df["Дата платежа"] >= past_date) &
                                   (df["Дата платежа"] <= date)]

    return filtered_transactions
