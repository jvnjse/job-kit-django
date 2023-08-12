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


class EmployeeSerializer(CustomUserSerializer):
    user_type = serializers.CharField(default="employee", write_only=True)


class CompanySerializer(CustomUserSerializer):
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
