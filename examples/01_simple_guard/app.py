from guards.functional import guard, require
from guards import GuardException

username = input("Username: ")


@guard
def admin_guard():
    return username == "admin"


@require(admin_guard)
def admin_function():
    print("Hello admin!")


try:
    admin_function()
except GuardException:
    print("Access denied")
