from rest_framework import serializers
from .models import CustomUser, Employee, EmployeeExperienceEducation, Company
from django.contrib.auth import get_user_model


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "is_staff",
            "is_active",
            "user_type",
            "password",
            "is_superuser",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class EmployeeregisterSerializer(CustomUserSerializer):
    user_type = serializers.CharField(default="employee", write_only=True)


class CompanyregisterSerializer(CustomUserSerializer):
    user_type = serializers.CharField(default="company", write_only=True)


class AdminSerializer(CustomUserSerializer):
    user_type = serializers.CharField(default="admin", write_only=True)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid email")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password")

        attrs["user"] = user
        return attrs


class OTPVerificationSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class EmployeeExperienceSerializer(serializers.ModelSerializer):
    experience_education_document = serializers.FileField(use_url=False)

    class Meta:
        model = EmployeeExperienceEducation
        fields = [
            "user_id",
            "course_job_name",
            "organization_id",
            "from_date",
            "to_date",
            "is_experience",
            "experience_education_document",
        ]


class EmployeeEducationSerializer(serializers.ModelSerializer):
    experience_education_document = serializers.FileField(use_url=False)

    class Meta:
        model = EmployeeExperienceEducation
        fields = [
            "user_id",
            "course_job_name",
            "organization_id",
            "from_date",
            "to_date",
            "is_education",
            "experience_education_document",
        ]
