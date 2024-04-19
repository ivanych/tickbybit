import yaml
import logging
from jsonpath_ng import parse
import re
import pprint

logger = logging.getLogger("tickbybit.settings")


def settings(dirpath: str) -> dict:
    filepatch = f'{dirpath}/settings.yaml'

    with open(filepatch) as fd:
        result = yaml.safe_load(fd)

        logger.info("Load settings %s", result)

        return result


def _load(dirpath: str) -> dict:
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


def set_key(dirpath: str, path: str, value: str | list | dict = None) -> dict:
    jsonpath = parse(path)
    jsonvalue = value

    settings_old = _load(dirpath=dirpath)
    pprint.pprint(settings_old)

    # Исключения и дефолты
    if path == 'tickers':
        raise Exception(f'Нельзя устанавливать ключ {path}.')
    elif re.match('tickers\.\w+$', path):
        # Нельзя устанавливать уже установленный ключ
        jsonpath = parse(path)
        matches = jsonpath.find(settings_old)
        if matches:
            raise Exception(f'Ключ {path} уже установлен.')

        jsonvalue = settings_default['tickers']['SYMBOL']


    else:
        raise Exception(f'Ой! Установка ключа {path} пока не доделана.')


    settings_new = jsonpath.update_or_create(settings_old, jsonvalue)

    #pprint.pprint(settings_new)

    _save(data=settings_new, dirpath=dirpath)

    return settings_new


def del_key( dirpath: str, path: str):
    jsonpath = parse(path)

    settings_old = _load(dirpath=dirpath)
    pprint.pprint(settings_old)

    # Исключения и дефолты
    if path == 'tickers':
        raise Exception(f'Нельзя удалять ключ {path}.')
    elif re.match('tickers\.\w+$', path):
        pass


    else:
        raise Exception(f'Ой! Удаление ключа {path} пока не доделано.')


    settings_new = jsonpath.filter(lambda d: True, settings_old)

    #pprint.pprint(settings_new)

    _save(data=settings_new, dirpath=dirpath)

    return settings_new