from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create your models here.
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

        