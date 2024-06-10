from typing import Any
import logging
import yaml

from jsonpath_ng import parse

logger = logging.getLogger(__name__)


def _load(file: str) -> dict:
    with open(file) as fd:
        result = yaml.safe_load(fd)

        logger.info("Load file")

        return result


def _save(data: dict, file: str) -> None:
    with open(file, mode='w') as fd:
        yaml.safe_dump(data, fd, allow_unicode=True)

        logger.info("Save file")


def get_all(file: str) -> dict:
    return _load(file)


def get_key(file: str, path: str) -> Any:
    jsonpath = parse(path)

    settings_old = _load(file)

    matches = jsonpath.find(settings_old)

    logger.info("Get key %s", path)

    if matches:
        return matches[0].value


def set_key(file: str, path: str, value: Any = None) -> None:
    jsonpath = parse(path)

    settings_old = _load(file)

    # TODO Тут есть косяк — если settings_old=None (т.е. если исходных данных ещё нет),
    # то ключ не создаётся, возвращается None.
    # Нужен костыль — файл с настройками нужно создавать не пустым, а хоть с какими-нибудь данными,
    # например с пуcтым словарём {}.
    # Надо что-то с этим придумать.
    settings_new = jsonpath.update_or_create(settings_old, value)

    _save(data=settings_new, file=file)

    logger.info("Set key %s", path)


def del_key(file: str, path: str) -> None:
    jsonpath = parse(path)

    settings_old = _load(file)

    settings_new = jsonpath.filter(lambda d: True, settings_old)

    _save(data=settings_new, file=file)

    logger.info("Del key %s", path)
