from jsonpath_ng.ext import parse
from typing import Dict, Any
from pydantic import RootModel

from .ticker import Ticker


class Tickers(RootModel):
    root: Dict[str, Any]

    def ticker(self, symbol: str) -> Ticker:
        # TODO поиск тикера в списке — это неэффективный способ,
        # нужно оптимизировать к поиску в словаре
        jsonpath = parse(f'result.list[?symbol = "{symbol}"]')

        return Ticker(jsonpath.find(self.root)[0].value)

    def list(self) -> map:
        return map(Ticker, self.root['result']['list'])
