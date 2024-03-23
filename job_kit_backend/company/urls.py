from django.urls import path
from .views import (CompanyPersonalInfo,
                    download_excel_file,
                    import_data,
                    CompanyEmployeeAPIView,
                    UpdateSectorAndDepartments,
                    CompanyListView,
                    OrganisationListView,
                    JobPostingUserAPI,
                    JobGetingingUserAPI,
                    EmployeeDepartment,
                    CompanyDetailsAPIView,
                    JobsByCategoryAPIView,
                    JobsByCategoryAndSkillsAPIView)

urlpatterns = [
    path("company/<int:user_id>/",CompanyPersonalInfo.as_view(),name="company_personal_info"),
    path("download/excel_file/", download_excel_file, name="download_excel_file"),
    path("import_data/<int:company_user_id>/", import_data, name="import_data"),
    path("company/employee/<int:company_user_id>/", CompanyEmployeeAPIView.as_view(), name="company_personal_info"),
    path("update-sectors-and-departments/", UpdateSectorAndDepartments.as_view(), name="update-sectors-and-departments"),
    path("companies/", CompanyListView.as_view(), name="company-list"),
    path("organizations/", OrganisationListView.as_view(), name="organisation-list"),
    path("post/job/<int:user_id>/", JobPostingUserAPI.as_view(), name="user-job-postings-api"),
    path("get/job/<int:id>/", JobGetingingUserAPI.as_view(), name="user-job-get-api"),
    path('jobs-by-category/', JobsByCategoryAPIView.as_view(), name='jobs_by_category'),
    path('jobs-by-category-and-skills/', JobsByCategoryAndSkillsAPIView.as_view(), name='jobs_by_category_and_skills'),
    path("employee/department/", EmployeeDepartment.as_view(), name="emplyee_department"),#department listing
    path("company/detail/<int:company_id>/",CompanyDetailsAPIView.as_view(),name="company_detail"),
]
