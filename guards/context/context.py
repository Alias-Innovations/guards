from typing import Any, Callable
from guards.core.guard_manager import GuardManager
from guards.core.guard import Guard
from guards.core.events import GuardEventKey


class StoreEvent(GuardEventKey):
    pass


class GuardContext:
    def __init__(self):
        self.parent: GuardContext = None
        self.store: dict[Any, Any] = {}
        self.guards: GuardManager = GuardManager()
        self.closed = False

    def add_guard(self, guard_constructor: Callable[[], Guard]):
        self.guards.add(guard_constructor())

    def run_guards(self):
        self.guards.run()

    def check(self):
        self.guards.check()

    def emit(self, event, *args, **kwargs):
        self.guards.run(event, *args, **kwargs)

    def set(self, name, value):
        self.store[name] = value
        self.emit(StoreEvent(name), value)

    def get(self, name, default=None):
        return self.store.get(name, default)

    def close(self):
        if self.closed:
            return
        self.closed = True
        self.guards.close()
