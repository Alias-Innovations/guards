import pytest
from guards.builtins.any_guard import any_guard
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


class TestAnyGuard:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.guard_1 = FakeGuard()

        self.guard_2 = FakeGuard()
        self.guard_2.permitted = False

    def test_closed_if_any_closed_permitted(self):
        self.guard_1.test_next_closed = True

        any_guard_instance = any_guard(lambda: self.guard_1, lambda: self.guard_2)()
        any_guard_instance.run(RUN_EVENT)

        assert any_guard_instance.closed

    def test_permitted_if_any_permitted(self):
        any_guard_instance = any_guard(lambda: self.guard_1, lambda: self.guard_2)()
        any_guard_instance.run(RUN_EVENT)

        assert any_guard_instance.permitted

    def test_permitted_on_rerun_if_all_closed(self):
        self.guard_1.test_next_closed = True

        any_guard_instance = any_guard(lambda: self.guard_1)()
        any_guard_instance.run(RUN_EVENT)
        any_guard_instance.run(RUN_EVENT)

        assert any_guard_instance.permitted

    def test_not_permitted_if_none_permitted(self):
        self.guard_1.permitted = False
        self.guard_1.test_next_closed = True

        self.guard_2.test_next_closed = True

        any_guard_instance = any_guard(lambda: self.guard_1, lambda: self.guard_2)()
        any_guard_instance.run(RUN_EVENT)

        assert not any_guard_instance.permitted

    def test_stays_permitted_on_later_events(self):
        TEST_EVENT = "test-event"

        self.guard_1.permitted = True
        self.guard_1.test_next_closed = False

        self.guard_2.permitted = False
        self.guard_2.listens_on = [TEST_EVENT]
        self.guard_2.test_next_closed = False

        any_guard_instance = any_guard(lambda: self.guard_1, lambda: self.guard_2)()
        any_guard_instance.run(RUN_EVENT)
        any_guard_instance.run(TEST_EVENT)

        assert any_guard_instance.permitted

    def test_short_circuit(self):
        self.guard_1.test_next_closed = True

        any_guard_instance = any_guard(lambda: self.guard_1, lambda: self.guard_2)()
        any_guard_instance.run(RUN_EVENT)

        assert self.guard_2.test_runs == 0

    def test_short_circuit_disabled(self):
        self.guard_1.test_next_closed = True

        any_guard_instance = any_guard(
            lambda: self.guard_1, lambda: self.guard_2, short_circuit=False
        )()
        any_guard_instance.run(RUN_EVENT)

        assert self.guard_2.test_runs == 1
