# Events

A guard can listen to specific events. By default it listens for an internal run event, but we can modify this behaviour

## Note

We have understood that a context manager manages a single scope. Like a request, or in our last example, the `admin_query` function.

This time we will omit a function, but notice that it should still need to be in a function if it was used multiple times.

## Listener guard

```python
@guard(listens_on=["resource_access"])
def resource_guard(_self, _event, resource):
    # If we are admins, we can access everything
    if username == "admin":
        return True
    # If we are not admins, we can access everything except the secret
    else:
        return resource != "secret"

```

This guard is set up to listen for `resource_access` events, and gets the resource as parameter.

## Emitting events

```python
    context_manager.current_context.emit("resource_access", resource)
```

We can simply call `emit` of the current context.

The first argument is the event key, and the rest will be passed to the guard.

## Checking guards

This will make sense in the next example.
