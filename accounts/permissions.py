"""
Reusable role-based permissions for Django REST Framework.

Assign one or more of the canonical Django Groups defined in accounts.roles
to each user. These permissions read group membership at request time, so
role changes take effect without waiting for an existing JWT to expire.
"""

from rest_framework.permissions import BasePermission

from accounts.roles import ROLE_HIERARCHY, Role


class RolePermission(BasePermission):
    """Base permission that checks active authenticated users and group roles."""

    allowed_roles = ()

    def has_permission(self, request, view):
        user = getattr(request, "user", None)

        if (
            user is None
            or not getattr(user, "is_authenticated", False)
            or not getattr(user, "is_active", False)
        ):
            return False

        # Django superusers are platform administrators.
        if getattr(user, "is_superuser", False):
            return True

        if not self.allowed_roles:
            return False

        return user.groups.filter(name__in=self.allowed_roles).exists()


class IsPlatformAdmin(RolePermission):
    """Allow platform administrators only."""

    allowed_roles = ROLE_HIERARCHY[Role.PLATFORM_ADMIN]


class IsSupportManager(RolePermission):
    """Allow platform administrators and support managers."""

    allowed_roles = ROLE_HIERARCHY[Role.SUPPORT_MANAGER]


class IsSupportAgent(RolePermission):
    """Allow platform administrators, managers, and support agents."""

    allowed_roles = ROLE_HIERARCHY[Role.SUPPORT_AGENT]


class IsCustomer(RolePermission):
    """Allow customers only; support roles do not implicitly become customers."""

    allowed_roles = ROLE_HIERARCHY[Role.CUSTOMER]


class IsSupportTeam(RolePermission):
    """Allow any support staff role, excluding ordinary customers."""

    allowed_roles = (
        Role.PLATFORM_ADMIN,
        Role.SUPPORT_MANAGER,
        Role.SUPPORT_AGENT,
    )
