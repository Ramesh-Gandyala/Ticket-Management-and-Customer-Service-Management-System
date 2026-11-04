
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def validate_user_password(password, user=None):

    try:
        validate_password(password, user=user)

        return {
            "valid": True,
            "errors": []
        }

    except ValidationError as error:

        return {
            "valid": False,
            "errors": error.messages
        }
