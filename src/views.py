import logging
from datetime import datetime

from src.utils import (read_transactions_from_xlsx, get_greeting, get_info_cards,
                       top_transactions, get_currency_rates, get_stock_prices)

import json

"""Создаем логгер для логирования функций и записываем логи в директорию logs"""
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: %(name)s %(funcName)s - %(levelname)s - %(message)s',
                    filename='../logs/views.log',  # Запись логов в файл
                    filemode='w')  # Перезапись файла при каждом запуске
logger = logging.getLogger("views.py")


def views(date: str) -> str:
    info_df = read_transactions_from_xlsx("../data/operations.xlsx")  # Открываем файл с операциями
    sort_file = info_df.sort_values(by="Дата платежа", ascending=True)

    date_obj = datetime.strptime(date, "%d.%m.%Y")
    new_date_obj = date_obj.replace(day=1)

    slice_time_last = date_obj.strftime("%d.%m.%Y")
    slice_time_first = new_date_obj.strftime("%d.%m.%Y")

    slice_df_to_data = sort_file[
        (sort_file["Дата платежа"] >= slice_time_first) & (sort_file["Дата платежа"] <= slice_time_last)
        ]
    with open("../user_settings.json", encoding="utf-8") as f:  # открываем польз. настройки по акциям и валютам
        load_json_info = json.load(f)

    information_user = dict()

    information_user["greeting"] = get_greeting()  # приветствие
    information_user["cards"] = get_info_cards(slice_df_to_data)  # получения инфо о картах по параметрам из файла
    information_user["top_transactions"] = top_transactions(slice_df_to_data)  # вывод топ транзакций по сумме
    information_user["currency_rates"] = get_currency_rates(load_json_info["user_currencies"])
    # получения текущего курса валют(валюты из польз. настроек)
    information_user["stock_prices"] = get_stock_prices(load_json_info["user_stocks"])
    # получения текущего курса стоимости акций (акции из польз. настроек)

    return json.dumps(information_user, ensure_ascii=False, indent=4)


# if __name__ == "__main__":
#     print(views('22.05.2020'))
