from contextlib import nullcontext
from functools import wraps

from guards.context.context import GuardContext


class GuardContextManager:
    def __init__(self):
        self.current_context = GuardContext()

    def subcontext(self):
        class Subcontext(GuardContext):
            def __enter__(subcontext_self):
                subcontext_self.parent = self.current_context
                self.current_context = subcontext_self
                return self

            def __exit__(subcontext_self, _type, _value, _traceback):
                subcontext_self.close()
                self.current_context = subcontext_self.parent

        return Subcontext()

    def close(self):
        while self.current_context is not None:
            self.current_context.close()
            self.current_context = self.current_context.parent

    def require(self, *guards, subcontext=False):
        def decorator(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                with self.subcontext() if subcontext else nullcontext():
                    for guard in list(guards):
                        self.current_context.add_guard(guard)
                    self.current_context.run_guards()
                    return fn(*args, **kwargs)

            return wrapper

        return decorator
