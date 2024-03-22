from django.contrib import admin
from .models import (Department, 
                     CompanySector, 
                     Company_Employee, 
                     CompanyDepartment, 
                     Company, 
                     JobDetail,)
# Register your models here.

admin.site.register(Department)
admin.site.register(Company)
admin.site.register(Company_Employee)
admin.site.register(CompanyDepartment)
admin.site.register(JobDetail)
admin.site.register(CompanySector)