import pytest

from guards.utils.transactions.transaction_manager import TransactionManager


class FakeOperation:
    def __init__(self) -> None:
        self.call_count = 0

    def __call__(self, *_):
        self.call_count += 1


class TestTransactionManager:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.transaction_manager = TransactionManager()
        self.test_operation = FakeOperation()

    def test_adding_operation_does_not_run_it(self):
        self.transaction_manager.add(self.test_operation)
        assert self.test_operation.call_count == 0

    def test_flush_transaction_runs_operations(self):
        self.transaction_manager.add(self.test_operation)
        self.transaction_manager.flush()
        assert self.test_operation.call_count == 1

    def test_flush_transaction_clears_operation_queue(self):
        self.transaction_manager.add(self.test_operation)
        self.transaction_manager.flush()
        self.transaction_manager.flush()
        assert self.test_operation.call_count == 1

    def test_flush_transaction_runs_observers(self):
        observer = FakeOperation()
        self.transaction_manager.before_flush.append(observer)

        self.transaction_manager.add(self.test_operation)
        self.transaction_manager.flush()
        assert observer.call_count == 1
