from guards.context import context

from guards.context.context_manager import GuardContextManager
from guards.core.guard import Guard


class FakeGuardContext(context.GuardContext):
    def __init__(self):
        super().__init__()
        self.test_closed = False
        self.test_added_guards = []

    def add_guard(self, guard_constructor):
        self.test_added_guards.append(guard_constructor)
        return super().add_guard(guard_constructor)

    def close(self):
        self.test_closed = True


class FakeGuard(Guard):
    def __init__(self, name=None, meta=None):
        super().__init__(name, meta)
        self.permitted = True

    def run(self, _event, *_args, **_kwargs):
        pass


class TestContextManager:
    def test_creates_context(self):
        context_manager = GuardContextManager()

        assert isinstance(context_manager.current_context, context.GuardContext)

    def test_closes_context(self, monkeypatch):
        guard_context = FakeGuardContext()
        monkeypatch.setattr(
            "guards.context.context_manager.GuardContext", lambda: guard_context
        )
        context_manager = GuardContextManager()

        context_manager.close()

        assert guard_context.test_closed

    def test_require_adds_guard(self, monkeypatch):
        guard_context = FakeGuardContext()
        monkeypatch.setattr(
            "guards.context.context_manager.GuardContext", lambda: guard_context
        )
        context_manager = GuardContextManager()

        @context_manager.require(FakeGuard)
        def dummy():
            pass

        dummy()

        assert len(guard_context.test_added_guards) == 1

    def test_subcontext_gives_new_context(self):
        context_manager = GuardContextManager()

        root_context = context_manager.current_context

        with context_manager.subcontext() as subcontext:
            assert root_context != subcontext
            assert root_context != context_manager.current_context

        assert root_context == context_manager.current_context

    def test_require_does_not_create_subcontext_on_missing_kwarg(self):
        context_manager = GuardContextManager()

        root_context = context_manager.current_context

        @context_manager.require(FakeGuard)
        def dummy():
            assert context_manager.current_context == root_context

        dummy()

    def test_require_create_subcontext_on_subcontext_kwarg(self):
        context_manager = GuardContextManager()

        root_context = context_manager.current_context

        @context_manager.require(FakeGuard, subcontext=True)
        def dummy():
            assert context_manager.current_context != root_context

        dummy()

    def test_closes_all_subcontexts(self):
        context_manager = GuardContextManager()

        root_context = context_manager.current_context

        subcontext = context_manager.subcontext()
        subcontext.__enter__()

        context_manager.close()

        assert root_context.closed
        assert subcontext.closed
        assert context_manager.current_context is None
