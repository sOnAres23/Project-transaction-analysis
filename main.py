# for greater simplicity install our package
# https://github.com/twelvedata/twelvedata-python

import requests

response = requests.get(
    "https://api.twelvedata.com/time_series?apikey=ab395b222dbb4a61ba0453d146af084b&interval=1day&format=JSON&type=stock&symbol=AAPL&start_date=2024-07-17 15:15:00&timezone=Europe/Moscow")
data = response.json()
print(data["values"][0]["close"])
