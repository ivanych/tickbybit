from typing import Dict, Any
from pydantic import RootModel


class Ticker(RootModel):
    root: Dict[str, Any]

    def __getitem__(self, name):
        return self.root[name]

    def __getattr__(self, name):
        return self.root[name]
