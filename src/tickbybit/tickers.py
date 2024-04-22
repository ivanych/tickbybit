from jsonpath_ng.ext import parse
from typing import Dict, Any
from pydantic import RootModel

from .ticker import Ticker


class Tickers(RootModel):
    root: Dict[str, Any]

    def __getitem__(self, item):
        return self.root[item]

    def __getattr__(self, item):
        return self.root[item]

    def ticker(self, symbol: str) -> Ticker:
        # TODO поиск тикера в списке — это неэффективный способ,
        # нужно оптимизировать к поиску в словаре
        jsonpath = parse(f'result.list[?symbol = "{symbol}"]')

        matches = jsonpath.find(self.root)

        if matches:
            return Ticker(matches[0].value)
        else:
            return Ticker({})

    def list(self) -> map:
        return map(Ticker, self.root['result']['list'])
