import pytest
from guards.builtins.all_guards import all_guards
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


class TestAllGuards:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.guard_1 = FakeGuard()

        self.guard_2 = FakeGuard()
        self.guard_2.permitted = False

    def test_closed_if_any_closed_not_permitted(self):
        self.guard_2.test_next_closed = True

        all_guards_instance = all_guards(lambda: self.guard_1, lambda: self.guard_2)()
        all_guards_instance.run(RUN_EVENT)

        assert all_guards_instance.closed

    def test_not_permitted_if_any_not_permitted(self):
        all_guards_instance = all_guards(lambda: self.guard_1, lambda: self.guard_2)()
        all_guards_instance.run(RUN_EVENT)

        assert not all_guards_instance.permitted

    def test_not_permitted_on_rerun_after_closed(self):
        self.guard_1.permitted = False
        self.guard_1.test_next_closed = True
        all_guards_instance = all_guards(lambda: self.guard_1)()
        all_guards_instance.run(RUN_EVENT)
        all_guards_instance.run(RUN_EVENT)

        assert not all_guards_instance.permitted

    def test_permitted_if_all_permitted(self):
        self.guard_2.permitted = True
        all_guards_instance = all_guards(lambda: self.guard_1, lambda: self.guard_2)()
        all_guards_instance.run(RUN_EVENT)

        assert all_guards_instance.permitted

    def test_short_circuit(self):
        self.guard_1.permitted = False
        self.guard_1.test_next_closed = True

        all_guards_instance = all_guards(lambda: self.guard_1, lambda: self.guard_2)()
        all_guards_instance.run(RUN_EVENT)

        assert self.guard_2.test_runs == 0

    def test_disabled_short_circuit(self):
        self.guard_1.permitted = False
        self.guard_1.test_next_closed = True

        all_guards_instance = all_guards(
            lambda: self.guard_1, lambda: self.guard_2, short_circuit=False
        )()
        all_guards_instance.run(RUN_EVENT)

        assert self.guard_2.test_runs == 1
        assert not all_guards_instance.permitted
