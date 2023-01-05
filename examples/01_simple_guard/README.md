# Simple guard

In this example we set up our guard context, write our first guard, and use it on a function.

## Guard

We set up a *functional guard*, that is a function decorated with `@guard`.

This function returns True if access is granted or False if access is denied.

## Require

The guarded function is decorated with `@require`. So when we call it, the guard passed to it as parameter will be ensured.
