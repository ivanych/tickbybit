from pydantic import BaseModel, computed_field

from .attrs_diff import AttrsDiff


class TickerDiff(BaseModel):
    symbol: str
    time: int
    period: int
    attrs: AttrsDiff

    @computed_field
    @property
    def is_alert(self) -> bool:
        # Превышена разница по любому атрибуту?
        return self.attrs.is_alert()

    def to_json(self) -> str:
        return self.model_dump_json(indent=2)
