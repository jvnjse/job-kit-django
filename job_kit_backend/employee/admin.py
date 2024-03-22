from django.contrib import admin
from .models import (Skill, 
                     Employee, 
                     EmployeeAppliedJobs,
                     EmployeeEducation, 
                     EmployeeExperience, 
                     EmployeeJobCategory,)
# Register your models here.

admin.site.register(Skill)
admin.site.register(Employee)
admin.site.register(EmployeeAppliedJobs)
admin.site.register(EmployeeEducation)
admin.site.register(EmployeeExperience)
admin.site.register(EmployeeJobCategory)