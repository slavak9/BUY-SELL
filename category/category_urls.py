
from django.urls import path, include, re_path
from .views import ShowCategory, Chosen_category

urlpatterns = [
    path('',ShowCategory.as_view(),name='category'),
    path('<slug:category_slug>/',Chosen_category.as_view(),name='chosen_category'),
    path('products/',include('products.products_urls')),

]




