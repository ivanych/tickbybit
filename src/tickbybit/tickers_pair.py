from pydantic import BaseModel

from .tickers import Tickers


class TickersPair(BaseModel):
    old: Tickers
    new: Tickers
