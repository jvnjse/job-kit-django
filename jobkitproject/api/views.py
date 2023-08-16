import random
import string
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import CustomUser, OTP
from .serializers import (
    EmployeeSerializer,
    CompanySerializer,
    AdminSerializer,
    OTPVerificationSerializer,
    LoginSerializer,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


from api.functions import send_otp_email, generate_otp


class RegistrationView(APIView):
    def post(self, request, user_type):
        if user_type not in ["employee", "company", "admin"]:
            return Response(
                {"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer_class = {
            "employee": EmployeeSerializer,
            "company": CompanySerializer,
            "admin": AdminSerializer,
        }[user_type]

        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            generated_otp = generate_otp()

            send_otp_email(user.id, user.email, generated_otp)

            response_data = {
                "message": "{user_type.capitalize()} registered successfully. Please verify using OTP.",
                "user": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerificationView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data["otp_code"]

            try:
                otp = OTP.objects.get(otp_code=otp_code)
                user = otp.user

                if user.is_verified:  # Check if the user is already verified
                    response_data = {"message": "User is already verified"}
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

                # Mark OTP as used
                user.is_verified = False

                if timezone.now() >= otp.expiry_time:
                    return Response(
                        {"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST
                    )

                # Mark the user as verified
                user.is_verified = True
                user.save()
                # refresh = RefreshToken.for_user(user)
                # access_token = str(refresh.access_token)

                response_data = {
                    "message": "OTP verification successful",
                    "access_token": access_token,
                    "refresh_token": str(refresh),
                }

                return Response(response_data, status=status.HTTP_200_OK)

            except OTP.DoesNotExist:
                return Response(
                    {"error": "Invalid OTP code"}, status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            if user is not None:
                if user.is_verified:
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)

                    response_data = {
                        "message": "Login successful",
                        "access_token": access_token,
                        "refresh_token": str(refresh),
                    }
                    return Response(response_data, status=status.HTTP_200_OK)

                else:
                    response_data = {"error": "User is not verified"}
                    return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
            else:
                response_data = {"error": "Invalid credentials"}
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
