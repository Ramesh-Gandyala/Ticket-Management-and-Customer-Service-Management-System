from types import SimpleNamespace

from django.test import SimpleTestCase

from accounts.permissions import (
    IsCustomer,
    IsPlatformAdmin,
    IsSupportAgent,
    IsSupportManager,
    IsSupportTeam,
)
from accounts.roles import Role


class FakeGroups:
    def __init__(self, names=()):
        self.names = set(names)

    def filter(self, *, name__in):
        matched = bool(self.names.intersection(name__in))
        return SimpleNamespace(exists=lambda: matched)


class RolePermissionTests(SimpleTestCase):
    def make_request(self, *, authenticated=True, active=True,
                     superuser=False, roles=()):
        user = SimpleNamespace(
            is_authenticated=authenticated,
            is_active=active,
            is_superuser=superuser,
            groups=FakeGroups(roles),
        )
        return SimpleNamespace(user=user)

    def test_anonymous_user_is_denied(self):
        request = self.make_request(authenticated=False)
        self.assertFalse(IsSupportAgent().has_permission(request, None))

    def test_inactive_user_is_denied(self):
        request = self.make_request(
            active=False,
            roles=(Role.SUPPORT_AGENT,),
        )
        self.assertFalse(IsSupportAgent().has_permission(request, None))

    def test_superuser_is_allowed_for_support_permissions(self):
        request = self.make_request(superuser=True)
        self.assertTrue(IsPlatformAdmin().has_permission(request, None))
        self.assertTrue(IsSupportManager().has_permission(request, None))
        self.assertTrue(IsSupportAgent().has_permission(request, None))
        self.assertTrue(IsSupportTeam().has_permission(request, None))

    def test_platform_admin_group_has_admin_and_inherited_support_access(self):
        request = self.make_request(roles=(Role.PLATFORM_ADMIN,))
        self.assertTrue(IsPlatformAdmin().has_permission(request, None))
        self.assertTrue(IsSupportManager().has_permission(request, None))
        self.assertTrue(IsSupportAgent().has_permission(request, None))

    def test_support_agent_cannot_access_manager_or_admin_permissions(self):
        request = self.make_request(roles=(Role.SUPPORT_AGENT,))
        self.assertFalse(IsPlatformAdmin().has_permission(request, None))
        self.assertFalse(IsSupportManager().has_permission(request, None))
        self.assertTrue(IsSupportAgent().has_permission(request, None))

    def test_customer_role_is_separate_from_support_roles(self):
        request = self.make_request(roles=(Role.CUSTOMER,))
        self.assertTrue(IsCustomer().has_permission(request, None))
        self.assertFalse(IsSupportTeam().has_permission(request, None))
