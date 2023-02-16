import pytest

from guards.builtins.guard_container import GuardContainer
from guards.core.guard import RUN_EVENT, Guard


class FakeGuard(Guard):
    def __init__(self, name=None, meta=None):
        super().__init__(name, meta)
        self.permitted = True

        self.test_runs = 0
        self.test_bound = False
        self.test_next_closed = False

    def bind(self):
        self.test_bound = True
        return super().bind()

    def run(self, _event, *_args, **_kwargs):
        self.test_runs += 1
        self.closed = self.test_next_closed
        pass


TEST_EVENT_1 = "EVENT_1"
TEST_EVENT_2 = "EVENT_2"


class TestGuardContainer:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.guard_container = GuardContainer("test_container", [])
        self.guard_1 = FakeGuard()
        self.guard_2 = FakeGuard()

    def test_constructor_adds_guards_by_constructor(self):
        self.guard_container = GuardContainer("test_container", [FakeGuard])
        assert len(self.guard_container.get_nested_guards()) == 1

    def test_add_adds_guards_by_instance(self):
        self.guard_container.add(self.guard_1)
        assert len(self.guard_container.get_nested_guards()) == 1

    def test_add_changes_listens_on(self):
        self.guard_1.listens_on = [TEST_EVENT_1]
        self.guard_container.add(self.guard_1)

        self.guard_2.listens_on = [TEST_EVENT_2]
        self.guard_container.add(self.guard_2)

        assert TEST_EVENT_1 in self.guard_container.listens_on
        assert TEST_EVENT_2 in self.guard_container.listens_on

    def test_binds_guards(self):
        self.guard_container.add(self.guard_1)

        assert self.guard_1.test_bound

    def test_run_runs_all_open_guards(self):
        self.guard_container.add(self.guard_1)
        self.guard_container.add(self.guard_2)

        self.guard_container.run(RUN_EVENT)

        assert self.guard_1.test_runs == 1
        assert self.guard_2.test_runs == 1

    def test_run_does_not_run_closed_guards(self):
        self.guard_1.closed = True
        self.guard_container.add(self.guard_1)
        self.guard_container.add(self.guard_2)

        self.guard_container.run(RUN_EVENT)

        assert self.guard_1.test_runs == 0
        assert self.guard_2.test_runs == 1

    def test_is_open_if_any_guards_are_open(self):
        self.guard_1.closed = True

        self.guard_container.add(self.guard_1)
        self.guard_container.add(self.guard_2)

        assert not self.guard_container.closed

    def test_is_closed_if_all_guards_are_closed(self):
        self.guard_1.closed = True
        self.guard_container.add(self.guard_1)

        self.guard_2.closed = True
        self.guard_container.add(self.guard_2)

        assert self.guard_container.closed

    def test_gets_closed_if_all_guards_get_closed(self):
        self.guard_1.test_next_closed = True
        self.guard_container.add(self.guard_1)

        self.guard_container.run(RUN_EVENT)

        assert self.guard_container.closed

    def test_returns_last_runned_guard_as_effective_guard(self):
        self.guard_container.add(self.guard_1)

        self.guard_container.run(RUN_EVENT)

        assert self.guard_container.get_effective_guard() == self.guard_1

    def test_stops_running_if_self_gets_closed_by_subclass(self):
        class TestGuardContainer(GuardContainer):
            def _run_guard(self, guard, *args, **kwargs):
                super()._run_guard(guard, *args, **kwargs)
                if guard.closed:
                    self.closed = True

        self.guard_container = TestGuardContainer("test_container", [])

        self.guard_1.test_next_closed = True
        self.guard_container.add(self.guard_1)
        self.guard_container.add(self.guard_2)

        self.guard_container.run(RUN_EVENT)

        assert self.guard_2.test_runs == 0
