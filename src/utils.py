import os
import logging

import pandas as pd
import pandas.errors
from pandas import DataFrame


dir_path = "../logs"
if not os.path.isdir(dir_path):
    os.mkdir(path=dir_path)


logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/utils.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_transactions_xlsx(path: str) -> DataFrame:
    """Принимает на вход путь к xlsx файлу с транзакциями
        и возвращает объект DataFrame"""

    try:
        logger.info(f"Открытие файла {path}")
        if os.path.getsize(path) == 0:
            logger.error("Файл пустой")
            raise pandas.errors.EmptyDataError("empty")
        df = pd.read_excel(path, parse_dates=True)
        logger.info("Чтение данных из файла")
        return df
    except FileNotFoundError:
        logger.error(f"Не найден файл {path}")
        raise FileNotFoundError("404")
