from functools import wraps
from inspect import signature
from guards.core.guard import Guard
from guards.context import GuardContextManager


class GuardResponse:
    def __init__(self, permitted=False, closed=True, message=None):
        self.permitted = permitted
        self.closed = closed
        self.message = message


def _guard(close=None, default_permitted=None, listens_on=None, name=None, meta=None):
    def decorator(fn):
        class FunctionalGuard(Guard):
            def __init__(self):
                super().__init__(name or fn.__name__, meta)

                if default_permitted is not None:
                    self.permitted = default_permitted

                if listens_on is not None:
                    self.listens_on = listens_on

            def run(self, event, *args, **kwargs):
                sig = signature(fn)
                args = [self, event] + list(args)
                args = args[: len(sig.parameters)]

                response = fn(*args, **kwargs)

                self.closed = close
                if close is None:
                    self.closed = len(listens_on or []) == 0

                if isinstance(response, GuardResponse):
                    self.closed = response.closed
                    self.permitted = response.permitted
                    self.message = response.message
                    return

                if type(response) is bool:
                    self.permitted = response
                    return

        return FunctionalGuard

    return decorator


def guard(*args, **kwargs):
    is_higher_order = len(args) != 1 or len(kwargs) != 0 or not callable(args[0])
    if is_higher_order:
        return _guard(*args, **kwargs)
    else:
        return _guard()(*args, **kwargs)


def require(*guards):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            context = GuardContextManager()

            wrapped = context.require(*guards)(fn)
            retval = wrapped(*args, **kwargs)

            context.close()

            return retval

        return wrapper

    return decorator
