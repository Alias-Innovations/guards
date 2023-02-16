from queue import Queue
from typing import Callable


class TransactionManager:
    def __init__(self) -> None:
        self.operations = Queue()
        self.before_flush = []

    def add(self, operation: Callable):
        self.operations.put(operation)
        return self

    def flush(self):
        for observer in self.before_flush:
            observer(self)

        while not self.operations.empty():
            operation = self.operations.get()
            operation()
