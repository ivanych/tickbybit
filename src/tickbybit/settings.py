from typing import Any
import logging
import yaml
import re

from jsonpath_ng import parse

logger = logging.getLogger(__name__)

DEFAULT_SETTINGS = {
    "period": 300000,
    "interval": 60000,
    "format": "json",
    "is_auto": False,
    "filters": {},
    "ticker": {
        "markPrice": {
            "alert_pcnt": 1
        },
        "openInterestValue": {
            "alert_pcnt": 1
        },
    }
}


def _load(file: str) -> dict:
    with open(file) as fd:
        result = yaml.safe_load(fd)

        logger.info("Load file")

        return result


def _save(data: dict, file: str) -> None:
    with open(file, mode='w') as fd:
        yaml.safe_dump(data, fd)

        logger.info("Save file")


def settings(file: str) -> dict:
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


def setup_key(data: dict, path: str, value: Any = None) -> dict:
    jsonpath = parse(path)
    jsonvalue = value

    # Исключения и дефолты
    # tickers
    if re.match('c\d', path):
        pass

    elif path == 'tickers':
        raise Exception(f'Нельзя устанавливать ключ tickers')

    elif re.match('is_auto$', path):
        vals = ['true', 'false']
        val = '|'.join(vals)
        assert re.match(f'({val})$', value), f'Допустимые значения: {vals}'
        jsonvalue = True if value == 'true' else False

    elif re.match('format$', path):
        vals = ['json', 'yaml', 'str1', 'str2', 'str3', 'str4', 'tpl1pa', 'tpl1pc', 'tpl1ps', 'tpl2pc', 'tpl2ps']
        val = '|'.join(vals)
        assert re.match(f'({val})$', value), f'Допустимые значения: {vals}'

    # tickers.[symbol]
    elif re.match('tickers\.\w+$', path):
        # нельзя устанавливать уже установленный ключ
        matches = jsonpath.find(data)
        if matches:
            raise Exception(f'Ключ {path} уже установлен')

        # дефолт
        jsonvalue = DEFAULT_SETTINGS['tickers']

    # filters.suffix
    elif re.match('filters\.suffix$', path):
        pass

    # ticker
    elif re.match('ticker$', path):
        raise Exception(f'Нельзя устанавливать ключ ticker')

    # ticker.[attr].[key]
    elif re.match('ticker\.\w+\.\w+$', path):
        if re.match('ticker\.\w+\.alert_pcnt$', path):
            if value is None:
                jsonvalue = 1
            else:
                # TODO тут надо бы перехватить исключение и вывести более читабельное сообщение
                jsonvalue = float(value)
        else:
            # TODO тут надо бы часть [attr] показывать именно как плейсхолдер [attr], а не как буквальное значение
            raise Exception(f'Ключ {path} не поддерживается')

    else:
        raise Exception(f'Установка ключа {path} пока не реализована')

    settings_new = jsonpath.update_or_create(data, jsonvalue)

    logger.info("Setup key %s: %s", path, jsonvalue)

    return settings_new


def delete_key(data: dict, path: str) -> dict:
    jsonpath = parse(path)

    # Исключения и дефолты
    # tickers
    if path == 'tickers':
        raise Exception(f'Нельзя удалять ключ tickers')

    elif re.match('format$', path):
        raise Exception(f'Нельзя удалять ключ format')

    # filters.suffix
    elif re.match('filters\.suffix$', path):
        pass

    # ticker
    elif re.match('ticker$', path):
        raise Exception(f'Нельзя удалять ключ ticker')

    # ticker.[attr]
    elif re.match('ticker\.\w+$', path):
        # ticker.markPrice - нельзя удалять, хотя бы один атрибут нужно оставить на всякий случай
        if re.match('ticker\.markPrice$', path):
            raise Exception(f'Нельзя удалять ключ ticker.markPrice')
        pass

    # ticker.[attr].[key]
    elif re.match('ticker\.\w+\.\w+$', path):
        raise Exception(f'Нельзя удалять ключ ticker.[attr].[key]')

    else:
        raise Exception(f'Удаление ключа {path} пока не реализовано')

    settings_new = jsonpath.filter(lambda d: True, data)

    logger.info("Delete key %s", path)

    return settings_new
