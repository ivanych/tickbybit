import logging

from tickbybit.bybit import tickers
from tickbybit.files import save, prune

logger = logging.getLogger(__name__)


async def download_new_tickers(dirpath: str) -> None:
    new_tickers = await tickers()
    await save(new_tickers['tickers'], time=new_tickers['time'], dirpath=dirpath)


async def prune_old_tickers(period: int, interval: int, dirpath: str) -> None:
    prune(period=period, interval=interval, dirpath=dirpath)
