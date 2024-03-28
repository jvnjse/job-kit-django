from django.db import models
from authentication.models import CustomUser
from administrator.models import JobCategory


# Create your models here.

class Skill(models.Model):
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)

class Employee(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to="profile_image")
    dob = models.DateField()
    mobile = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=10)
    skills = models.ManyToManyField(Skill, blank=True)
    job_category = job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, blank=True, null=True)
    

    def __str__(self):
        return f"{self.user_id} - {self.full_name}"
    

class EmployeeEducation(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    course_name = models.CharField(max_length=255, null=True)
    course_description = models.CharField(max_length=500, null=True)
    organization_name = models.ForeignKey( 
        'company.Organization', to_field="organization_name", on_delete=models.CASCADE, null=True
    )
    from_date = models.DateField()
    to_date = models.DateField()
    education_document = models.FileField(upload_to="ed_documents", null=True)


class EmployeeExperience(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    job_title = models.CharField(max_length=255, null=True)
    job_description = models.CharField(max_length=500, null=True)
    company_name = models.ForeignKey(
        'company.Company', to_field="company_name", on_delete=models.CASCADE
    )
    from_date = models.DateField()
    to_date = models.DateField()
    experience_document = models.FileField(upload_to="ex_documents")


class EmployeeAppliedJobs(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    saved_job_id = models.IntegerField()
    applied_job_id = models.IntegerField()

class EmployeeJobCategory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category_id = models.IntegerField()
    new_applied_category = models.CharField(max_length=255)

    # employee_user_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    # job_name = models.CharField(max_length=255)
    # logo_image = models.ImageField(upload_to="company_logos/")
    # job_position_in_company = models.CharField(max_length=255)
    # joined_date = models.DateField()
    # end_date = models.DateField()
    # is_working = models.BooleanField(default=False)
    # is_working_employee = models.BooleanField(default=False)