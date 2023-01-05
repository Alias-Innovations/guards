# Multiple events

We can pass multiple events to a guard, and the guard will be ran for every event.

This is useful in an edge case that is possible with the `GuardResponse` we did not show in the previous example.

Let's imagine we have an external authentication service, and an internal cache for authentication.

It is possible, that we immediately have an answer if we are authenticated, but it is possible that we need to query the external service.

We may or may not know if we are authenticated when we run the function.

## RUN_EVENT

```python
from guards import RUN_EVENT

@guard(listens_on=[RUN_EVENT, "authenticate"])
def auth_guard():
```

When we don't define any event, the guard runs when we call our protected function.
When we define an event, it does runs only when that event is emitted.

If we want both, we need to specify the run event and our custom event as well.

The key of the event which is ran when our function gets ran is `RUN_EVENT`

## Explanation

In this example, first we ask a cached username. It can be empty, or given.

If it is given, the `auth_guard` sees that we have an username, so it permits and closes immediately.

If it is not given, the `auth_guard` will not permit, but it will not close, so the external service can authenticate later.

When we don't have an username, we call our external service, which will ask an external username, then emit an `authenticate` event.

If it is given, the `auth_guard` sees that we now have an username, so it permits and closes now.

But if it is not given, the `auth_guard` will still not close, but not permit.

To ensure that we have an username in the protected part of the function, we need to call `check`, and it will fail if our guard is not permitted, even if it is not closed.