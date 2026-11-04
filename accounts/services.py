
from django.contrib.auth import get_user_model


def build_customer_user(validated_data):

    User = get_user_model()

    # Create a copy of validated data
    user_data = validated_data.copy()

    # Extract the raw password
    password = user_data.pop("password")

    # Prepare user object in memory
    user = User(**user_data)

    # Hash the password
    user.set_password(password)

    # Apply customer account permissions
    user.is_staff = False
    user.is_superuser = False

    # Email verification is pending
    user.is_email_verified = False
    user.is_active = False

    return user



def build_google_customer_user(google_user_data):

    User = get_user_model()

    google_id = google_user_data["google_id"]
    email = google_user_data["email"]

    # Generate a username using Google's unique ID
    username = f"google_{google_id}"

    # Prepare user information
    user = User(
        username=username,
        email=email,
        first_name=google_user_data.get("first_name", ""),
        last_name=google_user_data.get("last_name", ""),
        google_id=google_id,
        is_email_verified=True,
        is_active=True,
        is_staff=False,
        is_superuser=False
    )

    # Google users don't need a local password
    user.set_unusable_password()

    # Return an unsaved user object
    return user
