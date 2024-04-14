#!/usr/bin/env python

import asyncio
from tickbybit import tickers
from tickbybit.files import save, prune


async def main():
    new_tickers = await tickers()
    await save(new_tickers, dirpath='.tickers')

    pruned = prune(dirpath='.tickers', period=5*60*1000)

asyncio.run(main())
