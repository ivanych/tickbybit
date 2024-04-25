#!/usr/bin/env python

import sys
import logging
import asyncio

from tickbybit import settings, format
from tickbybit.files import pair

logging.basicConfig(level=logging.INFO, stream=sys.stderr)


async def main():
    # Настройки
    settings_dict = settings(dirpath='.settings')

    # Пара сравниваемых прайсов
    tickers_pair = await pair(settings_dict, dirpath='.tickers')

    # Изменения в отслеживаемых тикерах
    tickers_diff = tickers_pair.diff(settings_dict)

    # Вывод изменений
    diffs = tickers_diff.alert()

    if diffs:
        for ticker_diff in diffs:
            print(format(td=ticker_diff, settings=settings_dict))
    else:
        print("Уведомлений нет.")


asyncio.run(main())
