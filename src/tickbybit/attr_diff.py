from pydantic import BaseModel, computed_field


class AttrDiff(BaseModel):
    old: str | None
    new: str
    alert_pcnt: float

    @computed_field
    @property
    def pcnt(self) -> float | None:
        return round(
            number=float(self.new) / float(self.old) * 100 - 100,
            ndigits=6,
        ) if self.old is not None else None

    @computed_field
    @property
    def is_alert(self) -> bool:
        # Превышена разница по атрибуту?
        return (abs(self.pcnt) >= self.alert_pcnt) if self.pcnt is not None else False
