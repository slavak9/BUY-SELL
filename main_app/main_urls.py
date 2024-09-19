from django.urls import path,include
from .views import home, support, news, about, login,cart

urlpatterns = [
    path('',home,name='home'),
    path('category/',include('category.category_urls')),
    path('support/',support,name='support'),
    path('news/',news,name='news'),
    path('about/',about,name='about'),
    path('login/',login,name='login'),
    path('shopping_cart',cart,name='cart')
]