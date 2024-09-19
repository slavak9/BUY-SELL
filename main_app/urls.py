from django.urls import path, include, re_path
from .views import Home, support, news, about, logout_user

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('user_personal_area/', include('user_personal_area.urls')),
    path('category/', include('category.urls')),
    path('support/', support, name='support'),
    path('news/', news, name='news'),
    path('about/', about, name='about'),
    path('accounts/', include('accounts.urls')),
    path('shopping_cart/', include('shopping_cart.urls')),
    path('logout/', logout_user, name='logout'),
    path('management/', include('management.urls')),
]