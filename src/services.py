import logging

import pandas as pd
from src.utils import read_transactions_from_xlsx


"""Создаем логгер для логирования функций и записываем логи в директорию logs"""
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: %(name)s %(funcName)s - %(levelname)s - %(message)s',
                    filename='../logs/services.log',  # Запись логов в файл
                    filemode='w')  # Перезапись файла при каждом запуске
logger = logging.getLogger("services.py")


def filtering_by_search(search_string: str) -> pd.DataFrame:
    """Функция, которая фильтрует транзакции по строке поиска"""
    try:
        info_df = read_transactions_from_xlsx("../data/operations.xlsx")

        search_operations = info_df.loc[
            (info_df["Категория"] == search_string.title())
            | (info_df["Описание"] == search_string.title())
        ]
        logger.info("Функция отработала корректно")
        return search_operations
    except ExceptionGroup:
        logger.warning("функция не отработала, ошибка")


print(filtering_by_search('Связь'))
