from guards.context.context import GuardContext
from .filter_manager import FilterManager


class FilterManagerStoreKey:
    pass


FILTER_MANAGER_STORE_KEY = FilterManagerStoreKey()


def get_filter_manager(guard_context: GuardContext) -> FilterManager:
    if guard_context.get(FILTER_MANAGER_STORE_KEY, None) is None:
        guard_context.set(FILTER_MANAGER_STORE_KEY, FilterManager())

    return guard_context.get(FILTER_MANAGER_STORE_KEY, None)
