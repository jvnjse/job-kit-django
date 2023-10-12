import random
import string
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import (
    CustomUser,
    OTP,
    Employee,
    EmployeeEducation,
    Company,
    Skill,
    Organization,
)
from .serializers import (
    EmployeeregisterSerializer,
    CompanyregisterSerializer,
    AdminSerializer,
    OTPVerificationSerializer,
    EmployeeSerializer,
    CompanySerializer,
    LoginSerializer,
    EmployeeExperienceSerializer,
    EmployeeEducationSerializer,
    CompanyListSerializer,
    SkillSerializer,
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
            "employee": EmployeeregisterSerializer,
            "company": CompanyregisterSerializer,
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

                if user.is_verified:
                    response_data = {"message": "User is already verified"}
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

                user.is_verified = False

                if timezone.now() >= otp.expiry_time:
                    return Response(
                        {"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST
                    )

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


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# PERSONAL_INFO_EMPLOYEE
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------


class EmployeePersonalInfo(APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        try:
            employee = Employee.objects.get(user_id=user_id)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        try:
            employee = Employee.objects.get(user_id=user_id)
            serializer = EmployeeSerializer(employee, data=request.data)
        except Employee.DoesNotExist:
            serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        try:
            employee = Employee.objects.get(user_id=user_id)
            serializer = EmployeeSerializer(employee, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class EmployeeEducationView(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get("user_id", None)

        organization_name = data.get("organization", None)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                f"CustomUser with ID {user_id} not found.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        organization, created = Organization.objects.get_or_create(
            organization_name=organization_name
        )

        education = EmployeeEducation(
            user_id=user,
            course_job_name=data.get("course_job_name", None),
            organization_name=organization,
            from_date=data.get("from_date", None),
            to_date=data.get("to_date", None),
            education_document=data.get("education_document", None),
        )
        education.save()

        return Response(
            "EmployeeEducation created successfully.", status=status.HTTP_201_CREATED
        )

    # def post(self, request):
    #     serializer = EmployeeEducationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         organization_name = serializer.validated_data["organization_name"]
    #         organization, created = Organization.objects.get_or_create(
    #             organization_name=organization_name
    #         )
    #         serializer.save(organization_name=organization)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            employee_education = EmployeeEducation.objects.get(id=request.data["id"])
        except EmployeeEducation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeEducationSerializer(employee_education, data=request.data)

        if serializer.is_valid():
            organization_name = serializer.validated_data["organization_name"]
            organization, created = Organization.objects.get_or_create(
                organization_name=organization_name
            )
            serializer.save(organization_name=organization)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeExperienceView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        try:
            experience = EmployeeEducation.objects.filter(
                user_id=user_id, is_experience=True
            )
            serializer = EmployeeExperienceSerializer(experience, many=True)
            return Response(serializer.data)
        except EmployeeEducation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        request.data["is_experience"] = True
        serializer = EmployeeExperienceSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        try:
            experience = EmployeeEducation.objects.get(
                user_id=user_id, is_experience=True
            )
            serializer = EmployeeExperienceSerializer(
                experience, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployeeEducation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class EmployeeSkillsAPIView(APIView):
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
            serializer = SkillSerializer(data=request.data)
            print("sgcgavcgh")
            if serializer.is_valid():
                skill_name = serializer.validated_data["name"]
                skill, created = Skill.objects.get_or_create(name=skill_name)
                if created:
                    employee.skills.add(skill)
                else:
                    employee.skills.add(skill)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            if "name" in serializer.errors:
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
            serializer = SkillSerializer(data=request.data)
            if serializer.is_valid():
                skill_name = serializer.validated_data["name"]
                skill, created = Skill.objects.get_or_create(name=skill_name)
                employee.skills.add(skill)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# PERSONAL_INFO_COMPANY
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------


class CompanyPersonalInfo(APIView):
    def get(self, request, *args, **kwargs):
        company_user_id = kwargs["company_user_id"]
        try:
            company = Company.objects.get(company_user_id=company_user_id)
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        except Company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        company_user_id = kwargs["company_user_id"]
        try:
            company = Company.objects.get(company_user_id=company_user_id)
            serializer = CompanySerializer(company, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Company.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CompanyListView(APIView):
    def get(self, request, *args, **kwargs):
        companies = Company.objects.all()
        serializer = CompanyListSerializer(companies, many=True)
        return Response(serializer.data)


# class SampleAPI(APIView):
#     def get(self, request, *args, **kwargs):
#         # Retrieve all notes from the database
#         notes = Note.objects.all()
#         serializer = NoteSerializer(notes, many=True)
#         return Response(serializer.data)

#     def post(self, request, *args, **kwargs):
#         serializer = NoteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, *args, **kwargs):
#         try:
#             note = Note.objects.get(pk=kwargs["pk"])
#         except Note.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         serializer = NoteSerializer(note, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, *args, **kwargs):
#         try:
#             note = Note.objects.get(pk=kwargs["pk"])
#         except Note.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         note.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
