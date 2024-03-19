from rest_framework import serializers
from .models import CustomUser

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
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email_or_username = attrs.get("email_or_username")
        password = attrs.get("password")

        # Check if the input is a valid email address
        is_email = "@" in email_or_username

        if is_email:
            # If it's an email, try to find the user by email
            try:
                user = CustomUser.objects.get(email=email_or_username)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid email")
        else:
            # If it's not an email, try to find the user by username
            try:
                user = CustomUser.objects.get(username=email_or_username)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid username")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password")

        attrs["user"] = user
        return attrs


class OTPVerificationSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)
