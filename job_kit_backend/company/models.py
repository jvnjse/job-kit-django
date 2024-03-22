from django.db import models
from authentication.models import CustomUser
from employee.models import Skill
from administrator.models import JobCategory



# Create your models here.
class Department(models.Model):#extra------------
    name = models.CharField(max_length=100)


class CompanySector(models.Model):
    sector_name = models.CharField(max_length=100, unique=True)
    departments = models.ManyToManyField(Department) #extra----
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.sector_name
    
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
    company_sectors = models.ManyToManyField(CompanySector, blank=True)

    def __str__(self):
        return self.company_name


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
    employee_department = models.CharField(max_length=255, null=True)


class CompanyDepartment(models.Model):
    department_name = models.CharField(max_length=100, null=True)
    sector = models.ForeignKey(CompanySector, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.department_name



class JobDetail(models.Model):
    company_user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name='jobs', blank=True)
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
