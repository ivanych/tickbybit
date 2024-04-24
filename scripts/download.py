#!/usr/bin/env python

import asyncio

from tickbybit.bybit import tickers
from tickbybit.files import save, prune


async def main():
    new_tickers = await tickers()

    await save(new_tickers['tickers'], time=new_tickers['time'], dirpath='.tickers')

    pruned = prune(period=5 * 60 * 1000, interval=60 * 1000, dirpath='.tickers')


asyncio.run(main())
