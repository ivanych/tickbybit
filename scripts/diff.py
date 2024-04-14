#!/usr/bin/env python

from tickbybit import diff, tickers, notify, settings
from tickbybit.files import pair, save, prune

# Настройки
settings = settings()

# Пара сравниваемых прайсов
pair = pair(settings, dirpath='.tickers')

# Изменения в отслеживаемых тикерах
diffs = diff(settings, pair)

for dif in diffs:
    notify(dif)
