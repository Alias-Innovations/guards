from guards.core.guard import Guard


class GuardContainer(Guard):
    def __init__(self, name, guard_constructors):
        super().__init__(name)
        self.guards = []
        self.listener_map = {}
        self.effective_guard = None
        self.closed = True

        for guard in guard_constructors:
            self.add(guard())

    def add(self, guard: Guard):
        guard_collections = [self.guards]

        # Add to events if it listens on something
        if len(guard.listens_on) > 0:
            for event in guard.listens_on:
                if event not in self.listener_map:
                    self.listener_map[event] = []

                guard_collections.append(self.listener_map[event])

        for guard_collection in guard_collections:
            guard_collection.append(guard)

        if self.closed and not guard.closed:
            self.closed = False

        self.listens_on = self.listener_map.keys()

        guard.bind()

    def _run_guard(self, guard, *args, **kwargs):
        if not guard.closed:
            guard.run(*args, **kwargs)
            self.effective_guard = guard

    def _before_run(self):
        pass

    def run(self, event, *args, **kwargs):
        if self.closed:
            return

        any_open = False

        closed_guards = []
        listeners = self.listener_map.get(event, [])
        if len(listeners) == 0:
            return

        self._before_run()

        for guard in listeners:
            self._run_guard(guard, event, *args, **kwargs)
            if self.closed:
                return

            if guard.closed:
                closed_guards.append(guard)
            else:
                any_open = True

        for closed_guard in closed_guards:
            listeners.remove(closed_guard)

        self.closed = not any_open

    def get_effective_guard(self):
        if self.effective_guard:
            return self.effective_guard
        return super().get_effective_guard()

    def get_nested_guards(self):
        return self.guards
