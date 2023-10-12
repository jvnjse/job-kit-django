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
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
class Company(models.Model):
    company_user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # company_email = models.EmailField()
    company_name = models.CharField(max_length=255, unique=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    company_unique_id = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=10)


class Organization(models.Model):
    organization_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.organization_name


class Skill(models.Model):
    name = models.CharField(unique=True, max_length=255)


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


class EmployeeEducation(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    course_job_name = models.CharField(max_length=255, null=True)
    organization_name = models.ForeignKey(
        Organization, to_field="organization_name", on_delete=models.CASCADE
    )
    from_date = models.DateField()
    to_date = models.DateField()
    education_document = models.FileField(upload_to="ed_ex_documents")


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


class JobDetails(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=255)
    job_description = models.TextField()
    key_responsibilities = models.TextField()
    experience_required = models.CharField(max_length=255)
    qualification_required = models.CharField(max_length=255)
    key_skills = models.CharField(max_length=255)
    date_posted = models.DateField()
    application_last_date = models.DateField()
    package_details = models.CharField(max_length=255)
    job_type = models.CharField(max_length=255)
    job_category = models.CharField(max_length=255)
    company_type = models.CharField(max_length=255)
    company_website = models.CharField(max_length=255)
    about_company = models.CharField(max_length=255)
    company_verified = models.BooleanField(default=False)


class CompanyDepartment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_department_name = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
