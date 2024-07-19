import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv('../.env')

API_KEY_VALUES = os.getenv('API_KEY_VALUES')
API_KEY_STOCKS = os.getenv('API_KEY_STOCKS')
"""Создаем логгер для логирования функций и записываем логи в директорию logs"""
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: %(name)s %(funcName)s - %(levelname)s - %(message)s',
                    filename='../logs/utils.log',  # Запись логов в файл
                    filemode='w')  # Перезапись файла при каждом запуске
logger = logging.getLogger("utils.py")


def read_transactions_from_xlsx(file_path: str) -> pd.DataFrame | List:
    """Функция считывающая информацию XLSX формата с заданного файла,
    и возвращающая дата фрейм с данными"""
    try:
        logger.info("Открываем файл...")
        excel_transactions = pd.read_excel(file_path)
        logger.info("Файл корректный, возвращаем его содержимое")

        return excel_transactions

    except FileNotFoundError:
        logger.warning("Файл не найден, неверный путь до файла")
        return []


df = read_transactions_from_xlsx("../data/operations.xlsx")


def get_greeting() -> str:
    """Функция приветствие в зависимости от текущего времени пользователя"""
    hour = datetime.now().hour
    logger.info("Делаем приветствие...")
    if 5 <= hour < 12:
        return f"Доброе утро, сегодня {datetime.now().strftime('%d.%m.%Y')}"
    elif 12 <= hour < 17:
        return f"Добрый день, сегодня {datetime.now().strftime('%d.%m.%Y')}"
    elif 17 <= hour < 22:
        return f"Добрый вечер, сегодня {datetime.now().strftime('%d.%m.%Y')}"
    else:
        return f"Доброй ночи, сегодня {datetime.now().strftime('%d.%m.%Y')}"


def get_info_cards(operations_xlsx: pd.DataFrame) -> List[dict]:
    """Функция, которая принимает DataFrame и сортирует его по заданным параметрам"""
    group_card = operations_xlsx.groupby("Номер карты", as_index=False)
    logger.info("Возвращаем данные...")
    total_sum_cashback = group_card.sum().loc[:, ["Номер карты", "Сумма платежа", "Кэшбэк"]]

    return total_sum_cashback.to_dict(orient="records")


def top_transactions(operations_xlsx: pd.DataFrame) -> list[dict]:
    """Функция, которая принимает DataFrame и выводит топ 5 транзакций"""
    top_5_operation = operations_xlsx.sort_values(by="Сумма платежа").head()
    logger.info("Возвращаем данные...")
    information = top_5_operation.loc[:, ["Дата платежа", "Сумма платежа", "Категория", "Описание"]]

    return information.to_dict(orient="records")


def get_currency_rates(currencies: List[str]) -> List[Dict[str, float]]:
    """ Функция, которая принимает список Валют из пользовательских настроек,
    делает запрос и возвращает список со стоимостью каждой валюты по курсу на сегодня"""
    rates = []
    for currency in currencies:
        try:
            logger.info("Делаем запрос...")
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{currency}",
                                    headers={'apikey': API_KEY_VALUES})
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            logger.info("Запрос корректный, возвращаем данные...")
            rates.append({"currency": currency, "rate": data["rates"]["RUB"]})
        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе курса валюты {currency}: {e}")
    return rates


def get_stock_prices(stocks: List[str]) -> List[Dict[str, float]]:
    """Функция, которая принимает список Акций из пользовательских настроек,
    и возвращает стоимость акций в $ на конец дня"""
    prices = []
    d = datetime.now() - timedelta(days=1)
    date_str = d.strftime('%Y-%m-%d %H:%M:%S')
    for stock in stocks:
        try:
            logger.info("Делаем запрос...")
            response = requests.get(f"https://api.twelvedata.com/time_series?apikey={API_KEY_STOCKS}"
                                    f"&interval=1day&format=JSON&type=stock&symbol={stock}&start_date={date_str}"
                                    f"&timezone=Europe/Moscow")
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            logger.info("Запрос корректный, возвращаем данные...")
            prices.append({"stock": stock, "price": data["values"][0]["close"]})
        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе цены акции {stock}: {e}")
    return prices


# print(get_greeting(datetime.now()))
# with open('../user_settings.json') as f:
#     data_ = json.load(f)
#
# print(get_info_cards(df))
# print(top_transactions(df))
# print(get_currency_rates(data_["user_currencies"]))
# print(get_stock_prices(data_["user_stocks"]))
