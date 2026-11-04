# Authorization module

This project uses role-based access control (RBAC) with Django Groups.

## Roles

Create these Django Groups after the database is configured by running `python manage.py setup_roles`:

- `Platform Admin`
- `Support Manager`
- `Support Agent`
- `Customer`

The command creates the groups but does not assign users. Assign each user to the appropriate group in Django Admin. Do not trust a role
sent by the frontend; role assignment must be performed by a trusted
administrator or a validated backend workflow.

## Permission hierarchy

| Permission class | Allowed groups |
| --- | --- |
| `IsPlatformAdmin` | Platform Admin |
| `IsSupportManager` | Platform Admin, Support Manager |
| `IsSupportAgent` | Platform Admin, Support Manager, Support Agent |
| `IsSupportTeam` | Platform Admin, Support Manager, Support Agent |
| `IsCustomer` | Customer |

Django superusers are treated as platform administrators. Inactive and
unauthenticated users are denied.

## Use a permission in an API view

```python
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.permissions import IsSupportAgent


class TicketAssignmentAPIView(APIView):
    permission_classes = [IsSupportAgent]

    def post(self, request):
        return Response({"message": "You may access ticket assignment."})
```

Use the narrowest permission that matches the operation. For example, ticket
assignment should normally require support-agent access, while changing
organization-wide settings should require manager or administrator access.

## Important implementation notes

- JWT authentication identifies the user; these permission classes authorize
  each request.
- Group membership is checked on each request. A role change therefore takes
  effect without putting role claims into long-lived tokens.
- Group membership requires a working database. This code can be imported and
  its permission logic unit-tested without running migrations, but assigning
  groups and testing protected endpoints requires database tables.
- Object-level rules (for example, a customer may view only their own tickets)
  must be added when ticket and organization ownership models are implemented.

## Local settings

The Django secret key is now read from the `DJANGO_SECRET_KEY` environment
variable and is intentionally not stored in Git. In PowerShell, create a fresh
local key for the current terminal session with:

```powershell
$env:DJANGO_SECRET_KEY = (python -c "import secrets; print(secrets.token_urlsafe(50))")
```

Set `DJANGO_DEBUG=True` only for local development. The secret key that was
previously committed must be treated as exposed and replaced; changing the
current file does not erase it from earlier Git history.
