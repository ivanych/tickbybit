from typing import List, TypeVar

from pydantic import RootModel

from .ticker_diff import TickerDiff
from tickbybit.models.settings.triggers.trigger.trigger import Trigger

# Это костыль, нужен Питон 3.11 для правильного типа Self (https://peps.python.org/pep-0673/)
SelfTickersDiff = TypeVar("SelfTickersDiff", bound="TickersDiff")


class TickersDiff(RootModel):
    root: List[TickerDiff] = []

    def append(self, value):
        self.root.append(value)

    def list(self) -> list[TickerDiff]:
        return self.root

    def filter(self, trigger: Trigger) -> SelfTickersDiff:
        # TODO Не уверен, что это хорошее решение.
        #
        # Копия нужна из-за того, что данные о применённых и сработавших фильтрах (в частности, флаг is_alert)
        # вставляются в методах filter (в основном в attr_diff) прямо в фильтруемый объект.
        # А это создаёт проблему при использовании объекта больше, чем с одним триггером —
        # в следующих прогонах будет мусор от предыдущих.
        #
        # Но при копировании создаётся полная копия объекта, хотя полная копия на самом деле не нужна.
        # Более эффективным кажется отфильтровывать только нужные тикеры и уже отфильтрованные модифицировать.
        # Но сходу не знаю как это сделать.
        self_copy = self.copy(deep=True)

        return TickersDiff(list(filter(lambda x: x.filter(trigger), self_copy.root)))
