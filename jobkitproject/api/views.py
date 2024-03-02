import random
import string
import pandas as pd
import os
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from api.functions import send_otp_email, generate_otp
from .models import (
    CustomUser,
    OTP,
    Employee,
    EmployeeEducation,
    EmployeeExperience,
    Company,
    Skill,
    Organization,
    Company_Employee,
    CompanySector,
    CompanyDepartment,
    JobDetail,
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
    OrganisationListSerializer,
    SkillSerializer,
    EmployeeSKillSerializer,
    CompanyEmployeeSerializer,
    JobPostingSerializer,
)


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
                "message": user_type.capitalize()
                + " registered successfully. Please verify using OTP.",
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
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                response_data = {
                    "user_id": user.id,
                    "message": "OTP verification successful",
                    "access_token": access_token,
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
                        "user": user.user_type,
                        "user_id": user.id,
                        "message": "Login successful",
                        "access_token": access_token,
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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.GET.get("user_id")
        try:
            education = EmployeeEducation.objects.filter(user_id=user_id)
            serializer = EmployeeEducationSerializer(education, many=True)
            return Response(serializer.data)
        except EmployeeEducation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = request.data
        user_id = data.get("user_id", None)
        organization_name = data.get("organization_name")

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

        education = EmployeeEducation.objects.filter(
            user_id=user, organization_name__organization_name=organization_name
        ).first()

        if education:
            education.course_name = data.get("course_name", education.course_name)
            education.from_date = data.get("from_date", education.from_date)
            education.to_date = data.get("to_date", education.to_date)
            education.course_description = data.get(
                "course_description", education.course_description
            )
            education.education_document = data.get(
                "education_document", education.education_document
            )
            education.save()
        else:
            organization, created = Organization.objects.get_or_create(
                organization_name=organization_name
            )
            education = EmployeeEducation(
                user_id=user,
                course_name=data.get("course_name", None),
                organization_name=organization,
                course_description=data.get("course_description", None),
                from_date=data.get("from_date", None),
                to_date=data.get("to_date", None),
                education_document=data.get("education_document", None),
            )
            education.save()

        return Response(
            "EmployeeEducation created or updated successfully.",
            status=status.HTTP_201_CREATED,
        )


class SingleEducationView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, education_id):
        try:
            education = EmployeeEducation.objects.get(id=education_id)
            serializer = EmployeeEducationSerializer(education)
            return Response(serializer.data)
        except EmployeeEducation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, education_id):
        try:
            education = EmployeeEducation.objects.get(id=education_id)
        except EmployeeEducation.DoesNotExist:
            return Response(
                "EmployeeEducation not found.", status=status.HTTP_404_NOT_FOUND
            )

        data = request.data
        user_id = data.get("user_id", None)
        organization_name = data.get("organization_name")

        if user_id:
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

        education.course_name = data.get("course_name", education.course_name)
        education.from_date = data.get("from_date", education.from_date)
        education.to_date = data.get("to_date", education.to_date)
        education.course_description = data.get(
            "course_description", education.course_description
        )

        if "education_document" in request.FILES:
            education.education_document = request.FILES["education_document"]

        education.user_id = user if user_id else education.user_id
        education.organization_name = organization
        education.save()

        serializer = EmployeeEducationSerializer(education)
        return Response(serializer.data)

    def delete(self, request, education_id):
        try:
            education = EmployeeEducation.objects.get(id=education_id)
            education.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EmployeeEducation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class EmployeeExperienceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.GET.get("id")
        try:
            experience = EmployeeExperience.objects.filter(user_id=user_id)
            serializer = EmployeeExperienceSerializer(experience, many=True)
            return Response(serializer.data)
        except EmployeeExperience.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = request.data
        user_id = data.get("user_id")
        company_name = data.get("company_name")

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                f"CustomUser with ID {user_id} not found.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        company, created = Company.objects.get_or_create(company_name=company_name)

        experience = EmployeeExperience.objects.filter(
            user_id=user, company_name__company_name=company_name
        ).first()

        if experience:
            experience.job_title = data.get("job_title", experience.job_title)
            experience.from_date = data.get("from_date", experience.from_date)
            experience.to_date = data.get("to_date", experience.to_date)
            experience.job_description = data.get(
                "job_description", experience.job_description
            )
            experience.experience_document = data.get(
                "experience_document", experience.experience_document
            )
            experience.save()
        else:
            company, created = Company.objects.get_or_create(company_name=company_name)
            experience = EmployeeExperience(
                user_id=user,
                job_title=data.get("job_title", None),
                company_name=company,
                job_description=data.get("job_description", None),
                from_date=data.get("from_date", None),
                to_date=data.get("to_date", None),
                experience_document=data.get("experience_document", None),
            )
            experience.save()

        return Response(
            "Employee Experience created or updated successfully.",
            status=status.HTTP_201_CREATED,
        )


class SingleExperienceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, experience_id):
        try:
            experience = EmployeeExperience.objects.get(id=experience_id)
            serializer = EmployeeExperienceSerializer(experience)
            return Response(serializer.data)
        except EmployeeExperience.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, experience_id):
        try:
            experience = EmployeeExperience.objects.get(id=experience_id)
        except EmployeeExperience.DoesNotExist:
            return Response(
                "EmployeeExperience not found.", status=status.HTTP_404_NOT_FOUND
            )

        data = request.data
        user_id = data.get("user_id", None)
        company_name = data.get("company_name")

        if user_id:
            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return Response(
                    f"CustomUser with ID {user_id} not found.",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        company, created = Company.objects.get_or_create(company_name=company_name)

        experience.job_title = data.get("job_title", experience.job_title)
        experience.from_date = data.get("from_date", experience.from_date)
        experience.to_date = data.get("to_date", experience.to_date)
        experience.job_description = data.get(
            "job_description", experience.job_description
        )
        experience.experience_document = data.get(
            "experience_document", experience.experience_document
        )
        experience.user_id = user if user_id else experience.user_id
        experience.company_name = company
        experience.save()

        serializer = EmployeeExperienceSerializer(experience)
        return Response(serializer.data)

    def delete(self, request, experience_id):
        try:
            experience = EmployeeExperience.objects.get(id=experience_id)
            experience.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EmployeeExperience.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class EmployeeSkillsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        employee = get_object_or_404(Employee, user_id=user_id)
        skills = employee.skills.all()
        skill_serializer = SkillSerializer(skills, many=True)
        return Response(skill_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        employee = get_object_or_404(Employee, user_id=user_id)
        skill_names = request.data.get("skills", [])

        if not skill_names:
            return Response(
                {"error": "Skills are required"}, status=status.HTTP_400_BAD_REQUEST
            )

        for skill_name in skill_names:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            employee.skills.add(skill)

        return Response(
            {"message": "Skills added successfully"}, status=status.HTTP_201_CREATED
        )

    def delete(self, request, user_id):
        employee = get_object_or_404(Employee, user_id=user_id)
        skill_name = request.data.get("skills")

        if skill_name:
            try:
                skill = Skill.objects.get(name=skill_name)
                employee.skills.remove(skill)
                return Response(
                    {"message": "Skill deleted successfully"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            except Skill.DoesNotExist:
                return Response(
                    {"error": "Skill not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "Skill name is required"}, status=status.HTTP_400_BAD_REQUEST
            )


# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# PERSONAL_INFO_COMPANY
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------


class CompanyPersonalInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            companies = Company.objects.filter(company_user_id=user_id)
            serializer = CompanySerializer(companies, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, user_id):
        data = request.data.copy()
        data["company_user_id"] = user_id

        existing_company = Company.objects.filter(company_user_id=user_id).first()

        if existing_company:
            serializer = CompanySerializer(existing_company, data=data)
        else:
            serializer = CompanySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def download_excel_file(request):
    file_path = os.path.join(settings.MEDIA_ROOT, "AddEmployeeExcel.xlsx")

    if os.path.exists(file_path):
        file_url = os.path.join(settings.MEDIA_URL, "AddEmployeeExcel.xlsx")
        return JsonResponse({"download_url": file_url})

    return JsonResponse({"error": "File not found"}, status=404)


@api_view(["POST"])
def import_data(request, company_user_id):
    try:
        excel_file = request.FILES["excel_file"]
        df = pd.read_excel(excel_file)
        data = df.to_dict("records")

        for record in data:
            record["company_user_id"] = company_user_id

        serializer = CompanyEmployeeSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response(
            "Excel file not found in the request.", status=status.HTTP_400_BAD_REQUEST
        )


class CompanyEmployeeAPIView(APIView):
    def get(self, request, company_user_id):
        company_employees = Company_Employee.objects.filter(
            company_user_id=company_user_id
        )
        serializer = CompanyEmployeeSerializer(company_employees, many=True)
        return Response(serializer.data)

    def post(self, request, company_user_id):
        data = request.data
        data["company_user_id"] = company_user_id
        serializer = CompanyEmployeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateSectorAndDepartments(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        sectors = request.data.get("sectors", [])
        departments = request.data.get("departments", [])

        try:
            user = Company.objects.get(company_user_id=user_id)
        except CustomUser.DoesNotExist:
            return Response("User not found.", status=status.HTTP_404_NOT_FOUND)

        for sector_name in sectors:
            sector, _ = CompanySector.objects.get_or_create(sector_name=sector_name)
            user.company_sectors.add(sector)

        for department_data in departments:
            sector_name = department_data.get("sector_name")
            department_name = department_data.get("department_name")

            sector, _ = CompanySector.objects.get_or_create(sector_name=sector_name)
            department, _ = CompanyDepartment.objects.get_or_create(
                sector=sector,
                department_name=department_name,
            )

        return Response(
            f"Sectors and departments updated for user ID {user_id}.",
            status=status.HTTP_200_OK,
        )


class CompanyListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        companies = Company.objects.filter(is_verified=True)
        serializer = CompanyListSerializer(companies, many=True)
        return Response(serializer.data)


class OrganisationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        organizations = Organization.objects.filter(is_verified=True)
        serializer = OrganisationListSerializer(organizations, many=True)
        return Response(serializer.data)


class JobPostingUserAPI(APIView):
    def get(self, request, user_id):
        job_details = JobDetail.objects.filter(company_user_id=user_id)
        serializer = JobPostingSerializer(job_details, many=True)
        return Response(serializer.data)

    def post(self, request, user_id):
        data = request.data
        job_title = data.get("job_title")

        company_user = get_object_or_404(CustomUser, pk=user_id)
        skills = data.get("tags", [])

        job_detail = None
        for skill_name in skills:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            if job_detail is None:
                existing_job = JobDetail.objects.filter(
                    company_user_id=user_id, job_title=job_title
                ).first()

                if existing_job:
                    serializer = JobPostingSerializer(existing_job, data=data)
                else:
                    data["company_user_id"] = user_id
                    serializer = JobPostingSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                    job_detail = serializer.instance

        if job_detail:
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
