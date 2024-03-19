from django.shortcuts import render
import os
import pandas as pd
from rest_framework.decorators import api_view
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import (Company,
                     Company_Employee,
                     CompanyDepartment,
                     CompanySector,
                     Organization,
                     JobDetail,)

from authentication.models import CustomUser
from employee.models import Skill

from .serializers import (CompanySerializer,
                          CompanyEmployeeSerializer,
                          CompanyListSerializer,
                          OrganisationListSerializer,
                          JobPostingSerializer,
                          EmployeeDepartmentSerializer,)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView



# Create your views here.
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
        serializer = EmployeeDepartmentSerializer(company_employees, many=True)
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
       #------------------------------------------------------------
       
     

       if not skills:
            return Response(
                {"error": "Skills are required"}, status=status.HTTP_400_BAD_REQUEST
            )

       for skill_name in skills:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            # company_user .skills.add(skill)

        # return Response(
        #     {"message": "Skills added successfully"}, status=status.HTTP_201_CREATED
        # )
       #------------------------------------------------------------
       print(job_title, skills)
       job_detail = None
       serializer = None  # Initialize serializer variable here
       #------------------------------------------------------------------------------
       # uncommenting start
       #------------------------------------------------------------------------------
      # Moved the job creation logic outside the skills loop
       existing_job = JobDetail.objects.filter(
           company_user_id=user_id, job_title=job_title
       ).first()
   
       if existing_job:
           print("job already exist")
           serializer = JobPostingSerializer(existing_job, data=data)
       else:
       #---------------------------------------------------------------------------------
       # uncommenting end
       #----------------------------------------------------------------------------------  
            print("this block should not work if there is an existing job")
            data["company_user_id"] = user_id
            serializer = JobPostingSerializer(data=data)
   
       if serializer.is_valid():
           serializer.save()
           print("saved")
           job_detail = serializer.instance
   
       if job_detail:
           print("inside job detail")
           return Response({"message": "Job  created or updated", "data": serializer.data}, status=status.HTTP_201_CREATED)

       else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobGetingingUserAPI(APIView):
    def get(self, request, id):
        job_details = JobDetail.objects.filter(id=id)
        serializer = JobPostingSerializer(job_details, many=True)
        return Response(serializer.data)
    def put(self, request, id):
        try:
            job_detail = JobDetail.objects.get(id=id)
        except JobDetail.DoesNotExist:
            return Response({'message': 'Job detail not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        skills = data.get("tags", [])

        if not skills:
            return Response(
                {"error": "Skills are required"}, status=status.HTTP_400_BAD_REQUEST
            )

        for skill_name in skills:
            skill, created = Skill.objects.get_or_create(name=skill_name)

        serializer = JobPostingSerializer(job_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EmployeeDepartment(APIView):
    def get(self, request):
        employee_departments = Company_Employee.objects.filter(
            employee_department__isnull=False
        ).values_list('employee_department', flat=True).distinct()

        departments_list = [{'employee_department': dep} for dep in employee_departments]

        serializer = EmployeeDepartmentSerializer(data=departments_list, many=True)
        serializer.is_valid()
        return Response(serializer.data)