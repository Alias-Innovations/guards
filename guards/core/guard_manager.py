from typing import Any

from guards.core.guard import Guard
from guards.core.events import RUN_EVENT, CLOSE_EVENT
from guards.core.exception import GuardException


class GuardManager:
    def __init__(self):
        self.guards: list[Guard] = []
        self.listeners: dict[Any, list[Guard]] = {}

    def add(self, guard: Guard):
        guard_collections = [self.guards]

        # Add to events if it listens on something
        if len(guard.listens_on) > 0:
            for event in guard.listens_on:
                if event not in self.listeners:
                    self.listeners[event] = []

                guard_collections.append(self.listeners[event])

        for guard_collection in guard_collections:
            guard_collection.append(guard)

        guard.bind()

    def __run_guard(self, guard, event, *args, **kwargs):
        if guard.closed:
            # If a guard listens on multiple events, leftovers may occur
            return

        guard.run(event, *args, **kwargs)
        if guard.closed and not guard.permitted:
            raise GuardException(guard.get_effective_guard())

    def run(self, event: Any = RUN_EVENT, *args, **kwargs):
        closed_guards = []
        guards = self.listeners.get(event, [])
        for guard in guards:
            self.__run_guard(guard, event, *args, **kwargs)
            if guard.closed:
                closed_guards.append(guard)

        for closed_guard in closed_guards:
            guards.remove(closed_guard)

    def check(self):
        # Throw error for open guards as well when closing
        for guard in self.guards:
            if not guard.permitted:
                raise GuardException(guard.get_effective_guard())

    def close(self):
        self.run(CLOSE_EVENT)
        self.check()
