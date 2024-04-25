from typing import Any
import yaml
import logging
from jsonpath_ng import parse
import re

logger = logging.getLogger("tickbybit.settings")


def settings(dirpath: str) -> dict:
    filepatch = f'{dirpath}/settings.yaml'

    with open(filepatch) as fd:
        result = yaml.safe_load(fd)

        logger.info("Load settings file")

        return result


def _save(data: dict, dirpath: str):
    filepatch = f'{dirpath}/settings.yaml'

    with open(filepatch, mode='w') as fd:
        yaml.safe_dump(data, fd)

        logger.info("Save settings file")


settings_default = {
    "period": 300000,
    "interval": 60000,
    "format": "json",
    "tickers": {
        "SYMBOL": {
            "markPrice": {
                "alert_pcnt": 1
            },
            "openInterestValue": {
                "alert_pcnt": 1
            }
        }
    }
}


def set_key(dirpath: str, path: str, value: Any = None) -> dict:
    jsonpath = parse(path)
    jsonvalue = value

    settings_old = settings(dirpath=dirpath)

    # Исключения и дефолты
    # tickers
    if path == 'tickers':
        raise Exception(f'Нельзя устанавливать ключ tickers')

    elif re.match('format$', path):
        frmts = ['json', 'yaml', 'str1', 'str2', 'str3', 'str4']
        frmt = '|'.join(frmts)
        assert re.match(f'({frmt})$', value), f'Допустимые форматы: {frmts}'

    # tickers.[symbol]
    elif re.match('tickers\.\w+$', path):
        # нельзя устанавливать уже установленный ключ
        matches = jsonpath.find(settings_old)
        if matches:
            raise Exception(f'Ключ {path} уже установлен')

        # дефолт
        jsonvalue = settings_default['tickers']['SYMBOL']

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

    settings_new = jsonpath.update_or_create(settings_old, jsonvalue)

    logger.info("Set settings key %s: %s", path, jsonvalue)

    _save(data=settings_new, dirpath=dirpath)

    return settings_new


def del_key(dirpath: str, path: str) -> dict:
    jsonpath = parse(path)

    settings_old = settings(dirpath=dirpath)

    # Исключения и дефолты
    # tickers
    if path == 'tickers':
        raise Exception(f'Нельзя удалять ключ tickers')

    elif re.match('format$', path):
        raise Exception(f'Нельзя удалять ключ format')

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

    settings_new = jsonpath.filter(lambda d: True, settings_old)

    logger.info("Del settings key %s", path)

    _save(data=settings_new, dirpath=dirpath)

    return settings_new
