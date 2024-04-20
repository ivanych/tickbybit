from typing import Dict
from pydantic import RootModel


class Ticker(RootModel):
    root: Dict[str, str]

    def __getitem__(self, name):
        return self.root[name]

    def __getattr__(self, name):
        return self.root[name]
