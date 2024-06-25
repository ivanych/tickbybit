from typing import Optional

from pydantic import BaseModel

from .attrs_diff import AttrsDiff
from tickbybit.models.settings.triggers.trigger.trigger import Trigger


class TickerDiff(BaseModel):
    symbol: str
    time_new: int
    time_old: int
    interval: int  # интервал сравнения, в секундах
    icon: Optional[str] = None  # иконка триггера
    attrs: AttrsDiff

    def to_json(self) -> str:
        return self.model_dump_json(indent=2)

    def filter(self, trigger: Trigger) -> bool:
        is_alert = self.attrs.filter(trigger)

        if is_alert:
            self.icon = trigger.icon

        return is_alert
