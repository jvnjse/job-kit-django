from django.shortcuts import render
from .models import JobCategory
from .serializers import JobCategorySerializer

from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class JobCategoryView(APIView):
    def get(self, request):
        category = JobCategory.objects.all()
        serializer = JobCategorySerializer( category, many=True)
        return Response(serializer.data)