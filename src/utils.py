import logging
import os
import re
from datetime import datetime
from typing import Any, Dict, List

import openpyxl
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv('../.env')

API_KEY = os.getenv('API_KEY')
"""Создаем логгер для логирования функций и записываем логи в директорию logs"""
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: %(name)s %(funcName)s - %(levelname)s - %(message)s',
                    filename='../logs/utils.log',  # Запись логов в файл
                    filemode='w')  # Перезапись файла при каждом запуске
logger = logging.getLogger("utils.py")


def read_transactions_from_xlsx(file_path: str) -> List[Dict[str, Any]]:
    """Функция считывающая информацию XLSX формата с заданного файла,
    и возвращающая список словарей с данными"""
    transactions = []
    try:
        logger.info("Открываем файл...")
        excel_transactions = pd.read_excel(file_path)
        # print(excel_transactions.shape)
        logger.info("Файл корректный, возвращаем его содержимое")
        for index, row in excel_transactions.iterrows():
            transactions.append(dict(row))

        return transactions

    except FileNotFoundError:
        logger.warning("Файл не найден, неверный путь до файла")
        return []


def get_greeting(date: datetime) -> str:
    hour = date.hour
    if 5 <= hour < 12:
        return f"Доброе утро, сегодня {datetime.now().strftime('%d.%m.%Y')}"
    elif 12 <= hour < 17:
        return f"Добрый день, сегодня {datetime.now().strftime('%d.%m.%Y')}"
    elif 17 <= hour < 22:
        return f"Добрый вечер, сегодня {datetime.now().strftime('%d.%m.%Y')}"
    else:
        return f"Доброй ночи, сегодня {datetime.now().strftime('%d.%m.%Y')}"


def get_currency_rates(currencies: List[str]) -> List[Dict[str, float]]:
    rates = []
    for currency in currencies:
        try:
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{currency}")
                                    # headers={'apikey': API_KEY})
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            rates.append({"currency": currency, "rate": data["rates"]["RUB"]})
        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе курса валюты {currency}: {e}")
    return rates


def get_stock_prices(stocks: List[str]) -> List[Dict[str, float]]:
    prices = []
    for stock in stocks:
        try:
            response = requests.get(f"https://api.twelvedata.com/time_series?apikey=ab395b222dbb4a61ba0453d146af084b&interval=1day&format=JSON&type=stock&symbol={stock}&start_date=2024-07-17 15:15:00&timezone=Europe/Moscow")
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            prices.append({"stock": stock, "price": data["values"][0]["close"]})
        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе цены акции {stock}: {e}")
    return prices


print(get_greeting(datetime.now()))
# print(get_currency_rates(['USD', 'EUR', 'GBP']))
# print(get_stock_prices(['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN']))

# print(read_transactions_from_xlsx("../data/operations.xlsx"))
