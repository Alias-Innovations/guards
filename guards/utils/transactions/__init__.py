from guards.context.context import GuardContext
from .transaction_manager import TransactionManager


class TransactionManagerStoreKey:
    pass


TRANSACTION_MANAGER_STORE_KEY = TransactionManagerStoreKey()


def get_transaction_manager(guard_context: GuardContext) -> TransactionManager:
    if guard_context.get(TRANSACTION_MANAGER_STORE_KEY, None) is None:
        guard_context.set(TRANSACTION_MANAGER_STORE_KEY, TransactionManager())

    return guard_context.get(TRANSACTION_MANAGER_STORE_KEY, None)
