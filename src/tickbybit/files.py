import os
import json
import aiofiles
import aiofiles.os

def pair(settings: dict, dirpath: str) -> dict:
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
    print(f'new_file {new_file}')

    # Старый файл — первый файл в списке, который старше самого первого файла не более, period (каламбур, да...)
    old_file = _old(files, settings['period'])

    result = {}

    # Прочитать файлы
    old_fd = open(f'{dirpath}/{old_file}')
    result['old'] = json.load(old_fd)

    new_fd = open(f'{dirpath}/{new_file}')
    result['new'] = json.load(new_fd)

    return result


def _files(dirpath: str) -> list[int]:
    files = os.listdir(dirpath)

    return sorted(map(int, files), reverse=True)


def _old(files: list[int], period: int) -> int:
    """
    Определить старый файл.

    Это файл, который как можно старше первого файла, но не старше, чем на period.

    Для устранения "дребезга" добавляем к периоду 10 секунд.

    :param files: Список названий файлов.
    :param period: Период сравнения (миллисекунды).
    :return: Название старого файла.
    """
    # Возраст старого файла
    debounce = 10 * 1000
    age = files[0] - period - debounce

    result = None

    for file in files:

        if file > age:
            result = file
            continue
        else:
            break

    print(f'_old: {result}')

    return result


async def save(tickers: dict, dirpath: str) -> None:
    async with aiofiles.open(f'{dirpath}/{tickers["time"]}', mode='w') as fd:
        await fd.write(tickers["json"])

    print(f'save {tickers["time"]}')


def prune(period: int, dirpath: str) -> list:
    # Список имеющихся файлов
    files = _files(dirpath=dirpath)

    # Возраст старого файла
    debounce = 10 * 1000
    age = files[0] - period - debounce

    result = []

    for file in files:
        if file < age:
            os.remove(f'{dirpath}/{file}')
            result.append(file)

    print(f'prune {result}')

    return result
