# Context manager

To make guards much more powerful, we need to manage the context for ourself. This was handled by the require decorator in the previous examples.

This needs to be set up for every function call. This is usually set up and closed before and after every request.

## Theory

A guard context is a place where guards live. It is possible to have multiple nested guard contexts, so there is a context manager that gives us access to the current context.

## Setting up a context manager

```python
from guards.context import GuardContextManager

def admin_query():
    context_manager = GuardContextManager()

    # Our guarded action goes here

    context_manager.close()
```

As we need a separate context manager per call, it makes sense to put it in a function.

*Note: This is not a convinient use case in such a simple example, but in action it will make much more sense*

## Using context manager to require a guard

```python
@context_manager.require(admin_guard)
def admin_function():
    print("Hello admin!")

```

`context_manager.require` will require a guard in this context.

This will make us be able to use all the features of this library.