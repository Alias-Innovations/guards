# Closed guards

A guard has a hidden parameter, `closed`.

If a guard is closed, it means that it will not run again, its last "answer" is its "final answer".

For example, if we access multiple resources, and we emit the `resource_access` event multiple times, it runs the guard every time.

But if our guard sees that we are admin, it can decide that no further check is needed, everything is permitted.

Or otherwise, if we see something that is not permitted, we can say that we deny everything else. When a guard is closed and denied, an exception is thrown immediately.

## GuardResponse

```python
from guards.functional import guard, GuardResponse

@guard(listens_on=["resource_access"])
def resource_guard(_self, _event, resource):
    if username == "admin":
        # If we are admins, we can access everything forever
        return GuardResponse(permitted=True, closed=True)
```

We have seen that we can return a boolean from our guards, but we can return GuardResponse objects as well.

This object tells if the guard is closed, and if the access is permitted.

## Checking guards

We have seen this in the previous example:

```python
    context_manager.current_context.check()
```

This basically checks the open guards as well. If a guard is not permitted, but not closed, it does not generate an exception immediately.

To ensure that we don't have any guards that are not permitted, even if they are not closed, we need to call this function. This happens automatically when the context manager is closed.


