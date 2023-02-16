from guards.functional import guard
from guards.context import GuardContextManager
from guards import GuardException

username = input("Username: ") or None

context_manager = GuardContextManager()


@guard(default_permitted=True, close=True)
def greet_guard():
    if username == "admin":
        context_manager.current_context.set("greeting", "Hi")
    else:
        context_manager.current_context.set("greeting", "Welcome")


@context_manager.require(greet_guard)
def protected_function():
    greeting = context_manager.current_context.get("greeting", "")
    print(f"{greeting}, {username}")


try:
    protected_function()
    context_manager.close()
except GuardException:
    print("Access denied!")
