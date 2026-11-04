
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class UsernameOrEmailBackend(ModelBackend):

    def authenticate(
        self,
        request,
        username=None,
        password=None,
        **kwargs
    ):

        User = get_user_model()

        # Get username or email from the login input
        login_value = username or kwargs.get("email")

        if not login_value or not password:
            return None

        try:
            # Check whether input is an email address
            if "@" in login_value:

                user = User.objects.get(
                    email__iexact=login_value
                )

            else:

                user = User.objects.get(
                    username__iexact=login_value
                )

        except User.DoesNotExist:
            return None

        # Verify password and account status
        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
