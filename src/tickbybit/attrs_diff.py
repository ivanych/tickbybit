from typing import Dict
from pydantic import RootModel

from .attr_diff import FloatAttrDiff, StrAttrDiff


class AttrsDiff(RootModel):
    root: Dict[str, FloatAttrDiff | StrAttrDiff]

    def __getitem__(self, item):
        return self.root[item]

    def __setitem__(self, key, value):
        self.root[key] = value

    def __getattr__(self, item):
        return self.root[item]

    def filter(self, filters: dict) -> bool:
        """
        Проверяет прохождение атрибутов через фильтры. Все атрибуты объединяются через "И".

        Возвращает истину, если все атрибуты проходят через все свои фильтры

        :param filters: Словарь с фильтрами для атрибутов.
        :return:
        """

        return all(
            map(
                lambda key: self.root[key].filter(filters[key]),
                filters
            )
        )
