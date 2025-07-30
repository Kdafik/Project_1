import os
import logging


from pandas import DataFrame


dir_path = "../logs"
if not os.path.isdir(dir_path):
    os.mkdir(path=dir_path)


logger = logging.getLogger("services")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/services.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def search_description(search_line: str, df: DataFrame) -> DataFrame:
    """Принимает строку для поиска и объект Dataframe
        и возвращает DataFrame с транзакциями,
        содержащими строку в описании или категории"""

    logger.info("Фильтрация транзакций по строке")
    search_list = df[(df["Категория"].str.contains(search_line, regex=True, na=False))
                     | (df["Описание"].str.contains(search_line, regex=True, na=False))]
    return search_list
