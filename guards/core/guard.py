from abc import ABC, abstractmethod
from typing import Any
from guards.core.events import RUN_EVENT, CLOSE_EVENT


class Guard(ABC):
    def __init__(self, name: str = None, meta=None):
        self.name: str = name
        self.meta = meta
        self.listens_on: list[str] = [RUN_EVENT, CLOSE_EVENT]
        self.permitted: bool = False
        self.closed: bool = False
        self.message: Any = None
        self.__bound: bool = False

    def bind(self):
        if self.__bound:
            raise AttributeError(
                "Guard is already bound. You should not reuse guard instances"
            )
        self.__bound = True

    @abstractmethod
    def run(self, event: str, *args, **kwargs):
        pass

    def get_effective_guard(self):
        return self

    def get_nested_guards(self):
        return []

    def __str__(self) -> str:
        effective_guard = self.get_effective_guard()

        name = effective_guard.name or effective_guard.__class__.__name__

        if effective_guard.meta is None:
            return name
        else:
            return f"{name}({str(effective_guard.meta)})"
