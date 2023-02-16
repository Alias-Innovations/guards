from .filter_list import FilterList


class FilterChain:
    def __init__(self, *filter_lists):
        self.filter_lists = filter_lists or []

    @property
    def includes(self):
        filters = []
        for filter_list in self.filter_lists:
            filters.extend(iter(filter_list.includes))
        return filters

    @property
    def excludes(self):
        filters = []

        for filter_list in self.filter_lists:
            filters.extend(iter(filter_list.excludes))
        return filters

    def add_list(self, filter_list: FilterList):
        if filter_list is not None:
            self.filter_lists.append(filter_list)

        return self
