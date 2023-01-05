from abc import ABC, abstractmethod

from .filter_list import FilterList


class FilterCompiler(ABC):
    @abstractmethod
    def _and(self, *filters):
        pass

    @abstractmethod
    def _or(self, *filters):
        pass

    @abstractmethod
    def _not(self, filter):
        pass

    def compile(self, filter_list: FilterList):
        includes_combined = self._or(*filter_list.includes)
        excludes_combined = self._and(
            *[self._not(filter) for filter in filter_list.excludes]
        )
        return self._and(includes_combined, excludes_combined)
