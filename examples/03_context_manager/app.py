from guards.functional import guard
from guards.context import GuardContextManager
from guards import GuardException


username = input("Username: ")


@guard
def admin_guard():
    return username == "admin"


def admin_query():
    context_manager = GuardContextManager()

    @context_manager.require(admin_guard)
    def admin_function():
        print("Hello admin!")

    try:
        admin_function()
        context_manager.close()
    except GuardException:
        print("Access denied!")


admin_query()
