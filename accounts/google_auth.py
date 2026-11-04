
from django.conf import settings

from google.auth.transport import requests
from google.oauth2 import id_token


def verify_google_id_token(token):

    try:
        # Step 1: Verify Google's ID token
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            audience=settings.GOOGLE_CLIENT_ID
        )

        # Step 2: Check whether Google's email is verified
        if not id_info.get("email_verified"):
            return {
                "success": False,
                "message": "Google email is not verified."
            }

        # Step 3: Return verified Google information
        return {
            "success": True,
            "google_user": {
                "google_id": id_info["sub"],
                "email": id_info["email"].lower(),
                "first_name": id_info.get("given_name", ""),
                "last_name": id_info.get("family_name", ""),
                "picture": id_info.get("picture", "")
            }
        }

    except ValueError:
        return {
            "success": False,
            "message": "Invalid or expired Google ID token."
        }

    except Exception:
        return {
            "success": False,
            "message": "Unable to verify Google identity."
        }
