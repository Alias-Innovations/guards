import pytest

from guards.context.context import GuardContext, StoreEvent
from guards.core.events import GuardEventKey
from guards.core.guard import RUN_EVENT, Guard
from guards.core.guard_manager import GuardManager


class DummyGuard(Guard):
    def run(self, *_args, **_kwargs):
        pass


def build_fake_guard_manager():
    class FakeGuardManager(GuardManager):
        test_adds = []
        test_runs = []
        test_closed = False

        def add(self, guard):
            FakeGuardManager.test_adds.append(guard)
            return super().add(guard)

        def run(self, event=RUN_EVENT, *args, **kwargs):
            FakeGuardManager.test_runs.append(event)
            return super().run(event, *args, **kwargs)

        def close(self):
            FakeGuardManager.test_closed = True
            return super().close()

    return FakeGuardManager


TEST_KEY = "TEST_KEY"
TEST_VALUE = "TEST_VALUE"
TEST_EVENT = "TEST_EVENT"


class TestGuardContext:
    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch):
        self.FakeGuardManager = build_fake_guard_manager()
        monkeypatch.setattr(
            "guards.context.context.GuardManager", self.FakeGuardManager
        )
        self.context = GuardContext()

    def test_add_guard_calls_add_on_guard_manager(self):
        self.context.add_guard(DummyGuard)

        assert len(self.FakeGuardManager.test_adds) == 1
        assert isinstance(self.FakeGuardManager.test_adds[0], DummyGuard)

    def test_run_calls_run(self):
        self.context.run_guards()

        assert len(self.FakeGuardManager.test_runs) == 1
        assert self.FakeGuardManager.test_runs[0] == RUN_EVENT

    def test_emit_calls_run(self):
        self.context.emit(GuardEventKey(TEST_EVENT))

        assert len(self.FakeGuardManager.test_runs) == 1
        assert self.FakeGuardManager.test_runs[0] == GuardEventKey(TEST_EVENT)

    def test_close_sets_closed(self):
        self.context.close()

        assert self.context.closed

    def test_close_calls_close(self):
        self.context.close()

        assert self.FakeGuardManager.test_closed

    def test_close_calls_close_once(self):
        self.context.close()

        self.FakeGuardManager.test_closed = False
        self.context.close()

        assert not self.FakeGuardManager.test_closed

    def test_store_can_save_objects(self):
        self.context = GuardContext()
        self.context.set(TEST_KEY, TEST_VALUE)

        assert self.context.get(TEST_KEY) == TEST_VALUE

    def test_store_emits_event(self):
        self.context = GuardContext()
        self.context.set(TEST_KEY, TEST_VALUE)

        assert len(self.FakeGuardManager.test_runs) == 1
        assert self.FakeGuardManager.test_runs[0] == StoreEvent(TEST_KEY)
