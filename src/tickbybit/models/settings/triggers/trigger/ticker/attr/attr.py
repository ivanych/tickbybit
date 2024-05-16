from typing import ItemsView

from pydantic import BaseModel


class Attr(BaseModel):
    pass

    # TODO тут надо бы сделать абстрактный метод items(),
    # но не совсем понятно, как это делать в Пидантике.


class FloatAttr(Attr):
    absolute: float

    def items(self) -> ItemsView[str, float]:
        return self.__dict__.items()


class StrAttr(Attr):
    suffix: str

    def items(self) -> ItemsView[str, str]:
        return self.__dict__.items()
