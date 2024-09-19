from django.urls import path
from .views import Login, Register,forgotpassword

urlpatterns = [
    path('', Login.as_view(), name='accounts'),
    path('registration/', Register.as_view(), name='register'),
    path('forgot_password/', forgotpassword, name='forgot_password')

]