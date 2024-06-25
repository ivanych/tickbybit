from typing import Optional, ItemsView

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Attr(BaseModel):
    pass

    model_config = ConfigDict(validate_assignment=True)

    # TODO тут надо бы сделать абстрактный метод items(),
    # но не совсем понятно, как это делать в Пидантике.


class FloatAttr(Attr):
    absolute: float = Field(default=1)

    @field_validator('absolute', mode='before')
    @classmethod
    def default_absolute(cls, v: Optional[str]) -> float:
        return v if v is not None \
            else cls.model_fields['absolute'].default

    def items(self) -> ItemsView[str, float]:  # pragma: no cover
        return self.__dict__.items()


class StrAttr(Attr):
    suffix: str = Field(default='USDT')

    @field_validator('suffix', mode='before')
    @classmethod
    def default_suffix(cls, v: Optional[str]) -> str:
        return v if v is not None \
            else cls.model_fields['suffix'].default

    def items(self) -> ItemsView[str, str]:  # pragma: no cover
        return self.__dict__.items()
