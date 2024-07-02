import logging

from tickbybit.bybit import tickers
from tickbybit.files import save, prune

logger = logging.getLogger(__name__)


async def download_new_tickers(tickers_dir: str) -> None:
    new_tickers = await tickers()
    await save(new_tickers['tickers'], time=new_tickers['time'], tickers_dir=tickers_dir)

    logger.info("Загружен новый прайс")


async def prune_old_tickers(tickers_dir: str, ttl: int) -> None:
    """

    :param tickers_dir: каталог с прайсами
    :param ttl: время жизни прайса (в секундах)
    :return: None
    """
    prune(tickers_dir=tickers_dir, ttl=ttl)

    logger.info("Удалены старые старые прайсы")
