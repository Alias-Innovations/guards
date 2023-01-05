from guards.core.guard import Guard


class GuardException(Exception):
    def __init__(self, guard: Guard):
        super().__init__(f"Guard `{str(guard)}` denied access")
        self.guard = guard
