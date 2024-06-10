from typing import Any, Literal
import re
import logging

from pydantic import BaseModel, ConfigDict, Field, field_validator
from jsonpath_ng import parse
from pprint import pformat

from tickbybit.models.settings.triggers.triggers import Triggers

logger = logging.getLogger(__name__)

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
    format: Literal[
        'json', 'yaml',
        'str1', 'str1p', 'str2', 'str2p',
        'tpl1pa', 'tpl1pc', 'tpl1ps', 'tpl2pa', 'tpl2pc', 'tpl2ps'
    ] = Field(default='json')
    is_auto: bool = Field(default=False)
    triggers: Triggers = Field(default_factory=Triggers)

    model_config = ConfigDict(validate_assignment=True)

    @field_validator('format', mode='before')
    @classmethod
    def default_format(cls, v: str) -> str:
        return v if v is not None \
            else cls.model_fields['format'].default

    @field_validator('is_auto', mode='before')
    @classmethod
    def default_is_auto(cls, v: bool) -> bool:
        return v if v is not None \
            else cls.model_fields['is_auto'].default

    @field_validator('triggers', mode='before')
    @classmethod
    def default_triggers(cls, v: Triggers) -> Triggers:
        return v if v is not None \
            else cls.model_fields['triggers'].default_factory()

    @classmethod
    def new(cls):  # pragma: no cover
        return Settings(**DEFAULT_SETTINGS)

    def set_key(self, path: str, value: Any = None) -> dict:

        # Узлы пути
        nodes = path.split(".")
        logger.info('        nodes = %s', nodes)

        transit_nodes = nodes[0:-1]
        logger.info('transit_nodes = %s', transit_nodes)

        # Обработка последнего узла отличается от прочих, поэтому отделяем его для отдельной обработки
        last_node = nodes[-1]
        logger.info('    last_node = %s', last_node)

        # Режем узел пути с индексом (атрибут[индекс]) на атрибут и индекс
        # Если вместо числового индекса указан '+', то это добавление нового элемента
        # Скобок с индексом в узле может не быть, тогда будет запомнен только атрибут
        renode = re.compile(r'^(.+?)(?:\[(\d+|\+)\])?$')

        obj = self

        # Обработка транзитных узлов
        for node in transit_nodes:
            matches = renode.findall(node)

            # Если индекса нет, то в matches[0][1] будет пустая строка ''
            if matches[0][1]:
                attr = getattr(obj, matches[0][0])

                if matches[0][1] == '+':
                    logger.info('%s.append()', attr.__class__.__name__)
                    attr.append()
                    obj = attr[-1]
                else:
                    i = int(matches[0][1])
                    obj = attr[i]
            else:
                obj = getattr(obj, node)

            logger.info('  transit obj = %s.%s = %s', obj.__class__.__name__, node, pformat(obj))

        logger.info('          obj = %s', pformat(obj))
        logger.info('        value = %s', pformat(value))

        # Обработка последнего узла
        # Режем узел пути с индексом (атрибут[индекс]) на атрибут и индекс
        # Если вместо числового индекса указан '+', то это добавление нового элемента
        # Скобок с индексом в узле может не быть, тогда будет запомнен только атрибут
        renode = re.compile(r'^(.+?)(?:\[(\d+|\+)\])?$')
        matches = renode.findall(last_node)

        # Если индекса нет, то в matches[0][1] будет пустая строка ''
        if matches[0][1]:
            attr = getattr(obj, matches[0][0])

            if matches[0][1] == '+':
                attr.append(value)
            else:
                i = int(matches[0][1])
                attr[i] = value
        else:
            logger.info('setattr(%s, %s, %s)', obj.__class__.__name__, last_node, value)
            setattr(obj, last_node, value)

        logger.info('      new obj = %s', pformat(obj))

        return self.model_dump()

    def delete_key(self, path: str) -> dict:  # pragma: no cover
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
