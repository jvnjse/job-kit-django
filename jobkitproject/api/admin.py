from django.contrib import admin


from .models import CustomUser, OTP, Employee, Company, EmployeeExperienceEducation

admin.site.register(CustomUser)
admin.site.register(OTP)
admin.site.register(Employee)
admin.site.register(Company)
admin.site.register(EmployeeExperienceEducation)
