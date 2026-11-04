
from rest_framework import serializers

from accounts.validators import validate_user_password


class CustomerRegistrationSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=150
    )

    email = serializers.EmailField(
        max_length=255
    )

    first_name = serializers.CharField(
        max_length=150
    )

    last_name = serializers.CharField(
        max_length=150
    )

    phone_number = serializers.CharField(
        max_length=15,
        required=False,
        allow_blank=True
    )

    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False
    )

    confirm_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False
    )

    def validate_username(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Username cannot be empty."
            )

        return value

    def validate_email(self, value):

        return value.strip().lower()

    def validate_password(self, value):

        result = validate_user_password(value)

        if not result["valid"]:
            raise serializers.ValidationError(
                result["errors"]
            )

        return value

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:

            raise serializers.ValidationError({
                "confirm_password": "Passwords did not match."
            })

        attrs.pop("confirm_password")

        return attrs


class LoginSerializer(serializers.Serializer):

    login_identifier = serializers.CharField(
        max_length=255
    )

    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False
    )

    def validate_login_identifier(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Username or email is required."
            )

        return value


class GoogleLoginSerializer(serializers.Serializer):

    id_token = serializers.CharField(
        required=True,
        write_only=True,
        trim_whitespace=True
    )

    def validate_id_token(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Google ID token is required."
            )

        return value

