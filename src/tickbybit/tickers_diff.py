from typing import List, TypeVar

from pydantic import RootModel

from .ticker_diff import TickerDiff

# Это костыль, нужен Питон 3.11 для правильного типа Self (https://peps.python.org/pep-0673/)
SelfTickersDiff = TypeVar("SelfTickersDiff", bound="TickersDiff")


class TickersDiff(RootModel):
    root: List[TickerDiff] = []

    def append(self, value):
        self.root.append(value)

    def list(self) -> list[TickerDiff]:
        return self.root

    def alert(self) -> SelfTickersDiff:
        return TickersDiff(list(filter(lambda x: x.is_alert, self.root)))

    def suffix(self, suffix: str) -> SelfTickersDiff:
        return TickersDiff(list(filter(lambda x: x.is_suffix(suffix), self.root)))
