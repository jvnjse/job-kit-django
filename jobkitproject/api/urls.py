from django.urls import path
from .views import (
    RegistrationView,
    OTPVerificationView,
    LoginView,
    EmployeePersonalInfo,
    EmployeeExperienceView,
    EmployeeEducationView,
    CompanyPersonalInfo,
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("register/<str:user_type>/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify-otp/", OTPVerificationView.as_view(), name="verify-otp"),
    # employeee
    path(
        "employee/<int:user_id>/",
        EmployeePersonalInfo.as_view(),
        name="employee_personal_info",
    ),
    path(
        "employee/experience/",
        EmployeeExperienceView.as_view(),
        name="employee_experience",
    ),
    path(
        "employee/education/",
        EmployeeEducationView.as_view(),
        name="employee_education",
    ),
    # company
    path(
        "company/<int:user_id>/",
        CompanyPersonalInfo.as_view(),
        name="company_personal_info",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
