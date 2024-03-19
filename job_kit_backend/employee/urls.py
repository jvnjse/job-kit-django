from django.urls import path
from .views import ( EmployeePersonalInfo,
                     EmployeeEducationView,
                     SingleEducationView,
                     EmployeeExperienceView,
                     SingleExperienceView,
                     EmployeeSkillsAPIView,)
urlpatterns = [
    path("employee/<int:user_id>/",EmployeePersonalInfo.as_view(),name="employee_personal_info"),
    path("employee/education/",EmployeeEducationView.as_view(),name="employee_education"),
    path("employee/education/<int:education_id>/",SingleEducationView.as_view(),name="single_education"),
    path("employee/experience/",EmployeeExperienceView.as_view(),name="employee_experience"),
    path("employee/experience/<int:experience_id>/",SingleExperienceView.as_view(),name="single_experience"),
    path("employees/<int:user_id>/skills/",EmployeeSkillsAPIView.as_view(),name="employee-skills"),
]
