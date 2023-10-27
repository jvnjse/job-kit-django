from django.contrib import admin


from .models import (
    CustomUser,
    OTP,
    Employee,
    Company,
    EmployeeEducation,
    EmployeeExperience,
    Skill,
    Organization,
    Company_Employee,
)

admin.site.register(CustomUser)
admin.site.register(OTP)
admin.site.register(Employee)
admin.site.register(Company)
admin.site.register(EmployeeEducation)
admin.site.register(Skill)
admin.site.register(Organization)
admin.site.register(EmployeeExperience)
admin.site.register(Company_Employee)
