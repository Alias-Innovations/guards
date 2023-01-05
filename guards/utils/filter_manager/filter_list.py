class FilterList:
    def __init__(self):
        self.includes = []
        self.excludes = []

    def include(self, filter):
        self.includes.append(filter)
        return self

    def exclude(self, filter):
        self.excludes.append(filter)
        return self
