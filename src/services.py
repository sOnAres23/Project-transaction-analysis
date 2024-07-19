import logging

import pandas as pd
from utils import read_transactions_from_xlsx


"""Создаем логгер для логирования функций и записываем логи в директорию logs"""
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: %(name)s %(funcName)s - %(levelname)s - %(message)s',
                    filename='../logs/services.log',  # Запись логов в файл
                    filemode='w')  # Перезапись файла при каждом запуске
logger = logging.getLogger("services.py")


def filtering_by_search(search_string: str) -> pd.DataFrame:
    """Фильтруем транзакции по строке поиска"""
    try:
        file_operation = read_transactions_from_xlsx("../data/operations.xlsx")

        search_operations = file_operation.loc[
            (file_operation["Категория"] == search_string.title())
            | (file_operation["Описание"] == search_string.title())
        ]
        logger.info("Функция отработала корректно")
        return search_operations
    except ExceptionGroup:
        logger.warning("функция не отработала, ошибка")


# print(filtering_by_search('Связь'))
