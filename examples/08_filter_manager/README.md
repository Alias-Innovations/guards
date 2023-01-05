# Filter manager

This is for a bit more advanced use case.
If we want to filter given resources in specific guards, we can do that with the filter manager utility.

This is based on context store.

## FilterCompiler

```python
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
```

We can have many different types of data source. In this example we use a simple list, but it could be an orm, or an SQL expression.

To filter lists, we can have predicates, and use the builtin `filter` method of python.

We need to define our basic logic operators to combine our filters.

In this case, the filters are predicate functions that return true if a given item is in the output, and false if it is filtered.

So if we call `_and` with predicate functions, it returns a function that will call all the predicates we gave to `_and`, and it will return True only if all of those predicates return True.

## FilterLists

Many types of filters can exist. I.E. if we work with an RDBMS, we have different tables.

We can have multiple filter lists that represent filters of a given table.

## Applying filters

```python
@guard(default_permitted=True, close=True)
def filter_guard():
    filter_manager = get_filter_manager(context_manager.current_context)

    filter_list = filter_manager.list("data_source")
    for type in access_list:
        filter_list.include(lambda x, type=type: x["type"] == type)
```

We create a filter list with the key `"data_source"`, then we add our filters as `include` filters.

Include filters will say that these values are included, all the others are excluded.

## Filtering a data source

```python
@context_manager.require(filter_guard)
def protected_function():
    filter_manager = get_filter_manager(context_manager.current_context)
    filter_list = filter_manager.list("data_source")
    compiled_filter = filter_compiler.compile(filter_list)

    pprint([x for x in filter(compiled_filter, data_source)])
```

We just take our filter list, and compile a filter with our filter compiler.

It will give us back a compound filter that is built using the operators we specified in the filter compiler.

Then we just apply our filter, and print the results.