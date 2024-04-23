#!/usr/bin/env python

import asyncio

from tickbybit import settings
from tickbybit.files import pair


async def main():
    # Настройки
    settings_dict = settings(dirpath='.settings')

    # Пара сравниваемых прайсов
    tickers_pair = await pair(settings_dict, dirpath='.tickers')

    # Изменения в отслеживаемых тикерах
    tickers_diff = tickers_pair.diff(settings_dict)

    # Вывод изменений
    diffs = tickers_diff.all()

    if diffs:
        for ticker_diff in diffs:
            print(ticker_diff.to_json())
    else:
        print("Уведомлений нет.")


asyncio.run(main())
