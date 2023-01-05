from pprint import pprint
from guards.functional import guard
from guards.context import GuardContextManager
from guards import GuardException
from guards.utils.filter_manager import get_filter_manager
from guards.utils.filter_manager.filter_compiler import FilterCompiler

data_source = [
    {"type": "a", "value": 1},
    {"type": "a", "value": 2},
    {"type": "b", "value": 10},
    {"type": "b", "value": 20},
    {"type": "c", "value": 100},
    {"type": "c", "value": 200},
]


class PredicateFilterCompiler(FilterCompiler):
    def _and(self, *filters):
        def and_predicate(*args, **kwargs):
            for _filter in filters:
                if not _filter(*args, **kwargs):
                    return False

            return True

        return and_predicate

    def _or(self, *filters):
        def or_predicate(*args, **kwargs):
            for _filter in filters:
                if _filter(*args, **kwargs):
                    return True

            return False

        return or_predicate

    def _not(self, _filter):
        def not_predicate(*args, **kwargs):
            return not _filter(*args, **kwargs)

        return not_predicate


filter_compiler = PredicateFilterCompiler()

access_list = input("Access list: ")

context_manager = GuardContextManager()


@guard(default_permitted=True, close=True)
def filter_guard():
    filter_manager = get_filter_manager(context_manager.current_context)

    filter_list = filter_manager.list("data_source")
    for type in access_list:
        filter_list.include(lambda x, type=type: x["type"] == type)


@context_manager.require(filter_guard)
def protected_function():
    filter_manager = get_filter_manager(context_manager.current_context)
    filter_list = filter_manager.list("data_source")
    compiled_filter = filter_compiler.compile(filter_list)

    pprint([x for x in filter(compiled_filter, data_source)])


try:
    protected_function()
    context_manager.close()
except GuardException:
    print("Access denied!")
