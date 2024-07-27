import datetime
import logging

import pandas as pd

from src.utils import read_transactions_from_xlsx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(name)s %(funcName)s - %(levelname)s - %(message)s",
    filename="../logs/reports.log",
    filemode="w",
)

decorator_logger = logging.getLogger("spending_result")
logger = logging.getLogger("reports.py")
info_df = read_transactions_from_xlsx("../data/operations.xlsx")  # Открываем файл с операциями


def spending_result(path_file: str = "../data/spending_result.csv"):
    """Функция-декоратор, для функции, которая возвращает траты по заданной категории за последние три месяца """
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result.to_csv(path_file)

            decorator_logger.info("Декоратор отработал, записал результат функции в файл")

            return result

        return wrapper

    return decorator


@spending_result()
def spending_by_category(transactions: pd.DataFrame, category: str, date: str = None) -> pd.DataFrame:
    """
    Функция принимает на вход: датафрейм с транзакциями, название категории и опциональную дату.
    Если дата не передана, то берется текущая дата.
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    """
    sort_transactions = transactions.sort_values(by="Дата платежа", ascending=False)

    if date is None:
        date = datetime.datetime.now().strftime("%d.%m.%Y")

    date_split = date.split(".")
    three_months_ago = int(date_split[1]) - 3

    date_obj = datetime.datetime.strptime(date, "%d.%m.%Y")
    date_three_month_ago = date_obj.replace(month=three_months_ago)

    slice_time_first = date_three_month_ago.strftime("%d.%m.%Y")

    file_to_data = sort_transactions[
        (sort_transactions["Дата платежа"] >= slice_time_first) & (sort_transactions["Дата платежа"] <= date)
    ]

    sort_by_category = file_to_data[(file_to_data["Категория"] == category)]

    logger.info("Функция отработала, вернула результат")
    return pd.DataFrame(sort_by_category)


print(spending_by_category(info_df, "Фастфуд", "20.05.2020"))
