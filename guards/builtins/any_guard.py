from typing import Type
from guards.core.guard import Guard
from guards.builtins.guard_container import GuardContainer


class AnyGuard(GuardContainer):
    def __init__(self, guard_constructors, short_circuit):
        super().__init__("any_guard", guard_constructors)
        self.short_circuit = short_circuit

    def _run_guard(self, guard, *args, **kwargs):
        super()._run_guard(guard, *args, **kwargs)
        if self.short_circuit and guard.permitted and guard.closed:
            self.permitted = True
            self.closed = True

    def run(self, event, *args, **kwargs):
        super().run(event, *args, **kwargs)

        self.permitted = any([guard.permitted for guard in self.guards])


def any_guard(*guard_constructors: Type[Guard], short_circuit=True):
    return lambda: AnyGuard(guard_constructors, short_circuit)
