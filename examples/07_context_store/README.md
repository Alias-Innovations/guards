# Context store

It is great to be able to deny or grant access to a given resource, but what if we want something more specific?

Like if we are admins, we should greet with `"Hi"` but when we are users, we should greet with `"Welcome"`.

To make it possible, we don't need to restrict access, we need to alter behaviour.

The actual implementation is application specific, and not the goal of this package, but we provide a way to make this implementation possible through context stores.

This is a dictionary in the guard context that is intended to be used in both the guards and in the protected function.

## Guard decorator parameters

```python
@guard(default_permitted=True, close=True)
def greet_guard():

```

We did not cover `default_permitted` and `close` parameters of the guard decorator yet.

`default_permitted` specifies if we should permit by default, even if we don't run the guard. This is `False` by default.

`close` tells the guard to close itself after the first run.

## Setting value

```python
@guard(default_permitted=True, close=True)
def greet_guard():
    if username == "admin":
        context_manager.current_context.set("greeting", "Hi")
```

This `current_context.set(key, value)`, as the name implies, sets the value of `key` to `value`.

## Getting value

```python
@context_manager.require(greet_guard)
def protected_function():
    greeting = context_manager.current_context.get("greeting", "")
    print(f"{greeting}, {username}")
```

`current_context.get(key, default_value)` gets the `key` from the store, and if it is not present, it returns `default_value`.
