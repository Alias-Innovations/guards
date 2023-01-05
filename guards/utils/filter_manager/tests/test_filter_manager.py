import pytest

from guards.utils.filter_manager.filter_list import FilterList
from guards.utils.filter_manager.filter_manager import FilterManager

TEST_IDENTIFIER_1 = "TEST_LIST_1"
TEST_IDENTIFIER_2 = "TEST_LIST_2"


class TestFilterManager:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.filter_manager = FilterManager()

    def test_returns_list(self):
        filter_list = self.filter_manager.list(TEST_IDENTIFIER_1)

        assert isinstance(filter_list, FilterList)

    def test_returns_same_list_for_identifier(self):
        filter_list_1 = self.filter_manager.list(TEST_IDENTIFIER_1)
        filter_list_2 = self.filter_manager.list(TEST_IDENTIFIER_1)

        assert filter_list_1 == filter_list_2

    def test_returns_different_list_for_different_identifier(self):
        filter_list_1 = self.filter_manager.list(TEST_IDENTIFIER_1)
        filter_list_2 = self.filter_manager.list(TEST_IDENTIFIER_2)

        assert filter_list_1 != filter_list_2
