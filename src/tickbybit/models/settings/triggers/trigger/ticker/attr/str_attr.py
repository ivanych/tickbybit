from pydantic import BaseModel


class StrAttr(BaseModel):
    suffix: str
