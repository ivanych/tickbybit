import re

from pydantic import BaseModel, computed_field

from .attrs_diff import AttrsDiff


class TickerDiff(BaseModel):
    symbol: str
    time: int
    period: int
    attrs: AttrsDiff

    def to_json(self) -> str:
        return self.model_dump_json(indent=2)

    def filter(self, filters: dict) -> bool:
        return self.attrs.filter(filters)
