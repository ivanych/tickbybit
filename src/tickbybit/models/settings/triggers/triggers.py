from typing import List, TypeVar

from pydantic import RootModel
from tickbybit.models.settings.triggers.trigger.trigger import Trigger

# Это костыль, нужен Питон 3.11 для правильного типа Self (https://peps.python.org/pep-0673/)
SelfTriggers = TypeVar("SelfTriggers", bound="Triggers")


class Triggers(RootModel):
    root: List[Trigger]

    def sorted(self, reverse: bool = False) -> SelfTriggers:
        return Triggers(
            sorted(
                self.root,
                key=lambda x: x.interval,
                reverse=reverse,
            )
        )

    def list(self) -> List[Trigger]:
        return self.root
