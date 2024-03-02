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
    CompanyEmployeeAPIView,
    import_data,
    download_excel_file,
    UpdateSectorAndDepartments,
    JobPostingUserAPI,
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
        "company/<int:user_id>/",
        CompanyPersonalInfo.as_view(),
        name="company_personal_info",
    ),
    path(
        "company/employee/<int:company_user_id>/",
        CompanyEmployeeAPIView.as_view(),
        name="company_personal_info",
    ),
    path(
        "update-sectors-and-departments/",
        UpdateSectorAndDepartments.as_view(),
        name="update-sectors-and-departments",
    ),
    path(
        "post/job/<int:user_id>/",
        JobPostingUserAPI.as_view(),
        name="user-job-postings-api",
    ),
    path("import_data/<int:company_user_id>/", import_data, name="import_data"),
    path("download/excel_file/", download_excel_file, name="download_excel_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
