"""
Canonical role names for the support platform.

Roles are represented by Django Groups so they can be assigned and changed
without adding a custom role column to the User model.
"""


class Role:
    PLATFORM_ADMIN = "Platform Admin"
    SUPPORT_MANAGER = "Support Manager"
    SUPPORT_AGENT = "Support Agent"
    CUSTOMER = "Customer"


ALL_ROLES = (
    Role.PLATFORM_ADMIN,
    Role.SUPPORT_MANAGER,
    Role.SUPPORT_AGENT,
    Role.CUSTOMER,
)

# Permission inheritance: higher support roles include lower support access.
# The Platform Admin role itself remains exclusive to platform administrators.
ROLE_HIERARCHY = {
    Role.PLATFORM_ADMIN: (
        Role.PLATFORM_ADMIN,
    ),
    Role.SUPPORT_MANAGER: (
        Role.PLATFORM_ADMIN,
        Role.SUPPORT_MANAGER,
    ),
    Role.SUPPORT_AGENT: (
        Role.PLATFORM_ADMIN,
        Role.SUPPORT_MANAGER,
        Role.SUPPORT_AGENT,
    ),
    Role.CUSTOMER: (
        Role.CUSTOMER,
    ),
}
