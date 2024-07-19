from utils import (read_transactions_from_xlsx, get_greeting, get_info_cards,
                   top_transactions, get_currency_rates, get_stock_prices)

import json


def views() -> str:
    info_file = read_transactions_from_xlsx("../data/operations.xlsx")  # Открываем файл с операциями

    with open("../user_settings.json", encoding="utf-8") as f:  # открываем польз. настройки по акциям и валютам
        load_json_info = json.load(f)

    information_user = dict()

    information_user["greeting"] = get_greeting()  # приветствие
    information_user["cards"] = get_info_cards(info_file)  # получения инфо о картах по параметрам из файла
    information_user["top_transactions"] = top_transactions(info_file)  # вывод топ транзакций по сумме
    information_user["currency_rates"] = get_currency_rates(load_json_info["user_currencies"])
    # получения текущего курса валют(валюты из польз. настроек)
    information_user["stock_prices"] = get_stock_prices(load_json_info["user_stocks"])
    # получения текущего курса стоимости акций (акции из польз. настроек)

    return json.dumps(information_user, ensure_ascii=False, indent=4)


print(views())
