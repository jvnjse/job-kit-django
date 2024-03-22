from rest_framework import serializers
from .models import (Company,
                     Company_Employee,
                     Organization,
                     JobDetail,
                     Department,)
from employee.models import Skill


class CompanySerializer(serializers.ModelSerializer):
    company_sectors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Company
        fields = "__all__"



class CompanyEmployeeSerializer(serializers.ModelSerializer):
    department_names = serializers.SerializerMethodField()
   

    class Meta:
        model = Company_Employee
        fields = ['id', 'employee_name', 'employee_position', 'employee_phone_number', 'employee_email','employee_department','company_user_id', 'department_names' ]
        read_only_fields = ['department_names']

    def get_department_names(self, obj):
        return [department.name for department in obj.employee_department.all()]    
    # class Meta:
    #     model = Company_Employee
    #     fields = "__all__"


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "company_name"]


class OrganisationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "organization_name"]


class JobPostingSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True, queryset=Skill.objects.all(), slug_field="name"
    )

    class Meta:
        model = JobDetail
        fields = "__all__"

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        job_detail = JobDetail.objects.create(**validated_data)

        if tags_data:
          for tag_name in tags_data:
              # Try to get the skill if it already exists, or create a new one
              skill, created = Skill.objects.get_or_create(name=tag_name)
              job_detail.tags.add(skill)
  
        return job_detail
    

# class EmployeeDepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Company_Employee
#         fields = ['employee_department']


class DepartmentSerializer(serializers.ModelSerializer):#extraa----------------
    class Meta:
        model = Department
        fields = '__all__'