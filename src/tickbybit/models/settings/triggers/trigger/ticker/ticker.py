from typing import Optional

from pydantic import BaseModel

from tickbybit.models.settings.triggers.trigger.ticker.attr.float_attr import FloatAttr
from tickbybit.models.settings.triggers.trigger.ticker.attr.str_attr import StrAttr


class Ticker(BaseModel):
    markPrice: Optional[FloatAttr] = None
    openInterestValue: Optional[FloatAttr] = None
    symbol: Optional[StrAttr] = None
