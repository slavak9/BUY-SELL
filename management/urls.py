from django.urls import path, include
from .views import ManageCategory

urlpatterns = [
    path('', ManageCategory.as_view(), name='manage_category'),
]
