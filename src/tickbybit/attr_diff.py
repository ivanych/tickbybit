from pydantic import BaseModel, computed_field


class AttrDiff(BaseModel):
    old: str
    new: str
    alert_pcnt: float

    @computed_field
    @property
    def pcnt(self) -> float:
        return round(
            number=float(self.new) / float(self.old) * 100 - 100,
            ndigits=6,
        )

    @computed_field
    @property
    def is_alert(self) -> bool:
        # Превышена разница по атрибуту?
        return abs(self.pcnt) >= self.alert_pcnt
