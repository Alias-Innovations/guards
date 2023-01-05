from typing import Any

from .filter_list import FilterList


class FilterManager:
    def __init__(self):
        self.filter_lists = {}

    def list(self, identifier: Any) -> FilterList:
        if identifier not in self.filter_lists:
            self.filter_lists[identifier] = FilterList()

        return self.filter_lists[identifier]
