from django.urls import path
from .views import RegistrationView, OTPVerificationView, LoginView

urlpatterns = [
    path("register/<str:user_type>/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify-otp/", OTPVerificationView.as_view(), name="verify-otp"),
]
