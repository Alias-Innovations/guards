from typing import Type
from guards.core.guard import Guard
from guards.builtins.guard_container import GuardContainer


class AllGuards(GuardContainer):
    def __init__(self, guard_constructors, short_circuit):
        super().__init__("all_guard", guard_constructors)
        self.short_circuit = short_circuit

    def _run_guard(self, guard, *args, **kwargs):
        super()._run_guard(guard, *args, **kwargs)
        if self.short_circuit and not guard.permitted and guard.closed:
            self.permitted = False
            self.closed = True

    def run(self, event, *args, **kwargs):
        super().run(event, *args, **kwargs)

        self.permitted = all([guard.permitted for guard in self.guards])


def all_guards(*guard_constructors: Type[Guard], short_circuit=True):
    return lambda: AllGuards(guard_constructors, short_circuit=short_circuit)
