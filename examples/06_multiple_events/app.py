from guards.functional import guard, GuardResponse
from guards.context import GuardContextManager
from guards import GuardException, RUN_EVENT

username = input("Cached username: ") or None


@guard(listens_on=[RUN_EVENT, "authenticate"])
def auth_guard():
    authenticated = username is not None
    print("### checking if authenticated: ", authenticated)
    return GuardResponse(permitted=authenticated, closed=authenticated)


context_manager = GuardContextManager()


def authenticate():
    global username
    username = input("External username: ") or None
    context_manager.current_context.emit("authenticate")


@context_manager.require(auth_guard)
def protected_function():
    if username is None:
        authenticate()

    context_manager.current_context.check()
    print(f"Hi, {username}")


try:
    protected_function()
    context_manager.close()
except GuardException:
    print("Access denied!")
