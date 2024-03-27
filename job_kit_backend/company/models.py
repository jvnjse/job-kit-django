from django.db import models
from authentication.models import CustomUser
from employee.models import Skill



# Create your models here.
class Department(models.Model):#extra------------
    name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} (ID: {self.id})"



    
class Company(models.Model):
    company_user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True
    )
    company_name = models.CharField(max_length=255, unique=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)
    profile_image = models.ImageField(upload_to="company_logo", null=True)
    is_verified = models.BooleanField(default=False)
    company_website = models.CharField(max_length=100, null=True)
    # company_sectors = models.ManyToManyField(CompanySector, blank=True)

    def __str__(self):
         return f"{self.company_name} (ID: {self.id})"

class CompanySector(models.Model):
    sector_name = models.CharField(max_length=100)
    departments = models.ManyToManyField(Department) #extra----
    company_user_id = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'company'},
    )#extra-------------------------------------------------------company id or user id
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.sector_name

class Organization(models.Model):
    organization_name = models.CharField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.organization_name


class Company_Employee(models.Model):
    company_user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    employee_name = models.CharField(max_length=100, null=True)
    employee_position = models.CharField(max_length=100, null=True)
    employee_phone_number = models.CharField(max_length=20, null=True)
    employee_email = models.CharField(max_length=50, null=True)
    employee_department = models.ManyToManyField(Department) 
    
    def __str__(self):
        return f"{self.employee_name} (ID: {self.id})"

#----------------------this section may not be needed trying another logic----------------
# class CompanyDepartment(models.Model):
#     department_name = models.ManyToManyField(Department) 
#     sector = models.ForeignKey(CompanySector, on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return f"{self.department_name} (ID: {self.id})"
#---------------------------------------------------------------------------------------------



class JobDetail(models.Model):
    company_user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    qualifications_requirements = models.TextField()
    location = models.CharField(max_length=100)
    WORK_MODE_CHOICES = [
        ("Full-Time", "Full-Time"),
        ("Part-Time", "Part-Time"),
        ("Contract", "Contract"),
        ("Remote", "Remote"),
    ]
    mode_of_work = models.CharField(max_length=20, choices=WORK_MODE_CHOICES)
    salary_range_from = models.DecimalField(max_digits=10, decimal_places=2)
    salary_range_to = models.DecimalField(max_digits=10, decimal_places=2)
    application_deadline = models.DateField()
    tags = models.ManyToManyField(Skill, blank=True)
    contact_details = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.job_title
