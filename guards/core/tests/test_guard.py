import pytest

from guards.core.guard import Guard
from guards.core.events import RUN_EVENT, CLOSE_EVENT


class DummyGuard(Guard):
    def run(self, *args, **kwargs):
        pass


TEST_NAME = "TEST_GUARD"
TEST_META = "TEST_META"


class TestGuard:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.guard = DummyGuard()

    def test_instantiation_without_name(self):
        assert self.guard

    def test_instantiation_with_name(self):
        self.guard = DummyGuard(TEST_NAME)

        assert self.guard.name == TEST_NAME

    def test_instantiation_with_name_and_meta(self):
        self.guard = DummyGuard(TEST_NAME, TEST_META)
        assert self.guard.name == TEST_NAME
        assert self.guard.meta == TEST_META

    def test_listens_on_run_initially(self):
        assert RUN_EVENT in self.guard.listens_on

    def test_listens_on_close_initially(self):
        assert CLOSE_EVENT in self.guard.listens_on

    def test_can_call_bind_on_unbound(self):
        self.guard.bind()

    def test_cannot_call_bind_on_bound(self):
        self.guard.bind()

        with pytest.raises(Exception):
            self.guard.bind()

    def test_get_effective_guard_returns_self(self):
        effective_guard = self.guard.get_effective_guard()

        assert self.guard == effective_guard

    def test_get_nested_guards_returns_empty_list(self):
        nested_guards = self.guard.get_nested_guards()

        assert len(nested_guards) == 0

    def test_str_without_meta(self):
        self.guard = DummyGuard(TEST_NAME)

        assert str(self.guard) == TEST_NAME
