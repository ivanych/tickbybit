from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from tickbybit.models.settings.triggers.trigger.ticker.ticker import Ticker


class Trigger(BaseModel):
    icon: Optional[str] = Field(default=None)
    interval: int = Field(default=60)
    ticker: Ticker = Field(default_factory=Ticker)

    model_config = ConfigDict(validate_assignment=True)

    @field_validator('interval', mode='before')
    @classmethod
    def default_interval(cls, v: int) -> int:
        return v if v is not None \
            else cls.model_fields['interval'].default

    @field_validator('ticker', mode='before')
    @classmethod
    def default_ticker(cls, v: Ticker) -> Ticker:
        return v if v is not None \
            else cls.model_fields['ticker'].default_factory()
