from django.urls import path
from .views import (
    RegistrationView,
    OTPVerificationView,
    LoginView,
    EmployeePersonalInfo,
    EmployeeExperienceView,
    SingleExperienceView,
    EmployeeEducationView,
    SingleEducationView,
    CompanyPersonalInfo,
    CompanyListView,
    EmployeeSkillsAPIView,
    OrganisationListView,
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
        "employee/experience/<int:experience_id>/",
        SingleExperienceView.as_view(),
        name="single_experience",
    ),
    path(
        "employee/education/",
        EmployeeEducationView.as_view(),
        name="employee_education",
    ),
    path(
        "employee/education/<int:education_id>/",
        SingleEducationView.as_view(),
        name="single_education",
    ),
    path(
        "employees/<int:user_id>/skills/",
        EmployeeSkillsAPIView.as_view(),
        name="employee-skills",
    ),
    # organisation
    path("organizations/", OrganisationListView.as_view(), name="organisation-list"),
    # company
    path("companies/", CompanyListView.as_view(), name="company-list"),
    path(
        "company/<int:company_user_id>/",
        CompanyPersonalInfo.as_view(),
        name="company_personal_info",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
