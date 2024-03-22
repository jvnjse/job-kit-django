from rest_framework import serializers
from .models import (Company,
                     Company_Employee,
                     Organization,
                     JobDetail,
                     Department,)
from employee.models import Skill
from administrator.models import JobCategory


class CompanySerializer(serializers.ModelSerializer):
    company_sectors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Company
        fields = "__all__"



class CompanyEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company_Employee
        fields = "__all__"


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "company_name"]


class OrganisationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "organization_name"]


# class JobPostingSerializer(serializers.ModelSerializer):
#     tags = serializers.SlugRelatedField(
#         many=True, queryset=Skill.objects.all(), slug_field="name"
#     )

#     class Meta:
#         model = JobDetail
#         fields = "__all__"

#     def create(self, validated_data):
#         tags_data = validated_data.pop("tags", [])
#         job_detail = JobDetail.objects.create(**validated_data)

#         if tags_data:
#           for tag_name in tags_data:
#               # Try to get the skill if it already exists, or create a new one
#               skill, created = Skill.objects.get_or_create(name=tag_name)
#               job_detail.tags.add(skill)
  
#         return job_detail
        

    #reworked JobPostingSerializer by dhanoop
        
class JobPostingSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True, queryset=Skill.objects.all(), slug_field="name"
    )

    # Define a custom field for job category
    job_category = serializers.SlugRelatedField(
        queryset=JobCategory.objects.all(), slug_field="category_name"
    )

    class Meta:
        model = JobDetail
        fields = "__all__"

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        job_category_name = validated_data.pop("job_category", None)

        # Check if job category exists, if not, create it
        job_category, _ = JobCategory.objects.get_or_create(category_name=job_category_name)

        validated_data['job_category'] = job_category

        job_detail = JobDetail.objects.create(**validated_data)

        if tags_data:
            for tag_name in tags_data:
                skill, created = Skill.objects.get_or_create(name=tag_name)
                job_detail.tags.add(skill)

        return job_detail



    
    #reworked JobPostingSerializer by dhanoop
    

class EmployeeDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company_Employee
        fields = ['employee_department']


class DepartmentSerializer(serializers.ModelSerializer):#extraa----------------
    class Meta:
        model = Department
        fields = '__all__'