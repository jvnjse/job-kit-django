from django.urls import path
from .views import (
    RegistrationView,
    OTPVerificationView,
    LoginView,
    CheckUsernameAvailability,)


urlpatterns = [
    path("register/<str:user_type>/", RegistrationView.as_view(), name="register"),
    path("verify-otp/", OTPVerificationView.as_view(), name="verify-otp"),
    path("login/", LoginView.as_view(), name="login"),
    path("check-username/", CheckUsernameAvailability.as_view(), name="check-username"),
]
