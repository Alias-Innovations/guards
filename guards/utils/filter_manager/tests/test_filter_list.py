import pytest

from guards.utils.filter_manager.filter_list import FilterList

TEST_EXPRESSION = "expression-1"


class TestFilterList:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.filter_list = FilterList()

    def test_can_add_to_includes(self):
        self.filter_list.include(TEST_EXPRESSION)

        assert TEST_EXPRESSION in self.filter_list.includes

    def test_can_add_to_excludes(self):
        self.filter_list.exclude(TEST_EXPRESSION)

        assert TEST_EXPRESSION in self.filter_list.excludes

    def test_includes_is_chainable(self):
        assert self.filter_list.include(TEST_EXPRESSION) == self.filter_list

    def test_excludes_is_chainable(self):
        assert self.filter_list.exclude(TEST_EXPRESSION) == self.filter_list
