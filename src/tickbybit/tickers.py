from typing import Dict, Any
from pydantic import BaseModel

from .ticker import Ticker


class Tickers(BaseModel):
    time: int
    tickers: Dict[str, Any]

    def __getitem__(self, item):
        return self.tickers[item]

    def __getattr__(self, item):
        return self.tickers[item]

    def ticker(self, symbol: str) -> Ticker:
        if symbol in self.tickers:
            return Ticker(self.tickers[symbol])
        else:
            return Ticker({})

    def all(self) -> map:
        return map(Ticker, self.tickers.values())
