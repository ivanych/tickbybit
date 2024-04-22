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
for ticker_diff in tickers_diff.alert():
    print(ticker_diff.to_json())
