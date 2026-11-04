
from django.urls import path

from accounts.views import (CustomerRegistrationView,
                            LoginAPIView,
                            ProtectedAPIView,
                            CustomTokenRefreshView,
                            ProtectedAPIView,
                            LogoutAPIView,
                            GoogleLoginAPIView,
)


urlpatterns = [
    path(
        "register/validate/",
        CustomerRegistrationView.as_view(),
        name="customer-registration-validation"
    ),

    path(
        "login/",
        LoginAPIView.as_view(),
        name="customer-login"
    ),

    path(
        "token/refresh/",
        CustomTokenRefreshView.as_view(),
        name="token-refresh"
    ),

    path(
        "protected/",
        ProtectedAPIView.as_view(),
        name="protected-api"
    ),

    path(
        "logout/",
        LogoutAPIView.as_view(),
        name="customer-logout"
    ),

    path(
        'google-login/',
        GoogleLoginAPIView.as_view(),
        name='google-login'
    ),
]
