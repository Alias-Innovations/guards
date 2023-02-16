import pytest

from guards.core.events import GuardEventKey
from guards.core.exception import GuardException
from guards.core.guard_manager import GuardManager
from guards.core.guard import Guard
from guards.core.events import RUN_EVENT, CLOSE_EVENT


class FakeGuard(Guard):
    def __init__(self, name: str = None, meta=None):
        super().__init__(name, meta)
        self.test_next_closed = self.closed
        self.test_runs = []
        self.test_bound = False

    def bind(self):
        self.test_bound = True
        return super().bind()

    def run(self, *args, **kwargs):
        self.closed = self.test_next_closed
        self.test_runs.append({"args": args, "kwargs": kwargs})


class TestGuardManager:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.guard_manager = GuardManager()
        self.guard = FakeGuard()

    def test_can_add_guard(self):
        self.guard_manager.add(self.guard)

        assert self.guard.test_bound

    def test_runs_added_guard(self):
        self.guard.permitted = True
        self.guard.closed = False
        self.guard.listens_on = [RUN_EVENT]

        self.guard_manager.add(self.guard)
        self.guard_manager.run()

        assert len(self.guard.test_runs) == 1

    def test_runs_open_guard_multiple_times(self):
        self.guard.permitted = True
        self.guard.closed = False
        self.guard.listens_on = [RUN_EVENT]

        self.guard_manager.add(self.guard)

        self.guard_manager.run()
        self.guard_manager.run()

        assert len(self.guard.test_runs) == 2

    def test_does_not_run_closed_guard(self):
        self.guard.permitted = True
        self.guard.closed = True
        self.guard.listens_on = [RUN_EVENT]

        self.guard_manager.add(self.guard)

        self.guard_manager.run()

        assert len(self.guard.test_runs) == 0

    def test_does_not_run_guard_without_listener(self):
        self.guard.permitted = True
        self.guard.closed = False
        self.guard.listens_on = []

        self.guard_manager.add(self.guard)

        self.guard_manager.run()

        assert len(self.guard.test_runs) == 0

    def test_does_not_run_on_specific_listener(self):
        TEST_EVENT_ID = "TEST_EVENT"

        self.guard.permitted = True
        self.guard.closed = False
        self.guard.listens_on = [GuardEventKey(TEST_EVENT_ID)]

        self.guard_manager.add(self.guard)

        self.guard_manager.run()

        assert len(self.guard.test_runs) == 0

    def test_runs_on_listened_event(self):
        TEST_EVENT_ID = "TEST_EVENT"

        self.guard.permitted = True
        self.guard.closed = False
        self.guard.listens_on = [GuardEventKey(TEST_EVENT_ID)]

        self.guard_manager.add(self.guard)

        self.guard_manager.run(GuardEventKey(TEST_EVENT_ID))

        assert len(self.guard.test_runs) == 1

    def test_receives_args(self):
        TEST_EVENT_ID = "TEST_EVENT"
        ARGS = ["ARG_1", "ARG_2"]
        KWARGS = {"ARG_1": "VALUE_1", "ARG_2": "VALUE_2"}

        self.guard.permitted = True
        self.guard.closed = False
        self.guard.listens_on = [GuardEventKey(TEST_EVENT_ID)]

        self.guard_manager.add(self.guard)

        self.guard_manager.run(GuardEventKey(TEST_EVENT_ID), *ARGS, **KWARGS)

        assert len(self.guard.test_runs) == 1

        run_args = self.guard.test_runs[0]["args"]
        assert run_args[0] == GuardEventKey(TEST_EVENT_ID)
        assert run_args[1] == ARGS[0]
        assert run_args[2] == ARGS[1]

        run_kwargs = self.guard.test_runs[0]["kwargs"]
        assert run_kwargs["ARG_1"] == KWARGS["ARG_1"]
        assert run_kwargs["ARG_2"] == KWARGS["ARG_2"]

    def test_throws_for_not_permitted_and_closed_guard(self):
        self.guard.permitted = False
        self.guard.test_next_closed = True
        self.guard.closed = False
        self.guard.listens_on = [RUN_EVENT]

        self.guard_manager.add(self.guard)

        with pytest.raises(GuardException) as exception_info:
            self.guard_manager.run()

        assert exception_info.value.guard == self.guard

    def test_does_not_throw_for_not_permitted_and_not_closed_guard(self):
        self.guard.permitted = False
        self.guard.closed = False
        self.guard.listens_on = [RUN_EVENT]

        self.guard_manager.add(self.guard)

        self.guard_manager.run()

    def test_runs_open_guards_with_close_event_before_closing(self):
        self.guard.permitted = True
        self.guard.closed = False
        self.guard.listens_on = [CLOSE_EVENT]

        self.guard_manager.add(self.guard)
        self.guard_manager.close()

        assert len(self.guard.test_runs) == 1

    def test_throws_for_not_permitted_and_not_closed_guards(self):
        self.guard.permitted = False
        self.guard.closed = False
        self.guard.listens_on = []

        self.guard_manager.add(self.guard)

        with pytest.raises(GuardException) as exception_info:
            self.guard_manager.close()

        assert exception_info.value.guard == self.guard
