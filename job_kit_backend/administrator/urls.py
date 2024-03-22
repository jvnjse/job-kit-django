from django.urls import path
from .views import JobCategoryView
urlpatterns = [
    path('job-category/', JobCategoryView.as_view(), name='jobcategory'),
]
