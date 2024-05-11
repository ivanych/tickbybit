from pydantic import BaseModel

from .tickers import Tickers
from .ticker import Ticker
from .tickers_diff import TickersDiff
from .ticker_diff import TickerDiff
from .attrs_diff import AttrsDiff
from .attr_diff import FloatAttrDiff, StrAttrDiff


class TickersPair(BaseModel):
    interval: int  # интервал сравнения, в секундах
    new: Tickers
    old: Tickers

    def diff(self) -> TickersDiff:
        """
        Найти изменения в тикерах между старым и новым прайсами.

        :return: Список изменений тикеров.
        """

        tickers_diff = TickersDiff()

        # Цикл по тикерам нового прайса
        for ticker_new in self.new.all():
            ticker_old = self.old.ticker(symbol=ticker_new.symbol)

            attrs_diff = self._attrs_diff(ticker_old, ticker_new)

            ticker_diff = TickerDiff(
                symbol=ticker_new.symbol,
                time_new=self.new.time,
                time_old=self.old.time,
                interval=self.interval,
                attrs=attrs_diff,
            )

            tickers_diff.append(ticker_diff)

            # break

        return tickers_diff

    # TODO надо передалать этот метод, надо чтобы изменение атрибута создавалось сразу через класс AttrDiff
    def _attrs_diff(self, ticker_old: Ticker, ticker_new: Ticker) -> AttrsDiff:
        attrs_diff = {}

        # TODO надо сделать полноценный класс Ticker
        attrs = ['symbol', 'markPrice', 'openInterestValue']

        # Цикл по атрибутам тикера
        for attr in attrs:
            if attr == 'symbol':
                attrs_diff[attr] = StrAttrDiff(
                    old=ticker_old[attr],
                    new=ticker_new[attr],
                )
            else:
                attrs_diff[attr] = FloatAttrDiff(
                    old=ticker_old[attr],
                    new=ticker_new[attr],
                )

        return AttrsDiff(attrs_diff)
