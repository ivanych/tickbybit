from typing import Any, Literal
import re
import logging
from pprint import pformat

from pydantic import BaseModel, ConfigDict, Field, field_validator

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

    def get_key(self, path: str) -> Any:

        # Узлы пути
        nodes = path.split(".")
        logger.info('        nodes = %s', nodes)

        obj = self._transit_obj(nodes, enable_append=True)
        logger.info('          obj = %s', pformat(obj))

        return obj WIP

    def set_key(self, path: str, value: Any = None) -> dict:

        # Узлы пути
        nodes = path.split(".")
        logger.info('        nodes = %s', nodes)

        transit_nodes = nodes[0:-1]
        logger.info('transit_nodes = %s', transit_nodes)

        # Обработка последнего узла отличается от прочих, поэтому отделяем его для отдельной обработки
        last_node = nodes[-1]
        logger.info('    last_node = %s', last_node)

        obj = self._transit_obj(transit_nodes, enable_append=True)
        logger.info('          obj = %s', pformat(obj))

        logger.info('        value = %s', pformat(value))

        self._set_obj(obj, last_node, value)
        logger.info('      new obj = %s', pformat(obj))

        return self.model_dump()

    def del_key(self, path: str) -> dict:

        # Узлы пути
        nodes = path.split(".")
        logger.info('        nodes = %s', nodes)

        transit_nodes = nodes[0:-1]
        logger.info('transit_nodes = %s', transit_nodes)

        # Обработка последнего узла отличается от прочих, поэтому отделяем его для отдельной обработки
        last_node = nodes[-1]
        logger.info('    last_node = %s', last_node)

        obj = self._transit_obj(transit_nodes)
        logger.info('          obj = %s', pformat(obj))

        self._del_obj(obj, last_node)
        logger.info('      new obj = %s', pformat(obj))

        return self.model_dump()

    def _transit_obj(self, transit_nodes: list[str], enable_append: bool = False) -> Any:
        # Режем узел пути с индексом (атрибут[индекс]) на атрибут и индекс.
        # Если вместо числового индекса указан '+', то это добавление нового элемента.
        # ('-' на самом деле тут можно было бы не указывать и не распознавать,
        # потому что удалять промежуточные элементы всё-равно нельзя,
        # но для изящности сообщения об ошибке сделаем обработку '-')
        # Скобок с индексом в узле может не быть, тогда будет запомнен только атрибут.
        renode = re.compile(r'^(.+?)(?:\[(\d+|\+|\-)\])?$')

        obj = self

        # Обработка транзитных узлов
        for node in transit_nodes:
            matches = renode.findall(node)

            # Обращение к индексу (если индекса нет, то в matches[0][1] будет пустая строка '')
            if matches[0][1]:
                attr = getattr(obj, matches[0][0])

                # Добавлять промежуточную ноду можно только при установке ключа, но не при удалении
                if matches[0][1] == '+' and enable_append:
                    logger.info('%s.append()', attr.__class__.__name__)

                    attr.append()
                    obj = attr[-1]
                elif matches[0][1] == '-':
                    raise ValueError('Нельзя удалять промежуточные элементы пути')
                else:
                    i = int(matches[0][1])
                    obj = attr[i]
            # Обращение к атрибуту
            else:
                obj = getattr(obj, node)

            logger.info('  transit obj = %s.%s = %s', obj.__class__.__name__, node, pformat(obj))

        return obj

    def _set_obj(self, obj, node, value) -> None:
        # Обработка последнего узла
        # Режем узел пути с индексом (атрибут[индекс]) на атрибут и индекс
        # Если вместо числового индекса указан '+', то это добавление нового элемента
        # Скобок с индексом в узле может не быть, тогда будет запомнен только атрибут
        renode = re.compile(r'^(.+?)(?:\[(\d+|\+)\])?$')
        matches = renode.findall(node)

        # Обращение к индексу (если индекса нет, то в matches[0][1] будет пустая строка '')
        if matches[0][1]:
            attr = getattr(obj, matches[0][0])

            if matches[0][1] == '+':
                logger.info('%s.append(%s)', attr.__class__.__name__, pformat(value))
                attr.append(value)
            else:
                i = int(matches[0][1])
                logger.info('%s[%s] = %s', attr.__class__.__name__, i)
                attr[i] = value
        else:
            logger.info('setattr(%s, %s, %s)', obj.__class__.__name__, node, pformat(value))
            setattr(obj, node, value)

    def _del_obj(self, obj, last_node):
        # Обработка последнего узла
        # Режем узел пути с индексом (атрибут[индекс]) на атрибут и индекс
        # Если вместо числового индекса указан '-', то это удаление последнего элемента
        # Скобок с индексом в узле может не быть, тогда будет запомнен только атрибут
        renode = re.compile(r'^(.+?)(?:\[(\d+|\-)\])?$')
        matches = renode.findall(last_node)

        # Обращение к индексу (если индекса нет, то в matches[0][1] будет пустая строка '')
        if matches[0][1]:
            attr = getattr(obj, matches[0][0])

            if matches[0][1] == '-':
                logger.info('%s.pop()', attr.__class__.__name__)
                attr.pop()
            else:
                i = int(matches[0][1])
                logger.info('%s.pop(%s)', attr.__class__.__name__, i)
                attr.pop(i)
        # Обращение к атрибуту
        else:
            raise ValueError('Удалять можно только элементы списка')
