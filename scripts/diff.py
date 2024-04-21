#!/usr/bin/env python

from tickbybit import settings
from tickbybit.files import pair

# Настройки
settings = settings(dirpath='.settings')

# Пара сравниваемых прайсов
tickers_pair = pair(settings, dirpath='.tickers')

# Изменения в отслеживаемых тикерах
tickers_diff = tickers_pair.diff(settings)

for ticker_diff in tickers_diff:
    print(ticker_diff.to_json())
