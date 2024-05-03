import os
import aiofiles
import aiofiles.os
import logging
import pickle

from .tickers_pair import TickersPair
from .tickers import Tickers

logger = logging.getLogger("tickbybit.files")


async def pair(settings: dict, dirpath: str) -> TickersPair:
    """
    Получить пару сравниваемых прайсов из файлового хранилища.

    :param settings: Настройки.
    :param dirpath: Путь к каталогу с файлами.
    :return: Старый и новый прайсы.
    """
    # Список имеющихся файлов
    files = _files(dirpath=dirpath)

    # Новый файл
    new_file = files[0]
    logger.info("Identified new file %s", new_file)

    # Старый файл — первый файл в списке, который старше самого первого файла не более, period (каламбур, да...)
    old_file = _old(files, period=settings['period'], interval=settings['interval'])
    logger.info("Identified old file %s", old_file)

    # Прочитать файлы
    old = await load(time=old_file, dirpath=dirpath)
    new = await load(time=new_file, dirpath=dirpath)

    return TickersPair(
        old=Tickers(time=old_file, tickers=old),
        new=Tickers(time=new_file, tickers=new),
    )


def _files(dirpath: str) -> list[int]:
    files = os.listdir(dirpath)

    return sorted(map(int, files), reverse=True)


def _old(files: list[int], period: int, interval: int) -> int:
    """
    Определить старый файл.

    Это файл, который как можно старше первого файла, но не старше, чем на period+interval.

    :param files: Список названий файлов.
    :param period: Период сравнения (миллисекунды).
    :param interval: Интервал обновления (миллисекунды).
    :return: Название старого файла.
    """
    # Возраст старого файла
    age = files[0] - period - interval

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
