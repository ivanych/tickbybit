#!/usr/bin/env python

from tickbybit import settings
from tickbybit.files import pair

# Настройки
settings = settings(dirpath='.settings')

# Пара сравниваемых прайсов
tickers_pair = pair(settings, dirpath='.tickers')

# Изменения в отслеживаемых тикерах
tickers_diff = tickers_pair.diff(settings)

# Вывод изменений
diffs = tickers_diff.alert()

if diffs:
    for ticker_diff in diffs:
        print(ticker_diff.to_json())
else:
    print("Уведомлений нет.")
