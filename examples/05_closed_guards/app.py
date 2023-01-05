from guards.functional import guard, GuardResponse
from guards.context import GuardContextManager
from guards import GuardException


username = input("Username: ")


@guard(listens_on=["resource_access"])
def resource_guard(_self, _event, resource):
    print("### checking access")
    if username == "admin":
        # If we are admins, we can access everything forever
        return GuardResponse(permitted=True, closed=True)
    else:
        if resource == "secret":
            # If we are not admins, we cannot access secret
            # And we already violated a rule, so no further check is needed,
            # We already know that we won't permit anything after this
            return GuardResponse(permitted=False, closed=True)
        else:
            # If we are not admins, we can access the resource, if not secret
            # But we may try to access secret later, so we cannot close it yet
            return GuardResponse(permitted=True, closed=False)


context_manager = GuardContextManager()


@context_manager.require(resource_guard)
def resource_access_function():
    while True:
        resource = input("Resource: ")
        if resource == "exit":
            break
        context_manager.current_context.emit("resource_access", resource)
        print(f"You have access to {resource}")


try:
    resource_access_function()
    context_manager.close()
except GuardException:
    print("Access denied!")
