from typing import Optional, ItemsView

from pydantic import BaseModel, ConfigDict, Field, field_validator

from tickbybit.models.settings.triggers.trigger.ticker.attr.attr import FloatAttr, StrAttr


class Ticker(BaseModel):
    markPrice: FloatAttr = Field(default_factory=FloatAttr)
    openInterestValue: FloatAttr = Field(default_factory=FloatAttr)
    symbol: StrAttr = Field(default_factory=StrAttr)

    model_config = ConfigDict(validate_assignment=True)

    @field_validator('markPrice', mode='before')
    @classmethod
    def default_markPrice(cls, v: Optional[FloatAttr]) -> FloatAttr:
        return v if v is not None \
            else cls.model_fields['markPrice'].default_factory()

    @field_validator('openInterestValue', mode='before')
    @classmethod
    def default_openInterestValue(cls, v: Optional[FloatAttr]) -> FloatAttr:
        return v if v is not None \
            else cls.model_fields['openInterestValue'].default_factory()

    @field_validator('symbol', mode='before')
    @classmethod
    def default_symbol(cls, v: Optional[StrAttr]) -> StrAttr:
        return v if v is not None \
            else cls.model_fields['symbol'].default_factory()

    def items(self) -> ItemsView[str, FloatAttr | StrAttr]:  # pragma: no cover
        return self.__dict__.items()
