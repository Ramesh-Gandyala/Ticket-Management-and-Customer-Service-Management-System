from types import SimpleNamespace
from unittest.mock import Mock

from django.test import SimpleTestCase

from accounts.permissions import (
    IsCustomer,
    IsPlatformAdmin,
    IsSupportAgent,
    IsSupportManager,
    IsSupportTeam,
)


class RolePermissionTests(SimpleTestCase):
    def make_request(self, *, authenticated=True, active=True,
                     superuser=False, matching_group=False):
        groups = Mock()
        groups.filter.return_value.exists.return_value = matching_group

        user = SimpleNamespace(
            is_authenticated=authenticated,
            is_active=active,
            is_superuser=superuser,
            groups=groups,
        )
        return SimpleNamespace(user=user)

    def test_anonymous_user_is_denied(self):
        request = self.make_request(authenticated=False)
        self.assertFalse(IsSupportAgent().has_permission(request, None))

    def test_inactive_user_is_denied(self):
        request = self.make_request(active=False, matching_group=True)
        self.assertFalse(IsSupportAgent().has_permission(request, None))

    def test_platform_admin_is_allowed_for_support_permissions(self):
        request = self.make_request(superuser=True)
        self.assertTrue(IsPlatformAdmin().has_permission(request, None))
        self.assertTrue(IsSupportManager().has_permission(request, None))
        self.assertTrue(IsSupportAgent().has_permission(request, None))
        self.assertTrue(IsSupportTeam().has_permission(request, None))

    def test_support_agent_is_allowed_for_agent_permission(self):
        request = self.make_request(matching_group=True)
        self.assertTrue(IsSupportAgent().has_permission(request, None))

    def test_support_agent_is_not_allowed_for_manager_permission(self):
        request = self.make_request(matching_group=False)
        self.assertFalse(IsSupportManager().has_permission(request, None))

    def test_customer_permission_is_separate_from_support_permissions(self):
        customer_request = self.make_request(matching_group=True)
        self.assertTrue(IsCustomer().has_permission(customer_request, None))

        non_customer_request = self.make_request(matching_group=False)
        self.assertFalse(IsCustomer().has_permission(non_customer_request, None))
