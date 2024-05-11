import re
from typing import Dict, Optional

from pydantic import BaseModel, computed_field


class AttrDiff(BaseModel):
    old: str | None
    new: str
    filters: Optional[Dict[str, Dict[str, float | str | bool]]] = None

    def filter(self, filters: dict) -> bool:
        """
        Проверяет прохождение атрибута через фильтры. Все фильтры атрибута объединяются через "И".

        Возвращает истину, если атрибут проходит через все фильтры.

        :param filters: Словарь с фильтрами для атрибута.
        :return:
        """

        self.filters = {}

        return all(
            map(
                lambda key: getattr(self, key)(key, filters[key]),
                filters
            )
        )


class FloatAttrDiff(AttrDiff):

    @computed_field
    @property
    def pcnt(self) -> float | None:
        return round(
            number=float(self.new) / float(self.old) * 100 - 100,
            ndigits=6,
        ) if self.old is not None else None

    # Фильтры

    def absolute(self, key: str, value: float) -> bool:
        """
        Проверяет прохождение атрибута через фильтр "Абсолютное значение".

        Фильтр применяется к свойству "pcnt" атрибута.

        Возвращает истину, если абсолютное значение атрибута больше или равно значения фильтра.

        :param key: Название фильтра.
        :param value: Значение фильтра.
        :return:
        """
        self.filters[key] = {'value': value, 'is_alert': False}

        if abs(self.pcnt) >= value:
            self.filters[key]['is_alert'] = True
            return True
        else:
            return False


class StrAttrDiff(AttrDiff):

    # Фильтры

    def suffix(self, key: str, value: str) -> bool:
        """
        Проверяет прохождение атрибута через фильтр "Суффикс". Все значения фильтра объединяются через "ИЛИ".

        Фильтр применяется к свойству "new" атрибута.

        Возвращает истину, если атрибут соответствует любому из значений фильтра.

        :param key: Название фильтра.
        :param value: Значение фильтра (список суффиксов через запятую).
        :return:
        """
        self.filters[key] = {'value': value, 'is_alert': False}

        value_re = re.sub(r'\s*,\s*', '|', value)

        if re.fullmatch(f'.*({value_re})$', self.new):
            self.filters[key]['is_alert'] = True
            return True
        else:
            return False
