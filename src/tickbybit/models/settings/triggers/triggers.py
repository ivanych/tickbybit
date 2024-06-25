from typing import List, TypeVar

from pydantic import RootModel, ConfigDict, Field

from tickbybit.models.settings.triggers.trigger.trigger import Trigger

# Это костыль, нужен Питон 3.11 для правильного типа Self (https://peps.python.org/pep-0673/)
SelfTriggers = TypeVar("SelfTriggers", bound="Triggers")


class Triggers(RootModel):
    root: List[Trigger] = Field(default=[])

    model_config = ConfigDict(validate_assignment=True)

    def __getitem__(self, key) -> Trigger:  # pragma: no cover
        return self.root[key]

    def __setitem__(self, key: int, value: dict = None):
        if isinstance(value, dict):
            trigger = Trigger(**value)
            self.root[key] = trigger
        elif value is None:
            trigger = Trigger()
            self.root[key] = trigger
        else:
            raise ValueError('Значение должно быть словарём')

    def append(self, value: dict = None):
        if isinstance(value, dict):
            trigger = Trigger(**value)
            self.root.append(trigger)
        elif value is None:
            trigger = Trigger()
            self.root.append(trigger)
        else:
            raise ValueError('Значение должно быть словарём')

    def pop(self, index: int = -1):
        self.root.pop(index)

    def sorted(self, reverse: bool = False) -> SelfTriggers:  # pragma: no cover
        return Triggers(
            sorted(
                self.root,
                key=lambda x: x.interval,
                reverse=reverse,
            )
        )

    def list(self) -> List[Trigger]:
        return self.root
