from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import (Employee,
                     EmployeeEducation,
                     EmployeeExperience,
                     Skill,)

from administrator.models import JobCategory
from authentication.models import CustomUser
from company.models import Organization, Company

from .serializers import (EmployeeSerializer,
                          EmployeeEducationSerializer,
                          EmployeeExperienceSerializer,
                          SkillSerializer,)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
class EmployeePersonalInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        print("Logged-in user's id:", user_id)  # For debugging
        try:
            employee = Employee.objects.get(user_id=user_id)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

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
        print("Requested user_id:", user_id)
        employee = get_object_or_404(Employee, user_id=user_id)
        print("Found employee:", employee)
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
        
class JobCategoryCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        category_id = request.data.get("category_id")
        if not category_id:
            return Response({"error": "Category ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the selected job category
            job_category = JobCategory.objects.get(id=category_id)
        except JobCategory.DoesNotExist:
            return Response({"error": "Job category does not exist"}, status=status.HTTP_404_NOT_FOUND)

      
        user = request.user

        try:
            # Check if there's an employee associated with the logged-in user
            employee = Employee.objects.get(user_id=user.id)
            # Associate the job category with the employee
            employee.job_category = job_category
            employee.save()
            return Response({"message": "Job category selected successfully"}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
class JobCategoryUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        category_id = request.data.get("category_id")
        if not category_id:
            return Response({"error": "Category ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the selected job category
            job_category = JobCategory.objects.get(id=category_id)
        except JobCategory.DoesNotExist:
            return Response({"error": "Job category does not exist"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        try:
            # Check if there's an employee associated with the logged-in user
            employee = Employee.objects.get(user_id=user.id)
            # Update the job category associated with the employee
            employee.job_category = job_category
            employee.save()
            return Response({"message": "Job category updated successfully"}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
