from guards.functional import guard
from guards.context import GuardContextManager
from guards import GuardException


username = input("Username: ")


@guard(listens_on=["resource_access"])
def resource_guard(_self, _event, resource):
    # If we are admins, we can access everything
    if username == "admin":
        return True
    # If we are not admins, we can access everything except the secret
    else:
        return resource != "secret"


context_manager = GuardContextManager()


@context_manager.require(resource_guard)
def resource_access_function():
    resource = input("Resource: ")
    context_manager.current_context.emit("resource_access", resource)
    context_manager.current_context.check()
    print(f"You have access to {resource}")


try:
    resource_access_function()
    context_manager.close()
except GuardException:
    print("Access denied!")
