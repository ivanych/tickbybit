import httpx


async def tickers() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url='https://api.bybit.com/v5/market/tickers',
            params={
                'category': 'linear',
            },
        )

        response_data = response.json()

        return {
            'time': response_data['time'],
            'json': response.text,
        }
