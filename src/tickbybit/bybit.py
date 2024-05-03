import logging

import httpx

logger = logging.getLogger(__name__)


async def get_market_tickers() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url='https://api.bybit.com/v5/market/tickers',
            params={
                'category': 'linear',
            },
        )

        return response.json()


async def tickers() -> dict:
    bybit_tickers = await get_market_tickers()

    time = int(bybit_tickers['time'])

    tickbybit_tickers = {
        ticker['symbol']: ticker for ticker in bybit_tickers['result']['list']
    }

    logger.info("Загружен и приведён к внутреннему формату новый прайс %s", time)

    return {
        'time': time,
        'tickers': tickbybit_tickers
    }
