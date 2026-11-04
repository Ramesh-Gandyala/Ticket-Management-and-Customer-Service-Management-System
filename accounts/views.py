
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.serializers import (
    CustomerRegistrationSerializer,LoginSerializer
)

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import TokenRefreshView

from rest_framework.permissions import IsAuthenticated

from rest_framework.exceptions import ValidationError

from accounts.serializers import GoogleLoginSerializer
from accounts.google_auth import verify_google_id_token
from accounts.services import build_google_customer_user



class CustomTokenRefreshView(TokenRefreshView):
    pass


class CustomerRegistrationView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = CustomerRegistrationSerializer(
            data=request.data
        )

        # Validate customer registration information
        if serializer.is_valid():

            validated_data = serializer.validated_data

            # Return only non-sensitive information
            response_data = {
                "username": validated_data["username"],
                "email": validated_data["email"],
                "first_name": validated_data["first_name"],
                "last_name": validated_data["last_name"],
            }

            return Response(
                {
                    "success": True,
                    "message": (
                        "Registration information validated. "
                        "No account has been created."
                    ),
                    "data": response_data
                },
                status=status.HTTP_200_OK
            )

        # Return validation errors
        return Response(
            {
                "success": False,
                "message": "Registration validation failed.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    

class LoginAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        # Step 1: Validate incoming login data
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "Invalid login details.",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Step 2: Extract validated credentials
        login_identifier = serializer.validated_data[
            "login_identifier"
        ]

        password = serializer.validated_data["password"]

        # Step 3: Authenticate the user
        user = authenticate(
            request,
            username=login_identifier,
            password=password
        )

        # Step 4: Handle failed authentication
        if user is None:
            return Response(
                {
                    "success": False,
                    "message": "Invalid username/email or password."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Step 5: Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        access_token = refresh.access_token

        # Step 6: Return successful login response
        return Response(
            {
                "success": True,
                "message": "Login successful.",

                "tokens": {
                    "refresh": str(refresh),
                    "access": str(access_token)
                },

                "user": {
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
            },
            status=status.HTTP_200_OK
        )


class ProtectedAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response(
            {
                "success": True,
                "message": "You have accessed a protected API.",
                "user": {
                    "username": request.user.username,
                    "email": request.user.email
                }
            },
            status=status.HTTP_200_OK
        )


class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Step 1: Receive refresh token
        refresh_token = request.data.get("refresh")

        # Step 2: Check whether refresh token exists
        if not refresh_token:
            return Response(
                {
                    "success": False,
                    "message": "Refresh token is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Step 3: Convert token string into RefreshToken
            token = RefreshToken(refresh_token)

            # Step 4: Check token ownership
            if str(token["user_id"]) != str(request.user.pk):
                return Response(
                    {
                        "success": False,
                        "message": "Invalid refresh token."
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Step 5: Blacklist refresh token
            token.blacklist()

            # Step 6: Return logout response
            return Response(
                {
                    "success": True,
                    "message": "Logout successful."
                },
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {
                    "success": False,
                    "message": "Invalid or expired refresh token."
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class GoogleLoginAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = GoogleLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        google_token = serializer.validated_data["id_token"]

        result = verify_google_id_token(google_token)

        if not result["success"]:
            return Response(
                {
                    "success": False,
                    "message": result["message"]
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        google_user = result["google_user"]

        return Response(
            {
                "success": True,
                "message": "Google identity verified successfully.",
                "google_user": {
                    "google_id": google_user["google_id"],
                    "email": google_user["email"],
                    "first_name": google_user["first_name"],
                    "last_name": google_user["last_name"],
                    "picture": google_user["picture"]
                },
                "next_step": "Account creation and JWT login will be added later."
            },
            status=status.HTTP_200_OK
        )


