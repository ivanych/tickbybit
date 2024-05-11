import os
from os import getenv

import aiofiles
import aiofiles.os
import logging
import pickle

from .tickers_pair import TickersPair
from .tickers import Tickers

DOWNLOAD_PERIOD = int(getenv('DOWNLOAD_PERIOD'))

logger = logging.getLogger(__name__)


async def pair(interval: int, dirpath: str) -> TickersPair:
    """
    Получить пару сравниваемых прайсов из файлового хранилища.

    :param interval: интервал сравнения, в секундах
    :param dirpath: Путь к каталогу с файлами.
    :return: Старый и новый прайсы.
    """
    # Список имеющихся файлов
    files = _files(dirpath=dirpath)

    # Новый файл
    new_file = files[0]
    logger.info("Определён новый файл (new_file=%s)", new_file)
    new = await load(time=new_file, dirpath=dirpath)

    # Старый файл — первый файл в списке, который старше самого первого файла не более,
    # чем на interval + download_period
    old_file = _old(files, interval=interval, download_period=DOWNLOAD_PERIOD)
    logger.info("Определён старый файл (old_file=%s)", old_file)
    old = await load(time=old_file, dirpath=dirpath)

    return TickersPair(
        interval=interval,
        new=Tickers(time=new_file, tickers=new),
        old=Tickers(time=old_file, tickers=old),
    )


def _files(dirpath: str) -> list[int]:
    files = os.listdir(dirpath)

    return sorted(map(int, files), reverse=True)


def _old(files: list[int], interval: int, download_period: int) -> int:
    """
    Определить старый файл.

    Это файл, который как можно старше первого файла, но не старше, чем на interval + download_period.

    :param files: Список названий файлов.
    :param interval: интервал сравнения, секунды.
    :param download_period: период загрузки новых прайсов, секунды.
    :return: Название старого файла.
    """
    # Возраст старого файла
    age = files[0] - interval * 1000 - download_period * 1000

    result = None

    for file in files:
        if file > age:
            result = file
            continue
        else:
            break

    return result


async def save(tickers: dict, time: int, dirpath: str) -> None:
    tickers_pickle = pickle.dumps(tickers)

    async with aiofiles.open(f'{dirpath}/{time}', mode='wb') as fd:
        await fd.write(tickers_pickle)

    logger.info("Сохранён файл %s", time)


async def load(time: int, dirpath: str) -> dict:
    async with aiofiles.open(f'{dirpath}/{time}', mode='rb') as fd:
        tickers_pickle = await fd.read()

    tickers = pickle.loads(tickers_pickle)

    logger.info("Load file %s", time)

    return tickers


def prune(dirpath: str, ttl: int) -> list:
    # Список имеющихся файлов
    files = _files(dirpath=dirpath)

    # Возраст старого файла
    old = files[0] - ttl

    result = []

    for file in files:
        if file < old:
            os.remove(f'{dirpath}/{file}')
            result.append(file)

    logger.info("Очищены старые файлы %s (new=%s, old=%s, ttl=%s)", result, files[0], old, ttl)

    return result
