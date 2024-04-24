from typing import Dict, Any
from pydantic import RootModel


class Ticker(RootModel):
    root: Dict[str, Any]

    def __getitem__(self, item):
        return self.root[item] if item in self.root else None

    def __getattr__(self, item):
        return self.root[item]
