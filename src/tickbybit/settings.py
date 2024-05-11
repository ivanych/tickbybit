from typing import Any
import logging
import yaml
import re

from jsonpath_ng import parse

logger = logging.getLogger(__name__)

DEFAULT_SETTINGS = {
    "format": "json",
    "is_auto": False,
    "triggers": [
        {
            "interval": 60,
            "ticker": {
                "symbol": {
                    'suffix': "USDT"
                },
                "markPrice": {
                    "absolute": 1
                },
                "openInterestValue": {
                    "absolute": 1
                },
            }
        }
    ]
}


def _load(file: str) -> dict:
    with open(file) as fd:
        result = yaml.safe_load(fd)

        logger.info("Load file")

        return result


def _save(data: dict, file: str) -> None:
    with open(file, mode='w') as fd:
        yaml.safe_dump(data, fd, allow_unicode=True)

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

    # Используемые атрибуты тикера
    attrs = ['symbol', 'markPrice', 'openInterestValue']
    attrs_re = f"({'|'.join(attrs)})"

    # format
    if re.match('format$', path):
        vals = ['json', 'yaml', 'str1', 'str1p', 'str2', 'str2p', 'tpl1pa', 'tpl1pc', 'tpl1ps', 'tpl2pa', 'tpl2pc',
                'tpl2ps']
        val = '|'.join(vals)
        assert re.match(f'({val})$', value), f'Допустимые значения: {vals}'

    # is_auto
    elif re.match('is_auto$', path):
        vals = ['true', 'false']
        val = '|'.join(vals)
        assert re.match(f'({val})$', value), f'Допустимые значения: {vals}'
        jsonvalue = True if value == 'true' else False

    # triggers
    elif re.match('triggers$', path):
        raise Exception(f'Нельзя устанавливать ключ triggers')

    # triggers[*]
    elif re.match('triggers\.?\[\d+\]$', path):
        raise Exception(f'Нельзя устанавливать ключ triggers[*]')

    # triggers[*].interval
    elif re.match('triggers\.?\[\d+\]\.interval$', path):
        # TODO тут надо бы перехватить исключение и вывести более читабельное сообщение
        jsonvalue = int(value)

    # triggers[*].ticker
    # пока не поддерживается

    # triggers[*].ticker.[attr]
    # пока не поддерживается

    # triggers[*].ticker.[attr].[key]
    elif re.match(f"triggers\.?\[\d+\]\.ticker\.{attrs_re}\.\w+$", path):
        if re.match('.+absolute$', path):
            if value is None:
                jsonvalue = 1
            else:
                # TODO тут надо бы перехватить исключение и вывести более читабельное сообщение
                jsonvalue = float(value)
        elif re.match('.+suffix$', path):
            if value is None:
                raise Exception(f'Нужно указать значение')
        else:
            # TODO тут надо бы часть [attr] показывать именно как плейсхолдер [attr], а не как буквальное значение
            raise Exception(f'Ключ <code>{path}</code> не поддерживается')

    else:
        raise Exception(f'Установка ключа {path} пока не реализована')

    settings_new = jsonpath.update_or_create(data, jsonvalue)

    logger.info("Setup key %s: %s", path, jsonvalue)

    return settings_new


def delete_key(data: dict, path: str) -> dict:
    jsonpath = parse(path)

    # Исключения и дефолты

    # format
    if re.match('format$', path):
        raise Exception(f'Нельзя удалять ключ format')

    # is_auto
    if re.match('is_auto$', path):
        raise Exception(f'Нельзя удалять ключ is_auto')

    # triggers
    elif re.match('triggers$', path):
        raise Exception(f'Нельзя удалять ключ triggers')

    # triggers[*]
    # пока не поддерживается

    # triggers[*].interval
    elif re.match('triggers\.?\[\d+\]\.interval$', path):
        raise Exception(f'Нельзя удалять ключ triggers[*].interval')

    # triggers[*].ticker
    elif re.match('triggers\.?\[\d+\]\.ticker$', path):
        raise Exception(f'Нельзя удалять ключ triggers[*].ticker')

    # triggers[*].ticker.[attr]
    elif re.match('triggers\.?\[\d+\]\.ticker\.\w+$', path):
        pass

    # triggers[*].ticker.[attr].[key]
    elif re.match('triggers\.?\[\d+\]\.ticker\.\w+\.\w+$', path):
        pass

    else:
        raise Exception(f'Удаление ключа {path} пока не реализовано')

    settings_new = jsonpath.filter(lambda d: True, data)

    logger.info("Delete key %s", path)

    return settings_new
