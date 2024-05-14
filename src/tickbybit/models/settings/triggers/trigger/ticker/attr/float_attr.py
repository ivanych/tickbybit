from pydantic import BaseModel


class FloatAttr(BaseModel):
    absolute: float
