from pydantic import BaseModel

from .attrs_diff import AttrsDiff


class TickerDiff(BaseModel):
    symbol: str
    time_new: int
    time_old: int
    interval: int  # интервал сравнения, в секундах
    attrs: AttrsDiff

    def to_json(self) -> str:
        return self.model_dump_json(indent=2)

    def filter(self, filters: dict) -> bool:
        return self.attrs.filter(filters)
