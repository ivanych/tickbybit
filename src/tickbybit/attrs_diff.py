from typing import Dict
from pydantic import RootModel

from .attr_diff import AttrDiff


class AttrsDiff(RootModel):
    root: Dict[str, AttrDiff]

    def __getitem__(self, item):
        return self.root[item]

    def __setitem__(self, key, value):
        self.root[key] = value

    def __getattr__(self, item):
        return self.root[item]
