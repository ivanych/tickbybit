from typing import List
from pydantic import RootModel

from .ticker_diff import TickerDiff


class TickersDiff(RootModel):
    root: List[TickerDiff] = []

    def append(self, value):
        self.root.append(value)

    def list(self):
        return self.root

    def alerts(self):
        return filter(lambda x: x.is_alert, self.root)
