from guards.utils.filter_manager.filter_chain import FilterChain
from guards.utils.filter_manager.filter_list import FilterList

TEST_FILTER_1 = "test-filter-1"
TEST_FILTER_2 = "test-filter-2"


class TestFilterChain:
    def test_chains_includes(self):
        filter_chain = FilterChain()
        filter_chain.add_list(FilterList().include(TEST_FILTER_1))
        filter_chain.add_list(FilterList().include(TEST_FILTER_2))

        assert TEST_FILTER_1 in filter_chain.includes
        assert TEST_FILTER_2 in filter_chain.includes

    def test_chains_excludes(self):
        filter_chain = FilterChain()
        filter_chain.add_list(FilterList().exclude(TEST_FILTER_1))
        filter_chain.add_list(FilterList().exclude(TEST_FILTER_2))

        assert TEST_FILTER_1 in filter_chain.excludes
        assert TEST_FILTER_2 in filter_chain.excludes

    def test_accepts_filters_as_constructor_parameter(self):
        filter_list_1 = FilterList().exclude(TEST_FILTER_1)
        filter_list_2 = FilterList().exclude(TEST_FILTER_2)
        filter_chain = FilterChain(filter_list_1, filter_list_2)

        assert TEST_FILTER_1 in filter_chain.excludes
        assert TEST_FILTER_2 in filter_chain.excludes

    def test_add_list_is_chainable(self):
        filter_chain = (
            FilterChain()
            .add_list(FilterList().exclude(TEST_FILTER_1))
            .add_list(FilterList().exclude(TEST_FILTER_2))
        )

        assert TEST_FILTER_1 in filter_chain.excludes
        assert TEST_FILTER_2 in filter_chain.excludes

    def test_allows_filter_lists_to_be_modified(self):
        filter_list_1 = FilterList()
        filter_list_2 = FilterList()
        filter_chain = FilterChain(filter_list_1, filter_list_2)

        filter_list_1.exclude(TEST_FILTER_1)
        filter_list_2.exclude(TEST_FILTER_2)

        assert TEST_FILTER_1 in filter_chain.excludes
        assert TEST_FILTER_2 in filter_chain.excludes
