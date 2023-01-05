from guards.functional import guard
from guards.context import GuardContextManager
from guards import GuardException


username = input("Username: ")


@guard
def admin_guard():
    return "admin" in username


@guard
def super_guard():
    return "super" in username


guards = GuardContextManager()


@guards.require(admin_guard, super_guard)
def superadmin_function():
    print("Hello superadmin!")


try:
    superadmin_function()
except GuardException:
    print("Access denied")
