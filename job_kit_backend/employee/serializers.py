from rest_framework import serializers
from .models import (
    Skill,
    Employee,
    EmployeeExperience,
    EmployeeEducation,
)


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    skills = serializers.StringRelatedField(many=True)
    job_category_name = serializers.SerializerMethodField()

    def get_job_category_name(self, obj):
        if obj.job_category:
            return obj.job_category.category_name
        return None

    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeSKillSerializer(serializers.ModelSerializer):
    skills = serializers.StringRelatedField(many=True)

    class Meta:
        model = Employee
        fields = ["user_id", "skills"]


class EmployeeExperienceSerializer(serializers.ModelSerializer):
    experience_document = serializers.FileField(use_url=False)

    class Meta:
        model = EmployeeExperience
        fields = [
            "id",
            "user_id",
            "job_title",
            "job_description",
            "company_name",
            "from_date",
            "to_date",
            "experience_document",
        ]


class EmployeeEducationSerializer(serializers.ModelSerializer):
    education_document = serializers.FileField(use_url=False)

    class Meta:
        model = EmployeeEducation
        fields = [
            "id",
            "user_id",
            "course_name",
            "course_description",
            "organization_name",
            "from_date",
            "to_date",
            "education_document",
        ]



