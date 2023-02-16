from guards.utils.filter_manager.filter_compiler import FilterCompiler
from guards.utils.filter_manager.filter_list import FilterList


class DummyFilterCompiler(FilterCompiler):
    def _and(self, *filters):
        return ["AND"] + [filter for filter in filters if filter]

    def _or(self, *filters):
        return ["OR"] + [filter for filter in filters if filter]

    def _not(self, filter):
        return ["NOT", filter]


FILTER_1 = "FILTER_1"
FILTER_2 = "FILTER_2"


class TestFilterCompiler:
    def test_compiles_include_statements(self):
        filter_list = FilterList()
        filter_list.include(FILTER_1)
        filter_list.include(FILTER_2)

        compiled = DummyFilterCompiler().compile(filter_list)

        assert compiled == ["AND", ["OR", FILTER_1, FILTER_2], ["AND"]]

    def test_compiles_exclude_statements(self):
        filter_list = FilterList()
        filter_list.exclude(FILTER_1)
        filter_list.exclude(FILTER_2)

        compiled = DummyFilterCompiler().compile(filter_list)

        assert compiled == [
            "AND",
            ["OR"],
            [
                "AND",
                ["NOT", FILTER_1],
                ["NOT", FILTER_2]
            ]
        ]
