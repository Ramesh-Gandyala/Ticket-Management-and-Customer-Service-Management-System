from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class UsernameOrEmailBackend(ModelBackend):
    """
    Authenticate with either a username or an email address.

    Email matching is case-insensitive. The backend deliberately uses the
    configured custom user model instead of importing a concrete User class.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        login_value = username or kwargs.get("email")

        if not login_value or not password:
            return None

        login_value = login_value.strip()

        try:
            if "@" in login_value:
                user = User.objects.get(email__iexact=login_value)
            else:
                user = User.objects.get(username__iexact=login_value)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
