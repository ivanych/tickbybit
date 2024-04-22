from typing import List
from pydantic import RootModel

from .ticker_diff import TickerDiff


class TickersDiff(RootModel):
    root: List[TickerDiff] = []

    def append(self, value):
        self.root.append(value)

    def all(self) -> list[TickerDiff]:
        return self.root

    def alert(self) -> list[TickerDiff]:
        return list(filter(lambda x: x.is_alert, self.root))
