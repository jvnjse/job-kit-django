from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, user_type=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_employee(self, email, password=None, **extra_fields):
        extra_fields.setdefault("user_type", "employee")
        return self.create_user(email, password, **extra_fields)

    def create_company(self, email, password=None, **extra_fields):
        extra_fields.setdefault("user_type", "company")
        return self.create_user(email, password, **extra_fields)

    def create_admin(self, email, password=None, **extra_fields):
        extra_fields.setdefault("user_type", "admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, user_type="admin", **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        extra_fields["user_type"] = user_type  # Provide user_type explicitly
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ("employee", "Employee"),
        ("company", "Company"),
        ("admin", "Admin"),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    groups = models.ManyToManyField("auth.Group", related_name="custom_users")
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="custom_users"
    )


class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_time = models.DateTimeField()

    def is_expired(self):
        return timezone.now() >= self.expiry_time

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
            self.expiry_time = self.created_at + timezone.timedelta(minutes=10)
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
class CompanySector(models.Model):
    sector_name = models.CharField(max_length=100, unique=True)
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


class Skill(models.Model):
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.full_name


class Organization(models.Model):
    organization_name = models.CharField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.organization_name


class EmployeeEducation(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    course_name = models.CharField(max_length=255, null=True)
    course_description = models.CharField(max_length=500, null=True)
    organization_name = models.ForeignKey(
        Organization, to_field="organization_name", on_delete=models.CASCADE, null=True
    )
    from_date = models.DateField()
    to_date = models.DateField()
    education_document = models.FileField(upload_to="ed_documents", null=True)


class EmployeeExperience(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    job_title = models.CharField(max_length=255, null=True)
    job_description = models.CharField(max_length=500, null=True)
    company_name = models.ForeignKey(
        Company, to_field="company_name", on_delete=models.CASCADE
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


# class JobDetails(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     job_name = models.CharField(max_length=255)
#     job_description = models.TextField()
#     key_responsibilities = models.TextField()
#     experience_required = models.CharField(max_length=255)
#     qualification_required = models.CharField(max_length=255)
#     key_skills = models.CharField(max_length=255)
#     date_posted = models.DateField()
#     application_last_date = models.DateField()
#     package_details = models.CharField(max_length=255)
#     job_type = models.CharField(max_length=255)
#     job_category = models.CharField(max_length=255)
#     company_type = models.CharField(max_length=255)
#     company_website = models.CharField(max_length=255)
#     about_company = models.CharField(max_length=255)
#     company_verified = models.BooleanField(default=False)


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

    def __str__(self):
        return self.job_title
