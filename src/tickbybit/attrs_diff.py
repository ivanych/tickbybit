from typing import Dict
from pydantic import RootModel

from .attr_diff import FloatAttrDiff, StrAttrDiff
from tickbybit.models.settings.triggers.trigger.trigger import Trigger


class AttrsDiff(RootModel):
    root: Dict[str, FloatAttrDiff | StrAttrDiff]

    def __getitem__(self, item):
        return self.root[item]

    def __setitem__(self, key, value):
        self.root[key] = value

    def __getattr__(self, item):
        return self.root[item]

    def filter(self, trigger: Trigger) -> bool:
        """
        Проверяет прохождение атрибутов через фильтры. Все атрибуты объединяются через "И".

        Возвращает истину, если все атрибуты проходят через все свои фильтры

        :param trigger: триггер.
        :return:
        """

        return all(
            map(
                lambda kv: self.root[kv[0]].filter(kv[1]),
                trigger.ticker.items()
            )
        )
