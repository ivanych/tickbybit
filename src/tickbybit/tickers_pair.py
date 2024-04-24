from pydantic import BaseModel

from .tickers import Tickers
from .ticker import Ticker
from .tickers_diff import TickersDiff
from .ticker_diff import TickerDiff
from .attrs_diff import AttrsDiff
from .attr_diff import AttrDiff


class TickersPair(BaseModel):
    old: Tickers
    new: Tickers

    def time(self) -> int:
        return self.new.time

    def period(self) -> int:
        return self.new.time - self.old.time

    def diff(self, settings: dict) -> TickersDiff:
        """
        Найти изменения в тикерах между старым и новым прайсами.

        :param settings: Настройки.
        :return: Список изменений тикеров.
        """

        tickers_diff = TickersDiff()

        # Цикл по тикерам нового прайса
        for ticker_new in self.new.all():
            ticker_old = self.old.ticker(symbol=ticker_new.symbol)

            attrs_diff = self._attrs_diff(settings, ticker_old, ticker_new)

            ticker_diff = TickerDiff(
                symbol=ticker_new.symbol,
                time=self.time(),
                period=self.period(),
                attrs=attrs_diff,
            )

            tickers_diff.append(ticker_diff)

            # break

        return tickers_diff

    def _attrs_diff(self, settings: dict, ticker_old: Ticker, ticker_new: Ticker) -> AttrsDiff:
        attrs_diff = {}

        # Цикл по атрибутам тикера
        for attr in settings['ticker']:
            attr_diff = AttrDiff(
                old=ticker_old[attr],
                new=ticker_new[attr],
                alert_pcnt=settings['ticker'][attr]['alert_pcnt'],
            )

            attrs_diff[attr] = attr_diff

        return AttrsDiff(attrs_diff)
