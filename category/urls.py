
from django.urls import path, include
from .views import ShowCategory, ChosenCategory

urlpatterns = [
    path('', ShowCategory.as_view(), name='category'),
    path('<slug:category_slug>/', ChosenCategory.as_view(), name='chosen_category'),
    path('products/', include('products.urls')),
]




