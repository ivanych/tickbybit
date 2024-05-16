from typing import Optional, ItemsView, Any

from pydantic import BaseModel

from tickbybit.models.settings.triggers.trigger.ticker.attr.attr import FloatAttr, StrAttr


class Ticker(BaseModel):
    markPrice: Optional[FloatAttr] = None
    openInterestValue: Optional[FloatAttr] = None
    symbol: Optional[StrAttr] = None

    def items(self) -> ItemsView[str, FloatAttr | StrAttr]:
        return self.__dict__.items()
