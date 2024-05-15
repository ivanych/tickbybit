from typing import ItemsView

from pydantic import BaseModel


class AttrFilters(BaseModel):
    pass

    # TODO тут надо бы сделать абстрактный метод items(),
    # но не совсем понятно, как это делать в Пидантике.


class FloatAttrFilters(AttrFilters):
    absolute: float

    def items(self) -> ItemsView[str, float]:
        return self.__dict__.items()


class StrAttrFilters(AttrFilters):
    suffix: str

    def items(self) -> ItemsView[str, str]:
        return self.__dict__.items()
