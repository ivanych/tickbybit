from typing import Optional

from pydantic import BaseModel

from tickbybit.models.settings.triggers.trigger.ticker.ticker import Ticker


class Trigger(BaseModel):
    icon: Optional[str] = None
    interval: int
    ticker: Ticker
