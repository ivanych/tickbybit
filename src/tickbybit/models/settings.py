from typing import List, Dict, Any
import re

from pydantic import BaseModel
from jsonpath_ng import parse

DEFAULT_SETTINGS = {
    "format": "json",
    "is_auto": False,
    "triggers": [
        {
            "icon": "😀",
            "interval": 60,
            "ticker": {
                "markPrice": {
                    "absolute": 1
                },
                "openInterestValue": {
                    "absolute": 1
                },
                "symbol": {
                    'suffix': "USDT"
                },
            }
        }
    ]
}


class Settings(BaseModel):
    format: str
    is_auto: bool
    triggers: List[Dict[str, Any]]

    @classmethod
    def new(cls):
        return Settings(**DEFAULT_SETTINGS)

    def sorted_triggers(self, reverse: bool = False) -> List[Dict[str, Any]]:
        return sorted(self.triggers, key=lambda x: x['interval'], reverse=reverse)

    def setup_key(self, path: str, value: Any = None) -> dict:
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

        # triggers[*].icon
        elif re.match('triggers\.?\[\d+\]\.icon$', path):
            assert len(value) > 0, 'Нужно указать значение'

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

        settings_new = jsonpath.update_or_create(self.model_dump(), jsonvalue)

        return settings_new

    def delete_key(self, path: str) -> dict:
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

        # triggers[*].icon
        elif re.match('triggers\.?\[\d+\]\.icon$', path):
            pass

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

        settings_new = jsonpath.filter(lambda d: True, self.model_dump())

        return settings_new
